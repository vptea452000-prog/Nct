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
    # nhún khi đi, thở khi đứng
    if p.walk is not None:
        amp = 16 if p.run else 9
        bob = -amp * abs(math.cos(p.walk)) + amp * 0.5
        sway = (4 if p.run else 2.5) * math.sin(p.walk)
    else:
        bob = 1.5 * math.sin(t * 2.2 + seed)
        sway = 1.4 * math.sin(t * 1.1 + seed)
    drop = p.crouch * 70 + p.sit * 150
    hip = (0.0, -2 * LEG + drop + bob)
    stride = (62 if p.run else 44)

    def foot_pos(side):
        if p.sit > 0.5:
            return (side * 20 + 110, -4)
        if p.walk is not None:
            ph = p.walk + (0 if side > 0 else math.pi)
            return (side * 6 + stride * math.sin(ph), -max(0.0, math.cos(ph)) * (34 if p.run else 22))
        return (side * 24 * bodyk, 0)

    def leg(foot, col):
        fx, fy = foot
        kx, ky = ik2(hip[0], hip[1], fx, fy - 6, LEG, LEG, bend=1)
        pth = skia.Path(); pth.moveTo(*hip); pth.lineTo(kx, ky); pth.lineTo(fx, fy - 6)
        c.drawPath(pth, P(INK, stroke=14))
        if col:
            c.drawPath(pth, P(col, stroke=8))
        c.drawLine(fx - 4, fy - 4, fx + 24, fy - 4, P(INK, stroke=16))

    leg_col = UNIFORM[1] if p.uniform else None
    leg(p.foot_b or foot_pos(-1), leg_col)
    leg(p.foot_f or foot_pos(1), leg_col)

    c.save()
    c.translate(*hip); c.rotate(p.lean + sway); c.translate(-hip[0], -hip[1])
    sh = (0.0, hip[1] - TOR)
    swing = 30 * math.sin(p.walk) if p.walk is not None else 6 * math.sin(t * 1.6 + seed)

    def arm(hand, side, col):
        if hand is None:
            hx, hy = -side * swing * (1.4 if p.run else 1.0) + side * 26, 165 - (40 if p.run else 0)
        else:
            hx, hy = hand
        tx, ty = sh[0] + hx, sh[1] + hy
        ex, ey = ik2(sh[0], sh[1], tx, ty, 92, 88, bend=-1)
        pth = skia.Path(); pth.moveTo(*sh); pth.lineTo(ex, ey); pth.lineTo(tx, ty)
        c.drawPath(pth, P(INK, stroke=14))
        if col:
            c.drawPath(pth, P(col, stroke=8))
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
    c.drawLine(hip[0], hip[1], sh[0], sh[1], P(INK, stroke=14))
    # thân áo
    if cloth:
        w_top, w_bot = 22 * bodyk + 6, 36 * bodyk + 6
        bot = hip[1] + (55 if L.get("skirt") else 8)
        body = skia.Path(); body.moveTo(-w_top, sh[1] + 4); body.lineTo(w_top, sh[1] + 4)
        body.lineTo(w_bot, bot); body.lineTo(-w_bot, bot); body.close()
        fo(c, body, cloth[0], ow=6)
        c.save(); c.clipPath(body, skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect.MakeXYWH(w_top * 0.3, sh[1], 200, 400), P(cloth[1], 140))
        c.restore()
        if p.uniform:
            c.drawLine(0, sh[1] + 10, 0, bot - 6, P(INK, 120, stroke=4))
            for k in range(3):
                c.drawCircle(4, sh[1] + 30 + k * 34, 4, P("#D9C27A"))
            c.drawRect(skia.Rect.MakeXYWH(-w_bot + 4, hip[1] - 14, 2 * w_bot - 8, 12), P("#4A3A26"))
        elif L.get("apron"):
            ap = skia.Path(); ap.moveTo(-w_top * 0.7, hip[1] - 50); ap.lineTo(w_top * 0.7, hip[1] - 50)
            ap.lineTo(w_bot * 0.75, bot - 6); ap.lineTo(-w_bot * 0.75, bot - 6); ap.close()
            fo(c, ap, L["apron"], ow=4)
        else:
            c.drawLine(-w_top + 8, sh[1] + 8, 6, sh[1] + 70, P(INK, 140, stroke=4))
        if p.belt:
            c.drawRect(skia.Rect.MakeXYWH(-w_bot, hip[1] - 40, 2 * w_bot, 22), P("#F3EEE2"))
            for k in range(14):
                c.drawCircle(-w_bot + 6 + k * (2 * w_bot - 12) / 13, hip[1] - 29, 3, P("#C0392B"))
    hf = arm(p.hand_f, 1, cloth[1] if cloth else None)
    if p.rifle == "hold":
        with _Xf(c, hf[0], hf[1], -30):
            c.drawLine(-20, -120, -20, 150, P(INK, stroke=16)); c.drawLine(-20, -120, -20, 150, P("#6E4E30", stroke=9))
        c.drawCircle(hf[0], hf[1], 11, P(INK))
    # đầu (trễ nhịp nhẹ theo độ nghiêng)
    c.save()
    hx, hy = sh[0] + 4, sh[1] - HR + 4
    c.translate(hx, hy); c.rotate(p.head_tilt - (p.lean + sway) * 0.35)
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
