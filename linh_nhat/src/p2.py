"""Phần 2 (voice_2, 70 s): tàu xuôi phương Nam → hòn đảo → nướng cua → tàu lương thực chìm → bát cơm vơi dần →
ăn rễ cây, thằn lằn → Kenji đục lỗ thắt lưng → sốt rét → giày mục → "Đảo Đói" → đêm Kenji sốt → sáng hôm sau.
  python3 src/p2.py sheet | preview <t…> | full
"""
import math, subprocess, sys, json
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import p1  # noqa  (dùng lại bối cảnh/đạo cụ phần 1)
from p1 import (skia, Image, text, Stick, draw_stick, P, fo, oval, clamp, lerp, ease_out, ease_in_out, back_out, INK, LOOKS,
                Cam, grad, noise1, W, H, FPS, GROUND, head_xy, lying, ease_shot, lerp_col, barracks_bg)  # noqa
import test_open2 as T2  # noqa

PART = ROOT / "p2"
BUILD = PART / "build"
ALIGN = json.load(open(ROOT / "audio" / "voice_2_align.json"))
DUR = 69.97
p1.ALIGN = ALIGN

SEA_TOP, SEA_BOT = "#6FC3D8", "#2E8AA8"


def thin_at(t):
    return clamp((t - 24.0) / 16.0)          # gầy dần từ lúc cơm vơi


# ---------------------------------------------------------------- đạo cụ
def ship(c, x, y, s, t, smoke=True, dark=False):
    c.save(); c.translate(x, y + 5 * math.sin(t * 1.2)); c.rotate(1.2 * math.sin(t * 0.9)); c.scale(s, s)
    hull = skia.Path(); hull.moveTo(-620, -60); hull.lineTo(560, -60); hull.lineTo(680, -140); hull.lineTo(640, 40)
    hull.quadTo(500, 120, 300, 120); hull.lineTo(-520, 120); hull.quadTo(-620, 80, -620, -60); hull.close()
    fo(c, hull, "#2A2E34" if dark else "#5A6470", ow=8)
    if not dark:
        c.drawLine(-600, 10, 640, 10, P("#C0392B", stroke=10))
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-200, -200, 360, 140)) or skia.Path(), "#7A848E", ow=6)
        for k in range(4):
            c.drawCircle(-150 + k * 80, -130, 16, P("#F6E7C0")); c.drawCircle(-150 + k * 80, -130, 16, P(INK, stroke=4))
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-20, -320, 70, 120)) or skia.Path(), "#3A3E44", ow=6)
        c.drawLine(-60, -60, 520, -60, P(INK, stroke=6))      # lan can boong
        for k in range(12):
            c.drawLine(-60 + k * 48, -60, -60 + k * 48, -110, P(INK, stroke=4))
        c.drawLine(-60, -110, 520, -110, P(INK, stroke=5))
    c.restore()
    if smoke and not dark:
        for k in range(6):
            q = (t * 0.25 + k / 6) % 1
            sp = P("#E8E4DC", 200 * (1 - q)); sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8))
            c.drawCircle(x + (15 - q * 260) * s, y + (-330 - q * 200) * s, (30 + q * 60) * s, sp)


def palm(c, x, y, s, t, seed=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    tr = skia.Path(); tr.moveTo(-14, 0); tr.quadTo(-40, -250, 10, -480); tr.lineTo(30, -476); tr.quadTo(-10, -250, 14, 0); tr.close()
    fo(c, tr, "#8A6A44", ow=5)
    for k in range(7):
        a = -math.pi + k * math.pi / 6 + 0.06 * math.sin(t * 1.5 + seed + k)
        lf = skia.Path(); lf.moveTo(20, -478)
        ex, ey = 20 + 220 * math.cos(a), -478 + 120 * math.sin(a) + 60
        lf.quadTo(20 + 120 * math.cos(a), -560 + 40 * math.sin(a), ex, ey)
        lf.quadTo(20 + 110 * math.cos(a), -500 + 30 * math.sin(a), 20, -470); lf.close()
        fo(c, lf, "#3E8A4A", ow=4)
    c.restore()


def island(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    m = skia.Path(); m.moveTo(-700, 40); m.quadTo(-500, -120, -250, -180); m.quadTo(0, -330, 260, -200); m.quadTo(520, -110, 700, 40); m.close()
    fo(c, m, "#2E6A3A", ow=7)
    for k in range(9):
        c.drawCircle(-520 + k * 130, -120 - 60 * math.sin(k * 0.8), 70, P("#3E7E46"))
    c.drawRect(skia.Rect.MakeXYWH(-700, 20, 1400, 30), P("#E8D8A8"))
    c.restore()


def jungle_bg(c, K, t, wash=0.0, sun=0.0):
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), lerp_col("#8FD0E8", "#F2F0D8", wash), lerp_col("#E8F6E8", "#FFF8E0", wash))
    K.end(c)
    K.layer(c, 0.4)
    for k in range(-3, 9):
        c.drawCircle(k * 300, 520 + (k % 3) * 40, 230, P(lerp_col("#4E8A52", "#9AAA7A", wash)))
    K.end(c)
    K.layer(c, 0.7)
    for k in range(-2, 7):
        palm(c, 100 + k * 380, GROUND + 20, 1.1, t, seed=k)
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P(lerp_col("#7A6A3A", "#A89A6A", wash)))
    c.drawLine(-3000, GROUND, W + 3000, GROUND, P(INK, stroke=6))
    K.end(c)


def beach_bg(c, K, t, dusk=0.0, night=0.0):
    K.layer(c, 0.0)
    top = lerp_col(lerp_col("#7FC8E8", "#E8885A", dusk), "#141C30", night)
    bot = lerp_col(lerp_col("#E8F6F2", "#F8D29A", dusk), "#24304A", night)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), top, bot)
    K.end(c)
    K.layer(c, 0.3)
    T2.wave_band(c, 600, t, lerp_col(lerp_col(SEA_TOP, "#C8805A", dusk), "#1E2A44", night), amp=5, x0=-3000, x1=W + 3000)
    K.end(c)
    K.layer(c, 0.7)
    T2.wave_band(c, 700, t, lerp_col(lerp_col(SEA_BOT, "#A0604A", dusk), "#18223A", night), amp=8, x0=-3000, x1=W + 3000)
    K.end(c)
    K.layer(c, 1.0)
    sand = skia.Path(); sand.moveTo(-3000, H + 600); sand.lineTo(-3000, 800); sand.quadTo(900, 760, W + 3000, 820); sand.lineTo(W + 3000, H + 600); sand.close()
    fo(c, sand, lerp_col(lerp_col("#E8D8A8", "#D8B888", dusk), "#3A3A44", night), ow=6)
    palm(c, 120, 880, 1.2, t, 1.0); palm(c, 1820, 900, 1.3, t, 2.0)
    K.end(c)


def campfire(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    g = P("#F39C12", 90); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60))
    c.drawCircle(0, -60, 200, g)
    for k in range(3):
        c.drawLine(-70, 6 - k * 6, 70, -6 + k * 6, P("#5A3E26", stroke=14))
    for k, colr in enumerate(["#C0392B", "#F39C12", "#F4D03F"]):
        fl = skia.Path(); h = 120 - k * 30; w = 54 - k * 14
        fl.moveTo(-w, 0); fl.quadTo(-w, -h * 0.6, 8 * math.sin(t * 12 + k), -h); fl.quadTo(w, -h * 0.6, w, 0); fl.close()
        c.drawPath(fl, P(colr))
    c.restore()


def crab(c, x, y, s, t, run=0.0, roasted=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    col = "#D2603A" if roasted else "#E87A4A"
    for sd in (-1, 1):
        for k in range(3):
            a = math.sin(t * 20 + k) * 10 * run
            c.drawLine(sd * 30, 0 + k * 10, sd * (64 + k * 6), 20 + k * 8 + a, P(INK, stroke=5))
        c.drawLine(sd * 34, -14, sd * 70, -50, P(INK, stroke=6))
        fo(c, oval(sd * 80, -62, 22, 16), col, ow=4)
    fo(c, oval(0, 0, 44, 30), col, ow=5)
    for sd in (-1, 1):
        c.drawLine(sd * 12, -26, sd * 16, -46, P(INK, stroke=4)); c.drawCircle(sd * 16, -48, 6, P(INK))
    c.restore()


def bowl(c, x, y, s, fill=1.0, mode="rice"):
    c.save(); c.translate(x, y); c.scale(s, s)
    b = skia.Path(); b.moveTo(-180, -40); b.quadTo(-170, 120, 0, 130); b.quadTo(170, 120, 180, -40); b.close()
    if mode == "rice" and fill > 0:
        mound = skia.Path(); mound.moveTo(-150 * fill, -40); mound.quadTo(0, -40 - 170 * fill, 150 * fill, -40); mound.close()
        fo(c, mound, "#FBF8F0", ow=5)
        for k in range(int(14 * fill)):
            c.drawOval(skia.Rect.MakeXYWH(-100 * fill + (k * 37) % int(200 * fill + 1), -60 - (k * 23) % int(90 * fill + 1), 14, 8), P("#E8E2D0"))
    fo(c, b, "#7A5A3A", ow=6)
    c.drawOval(skia.Rect.MakeXYWH(-180, -60, 360, 40), P("#5A3E26"))
    c.drawOval(skia.Rect.MakeXYWH(-180, -60, 360, 40), P(INK, stroke=5))
    if mode == "gruel":
        c.drawOval(skia.Rect.MakeXYWH(-150, -52, 300, 26), P("#E8E2D0", 120))
        c.drawOval(skia.Rect.MakeXYWH(-40, -46, 80, 14), P("#4A3220", 160))     # nhìn thấy đáy bát
        c.drawCircle(30, -40, 5, P("#FFFFFF"))
    c.restore()


def tent_in(c, K, t, morning=0.0):
    K.layer(c, 0.6)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, H + 4000), lerp_col("#1E2436", "#C8B888", morning), lerp_col("#121624", "#8A7A58", morning))
    tp = skia.Path(); tp.moveTo(-200, GROUND); tp.lineTo(960, 120); tp.lineTo(2120, GROUND); tp.close()
    c.drawPath(tp, P(lerp_col("#3A3A30", "#C2B07A", morning), 200))
    c.drawPath(tp, P(INK, stroke=8))
    if morning > 0:
        beam = skia.Path(); beam.moveTo(1500, 200); beam.lineTo(1700, 200); beam.lineTo(1200, GROUND + 100); beam.lineTo(800, GROUND + 100); beam.close()
        c.drawPath(beam, P("#FFF4C8", 90 * morning))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-2000, GROUND, W + 4000, 900), P(lerp_col("#2A2A30", "#7A6A48", morning)))
    c.drawLine(-2000, GROUND, W + 2000, GROUND, P(INK, stroke=6))
    if morning < 1:
        g = P("#F6C46A", 140 * (1 - morning)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 80))
        c.drawCircle(1300, 760, 220, g)
        fo(c, skia.Path().addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(1270, 720, 60, 90), 10, 10)) or skia.Path(), "#F8E6B8", ow=4, a=255 * (1 - morning))
    K.end(c)


# ---------------------------------------------------------------- cảnh
def c_ship(c, t):                      # 0–5,5  lên tàu xuôi phương Nam, biển xanh hơn, nắng gắt hơn
    q = ease_shot(t, 0, 5.5)
    K = Cam(lerp(860, 1060, q), lerp(560, 520, q), lerp(1.15, 1.05, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#5EB8E8", "#E8F8FF")
    K.end(c)
    K.layer(c, 0.2)
    glow = P("#FFF6C8", 230); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
    c.drawCircle(1500, 260, lerp(100, 150, clamp(t / 4)), glow)
    c.drawCircle(1500, 260, 80, P("#FFFBE8"))
    K.end(c)
    K.layer(c, 0.5)
    T2.wave_band(c, 640, t * 1.4, SEA_TOP, amp=6, x0=-3000, x1=W + 3000)
    K.end(c)
    K.layer(c, 1.0)
    ship(c, 900, 820, 0.95, t)
    for i, (who, x) in enumerate([("recruit1", 640), ("you", 820), ("kenji", 960), ("recruit2", 1120)]):
        draw_stick(c, Stick(who, x, 820 - 0.95 * 64, 0.52, t + i, face=1, uniform=True, cap="soldier",
                            hand_f=(70, 40), hand_b=(40, 50), lean=6, eyes="squint" if t > 3.2 else "dot", mouth="flat"))
    T2.wave_band(c, 900, t * 1.4, SEA_BOT, amp=14, x0=-3000, x1=W + 3000)
    K.end(c)
    K.layer(c, 1.5)
    T2.wave_band(c, 1000, t * 2, "#1E6A88", amp=24, x0=-3000, x1=W + 3000)
    K.end(c)


def c_island(c, t):                    # 5,5–9,6  cuối hành trình là một hòn đảo phủ kín rừng rậm
    q = ease_shot(t, 5.5, 9.6)
    K = Cam(960, lerp(560, 600, q), lerp(1.0, 1.6, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#5EB8E8", "#E8F8FF")
    K.end(c)
    K.layer(c, 0.6)
    T2.wave_band(c, 620, t, SEA_TOP, amp=5, x0=-3000, x1=W + 3000)
    island(c, 960, 640, lerp(0.35, 0.8, q), t)
    K.end(c)
    K.layer(c, 1.4)
    T2.wave_band(c, 820, t * 1.5, SEA_BOT, amp=14, x0=-3000, x1=W + 3000)
    K.end(c)
    # mũi tàu tiền cảnh
    c.save(); c.translate(0, 0)
    bow = skia.Path(); bow.moveTo(-100, H + 50); bow.lineTo(560, 900); bow.lineTo(700, H + 50); bow.close()
    fo(c, bow, "#4A525C", ow=8)
    c.restore()


def c_map(c, t):                       # 9,6–11,6  xa đến mức không biết nó nằm ở đâu trên bản đồ
    lt = t - 9.6
    grad(c, skia.Rect.MakeWH(W, H), "#5A4636", "#3A2C22")
    c.save(); c.translate(W / 2, H / 2 + 20); c.rotate(-3 + lt); c.scale(1 + 0.05 * lt, 1 + 0.05 * lt)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-700, -400, 1400, 800)) or skia.Path(), "#E8DCC0", ow=8)
    c.drawRect(skia.Rect.MakeXYWH(-690, -390, 1380, 780), P("#9CC8D8", 120))
    jp = skia.Path(); jp.moveTo(-520, -330); jp.quadTo(-440, -260, -470, -160); jp.quadTo(-520, -100, -560, -60); jp.lineTo(-540, -40)
    jp.quadTo(-460, -110, -420, -190); jp.quadTo(-400, -290, -490, -350); jp.close()
    fo(c, jp, "#C8B88A", ow=5)
    pth = skia.Path(); pth.moveTo(-500, -100)
    pth.cubicTo(-300, 100, 100, 50, 380 * clamp(lt / 1.2) + 0 * (1 - clamp(lt / 1.2)) - 100 * (1 - clamp(lt / 1.2)), 260 * clamp(lt / 1.2))
    pe = P("#C0392B", stroke=7); pe.setPathEffect(skia.DashPathEffect.Make([22, 14], 0)); c.drawPath(pth, pe)
    if lt > 1.1:
        c.drawCircle(380, 260, 10, P("#C0392B"))
        text(c, "?", 440, 230, "xbold", int(120 * back_out(clamp((lt - 1.1) / 0.3))), "#C0392B", align="center")
    c.restore()


def c_rice_ok(c, t):                   # 11,6–14,6  lúc đầu ổn, vẫn có cơm dù ít
    q = ease_shot(t, 11.6, 14.6)
    K = Cam(lerp(900, 1000, q), 540, 1.2, t=t)
    beach_bg(c, K, t)
    K.layer(c, 1.0)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(560, 700, 300, 120)) or skia.Path(), "#8A6A44", ow=6)
    draw_stick(c, Stick("recruit3", 620, 880, 0.85, t, face=1, uniform=True, cap="soldier", hand_f=(140, 60), eyes="dot", mouth="flat"))
    for i, who in enumerate(["you", "kenji", "recruit1", "recruit2"]):
        x = 1000 + i * 210
        draw_stick(c, Stick(who, x, 900, 0.85, t + i, face=-1, uniform=True, cap="soldier", hand_f=(100, 60), eyes="happy" if i < 2 else "dot",
                            mouth="smile"))
        bowl(c, x - 0.85 * (26 + 100) - 10, 900 - 0.85 * 330, 0.18, fill=0.7)
    K.end(c)


def c_crab(c, t):                      # 14,6–19,9  Kenji bắt cua · hai người nướng bên bờ biển
    lt = t - 14.6
    if lt < 2.2:
        q = ease_shot(t, 14.6, 16.8)
        K = Cam(lerp(800, 1100, q), 600, 1.35, t=t, shake=2)
        beach_bg(c, K, t)
        K.layer(c, 1.0)
        cx = lerp(700, 1400, ease_in_out(clamp(lt / 1.8)))
        crab(c, cx + 180, 920, 0.9, t, run=1.0)
        draw_stick(c, Stick("kenji", cx, 920, 0.9, t, face=1, uniform=True, cap="soldier", walk=lt * 11, run=True,
                            hand_f=(170, 80), hand_b=(140, 40), lean=18, eyes="wide", mouth="grin"))
        if lt > 1.8:
            text(c, "BẮT ĐƯỢC!", cx + 160, 600, "xbold", 70, "#F4C430", align="center", stroke=7, stroke_color="#111111")
        K.end(c)
    else:
        q = ease_shot(t, 16.8, 19.9)
        K = Cam(960, lerp(620, 600, q), lerp(1.45, 1.6, q), t=t)
        beach_bg(c, K, t, dusk=1.0)
        K.layer(c, 1.0)
        campfire(c, 960, 900, 0.9, t)
        draw_stick(c, Stick("you", 720, 900, 0.9, t, face=1, uniform=True, sit=1.0, hand_f=(150, 40), eyes="happy", mouth="grin"))
        draw_stick(c, Stick("kenji", 1210, 900, 0.9, t, face=-1, uniform=True, sit=1.0, hand_f=(160, -10), eyes="happy", mouth="grin"))
        c.drawLine(1060, 760, 940, 800, P(INK, stroke=6))
        crab(c, 960, 790, 0.4, t, roasted=True)
        K.end(c)


def c_sink(c, t):                      # 19,9–24,3  tàu lương thực không tới nữa · bị đánh chìm từng chiếc
    lt = t - 19.9
    q = ease_shot(t, 19.9, 24.3)
    K = Cam(960, lerp(540, 500, q), lerp(1.0, 1.12, q), t=t)
    beach_bg(c, K, t, dusk=0.3)
    K.layer(c, 0.35)
    for i, (sx, t0) in enumerate([(500, 0.6), (1100, 2.0), (1600, 3.2)]):
        a = lt - t0
        sink = clamp(a / 1.4) if a > 0 else 0.0
        c.save(); c.translate(sx, 610 + 80 * sink); c.rotate(14 * sink)
        ship(c, 0, 0, 0.22, t, smoke=False, dark=True)
        c.restore()
        if 0 < a < 1.2:
            g = clamp(a / 0.2) * (1 - clamp((a - 0.4) / 0.8))
            col = P("#FFD9A0", 230 * g); col.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12))
            c.drawCircle(sx, 580, 40 + 60 * a, col)
            c.drawRect(skia.Rect.MakeXYWH(sx - 14, 420 - 60 * a, 28, 200), P("#FFFFFF", 160 * g))
        if a > 0.2:
            for k in range(4):
                qq = clamp((a - 0.2 - k * 0.15) / 2.0)
                sp = P("#3A3A3A", 140 * (1 - qq)); sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
                c.drawCircle(sx + 20 * k, 560 - qq * 260, 24 + qq * 50, sp)
    K.end(c)
    K.layer(c, 1.0)
    for i, who in enumerate(["you", "kenji"]):
        draw_stick(c, Stick(who, 820 + i * 260, 960, 1.0, t + i, face=1, uniform=True, cap="soldier", hand_f=(20, 170), eyes="wide", mouth="o",
                            look=(0.3, -0.6), idle=0.4))
    K.end(c)


def c_bowls(c, t):                     # 24,3–30,4  phần cơm ít đi · một nắm · nửa nắm · cháo loãng thấy đáy bát
    grad(c, skia.Rect.MakeWH(W, H), "#5A4A3A", "#3A2E24")
    q = ease_shot(t, 24.3, 30.4)
    if t < 26.84:
        fill = lerp(1.0, 0.75, clamp((t - 24.3) / 2.4)); mode = "rice"; lab = ""
    elif t < 27.98:
        fill, mode, lab = 0.55, "rice", "một nắm"
    elif t < 28.7:
        fill, mode, lab = 0.3, "rice", "nửa nắm"
    else:
        fill, mode, lab = 0.0, "gruel", "cháo loãng"
    bowl(c, W / 2, 620, lerp(1.6, 1.8, q), fill=fill, mode=mode)
    if lab:
        text(c, lab, W / 2, 260, "xbold", 76, "#F2E8D0", align="center", stroke=7, stroke_color="#111111")


def c_forage(c, t):                    # 30,4–36,8  rễ cây, cỏ dại, thằn lằn, ốc sên
    lt = t - 30.4
    k = min(3, int(max(0.0, lt - 1.6) / 1.2)) if lt > 1.6 else -1
    q = ease_shot(t, 30.4, 36.8)
    K = Cam(lerp(800, 1100, q), 580, 1.4, t=t)
    th = thin_at(t)
    jungle_bg(c, K, t, wash=0.2)
    K.layer(c, 1.0)
    draw_stick(c, Stick("you", 900, GROUND, 0.95, t, face=1, uniform=True, cap="soldier", crouch=0.8, thin=th,
                        hand_f=(150, 160 + 20 * math.sin(lt * 9)), hand_b=(110, 170), eyes="dot", look=(1, 1), mouth="flat"))
    ix, iy = 1110, GROUND - 40
    labels = ["rễ cây", "cỏ dại", "thằn lằn", "ốc sên"]
    if k >= 0:
        if k == 0:
            c.drawLine(ix, iy, ix + 30, iy - 80, P("#8A6A44", stroke=10)); c.drawLine(ix + 10, iy, ix - 20, iy + 40, P("#8A6A44", stroke=6))
        elif k == 1:
            for j in range(5):
                c.drawLine(ix + j * 10, iy, ix - 20 + j * 18, iy - 70 - (j % 2) * 20, P("#5A9A4A", stroke=6))
        elif k == 2:
            lz = skia.Path(); lz.moveTo(ix - 60, iy - 10); lz.quadTo(ix, iy - 30, ix + 60, iy - 10); lz.quadTo(ix, iy, ix - 60, iy - 10)
            fo(c, lz, "#7A9A4A", ow=4); c.drawCircle(ix + 50, iy - 16, 3, P(INK))
            c.drawLine(ix - 60, iy - 10, ix - 120, iy - 30 + 8 * math.sin(t * 10), P(INK, stroke=5))
        else:
            fo(c, oval(ix, iy - 20, 26, 22), "#C8A06A", ow=4)
            c.drawArc(skia.Rect.MakeXYWH(ix - 14, iy - 34, 28, 28), 0, 300, False, P(INK, stroke=4))
            c.drawLine(ix + 20, iy - 4, ix + 50, iy - 4, P("#A88A5A", stroke=10))
        text(c, labels[k], ix, iy - 160, "xbold", 54, "#FFFFFF", align="center", stroke=6, stroke_color="#111111")
    K.end(c)


def c_belt(c, t):                      # 36,8–40,9  Kenji gầy tới mức đục thêm ba lỗ thắt lưng
    lt = t - 36.8
    if lt < 1.8:
        q = ease_shot(t, 36.8, 38.6)
        K = Cam(1000, lerp(520, 500, q), lerp(1.4, 1.55, q), t=t)
        jungle_bg(c, K, t, wash=0.3)
        K.layer(c, 1.0)
        draw_stick(c, Stick("kenji", 1000, GROUND, 1.0, t, face=1, uniform=True, cap="soldier", thin=1.0, hand_f=(60, 160), hand_b=(30, 170),
                            eyes="sad", mouth="frown"))
        K.end(c)
    else:
        grad(c, skia.Rect.MakeWH(W, H), "#8C7E4E", "#6E623C")
        c.save(); c.translate(W / 2, H / 2)
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-900, -70, 1800, 140)) or skia.Path(), "#4A3A26", ow=8)
        holes = 2 + min(3, int((lt - 1.8) / 0.6))
        for k in range(holes):
            x = 300 + k * 110
            c.drawCircle(x, 0, 18, P("#1A120A"))
            if k >= 2 and lt - 1.8 - (k - 2) * 0.6 < 0.25:
                text(c, "CỘP", x, -110, "xbold", 60, "#F4C430", align="center", stroke=6, stroke_color="#111111")
        c.restore()


def c_fever(c, t):                     # 40,9–45,3  sốt rét: lạnh run giữa trời nóng 40 độ
    q = ease_shot(t, 40.9, 45.3)
    K = Cam(960, lerp(560, 520, q), lerp(1.3, 1.5, q), t=t)
    jungle_bg(c, K, t, wash=0.75)
    K.layer(c, 1.0)
    draw_stick(c, Stick("you", 960, GROUND, 1.0, t, face=1, uniform=True, cap="soldier", sit=1.0, shiver=1.0, thin=thin_at(t),
                        hand_f=(60, 60), hand_b=(90, 70), eyes="squint", mouth="wobble", sweat=1.0))
    K.end(c)
    for k in range(6):                 # hơi nóng bốc lên
        y = 400 + k * 90
        pth = skia.Path(); pth.moveTo(0, y)
        for x in range(0, W + 40, 40):
            pth.lineTo(x, y + 6 * math.sin(x * 0.02 + t * 6 + k))
        c.drawPath(pth, P("#FFFFFF", 40, stroke=4))
    text(c, "40°C", 1700, 160, "xbold", 80, "#C0392B", align="center", stroke=7, stroke_color="#FFFFFF")


def c_feet(c, t):                      # 45,3–49,7  giày mục rữa trong bùn, quấn chân bằng vải rách
    lt = t - 45.3
    q = ease_shot(t, 45.3, 49.7)
    grad(c, skia.Rect.MakeWH(W, H), "#5A4A30", "#3A2E1E")
    c.drawRect(skia.Rect.MakeXYWH(0, 700, W, 400), P("#4A3A22"))
    for k in range(10):
        c.drawOval(skia.Rect.MakeXYWH((k * 230 + 40) % W, 760 + (k % 3) * 70, 160, 30), P("#3A2C18"))
    x = lerp(400, 1500, ease_in_out(clamp((lt - 2.2) / 2.2)))
    for sd, ph in ((-1, 0.0), (1, math.pi)):
        st = math.sin(lt * 6 + ph) if lt > 2.2 else 0.0
        fx = x + sd * 120 + st * 60
        fy = 760 - max(0.0, math.cos(lt * 6 + ph)) * 50 * (lt > 2.2)
        c.drawLine(fx, fy - 400, fx, fy - 60, P(INK, stroke=40))
        if lt < 2.2 and sd < 0:
            boot = skia.Path(); boot.moveTo(fx - 60, fy - 80); boot.lineTo(fx + 40, fy - 80); boot.lineTo(fx + 120, fy); boot.lineTo(fx - 70, fy); boot.close()
            fo(c, boot, "#3A2A1A", ow=6)
            for j in range(4):
                c.drawLine(fx - 40 + j * 40, fy - 20, fx - 20 + j * 40, fy, P("#1A120A", stroke=8))
        else:
            wrap = skia.Path(); wrap.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(fx - 60, fy - 120, 160, 120), 40, 40))
            fo(c, wrap, "#C8BCA0", ow=6)
            for j in range(4):
                c.drawLine(fx - 50, fy - 110 + j * 26, fx + 90, fy - 90 + j * 26, P("#8A7A60", stroke=5))


def c_title(c, t):                     # 49,7–53,7  người ta gọi hòn đảo ấy là "Đảo Đói"
    lt = t - 49.7
    q = ease_shot(t, 49.7, 53.7)
    K = Cam(960, 560, lerp(1.25, 1.0, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#A8B8B8", "#D8D8C8")
    K.end(c)
    K.layer(c, 1.0)
    T2.wave_band(c, 700, t, "#6A8A98", amp=6, x0=-3000, x1=W + 3000)
    island(c, 960, 720, 1.2, t)
    K.end(c)
    c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 70))
    if lt > 2.2:
        p = back_out(clamp((lt - 2.2) / 0.35))
        c.save(); c.translate(W / 2, 420); c.rotate(-4); c.scale(p, p)
        text(c, "ĐẢO ĐÓI", 0, 0, "xbold", 180, "#E8D8B0", align="center", stroke=14, stroke_color="#2A1A10")
        c.restore()


def c_fallen(c, t):                    # 53,7–57,7  rất nhiều người ngã xuống vì đói và bệnh
    q = ease_shot(t, 53.7, 57.7)
    K = Cam(lerp(700, 1200, q), 540, 1.1, t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#C8885A", "#E8C89A")
    K.end(c)
    K.layer(c, 0.5)
    for k in range(-3, 8):
        palm(c, k * 340, GROUND + 40, 1.0, t, k)
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P("#6A5A3A"))
    for k in range(-4, 14):          # những cọc gỗ đội mũ lính — nhẹ nhàng, không hình ảnh thi thể
        x = 100 + k * 150
        y = GROUND + 40 + (k % 2) * 40
        c.drawLine(x, y, x, y - 130, P(INK, stroke=12)); c.drawLine(x, y, x, y - 130, P("#8A6A44", stroke=6))
        cp = skia.Path(); cp.moveTo(x - 34, y - 130); cp.quadTo(x - 30, y - 176, x + 4, y - 174); cp.quadTo(x + 34, y - 170, x + 34, y - 130); cp.close()
        fo(c, cp, "#8C7E4E", ow=4)
    K.end(c)


def c_night(c, t):                     # 57,7–60,0  có một đêm Kenji lên cơn sốt nặng
    q = ease_shot(t, 57.7, 60.0)
    K = Cam(lerp(900, 860, q), lerp(640, 660, q), lerp(1.3, 1.5, q), t=t)
    tent_in(c, K, t)
    K.layer(c, 1.0)
    lying(c, "kenji", 1080, GROUND - 40, 0.85, t, blanket="#5A5A4A", shake=1.0, eyes="closed", mouth="wobble", sweat=1.0, thin=1.0)
    K.end(c)


def c_feed(c, t):                      # 60,0–62,95  bạn ngồi cạnh, đút cho Kenji phần cháo của mình
    lt = t - 60.0
    q = ease_shot(t, 60.0, 62.95)
    K = Cam(lerp(820, 860, q), 640, lerp(1.5, 1.7, q), t=t)
    tent_in(c, K, t)
    K.layer(c, 1.0)
    lying(c, "kenji", 1080, GROUND - 40, 0.85, t, blanket="#5A5A4A", shake=0.4, eyes="closed", mouth="flat", thin=1.0)
    sp = 0.5 + 0.5 * math.sin(lt * 2.2)
    draw_stick(c, Stick("you", 560, GROUND, 0.95, t, face=1, sit=1.0, uniform=True, thin=1.0, hand_f=(lerp(80, 150, sp), lerp(80, 40, sp)),
                        hand_b=(70, 100), eyes="sad", mouth="flat", lean=8))
    bowl(c, 620, GROUND - 200, 0.18, mode="gruel")
    K.end(c)


def c_smile(c, t):                     # 62,95–67,4  Kenji mở mắt, cười yếu ớt: "mày nấu dở hơn mẹ tao nhiều"
    lt = t - 62.95
    q = ease_shot(t, 62.95, 67.4)
    K = Cam(lerp(760, 720, q), lerp(730, 740, q), lerp(2.4, 2.8, q), t=t)
    tent_in(c, K, t)
    K.layer(c, 1.0)
    awake = lt > 0.6
    lying(c, "kenji", 1080, GROUND - 40, 0.85, t, blanket="#5A5A4A", eyes="happy" if awake else "closed",
          mouth="smile" if lt > 1.4 else "flat", thin=1.0)
    K.end(c)
    if lt > 3.2:   # cắt nhẹ sang mặt bạn: cười, rơm rớm
        a = clamp((lt - 3.2) / 0.3)
        K2 = Cam(560, 440, 2.6, t=t)
        c.saveLayerAlpha(None, int(255 * a))
        tent_in(c, K2, t)
        K2.layer(c, 1.0)
        draw_stick(c, Stick("you", 560, GROUND, 0.95, t, face=1, sit=1.0, uniform=True, thin=1.0, hand_f=(80, 80), eyes="happy",
                            mouth="smile", tears=1.0))
        K2.end(c)
        c.restore()


def c_morning(c, t):                   # 67,4–70  sáng hôm sau, cơn sốt lui · Kenji vẫn còn đó
    q = ease_shot(t, 67.4, 69.97)
    K = Cam(lerp(860, 900, q), 620, lerp(1.25, 1.15, q), t=t)
    tent_in(c, K, t, morning=1.0)
    K.layer(c, 1.0)
    draw_stick(c, Stick("kenji", 1120, GROUND - 20, 0.9, t, face=-1, sit=1.0, uniform=True, thin=1.0, hand_f=(60, 120), eyes="dot",
                        look=(-1, 0.2), mouth="smile"))
    draw_stick(c, Stick("you", 640, GROUND, 0.9, t, face=1, sit=1.0, uniform=True, thin=1.0, hand_f=(60, 150), eyes="closed",
                        mouth="flat", head_tilt=18))
    K.end(c)


SHOTS = [(0.0, 5.5, c_ship), (5.5, 9.6, c_island), (9.6, 11.6, c_map), (11.6, 14.6, c_rice_ok), (14.6, 19.9, c_crab),
         (19.9, 24.3, c_sink), (24.3, 30.4, c_bowls), (30.4, 36.8, c_forage), (36.8, 40.9, c_belt), (40.9, 45.3, c_fever),
         (45.3, 49.7, c_feet), (49.7, 53.7, c_title), (53.7, 57.7, c_fallen), (57.7, 60.0, c_night), (60.0, 62.95, c_feed),
         (62.95, 67.4, c_smile), (67.4, DUR, c_morning)]
FADE = {11.6, 24.3, 49.7, 57.7, 67.4}


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
    p1.subtitle(c, t)
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def chunk(args):
    k, f0, f1 = args
    out = BUILD / f"c_{k:02d}.mp4"
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    s = skia.Surface(W, H)
    for i in range(f0, f1):
        pr.stdin.write(frame(i / FPS, s).tobytes())
    pr.stdin.close(); pr.wait()
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
                        str(BUILD / "P2_nosfx.mp4")], check=True)
        for x in chs:
            x.unlink()
        (BUILD / "c.txt").unlink()
        print("xong")
