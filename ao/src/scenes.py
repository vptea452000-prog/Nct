"""Tập 3: Kim khâu và áo da — Bộp và Gầm (phim hài không lời), dựng bằng bộ khung nhân vật v2 (tools/rig.py)."""
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
    return "coat" if t >= T["wear"][0] + 0.35 else "tunic"


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


# ================================================================ CẢNH 1 — cửa hang, sáng sớm
GX, BX = 200, 760  # chỗ Gầm (trong miệng hang) và Bộp (ngoài trời)


def gam_cave(c, t, s=0.85, **kw):
    kw.setdefault("crouch", 1.0)
    kw.setdefault("outfit", "bare")
    return ch(c, "gam", GX, GROUND, s, t, face=1, **kw)


def bop_cold(c, t, s=0.85, x=BX, **kw):
    ta = t
    scratch = (math.sin(ta * 1.3) > 0.55)
    hr = (10 + 10 * math.sin(ta * 30), 250) if scratch else (-40, 110)
    kw.setdefault("hand_r", hr)
    kw.setdefault("hand_l", (90, 110))
    kw.setdefault("crouch", 1.0)
    kw.setdefault("shiver", 0.5)
    kw.setdefault("mouth", "chatter")
    kw.setdefault("eyes", "squint")
    kw.setdefault("brow_tilt", -0.8)
    return ch(c, "bop", x, GROUND, s, t, face=-1, outfit="tunic", **kw)


def sc_open(c, t):
    ta, u = loc("open", t)
    K = Cam(540, 1000, lerp(0.98, 1.06, ease_in_out(u))); K.on(c)
    exterior(c, t, wind=True)
    fire(c, 360, GROUND - 20, 0.45, t)
    gam_cave(c, t, cape=1.0, hold="spear", hand_r=(50, 60), hold_ang=-8, hold_len=460, eyes="closed", mouth="smile")
    bop_cold(c, t)
    flea(c, BX - 160, GROUND - 4, t)
    K.off(c)
    kinetic(c, "TẬP 3", W / 2, 360, t, T["open"][0] + 0.3, size=70, per=0.04)
    kinetic(c, "KIM KHÂU", W / 2, 490, t, T["open"][0] + 0.6, size=130, color="#F4C430", per=0.06)
    kinetic(c, "VÀ ÁO DA", W / 2, 630, t, T["open"][0] + 1.0, size=110, color="#F4C430", per=0.06)


def sc_inside(c, t):
    ta, u = loc("inside", t)
    K = Cam(lerp(300, 260, u), 1010, lerp(1.6, 1.75, ease_in_out(u))); K.on(c)
    exterior(c, t, wind=True)
    fire(c, 360, GROUND - 20, 0.45, t)
    gam_cave(c, t, cape=1.0, hold="spear", hand_r=(50, 60), hold_ang=-8, hold_len=460, hand_l=(150, 70),
             eyes="happy", mouth="smile", blush=0.4, head_tilt=8 * math.sin(ta * 2))
    K.off(c)


def sc_warm(c, t, n):
    ta, u = loc(n, t)
    K = Cam(470, 1000, 1.2); K.on(c)
    exterior(c, t, wind=True)
    fire(c, 360, GROUND - 20, 0.45, t)
    if n == "warm1":
        puff = ease_out(clamp(ta / 0.4))
        gam_cave(c, t, cape=1.0, hold="spear", hand_r=(60, 40), hold_ang=-8, hold_len=460, hand_l=(80, 60),
                 lean=-8 * puff, squash=1 + 0.04 * puff, eyes="squint", brow=0.5, mouth="smirk", look=(1, 0))
    else:
        gam_cave(c, t, cape=1.0, hold="spear", hand_r=(60, 40), hold_ang=-8, hold_len=460, hand_l=(60, -60),
                 lean=-10, head_tilt=-12, eyes="closed", brow=0.8, mouth="grin")
    bop_cold(c, t, eyes="open", look=(-1, 0), brow_tilt=-1.0, mouth="frown")
    K.off(c)
    say(c, n, K, GX, GROUND, 0.85, t, crouch=1.0, bx=420)


def sc_gust(c, t):
    ta, u = loc("gust", t)
    K = Cam(560, 1000, 1.0); K.on(c)
    c.save(); shake(c, t, T["gust"][0] + 0.3, 10, 0.6)
    exterior(c, t, wind=False, hide_on_tree=ta > 1.9)
    wind_lines(c, t, n=9, a=200, speed=1800, y0=520, dy=90)
    fire(c, 360, GROUND - 20, 0.45 * (1 - 0.4 * clamp((ta - 0.2) / 0.3)), t)
    off = ta > 0.7
    reach = ease_out(clamp((ta - 0.8) / 0.3))
    gam_cave(c, t, cape=0.0 if off else 1.0, cape_flap=clamp((ta - 0.2) / 0.3), hold="spear", hand_r=(60, 40), hold_ang=-8 - 10 * reach,
             hold_len=460, hand_l=(lerp(60, -150, reach), lerp(60, -140, reach)), eyes="wide", mouth="o", brow=1.0,
             lean=12 * clamp((ta - 0.2) / 0.3) if not off else -6 * reach, look=(-0.4, -1) if off else (0, 0), shiver=0.5 * off)
    bop_cold(c, t, eyes="wide", look=(0, -1) if off else (-1, 0), mouth="o", shiver=0.8)
    if off and ta < 1.95:
        q = clamp((ta - 0.7) / 1.2)
        hx = lerp(GX - 40, 930, ease_in_out(q))
        hy = lerp(1000, 600, q) - 380 * math.sin(math.pi * q)
        hide_sheet(c, hx, hy, 240, 170, rot=q * 540, flap=1.0, t=t)
    K.off(c)
    c.restore()
    sfx_word(c, "VÙ!", 760, 560, t, T["gust"][0] + 0.25, size=150, color="white", dur=0.8)
    sfx_word(c, "PHẦN PHẬT", 560, 380, t, T["gust"][0] + 1.0, size=80, color="#C9A06A", dur=0.9)


def sc_naked(c, t, n="naked"):
    ta, u = loc(n, t)
    K = Cam(230, 1000, 1.9); K.on(c)
    exterior(c, t, wind=False, hide_on_tree=True)
    wind_lines(c, t, n=5, a=120, speed=900, y0=700, dy=110)
    fire(c, 360, GROUND - 20, 0.35, t)
    talking = LS.talk("gam", t) > 0.02
    gam_cave(c, t, cape=0, shiver=1.0, mouth="chatter" if not talking else "flat", eyes="squint", brow_tilt=-1.0, brow=0.6,
             hand_l=(150, 90), hand_r=(-60, 100), blush=0.0, head_tilt=-4)
    # giọt nước mũi đóng băng
    nx, ny = GX + 20, GROUND - (560 - 60 - 230) * 0.85
    ice = skia.Path(); ice.moveTo(nx - 6, ny); ice.lineTo(nx + 6, ny); ice.lineTo(nx, ny + 26 * clamp(ta / 0.8)); ice.close()
    fo(c, ice, "#CFEFFF", ow=3)
    K.off(c)
    if n == "better":
        say(c, n, K, GX, GROUND, 0.85, t, crouch=1.0, bx=560, by=420)


# ================================================================ CẢNH 2 — Bộp làm kim
def sc_grind(c, t):
    ta, u = loc("grind", t)
    bench(c, t)
    sharp = clamp(ta / 2.0)
    dx = 120 * math.sin(ta * 9)
    needle(c, 560 + dx, 1080, 520, -8, sharp=sharp, hole=0, shine=pop(t, T["grind"][0] + 2.0, 0.3), t=t)
    big_hand(c, 250 + dx, 1230, 1.7, 60)
    for k in range(6):
        q = (ta * 3 + k / 6) % 1
        c.drawCircle(840 + dx * 0.3 + q * 90, 1090 - 70 * q + 20 * math.sin(k), 6 * (1 - q) + 2, P("#F3EBD8", 220 * (1 - q)))
    for k, ts in enumerate([0.2, 0.9, 1.6]):
        sfx_word(c, "XOẸT", 700 + (k % 2) * -180, 820 - k * 60, t, T["grind"][0] + ts, size=90, color="white", dur=0.6)


def bop_work(c, t, K=None, x=600, s=1.0, **kw):
    kw.setdefault("outfit", bop_outfit(t))
    kw.setdefault("face", -1)
    return ch(c, "bop", x, GROUND, s, t, **kw)


def sc_sharp(c, t, n):
    ta, u = loc(n, t)
    K = Cam(620, 1000, 1.45); K.on(c)
    exterior(c, t, wind=True, hide_on_tree=True)
    flat_stone(c, 470, GROUND, 1.2)
    if n == "sharp1":
        bop_work(c, t, hand_r=(70, -150), prop_r=needle_prop(-70, 110), eyes="open", look=(-0.6, -1), brow=0.6, mouth="smile")
        nx, ny = K.map(0, 0)
    else:
        bop_work(c, t, hand_r=(60, -30), prop_r=needle_prop(-50, 110), hand_l=(-90, -170), eyes="open", look=(-1, 0), brow=0.9,
                 brow_tilt=-0.3, head_tilt=-8)
    K.off(c)
    say(c, n, K, 600, GROUND, 1.0, t, who="bop", bx=520)


def sc_drill(c, t):
    ta, u = loc("drill", t)
    bench(c, t)
    needle(c, 600, 1060, 640, 0, sharp=1, hole=clamp((ta - 0.3) / 1.2), t=t)
    # mảnh đá sắc xoay
    rot = 40 * math.sin(ta * 16)
    with Xf(c, 330, 990, rot, 1.0):
        p = skia.Path(); p.moveTo(0, 30); p.lineTo(-40, -90); p.lineTo(30, -120); p.lineTo(50, -40); p.close()
        fo(c, p, "#9AA3A8", ow=6)
    big_hand(c, 330, 800, 1.5, 180 + rot * 0.5)
    for k in range(5):
        q = (ta * 2.5 + k / 5) % 1
        c.drawCircle(330 + (k - 2) * 30 * q, 1060 + q * 80, 6 * (1 - q) + 2, P("#F3EBD8", 220 * (1 - q)))
    sfx_word(c, "XOAY XOAY", 640, 700, t, T["drill"][0] + 0.3, size=90, color="white", dur=1.3)


def sc_hole(c, t):
    ta, u = loc("hole", t)
    bench(c, t)
    needle(c, 540, 1080, 700, -12, sharp=1, hole=1, shine=0.0, t=t)
    # ánh sáng xuyên qua lỗ
    hx, hy = 540 - 350 * math.cos(math.radians(12)) + 30, 1080 + 350 * math.sin(math.radians(12)) - 6
    g = paint("#FFF6C8", 180 * (0.6 + 0.4 * math.sin(ta * 6))); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
    c.drawCircle(hx, hy, 70, g)
    stars_burst(c, hx, hy, t, T["hole"][0] + 0.3)
    say_at(c, "hole", t, 540, 520, (hx, hy - 60))


def sc_thread(c, t):
    ta, u = loc("thread", t)
    bench(c, t)
    needle(c, 640, 1080, 640, 0, sharp=1, hole=1, t=t)
    ex = 640 - 320 + 24
    if ta < 1.0:
        # tước gân thành sợi mảnh
        q = ease_out(clamp(ta / 0.8))
        for k in range(4):
            off = (k - 1.5) * 26 * q
            sinew(c, 80, 1300 + off, 420, 1260 + off * 0.3, w=8 if q > 0.5 else 14, sag=10)
        sfx_word(c, "TƯỚC", 300, 1480, t, T["thread"][0] + 0.2, size=80, color="white", dur=0.7)
    else:
        q = ease_in_out(clamp((ta - 1.0) / 0.8))
        tipx = lerp(160, ex + 80, q)
        sinew(c, -60, 1180, tipx, lerp(1150, 1080, q), w=8, sag=30 * (1 - q))
        big_hand(c, tipx - 90, lerp(1230, 1170, q), 1.4, 70)
        stars_burst(c, ex, 1080, t, T["thread"][0] + 1.85, n=4, r=80)


def sc_stitch(c, t):
    ta, u = loc("stitch", t)
    bench(c, t)
    gap = lerp(70, 0, ease_out(clamp((ta - 1.9) / 0.4)))
    hide_sheet(c, 360, 1150 - gap, 520, 300, rot=-4, col="#A6855C")
    hide_sheet(c, 720, 1170 + gap, 520, 300, rot=3, col="#B8966A")
    n = min(3, int(ta / 0.6))
    for k in range(n):
        sx = 380 + k * 160
        c.drawLine(sx - 22, 1110, sx + 22, 1210, P("#F1E2C0", stroke=10))
        c.drawLine(sx - 22, 1110, sx + 22, 1210, P(OUT, 90, stroke=2))
    k = int(ta / 0.6)
    if k < 3:
        q = (ta % 0.6) / 0.6
        sx = 380 + k * 160
        ny = 1160 - 220 * (1 - abs(math.cos(q * math.pi)))
        needle(c, sx + 30, ny, 300, 70 if q < 0.5 else -110, thread=1, t=t, thread_len=200)
        sfx_word(c, "PHẬP", sx + 60, 820, t, T["stitch"][0] + k * 0.6 + 0.25, size=100, color="white", dur=0.45)
    else:
        needle(c, 900, 900, 300, -40, thread=1, t=t, thread_len=260)
        text(c, "1 · 2 · 3", W / 2, 700, "xbold", 80, "#F4C430", a=255 * pop(t, T["stitch"][0] + 1.9), align="center",
             stroke=8, stroke_color="#1A120D")


def sc_lead(c, t, n):
    ta, u = loc(n, t)
    K = Cam(560, 1000, 1.4); K.on(c)
    exterior(c, t, wind=True, hide_on_tree=True)
    if n == "lead1":
        sweep = math.sin(ta * 3)
        bop_work(c, t, hand_r=(90 + 60 * sweep, -120 - 30 * sweep), prop_r=needle_prop(-90 - 20 * sweep, 110, thread=1.0, t=t),
                 eyes="happy", mouth="smile", look=(-1, -0.5), head_tilt=6 * sweep)
    else:
        bop_work(c, t, hand_r=(80, -60), prop_r=needle_prop(-60, 110, thread=0.6, t=t), hand_l=(-60, -120 + 20 * math.sin(ta * 5)),
                 eyes="open", look=(-1, 0), brow=0.5)
    K.off(c)
    if n == "lead2":
        p = pop(t, T[n][0] + 0.5, 0.4)
        panel(c, 540, 1500, 860, 300, p)
        if p > 0.5:
            # trước: dùi chọc lỗ rồi luồn sợi | giờ: kim kéo sợi theo
            with Xf(c, 330, 1500, 0, 1):
                c.drawLine(-120, 40, 40, -60, P(OUT, stroke=20)); c.drawLine(-120, 40, 40, -60, P("#9AA3A8", stroke=12))
                sinew(c, -60, 70, 90, 50, w=6, sag=40)
                check_mark(c, 110, -70, False, pop(t, T[n][0] + 0.9))
            with Xf(c, 750, 1500, 0, 1):
                needle(c, 0, 0, 220, -20, thread=1, t=t, thread_len=140)
                check_mark(c, 120, -70, True, pop(t, T[n][0] + 1.3))
    say(c, n, K, 600, GROUND, 1.0, t, who="bop", bx=520)


# ================================================================ CẢNH 3 — chiếc áo đầu tiên
def coat_flat(c, x, y, s, sleeves=1.0, stitch=1.0, cut=1.0, col="#B08A5A"):
    with Xf(c, x, y, 0, s):
        if cut < 1:
            hide_sheet(c, 0, 0, 520, 440, col="#A6855C")
            dash = skia.Path(); dash.moveTo(-150, -170); dash.lineTo(150, -170); dash.lineTo(160, 180); dash.lineTo(-160, 180); dash.close()
            pe = P(OUT, stroke=6); pe.setPathEffect(skia.DashPathEffect.Make([24, 16], 0))
            c.drawPath(dash, pe)
            return
        if sleeves > 0:
            for sd in (-1, 1):
                with Xf(c, sd * 150, -140, sd * (60 - 20 * sleeves), 1):
                    fo(c, rrect_path(-50, 0, 100, 240 * sleeves, 30), "#9C7A4C", ow=6)
        body = skia.Path(); body.moveTo(-150, -170); body.lineTo(150, -170); body.lineTo(170, 190); body.quadTo(0, 220, -170, 190); body.close()
        fo(c, body, col, ow=7)
        n = int(8 * stitch)
        for k in range(n):
            for sd in (-1, 1):
                yy = -150 + k * 42
                c.drawLine(sd * 140 - 8, yy, sd * 140 + 8, yy + 12, P("#F1E2C0", stroke=5))
        fur = skia.Path(); fur.moveTo(-90, -170)
        for k in range(6):
            fur.quadTo(-90 + 180 * (k + 0.5) / 6, -200 - (k % 2) * 10, -90 + 180 * (k + 1) / 6, -170)
        fur.close(); fo(c, fur, "#E6D6B0", ow=5)


def sc_montage(c, t):
    ta, u = loc("montage", t)
    K = Cam(560, 1000, 1.3); K.on(c)
    exterior(c, t, wind=True, hide_on_tree=True)
    step = min(3, int(ta / 0.8)); q = (ta % 0.8) / 0.8
    if step == 0:
        bop_work(c, t, x=700, hand_r=(120, -60), hand_l=(-120, -60), eyes="open", look=(1, 0.5), mouth="flat", face=1)
        hide_sheet(c, 700, 1060, 300, 240, rot=0)
        pe = P("#F4C430", stroke=7); pe.setPathEffect(skia.DashPathEffect.Make([20, 12], 0))
        c.drawLine(560, 990 + q * 120, 840, 990 + q * 120, pe)
    else:
        bop_work(c, t, x=820, hand_r=(90, 60 + 40 * math.sin(ta * 20)), prop_r=needle_prop(-30, 90, thread=1, t=t) if step >= 2 else None,
                 eyes="squint", look=(-1, 1), mouth="tongue", crouch=0.6)
        if step == 1:
            coat_flat(c, 470, 1150, 0.7, cut=0.0)
            with Xf(c, lerp(380, 560, q), lerp(1030, 1270, q), 30, 0.8):
                p = skia.Path(); p.moveTo(0, 30); p.lineTo(-40, -90); p.lineTo(30, -120); p.lineTo(50, -40); p.close()
                fo(c, p, "#9AA3A8", ow=6)
        else:
            coat_flat(c, 470, 1150, 0.7, sleeves=0.0 if step == 2 else ease_out(q * 1.5), stitch=q if step == 2 else 1.0)
    K.off(c)
    ff_badge(c, t)
    labels = ["ĐO", "CẮT", "KHÂU SƯỜN", "TAY ÁO"]
    text(c, labels[step], W / 2, 470, "xbold", 110, "#F4C430", align="center", stroke=10, stroke_color="#1A120D")
    text(c, f"{step + 1}/4", W / 2, 580, "xbold", 60, "white", align="center", stroke=6, stroke_color="#1A120D")


def sc_wear(c, t):
    ta, u = loc("wear", t)
    K = Cam(620, 1000, 1.4); K.on(c)
    exterior(c, t, wind=True, hide_on_tree=True)
    on = ta > 0.35
    cu = ease_out(clamp((ta - 0.6) / 0.5))
    ch(c, "bop", 640, GROUND, 1.0, t, face=-1, outfit="coat" if on else "tunic", collar_up=cu,
       hand_r=(-20, -40) if on else (60, -200), hand_l=(40, -40) if on else (-60, -200), eyes="happy" if on else "closed",
       mouth="smile", squash=1 + 0.08 * math.exp(-max(0, ta - 0.35) * 8) * on, feet_air=40 * math.sin(math.pi * clamp(ta / 0.35)) if not on else 0)
    if 0.2 < ta < 0.8:
        g = (ta - 0.2) / 0.6
        for k in range(9):
            ang = k * 0.7
            c.drawCircle(640 + 180 * g * math.cos(ang), 1050 + 120 * g * math.sin(ang), 70 * (1 - g) + 20, P("#FFFFFF", 230 * (1 - g)))
    K.off(c)
    sfx_word(c, "XOẠT!", 820, 600, t, T["wear"][0] + 0.3, size=110, color="white", dur=0.6)


def sc_nofly(c, t):
    ta, u = loc("nofly", t)
    K = Cam(620, 1000, 1.4); K.on(c)
    exterior(c, t, wind=False, hide_on_tree=True)
    wind_lines(c, t, n=9, a=200, speed=1800, y0=520, dy=90)
    ch(c, "bop", 640, GROUND, 1.0, t, face=-1, outfit="coat", collar_up=1.0, hand_r=(-20, 60), hand_l=(40, 60),
       eyes="closed" if ta < 1.2 else "happy", mouth="o" if 1.2 < ta < 1.8 else "smile", lag=6 * math.sin(t * 20))
    K.off(c)
    hx, hy = K.map(600, GROUND - 330)
    breath(c, hx, hy, t, T["nofly"][0] + 1.2, dirx=-1)
    sfx_word(c, "VÙ…", 300, 560, t, T["nofly"][0] + 0.1, size=100, color="white", dur=0.9)


def body_icon(c, x, y, mode, t, p=1.0):
    """Sơ đồ: người khoác hờ (gió lùa) / áo ôm sát (giữ lớp hơi ấm)."""
    with Xf(c, x, y, 0, 1):
        c.drawCircle(0, -120, 40, P("#8A5A3C")); c.drawCircle(0, -120, 40, P(OUT, stroke=5))
        body = skia.Path(); body.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-50, -80, 100, 170), 40, 40))
        if mode == "loose":
            fo(c, body, "#8A5A3C", ow=5)
            cape = skia.Path(); cape.moveTo(-60, -80); cape.lineTo(60, -80); cape.lineTo(110, 110); cape.lineTo(-30, 80); cape.close()
            fo(c, cape, "#A6855C", ow=5, a=230)
            for k in range(3):
                q = (t * 1.2 + k / 3) % 1
                xx = 160 - q * 260
                c.drawLine(xx, -40 + k * 50, xx + 50, -40 + k * 50, P("#5DADE2", 255 * p, stroke=8))
                tri = skia.Path(); tri.moveTo(xx - 14, -40 + k * 50); tri.lineTo(xx + 4, -52 + k * 50); tri.lineTo(xx + 4, -28 + k * 50); tri.close()
                c.drawPath(tri, P("#5DADE2", 255 * p))
        else:
            glow = P("#F39C12", 150 * p); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
            c.drawRoundRect(skia.Rect.MakeXYWH(-62, -92, 124, 194), 46, 46, glow)
            fo(c, body, "#B08A5A", ow=5)
            for k in range(3):
                q = (t * 1.2 + k / 3) % 1
                xx = 180 - q * 110
                bend = max(0, q - 0.7) * 300
                c.drawLine(xx, -40 + k * 50, xx + 50, -40 + k * 50 - bend, P("#5DADE2", 255 * p * (1 - max(0, q - 0.8) * 5), stroke=8))


def sc_fit(c, t, n):
    ta, u = loc(n, t)
    K = Cam(620, 980, 1.3); K.on(c)
    exterior(c, t, wind=True, hide_on_tree=True)
    ch(c, "bop", 660, GROUND, 1.0, t, face=-1, outfit="coat", collar_up=1.0,
       hand_r=(60, -60) if n == "fit1" else (-30, 40), hand_l=(-70, 30) if n == "fit1" else (-120, -140),
       eyes="open", look=(-1, 0), brow=0.4, mouth="smile")
    K.off(c)
    p = pop(t, T["fit1"][0] + 0.4, 0.4)
    panel(c, 540, 1530, 900, 420, p)
    if p > 0.5:
        body_icon(c, 330, 1560, "loose", t)
        body_icon(c, 750, 1560, "tight", t)
        check_mark(c, 440, 1410, False, pop(t, T["fit1"][0] + 0.9))
        check_mark(c, 860, 1410, True, pop(t, T["fit1"][0] + 1.2))
    say(c, n, K, 660, GROUND, 1.0, t, who="bop", bx=540, by=360)


TWOX_G, TWOX_B = 330, 760


def leaves_on(c, x, y, s):
    for k, (dx, rot) in enumerate([(-50, -30), (10, 20), (60, -10)]):
        with Xf(c, x + dx * s, y + (k % 2) * 10, rot, s):
            lf = skia.Path(); lf.moveTo(0, 0); lf.quadTo(20, -20, 40, 0); lf.quadTo(20, 16, 0, 0); lf.close()
            fo(c, lf, "#6E8A3A", ow=3)


def two_shot(c, t, gkw=None, bkw=None, K=None, gx=TWOX_G, bx=TWOX_B, leaves=True, snow=0.0):
    K = K or Cam(545, 1000, 1.15)
    K.on(c)
    exterior(c, t, wind=snow == 0, hide_on_tree=False, snow=snow, falling=40 if snow else 0)
    gkw = dict(gkw or {}); bkw = dict(bkw or {})
    gkw.setdefault("outfit", "bare")
    bkw.setdefault("outfit", bop_outfit(t)); bkw.setdefault("collar_up", 1.0)
    ch(c, "bop", bx, GROUND, 0.95, t, face=-1, **bkw)
    ch(c, "gam", gx, GROUND, 0.95, t, face=1, **gkw)
    if leaves:
        leaves_on(c, gx, GROUND - 560 * 0.95 + 10, 0.95)
    return K


def sc_sack(c, t):
    ta, u = loc("sack", t)
    walk_in = ease_out(clamp(ta / 0.8))
    gx = lerp(-200, TWOX_G, walk_in)
    laugh = ta > 1.0
    K = two_shot(c, t, gx=gx, gkw=dict(walk=ta * 9 if ta < 0.8 else None, prop_l=hide_prop, hand_l=(-40, 40),
                                       hand_r=(150, -70) if laugh else None, eyes="squint", mouth="grin", brow=0.6,
                                       lean=-6 * laugh + 3 * math.sin(ta * 14) * laugh),
                 bkw=dict(eyes="open", look=(-1, 0), mouth="flat"))
    K.off(c)
    say(c, "sack", K, gx, GROUND, 0.95, t, bx=540)


def sc_sleeve(c, t, n):
    ta, u = loc(n, t)
    if n == "sleeve1":
        bk = dict(hand_l=(140, -10), hand_r=(70, 80), eyes="open", look=(-1, 0), mouth="smile", brow=0.3)
    else:
        up = back_out(clamp(ta / 0.4))
        bk = dict(hand_l=(lerp(-40, -110, up), lerp(60, -230, up)), hand_r=(lerp(40, 110, up), lerp(60, -230, up)), eyes="happy",
                  mouth="grin", feet_air=30 * math.sin(math.pi * clamp(ta / 0.4)))
    K = two_shot(c, t, gkw=dict(prop_l=hide_prop, hand_l=(-40, 40), eyes="open", look=(1, 0), brow=-0.3, mouth="frown"), bkw=bk)
    K.off(c)
    say(c, n, K, TWOX_B, GROUND, 0.95, t, who="bop", bx=640)


def sc_fight(c, t):
    ta, u = loc("fight", t)
    pa = math.sin(ta * 14)
    K = two_shot(c, t, gkw=dict(hand_r=(lerp(40, 190, max(0, pa)), -90), hand_l=(lerp(60, 170, max(0, -pa)), -110), vein=1.0,
                                eyes="angry", brow=-0.4, brow_tilt=1.0, mouth="shout", lean=6 * pa, feet_air=10 * abs(pa)),
                 bkw=dict(eyes="wide", look=(-1, 0), mouth="o", lean=6, sweat=0.6))
    K.off(c)
    sfx_word(c, "HỰ! HỰ!", 330, 1500, t, T["fight"][0] + 0.4, size=90, color="white", dur=1.6)
    say(c, "fight", K, TWOX_G, GROUND, 0.95, t, bx=540)


def sc_grab(c, t):
    ta, u = loc("grab", t)
    snatch = clamp(ta / 0.3)
    back = ease_out(clamp((ta - 0.35) / 0.3))
    has = ta > 0.3
    if not has:
        ghr = (lerp(60, 330, ease_out(snatch)), lerp(-40, -60, snatch))
    else:
        ghr = (lerp(330, 110, back), lerp(-60, -210, back))
    K = two_shot(c, t, K=Cam(500, 1000, 1.3),
                 gkw=dict(hand_r=ghr, prop_r=needle_prop(-80, 90) if has else None, eyes="squint", look=(0.6, -0.6), mouth="smirk",
                          brow=0.6, head_tilt=-6 * back),
                 bkw=dict(hand_r=(80, -40), prop_r=None if has else needle_prop(-60, 90), eyes="wide" if has else "open", look=(-1, 0),
                          mouth="o" if has else "flat"))
    K.off(c)
    sfx_word(c, "VỤT!", 560, 820, t, T["grab"][0] + 0.25, size=100, color="white", dur=0.5)
    say(c, "grab", K, TWOX_G, GROUND, 0.95, t, bx=440, d=0.5)


def sc_broken(c, t):
    ta, u = loc("broken", t)
    K = Cam(360, 900, 2.0); K.on(c)
    exterior(c, t, wind=True)
    ch(c, "gam", TWOX_G, GROUND, 0.95, t, face=1, outfit="bare", hand_r=(130, -230 + 10 * math.sin(ta * 20)), prop_r=needle_prop(-90, 90),
       eyes="angry", brow=-0.5, brow_tilt=1.0, mouth="shout", vein=1.0, head_tilt=-4)
    leaves_on(c, TWOX_G, GROUND - 560 * 0.95 + 10, 0.95)
    K.off(c)
    say(c, "broken", K, TWOX_G, GROUND, 0.95, t, bx=540, by=320)


def sc_useless(c, t):
    ta, u = loc("useless", t)
    K = two_shot(c, t, gkw=dict(hand_r=(150, -150), prop_r=needle_prop(-90, 90), eyes="angry", brow_tilt=1.0, mouth="shout", vein=1.0,
                                lean=8, feet_air=20 * abs(math.sin(ta * 8))),
                 bkw=dict(eyes="open", brow_tilt=-1.0, mouth="frown", look=(-1, 0)))
    K.off(c)
    c.save(); shake(c, t, T["useless"][0] + 0.15, 14)
    say(c, "useless", K, TWOX_G, GROUND, 0.95, t, bx=400)
    c.restore()


def rock_crack(c, x, y, s=1.0):
    with Xf(c, x, y, 0, s):
        rock = skia.Path(); rock.moveTo(-600, 400); rock.lineTo(-600, -120); rock.quadTo(-300, -260, 0, -200); rock.quadTo(400, -280, 700, -100)
        rock.lineTo(700, 400); rock.close()
        fo(c, rock, "#8A7E70", ow=8)
        cr = skia.Path(); cr.moveTo(-40, -205); cr.lineTo(-20, -60); cr.lineTo(-50, 80); cr.lineTo(-10, 400); cr.lineTo(30, 400)
        cr.lineTo(10, 80); cr.lineTo(40, -60); cr.lineTo(30, -210); cr.close()
        fo(c, cr, "#1A1410", ow=6)


def sc_flick(c, t):
    ta, u = loc("flick", t)
    if ta < 0.7:
        K = two_shot(c, t, gkw=dict(hand_r=(lerp(110, 170, clamp(ta / 0.2)), lerp(-210, -170, clamp(ta / 0.2))),
                                    prop_r=needle_prop(-90, 90) if ta < 0.2 else None, eyes="angry", mouth="smirk"),
                     bkw=dict(eyes="wide", look=(-0.5, -1), mouth="o"))
        if ta > 0.2:
            q = (ta - 0.2) / 0.5
            needle(c, lerp(520, 1150, q), 760 - 300 * math.sin(math.pi * q * 0.8), 90, q * 1440, t=t)
        K.off(c)
        sfx_word(c, "BÚNG!", 400, 640, t, T["flick"][0] + 0.15, size=100, color="white", dur=0.5)
        sfx_word(c, "VÈO", 800, 480, t, T["flick"][0] + 0.3, size=110, color="#F4C430", dur=0.5)
    else:
        q = clamp((ta - 0.7) / 0.6)
        grad_rect(c, skia.Rect.MakeWH(W, H), "#9FC9E6", "#F6E7C0")
        rock_crack(c, 540, 1300, 1.0)
        if q < 1:
            needle(c, lerp(1100, 525, ease_in_out(q)), lerp(500, 1090, q ** 1.6), 260, lerp(0, 92, q) + 720 * (1 - q), t=t)
        dust(c, 525, 1100, t, T["flick"][0] + 1.3, n=8, col="#C9BBA6")
        sfx_word(c, "LỌT THỎM", 540, 600, t, T["flick"][0] + 1.35, size=110, color="white", dur=0.7)


def sc_long(c, t):
    ta, u = loc("long", t)
    K = Cam(760, 920, 1.9); K.on(c)
    exterior(c, t, wind=True)
    lf = ease_out(clamp(ta / 0.6))
    ch(c, "bop", TWOX_B, GROUND, 0.95, t, face=-1, outfit="coat", collar_up=1.0, head_squash=1 + 0.45 * lf, eyes="open",
       look=(-0.5, 1), brow=0.6 * lf, brow_tilt=-1.2, mouth="frown", head_tilt=-4)
    # đám mây u ám nhỏ
    cx_, cy_ = TWOX_B, GROUND - 760 - 20 * math.sin(ta * 2)
    for dx, r in [(-40, 40), (0, 54), (44, 38)]:
        c.drawCircle(cx_ + dx, cy_, r * lf, P("#6A7280"))
    for k in range(4):
        q = (ta * 1.8 + k / 4) % 1
        c.drawLine(cx_ - 40 + k * 26, cy_ + 40 + q * 120, cx_ - 44 + k * 26, cy_ + 60 + q * 120, P("#5DADE2", 255 * lf * (1 - q), stroke=5))
    K.off(c)
    say(c, "long", K, TWOX_B, GROUND, 0.95, t, who="bop", bx=540, by=320)


# ================================================================ CẢNH 4 — đêm, bão tuyết
NG, NB = 360, 20   # Gầm bên đống lửa, Bộp ngủ trong góc


def slip_cycle(ta, period):
    q = (ta % period) / period
    if q < 0.6:
        return ease_in_out(q / 0.6), False
    return 1 - ease_out((q - 0.6) / 0.4), True


def sleeping_bop(c, t, **kw):
    kw.setdefault("eyes", "closed"); kw.setdefault("mouth", "o"); kw.setdefault("talk", 0.15 + 0.1 * math.sin(t * 2.5))
    kw.setdefault("head_tilt", -10 + 4 * math.sin(t * 1.2)); kw.setdefault("crouch", 1.0)
    kw.setdefault("hand_l", (90, 100)); kw.setdefault("hand_r", (-30, 100))
    return ch(c, "bop", NB, GROUND, 0.9, t, face=1, outfit="coat", collar_up=1.0, **kw)


def sc_storm(c, t, n):
    ta, u = loc(n, t)
    K = Cam(470, 1000, 1.3); K.on(c)
    cave_in(c, t, door="night")
    period = 0.85 if n == "storm" else 0.62
    drop, yank = slip_cycle(ta, period)
    ch(c, "gam", NG, GROUND, 0.95, t, face=1, outfit="bare", crouch=1.0, cape=1.0, cape_drop=drop, cape_flap=0.4,
       hand_r=(-20, -120) if yank else (60, 90), hand_l=(90, -110) if yank else (120, 90), shiver=0.6 * drop,
       eyes="squint" if n == "storm" else "angry", brow_tilt=0.4 if n == "storm" else 1.0, mouth="frown" if n == "storm" else "wavy",
       vein=0.0 if n == "storm" else 0.8)
    K.off(c)
    snowfall(c, t, 25, wind=-1.0, a=160)
    if n == "storm":
        sfx_word(c, "TUỘT…", 600, 560, t, T[n][0] + 0.4, size=90, color="white", dur=0.7)
    else:
        sfx_word(c, "LẠI TUỘT!", 600, 560, t, T[n][0] + 0.3, size=90, color="white", dur=0.9)


def sc_stay(c, t):
    ta, u = loc("stay", t)
    K = Cam(420, 980, 1.5); K.on(c)
    cave_in(c, t, door="night")
    drop = ease_in_out(clamp((ta - 1.7) / 0.5))
    ch(c, "gam", NG, GROUND, 0.95, t, face=1, outfit="bare", crouch=0.4, cape=1.0, cape_drop=drop, cape_flap=0.3,
       hand_r=(-90 + 20 * math.sin(ta * 10), 40), hand_l=(80, 60), head_tilt=-14, look=(-1, 0.6), eyes="angry", brow_tilt=1.0,
       mouth="shout", vein=1.0)
    K.off(c)
    snowfall(c, t, 25, wind=-1.0, a=160)
    say(c, "stay", K, NG, GROUND, 0.95, t, crouch=0.4, bx=540)


def sc_burn(c, t):
    ta, u = loc("burn", t)
    K = Cam(470, 1000, 1.3); K.on(c)
    c.save(); shake(c, t, T["burn"][0] + 0.15, 10, 0.4)
    cave_in(c, t, door="night", fire_s=0.7 + 0.25 * clamp((ta - 0.6) / 0.2) * (ta < 1.3))
    flying = 0.2 < ta < 0.7
    pulled = ta > 1.3
    if pulled:
        lift = back_out(clamp((ta - 1.3) / 0.35))
        ch(c, "gam", NG + 40, GROUND, 0.95, t, face=1, outfit="bare", crouch=0.2, hand_r=(150, -200), hand_l=(160, -160),
           eyes="wide", mouth="o", brow=1.0, sweat=1.0)
        hx, hy = NG + 190, GROUND - 440 * lift - 40
        hide_sheet(c, hx, hy, 300, 230, rot=4 * math.sin(ta * 6), hole=True, col="#7A5A3A", dark="#3A2A1A")
        smoke(c, hx, hy - 100, t, T["burn"][0] + 1.3, n=6, a=150)
    else:
        ch(c, "gam", NG, GROUND, 0.95, t, face=1, outfit="bare", crouch=1.0, cape=0.0 if ta > 0.2 else 1.0, cape_flap=1.0,
           hand_r=(150, -40) if ta > 0.5 else (60, 90), hand_l=(170, -20) if ta > 0.5 else (120, 90), eyes="wide", mouth="o", brow=1.0,
           lean=10 if ta > 0.5 else 0)
        if flying:
            q = (ta - 0.2) / 0.5
            hide_sheet(c, lerp(NG - 20, 540, q), lerp(1050, 1230, q) - 120 * math.sin(math.pi * q), 230, 170, rot=q * 200, flap=1.0, t=t)
        elif ta >= 0.7:
            hide_sheet(c, 540, 1240, 250, 120, rot=-6, col="#5A4030", dark="#3A2A1A")
            sp = paint("#1A1A1A", 200)
            for k in range(7):
                age = (ta - 0.7) - k * 0.07
                if age > 0:
                    pt = paint("#222222", 220 * clamp(1 - age / 1.2)); pt.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8))
                    c.drawCircle(540 + 40 * math.sin(k * 2), 1180 - age * 300, 40 + age * 70, pt)
    K.off(c)
    c.restore()
    sfx_word(c, "VÙ!", 760, 600, t, T["burn"][0] + 0.1, size=130, color="white", dur=0.5)
    sfx_word(c, "XÈÈÈ!", 540, 760, t, T["burn"][0] + 0.75, size=110, color="#F4C430", dur=0.6)


def sc_snore(c, t):
    ta, u = loc("snore", t)
    K = Cam(lerp(360, 190, ease_in_out(clamp(ta / 0.8))), 1000, 1.6); K.on(c)
    cave_in(c, t, door="night")
    sleeping_bop(c, t)
    ch(c, "gam", NG, GROUND, 0.95, t, face=-1, outfit="bare", crouch=0.8, shiver=0.7, eyes="squint", look=(1, 0.3), brow_tilt=0.6,
       mouth="chatter", hand_l=(100, 80), hand_r=(-40, 90))
    hx, hy = NB + 30, GROUND - 450 * 0.9
    bub = 18 + 14 * math.sin(t * 2.5)
    c.drawCircle(hx, hy, bub, P("#DDF3FF", 200)); c.drawCircle(hx, hy, bub, P(OUT, 140, stroke=3))
    zzz(c, NB + 40, GROUND - 600, t)
    K.off(c)
    sfx_word(c, "KHÒ… KHÒ…", 400, 600, t, T["snore"][0] + 0.2, size=90, color="white", dur=1.6)


def sc_sneak(c, t):
    ta, u = loc("sneak", t)
    K = Cam(200, 1000, 1.5); K.on(c)
    cave_in(c, t, door="night")
    sleeping_bop(c, t)
    gx = lerp(NG + 40, NB + 170, ease_in_out(u))
    ch(c, "gam", gx, GROUND, 0.95, t, face=-1, outfit="bare", crouch=0.5, walk=ta * 5, stride=1.4, feet_air=0,
       hand_r=(90, -120 + 20 * math.sin(ta * 5)), hand_l=(130, -100 + 20 * math.cos(ta * 5)), eyes="squint", look=(math.sin(ta * 4), 0),
       brow=0.6, mouth="smirk", lean=10)
    K.off(c)
    sfx_word(c, "RÓN RÉN", 560, 560, t, T["sneak"][0] + 0.3, size=90, color="#C9A06A", dur=1.6)


def stuck_pair(c, t, ta, bop_awake=False, gam_face="strain"):
    wig = math.sin(ta * 9) * (1.0 if not bop_awake else 0.4)
    bx_, gx_ = NB + 20, NB + 120
    ch(c, "gam", gx_, GROUND, 0.9, t, face=-1, outfit="bare", lean=-18 + 4 * wig, crouch=0.3, head_dx=-10,
       head_squash=0.9, eyes="squint" if gam_face == "strain" else "wide", mouth="chatter" if gam_face == "strain" else "smile",
       sweat=1.0, blush=0.6 if gam_face != "strain" else 0.0, hand_r=(140, -30), hand_l=(60, 60))
    ch(c, "bop", bx_, GROUND, 0.9, t, face=1, outfit="coat", collar_up=1.0, crouch=0.6,
       eyes="wide" if bop_awake else "closed", mouth="shout" if bop_awake else "o", brow=1.0 if bop_awake else 0.0,
       hand_l=(90, 100), hand_r=(-30, 100), head_dx=-8 if bop_awake else 0)
    # chiếc áo bị kéo căng trùm cả hai người
    cx_, cy_ = (bx_ + gx_) / 2, GROUND - 240 * 0.9
    blob = skia.Path()
    n = 24
    for k in range(n + 1):
        a = k * 2 * math.pi / n
        r = 1 + 0.05 * math.sin(a * 3 + ta * 10) * (1 if not bop_awake else 0.3)
        x = cx_ + 150 * r * math.cos(a) + 10 * wig
        y = cy_ + 120 * r * math.sin(a)
        (blob.moveTo if k == 0 else blob.lineTo)(x, y)
    blob.close()
    fo(c, blob, rig.COAT["bop"][0], ow=7)
    for k in range(6):
        yy = cy_ - 80 + k * 30
        c.drawLine(cx_ - 120 - 8, yy, cx_ - 120 + 8, yy + 10, P("#F1E2C0", stroke=4))
    # căng chỉ
    for k in range(3):
        c.drawLine(cx_ - 30 + k * 30, cy_ - 50, cx_ - 20 + k * 30, cy_ + 50, P(rig.COAT["bop"][1], stroke=4))
    # tay Gầm thò ra ống tay áo
    sl = skia.Path(); sl.moveTo(cx_ + 120, cy_ - 40); sl.lineTo(cx_ + 240 + 6 * wig, cy_ - 120); sl.lineTo(cx_ + 260 + 6 * wig, cy_ - 80)
    sl.lineTo(cx_ + 130, cy_ + 10); sl.close()
    fo(c, sl, rig.COAT["bop"][1], ow=6)
    fo(c, oval(cx_ + 262 + 6 * wig, cy_ - 108, 26, 24), rig.STYLES["gam"]["skin"], ow=6)
    fur = skia.Path(); fur.moveTo(cx_ - 120, cy_ - 104)
    for k in range(8):
        fur.quadTo(cx_ - 120 + 240 * (k + 0.5) / 8, cy_ - 124 - (k % 2) * 12, cx_ - 120 + 240 * (k + 1) / 8, cy_ - 104)
    fur.close(); fo(c, fur, "#E6D6B0", ow=5)


def sc_stuck(c, t):
    ta, u = loc("stuck", t)
    K = Cam(130, 1000, 1.7); K.on(c)
    c.save(); shake(c, t, T["stuck"][0] + 0.6, 6, 1.6)
    cave_in(c, t, door="night", fire_x=540)
    stuck_pair(c, t, ta)
    K.off(c)
    c.restore()
    sfx_word(c, "KẸT!", 760, 640, t, T["stuck"][0] + 0.5, size=130, color="#F4C430", dur=0.8)
    sfx_word(c, "RỘT RỘT", 540, 1560, t, T["stuck"][0] + 1.2, size=80, color="white", dur=1.4)


def sc_wake(c, t, n):
    ta, u = loc(n, t)
    K = Cam(130, 980, 1.7); K.on(c)
    cave_in(c, t, door="night", fire_x=540)
    stuck_pair(c, t, ta + 3, bop_awake=True, gam_face="strain" if n == "wake" else "sheepish")
    K.off(c)
    if n == "wake":
        say(c, n, K, NB + 20, GROUND, 0.9, t, who="bop", crouch=0.6, bx=500)
    else:
        say(c, n, K, NB + 120, GROUND, 0.9, t, who="gam", bx=560)


# ================================================================ CẢNH 5 — Gầm tự khâu
SG, SB = 360, 800


def sc_find(c, t):
    ta, u = loc("find", t)
    grad_rect(c, skia.Rect.MakeWH(W, H), "#9FC9E6", "#F6E7C0")
    rock_crack(c, 540, 1300, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-100, 1060, W + 200, 30), P("#FFFFFF"))
    up = ease_out(clamp((ta - 0.5) / 0.7))
    needle(c, 528, lerp(1180, 820, up), 260, -92 + 30 * up, t=t, shine=pop(t, T["find"][0] + 1.2, 0.3))
    big_hand(c, 560, lerp(1120, 770, up) - 170, 1.6, 180, skin=rig.STYLES["gam"]["skin"])
    snowfall(c, t, 30, wind=0.2)
    sfx_word(c, "A HA!", 760, 520, t, T["find"][0] + 1.2, size=130, color="#F4C430", dur=0.8)


def ground_hide(c, x, y, s=1.0):
    hide_sheet(c, x, y, 420 * s, 110 * s, col="#A6855C")


def sc_sew(c, t):
    ta, u = loc("sew", t)
    K = Cam(520, 1000, 1.3); K.on(c)
    exterior(c, t, wind=False, snow=1.0, falling=30)
    ground_hide(c, SG, GROUND + 30)
    st = abs(math.sin(ta * math.pi / 0.8 * 1.0))
    ch(c, "gam", SG, GROUND, 0.95, t, face=1, outfit="bare", crouch=1.0, shiver=0.3,
       hand_r=(120, lerp(120, -80, st)), prop_r=needle_prop(lerp(-60, 60, st), 90, thread=1, t=t), hand_l=(160, 110),
       eyes="squint", look=(1, 1), mouth="tongue", brow=-0.3, head_tilt=8)
    hide_sheet(c, SG + 120, GROUND - 230, 200, 140, rot=8, col="#9A7450", stitches=min(6, int(ta / 0.4)))
    ch(c, "bop", SB, GROUND, 0.9, t, face=-1, outfit="coat", collar_up=1.0, crouch=1.0, eyes="open", look=(-1, 0.4), mouth="flat",
       hand_l=(90, 100), hand_r=(-30, 100))
    K.off(c)
    for k in range(3):
        sfx_word(c, "PHẬP", 360 + k * 170, 640 - k * 40, t, T["sew"][0] + 0.4 + k * 0.7, size=100, color="white", dur=0.45)


def drag_hide(c, x, y, s, face, t, walking=False):
    """Tấm da bị khâu dính sau lưng, kéo lê trên đất như cái đuôi."""
    bx_, by_ = x - face * 60 * s, y - 220 * s
    tail = skia.Path()
    wob = 10 * math.sin(t * 9) if walking else 0
    tail.moveTo(bx_, by_ - 40 * s)
    tail.cubicTo(bx_ - face * 120 * s, by_ + 40 * s, bx_ - face * 200 * s, y - 20 + wob, bx_ - face * 420 * s, y + 10)
    tail.lineTo(bx_ - face * 440 * s, y + 40 * s)
    tail.cubicTo(bx_ - face * 180 * s, y + 30 * s, bx_ - face * 60 * s, by_ + 120 * s, bx_ + face * 10 * s, by_ + 60 * s)
    tail.close()
    fo(c, tail, "#A6855C", ow=6)
    for k in range(5):
        q = k / 5
        c.drawLine(bx_ - face * 10 * s, by_ - 30 * s + q * 90 * s, bx_ + face * 10 * s, by_ - 20 * s + q * 90 * s, P("#F1E2C0", stroke=5))


def sc_done(c, t):
    ta, u = loc("done", t)
    K = Cam(520, 1000, 1.3); K.on(c)
    exterior(c, t, wind=False, snow=1.0, falling=30)
    up = back_out(clamp(ta / 0.4))
    drag_hide(c, SG, GROUND, 0.95, 1, t)
    ch(c, "gam", SG, GROUND, 0.95, t, face=1, outfit="coat", crouch=1 - up, hand_l=(lerp(60, -120, up), lerp(60, -220, up)),
       hand_r=(lerp(60, 120, up), lerp(60, -220, up)), prop_r=needle_prop(-90, 90), eyes="happy", mouth="grin", head_tilt=-8)
    ch(c, "bop", SB, GROUND, 0.9, t, face=-1, outfit="coat", collar_up=1.0, crouch=1.0, eyes="open", look=(-1, 0), mouth="flat",
       hand_l=(90, 100), hand_r=(-30, 100))
    K.off(c)
    say(c, "done", K, SG, GROUND, 0.95, t, bx=440)


def sc_tail(c, t):
    ta, u = loc("tail", t)
    K = Cam(540, 1000, 1.2); K.on(c)
    exterior(c, t, wind=False, snow=1.0, falling=30)
    turn = ta < 0.3
    gx = SG if ta < 0.5 else lerp(SG, SG + 260, ease_in_out(clamp((ta - 0.5) / 2.2)))
    face = 1
    if ta > 0.3:
        drag_hide(c, gx, GROUND, 0.95, face, t, walking=ta > 0.5)
    ch(c, "gam", gx, GROUND, 0.95, t, face=face, turn=0.35 if not turn else 0.0, outfit="coat", walk=ta * 6 if ta > 0.5 else None,
       hand_l=(-30, -230), hand_r=(110, -100), prop_r=needle_prop(-90, 90), eyes="closed", mouth="grin", head_tilt=-10, lean=-6)
    laugh = ta > 0.9
    ch(c, "bop", SB + 80, GROUND, 0.9, t, face=-1, outfit="coat", collar_up=1.0, crouch=1.0, eyes="squint" if laugh else "wide",
       look=(1, 0.5), mouth="flat", blush=1.0 * laugh, hand_r=(30, -170) if laugh else (-30, 100), hand_l=(90, -150) if laugh else (90, 100),
       shiver=0.5 * laugh, head_squash=1 - 0.05 * laugh)
    K.off(c)
    sfx_word(c, "SỘT… SỘT…", 400, 1520, t, T["tail"][0] + 0.8, size=80, color="#8A7A52", dur=2.0)
    if laugh:
        sfx_word(c, "PHÌ…", 900, 760, t, T["tail"][0] + 1.6, size=80, color="white", dur=0.8)


def sc_fix(c, t):
    ta, u = loc("fix", t)
    K = Cam(560, 1000, 1.25); K.on(c)
    exterior(c, t, wind=False, snow=1.0, falling=30)
    ch(c, "gam", 230, GROUND, 0.95, t, face=1, outfit="bare", shiver=1.0, mouth="chatter", eyes="squint", hand_l=(100, 80), hand_r=(-40, 90),
       brow_tilt=-0.8)
    ch(c, "bop", 820, GROUND, 0.9, t, face=-1, outfit="coat", collar_up=1.0, crouch=0.8, hand_r=(80, 80 + 60 * math.sin(ta * 22)),
       prop_r=needle_prop(-30, 90, thread=1, t=t), eyes="squint", mouth="wavy", blush=0.8, look=(-1, 1))
    g = ease_out(clamp(ta / 2.4))
    coat_flat(c, 560, 1150, lerp(0.6, 0.9, g), sleeves=clamp(g * 1.5 - 0.3), stitch=g, col=rig.COAT["gam"][0])
    for k in range(4):
        q = (ta * 2 + k / 4) % 1
        c.drawLine(560 - 100 + k * 60, 1000 - q * 200, 560 - 90 + k * 60, 990 - q * 200, P("#F1E2C0", 255 * (1 - q), stroke=5))
    K.off(c)
    ff_badge(c, t)
    text(c, "ÁO MỚI · CỠ GẦM", W / 2, 470, "xbold", 90, "#F4C430", a=255 * pop(t, T["fix"][0] + 0.3), align="center", stroke=9,
         stroke_color="#1A120D")


def sc_snow(c, t):
    ta, u = loc("snow", t)
    K = Cam(540, 980, 1.2); K.on(c)
    exterior(c, t, wind=False, snow=1.0, falling=70)
    gx = lerp(250, 470, ease_out(clamp(ta / 1.0)))
    spread = back_out(clamp((ta - 0.9) / 0.4))
    ch(c, "gam", gx, GROUND, 0.95, t, face=1, outfit="bigcoat", walk=ta * 7 if ta < 1.0 else None,
       hand_l=(lerp(-20, -190, spread), lerp(60, -120, spread)), hand_r=(lerp(20, 190, spread), lerp(60, -120, spread)),
       eyes="closed" if ta < 1.5 else "happy", mouth="smile", head_tilt=-12 * spread)
    K.off(c)
    hx, hy = K.map(gx + 30, GROUND - 330 * 0.95)
    breath(c, hx, hy, t, T["snow"][0] + 1.3, dirx=1)
    if ta > 1.4:
        text(c, "KHÔNG RUN!", W / 2, 1600, "xbold", 90, "#F4C430", a=255 * pop(t, T["snow"][0] + 1.4), align="center", stroke=9,
             stroke_color="#1A120D")


def snow_two(c, t, gkw, bkw, K=None):
    K = K or Cam(545, 1000, 1.15)
    K.on(c)
    exterior(c, t, wind=False, snow=1.0, falling=50)
    ch(c, "bop", TWOX_B, GROUND, 0.95, t, face=-1, outfit="coat", collar_up=1.0, **bkw)
    ch(c, "gam", TWOX_G + 60, GROUND, 0.95, t, face=1, outfit="bigcoat", **gkw)
    return K


def sc_sack2(c, t):
    ta, u = loc("sack2", t)
    hop = abs(math.sin(ta * 6))
    K = snow_two(c, t, dict(feet_air=50 * hop, squash=1 + 0.08 * hop - 0.06 * (hop < 0.2), hand_l=(-170, -200), hand_r=(170, -200),
                            eyes="happy", mouth="grin"),
                 dict(eyes="open", look=(-1, 0), mouth="flat", brow_tilt=-0.6))
    K.off(c)
    say(c, "sack2", K, TWOX_G + 60, GROUND, 0.95, t, bx=540)


def sc_mine(c, t):
    ta, u = loc("mine", t)
    K = snow_two(c, t, dict(hand_l=(60, 60), hand_r=(40, 60), eyes="happy", mouth="smile"),
                 dict(hand_r=(80, -160), prop_r=needle_prop(-80, 100), eyes="open", look=(-1, 0), brow_tilt=-1.0, mouth="frown"))
    K.off(c)
    say(c, "mine", K, TWOX_B, GROUND, 0.95, t, who="bop", bx=620)


def sc_allmine(c, t):
    ta, u = loc("allmine", t)
    k = min(2, int(ta / 0.9))
    if k == 0:
        g = dict(hand_r=(160, -60), hand_l=(-60, -150), eyes="closed", mouth="grin")
    elif k == 1:
        g = dict(hand_r=(150, -220), prop_r=needle_prop(-90, 90), hand_l=(-80, -100), eyes="happy", mouth="grin")
    else:
        g = dict(hand_r=(120, -260), hand_l=(-120, -260), eyes="closed", mouth="tongue", head_tilt=-22, look=(0, -1))
    K = snow_two(c, t, g, dict(hand_r=(-30, 100) if k else (80, -160), prop_r=None if k else needle_prop(-80, 100), eyes="open",
                                look=(-1, 0), brow_tilt=-1.0, mouth="frown"))
    K.off(c)
    say(c, "allmine", K, TWOX_G + 60, GROUND, 0.95, t, bx=540)


def sc_trophy(c, t):
    ta, u = loc("trophy", t)
    K = Cam(560, 1000, 1.25); K.on(c)
    cave_in(c, t, door="morning", snow=False, fire_x=430, fire_s=0.6)
    stone_spear_v(c, 640, GROUND, 520, 0.95, ang=4)
    hide_sheet(c, 640, GROUND - 400, 200, 260, rot=2 + 3 * math.sin(t * 2), hole=True, col="#7A5A3A", dark="#3A2A1A")
    ch(c, "gam", 250, GROUND, 0.95, t, face=1, outfit="bigcoat", hand_l=(40, 110), hand_r=(-30, 110), eyes="happy", mouth="grin",
       head_tilt=-6, lean=-6)
    K.off(c)
    text(c, "CHIẾN LỢI PHẨM CỦA GẦM", W / 2, 420, "xbold", 64, "white", a=255 * pop(t, T["trophy"][0] + 0.2), align="center", stroke=7,
         stroke_color="#1A120D")
    for i, w in enumerate(["LỬA", "GIÁO", "ÁO"]):
        p = pop(t, T["trophy"][0] + 0.6 + i * 0.4, 0.3)
        if p > 0:
            with Xf(c, 260 + i * 280, 540, 0, back_out(p)):
                text(c, w, 0, 0, "xbold", 90, "#F4C430", align="center", stroke=9, stroke_color="#1A120D")


# ================================================================ CẢNH 6 — mấy ngày sau
def scratch_hands(ta, speed=1.0):
    k = int(ta * 2.5 * speed) % 3
    w = 20 * math.sin(ta * 40)
    return [((-100, 120 + w), (40, 40 - w)), ((120, -20 + w), (-40, 80)), ((60, 160 + w), (-90, -40 - w))][k]


def sc_itch(c, t, n="itch"):
    ta, u = loc(n, t)
    hr, hl = scratch_hands(ta, 1.0 if n == "itch" else 1.6)
    K = snow_two(c, t, dict(hand_r=hr, hand_l=hl, eyes="squint", mouth="wavy" if n == "itch" else "shout", brow_tilt=0.6,
                            lean=6 * math.sin(ta * 12), shiver=0.6, feet_air=20 * abs(math.sin(ta * 9)) if n != "itch" else 0),
                 dict(crouch=1.0, hand_l=(90, 100), hand_r=(-30, 100), eyes="open", look=(-1, 0), mouth="flat"))
    for k in range(5):
        q = (ta * 2 + k / 5) % 1
        louse(c, TWOX_G + 60 + 120 * math.cos(k * 1.3), GROUND - 300 + 100 * math.sin(k * 2.1) - 20 * q, 0.35, t, seed=k)
    K.off(c)
    if n == "itch":
        sfx_word(c, "GÃI GÃI", 380, 1560, t, T[n][0] + 0.3, size=90, color="white", dur=2.0)
    else:
        say(c, n, K, TWOX_G + 60, GROUND, 0.95, t, bx=520)


def fur_closeup(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), rig.COAT["gam"][0], rig.COAT["gam"][1])
    for k in range(70):
        x = (k * 157) % (W + 100) - 50; y = (k * 263) % (H + 100) - 50
        c.drawLine(x, y, x + 30, y + 40, P("#6A4C30", 140, stroke=8))
    for k in range(9):
        y = 300 + k * 180
        c.drawLine(880 - 26, y, 880 + 26, y + 40, P("#F1E2C0", stroke=14))


def sc_lice(c, t, n):
    ta, u = loc(n, t)
    if n == "lice2":
        grad_rect(c, skia.Rect.MakeWH(W, H), "#F6E7C0", "#E9C99A")
        # đầu có tóc — chấy sống trên tóc
        c.drawCircle(540, 1050, 260, P("#8A5A3C")); c.drawCircle(540, 1050, 260, P(OUT, stroke=8))
        hair = skia.Path(); hair.moveTo(280, 1000)
        for k in range(13):
            a = math.pi + k * math.pi / 12
            r = 300 + (30 if k % 2 else 0)
            hair.lineTo(540 + r * math.cos(a), 1000 + r * math.sin(a))
        hair.lineTo(800, 1000); hair.close(); fo(c, hair, "#1F1712", ow=7)
        for k in range(3):
            louse(c, 400 + k * 140, 820 - (k % 2) * 60, 1.1, t, seed=k, wave=(k == 1))
        for sd in (-1, 1):
            c.drawCircle(540 + sd * 90, 1100, 26, P("#FFFFFF")); c.drawCircle(540 + sd * 90, 1104, 14, P(OUT))
        sm = skia.Path(); sm.moveTo(470, 1200); sm.quadTo(540, 1240, 610, 1200); c.drawPath(sm, P(OUT, stroke=8))
        text(c, "TÓC", W / 2, 520, "xbold", 110, "#F4C430", a=255 * pop(t, T[n][0] + 0.3), align="center", stroke=10, stroke_color="#1A120D")
        say_at(c, n, t, 540, 1580, (540, 1350))
        return
    fur_closeup(c, t)
    if n == "lice1":
        for k, (x, y) in enumerate([(420, 900), (640, 1080), (500, 1260)]):
            louse(c, x, y + 20 * math.sin(t * 3 + k), 2.2, t, seed=k, wave=(k == 0))
        say_at(c, n, t, 540, 520, (420, 760))
    else:
        for k in range(4):
            q = clamp(ta / 2.2 - k * 0.12)
            louse(c, lerp(160, 820, q), 900 + k * 170, 2.1, t, seed=k, bundle=True, rot=10)
        with Xf(c, 920, 820, -6, 1):
            c.drawLine(0, 0, 0, 220, P(OUT, stroke=14)); c.drawLine(0, 0, 0, 220, P("#8A6A44", stroke=8))
            fo(c, rrect_path(-130, -90, 260, 100, 14), "#F6E7C0", ow=6)
            text(c, "NHÀ MỚI", 0, -22, "xbold", 50, "#7A3A1A", align="center")
        say_at(c, n, t, 540, 480, (500, 900))


def sc_home(c, t):
    ta, u = loc("home", t)
    hop = abs(math.sin(ta * 7))
    hr, hl = scratch_hands(ta, 2.0)
    K = snow_two(c, t, dict(feet_air=70 * hop, hand_r=hr, hand_l=hl, eyes="angry", brow_tilt=1.0, mouth="shout", vein=1.0,
                            lean=14 * math.sin(ta * 5)),
                 dict(crouch=1.0, hand_l=(90, 60), hand_r=(-10, 60), eyes="open", look=(-1, -0.5), mouth="flat"))
    K.off(c)
    sfx_word(c, "TƯNG TƯNG", 380, 1560, t, T["home"][0] + 0.3, size=80, color="white", dur=2.0)
    say(c, "home", K, TWOX_G + 60, GROUND, 0.95, t, bx=540)


def sc_snap(c, t):
    ta, u = loc("snap", t)
    bench(c, t)
    br = ta > 0.9
    pull = ease_in_out(clamp(ta / 0.9)) if not br else 1.0
    lx, rx_ = lerp(320, 200, pull) - (60 * ease_out(clamp((ta - 0.9) / 0.2)) if br else 0), lerp(760, 880, pull) + (60 * ease_out(clamp((ta - 0.9) / 0.2)) if br else 0)
    if not br:
        sinew(c, lx + 60, 1040, rx_ - 60, 1040, w=8, sag=0)
    else:
        sinew(c, lx + 60, 1040, 520, 1080 + 40 * math.sin(ta * 30) * math.exp(-(ta - 0.9) * 5), w=8)
        sinew(c, 560, 1080 - 40 * math.sin(ta * 30) * math.exp(-(ta - 0.9) * 5), rx_ - 60, 1040, w=8)
    big_hand(c, lx, 1080, 1.4, 90)
    with Xf(c, rx_, 1080, 0, 1):
        c.scale(-1, 1); big_hand(c, 0, 0, 1.4, 90)
    sfx_word(c, "PHỰT!", 540, 760, t, T["snap"][0] + 0.9, size=150, color="#F4C430", dur=0.8)


def sc_twist(c, t):
    ta, u = loc("twist", t)
    bench(c, t)
    tw_ = ease_in_out(clamp(ta / 1.0))
    for k in range(2):
        pth = skia.Path()
        for j in range(41):
            q = j / 40
            x = lerp(260, 820, q)
            y = 1040 + 22 * math.sin(q * 14 * tw_ + k * math.pi + ta * 4 * (1 - tw_)) * (0.3 + 0.7 * tw_) + (1 - tw_) * (k * 40 - 20)
            (pth.moveTo if j == 0 else pth.lineTo)(x, y)
        c.drawPath(pth, P(OUT, stroke=16)); c.drawPath(pth, P("#E3C48E" if k == 0 else "#CDAA70", stroke=10))
    strain = ta > 1.1
    off = 20 * math.sin(ta * 30) if strain else 0
    big_hand(c, 220 - off, 1080, 1.4, 90)
    with Xf(c, 860 + off, 1080, 0, 1):
        c.scale(-1, 1); big_hand(c, 0, 0, 1.4, 90)
    if strain:
        text(c, "KHÔNG ĐỨT!", W / 2, 760, "xbold", 110, "#F4C430", a=255 * pop(t, T["twist"][0] + 1.2), align="center", stroke=10,
             stroke_color="#1A120D")
        stars_burst(c, 540, 1040, t, T["twist"][0] + 1.25)


def rope_icon(c, x, y, s, t):
    with Xf(c, x, y, -20, s):
        for k in range(3):
            pth = skia.Path()
            for j in range(31):
                q = j / 30
                xx = lerp(-160, 160, q)
                yy = 18 * math.sin(q * 16 + k * 2.1)
                (pth.moveTo if j == 0 else pth.lineTo)(xx, yy)
            c.drawPath(pth, P(OUT, stroke=16)); c.drawPath(pth, P(["#E3C48E", "#CDAA70", "#B8955E"][k], stroke=10))


def sc_idea(c, t):
    ta, u = loc("idea", t)
    hr, hl = scratch_hands(ta)
    K = Cam(560, 1000, 1.35); K.on(c)
    exterior(c, t, wind=False, snow=1.0, falling=30)
    ch(c, "gam", 260, GROUND, 0.9, t, face=1, outfit="bigcoat", hand_r=hr, hand_l=hl, eyes="squint", mouth="wavy", lean=5 * math.sin(ta * 12))
    ch(c, "bop", 720, GROUND, 0.95, t, face=-1, outfit="coat", collar_up=1.0, crouch=1.0, hand_r=(90, -40), hand_l=(-90, -40),
       eyes="open", look=(-0.3, -1), brow=0.8, mouth="o" if ta > 1.0 else "flat", head_tilt=10)
    sinew(c, 600, GROUND - 330, 820, GROUND - 330, w=6, sag=20)
    K.off(c)
    a = T["idea"][0]
    say(c, "idea", K, 720, GROUND, 0.95, t, who="bop", crouch=1.0, bx=600, by=420, d=0.3)
    if ta > 1.2:
        rope_icon(c, 600, 520, 0.8 * back_out(pop(t, a + 1.2)), t)


def sc_useless2(c, t):
    ta, u = loc("useless2", t)
    hr, hl = scratch_hands(ta, 2.0)
    K = Cam(560, 1000, 1.35); K.on(c)
    exterior(c, t, wind=False, snow=1.0, falling=30)
    ch(c, "gam", 260, GROUND, 0.9, t, face=1, outfit="bigcoat", hand_r=hr, hand_l=hl, eyes="angry", brow_tilt=1.0, mouth="shout",
       feet_air=40 * abs(math.sin(ta * 8)), vein=1.0)
    ch(c, "bop", 720, GROUND, 0.95, t, face=-1, outfit="coat", collar_up=1.0, crouch=1.0, hand_r=(90, -40), hand_l=(-90, -40),
       eyes="squint", look=(-1, 0), mouth="smile")
    rope_icon(c, 720 - 70, GROUND - 330, 0.45, t)
    K.off(c)
    say(c, "useless2", K, 260, GROUND, 0.9, t, bx=440)


def sc_black(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000"))


def sc_card(c, t):
    a, b = beat("card")
    grad_rect(c, skia.Rect.MakeWH(W, H), "#1A120D", "#0B0806")
    needle(c, 540, 1560, 640, -10, thread=1, t=t, thread_len=260, shine=pop(t, a + 0.5), wav=0.6)
    kinetic(c, "SỰ THẬT", W / 2, 300, t, a + 0.2, size=90, color="#F4C430", per=0.05)
    p1 = pop(t, a + 0.7, 0.5)
    l1 = ["Hang Denisova (Siberia): một cây kim", "bằng xương chim ~50.000 năm tuổi,", "dài hơn 7 cm, có lỗ xỏ sợi."]
    for i, l in enumerate(l1):
        text(c, l, W / 2, 470 + i * 72, "bold", 50, "white", a=255 * p1, align="center")
    p2 = pop(t, a + 2.2, 0.5)
    l2 = ["Chấy quần áo tách ra từ chấy đầu.", "Nhờ đó các nhà khoa học ước tính:", "con người mặc quần áo từ ít nhất",
          "83.000, có thể tới 170.000 năm trước."]
    for i, l in enumerate(l2):
        text(c, l, W / 2, 790 + i * 72, "bold", 50, "white" if i < 2 else "#F4C430", a=255 * p2, align="center")
    text(c, "Tập sau: dây thừng", W / 2, 1180, "semi", 42, "#B9B4AA", a=255 * pop(t, a + 4.0), align="center")
    if t > b - 0.8:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 255 * prog(t, b - 0.8, b, lambda q: q)))


FN = {
    "open": sc_open, "inside": sc_inside, "warm1": lambda c, t: sc_warm(c, t, "warm1"), "warm2": lambda c, t: sc_warm(c, t, "warm2"),
    "gust": sc_gust, "naked": sc_naked, "better": lambda c, t: sc_naked(c, t, "better"),
    "grind": sc_grind, "sharp1": lambda c, t: sc_sharp(c, t, "sharp1"), "sharp2": lambda c, t: sc_sharp(c, t, "sharp2"),
    "drill": sc_drill, "hole": sc_hole, "thread": sc_thread, "stitch": sc_stitch,
    "lead1": lambda c, t: sc_lead(c, t, "lead1"), "lead2": lambda c, t: sc_lead(c, t, "lead2"),
    "montage": sc_montage, "wear": sc_wear, "nofly": sc_nofly, "fit1": lambda c, t: sc_fit(c, t, "fit1"),
    "fit2": lambda c, t: sc_fit(c, t, "fit2"), "sack": sc_sack, "sleeve1": lambda c, t: sc_sleeve(c, t, "sleeve1"),
    "sleeve2": lambda c, t: sc_sleeve(c, t, "sleeve2"), "fight": sc_fight, "grab": sc_grab, "broken": sc_broken,
    "useless": sc_useless, "flick": sc_flick, "long": sc_long,
    "storm": lambda c, t: sc_storm(c, t, "storm"), "slip": lambda c, t: sc_storm(c, t, "slip"), "stay": sc_stay, "burn": sc_burn,
    "snore": sc_snore, "sneak": sc_sneak, "stuck": sc_stuck, "wake": lambda c, t: sc_wake(c, t, "wake"),
    "check": lambda c, t: sc_wake(c, t, "check"),
    "find": sc_find, "sew": sc_sew, "done": sc_done, "tail": sc_tail, "fix": sc_fix, "snow": sc_snow, "sack2": sc_sack2,
    "mine": sc_mine, "allmine": sc_allmine, "trophy": sc_trophy,
    "itch": sc_itch, "bite": lambda c, t: sc_itch(c, t, "bite"), "lice1": lambda c, t: sc_lice(c, t, "lice1"),
    "lice2": lambda c, t: sc_lice(c, t, "lice2"), "lice3": lambda c, t: sc_lice(c, t, "lice3"), "home": sc_home,
    "snap": sc_snap, "twist": sc_twist, "idea": sc_idea, "useless2": sc_useless2, "black": sc_black, "card": sc_card,
}
SCENE_CUT = {T["storm"][0], T["find"][0], T["itch"][0]}


def draw_frame(c, t):
    for name, (a, b, row) in T.items():
        if a <= t < b:
            FN[name](c, t)
            for sc in SCENE_CUT:
                if sc - 0.3 <= t < sc + 0.3:
                    c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 255 * (1 - abs(t - sc) / 0.3)))
            return
    sc_card(c, min(t, DUR - 0.01))
