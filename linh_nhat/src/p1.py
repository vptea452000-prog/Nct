"""Phần 1 (voice_1, 75,7 s): làng chài → giấy đỏ → thắt lưng nghìn mũi chỉ → sân ga → trại lính → Kenji.
Mốc câu lấy từ audio/voice_1_align.json (src/align.py). Máy chuyển động vừa phải; chỉ nhanh ở cao trào.
  python3 src/p1.py preview 5 20 ...   → p1/build/pv_<t>.png
  python3 src/p1.py full               → p1/build/P1_nosfx.mp4
"""
import math, subprocess, sys, json
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT.parent / "tools")); sys.path.insert(0, str(ROOT.parent / "cung" / "src"))
import skia  # noqa
from PIL import Image  # noqa
from lib import text  # noqa
import stick2  # noqa
from stick2 import Stick, draw_stick, P, fo, oval, clamp, lerp, ease_out, ease_in_out, back_out, INK, LOOKS  # noqa
import test_open2 as T2  # noqa
from test_open2 import Cam, grad, noise1, W, H, FPS  # noqa

PART = ROOT / "p1"
BUILD = PART / "build"
ALIGN = json.load(open(ROOT / "audio" / "voice_1_align.json"))
DUR = 75.69
SUBS = True

# người phụ nữ trong làng (khâu thắt lưng), lính mới khác
for i, (a, b) in enumerate([("#5A7A6A", "#46604F"), ("#8A6A9A", "#6E5480"), ("#A08A5A", "#806E46"), ("#6A6A8A", "#54546E")]):
    LOOKS[f"woman{i}"] = dict(LOOKS["mother"], civ=(a, b), hair_col=["#2A2A2A", "#4A3A2A", "#AAAAAA", "#2A2A2A"][i])
for i, hc in enumerate(["#1E1E1E", "#3A2A1A", "#2A2A2A", "#1E1E1E"]):
    LOOKS[f"recruit{i}"] = dict(LOOKS["you"], headband=None, hair_col=hc, head=72 + i * 2, body=1.0 + 0.06 * (i % 2))

GROUND = 860
HEAD_Y = 436          # tâm đầu cách chân (đơn vị khung) với nhân vật thân 1.0


def head_xy(x, y, s, who="you", crouch=0.0):
    L = LOOKS[who]
    tor = 150 * min(1.15, L["body"] ** 0.5)
    return x + 4 * s, y - (216 - crouch * 70 + tor + L["head"] - 4) * s


def cheek(c, x, y, s, face=1, who="you"):
    hx, hy = head_xy(x, y, s, who)
    c.drawOval(skia.Rect.MakeXYWH(hx + face * 8 * s - 22 * s, hy + 10 * s, 44 * s, 24 * s), P("#E8504A", 200))


def ease_shot(t, a, b):
    return ease_in_out(clamp((t - a) / max(1e-3, b - a)))


# ---------------------------------------------------------------- bối cảnh mới
def house_in(c, K, t, night=False, lamp=True):
    K.layer(c, 0.7)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, H + 4000), "#24304A" if night else "#6A5442", "#141A28" if night else "#4A3A2E")
    for k in range(-2, 6):
        x = 200 + k * 360
        c.drawLine(x, 200, x, GROUND, P("#000000", 50, stroke=10))
    win = skia.Rect.MakeXYWH(1300, 260, 360, 300)
    c.drawRect(win, P("#2E3E62" if night else "#F6E7C0"))
    if night:
        c.drawCircle(1560, 340, 34, P("#F2EED8"))
    for k in range(1, 3):
        c.drawLine(1300 + k * 120, 260, 1300 + k * 120, 560, P(INK, stroke=5))
    c.drawLine(1300, 410, 1660, 410, P(INK, stroke=5))
    c.drawRect(win, P(INK, stroke=6))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-2000, GROUND, W + 4000, 900), P("#3A3040" if night else "#8A7458"))
    c.drawLine(-2000, GROUND, W + 2000, GROUND, P(INK, stroke=6))
    if lamp:
        g = P("#F6C46A", 120 if night else 60); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 90))
        c.drawCircle(560, 720, 260, g)
        fo(c, skia.Path().addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(520, 640, 80, 120), 14, 14)) or skia.Path(), "#F8E6B8", ow=5)
        c.drawLine(560, 760, 560, GROUND, P(INK, stroke=6))
    K.end(c)


def lane_bg(c, K, t, sun=0.0):
    K.layer(c, 0.0)
    top = ["#9FC9E6", "#F2B48A"][0] if sun < 0.6 else "#F2B48A"
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), lerp_col("#A9D2EA", "#F2A878", sun), lerp_col("#EEF1E6", "#FCE0C0", sun))
    K.end(c)
    K.layer(c, 0.2)
    sx = lerp(300, 1700, sun); sy = 300 + 260 * (2 * sun - 1) ** 2
    c.drawCircle(sx, sy, 80, P("#FFE6A8"))
    K.end(c)
    K.layer(c, 0.5)
    for k in range(-2, 8):
        x = 60 + k * 420
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(x, 520, 300, 340)) or skia.Path(), "#D8C8A8", ow=6)
        roof = skia.Path(); roof.moveTo(x - 50, 530); roof.lineTo(x + 150, 400); roof.lineTo(x + 350, 530); roof.close()
        fo(c, roof, "#5A4A3E", ow=6)
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P("#CDBF9E"))
    c.drawLine(-3000, GROUND, W + 3000, GROUND, P(INK, stroke=6))
    # bóng đổ dài dần theo giờ
    K.end(c)


def lerp_col(a, b, q):
    a = a.lstrip("#"); b = b.lstrip("#")
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]; cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{int(lerp(x, y, clamp(q))):02X}" for x, y in zip(ca, cb))


def cloth_band(c, x0, y0, x1, y1, dots=0, w=26):
    c.drawLine(x0, y0, x1, y1, P(INK, stroke=w + 8)); c.drawLine(x0, y0, x1, y1, P("#F6F2E8", stroke=w))
    for k in range(min(dots, 40)):
        q = (k + 0.5) / 40
        c.drawCircle(lerp(x0, x1, q), lerp(y0, y1, q) + (5 if k % 2 else -5), 3.5, P("#C0392B"))


def flag(c, x, y, s, t, seed=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawLine(0, 0, 0, -140, P(INK, stroke=6))
    wv = 8 * math.sin(t * 6 + seed)
    f = skia.Path(); f.moveTo(0, -140); f.quadTo(40, -150 + wv, 90, -140); f.lineTo(90, -80); f.quadTo(40, -90 + wv, 0, -80); f.close()
    fo(c, f, "#FFFFFF", ow=4)
    c.drawCircle(45, -110 + wv * 0.5, 16, P("#C0392B"))
    c.restore()


def train(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(3):
        cx = k * 620
        fo(c, skia.Path().addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx, -420, 600, 360), 30, 30)) or skia.Path(), "#3E4A3E", ow=7)
        for j in range(4):
            fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(cx + 40 + j * 140, -370, 100, 110)) or skia.Path(), "#F6E7C0", ow=5)
        for wx in (cx + 90, cx + 510):
            c.drawCircle(wx, -50, 50, P("#2A2A2A")); c.drawCircle(wx, -50, 18, P("#8A8A8A"))
    c.restore()


def barracks_bg(c, K, t, inside=False, night=False):
    if inside:
        K.layer(c, 0.7)
        grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, H + 4000), "#2A3040" if night else "#8A7A62", "#181C26" if night else "#6A5C48")
        for k in range(-2, 7):
            x = 100 + k * 330
            c.drawLine(x, 120, x, GROUND, P("#000000", 60, stroke=14))
        K.end(c)
        K.layer(c, 1.0)
        c.drawRect(skia.Rect.MakeXYWH(-2000, GROUND, W + 4000, 900), P("#3A3A44" if night else "#7A6A52"))
        c.drawLine(-2000, GROUND, W + 2000, GROUND, P(INK, stroke=6))
        K.end(c)
        return
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#B8C4C8", "#E2E0D8")
    K.end(c)
    K.layer(c, 0.5)
    for k in range(-1, 4):
        x = k * 760
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(x, 420, 700, 440)) or skia.Path(), "#8A7458", ow=6)
        roof = skia.Path(); roof.moveTo(x - 40, 430); roof.lineTo(x + 350, 330); roof.lineTo(x + 740, 430); roof.close()
        fo(c, roof, "#4A4A4A", ow=6)
        for j in range(5):
            fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(x + 40 + j * 130, 520, 80, 90)) or skia.Path(), "#3A3A3A", ow=4)
    c.drawLine(1500, 860, 1500, 200, P(INK, stroke=10))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P("#B8A47E"))
    c.drawLine(-3000, GROUND, W + 3000, GROUND, P(INK, stroke=6))
    K.end(c)


def bunk(c, x, s=1.0):
    c.save(); c.translate(x, GROUND); c.scale(s, s)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-160, -150, 320, 40)) or skia.Path(), "#7A5A3A", ow=5)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-150, -175, 300, 30)) or skia.Path(), "#C9C2B0", ow=4)
    for lx in (-150, 140):
        c.drawLine(lx, -110, lx, 0, P(INK, stroke=10))
    c.restore()


def lying(c, who, x, y, s, t, blanket="#6A7A9A", shake=0.0, **kw):
    """Người nằm ngủ (đầu bên trái), đắp chăn."""
    c.save(); c.translate(x, y); c.rotate(-90)
    draw_stick(c, Stick(who, 0, 0, s, t, face=1, hand_f=(20, 120), hand_b=(-20, 120), **kw))
    c.restore()
    bl = skia.Path(); bl.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 300 * s, y - 70 * s + 6 * shake * math.sin(t * 30), 340 * s, 120 * s), 40 * s, 40 * s))
    fo(c, bl, blanket, ow=6)


def subtitle(c, t):
    if not SUBS:
        return
    for a, b, s in ALIGN:
        if a <= t < b:
            al = 255 * clamp(min(t - a, b - t) / 0.15)
            words, lines, cur = s.split(), [], ""
            from lib import tw
            for w_ in words:
                tst = (cur + " " + w_).strip()
                if tw(tst, "bold", 42) > 1500 and cur:
                    lines.append(cur); cur = w_
                else:
                    cur = tst
            lines.append(cur)
            y0 = 1040 - 54 * (len(lines) - 1)
            for i, l in enumerate(lines):
                text(c, l, W / 2, y0 + i * 54, "bold", 42, "#FFFFFF", a=al, align="center", stroke=8, stroke_color="#111111")
            return


# ---------------------------------------------------------------- các cảnh (mốc tuyệt đối trong phần 1)
def c_sea(c, t):                       # 0–4,0  Bạn 19 tuổi · làng chài
    T2.m1(c, t * 4.2 / 4.0)


def c_kitchen(c, t):                   # 4,0–6,6  mỗi sáng ra khơi… mỗi tối mẹ nấu cơm
    T2.m2(c, 4.2 + (t - 4.0) * 2.8 / 2.6)


def c_bay(c, t):                       # 6,6–10,2  thế giới chỉ rộng bằng cái vịnh
    q = ease_shot(t, 6.6, 10.2)
    K = Cam(lerp(1100, 960, q), lerp(620, 520, q), lerp(1.7, 1.0, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#E8946A", "#FAD9B0")
    K.end(c)
    K.layer(c, 0.3)
    c.drawCircle(960, 470, 90, P("#FFE0A8"))
    K.end(c)
    K.layer(c, 0.7)
    T2.wave_band(c, 560, t, "#7FA1B0", amp=4, x0=-3000, x1=W + 3000)
    for sd in (-1, 1):   # hai mũi đất ôm lấy vịnh
        hd = skia.Path(); hd.moveTo(960 + sd * 2400, 900); hd.lineTo(960 + sd * 2400, 420)
        hd.quadTo(960 + sd * 900, 430, 960 + sd * 520, 600); hd.lineTo(960 + sd * 600, 900); hd.close()
        fo(c, hd, "#5E6E4E", ow=6)
    for k in range(4):
        T2.boat(c, 760 + k * 140, 590 + (k % 2) * 14, 0.12, t + k)
    K.end(c)
    K.layer(c, 1.0)
    hill = skia.Path(); hill.moveTo(-3000, H + 400); hill.lineTo(-3000, 800); hill.quadTo(900, 700, 1500, 760); hill.quadTo(2400, 820, W + 3000, 800)
    hill.lineTo(W + 3000, H + 400); hill.close()
    fo(c, hill, "#6E7E52", ow=6)
    draw_stick(c, Stick("you", 1100, 820, 0.9, t, face=-1, sit=1.0, hand_f=(80, 150), hand_b=(-40, 160), look=(-0.5, 0.2), mouth="smile"))
    K.end(c)


def c_chief(c, t):                     # 10,2–13,0  trưởng làng mang tờ giấy đỏ
    T2.m3(c, 7.0 + (t - 10.2) * 2.0 / 2.8)


def c_zoom(c, t):                      # 13,0–13,4  CAO TRÀO
    T2.m4(c, 9.0 + (t - 13.0))


def c_paper(c, t):                     # 13,4–14,5  "giấy đỏ"
    T2.s7(c, 9.4 + (t - 13.4))


def c_must(c, t):                      # 14,5–16,2  ai nhận được nó, phải lên đường
    q = ease_shot(t, 14.5, 16.2)
    K = Cam(lerp(900, 980, q), lerp(560, 520, q), lerp(1.2, 1.45, q), t=t)
    house_in(c, K, t, night=False, lamp=False)
    K.layer(c, 1.0)
    draw_stick(c, Stick("mother", 620, GROUND, 1.0, t, face=1, hand_f=(60, 150), hand_b=(20, 160), eyes="dot", mouth="flat", look=(1, 0)))
    draw_stick(c, Stick("you", 1180, GROUND, 1.0, t, face=-1, hand_f=(70, 40), hand_b=(40, 60), eyes="dot", mouth="flat", look=(-0.3, 1)))
    hx = 1180 - 70 - 30
    c.save(); c.translate(hx, GROUND - 366 + 40); c.rotate(10)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-40, -50, 80, 100)) or skia.Path(), "#C0392B", ow=4)
    c.restore()
    K.end(c)


def c_night(c, t):                     # 16,2–18,0  đêm trước khi đi, mẹ không ngủ
    q = ease_shot(t, 16.2, 18.0)
    K = Cam(lerp(820, 760, q), lerp(640, 660, q), lerp(1.25, 1.45, q), t=t)
    house_in(c, K, t, night=True, lamp=True)
    K.layer(c, 1.0)
    lying(c, "you", 1250, GROUND - 40, 0.8, t, eyes="closed", mouth="flat")
    draw_stick(c, Stick("mother", 420, GROUND, 1.0, t, face=1, sit=1.0, hand_f=(60, 150), hand_b=(30, 160), eyes="dot", look=(1, 0.6), mouth="flat"))
    K.end(c)


def c_lane(c, t):                      # 18,0–24,1  đứng đầu ngõ từ sáng tới chiều, xin từng người một mũi chỉ
    lt = t - 18.0
    sun = clamp(lt / 6.0)
    K = Cam(lerp(860, 1000, ease_shot(t, 18.0, 24.1)), 560, 1.15, t=t)
    lane_bg(c, K, t, sun)
    K.layer(c, 1.0)
    period = 1.5
    k = int(lt / period); ph = (lt % period) / period
    who = f"woman{k % 4}"
    wx = lerp(1700, 1080, ease_out(clamp(ph / 0.35))) if ph < 0.65 else lerp(1080, 200, ease_in_out((ph - 0.65) / 0.35))
    sewing = 0.35 < ph < 0.65
    draw_stick(c, Stick(who, wx, GROUND, 0.95, t, face=-1 if ph < 0.65 else -1,
                        walk=None if sewing else lt * 7, lean=12 if sewing else 0,
                        hand_f=(110, 20 + 8 * math.sin(lt * 20)) if sewing else None, eyes="dot", mouth="smile"))
    dots = int(lt / period * 6) + (6 if ph > 0.5 else 0)
    draw_stick(c, Stick("mother", 820, GROUND, 1.0, t, face=1, hand_f=(160, 0), hand_b=(120, 20), eyes="dot", mouth="flat", look=(1, 0)))
    cloth_band(c, 870, GROUND - 330, 1020, GROUND - 330, dots=dots)
    K.end(c)
    n = min(1000, int(1000 * (lt / 6.1) ** 1.6))
    text(c, f"{n} mũi chỉ", 1720, 140, "xbold", 54, "#FFFFFF", align="center", stroke=7, stroke_color="#111111")


def c_cloth(c, t):                     # 24,1–26,3  một nghìn người, một nghìn mũi chỉ
    lt = t - 24.1
    grad(c, skia.Rect.MakeWH(W, H), "#E9DFC8", "#D8CCAE")
    c.save(); c.translate(W / 2, H / 2); c.rotate(-4 + lt * 0.8); c.scale(1 + 0.03 * lt, 1 + 0.03 * lt)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-860, -160, 1720, 320)) or skia.Path(), "#F6F2E8", ow=8)
    total = 25 * 8
    shown = int(total * clamp(0.6 + lt / 1.5))
    for i in range(shown):
        cx = -820 + (i % 25) * 68 + (i // 25 % 2) * 30
        cy = -130 + (i // 25) * 36
        c.drawLine(cx - 8, cy - 4, cx + 8, cy + 4, P("#C0392B", stroke=6))
        c.drawCircle(cx + 9, cy + 5, 4, P("#8A1E14"))
    c.restore()
    p = back_out(clamp((lt - 0.6) / 0.4))
    c.save(); c.translate(W / 2, 220); c.scale(p, p)
    text(c, "1.000", 0, 0, "xbold", 120, "#C0392B", align="center", stroke=10, stroke_color="#FFFFFF")
    c.restore()


def c_shield(c, t):                    # 26,3–29,3  tin rằng dải vải che chắn khỏi đạn
    lt = t - 26.3
    q = ease_shot(t, 26.3, 29.3)
    grad(c, skia.Rect.MakeWH(W, H), "#3A2E4A", "#1A1424")
    K = Cam(960, lerp(560, 500, q), lerp(1.4, 1.6, q), t=t)
    K.layer(c, 1.0)
    for r, a in [(330, 40), (250, 70), (180, 110)]:
        g = P("#F4D58A", a * (0.7 + 0.3 * math.sin(t * 3))); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
        c.drawCircle(960, 620, r, g)
    draw_stick(c, Stick("you", 960, GROUND, 1.0, t, face=1, uniform=True, belt=True, eyes="closed", mouth="flat", head_tilt=-4))
    for k in range(5):   # những vệt mờ bị lệch hướng quanh vầng sáng
        a = -0.8 + k * 0.4
        ph = (lt * 0.8 + k * 0.23) % 1
        x0, y0 = 960 + 900 * math.cos(a) * (1 - ph), 600 + 500 * math.sin(a) * (1 - ph)
        c.drawLine(x0, y0, x0 + 40 * math.cos(a), y0 + 40 * math.sin(a), P("#FFFFFF", 120 * (1 - ph), stroke=4))
    K.end(c)


def c_tie(c, t):                       # 29,3–35,2  buộc thắt lưng · bà không khóc · "ăn cho no vào"
    lt = t - 29.3
    if t < 32.3:
        q = ease_shot(t, 29.3, 32.3)
        K = Cam(lerp(940, 900, q), lerp(560, 540, q), lerp(1.45, 1.6, q), t=t)
        tie = ease_out(clamp(lt / 2.2))
        mh = (lerp(170, 120, tie), lerp(120, 160, tie))
    else:
        q = ease_shot(t, 32.3, 35.2)
        K = Cam(lerp(800, 760, q), lerp(430, 420, q), lerp(2.2, 2.5, q), t=t)   # đẩy chậm vào mặt mẹ
        mh = (120, 160) if t < 33.4 else (220, 40 + 6 * math.sin(t * 6))         # vỗ nhẹ vào tay con
    house_in(c, K, t, night=False, lamp=False)
    K.layer(c, 1.0)
    draw_stick(c, Stick("you", 1080, GROUND, 1.0, t, face=-1, belt=lt > 1.6, eyes="dot", look=(-0.6, -0.2), mouth="flat"))
    draw_stick(c, Stick("mother", 760, GROUND, 1.0, t, face=1, hand_f=mh, hand_b=(mh[0] - 40, mh[1] + 10), eyes="dot", look=(0.6, -0.3),
                        mouth="flat" if t < 33.4 else "smile", lean=8))
    K.end(c)


def c_station(c, t):                   # 35,2–40,2  sân ga, cờ phất, bạn cười vẫy tay
    q = ease_shot(t, 35.2, 40.2)
    K = Cam(lerp(700, 1100, q), 520, 1.05, t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#B8C8D0", "#ECEAE2")
    K.end(c)
    K.layer(c, 0.5)
    for k in range(-1, 5):
        c.drawLine(k * 480, 860, k * 480, 280, P("#5A5A5A", stroke=16))
    c.drawRect(skia.Rect.MakeXYWH(-1500, 260, 4800, 40), P("#4A4A4A"))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P("#9A9488"))
    train(c, 700, GROUND - 20, 1.0)
    draw_stick(c, Stick("you", 1080, GROUND - 120, 0.95, t, face=-1, uniform=True, hand_f=(90, -230 + 14 * math.sin(t * 9)), eyes="happy", mouth="grin"))
    crowd = [("woman0", 300), ("chief", 470), ("woman1", 640), ("woman2", 1500), ("recruit1", 1680), ("woman3", 1860), ("mother", 2080)]
    for i, (who, x) in enumerate(crowd):
        if who == "mother":
            draw_stick(c, Stick(who, x, GROUND + 160, 1.05, t, face=-1, hand_f=(40, 150), hand_b=(10, 160), eyes="dot", mouth="flat", look=(-1, -0.4)))
            continue
        draw_stick(c, Stick(who, x, GROUND + 160, 1.05, t + i, face=-1, hand_f=(60, -200 + 20 * math.sin(t * 7 + i)), eyes="happy", mouth="open"))
        flag(c, x - 1.05 * (26 + 60) + 4, GROUND + 160 - 1.05 * (366 + 200) + 40, 1.0, t, seed=i)
    K.end(c)


def c_noturn(c, t):                    # 40,2–42,7  không dám quay đầu nhìn mẹ lần thứ hai
    q = ease_shot(t, 40.2, 42.7)
    K = Cam(lerp(1060, 1900, ease_shot(t, 41.2, 42.7)), lerp(330, 560, ease_shot(t, 41.2, 42.7)), lerp(2.6, 2.0, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#B8C8D0", "#ECEAE2")
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P("#9A9488"))
    train(c, 700, GROUND - 20, 1.0)
    draw_stick(c, Stick("you", 1080, GROUND - 120, 0.95, t, face=-1, uniform=True, hand_f=(70, 40), eyes="dot", look=(-1, 0), mouth="flat"))
    draw_stick(c, Stick("mother", 2080, GROUND + 160, 1.05, t, face=-1, hand_f=(40, 150), hand_b=(10, 160), eyes="dot", mouth="flat", look=(-1, -0.4)))
    K.end(c)


def recruits_row(c, t, x0, n=5, gap=230, s=1.0, sweat=0.0, bow=0.0, start=0):
    for i in range(n):
        who = "you" if i == 2 else f"recruit{(i + start) % 4}"
        draw_stick(c, Stick(who, x0 + i * gap, GROUND, s, t + i * 0.3, face=1, uniform=True, cap="soldier",
                            hand_f=(20, 170), hand_b=(-20, 170), eyes="dot", mouth="flat", lean=bow * 30, sweat=sweat,
                            head_tilt=bow * 10))


def c_yard(c, t):                      # 42,7–47,2  doanh trại: không phải bắn súng, mà là đứng thẳng
    q = ease_shot(t, 42.7, 47.2)
    K = Cam(lerp(700, 1000, q), 540, lerp(1.0, 1.15, q), t=t)
    barracks_bg(c, K, t)
    K.layer(c, 1.0)
    recruits_row(c, t, 520)
    sx = lerp(400, 1500, ease_shot(t, 42.9, 47.0))
    draw_stick(c, Stick("sergeant", sx, GROUND + 120, 1.05, t, face=1, uniform=True, walk=None if t > 46.6 else t * 5,
                        hand_b=(-60, 120), mouth="frown", brow=-1))
    K.end(c)


def c_shout(c, t):                     # 47,2–49,7  đứng thẳng khi bị quát · khi bị tát
    K = Cam(980, 420, 2.1, t=t)
    slap = t > 48.84
    if slap:
        k = clamp((t - 48.84) / 0.12)
        K = Cam(1000, 420, lerp(2.1, 2.5, k), rot=lerp(0, 4, k), shake=8 * math.exp(-(t - 48.84) * 5), t=t)
    barracks_bg(c, K, t)
    K.layer(c, 1.0)
    draw_stick(c, Stick("you", 1160, GROUND, 1.0, t, face=-1, uniform=True, cap="soldier", hand_f=(20, 170), hand_b=(-20, 170),
                        eyes="squint" if slap else "dot", mouth="flat", head_tilt=14 if slap else 0, look=(-1, 0)))
    if slap:
        cheek(c, 1160, GROUND, 1.0, face=-1)
    draw_stick(c, Stick("sergeant", 800, GROUND, 1.05, t, face=1, uniform=True, hand_f=(80, -60) if not slap else (170, -120),
                        mouth="open", brow=-1, lean=8))
    if not slap:
        hx, hy = head_xy(800, GROUND, 1.05, "sergeant")
        for k in range(4):
            a = -0.5 + k * 0.33
            c.drawLine(hx + 120 + 30 * math.cos(a), hy + 40 * math.sin(a), hx + 200 + 30 * math.cos(a), hy + 70 * math.sin(a), P(INK, stroke=5))
    K.end(c)
    if slap and t - 48.84 < 0.07:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#FFFFFF", 140))


def c_inspect(c, t):                   # 49,7–55,6  một chiếc cúc chưa cài… cả phòng chịu phạt
    lt = t - 49.7
    if lt < 1.8:   # cận chiếc cúc chưa cài
        q = ease_shot(t, 49.7, 51.5)
        grad(c, skia.Rect.MakeWH(W, H), "#8C7E4E", "#6E623C")
        c.save(); c.translate(W / 2, H / 2); c.scale(1 + 0.06 * q, 1 + 0.06 * q)
        for k in range(4):
            y = -330 + k * 220
            c.drawCircle(-20 if k != 2 else 40, y, 46, P("#D9C27A")); c.drawCircle(-20 if k != 2 else 40, y, 46, P(INK, stroke=6))
            if k != 2:
                c.drawLine(-80, y, 40, y, P(INK, stroke=5))
        c.drawLine(0, -500, 0, 600, P(INK, 140, stroke=6))
        c.restore()
        # ngón tay đội trưởng chỉ vào
        hx = lerp(W + 200, 1200, ease_out(clamp(lt / 0.6)))
        c.drawLine(hx, 560, hx + 600, 640, P(INK, stroke=40)); c.drawLine(hx, 560, hx + 600, 640, P(stick2.UNIFORM[0], stroke=30))
        c.drawCircle(hx, 560, 26, P(INK))
        return
    q = ease_shot(t, 51.5, 55.6)
    K = Cam(lerp(960, 900, q), 540, lerp(1.0, 1.1, q), t=t)
    barracks_bg(c, K, t, inside=True)
    K.layer(c, 1.0)
    for k in range(5):
        bunk(c, 280 + k * 360, 1.0)
    recruits_row(c, t, 420, n=5, gap=270, s=0.95, sweat=clamp((lt - 2.5) / 1.0))
    sx = lerp(1700, 300, ease_shot(t, 51.8, 55.4))
    draw_stick(c, Stick("sergeant", sx, GROUND + 120, 1.05, t, face=-1, uniform=True, walk=t * 5, hand_b=(-60, 120), mouth="frown", brow=-1))
    K.end(c)


def c_cheek(c, t):                     # 55,6–57,8  mặt đỏ ửng không phải vì xấu hổ
    q = ease_shot(t, 55.6, 57.8)
    K = Cam(1110, 400, lerp(2.6, 2.9, q), t=t)
    barracks_bg(c, K, t, inside=True)
    K.layer(c, 1.0)
    draw_stick(c, Stick("you", 1100, GROUND, 1.0, t, face=-1, uniform=True, cap="soldier", hand_f=(20, 170), hand_b=(-20, 170),
                        eyes="dot", look=(-1, 0), mouth="flat"))
    cheek(c, 1100, GROUND, 1.0, face=-1)
    K.end(c)


def c_recite(c, t):                    # 57,8–63,9  học thuộc điều luật: không bao giờ bị bắt làm tù binh
    q = ease_shot(t, 57.8, 63.9)
    K = Cam(lerp(600, 1300, q), 520, 1.15, t=t)
    barracks_bg(c, K, t, inside=True)
    K.layer(c, 0.8)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(800, 180, 420, 300)) or skia.Path(), "#F2EAD6", ow=8)
    for k in range(6):
        c.drawLine(1180 - k * 64, 220, 1180 - k * 64, 440, P(INK, stroke=10))
    K.end(c)
    K.layer(c, 1.0)
    bow = 0.5 + 0.5 * math.sin((t - 57.8) * 2.0)
    for i in range(7):
        who = "you" if i == 3 else f"recruit{i % 4}"
        draw_stick(c, Stick(who, 260 + i * 260, GROUND, 0.95, t + i * 0.2, face=1, uniform=True, cap="soldier", hand_f=(20, 170), hand_b=(-20, 170),
                            eyes="closed", mouth="o" if bow > 0.5 else "flat", lean=-4, head_tilt=-6))
    K.end(c)


def c_honor(c, t):                     # 63,9–65,7  thà chết, chứ không chịu nhục
    q = ease_shot(t, 63.9, 65.7)
    grad(c, skia.Rect.MakeWH(W, H), "#5A1A14", "#C04A2A")
    K = Cam(960, lerp(620, 600, q), lerp(1.0, 1.12, q), t=t)
    K.layer(c, 0.3)
    c.drawCircle(960, 560, 330, P("#E8604A"))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-2000, GROUND, W + 4000, 900), P("#1A0E0A"))
    sil = Stick("you", 960, GROUND, 1.25, t, face=1, uniform=True, cap="soldier", hand_f=(20, 170), hand_b=(-20, 170), eyes="closed")
    c.saveLayer(None, None)
    draw_stick(c, sil)
    c.drawRect(skia.Rect.MakeXYWH(-2000, -2000, W + 4000, H + 4000), skia.Paint(Color=skia.ColorSetRGB(20, 10, 8), BlendMode=skia.BlendMode.kSrcIn))
    c.restore()
    K.end(c)


def c_kenji(c, t):                     # 65,7–70,4  giường bên cạnh là Kenji · bị phạt vì ăn vụng
    lt = t - 65.7
    if lt < 2.3:
        q = ease_shot(t, 65.7, 68.0)
        K = Cam(lerp(1150, 1250, q), 560, lerp(1.6, 1.75, q), t=t)
        barracks_bg(c, K, t, inside=True, night=False)
        K.layer(c, 1.0)
        bunk(c, 760); bunk(c, 1300)
        draw_stick(c, Stick("you", 860, GROUND, 0.95, t, face=1, uniform=True, sit=0.0, hand_f=(40, 160), eyes="dot", look=(1, 0), mouth="smile"))
        chew = math.sin(lt * 14)
        draw_stick(c, Stick("kenji", 1320, GROUND, 1.0, t, face=-1, uniform=True, hand_f=(60, -120 + 10 * chew), eyes="happy", mouth="grin" if chew > 0 else "o"))
        hx, hy = head_xy(1320, GROUND, 1.0, "kenji")
        fo(c, oval(hx - 60, hy + 110, 26, 22), "#FFFFFF", ow=4)        # nắm cơm
        c.drawRect(skia.Rect.MakeXYWH(hx - 74, hy + 112, 28, 14), P("#2A3A2A"))
        text(c, "Kenji", 1320, GROUND - 600, "xbold", 46, "#F4C430", a=255 * clamp(lt / 0.4), align="center", stroke=6, stroke_color="#111111")
        K.end(c)
    else:
        q = ease_shot(t, 68.0, 70.4)
        K = Cam(lerp(980, 1040, q), 520, lerp(1.25, 1.35, q), t=t)
        barracks_bg(c, K, t, inside=True)
        K.layer(c, 1.0)
        sway = math.sin(lt * 2) * 3
        draw_stick(c, Stick("kenji", 1160, GROUND, 1.0, t, face=1, uniform=True, hand_f=(20, -260), hand_b=(-20, -260), eyes="squint", mouth="wobble",
                            sweat=1.0, lean=sway))
        fo(c, skia.Path().addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(1110, GROUND - 760, 110, 100), 16, 16)) or skia.Path(), "#8A8A8A", ow=6)
        draw_stick(c, Stick("sergeant", 820, GROUND, 1.05, t, face=1, uniform=True, hand_b=(-60, 120), hand_f=(80, 60), mouth="frown", brow=-1))
        K.end(c)


def c_jokes(c, t):                     # 70,4–75,7  tối nào Kenji cũng kể chuyện cười… tới khi đội trưởng đập cửa
    lt = t - 70.4
    door = t > 73.5
    q = ease_shot(t, 70.4, 73.4)
    if not door:
        K = Cam(lerp(900, 960, q), 600, lerp(1.2, 1.3, q), t=t)
    else:
        k = clamp((t - 73.5) / 0.15)
        K = Cam(960, 600, lerp(1.3, 1.1, k), shake=7 * math.exp(-(t - 73.5) * 5), t=t)
    barracks_bg(c, K, t, inside=True, night=True)
    K.layer(c, 1.0)
    if door:
        light = P("#F6E2A8", 200); c.drawRect(skia.Rect.MakeXYWH(1560, 300, 300, 560), light)
        draw_stick(c, Stick("sergeant", 1700, GROUND, 1.05, t, face=-1, uniform=True, hand_b=(-40, 120), hand_f=(60, 40), mouth="frown", brow=-1))
    for i, x in enumerate([300, 700, 1100]):
        laugh = 0.0 if door else (0.5 + 0.5 * math.sin(lt * 9 + i))
        bunk(c, x - 160, 1.0)
        lying(c, "you" if i == 0 else f"recruit{i}", x, GROUND - 200, 0.75, t, blanket="#4A5470", shake=laugh,
              eyes="closed", mouth="flat" if door else "grin")
    # Kenji ngồi trên giường, kể chuyện bằng tay
    g = math.sin(lt * 5)
    bunk(c, 1300, 1.0)
    if not door:
        draw_stick(c, Stick("kenji", 1430, GROUND - 160, 0.9, t, face=-1, sit=1.0,
                            hand_f=(90 + 40 * g, -140 + 30 * g), hand_b=(30, -100), eyes="happy", mouth="grin"))
    else:
        lying(c, "kenji", 1460, GROUND - 200, 0.75, t, blanket="#4A5470", eyes="closed", mouth="flat")
    K.end(c)
    if door and t - 73.5 < 0.06:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#FFFFFF", 120))


SHOTS = [(0.0, 4.0, c_sea), (4.0, 6.6, c_kitchen), (6.6, 10.2, c_bay), (10.2, 13.0, c_chief), (13.0, 13.4, c_zoom), (13.4, 14.5, c_paper),
         (14.5, 16.2, c_must), (16.2, 18.0, c_night), (18.0, 24.1, c_lane), (24.1, 26.3, c_cloth), (26.3, 29.3, c_shield),
         (29.3, 35.2, c_tie), (35.2, 40.2, c_station), (40.2, 42.7, c_noturn), (42.7, 47.2, c_yard), (47.2, 49.7, c_shout),
         (49.7, 55.6, c_inspect), (55.6, 57.8, c_cheek), (57.8, 63.9, c_recite), (63.9, 65.7, c_honor), (65.7, 70.4, c_kenji),
         (70.4, DUR, c_jokes)]
FADE = {16.2, 35.2, 42.7, 70.4}     # chuyển cảnh mềm (mờ qua đen ngắn)


def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas(); c.clear(skia.ColorBLACK)
    for a, b, fn in SHOTS:
        if a <= t < b:
            c.save(); fn(c, t); c.restore()
            for f in FADE:
                if abs(t - f) < 0.25:
                    c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 255 * (1 - abs(t - f) / 0.25)))
            break
    subtitle(c, t)
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def chunk(args):
    k, f0, f1 = args
    out = BUILD / f"c_{k:02d}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    s = skia.Surface(W, H)
    for i in range(f0, f1):
        p.stdin.write(frame(i / FPS, s).tobytes())
    p.stdin.close(); p.wait()
    return out


if __name__ == "__main__":
    BUILD.mkdir(parents=True, exist_ok=True)
    if sys.argv[1] == "preview":
        for ts in sys.argv[2:]:
            Image.fromarray(frame(float(ts))[..., :3]).save(BUILD / f"pv_{float(ts):05.2f}.png")
    elif sys.argv[1] == "sheet":
        ts = [a + (b - a) * 0.6 for a, b, _ in SHOTS]
        ims = [Image.fromarray(frame(x)[..., :3]).resize((480, 270)) for x in ts]
        sh = Image.new("RGB", (480 * 4, 270 * math.ceil(len(ims) / 4)))
        for i, im in enumerate(ims):
            sh.paste(im, ((i % 4) * 480, (i // 4) * 270))
        sh.save(BUILD / "sheet.png")
    else:
        nfr = int(DUR * FPS); step = math.ceil(nfr / 8)
        with Pool(4) as pool:
            chs = pool.map(chunk, [(k, f, min(nfr, f + step)) for k, f in enumerate(range(0, nfr, step))])
        (BUILD / "c.txt").write_text("".join(f"file '{x.name}'\n" for x in chs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(BUILD / "c.txt"), "-c", "copy",
                        str(BUILD / "P1_nosfx.mp4")], check=True)
        for x in chs:
            x.unlink()
        (BUILD / "c.txt").unlink()
        print("xong")
