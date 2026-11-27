"""Phần 3 (voice_3, 63,7 s): đêm rút quân → ngoái nhìn đảo → dải vải bạc màu → Philippines, lùi vào núi → thành phố cháy →
tháng Tám 1945, thông báo, radio → chiến tranh kết thúc → phản ứng → "thà chết…" → buông súng → Kenji: "thế thì đi thôi".
  python3 src/p3.py sheet | preview <t…> | full
"""
import math, subprocess, sys, json
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import p1, p2  # noqa
from p1 import (skia, Image, text, Stick, draw_stick, P, fo, oval, clamp, lerp, ease_out, ease_in_out, back_out, INK, LOOKS,
                Cam, grad, noise1, W, H, FPS, GROUND, head_xy, lying, ease_shot, lerp_col)  # noqa
from p2 import palm, island, ship, jungle_bg, beach_bg  # noqa
import test_open2 as T2  # noqa

PART = ROOT / "p3"
BUILD = PART / "build"
ALIGN = json.load(open(ROOT / "audio" / "voice_3_align.json"))
DUR = 63.69
p1.ALIGN = ALIGN
TH = 1.0     # cả đơn vị gầy rộc


def soldier(who, x, y, s, t, **kw):
    kw.setdefault("uniform", True); kw.setdefault("cap", "soldier"); kw.setdefault("thin", TH)
    return draw_stick(c_ref[0], Stick(who, x, y, s, t, **kw))


c_ref = [None]


def S(c, who, x, y, s, t, **kw):
    kw.setdefault("uniform", True); kw.setdefault("cap", "soldier"); kw.setdefault("thin", TH)
    draw_stick(c, Stick(who, x, y, s, t, **kw))


def mountains_bg(c, K, t, mist=0.6, glow=0.0, night=0.0):
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), lerp_col("#8AA8A0", "#141C2C", night), lerp_col("#D8E2D8", "#2A2438", night))
    K.end(c)
    if glow > 0:
        K.layer(c, 0.1)
        g = P("#E8743A", 160 * glow); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 120))
        c.drawOval(skia.Rect.MakeXYWH(-400, 500, W + 800, 360), g)
        K.end(c)
    for depth, (yy, col) in enumerate([(560, "#6A8A7A"), (660, "#4E7262"), (760, "#36584A")]):
        K.layer(c, 0.3 + depth * 0.25)
        p = skia.Path(); p.moveTo(-3000, H + 600)
        for i in range(0, 60):
            x = -3000 + i * 160
            p.lineTo(x, yy - 160 * abs(math.sin(i * 0.7 + depth * 1.3)) - 40 * math.sin(i * 2.1))
        p.lineTo(W + 3000, H + 600); p.close()
        c.drawPath(p, P(lerp_col(col, "#1A2030", night)))
        if mist > 0:
            m = P("#FFFFFF", 60 * mist); m.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
            c.drawRect(skia.Rect.MakeXYWH(-3000, yy - 20, W + 6000, 80), m)
        K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P(lerp_col("#4A5A3A", "#1A1E24", night)))
    c.drawLine(-3000, GROUND, W + 3000, GROUND, P(INK, stroke=6))
    K.end(c)


def radio(c, x, y, s, t, on=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Path(); body.moveTo(-160, 0); body.lineTo(-160, -180); body.quadTo(-160, -300, 0, -300); body.quadTo(160, -300, 160, -180)
    body.lineTo(160, 0); body.close()
    fo(c, body, "#8A5A3A", ow=7)
    fo(c, skia.Path().addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-120, -240, 240, 120), 40, 40)) or skia.Path(), "#D8C8A0", ow=5)
    for k in range(6):
        c.drawLine(-100 + k * 40, -230, -100 + k * 40, -130, P("#8A7A5A", stroke=4))
    for dx in (-60, 60):
        c.drawCircle(dx, -60, 24, P("#3A2A1A")); c.drawCircle(dx, -60, 24, P(INK, stroke=4))
    c.restore()
    if on:
        for k in range(3):
            q = (t * 0.8 + k / 3) % 1
            c.drawArc(skia.Rect.MakeXYWH(x + 120 * s, y - 260 * s - 60 * q * s, 160 * q * s + 30, 160 * q * s + 30), -60, 120, False,
                      P("#FFFFFF", 200 * (1 - q), stroke=6))


# ---------------------------------------------------------------- cảnh
def c_line(c, t):                      # 0–4,3  đêm không trăng, lặng lẽ xếp hàng ra bờ biển
    q = ease_shot(t, 0, 4.3)
    K = Cam(lerp(700, 1050, q), 600, 1.15, t=t)
    beach_bg(c, K, t, night=1.0)
    K.layer(c, 1.0)
    for i in range(7):
        who = ["recruit0", "recruit1", "you", "kenji", "recruit2", "recruit3", "recruit1"][i]
        x = 300 + i * 220 + t * 40
        S(c, who, x, 910, 0.85, t + i * 0.37, face=1, walk=(t * 4.2 + i * 0.9), pack=True, eyes="dot", mouth="flat", idle=0.6)
    K.end(c)
    c.drawRect(skia.Rect.MakeWH(W, H), P("#0A1020", 70))


def c_hush(c, t):                      # 4,3–5,84  không ai được nói một lời
    K = Cam(960, 430, 2.3, t=t)
    beach_bg(c, K, t, night=1.0)
    K.layer(c, 1.0)
    S(c, "sergeant", 860, GROUND + 40, 1.0, t, face=1, hand_f=(62, -42), eyes="dot", mouth="flat", brow=-1)
    S(c, "you", 1160, GROUND + 40, 1.0, t, face=-1, eyes="wide", mouth="flat", look=(-1, 0), idle=0.4)
    K.end(c)
    c.drawRect(skia.Rect.MakeWH(W, H), P("#0A1020", 60))


def c_destroyer(c, t):                 # 5,84–11,12  tàu khu trục áp sát bờ trong bóng tối… rời đi trước khi trời sáng
    lt = t - 5.84
    q = ease_shot(t, 5.84, 11.12)
    dawn = clamp((lt - 3.5) / 1.8) * 0.35
    K = Cam(lerp(1000, 1150, q), 560, lerp(1.0, 1.08, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), lerp_col("#0E1424", "#3A3A5A", dawn), lerp_col("#1A2238", "#C8806A", dawn))
    K.end(c)
    K.layer(c, 0.6)
    T2.wave_band(c, 640, t, lerp_col("#141C30", "#3A3A50", dawn), amp=5, x0=-3000, x1=W + 3000)
    sx = 1250 + max(0.0, lt - 3.0) * 160
    ship(c, sx, 680, 0.9, t, smoke=False, dark=True)
    K.end(c)
    K.layer(c, 1.0)
    T2.wave_band(c, 760, t * 1.3, lerp_col("#101828", "#2A2A40", dawn), amp=10, x0=-3000, x1=W + 3000)
    for k in range(2):     # xuồng nhỏ chở người ra tàu
        bx = lerp(500 + k * 200, 1150, clamp((lt - k * 0.8) / 2.6))
        c.save(); c.translate(bx, 760); c.scale(0.35, 0.35)
        hull = skia.Path(); hull.moveTo(-300, -40); hull.lineTo(300, -40); hull.quadTo(260, 60, 0, 60); hull.quadTo(-260, 60, -300, -40); hull.close()
        fo(c, hull, "#1E1E24", ow=8)
        for j in range(4):
            draw_stick(c, Stick(["you", "kenji", "recruit1", "recruit2"][j], -180 + j * 120, -40, 0.7, t + j, face=1, uniform=True, cap="soldier",
                                thin=TH, sit=1.0, eyes="dot", idle=0.3))
        c.restore()
    K.end(c)
    c.drawRect(skia.Rect.MakeWH(W, H), P("#0A1020", int(90 * (1 - dawn * 2))))


def c_lookback(c, t):                  # 11,12–15,78  ngoái nhìn hòn đảo · quá nhiều người không lên được
    lt = t - 11.12
    if lt < 2.4:
        q = ease_shot(t, 11.12, 13.52)
        K = Cam(lerp(1120, 1080, q), lerp(430, 420, q), lerp(2.0, 2.3, q), t=t)
        K.layer(c, 0.0)
        grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#3A3A5A", "#C8806A")
        K.end(c)
        K.layer(c, 0.4)
        T2.wave_band(c, 640, t, "#3A3A50", amp=5, x0=-3000, x1=W + 3000)
        c.save(); c.translate(500, 650); c.scale(0.55, 0.55)
        m = skia.Path(); m.moveTo(-700, 40); m.quadTo(-300, -220, 0, -300); m.quadTo(300, -220, 700, 40); m.close()
        c.drawPath(m, P("#14141E"))
        c.restore()
        K.end(c)
        K.layer(c, 1.0)
        c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND - 40, W + 6000, 900), P("#3A3E46"))
        c.drawLine(-3000, GROUND - 80, W + 3000, GROUND - 80, P(INK, stroke=8))
        S(c, "you", 1150, GROUND - 40, 1.0, t, face=-1, hand_f=(80, 20), eyes="dot", look=(-1, 0), mouth="flat", head_tilt=-4)
        K.end(c)
    else:
        q = ease_shot(t, 13.52, 15.78)
        K = Cam(lerp(960, 900, q), 640, lerp(1.2, 1.35, q), t=t)
        beach_bg(c, K, t, dusk=0.4, night=0.4)
        K.layer(c, 1.0)
        for k in range(9):     # những chiếc mũ bỏ lại trên cát, sóng liếm nhẹ — không hình ảnh thi thể
            x = 300 + k * 170 + 30 * math.sin(k * 2.1)
            y = 900 + (k % 3) * 30
            cp = skia.Path(); cp.moveTo(x - 40, y); cp.quadTo(x - 36, y - 50, x + 4, y - 48); cp.quadTo(x + 40, y - 44, x + 40, y); cp.close()
            fo(c, cp, "#8C7E4E", ow=4)
        T2.wave_band(c, 960 + 10 * math.sin(t), t, "#2E6A88", amp=8, x0=-3000, x1=W + 3000, a=120)
        K.end(c)


def c_belt(c, t):                      # 15,78–21,66  đặt tay lên bụng · dải vải bạc màu, sờn rách, vẫn còn đó
    lt = t - 15.78
    if lt < 1.1:
        K = Cam(1100, 560, 1.9, t=t)
        K.layer(c, 0.0)
        grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#5A5A7A", "#D8A07A")
        K.end(c)
        K.layer(c, 1.0)
        c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND - 40, W + 6000, 900), P("#3A3E46"))
        S(c, "you", 1150, GROUND - 40, 1.0, t, face=-1, hand_f=(lerp(80, 30, ease_out(lt / 0.8)), lerp(20, 150, ease_out(lt / 0.8))),
          eyes="dot", look=(0, 1), mouth="flat", head_tilt=8)
        K.end(c)
        return
    q = ease_shot(t, 16.89, 21.66)
    grad(c, skia.Rect.MakeWH(W, H), "#7A6E48", "#5A5034")
    c.save(); c.translate(W / 2, H / 2); c.rotate(-2 + 1.5 * q); c.scale(lerp(1.0, 1.12, q), lerp(1.0, 1.12, q))
    band = skia.Path(); band.moveTo(-820, -90)
    for k in range(17):
        band.lineTo(-820 + k * 102, -90 + (8 if k % 2 else -6))
    band.lineTo(820, 90)
    for k in range(17):
        band.lineTo(820 - k * 102, 90 + (10 if k % 3 == 0 else -4))
    band.close()
    fo(c, band, "#D8CDB2", ow=8)
    for i in range(160):
        cx = -780 + (i % 40) * 40 + (i // 40 % 2) * 18
        cy = -60 + (i // 40) * 40
        if (i * 7) % 11 == 0:
            continue                        # vài mũi chỉ đã sút mất
        c.drawLine(cx - 7, cy - 4, cx + 7, cy + 4, P("#9A5A4A", stroke=5))
    for k in range(5):                      # chỗ sờn rách
        hx = -600 + k * 300
        c.drawOval(skia.Rect.MakeXYWH(hx - 30, -20, 60, 44), P("#5A5034"))
        for j in range(6):
            c.drawLine(hx - 30 + j * 12, -20, hx - 34 + j * 12, -44, P("#D8CDB2", stroke=3))
    # bàn tay đặt lên
    hx = lerp(500, 380, q)
    c.drawLine(hx + 400, 420, hx + 60, 40, P(INK, stroke=26))
    c.drawCircle(hx + 40, 20, 60, P(INK))
    c.restore()


def c_islands(c, t):                   # 21,66–26,39  từ đảo này sang đảo khác, rồi vào núi ở Philippines
    lt = t - 21.66
    grad(c, skia.Rect.MakeWH(W, H), "#5A4636", "#3A2C22")
    c.save(); c.translate(W / 2, H / 2 + 10); c.rotate(-2)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-760, -420, 1520, 840)) or skia.Path(), "#E8DCC0", ow=8)
    c.drawRect(skia.Rect.MakeXYWH(-750, -410, 1500, 820), P("#9CC8D8", 120))
    pts = [(360, 260), (120, 210), (-80, 120), (-200, 0), (-260, -140)]
    for i, (x, y) in enumerate(pts):
        r = 30 if i < 4 else 60
        fo(c, oval(x, y, r, r * 0.7), "#C8B88A", ow=4)
    k = clamp(lt / 3.6) * (len(pts) - 1)
    pth = skia.Path(); pth.moveTo(*pts[0])
    for i in range(1, len(pts)):
        f = clamp(k - (i - 1))
        if f <= 0:
            break
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        pth.quadTo((x0 + x1) / 2, (y0 + y1) / 2 - 60, lerp(x0, x1, f), lerp(y0, y1, f))
    pe = P("#C0392B", stroke=7); pe.setPathEffect(skia.DashPathEffect.Make([22, 14], 0)); c.drawPath(pth, pe)
    if lt > 3.6:
        p = back_out(clamp((lt - 3.6) / 0.4))
        c.save(); c.translate(-260, -240); c.scale(p, p)
        text(c, "Philippines", 0, 0, "xbold", 70, "#7A3A1A", align="center")
        c.restore()
        for j in range(3):
            tri = skia.Path(); tri.moveTo(-320 + j * 50, -120); tri.lineTo(-295 + j * 50, -170); tri.lineTo(-270 + j * 50, -120); tri.close()
            fo(c, tri, "#5A6A4A", ow=3)
    c.restore()


def c_retreat(c, t):                   # 26,39–28,47  quân đội càng lúc càng lùi sâu vào rừng
    q = ease_shot(t, 26.39, 28.47)
    K = Cam(lerp(900, 1100, q), 520, 1.1, t=t)
    mountains_bg(c, K, t, mist=0.9)
    K.layer(c, 1.0)
    for i in range(6):
        x = 400 + i * 250 + (t - 26.39) * 70
        S(c, ["recruit0", "you", "kenji", "recruit1", "recruit2", "recruit3"][i], x, GROUND - i * 20, 0.8 - i * 0.03, t + i,
          face=1, walk=t * 4 + i, pack=True, lean=8, eyes="dot", mouth="flat")
    K.end(c)
    m = P("#FFFFFF", 70); m.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60))
    c.drawRect(skia.Rect.MakeXYWH(-200, 650, W + 400, 200), m)


def c_letters(c, t):                   # 28,47–30,77  tin tức từ quê nhà thưa dần, rồi im hẳn
    lt = t - 28.47
    q = ease_shot(t, 28.47, 30.77)
    K = Cam(lerp(980, 960, q), lerp(520, 500, q), lerp(1.6, 1.75, q), t=t)
    mountains_bg(c, K, t, mist=0.5)
    K.layer(c, 1.0)
    palm(c, 760, GROUND + 10, 1.2, t)
    S(c, "you", 900, GROUND, 0.95, t, face=1, sit=1.0, hand_f=(150, -10), hand_b=(120, 10), eyes="dot", look=(1, 0.8), mouth="flat")
    c.save(); c.translate(900 + 0.95 * 150, GROUND - 0.95 * 230); c.rotate(-10)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-10, -60, 110, 80)) or skia.Path(), "#E8DCC0", ow=4)
    for k in range(3):
        c.drawLine(4, -46 + k * 18, 86, -46 + k * 18, P("#8A7A5A", stroke=3))
    c.restore()
    K.end(c)
    for k in range(5):                     # thư thưa dần: ít phong bì dần
        a = clamp(1 - lt / 2.0 - k * 0.12)
        if a <= 0:
            continue
        x, y = 1500 + k * 60, 200 + k * 30
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(x, y, 120, 80)) or skia.Path(), "#F2EAD6", ow=4, a=255 * a)
        c.drawLine(x, y, x + 60, y + 44, P(INK, 255 * a, stroke=3)); c.drawLine(x + 120, y, x + 60, y + 44, P(INK, 255 * a, stroke=3))


def c_glow(c, t):                      # 30,77–34,1  nghe thì thầm thành phố bên Nhật đang cháy
    q = ease_shot(t, 30.77, 34.1)
    K = Cam(lerp(1000, 960, q), lerp(540, 520, q), lerp(1.3, 1.2, q), t=t)
    mountains_bg(c, K, t, mist=0.2, glow=0.8 + 0.2 * math.sin(t * 2), night=1.0)
    K.layer(c, 1.0)
    S(c, "recruit1", 820, GROUND, 0.95, t, face=1, sit=1.0, hand_f=(80, -40), eyes="dot", look=(1, 0), mouth="o", lean=10)
    S(c, "you", 1080, GROUND, 0.95, t, face=-1, sit=1.0, hand_f=(60, 150), eyes="wide", look=(-0.6, -0.4), mouth="flat")
    K.end(c)


def c_assembly(c, t):                  # 34,1–40,39  tháng Tám 1945: tập hợp đơn vị · đọc thông báo, giọng run run
    lt = t - 34.1
    if lt < 3.6:
        q = ease_shot(t, 34.1, 37.7)
        K = Cam(lerp(800, 1000, q), 540, 1.05, t=t)
        mountains_bg(c, K, t, mist=0.4)
        K.layer(c, 1.0)
        for i in range(6):
            S(c, "you" if i == 2 else ("kenji" if i == 3 else f"recruit{i % 4}"), 520 + i * 200, GROUND, 0.85, t + i, face=1,
              hand_f=(20, 170), hand_b=(-20, 170), eyes="dot", mouth="flat", idle=0.3)
        S(c, "sergeant", 1700, GROUND + 60, 0.95, t, face=-1, walk=None if lt > 1.4 else t * 5, hand_b=(-40, 140), mouth="flat")
        K.end(c)
        if lt < 1.4:
            p = clamp(lt / 0.4) * clamp((1.4 - lt) / 0.3)
            text(c, "Tháng 8 · 1945", W / 2, 180, "xbold", 72, "#FFFFFF", a=255 * p, align="center", stroke=7, stroke_color="#111111")
    else:
        q = ease_shot(t, 37.7, 40.39)
        K = Cam(lerp(1500, 1460, q), lerp(430, 420, q), lerp(2.1, 2.4, q), t=t)
        mountains_bg(c, K, t, mist=0.4)
        K.layer(c, 1.0)
        S(c, "sergeant", 1500, GROUND + 60, 0.95, t, face=-1, hand_f=(120, -40), hand_b=(110, -30), eyes="dot", look=(0, 1), mouth="o",
          brow=-0.6, shiver=0.35)
        hx, hy = 1500 - 0.95 * (88 + 120 - 30), GROUND + 60 - 0.95 * (366 + 30)
        c.save(); c.translate(hx, hy); c.rotate(6 + 2 * math.sin(t * 30))
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-70, -90, 140, 180)) or skia.Path(), "#F2EAD6", ow=5)
        for k in range(6):
            c.drawLine(-50, -60 + k * 26, 50, -60 + k * 26, P("#8A7A5A", stroke=4))
        c.restore()
        K.end(c)


def c_radio(c, t):                     # 40,39–45,31  Nhật Hoàng lên tiếng trên radio · dân chúng lần đầu nghe giọng ông
    lt = t - 40.39
    if lt < 2.05:
        q = ease_shot(t, 40.39, 42.44)
        grad(c, skia.Rect.MakeWH(W, H), "#4A3A2C", "#2A2018")
        radio(c, W / 2, 820, lerp(1.6, 1.8, q), t)
        return
    q = ease_shot(t, 42.44, 45.31)
    K = Cam(lerp(980, 940, q), 560, lerp(1.1, 1.25, q), t=t)
    p1.house_in(c, K, t, night=False, lamp=False)
    K.layer(c, 1.0)
    radio(c, 1500, GROUND - 120, 0.6, t)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(1380, GROUND - 120, 240, 120)) or skia.Path(), "#6A4A30", ow=5)
    for i, (who, x) in enumerate([("woman1", 560), ("chief", 800), ("woman3", 1040), ("mother", 1260)]):
        draw_stick(c, Stick(who, x, GROUND, 0.9, t + i, face=1, sit=1.0, hand_f=(60, 150), eyes="closed" if i % 2 else "dot",
                            look=(1, 0), mouth="flat", head_tilt=12, lean=10))
    K.end(c)


def c_end(c, t):                       # 45,31–47,88  chiến tranh đã kết thúc · Nhật Bản đầu hàng
    lt = t - 45.31
    q = ease_shot(t, 45.31, 47.88)
    K = Cam(1460, lerp(470, 560, q), lerp(2.2, 1.6, q), t=t)
    mountains_bg(c, K, t, mist=0.5)
    K.layer(c, 1.0)
    S(c, "sergeant", 1500, GROUND + 60, 0.95, t, face=-1, hand_f=(20, 170), hand_b=(-20, 170), eyes="closed", mouth="flat", head_tilt=14)
    fx = 1500 - 0.95 * 150 + lt * 20
    fy = lerp(GROUND + 60 - 0.95 * 400, GROUND + 50, clamp(lt / 1.8) ** 1.5)
    c.save(); c.translate(fx, fy); c.rotate(6 + 60 * clamp(lt / 1.8) + 10 * math.sin(lt * 4))
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-70, -90, 140, 180)) or skia.Path(), "#F2EAD6", ow=5)
    c.restore()
    K.end(c)


def c_react(c, t):                     # 47,88–51,55  có người quỳ khóc · có người đứng lặng · có người không tin
    lt = t - 47.88
    k = 0 if t < 49.0 else (1 if t < 49.88 else 2)
    K = Cam([800, 1000, 1200][k], 470, 2.0, t=t)
    mountains_bg(c, K, t, mist=0.5)
    K.layer(c, 1.0)
    if k == 0:
        S(c, "recruit1", 800, GROUND, 1.0, t, face=1, crouch=1.0, hand_f=(60, -80), hand_b=(40, -70), eyes="closed", mouth="wobble", tears=1.0,
          head_tilt=20, lean=20)
    elif k == 1:
        S(c, "recruit2", 1000, GROUND, 1.0, t, face=1, hand_f=(20, 170), hand_b=(-20, 170), eyes="dot", mouth="flat", look=(0, 0.2), idle=0.1)
    else:
        S(c, "recruit3", 1200, GROUND, 1.0, t, face=-1, hand_f=(60, 60), eyes="wide", mouth="o", head_tilt=12 * math.sin(lt * 9))
    K.end(c)


def c_thought(c, t):                   # 51,55–56,08  bạn chỉ nghĩ đến một câu: "thà chết…" · người ta dạy mỗi ngày
    lt = t - 51.55
    q = ease_shot(t, 51.55, 56.08)
    K = Cam(1110, 420, lerp(2.4, 2.8, q), t=t)
    mountains_bg(c, K, t, mist=0.5)
    K.layer(c, 1.0)
    S(c, "you", 1100, GROUND, 1.0, t, face=-1, hand_f=(60, 90), hand_b=(30, 100), rifle="hold", eyes="dot", look=(-0.3, 0.6), mouth="flat")
    K.end(c)
    if 0.6 < lt < 3.4:                     # hồi ức: mặt trời đỏ, hàng lính cúi chào — chồng mờ
        a = clamp((lt - 0.6) / 0.4) * clamp((3.4 - lt) / 0.4) * 0.55
        c.saveLayerAlpha(None, int(255 * a))
        p1.c_honor(c, 63.9 + (lt - 0.6) * 0.6)
        c.restore()


def c_drop(c, t):                      # 56,08–58,2  giờ bạn phải buông súng, và bước ra
    lt = t - 56.08
    if lt < 1.1:
        grad(c, skia.Rect.MakeWH(W, H), "#4A5A3A", "#2E3A24")
        ry = lerp(300, 820, clamp((lt - 0.3) / 0.6) ** 2)
        c.save(); c.translate(W / 2, ry); c.rotate(lerp(-20, -78, clamp((lt - 0.3) / 0.6)))
        c.drawLine(-260, 0, 300, 0, P(INK, stroke=40)); c.drawLine(-260, 0, 300, 0, P("#6E4E30", stroke=28))
        c.restore()
        c.drawLine(W / 2 - 100, 260, W / 2 + 300, -100, P(INK, stroke=28))
        return
    q = ease_shot(t, 57.18, 58.2)
    K = Cam(lerp(1000, 1060, q), 540, 1.3, t=t)
    mountains_bg(c, K, t, mist=0.5)
    K.layer(c, 1.0)
    c.drawLine(820, GROUND - 4, 1060, GROUND - 14, P(INK, stroke=14)); c.drawLine(820, GROUND - 4, 1060, GROUND - 14, P("#6E4E30", stroke=8))
    S(c, "you", lerp(1000, 1120, ease_in_out(clamp((lt - 1.3) / 0.8))), GROUND, 1.0, t, face=1, walk=(lt - 1.3) * 5 if lt > 1.3 else None,
      eyes="dot", mouth="flat", look=(1, 0))
    K.end(c)


def c_kenji(c, t):                     # 58,2–63,69  Kenji đặt tay lên vai · "Mày có muốn về nhà không?" · gật đầu · "Thế thì đi thôi."
    lt = t - 58.2
    if t < 62.25:
        q = ease_shot(t, 58.2, 62.25)
        K = Cam(lerp(1060, 1020, q), lerp(440, 450, q), lerp(2.0, 2.2, q), t=t)
        mountains_bg(c, K, t, mist=0.5)
        K.layer(c, 1.0)
        nod = math.sin(clamp((t - 61.38) / 0.8) * math.pi * 2) * 12 if t > 61.38 else 0
        S(c, "you", 1120, GROUND, 1.0, t, face=-1, eyes="dot", look=(1, 0) if lt > 0.6 else (0, 0.3), mouth="flat", head_tilt=nod)
        S(c, "kenji", 860, GROUND, 1.05, t, face=1, hand_f=(lerp(60, 205, ease_out(clamp(lt / 0.6))), lerp(150, 25, ease_out(clamp(lt / 0.6)))),
          eyes="dot", look=(1, 0), mouth="smile" if lt > 1.6 else "flat")
        K.end(c)
    else:
        q = ease_shot(t, 62.25, 63.69)
        K = Cam(lerp(960, 1140, q), 520, lerp(1.2, 1.05, q), t=t)
        mountains_bg(c, K, t, mist=0.6)
        K.layer(c, 0.2)
        g = P("#FFF0C8", 160); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 100))
        c.drawCircle(1800, 520, 300, g)
        K.end(c)
        K.layer(c, 1.0)
        for i, who in enumerate(["kenji", "you"]):
            x = 900 + i * 170 + (t - 62.25) * 120
            S(c, who, x, GROUND, 0.95, t + i, face=1, walk=(t - 62.25) * 5 + i * 0.6, eyes="dot", mouth="smile" if who == "kenji" else "flat")
        K.end(c)


SHOTS = [(0.0, 4.29, c_line), (4.29, 5.84, c_hush), (5.84, 11.12, c_destroyer), (11.12, 15.78, c_lookback), (15.78, 21.66, c_belt),
         (21.66, 26.39, c_islands), (26.39, 28.47, c_retreat), (28.47, 30.77, c_letters), (30.77, 34.10, c_glow),
         (34.10, 40.39, c_assembly), (40.39, 45.31, c_radio), (45.31, 47.88, c_end), (47.88, 51.55, c_react),
         (51.55, 56.08, c_thought), (56.08, 58.20, c_drop), (58.20, DUR, c_kenji)]
FADE = {15.78, 21.66, 34.10, 58.20}


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
                        str(BUILD / "P3_nosfx.mp4")], check=True)
        for x in chs:
            x.unlink()
        (BUILD / "c.txt").unlink()
        print("xong")
