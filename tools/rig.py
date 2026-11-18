"""Bộ khung nhân vật hoạt hình v2 cho chuỗi Bộp và Gầm — tỉ lệ chibi, tay chân IK, co giãn, biểu cảm phong phú,
chuyển động phụ (râu, tóc, vạt áo theo quán tính), nhép miệng theo âm lượng giọng ú ớ.

Mọi thứ là hàm thuần của thời gian: cảnh gọi draw_char(c, Pose(...)) cho mỗi khung hình.
"""
import math
from dataclasses import dataclass, field
import skia

OUT = "#2A1D16"


def P(color, a=255, stroke=None):
    h = color.lstrip("#")
    p = skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(int(max(0, min(255, a))), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def fo(c, path, fill, ow=7, a=255):
    c.drawPath(path, P(fill, a)); c.drawPath(path, P(OUT, a, stroke=ow))


def oval(cx, cy, rx, ry):
    p = skia.Path(); p.addOval(skia.Rect.MakeXYWH(cx - rx, cy - ry, 2 * rx, 2 * ry)); return p


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, p):
    return a + (b - a) * p


def ease_out(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = clamp(x); return 3 * x * x - 2 * x * x * x


def back_out(x, k=1.8):
    x = clamp(x) - 1; return 1 + x * x * ((k + 1) * x + k)


def noise1(t, seed=0.0):
    """Nhiễu mượt 1 chiều (tổng sin), dùng cho đung đưa tự nhiên."""
    return (math.sin(t * 1.3 + seed) * 0.5 + math.sin(t * 2.7 + seed * 1.7) * 0.3 + math.sin(t * 5.1 + seed * 2.3) * 0.2)


def blink_amt(t, seed=0.0):
    """Chớp mắt không đều: trả về độ mở mắt 0..1."""
    period = 2.6 + 1.4 * (0.5 + 0.5 * math.sin(seed * 3.1))
    ph = (t + seed * 0.77) % period
    if ph < 0.06:
        return 1 - ph / 0.06
    if ph < 0.12:
        return (ph - 0.06) / 0.06
    # thỉnh thoảng chớp đôi
    if math.sin(seed * 5 + int((t + seed * 0.77) / period)) > 0.6 and 0.18 < ph < 0.3:
        return abs((ph - 0.24) / 0.06)
    return 1.0


def spring(f, t, freq=6.0, damp=4.0, window=0.9, n=36):
    """Độ trễ đàn hồi của một đại lượng f(t) (dùng cho râu/tóc/vạt áo): tích chập vận tốc với dao động tắt dần."""
    acc = 0.0
    dt = window / n
    for i in range(n):
        tau = (i + 0.5) * dt
        v = (f(t - tau + dt / 2) - f(t - tau - dt / 2)) / dt
        acc += -v * math.exp(-damp * tau) * math.sin(2 * math.pi * freq * tau) / (2 * math.pi * freq) * dt * (2 * math.pi * freq)
    return acc


def ik2(sx, sy, tx, ty, l1, l2, bend=1):
    """IK 2 đoạn: trả về vị trí khớp giữa (khuỷu/gối)."""
    dx, dy = tx - sx, ty - sy
    d = max(1e-3, min(l1 + l2 - 0.01, math.hypot(dx, dy)))
    a = math.atan2(dy, dx)
    cosb = clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1)
    b = math.acos(cosb)
    ang = a - bend * b
    return sx + l1 * math.cos(ang), sy + l1 * math.sin(ang)


def limb_path(c, pts, width, fill):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p, P(OUT, stroke=width + 14)); c.drawPath(p, P(fill, stroke=width))


# ---------------------------------------------------------------------- phong cách nhân vật
STYLES = {
    "bop": dict(skin="#8A5A3C", skin_d="#6E452C", hair="#1F1712", tunic="#8A6A44", tunic_d="#6B5032", fur="#C9B48A",
                head=(118, 128), torso_w=150, torso_h=170, leg=78, arm=(78, 72), nose="small", beard=False, eye_scale=1.08,
                brow_w=11),
    "gam": dict(skin="#C8946A", skin_d="#A87650", hair="#5A3E2A", tunic="#7A5A3A", tunic_d="#5E4430", fur="#B9A37A",
                head=(134, 118), torso_w=196, torso_h=160, leg=70, arm=(82, 74), nose="big", beard=True, eye_scale=0.92,
                brow_w=17),
}


@dataclass
class Pose:
    who: str = "bop"
    x: float = 540
    y: float = 1300
    s: float = 1.0
    t: float = 0.0
    face: int = 1                 # 1 nhìn sang phải, -1 sang trái
    turn: float = 0.35            # 0 nhìn thẳng .. 1 nhìn nghiêng (dịch nét mặt)
    squash: float = 1.0           # <1 bẹp, >1 dài
    lean: float = 0.0             # độ nghiêng thân (độ)
    head_tilt: float = 0.0
    head_dx: float = 0.0
    head_dy: float = 0.0
    head_squash: float = 1.0
    # tay: vị trí bàn tay so với vai (đơn vị khung), None = buông
    hand_l: tuple = None
    hand_r: tuple = None
    hold: str = None              # "stick" / "spear" ở tay phải
    hold_ang: float = 0.0         # góc vật cầm (độ, 0 = dựng đứng)
    hold_len: float = 420
    hold_side: str = "r"          # "r" tay trước, "l" tay sau (vật nằm sau thân)
    # chân
    walk: float = None            # pha bước
    stride: float = 1.0
    crouch: float = 0.0           # 0..1 khuỵu gối
    feet_air: float = 0.0         # nhấc chân khi nhảy
    # mặt
    eyes: str = "open"            # open / wide / squint / happy / closed / dizzy / angry
    look: tuple = (0.0, 0.0)
    brow: float = 0.0             # nâng(+)/hạ(-)
    brow_tilt: float = 0.0        # + giận (trong hạ), - lo lắng
    mouth: str = "flat"           # flat / smile / grin / frown / smirk / o / shout / wavy / tongue
    talk: float = 0.0             # độ mở miệng 0..1 (theo âm lượng)
    blush: float = 0.0
    sweat: float = 0.0
    vein: float = 0.0
    lag: float = 0.0              # độ trễ đàn hồi (râu/tóc/vạt áo)
    alpha: float = 1.0


def _hide_tunic(c, st, w, h, lag):
    top, bot = -150 - h, -150
    p = skia.Path()
    p.moveTo(-w / 2 + 6, top); p.lineTo(w / 2 - 6, top)
    p.quadTo(w / 2 + 14, (top + bot) / 2, w / 2 + 8 + lag * 0.4, bot + 20)
    # gấu răng cưa
    n = 6
    for k in range(n, -1, -1):
        px = -w / 2 - 8 + lag * 0.4 + (w + 16) * k / n
        py = bot + (34 if k % 2 else 18)
        p.lineTo(px, py)
    p.quadTo(-w / 2 - 14, (top + bot) / 2, -w / 2 + 6, top)
    p.close()
    c.drawPath(p, P(st["tunic"]))
    c.save(); c.clipPath(p, skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeXYWH(w * 0.12, top, w, h + 60), P(st["tunic_d"], 120))
    c.drawLine(-w * 0.32, top + 20, w * 0.18, bot - 10, P(st["tunic_d"], stroke=7))
    c.restore()
    c.drawPath(p, P(OUT, stroke=7))
    fur = skia.Path(); fur.moveTo(-w / 2 + 2, top + 6)
    for k in range(8):
        fur.quadTo(-w / 2 + 2 + (w - 4) * (k + 0.5) / 8, top - (22 if k % 2 else 12), -w / 2 + 2 + (w - 4) * (k + 1) / 8, top + 6)
    fur.close(); fo(c, fur, st["fur"], ow=5)


def _eye(c, ex, ey, rw, rh, kind, look, openness, t, side):
    if kind == "happy":
        p = skia.Path(); p.moveTo(ex - rw, ey + rh * 0.2); p.quadTo(ex, ey - rh * 1.0, ex + rw, ey + rh * 0.2)
        c.drawPath(p, P(OUT, stroke=9)); return
    if kind == "closed" or openness < 0.12:
        c.drawLine(ex - rw * 0.9, ey, ex + rw * 0.9, ey, P(OUT, stroke=8)); return
    if kind == "dizzy":
        c.drawOval(skia.Rect.MakeXYWH(ex - rw, ey - rh, 2 * rw, 2 * rh), P("#FFFFFF"))
        c.drawOval(skia.Rect.MakeXYWH(ex - rw, ey - rh, 2 * rw, 2 * rh), P(OUT, stroke=5))
        sp = skia.Path()
        for k in range(40):
            a = k * 0.45 + t * 9 * side
            r = rw * 0.85 * k / 40
            (sp.moveTo if k == 0 else sp.lineTo)(ex + r * math.cos(a), ey + r * math.sin(a) * rh / rw)
        c.drawPath(sp, P(OUT, stroke=5)); return
    h = rh * openness
    if kind == "squint":
        h *= 0.45
    if kind == "wide":
        rw *= 1.18; h *= 1.18
    c.drawOval(skia.Rect.MakeXYWH(ex - rw, ey - h, 2 * rw, 2 * h), P("#FFFFFF"))
    c.save(); c.clipRect(skia.Rect.MakeXYWH(ex - rw, ey - h, 2 * rw, 2 * h))
    pr = rw * (0.34 if kind == "wide" else 0.5)
    px, py = ex + look[0] * rw * 0.45, ey + look[1] * h * 0.4
    c.drawCircle(px, py, pr, P(OUT))
    c.drawCircle(px + pr * 0.35, py - pr * 0.4, pr * 0.32, P("#FFFFFF"))
    c.restore()
    c.drawOval(skia.Rect.MakeXYWH(ex - rw, ey - h, 2 * rw, 2 * h), P(OUT, stroke=5))
    if kind == "angry":
        lid = skia.Path(); lid.moveTo(ex - rw - 4, ey - h - 4); lid.lineTo(ex + rw + 4, ey - h - 4)
        lid.lineTo(ex + rw * side * 0.9 * -1 + 0, ey - h * 0.1)
        lid.close()


def _mouth(c, mx, my, rx, kind, talk, t, st):
    o = clamp(talk)
    if o > 0.06 or kind in ("o", "shout"):
        if kind == "shout":
            o = max(o, 0.65)
        if kind == "o":
            o = max(o, 0.5)
        w = rx * (0.30 + 0.18 * o) * (1.25 if kind in ("shout", "grin") else 1.0)
        h = rx * (0.06 + 0.34 * o)
        p = skia.Path()
        if kind == "shout":
            p.moveTo(mx - w, my - h * 0.4); p.lineTo(mx + w, my - h * 0.5); p.quadTo(mx + w * 0.7, my + h * 1.1, mx, my + h * 1.1)
            p.quadTo(mx - w * 0.7, my + h * 1.1, mx - w, my - h * 0.4); p.close()
        else:
            p.addOval(skia.Rect.MakeXYWH(mx - w, my - h, 2 * w, 2 * h))
        fo(c, p, "#5A1E16", ow=5)
        c.save(); c.clipPath(p, skia.ClipOp.kIntersect, True)
        c.drawOval(skia.Rect.MakeXYWH(mx - w * 0.6, my + h * 0.2, w * 1.2, h * 1.2), P("#D9646B"))
        if kind in ("shout", "grin"):
            c.drawRect(skia.Rect.MakeXYWH(mx - w, my - h * 1.2, 2 * w, h * 0.45), P("#FFFFFF"))
        c.restore()
        c.drawPath(p, P(OUT, stroke=5))
        return
    if kind == "smile":
        p = skia.Path(); p.moveTo(mx - rx * 0.28, my - 6); p.quadTo(mx, my + rx * 0.22, mx + rx * 0.28, my - 6); c.drawPath(p, P(OUT, stroke=7))
    elif kind == "grin":
        p = skia.Path(); p.moveTo(mx - rx * 0.36, my - 10); p.quadTo(mx, my + rx * 0.3, mx + rx * 0.36, my - 10); p.close()
        fo(c, p, "#FFFFFF", ow=6)
        for k in range(1, 4):
            x = mx - rx * 0.36 + rx * 0.72 * k / 4
            c.drawLine(x, my - 8, x, my + rx * 0.1, P(OUT, stroke=3))
    elif kind == "frown":
        p = skia.Path(); p.moveTo(mx - rx * 0.24, my + 10); p.quadTo(mx, my - rx * 0.14, mx + rx * 0.24, my + 10); c.drawPath(p, P(OUT, stroke=7))
    elif kind == "smirk":
        p = skia.Path(); p.moveTo(mx - rx * 0.2, my + 4); p.quadTo(mx + rx * 0.1, my + 8, mx + rx * 0.3, my - 12); c.drawPath(p, P(OUT, stroke=7))
    elif kind == "wavy":
        p = skia.Path(); p.moveTo(mx - rx * 0.3, my)
        for k in range(6):
            p.quadTo(mx - rx * 0.3 + rx * 0.6 * (k + 0.5) / 6, my + (10 if k % 2 else -10), mx - rx * 0.3 + rx * 0.6 * (k + 1) / 6, my)
        c.drawPath(p, P(OUT, stroke=6))
    elif kind == "tongue":
        c.drawLine(mx - rx * 0.24, my, mx + rx * 0.24, my, P(OUT, stroke=7))
        fo(c, oval(mx + rx * 0.08, my + 18, 16, 22), "#D9646B", ow=5)
    else:
        c.drawLine(mx - rx * 0.2, my, mx + rx * 0.2, my + 2, P(OUT, stroke=7))


def _head(c, st, p, rx, ry):
    hx, hy = 0.0, 0.0
    ft = p.turn
    t = p.t
    # tóc sau / râu
    if p.who == "gam":
        hair = skia.Path(); hair.moveTo(-rx - 6, -ry * 0.05)
        for k in range(17):
            a = math.pi + k * math.pi / 16
            r = 1.07 + (0.07 if k % 2 else 0)
            px_, py_ = rx * r * math.cos(a) - p.lag * 0.3 * (k / 16), ry * r * math.sin(a) - 6
            if k == 0:
                hair.lineTo(px_, py_)
            else:
                hair.quadTo(rx * (r + 0.1) * math.cos(a - math.pi / 32), ry * (r + 0.1) * math.sin(a - math.pi / 32) - 6, px_, py_)
        hair.lineTo(rx + 6, -ry * 0.05); hair.close()
        fo(c, hair, st["hair"], ow=6)
    head = oval(hx, hy, rx, ry)
    fo(c, head, st["skin"], ow=8)
    c.save(); c.clipPath(head, skia.ClipOp.kIntersect, True)
    c.drawCircle(rx * 0.55, ry * 0.35, rx * 0.9, P(st["skin_d"], 90))
    c.restore(); c.drawPath(head, P(OUT, stroke=8))
    # tóc trước
    if p.who == "bop":
        hp = skia.Path(); hp.moveTo(-rx * 0.95, -ry * 0.25)
        hp.quadTo(-rx * 0.9, -ry * 1.15, 0, -ry * 1.08)
        hp.quadTo(rx * 0.9, -ry * 1.15, rx * 0.95, -ry * 0.25)
        for k in range(5, -1, -1):
            px = -rx * 0.95 + rx * 1.9 * k / 5
            hp.lineTo(px + p.lag * 0.15, -ry * (0.55 if k % 2 else 0.4))
        hp.close()
        fo(c, hp, st["hair"], ow=6)
        tuft = skia.Path(); tuft.moveTo(-10, -ry * 1.04); tuft.quadTo(-6 - p.lag * 0.6, -ry * 1.45, 26 - p.lag * 0.8, -ry * 1.38)
        tuft.quadTo(10, -ry * 1.2, 14, -ry * 1.04); tuft.close(); fo(c, tuft, st["hair"], ow=5)
    else:
        bang = skia.Path(); bang.moveTo(-rx * 0.9, -ry * 0.35)
        bang.quadTo(0, -ry * 0.75 + p.lag * 0.05, rx * 0.9, -ry * 0.35); bang.lineTo(rx * 0.75, -ry * 0.62); bang.quadTo(0, -ry * 1.05, -rx * 0.75, -ry * 0.62); bang.close()
        fo(c, bang, st["hair"], ow=5)
    fx = ft * rx * 0.28 * p.face
    # má hồng
    if p.blush > 0:
        for sd in (-1, 1):
            c.drawOval(skia.Rect.MakeXYWH(fx + sd * rx * 0.55 - 26, ry * 0.18 - 12, 52, 24), P("#E8746B", 160 * p.blush))
    # mắt
    es = st["eye_scale"]
    rw, rh = rx * 0.21 * es, ry * 0.25 * es
    openness = blink_amt(t, 1.3 if p.who == "gam" else 0.4) if p.eyes in ("open", "wide", "squint", "angry") else 1.0
    lk = (p.look[0] * p.face, p.look[1])
    for sd in (-1, 1):
        ex = fx + sd * rx * 0.36 * (1 - 0.18 * ft * (1 if sd == p.face else -1) * 0)
        ey = -ry * 0.08
        _eye(c, ex, ey, rw, rh, p.eyes, lk, openness, t, sd)
        # lông mày
        by = ey - rh - 16 - p.brow * 14
        tilt = p.brow_tilt * 16
        inner, outer = (ex - sd * rw * 1.0, ex + sd * rw * 1.0) if True else (0, 0)
        x_in, x_out = ex - sd * rw * 0.95, ex + sd * rw * 1.05
        c.drawLine(x_in, by + tilt, x_out, by - tilt * 0.6, P(OUT, stroke=st["brow_w"]))
    if p.who == "gam":
        rid = skia.Path(); rid.moveTo(fx - rx * 0.72, -ry * 0.36 - p.brow * 10); rid.quadTo(fx, -ry * 0.55 - p.brow * 14, fx + rx * 0.72, -ry * 0.36 - p.brow * 10)
        c.drawPath(rid, P(st["skin_d"], 140, stroke=10))
    # mũi
    nx, ny = fx + ft * rx * 0.1 * p.face, ry * 0.18
    if st["nose"] == "big":
        fo(c, oval(nx, ny, rx * 0.17, ry * 0.15), st["skin"], ow=6)
        c.drawCircle(nx + rx * 0.06, ny - 4, 6, P("#FFFFFF", 90))
    else:
        np_ = skia.Path(); np_.moveTo(nx, ny - 20); np_.quadTo(nx + 14 * p.face, ny + 6, nx - 2 * p.face, ny + 10)
        c.drawPath(np_, P(OUT, stroke=6))
    # râu (Gầm) — có trễ đàn hồi
    my = ry * 0.52
    if st["beard"]:
        bd = skia.Path(); bd.moveTo(fx - rx * 0.78, ry * 0.12)
        bd.quadTo(fx - rx * 0.7, ry * 1.05, fx + p.lag * 0.5, ry * 1.18 + abs(p.lag) * 0.1)
        bd.quadTo(fx + rx * 0.7, ry * 1.05, fx + rx * 0.78, ry * 0.12)
        bd.quadTo(fx + rx * 0.4, ry * 0.4, fx, ry * 0.36); bd.quadTo(fx - rx * 0.4, ry * 0.4, fx - rx * 0.78, ry * 0.12); bd.close()
        fo(c, bd, st["hair"], ow=6)
        mus = skia.Path(); mus.moveTo(fx - rx * 0.32, my - 6); mus.quadTo(fx, my - 30, fx + rx * 0.32, my - 6); mus.quadTo(fx, my - 14, fx - rx * 0.32, my - 6); mus.close()
        fo(c, mus, st["hair"], ow=5)
    _mouth(c, fx + ft * rx * 0.06 * p.face, my + (6 if st["beard"] else 0), rx, p.mouth, p.talk, t, st)
    # mồ hôi, gân tức
    if p.sweat > 0:
        sx, sy = -rx * 0.95 * p.face, -ry * 0.4 + (t * 160 % 60)
        d = skia.Path(); d.moveTo(sx, sy - 26); d.quadTo(sx + 18, sy + 4, sx, sy + 14); d.quadTo(sx - 18, sy + 4, sx, sy - 26); d.close()
        fo(c, d, "#9FD3F0", ow=4, a=255 * p.sweat)
    if p.vein > 0:
        vx, vy = rx * 0.55 * p.face, -ry * 0.75
        for a in range(4):
            ang = a * math.pi / 2 + 0.6
            c.drawLine(vx + 8 * math.cos(ang), vy + 8 * math.sin(ang), vx + 26 * math.cos(ang), vy + 26 * math.sin(ang), P("#C0392B", 255 * p.vein, stroke=7))


def draw_char(c, p: Pose):
    st = STYLES[p.who]
    rx, ry = st["head"]
    tw_, th_ = st["torso_w"], st["torso_h"]
    t = p.t
    breathe = 1 + 0.018 * math.sin(t * 2.4 + (1 if p.who == "gam" else 0))
    c.save()
    if p.alpha < 0.999:
        c.saveLayerAlpha(None, int(255 * clamp(p.alpha)))
    c.translate(p.x, p.y); c.scale(p.s, p.s)
    c.scale(p.face, 1)
    # bóng đổ
    c.drawOval(skia.Rect.MakeXYWH(-120, -14, 240, 28), P("#000000", 50 * (1 - 0.5 * p.feet_air / 100)))
    sq = p.squash
    c.save()
    c.scale(1 / math.sqrt(sq), sq)
    crouch_drop = p.crouch * 60
    lift = -p.feet_air
    c.translate(0, lift)
    # chân (IK)
    hip_y = -150 + crouch_drop
    L = st["leg"]
    for sd in (-1, 1):
        hx = sd * tw_ * 0.22
        if p.walk is not None:
            ph = p.walk + (0 if sd < 0 else math.pi)
            fx = hx + 46 * p.stride * math.sin(ph)
            fy = -max(0.0, math.cos(ph)) * 34 * p.stride
        else:
            fx, fy = hx + sd * 8 * (1 + p.crouch), 0
        if p.feet_air > 0:
            fy = -min(60, p.feet_air * 0.4)
            fx = hx + sd * 10
        kx, ky = ik2(hx, hip_y, fx, fy - 10, L, L, bend=1)
        if ky > hip_y + L * 1.9:
            ky = hip_y + L
        limb_path(c, [(hx, hip_y), (kx, ky), (fx, fy - 10)], 40, st["skin"])
        fo(c, skia.Path().addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(fx - 30, fy - 30, 66, 32), 14, 14)) or skia.Path(), st["tunic_d"], ow=5)
    # thân
    c.save()
    c.translate(0, hip_y); c.rotate(p.lean); c.scale(1, breathe); c.translate(0, -hip_y + crouch_drop * 0)
    c.translate(0, crouch_drop)
    # tay sau (trái)
    sh_y = -150 - th_ + 22
    al, af = st["arm"]

    def arm(sd, hand, behind):
        sx = sd * (tw_ / 2 - 10)
        if hand is None:
            sw = 10 * math.sin(t * 2.4 + sd)
            if p.walk is not None:
                sw = 34 * math.sin(p.walk + (math.pi if sd > 0 else 0))
            tx, ty = sx + sd * 14 + sw * 0.6, sh_y + (al + af) * 0.93
        else:
            tx, ty = sx + hand[0], sh_y + hand[1]
        ex, ey = ik2(sx, sh_y, tx, ty, al, af, bend=-1 if sd > 0 else 1)
        limb_path(c, [(sx, sh_y), (ex, ey), (tx, ty)], 34, st["skin"])
        fo(c, oval(tx, ty, 26, 24), st["skin"], ow=6)
        return tx, ty

    # vật cầm (sau tay phải)
    hl = arm(-1, p.hand_l, True)
    if p.hold and p.hold_side == "l":
        _held(c, hl, p)
    _hide_tunic(c, st, tw_, th_, p.lag)
    # đầu
    c.save()
    c.translate(p.head_dx, sh_y - ry * 0.98 + p.head_dy)
    c.rotate(p.head_tilt)
    c.scale(1 / math.sqrt(p.head_squash), p.head_squash)
    _head(c, st, p, rx, ry)
    c.restore()
    hr = arm(1, p.hand_r, False)
    if p.hold and p.hold_side == "r":
        _held(c, hr, p)
    c.restore()  # thân
    c.restore()  # co giãn
    if p.alpha < 0.999:
        c.restore()
    c.restore()
    return hr


def _held(c, hand, p):
    hx, hy = hand
    with_s = 1.0
    c.save(); c.translate(hx, hy); c.rotate(p.hold_ang)
    L = p.hold_len
    c.drawLine(0, 120, 0, -L + 120, P(OUT, stroke=26)); c.drawLine(0, 120, 0, -L + 120, P("#8A6A44", stroke=17))
    if p.hold == "spear":
        tip = skia.Path(); tip.moveTo(-24, -L + 130); tip.lineTo(0, -L + 20); tip.lineTo(24, -L + 130); tip.close()
        fo(c, tip, "#9AA3A8", ow=5)
        fo(c, skia.Path().addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-15, -L + 120, 30, 36), 8, 8)) or skia.Path(), "#C98A2A", ow=4)
    # tay nắm phủ lên cán
    c.restore()
    fo(c, oval(hx, hy, 26, 24), STYLES[p.who]["skin"], ow=6)


# ---------------------------------------------------------------------- lợn rừng v2
def draw_boar(c, x, y, s, t, face=1, mood="calm", run=None, big=False, root=0.0, turn_head=0.0, eyes_cross=0.0,
              paw=0.0, squash=1.0, snort=0.0, alpha=1.0, lag=0.0):
    """Lợn rừng có thở, vẫy đuôi, vẫy tai, cúi ủi đất, cào chân, phì hơi."""
    S_ = s * (1.4 if big else 1.0)
    c.save()
    if alpha < 0.999:
        c.saveLayerAlpha(None, int(255 * alpha))
    c.translate(x, y); c.scale(S_ * face, S_)
    c.drawOval(skia.Rect.MakeXYWH(-180, -10, 360, 26), P("#000000", 50))
    c.scale(1 / math.sqrt(squash), squash)
    body_c, dark = ("#6B4A34", "#4E3424") if not big else ("#5A3E2C", "#3E2A1E")
    br = 1 + 0.03 * math.sin(t * 3)
    ph = run if run is not None else 0
    for k, lx in enumerate([-110, -60, 60, 110]):
        a = (32 * math.sin(ph + k * 1.6) if run is not None else 0) + (paw * 35 * max(0, math.sin(t * 14)) if k == 3 else 0)
        c.save(); c.translate(lx, -96); c.rotate(-a)
        c.drawLine(0, 0, 0, 74, P(OUT, stroke=32)); c.drawLine(0, 0, 0, 74, P(dark, stroke=21))
        fo(c, skia.Path().addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-16, 64, 32, 20), 6, 6)) or skia.Path(), "#2E2018", ow=4)
        c.restore()
    c.save(); c.scale(1, br)
    body = oval(-20, -140, 180, 88)
    fo(c, body, body_c, ow=7)
    c.save(); c.clipPath(body, skia.ClipOp.kIntersect, True); c.drawCircle(60, -80, 150, P(dark, 80)); c.restore()
    for k in range(10):
        bx = -170 + k * 30
        c.drawLine(bx, -210 + abs(k - 5) * 4, bx + 12 - lag * 0.2, -245 + abs(k - 5) * 6, P(OUT, stroke=6))
    # đuôi vẫy
    tw = math.sin(t * 9) * 20
    tl = skia.Path(); tl.moveTo(-195, -160); tl.cubicTo(-240, -190 + tw, -210, -220 + tw, -240, -230 + tw)
    c.drawPath(tl, P(OUT, stroke=6))
    c.restore()
    # đầu (cúi ủi đất / quay đầu)
    hd = root * 30 * (0.5 + 0.5 * math.sin(t * 10)) if root > 0 else 0
    c.save(); c.translate(130, -150); c.rotate(hd + turn_head * -10)
    head = skia.Path(); head.moveTo(-30, -40); head.lineTo(110, 0); head.lineTo(132, 46); head.lineTo(20, 80); head.lineTo(-40, 50); head.close()
    fo(c, head, body_c, ow=7)
    fo(c, oval(132, 26, 22, 30), "#C98A80", ow=5)
    c.drawCircle(128, 18, 5, P(OUT)); c.drawCircle(128, 36, 5, P(OUT))
    tusk = skia.Path(); tusk.moveTo(90, 50); tusk.quadTo(118, 20, 106, -18); tusk.quadTo(98, 20, 76, 48); tusk.close()
    fo(c, tusk, "#F6F1E4", ow=4)
    ef = math.sin(t * 7) * 8 if int(t * 1.3) % 3 == 0 else 0
    ear = skia.Path(); ear.moveTo(-4, -30); ear.lineTo(18 + ef, -86); ear.lineTo(40, -26); ear.close()
    fo(c, ear, dark, ow=5)
    ex, ey = 50, -4
    if eyes_cross > 0:
        for k, (xx, rr) in enumerate([(ex, 18), (ex - 34, 15)]):
            c.drawCircle(xx, ey, rr, P("#FFFFFF")); c.drawCircle(xx, ey, rr, P(OUT, stroke=4))
            c.drawCircle(xx + (10 if k == 0 else 12) * eyes_cross * (1 if k == 0 else 1), ey + 6, 6, P(OUT))
    else:
        op = blink_amt(t, 2.2)
        c.drawOval(skia.Rect.MakeXYWH(ex - 10, ey - 10 * op, 20, 20 * op), P(OUT))
        c.drawCircle(ex + 3, ey - 3, 3, P("#FFFFFF"))
    if mood == "angry":
        c.drawLine(ex - 28, ey - 26, ex + 22, ey - 10, P(OUT, stroke=10))
    elif mood == "scared":
        c.drawLine(ex - 22, ey - 14, ex + 22, ey - 30, P(OUT, stroke=7))
    if big:
        c.drawLine(10, -10, 60, 40, P("#C98A80", stroke=6)); c.drawLine(20, 30, 50, 0, P("#C98A80", stroke=5))
    c.restore()
    # phì hơi
    if snort > 0:
        for k in range(4):
            a = (snort + k * 0.15) % 1
            c.drawCircle(290 + a * 120, -120 + k * 14 - a * 20, 14 + a * 26, P("#FFFFFF", 200 * (1 - a)))
    if alpha < 0.999:
        c.restore()
    c.restore()
