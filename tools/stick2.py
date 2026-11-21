"""Bộ khung người que v2 cho định dạng kể chuyện 16:9.

Đầu tròn trắng, tay chân nét đen, quần áo là mảng màu phẳng. Chuyển động được tính sẵn:
đi có nhún và vung tay ngược chân, đứng yên vẫn thở và chuyển trọng tâm, chớp mắt không đều,
đầu trễ nhịp nhẹ khi thân nghiêng. Mỗi nhân vật là một bộ "look" cố định (tóc, mũ, áo, râu…).

Dùng:  from stick2 import Stick, LOOKS, draw_stick
       draw_stick(c, Stick("you", x, y, s, t, walk=..., hand_f=..., look=...))
"""
import math
from dataclasses import dataclass
import skia

INK = "#1A1A1A"


def _paint(col, a=255, stroke=None):
    h = col.lstrip("#")
    p = skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(int(max(0, min(255, a))), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


P = _paint


def fo(c, path, fill, ow=6, a=255):
    c.drawPath(path, P(fill, a)); c.drawPath(path, P(INK, a, stroke=ow))


def oval(cx, cy, rx, ry):
    p = skia.Path(); p.addOval(skia.Rect.MakeXYWH(cx - rx, cy - ry, 2 * rx, 2 * ry)); return p


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, q):
    return a + (b - a) * q


def ease_out(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = clamp(x); return 3 * x * x - 2 * x * x * x


def back_out(x, k=1.7):
    x = clamp(x) - 1; return 1 + x * x * ((k + 1) * x + k)


def ik2(sx, sy, tx, ty, l1, l2, bend=1):
    dx, dy = tx - sx, ty - sy
    d = max(1e-3, min(l1 + l2 - 0.01, math.hypot(dx, dy)))
    a = math.atan2(dy, dx)
    b = math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1))
    ang = a - bend * b
    return sx + l1 * math.cos(ang), sy + l1 * math.sin(ang)


def blink(t, seed):
    period = 2.8 + 1.3 * (0.5 + 0.5 * math.sin(seed * 3.1))
    ph = (t + seed) % period
    return 0.1 if ph < 0.1 else 1.0


# ---------------------------------------------------------------- bộ nhân vật cố định
LOOKS = {
    # "bạn": chàng trai làng chài 19 tuổi — tóc đen ngắn, (dân thường) khăn buộc đầu xanh, áo ngắn chàm
    "you": dict(hair="short", hair_col="#1E1E1E", headband="#3A6EA5", body=1.0, head=74,
                civ=("#3A5A8A", "#2C4468"), cap=None),
    # Kenji: to con, đầu tròn to, tóc húi cua, mắt híp hay cười
    "kenji": dict(hair="buzz", hair_col="#2A2A2A", headband=None, body=1.25, head=84,
                  civ=("#8A6A44", "#6E5236"), cap=None, cheeks=True),
    # mẹ: tóc búi, áo kimono lao động nâu đỏ, tạp dề
    "mother": dict(hair="bun", hair_col="#2A2A2A", headband=None, body=0.92, head=70,
                   civ=("#9A4A3A", "#7A3A2E"), apron="#E9DFC8", cap=None, skirt=True),
    "mother_old": dict(hair="bun", hair_col="#C9C9C9", headband=None, body=0.9, head=70,
                       civ=("#7A5A50", "#5E463E"), apron="#E9DFC8", cap=None, skirt=True),
    # viên đội trưởng: ria mép, mũ lính, quân phục
    "sergeant": dict(hair="short", hair_col="#1E1E1E", headband=None, body=1.1, head=76, mustache=True,
                     civ=None, cap="soldier"),
    # trưởng làng: già, hói, râu dê
    "chief": dict(hair="bald", hair_col="#BBBBBB", headband=None, body=0.95, head=72, goatee=True,
                  civ=("#5A5A6A", "#44444E"), cap=None),
    "father": dict(hair="short", hair_col="#555555", headband="#E9DFC8", body=1.05, head=74,
                   civ=("#4A5A6A", "#384654"), cap=None, mustache=True),
}
UNIFORM = ("#8C7E4E", "#6E623C")   # quân phục kaki


@dataclass
class Stick:
    who: str = "you"
    x: float = 0.0
    y: float = 0.0
    s: float = 1.0
    t: float = 0.0
    face: int = 1
    walk: float = None            # pha bước (radian)
    run: bool = False
    hand_f: tuple = None          # tay trước, toạ độ tính từ vai
    hand_b: tuple = None
    foot_f: tuple = None          # chân, toạ độ tính từ mặt đất dưới hông
    foot_b: tuple = None
    lean: float = 0.0
    crouch: float = 0.0           # 0..1
    sit: float = 0.0              # 0..1 ngồi bệt
    head_tilt: float = 0.0
    look: tuple = (0.0, 0.0)
    eyes: str = "dot"             # dot / wide / closed / happy / sad / squint
    mouth: str = "flat"           # flat / smile / frown / o / grin / open / wobble
    brow: float = 0.0             # +nâng / -cau
    tears: float = 0.0
    sweat: float = 0.0
    uniform: bool = False         # mặc quân phục (thay đồ dân thường)
    cap: str = None               # ghi đè mũ: "soldier" / None
    thin: float = 0.0             # 0..1 gầy đi (đảo đói)
    pack: bool = False            # ba lô
    rifle: str = None             # None / "shoulder" / "hold"
    belt: bool = False            # thắt lưng nghìn mũi chỉ (lộ ra)
    shiver: float = 0.0
    alpha: float = 1.0
    idle: float = 1.0             # độ cử động khi đứng yên (0,3 = đứng nghiêm)
    scarf: str = None             # khăn quàng cổ (màu)
    shawl: str = None             # khăn choàng vai (màu)


def draw_stick(c, p: Stick):
    L = LOOKS[p.who]
    t = p.t
    bodyk = L["body"] * (1 - 0.18 * p.thin)
    HR = L["head"]
    LEG, TOR = 108, 150 * min(1.15, L["body"] ** 0.5)
    seed = sum(ord(ch) for ch in p.who) * 0.01
    c.save()
    if p.alpha < 0.999:
        c.saveLayerAlpha(None, int(255 * clamp(p.alpha)))
    c.translate(p.x + p.shiver * 5 * math.sin(t * 70), p.y)
    c.scale(p.s * p.face, p.s)
    c.drawOval(skia.Rect.MakeXYWH(-80 * bodyk, -10, 160 * bodyk, 20), P("#000000", 38))
    # ---- chuyển động thân: đi có 2 nhịp nhún mỗi chu kỳ; đứng thì dồn trọng tâm, thở, gật nhẹ
    walking = p.walk is not None and p.sit < 0.5
    still = (1.0 - min(1.0, p.sit + p.crouch)) * p.idle        # bớt cử động thừa khi ngồi/khom/đứng nghiêm
    if walking:
        amp = 18 if p.run else 10
        bob = amp * 0.5 * (1 - math.cos(2 * p.walk)) - amp * 0.6     # thấp nhất lúc hai chân dang rộng
        sway = (5 if p.run else 3) * math.sin(p.walk)
        hip_x = 0.0
        lean_auto = 7 if p.run else 3.5
        head_bob = amp * 0.35 * math.cos(2 * p.walk - 0.8)          # đầu nảy trễ sau thân
    else:
        bob = (2.2 * math.sin(t * 2.1 + seed)) * still
        shift = math.sin(t * 0.55 + seed * 2.0)                      # dồn trọng tâm chậm sang trái/phải
        hip_x = 9 * shift * still
        sway = (-2.2 * shift + 1.0 * math.sin(t * 1.3 + seed)) * still
        lean_auto = 0.0
        head_bob = 1.2 * math.sin(t * 2.1 + seed - 0.6) * still
    drop = p.crouch * 70 + p.sit * 150
    hip = (hip_x, -2 * LEG + drop + bob)
    stride = (64 if p.run else 46)

    def foot_pos(side):
        if p.sit > 0.5:
            return (side * 20 + 110, -4), 0.0
        if walking:
            ph = p.walk + (0 if side > 0 else math.pi)
            sw = math.sin(ph)
            lift = max(0.0, math.cos(ph)) ** 1.5 * (40 if p.run else 26)
            toe = -18 * max(0.0, math.cos(ph)) * (1 if sw > 0 else 0.4)     # mũi chân chúc xuống khi nhấc
            return (side * 6 + stride * sw, -lift), toe
        # đứng: chân chịu lực thẳng dưới hông, chân kia thả lỏng
        load = 0.5 + 0.5 * math.sin(t * 0.55 + seed * 2.0) * side * still
        return (side * (20 + 8 * (1 - load)) * bodyk + hip_x * 0.5, 0), 0.0

    def hose(a, j, b, width, col):
        """Chi uốn cong mềm: đường cong đi qua khớp giữa (kiểu 'ống cao su')."""
        cx, cy = 2 * j[0] - (a[0] + b[0]) / 2, 2 * j[1] - (a[1] + b[1]) / 2
        pth = skia.Path(); pth.moveTo(*a); pth.quadTo(cx, cy, *b)
        c.drawPath(pth, P(INK, stroke=width))
        if col:
            c.drawPath(pth, P(col, stroke=width - 6))

    def leg(foot_toe, col):
        (fx, fy), toe = foot_toe
        kx, ky = ik2(hip[0], hip[1], fx, fy - 6, LEG, LEG, bend=1)
        hose(hip, (kx, ky), (fx, fy - 6), 14, None)      # chân: một nét đen
        a = math.radians(toe)
        c.drawLine(fx - 4, fy - 4, fx - 4 + 28 * math.cos(a), fy - 4 - 28 * math.sin(a) * -1, P(INK, stroke=16))

    leg_col = UNIFORM[1] if p.uniform else None
    leg((p.foot_b, 0.0) if p.foot_b else foot_pos(-1), leg_col)
    leg((p.foot_f, 0.0) if p.foot_f else foot_pos(1), leg_col)

    c.save()
    c.translate(*hip); c.rotate(p.lean + sway + lean_auto); c.translate(-hip[0], -hip[1])
    breath = 2.5 * math.sin(t * 2.1 + seed) * still
    sh = (hip[0] - 0.6 * sway, hip[1] - TOR - breath)

    def arm(hand, side, col):
        if hand is None:
            if walking:
                ph = p.walk + (0 if side < 0 else math.pi)
                sw = math.sin(ph); lag = math.sin(ph - 0.7)               # cẳng tay trễ nhịp sau bắp tay
                k = 1.5 if p.run else 1.0
                hx = side * 22 + 38 * k * lag
                hy = 160 - 22 * k * abs(sw) - (45 if p.run else 0)
            else:
                hx = side * 26 + 5 * math.sin(t * 1.3 + seed + side) * still
                hy = 163 + 3 * math.sin(t * 2.1 + seed) * still
        else:
            hx, hy = hand
            hx += 3 * math.sin(t * 1.7 + seed + side) * still               # tay đang giữ tư thế vẫn trôi rất nhẹ
            hy += 3 * math.sin(t * 2.3 + seed * 1.3 + side) * still
        tx, ty = sh[0] + hx, sh[1] + hy
        ex, ey = ik2(sh[0], sh[1], tx, ty, 92, 88, bend=-1)
        hose(sh, (ex, ey), (tx, ty), 14, None)           # tay: một nét đen
        c.drawCircle(tx, ty, 11, P(INK))
        return tx, ty

    cloth = UNIFORM if p.uniform else L["civ"]
    if p.pack and p.uniform:
        fo(c, skia.Path().addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-70 * bodyk, sh[1] + 10, 46, 100), 12, 12)) or skia.Path(),
           "#6E5A3A", ow=5)
    hb = arm(p.hand_b, -1, cloth[1] if cloth else None)
    if p.rifle == "shoulder":
        with _Xf(c, -18, sh[1] + 20, -24):
            c.drawLine(0, -40, 0, 240, P(INK, stroke=16)); c.drawLine(0, -40, 0, 240, P("#6E4E30", stroke=9))
    spine = skia.Path(); spine.moveTo(*hip)
    spine.quadTo(hip[0] + 10 + 0.8 * sway, (hip[1] + sh[1]) / 2, sh[0], sh[1])          # sống lưng hơi cong
    c.drawPath(spine, P(INK, stroke=14))
    # thân áo
    if cloth:
        w_top, w_bot = 24 * bodyk + 6, 36 * bodyk + 6
        bot = hip[1] + (55 if L.get("skirt") else 10)
        top = sh[1] - 2
        mid = (top + bot) / 2
        # thân bo tròn: vai tròn, hông phình nhẹ, gấu bo góc
        body = skia.Path(); body.moveTo(0, top)
        body.cubicTo(w_top * 0.9, top, w_top + 6, top + 10, w_top + 4, top + 34)
        body.cubicTo(w_bot + 6, mid, w_bot + 8, bot - 26, w_bot - 6, bot)
        body.quadTo(0, bot + 10, -w_bot + 6, bot)
        body.cubicTo(-w_bot - 8, bot - 26, -w_bot - 6, mid, -w_top - 4, top + 34)
        body.cubicTo(-w_top - 6, top + 10, -w_top * 0.9, top, 0, top)
        body.close()
        fo(c, body, cloth[0], ow=6)
        c.save(); c.clipPath(body, skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect.MakeXYWH(w_top * 0.3, sh[1], 200, 400), P(cloth[1], 140))
        c.restore()
        if p.uniform:
            c.drawLine(0, sh[1] + 10, 0, bot - 6, P(INK, 120, stroke=4))
            for k in range(3):
                c.drawCircle(4, sh[1] + 30 + k * 34, 4, P("#D9C27A"))
            c.save(); c.clipPath(body, skia.ClipOp.kIntersect, True)
            c.drawRect(skia.Rect.MakeXYWH(-w_bot - 10, hip[1] - 16, 2 * w_bot + 20, 12), P("#4A3A26"))
            c.restore()
        elif L.get("apron"):
            ap = skia.Path(); ap.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w_top * 0.75, hip[1] - 50, w_top * 1.5, bot - hip[1] + 40), 14, 14))
            fo(c, ap, L["apron"], ow=4)
        else:
            c.drawLine(-w_top + 8, sh[1] + 8, 6, sh[1] + 70, P(INK, 140, stroke=4))
        if p.belt:
            c.save(); c.clipPath(body, skia.ClipOp.kIntersect, True)
            c.drawRect(skia.Rect.MakeXYWH(-w_bot - 10, hip[1] - 40, 2 * w_bot + 20, 22), P("#F3EEE2"))
            c.restore()
            for k in range(14):
                c.drawCircle(-w_bot + 6 + k * (2 * w_bot - 12) / 13, hip[1] - 29, 3, P("#C0392B"))
    if p.shawl:
        sw = skia.Path(); sw.moveTo(-34 * bodyk - 10, sh[1] + 2); sw.quadTo(0, sh[1] - 14, 34 * bodyk + 10, sh[1] + 2)
        sw.lineTo(30 * bodyk + 14, sh[1] + 70); sw.quadTo(0, sh[1] + 96, -30 * bodyk - 14, sh[1] + 70); sw.close()
        fo(c, sw, p.shawl, ow=5)
    if p.scarf:
        c.drawLine(-22, sh[1] + 4, 22, sh[1] + 4, P(INK, stroke=22)); c.drawLine(-22, sh[1] + 4, 22, sh[1] + 4, P(p.scarf, stroke=14))
        tail = skia.Path(); tail.moveTo(-14, sh[1] + 6); tail.lineTo(-30 - 6 * math.sin(t * 3), sh[1] + 70); tail.lineTo(-12, sh[1] + 74); tail.lineTo(2, sh[1] + 8); tail.close()
        fo(c, tail, p.scarf, ow=4)
    hf = arm(p.hand_f, 1, cloth[1] if cloth else None)
    if p.rifle == "hold":
        with _Xf(c, hf[0], hf[1], -30):
            c.drawLine(-20, -120, -20, 150, P(INK, stroke=16)); c.drawLine(-20, -120, -20, 150, P("#6E4E30", stroke=9))
        c.drawCircle(hf[0], hf[1], 11, P(INK))
    # đầu (trễ nhịp nhẹ theo độ nghiêng)
    c.save()
    hx, hy = sh[0] + 4, sh[1] - HR + 4 + head_bob
    nod = (2.5 * math.sin(t * 0.9 + seed * 3) + 1.5 * math.sin(t * 2.3 + seed)) * still
    c.translate(hx, hy); c.rotate(p.head_tilt + nod - (p.lean + sway + lean_auto) * 0.45)
    if p.look == (0.0, 0.0) and p.eyes in ("dot", "wide"):
        dart = math.floor((t + seed * 7) / 2.6)                         # thỉnh thoảng đảo mắt
        p.look = (0.5 * math.sin(dart * 2.7), 0.25 * math.sin(dart * 1.9))
    _head(c, L, p, HR, t, seed)
    c.restore()
    c.restore()
    if p.alpha < 0.999:
        c.restore()
    c.restore()


class _Xf:
    def __init__(self, c, x, y, rot=0.0, s=1.0):
        self.c, self.x, self.y, self.rot, self.s = c, x, y, rot, s

    def __enter__(self):
        self.c.save(); self.c.translate(self.x, self.y); self.c.rotate(self.rot); self.c.scale(self.s, self.s)

    def __exit__(self, *a):
        self.c.restore()


def _head(c, L, p, R, t, seed):
    hair, hc = L["hair"], L["hair_col"]
    cap = p.cap if p.cap is not None else (L.get("cap") or ("soldier" if p.uniform else None))
    # tóc sau
    if hair == "bun":
        fo(c, oval(-R * 0.55, -R * 0.75, R * 0.38, R * 0.36), hc, ow=6)
    fo(c, oval(0, 0, R, R), "#FFFFFF", ow=7)
    if L.get("cheeks"):
        for dx in (-0.45, 0.55):
            c.drawOval(skia.Rect.MakeXYWH(dx * R - 16, R * 0.18, 32, 16), P("#F2A0A0", 170))
    if not cap:
        if hair in ("short", "bun"):
            hp = skia.Path(); hp.moveTo(-R * 0.98, -R * 0.08)
            hp.quadTo(-R * 1.02, -R * 1.08, R * 0.1, -R * 1.02)
            hp.quadTo(R * 0.95, -R * 0.95, R * 0.98, -R * 0.2)
            hp.quadTo(R * 0.5, -R * 0.55, -R * 0.2, -R * 0.5); hp.quadTo(-R * 0.7, -R * 0.45, -R * 0.98, -R * 0.08); hp.close()
            fo(c, hp, hc, ow=6)
        elif hair == "buzz":
            hp = skia.Path(); hp.addArc(skia.Rect.MakeXYWH(-R, -R, 2 * R, 2 * R), 190, 160); hp.close()
            fo(c, hp, hc, ow=6)
        elif hair == "bald":
            c.drawArc(skia.Rect.MakeXYWH(-R * 1.0, -R * 0.4, R * 0.5, R * 0.8), 120, 120, False, P(hc, stroke=10))
        if L.get("headband"):
            c.drawLine(-R * 0.96, -R * 0.42, R * 0.96, -R * 0.42, P(INK, stroke=22))
            c.drawLine(-R * 0.96, -R * 0.42, R * 0.96, -R * 0.42, P(L["headband"], stroke=14))
    # mặt (dịch nhẹ về phía trước — hướng nhìn)
    fx = R * 0.22
    op = blink(t, seed)
    ey = -R * 0.08
    for dx in (-R * 0.28, R * 0.32):
        ex = fx + dx
        if p.eyes == "closed" or op < 0.5:
            c.drawLine(ex - 9, ey, ex + 9, ey, P(INK, stroke=5))
        elif p.eyes == "happy":
            pth = skia.Path(); pth.moveTo(ex - 11, ey + 4); pth.quadTo(ex, ey - 12, ex + 11, ey + 4); c.drawPath(pth, P(INK, stroke=5))
        elif p.eyes == "wide":
            c.drawCircle(ex, ey, 14, P("#FFFFFF")); c.drawCircle(ex, ey, 14, P(INK, stroke=4))
            c.drawCircle(ex + p.look[0] * 5, ey + p.look[1] * 5, 6, P(INK))
        elif p.eyes == "squint":
            c.drawLine(ex - 10, ey, ex + 10, ey - 2, P(INK, stroke=6))
        else:
            c.drawCircle(ex + p.look[0] * 6, ey + p.look[1] * 6, 8 if not L.get("cheeks") else 7, P(INK))
        by = ey - 24 - p.brow * 8
        if p.eyes == "sad" or p.brow < -0.5:
            tilt = 6 if dx < 0 else -6
            c.drawLine(ex - 11, by - tilt, ex + 11, by + tilt, P(INK, stroke=5))
        else:
            c.drawLine(ex - 11, by, ex + 11, by, P(INK, stroke=5))
    if p.tears > 0:
        for dx in (-R * 0.28, R * 0.32):
            ty = ey + 14 + (t * 60 % 30)
            c.drawCircle(fx + dx, ty, 6, P("#7FC4E8", 230 * p.tears))
    if p.sweat > 0:
        d = skia.Path(); sx, sy = -R * 0.7, -R * 0.3 + (t * 90 % 30)
        d.moveTo(sx, sy - 14); d.quadTo(sx + 10, sy + 4, sx, sy + 8); d.quadTo(sx - 10, sy + 4, sx, sy - 14); d.close()
        fo(c, d, "#9FD3F0", ow=3, a=255 * p.sweat)
    my = R * 0.42
    mx = fx + 4
    if L.get("mustache"):
        m = skia.Path(); m.moveTo(mx - 22, my - 8); m.quadTo(mx, my - 22, mx + 22, my - 8); m.quadTo(mx, my - 12, mx - 22, my - 8); m.close()
        fo(c, m, L["hair_col"] if L["hair_col"] != "#BBBBBB" else "#888888", ow=3)
    if L.get("goatee"):
        g = skia.Path(); g.moveTo(mx - 10, my + 10); g.lineTo(mx + 10, my + 10); g.lineTo(mx, my + 40); g.close(); fo(c, g, "#CCCCCC", ow=3)
    if p.mouth == "smile":
        pth = skia.Path(); pth.moveTo(mx - 14, my - 2); pth.quadTo(mx, my + 12, mx + 14, my - 2); c.drawPath(pth, P(INK, stroke=5))
    elif p.mouth == "grin":
        pth = skia.Path(); pth.moveTo(mx - 18, my - 4); pth.quadTo(mx, my + 20, mx + 18, my - 4); pth.close(); fo(c, pth, "#FFFFFF", ow=4)
    elif p.mouth == "frown":
        pth = skia.Path(); pth.moveTo(mx - 12, my + 6); pth.quadTo(mx, my - 6, mx + 12, my + 6); c.drawPath(pth, P(INK, stroke=5))
    elif p.mouth == "o":
        fo(c, oval(mx, my + 2, 8, 10), "#5A1E16", ow=3)
    elif p.mouth == "open":
        fo(c, oval(mx, my + 4, 14, 14), "#5A1E16", ow=3)
    elif p.mouth == "wobble":
        pth = skia.Path(); pth.moveTo(mx - 14, my)
        for k in range(4):
            pth.quadTo(mx - 14 + 7 * (k + 0.5) * 1.0, my + (5 if k % 2 else -5), mx - 14 + 7 * (k + 1), my)
        c.drawPath(pth, P(INK, stroke=4))
    else:
        c.drawLine(mx - 10, my, mx + 10, my, P(INK, stroke=5))
    if cap == "flat":
        cp = skia.Path(); cp.moveTo(-R * 1.02, -R * 0.2); cp.quadTo(-R * 0.95, -R * 1.12, R * 0.2, -R * 1.02)
        cp.quadTo(R * 1.05, -R * 0.92, R * 1.02, -R * 0.36); cp.lineTo(R * 1.45, -R * 0.3); cp.quadTo(R * 1.2, -R * 0.16, R * 0.9, -R * 0.2); cp.close()
        fo(c, cp, L.get("cap_col", "#6A5A4A"), ow=6)
        c.drawLine(-R * 0.9, -R * 0.42, R * 0.9, -R * 0.42, P("#000000", 40, stroke=6))
    if cap == "soldier":
        cp = skia.Path(); cp.moveTo(-R * 1.0, -R * 0.25); cp.quadTo(-R * 0.95, -R * 1.15, R * 0.15, -R * 1.08)
        cp.quadTo(R * 0.98, -R * 1.0, R * 1.0, -R * 0.3); cp.close()
        fo(c, cp, UNIFORM[0], ow=6)
        c.drawLine(-R * 1.0, -R * 0.3, R * 1.0, -R * 0.3, P(INK, stroke=8))
        visor = skia.Path(); visor.moveTo(R * 0.5, -R * 0.32); visor.quadTo(R * 1.2, -R * 0.34, R * 1.25, -R * 0.18); visor.lineTo(R * 0.5, -R * 0.22); visor.close()
        fo(c, visor, "#4A3A26", ow=4)
        c.drawCircle(R * 0.2, -R * 0.72, 9, P("#D9B02A"))
        # tấm vải che gáy
        nf = skia.Path(); nf.moveTo(-R * 1.0, -R * 0.3); nf.lineTo(-R * 1.15, R * 0.55); nf.lineTo(-R * 0.55, R * 0.5); nf.lineTo(-R * 0.6, -R * 0.3); nf.close()
        fo(c, nf, UNIFORM[0], ow=5)
