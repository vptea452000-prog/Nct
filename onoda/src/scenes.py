"""Onoda v2 — hoạt hình 2D thuần (không ảnh thật), nhân vật có chuyển động, cắt cảnh nhanh, chuyển cảnh lia máy.
Mốc giây theo MP3 (ước lượng, build/words.json)."""
import math
import skia
from lib import *  # noqa
from toon import mascot, big_title, OUT, fill_out, rrect_path, oval_path, limb  # noqa
from toon2 import soldier2, civilian, kinetic
from sets import cam, grad_rect, vignette, blurred, frond, jungle, fg_leaves, bookshop, plane, sea_sky


def pop(t, t0, d=0.3):
    return prog(t, t0, t0 + d)


def phase(t, t0, speed=7.0):
    return (t - t0) * speed


def shake(c, t, t0, amp=16, dur=0.35):
    if t0 <= t < t0 + dur:
        k = 1 - (t - t0) / dur
        c.translate(amp * k * math.sin((t - t0) * 90), amp * k * math.cos((t - t0) * 70))


def stamp_big(c, s, x, y, t, t0, color="#C0392B", rot=-10, size=80):
    stamp(c, s, x, y, prog(t, t0, t0 + 0.22), size=size, color=color, rot=rot)


def bubble(c, x, y, l1, l2=None, t=0, t0=0, rot=-3, red2=True, tail=-1):
    p = pop(t, t0, 0.35)
    if p <= 0:
        return
    w = max(tw(l1, "xbold", 50), tw(l2 or "", "xbold", 44)) + 90
    h = 120 if not l2 else 170
    with Xf(c, x, y, rot, max(0.01, back_out(p))):
        fill_out(c, rrect_path(-w / 2, -h / 2, w, h, 60), "white")
        tl = skia.Path(); tl.moveTo(tail * 40, h / 2 - 4); tl.lineTo(tail * 90, h / 2 + 60); tl.lineTo(tail * -10, h / 2 - 4); tl.close()
        fill_out(c, tl, "white")
        c.drawRect(skia.Rect.MakeXYWH(-50, h / 2 - 12, 100, 14), paint("white"))
        if l2:
            text(c, l1, 0, -12, "xbold", 50, "ink", align="center")
            text(c, l2, 0, 50, "xbold", 44, "#C0392B" if red2 else "ink", align="center")
        else:
            text(c, l1, 0, 18, "xbold", 50, "ink", align="center")


def rays(c, t, color="#F4C430", a=60, cx=540, cy=760):
    for k in range(14):
        ang = k * math.pi / 7 + t * 0.12
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + 1800 * math.cos(ang), cy + 1800 * math.sin(ang)); p.lineTo(cx + 1800 * math.cos(ang + 0.18), cy + 1800 * math.sin(ang + 0.18)); p.close()
        c.drawPath(p, paint(color, a))


def cloud(c, x, y, s, a=230):
    for dx, dy, r in [(-60, 10, 50), (0, -10, 70), (70, 8, 55), (20, 30, 50)]:
        c.drawCircle(x + dx * s, y + dy * s, r * s, paint("white", a))


def island(c, cx, cy, s):
    with Xf(c, cx, cy, 0, s):
        p = skia.Path(); p.moveTo(-300, 40); p.cubicTo(-280, -120, -60, -170, 60, -110); p.cubicTo(200, -150, 330, -40, 300, 40)
        p.cubicTo(250, 110, -220, 120, -300, 40); p.close()
        c.drawPath(p, paint("#F2E2B5")); c.drawPath(p, paint(OUT, stroke=6))
        q = skia.Path(); q.moveTo(-250, 20); q.cubicTo(-220, -100, -40, -140, 60, -90); q.cubicTo(180, -120, 280, -30, 250, 20)
        q.cubicTo(200, 80, -180, 90, -250, 20); q.close()
        fill_out(c, q, "#4F7F45", ow=5)
        m = skia.Path(); m.moveTo(-60, -40); m.lineTo(20, -150); m.lineTo(110, -50); m.close()
        fill_out(c, m, "#3E6A3A", ow=5)
        for k in range(14):
            c.drawCircle(-200 + k * 30, -10 + 20 * math.sin(k), 18, paint("#3A6A36"))


def bushes(c, t, part=0.0, y=1250):
    for side in (-1, 1):
        x0 = 540 + side * (140 + 420 * part)
        for k in range(5):
            c.drawCircle(x0 + side * k * 70, y - 120 - (k % 2) * 60, 150, paint("#1F3A20"))
            c.drawCircle(x0 + side * k * 70, y - 120 - (k % 2) * 60, 150, paint(OUT, 120, stroke=5))


def campfire(c, x, y, s, t, strength=1.0):
    with Xf(c, x, y, 0, s):
        for k in range(3):
            c.drawLine(-80, 10 - k * 6, 80, -10 + k * 6, paint("#5A3E26", stroke=18))
        glow = paint("#F39C12", 70 * strength); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60))
        c.drawCircle(0, -60, 200 * strength, glow)
        for k, (colr, sc) in enumerate([("#C0392B", 1.0), ("#F39C12", 0.72), ("#F4D03F", 0.45)]):
            fl = skia.Path(); wob = 10 * math.sin(t * 12 + k)
            h = 190 * sc * strength
            fl.moveTo(-60 * sc, 0); fl.quadTo(-70 * sc, -h * 0.5, wob, -h); fl.quadTo(70 * sc, -h * 0.5, 60 * sc, 0); fl.close()
            c.drawPath(fl, paint(colr, 235))


def rain(c, t, a=150):
    for k in range(80):
        x = (k * 137 + t * 300) % (W + 200) - 100
        y = (k * 211 + t * 1500) % (H + 200) - 100
        c.drawLine(x, y, x - 14, y + 50, paint("#BFD3E6", a, stroke=3))


def map_proj(lon0, lon1, lat1, y0=280):
    sx = W / (lon1 - lon0)
    return lambda lon, lat: ((lon - lon0) * sx, y0 + (lat1 - lat) * sx)


def draw_map(c, pr, rings_list, land="#9BC27A"):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#7FB3D5", "#4F8FB8")
    for k in range(0, 40):
        c.drawLine(0, 300 + k * 80, W, 300 + k * 80, paint("white", 25, stroke=2))
    for rings_ in rings_list:
        for ring in rings_:
            p = skia.Path()
            for j, (lon, lat) in enumerate(ring):
                (p.moveTo if j == 0 else p.lineTo)(*pr(lon, lat))
            p.close()
            fill_out(c, p, land, ow=6)


def tv(c, x, y, s, t, content):
    with Xf(c, x, y, 0, s):
        fill_out(c, rrect_path(-300, -230, 600, 460, 40), "#6B4A30")
        fill_out(c, rrect_path(-250, -190, 420, 330, 30), "#202A24")
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-250, -190, 420, 330), 30, 30), True)
        content(c)
        for k in range(60):
            c.drawLine(-250, -190 + k * 6, 170, -190 + k * 6, paint("#000000", 40, stroke=2))
        c.restore()
        for k in range(2):
            c.drawCircle(235, -100 + k * 90, 26, paint("#C9A55A")); c.drawCircle(235, -100 + k * 90, 26, paint(OUT, stroke=5))
        for side in (-1, 1):
            c.drawLine(side * 60, -230, side * 140, -330, paint(OUT, stroke=6))


def radar_dish(c, x, y, s, t):
    """Trạm radar: tháp + vòm radar tròn + ăng-ten quay."""
    with Xf(c, x, y, 0, s):
        fill_out(c, rrect_path(-150, -160, 300, 160, 10), "#E9E2CF")
        for k in range(3):
            fill_out(c, rrect_path(-120 + k * 90, -120, 50, 50, 6), "#9FC3D9", ow=4)
        fill_out(c, rrect_path(-40, -330, 80, 180, 8), "#C9C3B4")
        dome = skia.Path(); dome.moveTo(-130, -330); dome.arcTo(skia.Rect.MakeXYWH(-130, -460, 260, 260), 180, 180, False); dome.close()
        fill_out(c, dome, "#F6F1E4")
        a = (t * 90) % 360
        with Xf(c, 0, -470, 0, 1):
            w = 90 * math.cos(math.radians(a))
            c.drawLine(0, 40, 0, 0, paint(OUT, stroke=6))
            c.drawLine(-w, 0, w, 0, paint(OUT, stroke=10))


def candle(c, x, y, s, t, k):
    with Xf(c, x, y, 0, s):
        fill_out(c, rrect_path(-14, -60, 28, 60, 4), "#EFE6D2", ow=4)
        g = paint("#F39C12", 80); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
        c.drawCircle(0, -78, 30, g)
        fl = skia.Path(); wob = 3 * math.sin(t * 9 + k)
        fl.moveTo(-9, -62); fl.quadTo(-10, -80, wob, -100); fl.quadTo(10, -80, 9, -62); fl.close()
        c.drawPath(fl, paint("#F4D03F"))


def year_counter(c, t, years):
    """Đồng hồ năm góc trên: years = [(thời điểm, năm)]."""
    y = years[0][1]
    for ts, yy in years:
        if t >= ts:
            y = yy
    with Xf(c, W - 200, 300, 0, 1):
        fill_out(c, rrect_path(-140, -60, 280, 120, 16), "#2E2A25")
        text(c, str(y), 0, 30, "xbold", 80, "#F4C430", align="center")


# ================================================================ CẢNH
def a1_dive(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#F2B36B", "#7FB3D5")
    p = ease_in_out(clamp(t / 2.1))
    z = math.exp(lerp(math.log(0.35), math.log(2.2), p))
    c.save(); c.translate(W / 2, 900); c.scale(z, z)
    c.drawRect(skia.Rect.MakeXYWH(-3000, -200, 6000, 4000), paint("#3F7FA6"))
    for k in range(12):
        c.drawLine(-3000, -100 + k * 60, 3000, -100 + k * 60, paint("white", 40, stroke=3))
    island(c, 0, 0, 1.0)
    c.restore()
    for k in range(6):
        sc = lerp(0.8, 4.0, p) * (1 + k * 0.2)
        cloud(c, W / 2 + (k - 2.5) * 260 * sc * 0.5, 500 + (k % 3) * 300 * (1 + p), sc, a=int(220 * (1 - p * 0.8)))
    kinetic(c, "1974", W / 2, 560, t, 0.5, size=170)


def a2_canopy(c, t):
    z = lerp(1.0, 1.25, ease_out(clamp((t - 2.1) / 2.0)))
    c.save(); cam(c, 540, 880, z); jungle(c, t); c.restore()
    blurred(c, 10, lambda: fg_leaves(c, t))
    vignette(c)
    kinetic(c, "PHILIPPINES", W / 2, 520, t, 2.3, size=96, color="#F4C430", per=0.04)
    # linh vật đu dây leo vào khung
    p = clamp((t - 2.6) / 0.9)
    ang = lerp(-60, 0, back_out(p)) if p < 1 else 4 * math.sin((t - 3.5) * 5)
    px, py = 860, 200
    ex, ey = px + 700 * math.sin(math.radians(ang)), py + 700 * math.cos(math.radians(ang))
    c.drawLine(px, py - 400, ex, ey - 175, paint("#3A5A2C", stroke=10))
    mascot(c, ex, ey, 0.75, "smile", t=t, arm="up", rot=-ang * 0.5)


def b1_bush(c, t):
    night = 1 - pop(t, 4.9, 0.6) * 0.5
    c.save(); cam(c, 540, 900, 1.25); jungle(c, t); c.restore()
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#0E1A2B", 150 * night))
    part = ease_out(clamp((t - 4.9) / 0.6))
    if t > 4.9:
        w = ease_out(clamp((t - 4.95) / 0.8))
        soldier2(c, 540, 1300, 1.2, t=t, walk=phase(t, 4.95) if w < 1 else None, look=0.0, mood="angry")
    bushes(c, t, part)
    if t < 5.0:
        for side in (-1, 1):
            g = paint("#F4D03F", 230 * pop(t, 4.3, 0.15)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
            c.drawOval(skia.Rect.MakeXYWH(540 + side * 40 - 14, 760, 28, 12), g)
    vignette(c, 190)


def b2_inserts(c, t):
    c.save()
    if t < 6.3:
        cam(c, 540, 1250, 3.2)
    elif t < 6.75:
        cam(c, 700, 700, 2.8)
    else:
        cam(c, 540, 630, 3.6)
    jungle(c, t)
    soldier2(c, 540, 1300, 1.2, t=t, look=0.0, mood="angry")
    c.restore()
    vignette(c, 200)
    lab = "quân phục" if t < 6.3 else ("súng" if t < 6.75 else "sĩ quan Nhật")
    t0 = 5.85 if t < 6.3 else (6.3 if t < 6.75 else 6.75)
    kinetic(c, lab.upper(), W / 2, 420, t, t0, size=90, color="#F4C430", per=0.02)


def b3_believe(c, t):
    c.save(); cam(c, 470, 720, lerp(1.6, 1.8, clamp((t - 7.2) / 1.5))); jungle(c, t)
    soldier2(c, 470, 1290, 1.25, t=t, talk=True, mood="angry", look=0.3)
    c.restore()
    vignette(c, 170)
    bubble(c, 640, 400, "THẾ CHIẾN", "CHƯA KẾT THÚC!", t=t, t0=7.3)
    pm = pop(t, 7.8, 0.35)
    if pm > 0:
        mascot(c, 900, lerp(1700, 1290, back_out(pm)), 0.6, "worried", look=(-1, -0.5), t=t, arm="point")
        with Xf(c, 1010, 1080, 8, 0.8):
            fill_out(c, rrect_path(-70, -60, 140, 120, 10), "white")
            c.drawRect(skia.Rect.MakeXYWH(-70, -60, 140, 34), paint("#C0392B"))
            text(c, "1974", 0, 42, "xbold", 44, "ink", align="center")


def c1_bookshop(c, t):
    c.save(); cam(c, 540, 900, lerp(1.35, 1.1, ease_out(clamp((t - 8.71) / 1.2)))); bookshop(c, t)
    talk = t > 10.8
    civilian(c, 620, 1290, 1.15, t=t, kind="taniguchi", pose="read" if t < 10.8 else "arms", talk=False, look=-0.4 if t < 10.8 else 0.5,
             mood="flat")
    mascot(c, 240, 1020, 0.72, "think", look=(1, 0), t=t)
    c.restore()
    vignette(c, 120)
    kinetic(c, "CHỈ HUY CŨ", W / 2, 340, t, 9.5, size=70, per=0.03)
    if t > 10.8:
        kinetic(c, "NAY BÁN SÁCH", W / 2, 440, t, 10.9, size=64, color="#F4C430", per=0.03)


RJ = country_rings("Japan")
RP = country_rings("Philippines")


def c3_fly(c, t):
    pr = map_proj(115, 145, 40, y0=200)
    draw_map(c, pr, [RJ, RP])
    jx, jy = pr(139.7, 35.7); mx, my = pr(120.98, 14.6)
    pin(c, jx, jy, 1, color="white"); label_tag(c, "NHẬT BẢN", jx + 24, jy - 44, 1, size=30)
    pin(c, mx, my, pop(t, 12.4)); label_tag(c, "PHILIPPINES", mx + 24, my + 40, pop(t, 12.4), size=30, bg="yellow")
    p = clamp((t - 12.1) / 1.4)
    r = path_partial(c, [(jx, jy), (mx, my)], p, paint(OUT, stroke=6, PathEffect=skia.DashPathEffect.Make([18, 12], 0)), curve=0.2)
    if r:
        ang = math.degrees(math.atan2(r[1][1], r[1][0]))
        with Xf(c, r[0][0], r[0][1], ang, 0.5):
            plane(c, 0, 0, 1.0)


def d_name(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#D4BE86")
    rays(c, t)
    c.save(); shake(c, t, 13.75, 18)
    p = pop(t, 13.57, 0.2)
    sc = lerp(3.0, 1.0, ease_out(p))
    with Xf(c, W / 2, 700, -3, sc, clamp(p * 3)):
        fill_out(c, rrect_path(-260, -320, 520, 600, 10), "#FBF7EE")
        c.save(); c.clipRect(skia.Rect.MakeXYWH(-230, -290, 460, 520))
        grad_rect(c, skia.Rect.MakeXYWH(-230, -290, 460, 520), "#9FB8C9", "#6E8FA6")
        soldier2(c, 0, 520, 1.05, t=t, look=0.0, mood="flat", rifle=False)
        c.restore()
        c.drawRect(skia.Rect.MakeXYWH(-230, -290, 460, 520), paint(OUT, stroke=5, cap=False))
    c.restore()
    kinetic(c, "HIROO ONODA", W / 2, 1110, t, 14.2, size=86, color="#F4C430", per=0.04)
    label_tag(c, "thiếu úy · Lục quân Đế quốc Nhật", W / 2, 1200, pop(t, 14.9), size=30, anchor="center")
    mascot(c, 950, 1300, 0.5, "smile", look=(-1, -0.4), t=t, arm="point")


def e1_route(c, t):
    pr = map_proj(119.0, 122.4, 15.8, y0=260)
    draw_map(c, pr, [RP])
    lx, ly = pr(120.12, 13.82)
    fill_out(c, oval_path(lx, ly, 46, 22), "#9BC27A", ow=5)
    mx, my = pr(120.98, 14.6)
    chip(c, "CUỐI 1944", W / 2, 250, pop(t, 15.85))
    pin(c, mx, my, pop(t, 16.3), color="white"); label_tag(c, "MANILA", mx + 26, my - 44, pop(t, 16.3), size=32)
    pin(c, lx, ly, pop(t, 17.6)); label_tag(c, "LUBANG", lx - 26, ly + 70, pop(t, 17.6), size=36, anchor="right", bg="yellow")
    p = clamp((t - 17.5) / 1.3)
    r = path_partial(c, [(mx, my + 20), (lx + 40, ly)], p, paint(OUT, stroke=6, PathEffect=skia.DashPathEffect.Make([16, 12], 0)), curve=-0.3)
    if r:
        with Xf(c, r[0][0], r[0][1], 0, 0.5):
            fill_out(c, rrect_path(-60, -10, 120, 30, 10), "#5A4A3A"); fill_out(c, rrect_path(-20, -40, 40, 30, 4), "#E9E2CF", ow=4)


def e2_order(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#3A2418", "#1C110B")
    c.save(); shake(c, t, 20.32, 20)
    p = pop(t, 18.9, 0.4)
    with Xf(c, W / 2, lerp(1400, 720, ease_out(p)), -4, 1, clamp(p * 2)):
        fill_out(c, rrect_path(-330, -220, 660, 440, 8), "#E9D9A6")
        c.drawLine(-330, -220, 0, 40, paint(OUT, stroke=5)); c.drawLine(330, -220, 0, 40, paint(OUT, stroke=5))
        c.drawCircle(0, 30, 50, paint("#C0392B")); c.drawCircle(0, 30, 50, paint(OUT, stroke=5))
        text(c, "LỆNH", 0, 170, "xbold", 50, "ink", align="center")
    stamp_big(c, "KHÔNG ĐẦU HÀNG", W / 2, 1060, t, 20.3, size=76, rot=-6)
    c.restore()
    mascot(c, 920, 1300, 0.55, "shock", t=t, arm="up")


def e3_retreat(c, t):
    c.save(); cam(c, lerp(400, 700, clamp((t - 21.44) / 3)), 880, 1.12); jungle(c, t)
    for k in range(4):
        x = lerp(150, 1250, clamp((t - 21.6 - k * 0.12) / 2.8)) - k * 170
        soldier2(c, x, 1250, 0.7 if k == 0 else 0.62, t=t + k, walk=phase(t, 21.6 + k, 9), look=0.6, variant=k)
    c.restore()
    blurred(c, 12, lambda: fg_leaves(c, t))
    vignette(c)
    for k in range(3):
        x = 120 + k * 160 - 30 * clamp((t - 21.5) / 3)
        fill_out(c, rrect_path(x - 60, 300, 120, 30, 6), "#6E767C", a=170, ow=4)
        c.drawRect(skia.Rect.MakeXYWH(x - 10, 270, 20, 30), paint("#6E767C", 170))
    label_tag(c, "quân Mỹ đổ bộ", 120, 380, pop(t, 21.5), size=30)
    label_tag(c, "Onoda + 3 lính rút vào núi", W / 2, 470, pop(t, 22.6), size=34, anchor="center", bg="yellow")


def f1_split(c, t):
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 0, W, 960))
    grad_rect(c, skia.Rect.MakeXYWH(0, 0, W, 960), "#E9D9A6", "#C9A86A")
    with Xf(c, W / 2, 620, 0, 1):
        fill_out(c, rrect_path(-200, -120, 400, 240, 30), "#7B3B2E")
        c.drawCircle(-80, 0, 70, paint("#2E2A25")); c.drawCircle(-80, 0, 70, paint(OUT, stroke=5))
        for k in range(3):
            c.drawLine(40, -50 + k * 40, 150, -50 + k * 40, paint("#E9E2CF", stroke=8))
    rings(c, W / 2, 560, t, 24.5, 27.4, "#C0392B", max_r=500, period=0.4, width=5)
    big_title(c, "8 · 1945", "NHẬT ĐẦU HÀNG", 300, pop(t, 24.6, 0.4), size=110, bsize=50)
    c.restore()
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 960, W, 960))
    c.translate(0, 480)
    c.save(); cam(c, 540, 900, 1.3); jungle(c, t); c.restore()
    soldier2(c, 540, 1240, 0.85, t=t, look=math.sin(t * 2) * 0.6, mood="flat")
    c.restore()
    c.drawRect(skia.Rect.MakeXYWH(0, 952, W, 16), paint(OUT))
    label_tag(c, "trong rừng: không ai biết", W / 2, 1050, pop(t, 25.8), size=32, anchor="center")


def f2_leaflets(c, t):
    c.save(); cam(c, 540, 880, 1.12); jungle(c, t)
    p = clamp((t - 27.5) / 2.0)
    plane(c, lerp(-250, 1300, p), lerp(420, 360, p), 1.0)
    soldier2(c, 560, 1250, 1.0, t=t, look=-0.2, mood="surprise" if t > 30.2 else "flat")
    for k in range(16):
        st = 27.9 + k * 0.14
        a = t - st
        if a > 0:
            x = lerp(-250, 1300, clamp((st - 27.5) / 2.0)) + 50 * math.sin(a * 3 + k) + a * 20
            y = 380 + a * 300
            if k == 9:
                q = clamp((t - 29.6) / 0.6)
                x = lerp(x, 560, q); y = lerp(y, 610, q)
            with Xf(c, x, y, a * 140 + k * 30 if k != 9 or t < 30.2 else 4, 0.22 if k != 9 or t < 30.2 else 0.5):
                fill_out(c, rrect_path(-150, -200, 300, 400, 6), "#F1EAD7")
                c.drawLine(-100, -100, 100, -100, paint(OUT, stroke=12)); c.drawLine(-100, 0, 80, 0, paint(OUT, stroke=12))
    c.restore()
    label_tag(c, "truyền đơn: lệnh đầu hàng", W / 2, 330, pop(t, 28.3), size=34, anchor="center", bg="yellow")


def f3_fake(c, t):
    c.save(); cam(c, 540, 900, 1.2); jungle(c, t)
    for k, (x, f) in enumerate([(220, False), (400, False), (720, True), (900, True)]):
        soldier2(c, x, 1260, 0.75, t=t + k, pose="read" if k == 0 else "stand", flip=f, look=0.6 if not f else 0.6, variant=k, mood="angry")
    c.restore()
    vignette(c, 160)
    p = pop(t, 32.3, 0.4)
    if p > 0:
        with Xf(c, W / 2, 680, 3, back_out(p)):
            fill_out(c, rrect_path(-260, -330, 520, 660, 6), "#F1EAD7")
            text(c, "LỆNH", 0, -200, "xbold", 80, "ink", align="center")
            text(c, "ĐẦU HÀNG", 0, -110, "xbold", 64, "ink", align="center")
            for k in range(6):
                c.drawLine(-200, -20 + k * 45, 200 - (k % 2) * 60, -20 + k * 45, paint("#8E846F", stroke=8))
            gx = lerp(-150, 120, (math.sin(t * 2) + 1) / 2)
            c.drawCircle(gx, 80, 90, paint("white", 60)); c.drawCircle(gx, 80, 90, paint(OUT, stroke=12))
            c.drawLine(gx + 60, 150, gx + 140, 260, paint(OUT, stroke=24))
    note_label(c, "MINH HỌA", 60, 330, 1)
    c.save(); shake(c, t, 33.42, 18); stamp_big(c, "ĐỒ GIẢ!", W / 2, 760, t, 33.4, size=120); c.restore()


def f4_swat(c, t):
    c.save(); cam(c, 540, 900, 1.2); jungle(c, t); c.restore()
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#0E1A2B", 80))
    soldier2(c, 600, 1260, 1.1, t=t, pose="swat" if t < 37.3 else "cross", mood="angry", look=-0.5)
    with Xf(c, 160, 560, -10, 1, pop(t, 35.1)):
        fill_out(c, rrect_path(-50, -40, 60, 80, 8), "#5A524A")
        horn = skia.Path(); horn.moveTo(10, -30); horn.lineTo(130, -90); horn.lineTo(130, 90); horn.lineTo(10, 30); horn.close()
        fill_out(c, horn, "#8E959B")
    rings(c, 300, 540, t, 35.2, 37.0, "#F4C430", max_r=300, period=0.3, width=5)
    for k in range(5):
        st = 35.6 + k * 0.32; a = t - st
        if a > 0:
            hit = clamp(a / 0.45)
            x = lerp(-120, 520, hit); y = lerp(400 + k * 90, 640 + k * 30, hit)
            b = clamp((a - 0.45) / 0.6)
            with Xf(c, lerp(x, -200, b), lerp(y, y - 400, b), k * 25 + a * 200 * b, 1, 1 - b * 0.7):
                fill_out(c, rrect_path(-70, -46, 140, 92, 6), "#F1EAD7", ow=5)
                c.drawLine(-70, -46, 0, 10, paint(OUT, stroke=4)); c.drawLine(70, -46, 0, 10, paint(OUT, stroke=4))
    c.save(); shake(c, t, 37.35, 14); stamp_big(c, "KHÔNG ĐỔI Ý", W / 2, 420, t, 37.3, color="#1F3A5F", size=70, rot=-5); c.restore()


def g1_raid(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#2A0E08", "#0B0604")
    burn = pop(t, 41.0, 1.0)
    glow = paint("#E67E22", 160 * burn); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 120))
    c.drawRect(skia.Rect.MakeXYWH(-200, 900, W + 400, 500), glow)
    for k in range(9):
        x = 60 + k * 125
        if burn > 0:
            campfire(c, x, 1240, 0.55 * burn * (0.8 + 0.3 * math.sin(k)), t + k, 1.0)
        for j in range(4):
            c.drawLine(x + j * 14 - 20, 1250, x + j * 14 - 20 + 6 * math.sin(t * 2 + k), 1170, paint("#1A0C06", stroke=6))
    for k in range(4):
        x = lerp(-200, 1300, clamp((t - 38.8 - k * 0.3) / 4.5))
        with Xf(c, 0, 0, 0, 1, 1):
            c.save()
            c.saveLayer(None, skia.Paint(ColorFilter=skia.ColorFilters.Blend(skia.ColorSetARGB(255, 12, 6, 4), skia.BlendMode.kSrcIn)))
            soldier2(c, x, 1250, 0.6, t=t + k, walk=phase(t, 38.8 + k, 8), variant=k)
            c.restore(); c.restore()
    for k, ts in enumerate([41.7, 42.1, 42.5, 42.9]):
        a = t - ts
        if 0 < a < 0.14:
            fl = paint("#FFE7A8", 255 * (1 - a / 0.14)); fl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12))
            c.drawCircle(220 + k * 210, 800 + (k % 2) * 60, 55, fl)
    kinetic(c, "DU KÍCH", W / 2, 400, t, 38.7, size=110, color="#E9E2CF", per=0.04)
    label_tag(c, "lấy lương thực · đốt lúa · nổ súng", W / 2, 520, pop(t, 39.8), size=32, anchor="center")


def g2_candles(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#120E0B"))
    n = int(clamp((t - 45.4) / 1.5) * 30)
    for k in range(n):
        r, cc = divmod(k, 6)
        candle(c, 210 + cc * 132, 780 + r * 100, 0.8, t, k)
    label_tag(c, "theo lời dân làng kể lại", W / 2, 420, pop(t, 43.9), size=32, anchor="center")
    text(c, "khoảng 30 người chết", W / 2, 560, "bold", 54, "#E9E2CF", a=255 * pop(t, 46.0, 0.6), align="center")


YEARS = [(47.4, 1949), (48.7, 1950), (51.0, 1954), (53.0, 1972)]


def h_campfire(c, t):
    night = "#0E1A2B"
    c.save(); cam(c, 540, 900, 1.15); jungle(c, t); c.restore()
    c.drawRect(skia.Rect.MakeWH(W, H), paint(night, 160))
    if t < 53.0:
        campfire(c, 540, 1250, 0.9, t)
        for k, x in enumerate([200, 380, 700, 880]):
            a, dx, rot = 1.0, 0, 0
            if k == 1:
                q = clamp((t - 49.0) / 1.6); dx = -500 * ease_in_out(q); a = 1 - q * 0.6
            if k == 2 and t > 51.6:
                a = 1 - pop(t, 51.6, 0.7) * 0.9
            c.save(); c.saveLayerAlpha(None, int(255 * a))
            soldier2(c, x + dx, 1260, 0.62, t=t + k, flip=(x > 540) if k != 1 or t < 49 else True, look=0.4,
                     walk=phase(t, 49.0) if k == 1 and 49 < t < 50.6 else None, variant=k, age=0.2)
            c.restore(); c.restore()
        if 51.6 < t < 51.75:
            fl = paint("#FFE7A8", 220); fl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)); c.drawCircle(980, 700, 100, fl)
        label_tag(c, "1950 · một người bỏ đi, đầu hàng", W / 2, 420, pop(t, 48.8), size=30, anchor="center", bg="yellow")
        label_tag(c, "1954 · một người bị bắn chết", W / 2, 500, pop(t, 51.1), size=30, anchor="center", bg="red", fg="white")
    elif t < 60.78:
        rice_x = 0
        burn = pop(t, 57.0, 0.6)
        for k in range(8):
            campfire(c, 80 + k * 135, 1260, 0.45 * burn, t + k)
        fall = pop(t, 58.6, 0.5)
        soldier2(c, 330, 1260, 0.8, t=t, look=0.6, age=0.6, worn=0.8, rifle=True)
        c.save(); c.saveLayerAlpha(None, int(255 * (1 - fall * 0.7)))
        soldier2(c, 760, 1260, 0.8, t=t + 1, flip=True, look=0.6, variant=2, age=0.6, worn=0.8, rot=fall * 80)
        c.restore(); c.restore()
        if 58.5 < t < 58.65:
            c.drawRect(skia.Rect.MakeWH(W, H), paint("#FFFFFF", 160))
        name_tag(c, 60, 360, "Kinshichi Kozuka", "người lính cuối cùng bên Onoda", pop(t, 54.8, 0.4) * (1 - pop(t, 58.4, 0.3)), size=42, role_size=28)
        label_tag(c, "bị cảnh sát bắn chết khi đang đốt lúa", W / 2, 360, pop(t, 58.7), size=30, anchor="center", bg="red", fg="white")
    else:
        campfire(c, 540, 1250, 0.5, t, 0.6)
        soldier2(c, 700, 1260, 0.6, t=t, flip=True, look=0.0, mood="sad", age=0.7, worn=1.0)
        rain(c, t)
        kinetic(c, "MỘT MÌNH", W / 2, 560, t, 61.2, size=110, per=0.05)
    vignette(c, 200)
    year_counter(c, t, YEARS)


def i1_tv(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#C9A86A", "#8A6A3A")
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, 800), paint("#6B4A30"))

    def news(cc):
        grad_rect(cc, skia.Rect.MakeXYWH(-250, -190, 420, 330), "#5A7A8A", "#2E4A5A")
        soldier2(cc, -40, 180, 0.42, t=t, look=0.0)
        cc.drawRect(skia.Rect.MakeXYWH(-250, 80, 420, 60), paint("#C0392B"))
        text(cc, "TIN NÓNG", -230, 122, "xbold", 34, "white")

    tv(c, 400, 760, 1.15, t, news)
    note_label(c, "MINH HỌA", 60, 330, 1)
    pm = pop(t, 63.0, 0.3)
    mascot(c, 880, 1300 - 120 * math.sin(clamp((t - 63.0) / 0.5) * math.pi), 0.7, "shock" if t > 63 else "smile", t=t, arm="up")
    kinetic(c, "NHẬT BẢN SỬNG SỜ", W / 2, 360, t, 63.4, size=72, color="#1A120D", stroke_color="#F6F1E4", per=0.03)


def i2_dead(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#D4BE86")
    with Xf(c, 540, 700, 2, 1, pop(t, 66.6, 0.3)):
        fill_out(c, rrect_path(-320, -360, 640, 720, 4), "#F6F1E4")
        text(c, "CHÍNH PHỦ NHẬT", 0, -260, "xbold", 44, "ink", align="center")
        text(c, "1959", 0, -150, "xbold", 90, "ink", align="center")
        text(c, "những người lính này", 0, -40, "semi", 38, "grey", align="center")
        text(c, "đều đã chết", 0, 10, "semi", 38, "grey", align="center")
    note_label(c, "MINH HỌA", 700, 290, 1)
    c.save(); shake(c, t, 68.32, 16); stamp_big(c, "ĐÃ CHẾT", 560, 900, t, 68.3, size=90); c.restore()


def i3_alive(c, t):
    c.save(); cam(c, 540, 880, 1.1); jungle(c, t); c.restore()
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#05080C", 200))
    ang = math.sin((t - 69.2) * 1.4) * 35
    beam = skia.Path(); beam.moveTo(540, 1900)
    for s_ in (-1, 1):
        a = math.radians(ang + s_ * 8 - 90)
        beam.lineTo(540 + 2200 * math.cos(a), 1900 + 2200 * math.sin(a))
    beam.close()
    c.drawPath(beam, paint("#FFF3C4", 70))
    if t > 71.8:
        for side in (-1, 1):
            g = paint("#F4D03F", 240 * pop(t, 71.8, 0.15)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
            c.drawOval(skia.Rect.MakeXYWH(620 + side * 40 - 14, 980, 28, 12), g)
    kinetic(c, "KOZUKA CÒN SỐNG TỚI 1972…", W / 2, 360, t, 69.3, size=56, per=0.02)
    kinetic(c, "THÌ ONODA?", W / 2, 470, t, 71.8, size=84, color="#F4C430", per=0.04)


def j1_suzuki(c, t):
    c.save(); cam(c, lerp(300, 700, clamp((t - 73.3) / 5.5)), 880, 1.15); jungle(c, t)
    civilian(c, lerp(-100, 900, clamp((t - 73.3) / 5.5)), 1250, 1.0, t=t, kind="suzuki", walk=phase(t, 73.3, 7), look=0.6, mood="smile")
    c.restore()
    blurred(c, 12, lambda: fg_leaves(c, t))
    vignette(c)
    chip(c, "2 · 1974", W / 2, 250, pop(t, 73.4))
    name_tag(c, 60, 340, "Norio Suzuki", "chàng trai Nhật · một mình tới Lubang", pop(t, 75.4, 0.4), size=44, role_size=28)


def j2_meet(c, t):
    days = clamp((t - 78.85) / 1.6)
    sky_t = (days * 4) % 1
    top = ["#F2B36B", "#9FC9E6", "#F2B36B", "#22314A"]
    c.save(); cam(c, 540, 900, 1.15); jungle(c, t); c.restore()
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#0E1A2B", 120 * abs(math.sin(days * 4 * math.pi)) if t < 80.45 else 0))
    sx = lerp(100, 980, sky_t); sy = 500 - 260 * math.sin(sky_t * math.pi)
    if t < 80.45:
        g = paint("#FFE7A8", 230); c.drawCircle(sx, sy, 70, g)
        label_tag(c, f"NGÀY {min(4, 1 + int(days * 4))}", W / 2, 340, 1, size=46, anchor="center", bg="yellow")
    up = pop(t, 80.6, 0.25)
    civilian(c, 330, 1260, 1.0, t=t, kind="suzuki", look=0.6, mood="surprise" if t > 80.5 else "flat", hands_up=up)
    pe = prog(t, 80.4, 80.7, ease_out)
    soldier2(c, lerp(1300, 820, pe), 1260, 1.0, t=t, pose="aim", flip=True, mood="angry")
    if t > 80.45:
        kinetic(c, "GẶP RỒI!", W / 2, 360, t, 80.5, size=96, color="#F4C430", per=0.04)


def j3_photo(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#2E4A62", "#13263B")
    a = t - 81.67
    p = pop(t, 81.75, 0.4)
    dev = clamp((t - 82.0) / 1.0)
    with Xf(c, W / 2, 700, lerp(-12, -3, ease_out(p)), lerp(0.7, 1.0, back_out(p)), clamp(p * 2)):
        fill_out(c, rrect_path(-330, -360, 660, 760, 8), "#FBF7EE")
        c.save(); c.clipRect(skia.Rect.MakeXYWH(-290, -320, 580, 560))
        jungle(c, t * 0)  # khung nền rừng (vẽ theo toạ độ cục bộ đã dịch)
        c.restore()
        c.save(); c.clipRect(skia.Rect.MakeXYWH(-290, -320, 580, 560))
        grad_rect(c, skia.Rect.MakeXYWH(-290, -320, 580, 560), "#5E7A4E", "#2F4A2A")
        civilian(c, -110, 330, 0.62, t=0.3, kind="suzuki", mood="smile", look=0.4)
        soldier2(c, 130, 330, 0.62, t=0.3, look=-0.4, mood="smile", age=0.7, worn=0.8)
        c.drawRect(skia.Rect.MakeXYWH(-290, -320, 580, 560), paint("#FBF7EE", 255 * (1 - dev)))
        c.restore()
        c.drawRect(skia.Rect.MakeXYWH(-290, -320, 580, 560), paint(OUT, stroke=4, cap=False))
        text(c, "Lubang · 2/1974", 0, 330, "ital", 40, "#2E3550", align="center")
    if a < 0.15:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("white", 255 * (1 - a / 0.15)))
    label_tag(c, "chụp ảnh chung làm bằng chứng", W / 2, 1180, pop(t, 82.2), size=32, anchor="center", bg="yellow")


def j4_refuse(c, t):
    c.save(); cam(c, 640, 760, 1.6); jungle(c, t)
    soldier2(c, 640, 1290, 1.2, t=t, pose="cross", look=math.sin((t - 83.3) * 9) * 0.9 if t < 84.8 else 0.0, mood="angry",
             talk=85.2 < t < 87.4, age=0.7, worn=0.8)
    c.restore()
    vignette(c, 170)
    bubble(c, 560, 410, "CHỈ ĐI", "KHI CÓ LỆNH CẤP TRÊN", t=t, t0=85.2)


def k1_home(c, t):
    c.save(); cam(c, 540, 900, 1.1); sea_sky(c, t)
    p = clamp((t - 87.75) / 1.45)
    with Xf(c, lerp(1300, -200, p), lerp(560, 700, p), 0, 1):
        c.scale(-1, 1); plane(c, 0, 0, 1.4)
    c.restore()
    with Xf(c, 300, 1150, -10 + 10 * math.sin(t * 3), 0.6, pop(t, 87.8)):
        fill_out(c, rrect_path(-120, -140, 240, 280, 6), "#FBF7EE")
        grad_rect(c, skia.Rect.MakeXYWH(-100, -120, 200, 200), "#5E7A4E", "#2F4A2A")
    label_tag(c, "bằng chứng về tới Nhật", W / 2, 330, pop(t, 87.8), size=34, anchor="center", bg="yellow")


def k2_taniguchi(c, t):
    c.save(); cam(c, 540, 900, lerp(1.3, 1.12, ease_out(clamp((t - 89.22) / 1.0)))); bookshop(c, t)
    civilian(c, lerp(-200, 300, clamp((t - 89.3) / 1.0)), 1290, 1.05, t=t, kind="official", walk=phase(t, 89.3) if t < 90.3 else None, look=0.6)
    civilian(c, 760, 1290, 1.1, t=t, kind="taniguchi", look=-0.5, mood="surprise" if t > 90.4 else "flat", flip=True)
    c.restore()
    vignette(c, 120)
    name_tag(c, 60, 340, "Thiếu tá Yoshimi Taniguchi", "chỉ huy cũ · nay bán sách", pop(t, 91.3, 0.4), size=42, role_size=28)


def k3_walk(c, t):
    c.save(); cam(c, lerp(700, 400, clamp((t - 94.12) / 4.8)), 880, 1.15); jungle(c, t)
    p = clamp((t - 94.6) / 4.2)
    civilian(c, lerp(1250, 450, p), 1250, 0.95, t=t, kind="taniguchi", walk=phase(t, 94.6), flip=True, look=0.5, prop="paper")
    civilian(c, lerp(1450, 650, p), 1250, 0.9, t=t, kind="suzuki", walk=phase(t, 94.8), flip=True, look=0.5)
    c.restore()
    blurred(c, 12, lambda: fg_leaves(c, t))
    vignette(c)
    chip(c, "9 · 3 · 1974", W / 2, 250, pop(t, 94.2))
    label_tag(c, "điểm hẹn trong rừng", W / 2, 340, pop(t, 97.4), size=34, anchor="center", bg="yellow")


def k4_salute(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#F2B36B", "#E9D9A6")
    rays(c, t, "#FFFFFF", 50, cy=600)
    c.save(); cam(c, 540, 700, 1.25)
    soldier2(c, 540, 1350, 1.3, t=t, pose="salute", mood="flat", age=0.7, worn=0.9)
    c.restore()
    kinetic(c, "NGHIÊM!", W / 2, 360, t, 99.1, size=110, per=0.05)


def k5_order(c, t):
    c.save(); cam(c, 540, 900, 1.15); jungle(c, t)
    soldier2(c, 330, 1250, 1.05, t=t, pose="attention", look=0.6, age=0.7, worn=0.9)
    civilian(c, 760, 1250, 1.05, t=t, kind="taniguchi", pose="read", talk=100.3 < t < 103.8, look=-0.5, flip=True)
    c.restore()
    blurred(c, 12, lambda: fg_leaves(c, t))
    vignette(c)
    bubble(c, 640, 400, "MIỄN TOÀN BỘ", "NHIỆM VỤ CHIẾN ĐẤU", t=t, t0=101.3, red2=False, tail=1)


def l1_radar(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#9FC9E6", "#E9D9A6")
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, 800), paint("#7A9A5A"))
    radar_dish(c, 800, 1150, 1.3, t)
    p = clamp((t - 104.2) / 2.8)
    soldier2(c, lerp(-150, 480, p), 1250, 0.95, t=t, walk=phase(t, 104.2) if p < 1 else None, look=0.6, age=0.7, worn=0.9)
    label_tag(c, "trạm radar trên đảo", 800, 1210, pop(t, 105.4), size=32, anchor="center", bg="yellow")
    kinetic(c, "RA TRÌNH DIỆN", W / 2, 330, t, 104.9, size=84, per=0.03)


def l2_weapons(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#6B4A30", "#3A2618")
    fill_out(c, rrect_path(60, 1090, 960, 60, 10), "#8A6542")
    p = pop(t, 107.4, 0.35)
    with Xf(c, 540, lerp(500, 1040, ease_out(p)), -4, 1, clamp(p * 3)):
        gun = skia.Path(); gun.moveTo(-380, 0); gun.lineTo(300, -20); gun.lineTo(380, -10); gun.lineTo(380, 20); gun.lineTo(-200, 30); gun.lineTo(-380, 60); gun.close()
        fill_out(c, gun, "#6B4A30")
        c.drawRect(skia.Rect.MakeXYWH(-40, -34, 300, 14), paint("#3A3632"))
    label_tag(c, "súng trường · vẫn bắn được", W / 2, 400, pop(t, 107.6), size=34, anchor="center", bg="yellow")
    if t > 109.0:
        n = int(lerp(0, 500, prog(t, 109.1, 110.3, lambda q: q)))
        text(c, f"{n}", W / 2, 680, "xbold", 160, "white", align="center", stroke=10, stroke_color="#1A120D")
        text(c, "viên đạn", W / 2, 760, "bold", 50, "#F4C430", align="center", stroke=5, stroke_color="#1A120D")
        for k in range(min(40, int(n / 12))):
            c.drawRoundRect(skia.Rect.MakeXYWH(120 + (k % 20) * 42, 980 - (k // 20) * 40, 14, 34), 7, 7, paint("#C9A55A"))
    for k in range(3):
        st = 110.0 + k * 0.15
        pg = clamp((t - st) / 0.35)
        if pg > 0:
            yy = lerp(600, 1040, ease_out(pg)) - 30 * abs(math.sin(pg * math.pi * 2)) * (1 - pg)
            with Xf(c, 760 + k * 100, yy, 0, 1):
                fill_out(c, oval_path(0, 0, 40, 50), "#4E5E3A"); fill_out(c, rrect_path(-14, -74, 28, 28, 6), "#3A3632", ow=5)


def sword(c, x, y, ang, s=1.0):
    with Xf(c, x, y, ang, s):
        blade = skia.Path(); blade.moveTo(0, -8); blade.quadTo(200, -26, 340, -8); blade.lineTo(340, 4); blade.quadTo(200, -10, 0, 8); blade.close()
        fill_out(c, blade, "#D6DCE0", ow=5)
        fill_out(c, rrect_path(-20, -26, 16, 52, 6), "#C9A55A", ow=5)
        fill_out(c, rrect_path(-130, -12, 112, 24, 10), "#3A2618", ow=5)


def l3_sword(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E2B77A", "#B98A52")
    for k in range(9):
        x = 60 + k * 125
        c.drawCircle(x, 1300, 70, paint("#5A3E26", 200)); c.drawRect(skia.Rect.MakeXYWH(x - 60, 1300, 120, 300), paint("#5A3E26", 200))
        ts = 111.3 + (k * 0.37) % 3.6
        if 0 < t - ts < 0.12:
            fl = paint("white", 230); fl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)); c.drawCircle(x + 20, 1250, 40, fl)
    chip(c, "11 · 3 · 1974", W / 2, 250, pop(t, 111.0))
    soldier2(c, 300, 1200, 0.95, t=t, pose="attention", look=0.6, age=0.7, worn=0.9)
    civilian(c, 780, 1200, 0.95, t=t, kind="president", pose="give" if t > 112.8 else "arms", flip=True, look=-0.6, mood="smile")
    pa = prog(t, 112.0, 113.2, ease_in_out)
    sword(c, lerp(360, 470, pa), lerp(940, 830, pa), -6, 1.0)
    name_tag(c, 60, 320, "Tổng thống Ferdinand Marcos", "Philippines", pop(t, 113.4, 0.4), size=40, role_size=28)
    note_label(c, "HOẠT HÌNH MINH HỌA", 640, 440, 1)


def l4_end(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#F2B36B", "#E9D9A6")
    rays(c, t, "#FFFFFF", 40, cy=900)
    c.drawCircle(540, 1150, 260, paint("#FFE7A8", 200))
    c.save(); cam(c, 540, 900, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-400, 1150, W + 800, 900), paint("#3E5A34"))
    for x in range(-300, W + 400, 160):
        frond(c, x, 1180, 240, -150 + (x % 5) * 12, "#2C4A2A")
    soldier2(c, 540, 1250, 1.0, t=t, look=-0.3, mood="sad", age=0.7, worn=0.9, flip=True)
    c.restore()
    c.save(); shake(c, t, 115.42, 18); stamp_big(c, "ÂN XÁ", 540, 420, t, 115.4, color="#1F3A5F", size=110, rot=-8); c.restore()
    label_tag(c, "vì ông vẫn tin chiến tranh còn tiếp diễn", W / 2, 1140, pop(t, 116.8), size=30, anchor="center", bg="yellow")
    pm = pop(t, 117.6, 0.4)
    if pm > 0:
        mascot(c, 920, lerp(1600, 1290, back_out(pm)), 0.5, "worried", look=(-1, -0.3), t=t)
    if t > 119.6:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 255 * prog(t, 119.6, 120.8, lambda q: q)))


SHOTS = [
    (0.00, 2.10, a1_dive), (2.10, 4.17, a2_canopy), (4.17, 5.85, b1_bush), (5.85, 7.20, b2_inserts), (7.20, 8.71, b3_believe),
    (8.71, 12.10, c1_bookshop), (12.10, 13.57, c3_fly), (13.57, 15.77, d_name),
    (15.77, 18.88, e1_route), (18.88, 21.44, e2_order), (21.44, 24.48, e3_retreat),
    (24.48, 27.43, f1_split), (27.43, 31.75, f2_leaflets), (31.75, 35.02, f3_fake), (35.02, 38.61, f4_swat),
    (38.61, 43.76, g1_raid), (43.76, 47.39, g2_candles), (47.39, 62.58, h_campfire),
    (62.58, 66.59, i1_tv), (66.59, 69.16, i2_dead), (69.16, 73.30, i3_alive),
    (73.30, 78.85, j1_suzuki), (78.85, 81.67, j2_meet), (81.67, 83.27, j3_photo), (83.27, 87.73, j4_refuse),
    (87.73, 89.22, k1_home), (89.22, 94.12, k2_taniguchi), (94.12, 98.98, k3_walk), (98.98, 100.21, k4_salute), (100.21, 104.10, k5_order),
    (104.10, 107.30, l1_radar), (107.30, 110.93, l2_weapons), (110.93, 115.28, l3_sword), (115.28, 120.90, l4_end),
]
# chuyển cảnh lia máy (whip pan) tại các mốc này; còn lại cắt thẳng
WHIP = {8.71, 15.77, 24.48, 62.58, 73.30, 87.73, 104.10, 13.57, 21.44, 94.12}
FADE = {38.61, 43.76, 47.39}
_surf = []


def _render(fn, t, k):
    while len(_surf) < 2:
        _surf.append(skia.Surface(W, H))
    cc = _surf[k].getCanvas(); cc.clear(skia.ColorBLACK)
    cc.save(); fn(cc, t); cc.restore()
    return _surf[k].makeImageSnapshot()


def draw_frame(c, t):
    for i, (a, b, fn) in enumerate(SHOTS):
        if i > 0 and (a in WHIP or a in FADE) and a - 0.14 <= t < a + 0.14:
            p = ease_in_out((t - (a - 0.14)) / 0.28)
            old = _render(SHOTS[i - 1][2], t, 0)
            new = _render(fn, t, 1)
            if a in FADE:
                c.drawImage(old, 0, 0)
                pp = skia.Paint(); pp.setAlphaf(p); c.drawImage(new, 0, 0, SAMP, pp)
            else:
                bl = skia.Paint(ImageFilter=skia.ImageFilters.Blur(60 * math.sin(p * math.pi) + 0.1, 0.1))
                c.saveLayer(None, bl)
                c.drawImage(old, -W * p, 0); c.drawImage(new, W * (1 - p), 0)
                c.restore()
            return
    for a, b, fn in SHOTS:
        if a <= t < b:
            fn(c, t)
            return
