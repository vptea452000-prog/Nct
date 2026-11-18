"""Dựng thử phong cách người que 2D (theo mẫu 'đạo diễn từng cảnh, mỗi 10 giây một prompt').
Đoạn: đầu Tập 5 — Gầm xiên cá, đại bàng cuỗm mất, phóng giáo hụt. 25 giây, 9:16, chỉ hiệu ứng tiếng.
  python3 src/demo.py preview 1.0 4.5 ...   → build/pv_<t>.png
  python3 src/demo.py full                  → build/Stick_demo.mp4
"""
import math, subprocess, sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT.parent / "tools"))
import numpy as np  # noqa
import skia  # noqa
from PIL import Image  # noqa
from lib import W, H, FPS, paint, text, Xf, clamp, lerp, nfc  # noqa
from sets import grad_rect  # noqa
from rig import ik2, ease_out, ease_in_out, back_out  # noqa

DUR = 25.0
INK = "#1A1A1A"
BUILD = ROOT / "build"


def P(col, a=255, stroke=None):
    return paint(col, a, stroke=stroke)


def oval(cx, cy, rx, ry):
    p = skia.Path(); p.addOval(skia.Rect.MakeXYWH(cx - rx, cy - ry, 2 * rx, 2 * ry)); return p


def fo(c, path, fill, ow=7, a=255):
    c.drawPath(path, P(fill, a)); c.drawPath(path, P(INK, a, stroke=ow))


# ---------------------------------------------------------------- người que Gầm (nét cố định)
# Gầm: đầu tròn trắng to, tóc nâu bờm xờm, râu nâu rậm che nửa dưới mặt, mắt chấm đen, lông mày dày;
#      tay chân là nét đen; mặc áo da nâu hình thang ngắn tới hông.
HAIR, BEARD, COAT = "#6B4A30", "#5A3A24", "#9A7450"


def stick(c, x, y, s, t, face=1, hand_f=None, hand_b=None, foot_f=None, foot_b=None, lean=0.0, look=(0.0, 0.0),
          mouth="flat", eyes="dot", brow=0.0, squash=1.0, back_view=False, spear=None):
    """Người que. Toạ độ tay/chân tính từ hông (đơn vị khung). spear = (góc độ, chiều dài) cầm ở tay trước."""
    c.save(); c.translate(x, y); c.scale(s * face / math.sqrt(squash), s * squash)
    L, TOR, HR = 105, 165, 78
    hip = (0.0, -2 * L)
    c.drawOval(skia.Rect.MakeXYWH(-90, -12, 180, 24), P("#000000", 40))

    def leg(foot):
        fx, fy = foot
        kx, ky = ik2(hip[0], hip[1], fx, fy, L, L, bend=1)
        pth = skia.Path(); pth.moveTo(*hip); pth.lineTo(kx, ky); pth.lineTo(fx, fy)
        c.drawPath(pth, P(INK, stroke=14))
        c.drawLine(fx, fy, fx + 22, fy, P(INK, stroke=14))

    leg(foot_b or (-28, 0)); leg(foot_f or (28, 0))
    c.save(); c.translate(*hip); c.rotate(lean); c.translate(-hip[0], -hip[1])
    sh = (0.0, hip[1] - TOR)

    def arm(hand):
        hx, hy = hand
        tx, ty = sh[0] + hx, sh[1] + hy
        ex, ey = ik2(sh[0], sh[1], tx, ty, 95, 90, bend=-1)
        pth = skia.Path(); pth.moveTo(*sh); pth.lineTo(ex, ey); pth.lineTo(tx, ty)
        c.drawPath(pth, P(INK, stroke=14))
        c.drawCircle(tx, ty, 12, P(INK))
        return tx, ty

    arm(hand_b or (-20, 175))
    c.drawLine(hip[0], hip[1], sh[0], sh[1], P(INK, stroke=14))
    coat = skia.Path(); coat.moveTo(-34, sh[1] + 6); coat.lineTo(34, sh[1] + 6); coat.lineTo(58, hip[1] + 22)
    for k in range(5, -1, -1):
        coat.lineTo(-58 + 116 * k / 5, hip[1] + (34 if k % 2 else 18))
    coat.close(); fo(c, coat, COAT, ow=6)
    hf = arm(hand_f or (20, 175))
    if spear:
        ang, ln = spear
        with Xf(c, hf[0], hf[1], ang, 1):
            c.drawLine(0, 140, 0, -ln + 140, P(INK, stroke=16)); c.drawLine(0, 140, 0, -ln + 140, P("#8A6A44", stroke=9))
            tip = skia.Path(); tip.moveTo(-18, -ln + 150); tip.lineTo(0, -ln + 70); tip.lineTo(18, -ln + 150); tip.close()
            fo(c, tip, "#9AA3A8", ow=5)
        c.drawCircle(hf[0], hf[1], 12, P(INK))
    # đầu
    hx, hy = sh[0] + 6, sh[1] - HR - 6
    hair = skia.Path(); hair.moveTo(hx - HR - 8, hy + 4)
    for k in range(13):
        a = math.pi + k * math.pi / 12
        r = HR + (22 if k % 2 else 8)
        hair.lineTo(hx + r * math.cos(a), hy + r * math.sin(a))
    hair.lineTo(hx + HR + 8, hy + 4); hair.close()
    fo(c, hair, HAIR, ow=6)
    if back_view:
        fo(c, oval(hx, hy, HR, HR), HAIR, ow=7)
        for k in range(6):
            c.drawLine(hx - 50 + k * 20, hy - 40, hx - 46 + k * 20, hy + 40, P("#4E3420", stroke=5))
    else:
        fo(c, oval(hx, hy, HR, HR), "#FFFFFF", ow=7)
        bd = skia.Path(); bd.moveTo(hx - HR + 4, hy + 4); bd.quadTo(hx - HR + 10, hy + HR * 1.2, hx + 14, hy + HR * 1.15)
        bd.quadTo(hx + HR, hy + HR * 1.0, hx + HR - 4, hy + 4); bd.quadTo(hx + 10, hy + 30, hx - HR + 4, hy + 4); bd.close()
        fo(c, bd, BEARD, ow=6)
        ex = hx + 18
        for dx in (-20, 22):
            if eyes == "dot":
                c.drawCircle(ex + dx + look[0] * 6, hy - 18 + look[1] * 6, 9, P(INK))
            elif eyes == "wide":
                c.drawCircle(ex + dx, hy - 18, 16, P("#FFFFFF")); c.drawCircle(ex + dx, hy - 18, 16, P(INK, stroke=4))
                c.drawCircle(ex + dx + look[0] * 6, hy - 18 + look[1] * 6, 6, P(INK))
            elif eyes == "happy":
                pth = skia.Path(); pth.moveTo(ex + dx - 12, hy - 14); pth.quadTo(ex + dx, hy - 30, ex + dx + 12, hy - 14)
                c.drawPath(pth, P(INK, stroke=6))
            elif eyes == "angry":
                c.drawCircle(ex + dx, hy - 16, 8, P(INK))
            by = hy - 44 - brow * 10
            tilt = 8 if eyes == "angry" else 0
            c.drawLine(ex + dx - 14, by - (tilt if dx < 0 else -tilt) * -1, ex + dx + 14, by + (tilt if dx < 0 else -tilt) * -1, P(INK, stroke=9))
        my = hy + 30
        if mouth == "o":
            fo(c, oval(ex, my, 12, 16), "#5A1E16", ow=4)
        elif mouth == "grin":
            pth = skia.Path(); pth.moveTo(ex - 24, my - 6); pth.quadTo(ex, my + 22, ex + 24, my - 6); pth.close(); fo(c, pth, "#FFFFFF", ow=4)
        elif mouth == "shout":
            fo(c, oval(ex, my + 4, 20, 22), "#5A1E16", ow=4)
        else:
            c.drawLine(ex - 14, my, ex + 14, my, P(INK, stroke=5))
    c.restore()
    c.restore()


# ---------------------------------------------------------------- đại bàng & cá
def fish(c, x, y, s, rot=0.0, wig=0.0):
    with Xf(c, x, y, rot + wig, s):
        b = skia.Path(); b.addOval(skia.Rect.MakeXYWH(-90, -34, 180, 68)); fo(c, b, "#7FA6B8", ow=6)
        tl = skia.Path(); tl.moveTo(80, 0); tl.lineTo(140, -40); tl.lineTo(140, 40); tl.close(); fo(c, tl, "#6A90A2", ow=6)
        c.drawCircle(-56, -8, 9, P(INK))
        c.drawLine(-20, -30, -10, 30, P("#5E8496", stroke=4))


def eagle(c, x, y, s, t, flap=1.0, perched=False, face=1, fish_on=False, bite=0.0, look=(0.0, 0.0), dive=0.0):
    with Xf(c, x, y, dive * 40 * face, s):
        c.scale(face, 1)
        if perched:
            for dx in (-14, 14):
                c.drawLine(dx, 40, dx, 76, P("#E0A820", stroke=8))
        if fish_on:
            fish(c, 40 if perched else 10, 70 if perched else 96, 0.55, rot=0 if perched else 20)
        w = math.sin(t * 14) * flap
        for sd in (-1, 1):
            wing = skia.Path(); wing.moveTo(-10, -10)
            tipx, tipy = (-130 if perched else -190) * (1 if sd < 0 else 0.4), -60 - 80 * w * (1 if not perched else 0.1)
            if perched:
                wing.quadTo(-60, -30, -110, 50); wing.lineTo(-20, 40); wing.close()
            else:
                wing.quadTo(-80 * sd * -1, -80 * w - 40, sd * 220, -40 - 110 * w)
                for k in range(4):
                    wing.lineTo(sd * (220 - k * 40), -10 - 110 * w + k * 12)
                wing.lineTo(0, 20); wing.close()
            fo(c, wing, "#6B4A30", ow=6)
            if perched:
                break
        body = oval(0, 10, 70, 46); fo(c, body, "#7A5638", ow=6)
        tail = skia.Path(); tail.moveTo(-60, 10); tail.lineTo(-120, -10 if not perched else 60); tail.lineTo(-110, 30 if not perched else 80); tail.close()
        fo(c, tail, "#6B4A30", ow=5)
        hb = bite * 30
        fo(c, oval(66, -30 + hb, 40, 34), "#F6F1E4", ow=6)
        beak = skia.Path(); beak.moveTo(96, -40 + hb); beak.quadTo(136, -34 + hb, 118, -6 + hb); beak.lineTo(100, -18 + hb); beak.close()
        fo(c, beak, "#F4C430", ow=5)
        c.drawCircle(78 + look[0] * 4, -38 + hb + look[1] * 4, 7, P(INK))
        c.drawLine(62, -56 + hb, 96, -48 + hb, P(INK, stroke=6))


# ---------------------------------------------------------------- bối cảnh
TREE_X, BRANCH_Y = 930, 560
WATER_Y = 1300


def stream_bg(c, t, z=1.0):
    grad_rect(c, skia.Rect.MakeXYWH(-800, -800, W + 1600, H + 1600), "#BFE4F2", "#F1F6E6")
    for k, (yy, col_) in enumerate([(900, "#B8D6A0"), (980, "#9CC484")]):
        p = skia.Path(); p.moveTo(-800, 1400)
        for i in range(0, 26):
            p.lineTo(-800 + i * 110, yy - 90 * abs(math.sin(i * 0.7 + k)))
        p.lineTo(W + 800, 1400); p.close(); c.drawPath(p, P(col_))
    c.drawRect(skia.Rect.MakeXYWH(-800, 1080, W + 1600, 240), P("#A9CF8A"))
    # cây cao bên kia suối
    c.drawLine(TREE_X, 1180, TREE_X, BRANCH_Y - 200, P(INK, stroke=34)); c.drawLine(TREE_X, 1180, TREE_X, BRANCH_Y - 200, P("#8A6A44", stroke=24))
    c.drawLine(TREE_X, BRANCH_Y + 10, TREE_X - 230, BRANCH_Y - 20, P(INK, stroke=22)); c.drawLine(TREE_X, BRANCH_Y + 10, TREE_X - 230, BRANCH_Y - 20, P("#8A6A44", stroke=14))
    for dx, dy, r in [(-60, -300, 150), (90, -340, 170), (40, -200, 130)]:
        c.drawCircle(TREE_X + dx, BRANCH_Y + dy, r, P("#7FB069")); c.drawCircle(TREE_X + dx, BRANCH_Y + dy, r, P(INK, stroke=6))
    c.drawRect(skia.Rect.MakeXYWH(-800, WATER_Y, W + 1600, 900), P("#6FB7D8"))
    c.drawLine(-800, WATER_Y, W + 800, WATER_Y, P(INK, stroke=6))
    for k in range(14):
        xx = (k * 160 + t * 70) % (W + 400) - 200
        c.drawLine(xx, WATER_Y + 60 + (k % 5) * 90, xx + 80, WATER_Y + 60 + (k % 5) * 90, P("#FFFFFF", 150, stroke=6))


def water_front(c, x, w=240):
    """Mặt nước phủ ngang ống chân (nhân vật đứng giữa suối)."""
    c.drawRect(skia.Rect.MakeXYWH(x - w / 2 - 400, WATER_Y + 10, w + 800, 900), P("#6FB7D8"))
    c.drawOval(skia.Rect.MakeXYWH(x - w / 2, WATER_Y - 6, w, 34), P("#FFFFFF", 160, stroke=6))


def splash(c, x, y, t, t0, n=10, r=200):
    age = t - t0
    if age < 0 or age > 0.8:
        return
    for k in range(n):
        a = -math.pi * (0.15 + 0.7 * k / (n - 1))
        d = r * age * 1.6
        c.drawCircle(x + d * math.cos(a), y + d * math.sin(a) + 400 * age * age, 14 * (1 - age), P("#DFF3FB"))
        c.drawCircle(x + d * math.cos(a), y + d * math.sin(a) + 400 * age * age, 14 * (1 - age), P(INK, stroke=3))


class Cam:
    def __init__(self, cx, cy, z):
        self.cx, self.cy, self.z = cx, cy, z

    def on(self, c):
        c.save(); c.translate(W / 2, H / 2); c.scale(self.z, self.z); c.translate(-self.cx, -self.cy)

    def off(self, c):
        c.restore()


GX = 420  # Gầm đứng giữa suối


# ================================================================ Prompt 1 — 0:00–0:10
def s1(c, t):  # 0–3: toàn cảnh, rình rồi xiên
    K = Cam(560, 1050, 1.05); K.on(c)
    stream_bg(c, t)
    stab = clamp((t - 1.8) / 0.15)
    if t < 1.8:
        ang, hand = 150 + 4 * math.sin(t * 3), (40, -150)
    else:
        ang, hand = lerp(150, 172, stab), (lerp(40, 70, stab), lerp(-150, 60, stab))
    shadow_x = lerp(700, GX + 60, clamp(t / 1.7))
    c.drawOval(skia.Rect.MakeXYWH(shadow_x - 70, WATER_Y + 70, 140, 34), P("#3E7FA0", 160))
    stick(c, GX, WATER_Y + 90, 1.25, t, face=1, hand_f=hand, hand_b=(70, -110 + 120 * stab), spear=(ang, 520),
          lean=10 * stab, eyes="angry" if t < 1.8 else "wide", look=(1, 1), mouth="flat" if t < 1.8 else "o", foot_f=(40, 0), foot_b=(-40, 0))
    water_front(c, GX + 10)
    splash(c, GX + 130, WATER_Y + 10, t, 1.95)
    K.off(c)


def s2(c, t):  # 3–6: cận cảnh mũi giáo nhấc khỏi mặt nước, cá giãy
    lt = t - 3
    grad_rect(c, skia.Rect.MakeWH(W, H), "#BFE4F2", "#F1F6E6")
    up = ease_out(clamp(lt / 0.9))
    sy = lerp(1700, 980, up)
    c.drawLine(560, sy + 900, 560, sy - 40, P(INK, stroke=34)); c.drawLine(560, sy + 900, 560, sy - 40, P("#8A6A44", stroke=22))
    fish(c, 560, sy + 40, 2.2, rot=-8, wig=10 * math.sin(lt * 22) * (1 - 0.6 * clamp(lt / 3)))
    tip = skia.Path(); tip.moveTo(-40, 20); tip.lineTo(0, -160); tip.lineTo(40, 20); tip.close()
    with Xf(c, 560, sy - 40, 0, 1):
        fo(c, tip, "#9AA3A8", ow=7)
    c.drawRect(skia.Rect.MakeXYWH(0, 1500, W, 500), P("#6FB7D8"))
    c.drawLine(0, 1500, W, 1500, P(INK, stroke=8))
    for k in range(12):
        q = (lt * 1.5 + k / 12) % 1
        c.drawCircle(380 + k * 34, sy + 140 + q * 600, 10 * (1 - q) + 3, P("#DFF3FB"))


def s3(c, t):  # 6–10: góc thấp sau lưng, giơ cá khoe — chấm đen lượn trên trời
    lt = t - 6
    grad_rect(c, skia.Rect.MakeWH(W, H), "#8FCBE6", "#E8F4F8")
    for k in range(3):
        c.drawCircle(220 + k * 340, 300 + (k % 2) * 80, 90, P("#FFFFFF", 200))
    lift = back_out(clamp(lt / 0.6))
    S_, Y_ = 2.2, 2150
    stick(c, 470, Y_, S_, t, face=1, back_view=True, hand_f=(30, lerp(-60, -260, lift)), hand_b=(110, lerp(-40, -250, lift)),
          spear=(0, 380), lean=-4)
    hx, hy = 470 + S_ * 30, Y_ + S_ * (-2 * 105 - 165 + lerp(-60, -260, lift))
    fish(c, hx, hy - S_ * 175, 1.3, rot=-80, wig=8 * math.sin(lt * 18))
    # đại bàng: chấm đen lượn vòng, rồi khựng lại
    a = lt * 1.6
    ex, ey = 820 + 90 * math.cos(a), 300 + 40 * math.sin(a)
    r_ = 10 + 3 * lt
    c.drawCircle(ex, ey, r_, P(INK))
    c.drawLine(ex - r_ * 2.4, ey - r_ * 0.6 * math.sin(t * 10), ex + r_ * 2.4, ey - r_ * 0.6 * math.sin(t * 10), P(INK, stroke=5))
    if lt > 2.6:
        g = clamp((lt - 2.6) / 0.3)
        text(c, "!", ex + 40, ey - 30, "xbold", int(60 + 30 * g), "#C0392B", a=255 * g, align="center")


# ================================================================ Prompt 2 — 0:10–0:20
def s4(c, t):  # 10–13: góc nhìn của đại bàng lao xuống
    lt = t - 10
    z = lerp(0.35, 1.9, ease_in_out(clamp(lt / 2.8)) ** 1.4)
    c.drawRect(skia.Rect.MakeWH(W, H), P("#6FB7D8"))
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z)
    for k in range(40):
        xx = ((k * 173) % 2400) - 1200; yy = ((k * 97) % 2400) - 1200
        c.drawLine(xx, yy, xx + 80, yy, P("#FFFFFF", 140, stroke=6 / z * 2))
    c.drawOval(skia.Rect.MakeXYWH(-150, -110, 300, 220), P("#FFFFFF", 150, stroke=8))
    fo(c, oval(0, 0, 90, 90), HAIR, ow=8)                         # đỉnh đầu Gầm
    for sd in (-1, 1):
        c.drawLine(sd * 50, 20, sd * 130, -60, P(INK, stroke=16))  # hai tay giơ lên
    fish(c, 0, -170, 1.1, rot=90, wig=6 * math.sin(lt * 20))
    c.restore()
    if lt > 2.1:
        q = clamp((lt - 2.1) / 0.6)
        for sd in (-1, 1):
            with Xf(c, W / 2 + sd * lerp(700, 260, q), lerp(-200, 260, q), sd * 20, 2.2):
                for k in range(3):
                    c.drawLine(0, 0, -30 + k * 30, 110, P("#E0A820", stroke=16))
                    c.drawLine(-30 + k * 30, 110, -30 + k * 30 + 14 * sd, 150, P(INK, stroke=12))
    for k in range(10):
        a = k * 2 * math.pi / 10 + lt
        c.drawLine(W / 2 + 500 * math.cos(a), H / 2 + 500 * math.sin(a), W / 2 + 1200 * math.cos(a), H / 2 + 1200 * math.sin(a),
                   P("#FFFFFF", 120, stroke=6))


def s5(c, t):  # 13–16: toàn cảnh, đại bàng giật cá, bay lên cành cao
    lt = t - 13
    K = Cam(620, 1000, 0.95); K.on(c)
    stream_bg(c, t)
    grab = lt > 0.6
    jerk = math.exp(-max(0, lt - 0.6) * 6) * grab
    hx = GX + 1.25 * 60
    hy = WATER_Y + 90 + 1.25 * (-2 * 105 - 165 - 260)
    stick(c, GX, WATER_Y + 90, 1.25, t, face=1, hand_f=(30, -260 + 40 * jerk), hand_b=(110, -250 + 40 * jerk), spear=(0, 560),
          eyes="wide", look=(0.6, -1) if grab else (0, 0), mouth="o" if grab else "grin", squash=1 - 0.06 * jerk)
    water_front(c, GX + 10)
    if not grab:
        fish(c, hx - 10, hy - 1.25 * 380 + 60, 0.9, rot=-80)
        q = clamp(lt / 0.6)
        eagle(c, lerp(-200, hx - 20, ease_in_out(q)), lerp(200, hy - 1.25 * 380, q), 0.9, t, dive=1 - q)
    else:
        q = clamp((lt - 0.6) / 1.6)
        ex = lerp(hx - 20, TREE_X - 130, ease_in_out(q))
        ey = lerp(hy - 1.25 * 380, BRANCH_Y - 90, ease_out(q)) - 120 * math.sin(math.pi * q)
        eagle(c, ex, ey, 0.9, t, flap=1.0 if q < 1 else 0.0, perched=q >= 1, fish_on=True, face=1 if q < 0.95 else -1)
        if lt < 1.0:
            for k in range(5):
                c.drawLine(hx - 80 + k * 30, hy - 560, hx - 60 + k * 30, hy - 680, P("#FFFFFF", 200 * (1 - (lt - 0.6) / 0.4), stroke=6))
    K.off(c)


def s6(c, t):  # 16–20: phóng giáo, giáo chúi xuống cắm bùn giữa suối
    lt = t - 16
    K = Cam(620, 1000, 0.95); K.on(c)
    stream_bg(c, t)
    eagle(c, TREE_X - 130, BRANCH_Y - 90, 0.9, t, flap=0, perched=True, fish_on=True, face=-1, look=(-1, 1))
    if lt < 0.6:
        w = ease_in_out(lt / 0.6)
        stick(c, GX, WATER_Y + 90, 1.25, t, face=1, hand_f=(lerp(30, -150, w), lerp(-200, -120, w)), hand_b=(120, -60),
              spear=(lerp(20, 60, w), 520), lean=-14 * w, eyes="angry", mouth="flat", foot_f=(50, 0), foot_b=(-50, 0))
    else:
        stick(c, GX, WATER_Y + 90, 1.25, t, face=1, hand_f=(200, -160), hand_b=(-60, 40), lean=14, eyes="wide" if lt > 1.8 else "angry",
              look=(1, 0.5), mouth="o" if lt > 1.8 else "shout", foot_f=(60, 0), foot_b=(-50, 0))
        q = clamp((lt - 0.6) / 1.3)
        sx = lerp(GX + 230, 720, q)
        sy = lerp(WATER_Y - 250, WATER_Y - 50, q * q) - 260 * math.sin(math.pi * q * 0.9)
        ang = lerp(-75, -12, q)
        wob = 10 * math.sin((lt - 1.9) * 30) * math.exp(-(lt - 1.9) * 3) if q >= 1 else 0
        with Xf(c, sx, sy, (ang if q < 1 else -14) + wob, 1.25):
            c.drawLine(0, 0, 0, -520, P(INK, stroke=16)); c.drawLine(0, 0, 0, -520, P("#8A6A44", stroke=9))
            tip = skia.Path(); tip.moveTo(-18, -10); tip.lineTo(0, 70); tip.lineTo(18, -10); tip.close(); fo(c, tip, "#9AA3A8", ow=5)
        if q >= 1:
            c.drawOval(skia.Rect.MakeXYWH(680, WATER_Y + 30, 90, 26), P("#7A5A3A"))
    water_front(c, GX + 10)
    K.off(c)


# ================================================================ Prompt 3 — 0:20–0:25
def s7(c, t):  # 20–25: cận cành cây — đại bàng ăn thong thả, Gầm bé xíu nhảy dưới kia
    lt = t - 20
    grad_rect(c, skia.Rect.MakeWH(W, H), "#BFE4F2", "#F1F6E6")
    c.drawRect(skia.Rect.MakeXYWH(0, 1500, W, 500), P("#6FB7D8"))
    c.drawLine(0, 1500, W, 1500, P(INK, stroke=5))
    hop = abs(math.sin(lt * 7)) * 40
    stick(c, 300, 1560 - hop, 0.45, t, face=1, hand_f=(60, -250), hand_b=(110, -240), eyes="angry", mouth="shout")
    c.drawLine(-50, 1060, 1200, 1000, P(INK, stroke=60)); c.drawLine(-50, 1060, 1200, 1000, P("#8A6A44", stroke=46))
    bite = max(0.0, math.sin(lt * 3.2)) ** 3 if not (2.6 < lt < 3.6) else 0.0
    eagle(c, 620, 780, 2.6, t, flap=0, perched=True, fish_on=True, face=1, bite=bite,
          look=(-0.6, 1) if 2.6 < lt < 3.6 else (0.5, 0.3))
    if bite > 0.6:
        for k in range(3):
            c.drawCircle(980 + k * 30, 900 - k * 20, 8, P("#FFFFFF"))


SHOTS = [(0, 3, s1), (3, 6, s2), (6, 10, s3), (10, 13, s4), (13, 16, s5), (16, 20, s6), (20, 25, s7)]

# Lời dẫn (chủ kênh sẽ tự thu) — trong bản thử hiện tạm thành phụ đề
VO = [
    (0.3, 4.6, "Sáng hôm ấy, Gầm xiên được con cá to nhất suối."),
    (5.0, 9.8, "Hắn giơ lên thật cao để khoe… và đó là sai lầm."),
    (10.2, 15.6, "Một con đại bàng sà xuống, cuỗm con cá ngay trên mũi giáo."),
    (16.0, 19.8, "Gầm phóng giáo đuổi theo — nhưng giáo nặng, chỉ bay được nửa đường."),
    (20.3, 24.6, "Còn con đại bàng thì ăn sáng rất thong thả."),
]


def subtitle(c, t):
    for a, b, s in VO:
        if a <= t < b:
            al = 255 * clamp(min(t - a, b - t) / 0.2)
            from lib import font, tw
            words, lines, cur = nfc(s).split(), [], ""
            for w_ in words:
                test = (cur + " " + w_).strip()
                if tw(test, "bold", 52) > 900 and cur:
                    lines.append(cur); cur = w_
                else:
                    cur = test
            lines.append(cur)
            for i, l in enumerate(lines):
                text(c, l, W / 2, 1640 + i * 70, "bold", 52, "#FFFFFF", a=al, align="center", stroke=9, stroke_color="#111111")


def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas(); c.clear(skia.ColorWHITE)
    for a, b, fn in SHOTS:
        if a <= t < b:
            c.save(); fn(c, t); c.restore(); break
    subtitle(c, t)
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def chunk(args):
    k, f0, f1 = args
    out = BUILD / f"sc_{k:02d}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    s = skia.Surface(W, H)
    for i in range(f0, f1):
        p.stdin.write(frame(i / FPS, s).tobytes())
    p.stdin.close(); p.wait()
    return out


if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for ts in sys.argv[2:]:
            Image.fromarray(frame(float(ts))[..., :3]).save(BUILD / f"pv_{float(ts):05.2f}.png")
    else:
        nfr = int(DUR * FPS); step = math.ceil(nfr / 4)
        with Pool(4) as pool:
            ch = pool.map(chunk, [(k, f, min(nfr, f + step)) for k, f in enumerate(range(0, nfr, step))])
        (BUILD / "sc.txt").write_text("".join(f"file '{x.name}'\n" for x in ch))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(BUILD / "sc.txt"), "-c", "copy",
                        str(BUILD / "Stick_demo_nosfx.mp4")], check=True)
        for x in ch:
            x.unlink()
        (BUILD / "sc.txt").unlink()
        print("xong")
