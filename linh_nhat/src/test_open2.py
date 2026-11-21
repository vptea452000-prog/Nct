"""Bản thử 2: 10,5 giây mở đầu, máy quay chuyển động liên tục kiểu điện ảnh (người que v2, 16:9).
Cẩu máy, lướt sát mặt nước, ngước theo khói, qua vai, bám gót chân, zoom giật + nghiêng khung, lớp cảnh lệch nhau (parallax).
  python3 linh_nhat/src/test_open2.py preview 1 3 ...   → linh_nhat/build/pv2_<t>.png
  python3 linh_nhat/src/test_open2.py full              → linh_nhat/build/Test_mo_dau_v2_nosfx.mp4
"""
import math, subprocess, sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools")); sys.path.insert(0, str(ROOT.parent / "cung" / "src"))
import skia  # noqa
from PIL import Image  # noqa
from lib import text  # noqa
from stick2 import Stick, draw_stick, P, fo, oval, clamp, lerp, ease_out, ease_in_out, back_out, INK  # noqa

W, H, FPS = 1920, 1080, 30
DUR = 10.5
BUILD = ROOT / "build"


def noise1(t, s=0.0):
    return math.sin(t * 1.3 + s) * 0.5 + math.sin(t * 2.9 + s * 1.7) * 0.3 + math.sin(t * 6.1 + s * 2.3) * 0.2


def grad(c, rect, top, bot):
    def col(h):
        h = h.lstrip("#"); return skia.ColorSetRGB(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, rect.top()), skia.Point(0, rect.bottom())], [col(top), col(bot)])
    c.drawRect(rect, skia.Paint(Shader=sh))


class Cam:
    """Máy quay: tâm (cx,cy), zoom z, nghiêng rot (độ), rung tay shake (px)."""

    def __init__(self, cx, cy, z=1.0, rot=0.0, shake=0.0, t=0.0):
        self.cx, self.cy, self.z, self.rot = cx, cy, z, rot
        self.sx, self.sy = shake * noise1(t * 3, 1.0), shake * noise1(t * 3, 4.0)

    def layer(self, c, f=1.0):
        """f < 1: lớp xa (trôi chậm hơn), f > 1: lớp tiền cảnh (trôi nhanh hơn)."""
        c.save()
        c.translate(W / 2 + self.sx, H / 2 + self.sy)
        c.rotate(self.rot)
        z = 1 + (self.z - 1) * f
        c.scale(z, z)
        c.translate(-(W / 2 + (self.cx - W / 2) * f), -(H / 2 + (self.cy - H / 2) * f))

    def end(self, c):
        c.restore()


def wave_band(c, y, t, col, amp=14, speed=1.0, x0=-1200, x1=W + 1200, a=255):
    p = skia.Path(); p.moveTo(x0, y + 2000)
    for x in range(int(x0), int(x1) + 60, 60):
        p.lineTo(x, y + amp * math.sin(x * 0.011 + t * speed * 1.4))
    p.lineTo(x1, y + 2000); p.close()
    c.drawPath(p, P(col, a))


def boat(c, x, y, s, t):
    c.save(); c.translate(x, y + 6 * math.sin(t * 2)); c.rotate(2 * math.sin(t * 1.6)); c.scale(s, s)
    hull = skia.Path(); hull.moveTo(-340, -40); hull.lineTo(340, -40); hull.quadTo(300, 60, 220, 70); hull.lineTo(-240, 70)
    hull.quadTo(-320, 50, -340, -40); hull.close()
    fo(c, hull, "#8A5E3A", ow=7)
    c.drawLine(-320, -10, 320, -10, P("#6E4A2E", stroke=6))
    c.restore()


def fish(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    fo(c, oval(0, 0, 40, 16), "#B8C8D0", ow=4)
    tl = skia.Path(); tl.moveTo(34, 0); tl.lineTo(60, -16); tl.lineTo(60, 16); tl.close(); fo(c, tl, "#A0B4BE", ow=4)
    c.drawCircle(-24, -3, 4, P(INK))
    c.restore()


def fishers(c, t, x, y, s):
    pull = math.sin(t * 2.4)
    draw_stick(c, Stick("father", x - 130 * s, y, s, t, face=1, hand_f=(120 + 30 * pull, 40 - 20 * pull), hand_b=(150 + 30 * pull, 60 - 20 * pull),
                        lean=8 + 6 * pull, mouth="smile"))
    draw_stick(c, Stick("you", x + 130 * s, y, s, t + 0.4, face=1, hand_f=(110 + 30 * pull, 50 - 20 * pull), hand_b=(140 + 30 * pull, 70 - 20 * pull),
                        lean=8 + 6 * pull, eyes="happy" if t > 3.0 else "dot", mouth="grin" if t > 3.0 else "smile"))
    net = skia.Path(); net.moveTo(x + 270 * s + 30 * pull * s, y - 260 * s - 20 * pull * s); net.quadTo(x + 450 * s, y - 60 * s, x + 530 * s, y + 40 * s)
    c.drawPath(net, P(INK, stroke=4 * s))
    boat(c, x, y + 20 * s, s, t)


# ---------------------------------------------------------------- 1. Cẩu máy từ trời xuống biển (0–2,2)
def s1(c, t):
    q = ease_in_out(t / 2.2)
    K = Cam(lerp(1100, 980, q), lerp(-420, 600, q), lerp(0.95, 1.3, q), rot=lerp(-2, 0, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, 3000), "#E89A6A", "#FCE6C8")
    K.end(c)
    K.layer(c, 0.25)
    c.drawCircle(1500, 500, 120, P("#FFE0A8"))
    for k in range(6):
        c.drawCircle(300 + k * 300, 120 + (k % 2) * 80, 60, P("#FFFFFF", 120))
    K.end(c)
    K.layer(c, 0.5)
    wave_band(c, 560, t, "#9DB7C2", amp=6)
    for k in range(5):
        x = 120 + k * 90
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(x, 520, 70, 46)) or skia.Path(), "#C9B79A", ow=4)
    K.end(c)
    K.layer(c, 1.0)
    wave_band(c, 640, t, "#7FA1B0", amp=8)
    fishers(c, t, 980, 760, 0.85)
    wave_band(c, 830, t + 1, "#6A92A4", amp=12)
    K.end(c)
    K.layer(c, 1.5)
    wave_band(c, 900, t * 1.4, "#5A8294", amp=18)
    K.end(c)


# ---------------------------------------------------------------- 2. Lướt sát mặt nước, cá vọt về phía máy (2,2–4,2)
def s2(c, t):
    lt = t - 2.2
    q = ease_in_out(lt / 2.0)
    K = Cam(lerp(700, 1350, q), 560, 1.0, rot=3 * noise1(t, 2.0), shake=6, t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, 4000), "#F2B48A", "#FCE6C8")
    K.end(c)
    K.layer(c, 0.3)
    c.drawCircle(1700, 380, 140, P("#FFE0A8"))
    wave_band(c, 520, t, "#9DB7C2", amp=6)
    K.end(c)
    K.layer(c, 1.0)
    fishers(c, t, 900, 800, 1.2)
    K.end(c)
    K.layer(c, 1.4)
    wave_band(c, 880, t * 1.5, "#6A92A4", amp=26)
    K.end(c)
    # cá vọt khỏi mặt nước, lao thẳng về phía ống kính
    if lt > 0.9:
        k = clamp((lt - 0.9) / 1.1)
        fish(c, lerp(1300, 1000, k), lerp(900, 420, k) - 200 * math.sin(math.pi * k * 0.7), lerp(1.0, 9.0, k ** 2.2), rot=lerp(-30, 25, k))
    K.layer(c, 2.2)
    wave_band(c, 1000, t * 2, "#4A7284", amp=40)
    K.end(c)


# ---------------------------------------------------------------- 3. Nồi cơm cận, máy ngước theo khói lên mặt mẹ (4,2–5,6)
def kitchen(c, t, K, with_you=0.0, you_x=1700, mother=True):
    K.layer(c, 0.6)
    grad(c, skia.Rect.MakeXYWH(-1500, -1500, W + 3000, H + 3000), "#5A4636", "#3A2C22")
    door_open = with_you
    for k in range(3):
        x = 1500 + k * 100 + door_open * 220 * (k - 1)
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(x, 300, 100, 560)) or skia.Path(), "#F6E7C0", ow=5)
        for j in range(1, 4):
            c.drawLine(x, 300 + j * 140, x + 100, 300 + j * 140, P(INK, stroke=4))
    if door_open > 0:
        light = P("#FFF4D6", 255 * door_open)
        c.drawRect(skia.Rect.MakeXYWH(1600 - 220 * door_open, 300, 440 * door_open, 560), light)
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-1500, 860, W + 3000, 800), P("#6E5642"))
    c.drawLine(-1500, 860, W + 1500, 860, P(INK, stroke=6))
    glow = P("#F39C12", 90); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60))
    c.drawCircle(760, 820, 220, glow)
    stir = math.sin(t * 4)
    if mother:
        draw_stick(c, Stick("mother", 560, 860, 1.0, t, face=1, hand_f=(150 + 20 * stir, 10 + 10 * math.cos(t * 4)), hand_b=(110, 60),
                            lean=6, mouth="smile", look=(1, 0.3) if with_you < 0.3 else (1, -0.2)))
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(620, 760, 280, 100)) or skia.Path(), "#8A7A6A", ow=6)
    for k, colr in enumerate(["#C0392B", "#F39C12", "#F4D03F"]):
        fl = skia.Path(); h = 70 - k * 18; w = 50 - k * 12
        fl.moveTo(760 - w, 770); fl.quadTo(760 - w, 770 - h * 0.6, 760 + 6 * math.sin(t * 12 + k), 770 - h); fl.quadTo(760 + w, 770 - h * 0.6, 760 + w, 770); fl.close()
        c.drawPath(fl, P(colr))
    pot = skia.Path(); pot.moveTo(660, 640); pot.lineTo(860, 640); pot.quadTo(850, 740, 760, 745); pot.quadTo(670, 740, 660, 640); pot.close()
    fo(c, pot, "#3A3A3A", ow=6)
    fo(c, oval(760, 640, 110, 22), "#2A2A2A", ow=5)
    for k in range(5):
        q = (t * 0.6 + k / 5) % 1
        stp = P("#FFFFFF", 180 * (1 - q)); stp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
        c.drawCircle(740 + 30 * math.sin(q * 6 + k), 610 - q * 300, 24 + q * 34, stp)
    if with_you > 0:
        walking = you_x > 1185
        draw_stick(c, Stick("you", you_x, 860, 1.0, t, face=-1, walk=abs(you_x - 1700) / 70 * math.pi if walking else None,
                            hand_f=None if walking else (60, -180 + 10 * math.sin(t * 8)), eyes="happy", mouth="grin"))
        if not walking:
            for k in range(3):
                fo(c, oval(you_x - 70 + k * 8, 860 - 360 + k * 30, 14, 30), "#B8C8D0", ow=4)
    K.end(c)


def s3(c, t):
    lt = t - 4.2
    q = ease_in_out(lt / 1.4)
    K = Cam(lerp(760, 640, q), lerp(700, 470, q), lerp(3.2, 2.2, q), rot=lerp(4, 0, q), t=t)
    kitchen(c, t, K)


# ---------------------------------------------------------------- 4. Qua vai mẹ: cửa kéo mở, bạn bước vào ngược sáng (5,6–7,0)
def s4(c, t):
    lt = t - 5.6
    q = ease_in_out(lt / 1.4)
    K = Cam(lerp(1150, 1280, q), 560, lerp(1.2, 1.45, q), t=t, shake=2)
    door = ease_out(clamp(lt / 0.5))
    yx = lerp(1700, 1260, ease_out(clamp((lt - 0.3) / 1.0)))
    kitchen(c, t, K, with_you=door, you_x=yx, mother=False)
    # vai mẹ tiền cảnh (mờ, tối) — trôi nhanh hơn cảnh
    K.layer(c, 1.6)
    sil = P("#1A120E", 235); sil.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
    c.drawCircle(1000, 360, 150, sil)
    c.drawRoundRect(skia.Rect.MakeXYWH(820, 470, 380, 700), 120, 120, sil)
    K.end(c)


# ---------------------------------------------------------------- 5. Bám gót chân trưởng làng, ngước lên tờ giấy đỏ (7,0–8,4)
def village(c, K, t, chief_x, give=0.0, show_you=False):
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#C9D6DA", "#EDEAE2")
    K.end(c)
    K.layer(c, 0.45)
    for k in range(-2, 8):
        x = 100 + k * 480
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(x, 520, 300, 340)) or skia.Path(), "#D8C8A8", ow=6)
        roof = skia.Path(); roof.moveTo(x - 50, 530); roof.lineTo(x + 150, 400); roof.lineTo(x + 350, 530); roof.close()
        fo(c, roof, "#5A4A3E", ow=6)
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, 860, W + 6000, 800), P("#CDBF9E"))
    c.drawLine(-3000, 860, W + 3000, 860, P(INK, stroke=6))
    for k in range(30):
        x = -1000 + k * 140
        c.drawCircle(x, 900 + (k % 3) * 30, 6, P("#A89A7A"))
    walking = give <= 0
    draw_stick(c, Stick("chief", chief_x, 860, 1.0, t, face=1, walk=chief_x / 70 * math.pi if walking else None,
                        hand_f=(lerp(60, 170, give), lerp(120, -20, give)), mouth="flat", brow=-0.3))
    hx = chief_x + lerp(60, 170, give) + 20
    hy = 860 - 2 * 108 - 150 + lerp(120, -20, give)
    c.save(); c.translate(hx, hy); c.rotate(-8)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-10, -40, 70, 90)) or skia.Path(), "#C0392B", ow=4)
    c.restore()
    if show_you:
        draw_stick(c, Stick("you", chief_x + 380, 860, 1.0, t, face=-1, eyes="wide" if give > 0.6 else "dot",
                            mouth="o" if give > 0.6 else "smile", hand_f=(70, lerp(140, 30, give)), look=(-1, 0.3)))
    K.end(c)
    K.layer(c, 1.8)
    for k in range(6):
        x = -600 + k * 700
        c.drawCircle(x, 1080, 90, P("#7A8A5A"))
        c.drawCircle(x + 60, 1050, 70, P("#6A7A4A"))
    K.end(c)


def s5(c, t):
    lt = t - 7.0
    chief_x = lerp(200, 760, clamp(lt / 1.0))
    up = ease_in_out(clamp((lt - 0.8) / 0.6))
    give = ease_out(clamp((lt - 1.0) / 0.4))
    K = Cam(chief_x + lerp(0, 80, up), lerp(840, 520, up), lerp(2.6, 1.6, up), rot=lerp(-4, 0, up), shake=4, t=t)
    village(c, K, t, chief_x, give=give if lt > 1.0 else 0.0, show_you=True)


# ---------------------------------------------------------------- 6. Cận mặt bạn, zoom giật + nghiêng khung (8,4–9,4)
def s6(c, t):
    lt = t - 8.4
    hit = clamp((lt - 0.35) / 0.12)
    K = Cam(1140, 330, lerp(2.4, 3.6, hit), rot=lerp(0, -9, hit), shake=3 + 8 * hit * math.exp(-max(0, lt - 0.4) * 4), t=t)
    village(c, K, t, 760, give=1.0, show_you=True)
    if hit > 0:
        for k in range(24):
            a = k * 2 * math.pi / 24
            c.drawLine(W / 2 + 600 * math.cos(a), H / 2 + 600 * math.sin(a), W / 2 + 1400 * math.cos(a), H / 2 + 1400 * math.sin(a),
                       P("#FFFFFF", 90 * hit, stroke=5))


# ---------------------------------------------------------------- 7. Tờ giấy đỏ đập vào khung, thế giới quanh hóa xám (9,4–10,5)
def s7(c, t):
    lt = t - 9.4
    q = ease_out(clamp(lt / 0.35))
    grad(c, skia.Rect.MakeWH(W, H), "#6E6E6E", "#3E3E3E")
    c.save(); c.translate(W / 2 + 4 * noise1(t * 4), H / 2 + 10); c.rotate(lerp(25, -3, q) + 0.8 * math.sin(lt * 3)); c.scale(lerp(3.2, 0.95, q) + 0.03 * lt, lerp(3.2, 0.95, q) + 0.03 * lt)
    c.drawRect(skia.Rect.MakeXYWH(-310, -400, 640, 840), P("#000000", 80))
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-320, -430, 640, 840)) or skia.Path(), "#C83A2E", ow=8)
    for k in range(9):
        w = 460 if k % 3 else 300
        c.drawLine(-w / 2, -300 + k * 70, w / 2, -300 + k * 70, P("#3A1410", stroke=12))
    c.drawCircle(200, 300, 60, P("#3A1410", stroke=8))
    c.restore()


# ---------------------------------------------------------------- bản v3: nhịp vừa phải, chỉ nhanh ở cao trào
def m1(c, t):  # 0–4,2: một cú cẩu máy chậm từ trời xuống, trôi nhẹ theo thuyền; cá nhảy trong khung
    q = ease_in_out(clamp(t / 3.4))
    K = Cam(lerp(1060, 1000, q), lerp(150, 600, q), lerp(1.0, 1.18, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, 3000), "#E89A6A", "#FCE6C8")
    K.end(c)
    K.layer(c, 0.25)
    c.drawCircle(1500, 500, 120, P("#FFE0A8"))
    for k in range(6):
        c.drawCircle(300 + k * 300 + t * 6, 120 + (k % 2) * 80, 60, P("#FFFFFF", 120))
    K.end(c)
    K.layer(c, 0.5)
    wave_band(c, 560, t, "#9DB7C2", amp=6)
    for k in range(5):
        x = 120 + k * 90
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(x, 520, 70, 46)) or skia.Path(), "#C9B79A", ow=4)
    K.end(c)
    K.layer(c, 1.0)
    wave_band(c, 640, t, "#7FA1B0", amp=8)
    fishers(c, t, 980, 760, 0.85)
    if t > 2.6:
        k = clamp((t - 2.6) / 0.9)
        fish(c, 1430 + 70 * k, 790 - 200 * math.sin(math.pi * k), 1.2, rot=-40 + 80 * k)
    wave_band(c, 830, t + 1, "#6A92A4", amp=12)
    K.end(c)
    K.layer(c, 1.3)
    wave_band(c, 900, t * 1.2, "#5A8294", amp=16)
    K.end(c)


def m2(c, t):  # 4,2–7,0: cận nồi cơm, ngước chậm lên mặt mẹ, rồi lia nhẹ sang cửa khi bạn bước vào
    lt = t - 4.2
    up = ease_in_out(clamp(lt / 1.4))
    pan = ease_in_out(clamp((lt - 1.3) / 1.4))
    K = Cam(lerp(lerp(760, 640, up), 1050, pan), lerp(lerp(640, 480, up), 560, pan), lerp(lerp(2.2, 1.9, up), 1.2, pan), t=t)
    door = ease_out(clamp((lt - 1.2) / 0.5))
    yx = lerp(1700, 1260, ease_out(clamp((lt - 1.5) / 1.1)))
    kitchen(c, t, K, with_you=door, you_x=yx)


def m3(c, t):  # 7,0–9,0: máy trôi chậm theo trưởng làng tới chỗ bạn
    lt = t - 7.0
    chief_x = lerp(300, 760, ease_out(clamp(lt / 1.2)))
    give = ease_out(clamp((lt - 1.25) / 0.45))
    K = Cam(lerp(700, 960, ease_in_out(clamp(lt / 2.0))), 540, 1.25, t=t)
    village(c, K, t, chief_x, give=give if lt > 1.25 else 0.0, show_you=True)


def m4(c, t):  # 9,0–9,4: CAO TRÀO — zoom nhanh vào mặt bạn, khung nghiêng
    lt = t - 9.0
    hit = ease_out(clamp(lt / 0.25))
    K = Cam(lerp(960, 1140, hit), lerp(540, 330, hit), lerp(1.25, 3.4, hit), rot=lerp(0, -8, hit),
            shake=6 * hit * math.exp(-max(0, lt - 0.25) * 6), t=t)
    village(c, K, t, 760, give=1.0, show_you=True)


SHOTS = [(0, 4.2, m1), (4.2, 7.0, m2), (7.0, 9.0, m3), (9.0, 9.4, m4), (9.4, DUR, s7)]
FLASH = {9.4}   # chỉ chớp sáng ở điểm cắt cao trào
VO = [(0.3, 2.0, "Bạn mười chín tuổi."), (2.2, 4.1, "Bạn sống ở một làng chài nhỏ bên bờ biển Nhật Bản."),
      (4.3, 6.9, "Mỗi tối mẹ bạn nấu một nồi cơm trắng…"), (7.1, 9.3, "Rồi một hôm, ông trưởng làng mang tới một tờ giấy màu đỏ."),
      (9.4, 10.4, "Người ta gọi nó là “giấy đỏ”.")]


def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas(); c.clear(skia.ColorWHITE)
    for a, b, fn in SHOTS:
        if a <= t < b:
            c.save(); fn(c, t); c.restore()
            if a in FLASH and t - a < 0.08:        # chớp sáng chỉ ở điểm cắt cao trào
                c.drawRect(skia.Rect.MakeWH(W, H), P("#FFFFFF", 70 * (1 - (t - a) / 0.08)))
            break
    for a, b, s in VO:
        if a <= t < b:
            al = 255 * clamp(min(t - a, b - t) / 0.2)
            text(c, s, W / 2, 1040, "bold", 44, "#FFFFFF", a=al, align="center", stroke=8, stroke_color="#111111")
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def chunk(args):
    k, f0, f1 = args
    out = BUILD / f"t2_{k:02d}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    s = skia.Surface(W, H)
    for i in range(f0, f1):
        p.stdin.write(frame(i / FPS, s).tobytes())
    p.stdin.close(); p.wait()
    return out


if __name__ == "__main__":
    BUILD.mkdir(exist_ok=True)
    if sys.argv[1] == "preview":
        for ts in sys.argv[2:]:
            Image.fromarray(frame(float(ts))[..., :3]).save(BUILD / f"pv3_{float(ts):05.2f}.png")
    else:
        nfr = int(DUR * FPS); step = math.ceil(nfr / 4)
        with Pool(4) as pool:
            chs = pool.map(chunk, [(k, f, min(nfr, f + step)) for k, f in enumerate(range(0, nfr, step))])
        (BUILD / "t2.txt").write_text("".join(f"file '{x.name}'\n" for x in chs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(BUILD / "t2.txt"), "-c", "copy",
                        str(BUILD / "Test_mo_dau_v3_nosfx.mp4")], check=True)
        for x in chs:
            x.unlink()
        (BUILD / "t2.txt").unlink()
        print("xong")
