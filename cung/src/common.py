"""Bộ công cụ cảnh dùng chung cho Bộp và Gầm (bộ khung v2) — tách từ Tập 3."""
import math
import sys
from pathlib import Path

import skia

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from lib import *  # noqa
from toon import fill_out, rrect_path, oval_path  # noqa
from toon2 import kinetic  # noqa
from sets import grad_rect  # noqa
from kit import pop, shake, cam, comic_bubble, sfx_word, cave_exterior, fire, smoke, flat_stone  # noqa
from beats import T, DUR  # noqa
import rig  # noqa
from rig import Pose, draw_char, P, OUT, fo, oval, noise1  # noqa
from lipsync import LipSync  # noqa

LS = LipSync(T, ROOT / "build" / "lipsync_cache.npz")
GROUND = 1290


def beat(n):
    return T[n][0], T[n][1]


def loc(n, t):
    a, b = beat(n)
    return t - a, clamp((t - a) / (b - a))


class Cam:
    def __init__(self, cx=540, cy=960, z=1.0):
        self.cx, self.cy, self.z = cx, cy, z

    def on(self, c):
        c.save(); cam(c, self.cx, self.cy, self.z)

    def off(self, c):
        c.restore()

    def map(self, x, y):
        return W / 2 + self.z * (x - self.cx), H / 2 + self.z * (y - self.cy)


HEAD_TOP = {"bop": 600, "gam": 560}


def say(c, n, K, who_x, who_y, s, t, who=None, bx=None, by=380, d=0.1, crouch=0.0):
    """Bóng thoại; đuôi chỉ vào đỉnh đầu nhân vật (toạ độ thế giới → màn hình qua camera K)."""
    a, b = beat(n)
    row = T[n][2]
    who = who or row[3] or "bop"
    hx, hy = K.map(who_x, who_y - (HEAD_TOP[who] - 60 * crouch) * s)
    if bx is None:
        bx = clamp(hx, 430, 650)
    comic_bubble(c, bx, by, row[5], row[4], (hx, hy - 10), pop(t, a + d))


def say_at(c, n, t, x, y, tail, d=0.1):
    a, b = beat(n)
    row = T[n][2]
    comic_bubble(c, x, y, row[5], row[4], tail, pop(t, a + d))


def ch(c, who, x, y, s, t, **kw):
    """Nhân vật với nhép miệng tự động + đung đưa nhẹ."""
    tk = LS.talk(who, t)
    kw.setdefault("talk", tk)
    seed = 0.4 if who == "bop" else 1.9
    kw["head_tilt"] = kw.get("head_tilt", 0.0) + 3 * noise1(t * 0.8, seed)
    kw["head_dx"] = kw.get("head_dx", 0.0) + 3 * noise1(t, seed + 2)
    return draw_char(c, Pose(who, x, y, s, t, **kw))


def bop_outfit(t):
    return "coat"


# ---------------------------------------------------------------- đạo cụ
def needle(c, x, y, L, ang, sharp=1.0, hole=1.0, thread=0.0, shine=0.0, t=0.0, thread_len=160, wav=1.0):
    """Kim xương chim. Gốc (x,y) = giữa kim; ang độ (0 = nằm ngang, mũi bên phải)."""
    c.save(); c.translate(x, y); c.rotate(ang)
    h = L * 0.07
    p = skia.Path()
    tip = L / 2 + L * 0.08 * sharp
    p.moveTo(-L / 2, -h); p.lineTo(L / 2 - L * 0.12, -h * (1 - 0.3 * sharp))
    p.lineTo(tip, 0); p.lineTo(L / 2 - L * 0.12, h * (1 - 0.3 * sharp)); p.lineTo(-L / 2, h)
    p.quadTo(-L / 2 - h * 1.2, 0, -L / 2, -h); p.close()
    fo(c, p, "#F3EBD8", ow=max(3, L * 0.018))
    c.drawLine(-L * 0.3, -h * 0.4, L * 0.3, -h * 0.3, P("#FFFFFF", 200, stroke=max(2, L * 0.012)))
    if hole > 0:
        hr = h * 0.55 * hole
        c.drawOval(skia.Rect.MakeXYWH(-L / 2 + h * 0.6 - hr * 1.3, -hr, hr * 2.6, hr * 2), P("#3A2A20"))
    if thread > 0:
        tp = skia.Path(); tp.moveTo(-L / 2 + h * 0.6, 0)
        n = 12
        for k in range(1, n + 1):
            q = k / n
            tp.lineTo(-L / 2 + h * 0.6 - thread_len * q * thread, wav * 18 * math.sin(q * 7 + t * 6) * q)
        c.drawPath(tp, P("#E3C48E", stroke=max(3, L * 0.02)))
    if shine > 0:
        sp = skia.Path()
        for j in range(8):
            rr = (L * 0.12 if j % 2 == 0 else L * 0.04) * shine
            aa = j * math.pi / 4 + t * 2
            (sp.moveTo if j == 0 else sp.lineTo)(tip + rr * math.cos(aa), rr * math.sin(aa))
        sp.close(); c.drawPath(sp, P("#FFF6C8"))
    c.restore()


def needle_prop(ang=-60, L=90, thread=0.0, t=0.0):
    def f(c):
        needle(c, 0, -L * 0.25, L, ang, thread=thread, t=t, thread_len=70)
    return f


def hide_prop(c):
    p = skia.Path(); p.moveTo(-60, -20); p.quadTo(-20, -70, 50, -40); p.quadTo(90, 0, 50, 40); p.quadTo(-10, 70, -60, 30); p.close()
    fo(c, p, "#A6855C", ow=5)
    c.drawCircle(-10, 0, 14, P("#8C6E48")); c.drawCircle(30, -10, 10, P("#8C6E48"))


def hide_sheet(c, x, y, w, h, rot=0.0, flap=0.0, t=0.0, hole=False, col="#A6855C", dark="#8C6E48", stitches=0, smoke_k=0.0):
    """Tấm da thú có mép lượn (bay phần phật khi flap > 0)."""
    c.save(); c.translate(x, y); c.rotate(rot)
    p = skia.Path()
    n = 10
    pts = []
    for k in range(n):
        q = k / n
        pts.append((-w / 2 + w * q, -h / 2 + flap * 22 * math.sin(t * 20 + q * 6) + (8 if k % 2 else -4)))
    for k in range(n):
        q = k / n
        pts.append((w / 2 + flap * 14 * math.sin(t * 18 + q * 5), -h / 2 + h * q))
    for k in range(n):
        q = k / n
        pts.append((w / 2 - w * q, h / 2 + flap * 26 * math.sin(t * 21 + q * 7) + (6 if k % 2 else -6)))
    for k in range(n):
        q = k / n
        pts.append((-w / 2 + flap * 14 * math.sin(t * 19 + q * 4), h / 2 - h * q))
    p.moveTo(*pts[0])
    for i in range(1, len(pts)):
        mx, my = (pts[i - 1][0] + pts[i][0]) / 2, (pts[i - 1][1] + pts[i][1]) / 2
        p.quadTo(pts[i - 1][0], pts[i - 1][1], mx, my)
    p.close()
    if hole:
        p.addOval(skia.Rect.MakeXYWH(-w * 0.2, -h * 0.22, w * 0.4, h * 0.44))
        p.setFillType(skia.PathFillType.kEvenOdd)
    fo(c, p, col, ow=6)
    c.save(); c.clipPath(p, skia.ClipOp.kIntersect, True)
    for k in range(6):
        c.drawCircle(-w * 0.35 + (k % 3) * w * 0.35, -h * 0.2 + (k // 3) * h * 0.4, min(w, h) * 0.09, P(dark))
    if hole:
        c.drawOval(skia.Rect.MakeXYWH(-w * 0.2 - 8, -h * 0.22 - 8, w * 0.4 + 16, h * 0.44 + 16), P("#2A2A2A", stroke=14))
    c.restore()
    for k in range(stitches):
        sx = -w * 0.4 + w * 0.8 * k / max(1, stitches - 1)
        c.drawLine(sx - 8, -6, sx + 8, 6, P("#F1E2C0", stroke=5))
    c.restore()


def big_hand(c, x, y, s, rot, skin="#8A5A3C", pinch=True):
    """Bàn tay cận cảnh (kiểu găng hoạt hình)."""
    with Xf(c, x, y, rot, s):
        arm = skia.Path(); arm.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-70, 40, 140, 400), 60, 60))
        fo(c, arm, skin, ow=7)
        palm = oval(0, 0, 95, 80); fo(c, palm, skin, ow=7)
        for k in range(3):
            fo(c, oval(-50 + k * 40, -70, 24, 34), skin, ow=6)
        fo(c, oval(80 if pinch else 90, -30, 26, 40), skin, ow=6)


def winter_tree(c, x, y, s=1.0, snow=0.0):
    with Xf(c, x, y, 0, s):
        tr = skia.Path(); tr.moveTo(-34, 0); tr.lineTo(-18, -700); tr.lineTo(18, -700); tr.lineTo(34, 0); tr.close()
        fo(c, tr, "#6E5236", ow=7)
        for sd, yy, L in [(-1, -420, 180), (1, -520, 200), (-1, -620, 150), (1, -300, 150)]:
            c.drawLine(0, yy, sd * L, yy - L * 0.6, P(OUT, stroke=24)); c.drawLine(0, yy, sd * L, yy - L * 0.6, P("#6E5236", stroke=15))
        if snow > 0:
            for sd, yy, L in [(-1, -420, 180), (1, -520, 200), (-1, -620, 150), (1, -300, 150)]:
                c.drawLine(sd * L * 0.3, yy - L * 0.2 - 12, sd * L, yy - L * 0.6 - 12, P("#FFFFFF", 255 * snow, stroke=12))


def snowfall(c, t, dens=60, wind=0.4, a=230, big=1.0):
    for k in range(dens):
        sp = 120 + (k * 37) % 140
        x = ((k * 173) % 1400 - 160 + t * sp * wind * 3 + 30 * math.sin(t * 1.3 + k)) % 1400 - 160
        y = ((k * 97) % 2100 + t * sp) % 2100 - 100
        c.drawCircle(x, y, (4 + (k % 4) * 2.5) * big, P("#FFFFFF", a))


def wind_lines(c, t, n=6, a=140, speed=900, y0=420, dy=140, direction=-1):
    for k in range(n):
        x = (t * speed + k * 330) % (W + 800) - 400
        if direction < 0:
            x = W - x
        y = y0 + k * dy + 20 * math.sin(t * 3 + k)
        pth = skia.Path(); pth.moveTo(x, y); pth.quadTo(x + 90, y - 34, x + 200, y); pth.quadTo(x + 260, y + 20, x + 300, y - 6)
        c.drawPath(pth, P("#FFFFFF", a, stroke=6))


def breath(c, x, y, t, t0, dirx=1, a=210):
    age = t - t0
    if age < 0 or age > 1.4:
        return
    for k in range(4):
        q = clamp(age * 1.4 - k * 0.12)
        if q <= 0:
            continue
        pt = paint("#FFFFFF", a * (1 - q))
        pt.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
        c.drawCircle(x + dirx * (30 + q * 150), y - q * 60 + k * 6, 16 + q * 40, pt)


def zzz(c, x, y, t):
    for k in range(3):
        q = (t * 0.7 + k / 3) % 1
        text(c, "z", x + q * 60 + 10 * math.sin(q * 6), y - q * 160, "xbold", 40 + 30 * q, "#FFFFFF", a=255 * math.sin(q * math.pi),
             align="center", stroke=6, stroke_color="#1A120D")


def louse(c, x, y, s, t, seed=0.0, rot=0.0, bundle=False, wave=False):
    """Con chấy dễ thương: thân tròn, sáu chân nhỏ, mắt to, cười."""
    with Xf(c, x, y, rot + 6 * math.sin(t * 8 + seed), s):
        for k in range(3):
            for sd in (-1, 1):
                a = math.sin(t * 16 + k + seed) * 10
                c.drawLine(sd * 18, -10 + k * 14, sd * (40 + a * 0.3), -18 + k * 16 + a, P(OUT, stroke=5))
        fo(c, oval(0, 0, 26, 32), "#E8C8A0", ow=5)
        fo(c, oval(0, -30, 20, 18), "#E8C8A0", ow=5)
        for sd in (-1, 1):
            c.drawCircle(sd * 8, -32, 7, P("#FFFFFF")); c.drawCircle(sd * 8, -31, 4, P(OUT))
        sm = skia.Path(); sm.moveTo(-6, -22); sm.quadTo(0, -16, 6, -22); c.drawPath(sm, P(OUT, stroke=3))
        c.drawOval(skia.Rect.MakeXYWH(-16, -26, 8, 5), P("#E8746B", 160)); c.drawOval(skia.Rect.MakeXYWH(8, -26, 8, 5), P("#E8746B", 160))
        if bundle:
            c.drawLine(10, -10, 40, -60, P(OUT, stroke=5))
            fo(c, oval(46, -66, 20, 16), "#C9A06A", ow=4)
        if wave:
            wv = math.sin(t * 12) * 20
            c.drawLine(-22, -10, -46, -46 + wv, P(OUT, stroke=6))


def sinew(c, x0, y0, x1, y1, w=8, col="#E3C48E", sag=0.0):
    p = skia.Path(); p.moveTo(x0, y0); p.quadTo((x0 + x1) / 2, (y0 + y1) / 2 + sag, x1, y1)
    c.drawPath(p, P(OUT, stroke=w + 6)); c.drawPath(p, P(col, stroke=w))


def stone_spear_v(c, x, y, L=520, s=1.0, ang=0.0):
    with Xf(c, x, y, ang, s):
        c.drawLine(0, 0, 0, -L, P(OUT, stroke=26)); c.drawLine(0, 0, 0, -L, P("#8A6A44", stroke=17))
        tip = skia.Path(); tip.moveTo(-26, -L + 10); tip.lineTo(0, -L - 110); tip.lineTo(26, -L + 10); tip.close()
        fo(c, tip, "#9AA3A8", ow=5)
        fo(c, rrect_path(-16, -L - 6, 32, 40, 8), "#C98A2A", ow=4)


def flea(c, x, y, t, t0=0.0):
    ph = ((t - t0) * 1.6) % 1
    k = int((t - t0) * 1.6)
    px = x + ((k * 53) % 120) - 60 + 50 * ph * (1 if k % 2 else -1)
    py = y - 110 * 4 * ph * (1 - ph)
    c.drawCircle(px, py, 7, P("#3A2A20"))
    c.drawLine(px - 6, py + 4, px - 12, py + 12, P(OUT, stroke=3)); c.drawLine(px + 6, py + 4, px + 12, py + 12, P(OUT, stroke=3))


def ff_badge(c, t, txt="▶▶ x4"):
    with Xf(c, 900, 200, 0, 1):
        fo(c, rrect_path(-130, -50, 260, 100, 30), "#1A120D", ow=4)
        text(c, txt, 0, 18, "xbold", 52, "#F4C430", align="center")


def panel(c, x, y, w, h, p=1.0, col="#FBF7EE"):
    if p <= 0:
        return
    with Xf(c, x, y, 0, back_out(clamp(p)) if p < 1 else 1.0):
        fo(c, rrect_path(-w / 2, -h / 2, w, h, 36), col, ow=8)


def check_mark(c, x, y, ok, p=1.0):
    if p <= 0:
        return
    with Xf(c, x, y, 0, back_out(clamp(p))):
        if ok:
            pth = skia.Path(); pth.moveTo(-34, 0); pth.lineTo(-8, 28); pth.lineTo(40, -32)
            c.drawPath(pth, P("#2E8B57", stroke=18))
        else:
            c.drawLine(-30, -30, 30, 30, P("#C0392B", stroke=18)); c.drawLine(30, -30, -30, 30, P("#C0392B", stroke=18))


# ---------------------------------------------------------------- bối cảnh
def exterior(c, t, snow=0.0, wind=True, tree_snow=0.0, falling=0, hide_on_tree=False):
    cave_exterior(c, t, morning=1.0, wind=False)
    if snow > 0:
        c.drawRect(skia.Rect.MakeXYWH(-400, GROUND, W + 800, 900), paint("#EEF3F7", 255 * snow))
        c.drawRect(skia.Rect.MakeXYWH(-400, GROUND, W + 800, 12), paint("#B8C6D2", 255 * snow))
        for k in range(8):
            c.drawOval(skia.Rect.MakeXYWH(-100 + k * 170, GROUND + 40 + (k % 3) * 70, 120, 26), paint("#D5E0E8", 200 * snow))
    winter_tree(c, 930, GROUND, 1.0, max(snow, tree_snow))
    if hide_on_tree:
        hide_draped(c, 930, 600, t)
    if wind:
        wind_lines(c, t, n=5, a=110, speed=700, y0=560, dy=130)
    if falling:
        snowfall(c, t, falling, wind=0.3)


def hide_draped(c, x, y, t):
    with Xf(c, x, y, 4 * math.sin(t * 3), 1):
        p = skia.Path(); p.moveTo(-120, -20); p.quadTo(0, -70, 120, -20)
        p.lineTo(110 + 8 * math.sin(t * 5), 110); p.lineTo(60, 90); p.lineTo(20, 130); p.lineTo(-30, 95); p.lineTo(-80, 125); p.lineTo(-115, 90); p.close()
        fo(c, p, "#A6855C", ow=6)
        c.drawCircle(-40, 30, 16, P("#8C6E48")); c.drawCircle(40, 50, 13, P("#8C6E48"))


def cave_in(c, t, door="night", snow=True, fire_x=540, fire_s=0.7, fire_on=True):
    """Trong hang nhìn ra cửa (bên phải). door: night / morning."""
    grad_rect(c, skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), "#2A211B", "#120D0A")
    dp = skia.Path(); dp.moveTo(760, 1300); dp.quadTo(770, 700, 940, 680); dp.quadTo(1120, 700, 1140, 1300); dp.close()
    c.save(); c.clipPath(dp, skia.ClipOp.kIntersect, True)
    if door == "night":
        grad_rect(c, skia.Rect.MakeXYWH(740, 650, 440, 700), "#1D2A44", "#3A4A6A")
    else:
        grad_rect(c, skia.Rect.MakeXYWH(740, 650, 440, 700), "#9FC9E6", "#F6E7C0")
    c.drawRect(skia.Rect.MakeXYWH(740, 1200, 440, 120), paint("#EEF3F7"))
    if snow:
        for k in range(40):
            x = 760 + (k * 53 - t * 500) % 420; y = 650 + ((k * 97 + t * 400) % 700)
            c.drawCircle(x, y, 5 + k % 3 * 2, paint("#FFFFFF", 230))
    c.restore()
    c.drawPath(dp, paint(OUT, stroke=8))
    c.drawRect(skia.Rect.MakeXYWH(-400, GROUND, W + 800, 900), paint("#3A2E24"))
    c.drawRect(skia.Rect.MakeXYWH(-400, GROUND, W + 800, 10), paint(OUT, 140))
    for k in range(7):
        c.drawCircle(80 + k * 160, 300 + (k % 3) * 60, 50, paint("#3A2E24"))
    if snow and door == "night":
        # tuyết lùa vào trong hang
        for k in range(26):
            q = (t * 0.9 + k / 26) % 1
            x = 900 - q * 900
            y = 760 + (k * 41) % 480 + 40 * math.sin(q * 8 + k)
            c.drawCircle(x, y, 4 + k % 3, paint("#FFFFFF", 200 * (1 - q)))
    if fire_on:
        fire(c, fire_x, GROUND - 20, fire_s, t)


def bench(c, t, tone="#6E5642"):
    grad_rect(c, skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), "#4A3A2C", "#2A2018")
    glow = paint("#F39C12", 60); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 120))
    c.drawCircle(200, 700, 420, glow)
    st = skia.Path(); st.moveTo(-100, 1150); st.quadTo(300, 1010, 760, 1050); st.quadTo(1180, 1090, 1200, 1300)
    st.lineTo(1200, 2100); st.lineTo(-100, 2100); st.close()
    fo(c, st, "#8E969B", ow=8)
    c.drawLine(120, 1250, 420, 1210, P("#767E83", stroke=8)); c.drawLine(640, 1330, 980, 1290, P("#767E83", stroke=8))


def dust(c, x, y, t, t0, n=10, col="#D8CCB4", spread=1.0):
    age = t - t0
    if age < 0 or age > 0.9:
        return
    for k in range(n):
        ang = k * 2 * math.pi / n + 0.4
        r = age * 220 * spread
        c.drawCircle(x + r * math.cos(ang), y + r * math.sin(ang) * 0.6 - age * 60, 10 * (1 - age), P(col, 220 * (1 - age)))


def stars_burst(c, x, y, t, t0, n=5, r=120):
    age = t - t0
    if age < 0 or age > 0.8:
        return
    for k in range(n):
        ang = k * 2 * math.pi / n + age
        px, py = x + r * age * 1.4 * math.cos(ang), y + r * age * 1.4 * math.sin(ang)
        sp = skia.Path()
        for j in range(10):
            rr = 22 if j % 2 == 0 else 9
            aa = -math.pi / 2 + j * math.pi / 5
            (sp.moveTo if j == 0 else sp.lineTo)(px + rr * math.cos(aa), py + rr * math.sin(aa))
        sp.close(); fo(c, sp, "#F4D03F", ow=4, a=255 * (1 - age / 0.8))


