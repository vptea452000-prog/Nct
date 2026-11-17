"""Tập Neanderthal — chuỗi fact nguyên thủy, hoạt hình thuần, linh vật dẫn chuyện. Mốc giây theo MP3 (ước lượng).
Chữ trên hình viết trung tính ở hai câu cần thu lại (xem BAN_GIAO.md)."""
import math
import skia
from lib import *  # noqa
from toon import mascot, big_title, OUT, fill_out, rrect_path, oval_path, limb  # noqa
from toon2 import kinetic
from prehist import caveperson, helix, bone, puzzle_piece, person_icon, ORANGE, BLUE
from sets import grad_rect, vignette, blurred, frond


def pop(t, t0, d=0.3):
    return prog(t, t0, t0 + d)


def phase(t, t0, speed=7.0):
    return (t - t0) * speed


def shake(c, t, t0, amp=16, dur=0.35):
    if t0 <= t < t0 + dur:
        k = 1 - (t - t0) / dur
        c.translate(amp * k * math.sin((t - t0) * 90), amp * k * math.cos((t - t0) * 70))


def rays(c, t, color="#F4C430", a=60, cx=540, cy=760):
    for k in range(14):
        ang = k * math.pi / 7 + t * 0.12
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + 1800 * math.cos(ang), cy + 1800 * math.sin(ang)); p.lineTo(cx + 1800 * math.cos(ang + 0.18), cy + 1800 * math.sin(ang + 0.18)); p.close()
        c.drawPath(p, paint(color, a))


def lab_bg(c):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#DCE6EA", "#AFC3CC")
    for k in range(9):
        c.drawLine(k * 140, 0, k * 140, 1200, paint("#FFFFFF", 50, stroke=3))
    fill_out(c, rrect_path(-40, 1150, W + 80, 100, 8), "#E9E2CF")
    c.drawRect(skia.Rect.MakeXYWH(0, 1250, W, 700), paint("#8E9AA0"))


def ice_age(c, t, snow=0.0):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#BFD6E6", "#EAF1F4")
    for k, (yy, colr) in enumerate([(820, "#A7BCC9"), (920, "#8FA7B6")]):
        p = skia.Path(); p.moveTo(-100, 1400)
        for i in range(0, 14):
            x = -100 + i * 110
            p.lineTo(x, yy - 160 * abs(math.sin(i * 1.1 + k)))
        p.lineTo(W + 100, 1400); p.close()
        c.drawPath(p, paint(colr))
        for i in range(0, 14):
            x = -100 + i * 110
            pk = yy - 160 * abs(math.sin(i * 1.1 + k))
            c.drawCircle(x, pk + 18, 22, paint("white", 200))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, 800), paint("#F2F6F8"))
    for x in range(-50, W + 100, 180):
        tri = skia.Path(); tri.moveTo(x, 1150); tri.lineTo(x + 50, 980); tri.lineTo(x + 100, 1150); tri.close()
        fill_out(c, tri, "#3E5A4A", ow=4)
    if snow > 0:
        for k in range(90):
            x = (k * 137 + t * 40) % (W + 100) - 50
            y = (k * 211 + t * 160) % (H + 100) - 50
            c.drawCircle(x + 8 * math.sin(t + k), y, 4 + (k % 3), paint("white", 220 * snow))


def savanna(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#F2B36B", "#F6DDA8")
    c.drawCircle(820, 520, 120, paint("#FFE7A8", 230))
    c.drawRect(skia.Rect.MakeXYWH(0, 1100, W, 900), paint("#C9A54A"))
    for x in (160, 900):
        c.drawRect(skia.Rect.MakeXYWH(x - 14, 880, 28, 230), paint("#5A3E26"))
        c.drawOval(skia.Rect.MakeXYWH(x - 170, 820, 340, 90), paint("#5E7A3A")); c.drawOval(skia.Rect.MakeXYWH(x - 170, 820, 340, 90), paint(OUT, stroke=5))


def world_map(c, pr, rings_list, land="#E9DDB8", sea=("#7FB3D5", "#4F8FB8")):
    grad_rect(c, skia.Rect.MakeWH(W, H), *sea)
    for rings_ in rings_list:
        for ring in rings_:
            p = skia.Path()
            for j, (lon, lat) in enumerate(ring):
                (p.moveTo if j == 0 else p.lineTo)(*pr(lon, lat))
            p.close()
            c.drawPath(p, paint(land)); c.drawPath(p, paint(OUT, 160, stroke=3))


def proj(lon0, lon1, lat1, y0=260):
    sx = W / (lon1 - lon0)
    return lambda lon, lat: ((lon - lon0) * sx, y0 + (lat1 - lat) * sx)


ALL = None


def all_rings():
    global ALL
    if ALL is None:
        import shapefile
        sf = shapefile.Reader(str(ROOT / "assets/map/naturalearth_lowres.shp"))
        out = []
        for shp in sf.shapes():
            parts = list(shp.parts) + [len(shp.points)]
            for i in range(len(parts) - 1):
                ring = shp.points[parts[i]:parts[i + 1]]
                if len(ring) > 8:
                    out.append(ring)
        ALL = [out]
    return ALL


def neander_range(c, pr, p, t):
    """Vùng phân bố người Neanderthal (gần đúng): châu Âu → Trung Á → Altai."""
    if p <= 0:
        return
    pts = [(-9, 37), (-9, 43), (-2, 51), (10, 54), (25, 52), (40, 50), (55, 52), (70, 53), (85, 53), (88, 49), (75, 40), (60, 36),
           (45, 31), (35, 30), (28, 36), (15, 38), (2, 37)]
    path = skia.Path()
    for j, (lon, lat) in enumerate(pts):
        (path.moveTo if j == 0 else path.lineTo)(*pr(lon, lat))
    path.close()
    c.save()
    cx, cy = pr(30, 46)
    c.translate(cx, cy); c.scale(ease_out(p), ease_out(p)); c.translate(-cx, -cy)
    c.drawPath(path, paint(ORANGE, 110))
    c.drawPath(path, paint(ORANGE, 230, stroke=6, PathEffect=skia.DashPathEffect.Make([18, 10], t * 30)))
    c.restore()


def grid100(c, x0, y0, cell, n_orange, t, t0, extra=0.0, gap=8):
    for k in range(100):
        r, cc = divmod(k, 10)
        x, y = x0 + cc * (cell + gap), y0 + r * (cell + gap)
        p = pop(t, t0 + k * 0.008, 0.25)
        if p <= 0:
            continue
        colr = BLUE
        if k < int(n_orange):
            colr = ORANGE
        with Xf(c, x + cell / 2, y + cell / 2, 0, max(0.01, back_out(p))):
            c.drawRoundRect(skia.Rect.MakeXYWH(-cell / 2, -cell / 2, cell, cell), 8, 8, paint(colr))
            c.drawRoundRect(skia.Rect.MakeXYWH(-cell / 2, -cell / 2, cell, cell), 8, 8, paint(OUT, stroke=4))
            frac = n_orange - int(n_orange) if k == int(n_orange) else 0
            if frac > 0:
                c.drawRect(skia.Rect.MakeXYWH(-cell / 2, -cell / 2, cell * frac, cell), paint(ORANGE))
                c.drawRoundRect(skia.Rect.MakeXYWH(-cell / 2, -cell / 2, cell, cell), 8, 8, paint(OUT, stroke=4))


def meter(c, x, y, h, frac, colr, label, val, p):
    fill_out(c, rrect_path(x - 60, y - h, 120, h, 18), "#F6F1E4")
    hh = h * frac * ease_out(p)
    c.drawRoundRect(skia.Rect.MakeXYWH(x - 52, y - hh - 8, 104, hh), 14, 14, paint(colr))
    c.drawRoundRect(skia.Rect.MakeXYWH(x - 60, y - h, 120, h, ), 18, 18, paint(OUT, stroke=6))
    label_tag(c, label, x, y + 60, 1, size=34, anchor="center")
    text(c, val, x, y - h - 30, "xbold", 52, "ink", a=255 * p, align="center")


def sun(c, x, y, r, t):
    for k in range(12):
        a = k * math.pi / 6 + t * 0.6
        c.drawLine(x + (r + 20) * math.cos(a), y + (r + 20) * math.sin(a), x + (r + 60) * math.cos(a), y + (r + 60) * math.sin(a), paint("#F39C12", stroke=12))
    c.drawCircle(x, y, r, paint("#F4C430")); c.drawCircle(x, y, r, paint(OUT, stroke=6))


# ================================================================ CẢNH
def s01_hook(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#24476B", "#13263B")
    rays(c, t, "#FFFFFF", 14, cy=820)
    def col(i):
        return ORANGE if (i % 11 == 5 and t > 2.6) else BLUE
    helix(c, 540, 820, 1100, t, 1.0, rot=-12, colors=col, thick=1.2)
    pm = pop(t, 0.5, 0.4)
    mascot(c, 860, lerp(1600, 1300, back_out(pm)), 0.7, "smile" if t < 2.6 else "shock", t=t, arm="point" if t < 2.6 else "up")
    kinetic(c, "ADN CỦA BẠN", W / 2, 320, t, 0.4, size=96, per=0.03)
    if t > 2.6:
        g = paint(ORANGE, 120); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
        c.drawCircle(540, 820, 300 * pop(t, 2.6, 0.5), g)


def s02_reveal(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#C9A86A")
    rays(c, t, "#F4C430", 60, cy=820)
    c.save(); shake(c, t, 4.85, 16)
    p = pop(t, 4.8, 0.35)
    caveperson(c, 540, lerp(1700, 1260, back_out(p)), 1.25, t=t, kind="nea", look=0.0, mood="smile")
    c.restore()
    kinetic(c, "NEANDERTHAL", W / 2, 320, t, 4.85, size=100, color="#F4C430", per=0.04)
    label_tag(c, "một loài người đã tuyệt chủng", W / 2, 430, pop(t, 5.1), size=34, anchor="center")


def s03_range(c, t):
    pr = proj(-20, 100, 66, y0=360)
    world_map(c, pr, all_rings())
    neander_range(c, pr, pop(t, 6.2, 0.6), t)
    label_tag(c, "CHÂU ÂU", *pr(10, 58), pop(t, 6.9), size=32, anchor="center")
    label_tag(c, "CHÂU Á", *pr(80, 60), pop(t, 7.7), size=32, anchor="center")
    kinetic(c, "NƠI NGƯỜI NEANDERTHAL SỐNG", W / 2, 260, t, 6.0, size=52, per=0.02)
    caveperson(c, 860, 1300, 0.55, t=t, kind="nea", walk=phase(t, 6.0, 6), look=-0.5, flip=True)


def tree(c, t, p_split, p_label):
    with Xf(c, 540, 1300, 0, 1):
        c.drawLine(0, 0, 0, -320, paint(OUT, stroke=34)); c.drawLine(0, 0, 0, -320, paint("#8A6A44", stroke=24))
        q = ease_out(p_split)
        for side, colr in ((-1, BLUE), (1, ORANGE)):
            path = skia.Path(); path.moveTo(0, -320); path.quadTo(side * 40, -500, side * 260 * q, -720 * q - 320 * (1 - q))
            c.drawPath(path, paint(OUT, stroke=30)); c.drawPath(path, paint(colr, stroke=20))
        if p_label > 0:
            caveperson(c, -280, -720, 0.45, t=t, kind="sap", look=0.4, alpha=clamp(p_label * 2))
            caveperson(c, 280, -720, 0.45, t=t, kind="nea", look=-0.4, flip=True, alpha=clamp(p_label * 2))


def s04_branch(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#D4BE86")
    tree(c, t, prog(t, 8.6, 9.6), pop(t, 9.6, 0.4))
    label_tag(c, "NGƯỜI HIỆN ĐẠI", 260, 1360, pop(t, 9.8), size=32, anchor="center", bg=None or "white")
    label_tag(c, "NEANDERTHAL", 820, 1360, pop(t, 10.0), size=32, anchor="center", bg="yellow")
    kinetic(c, "HAI NHÁNH NGƯỜI", W / 2, 300, t, 10.7, size=80, per=0.03)


def s05_meet(c, t):
    if t < 13.68:
        pr = proj(-20, 70, 52, y0=320)
        world_map(c, pr, all_rings())
        neander_range(c, pr, 1, t)
        a = pr(35, 8); b = pr(42, 36)
        p = clamp((t - 12.0) / 1.5)
        r = path_partial(c, [a, b], p, paint(BLUE, stroke=12), curve=-0.2)
        if r:
            arrow_head(c, *r, size=36, color=BLUE)
        label_tag(c, "rời châu Phi", a[0] + 30, a[1] + 70, pop(t, 12.1), size=32, anchor="center", bg="white")
        return
    savanna(c, t) if False else ice_age(c, t * 0)
    pa = clamp((t - 13.7) / 0.8)
    caveperson(c, lerp(-150, 330, ease_out(pa)), 1260, 0.95, t=t, kind="sap", walk=phase(t, 13.7) if pa < 1 else None, look=0.6, mood="surprise" if t < 14.6 else "smile")
    caveperson(c, lerp(1230, 750, ease_out(pa)), 1260, 0.95, t=t, kind="nea", walk=phase(t, 13.7) if pa < 1 else None, look=-0.6, flip=True,
               mood="surprise" if t < 14.6 else "smile", female=True, spear=False)
    ph = pop(t, 14.7, 0.4)
    if ph > 0:
        with Xf(c, 540, 700 - 30 * math.sin(t * 3), 0, back_out(ph)):
            hp = skia.Path(); hp.moveTo(0, 60); hp.cubicTo(-140, -40, -60, -150, 0, -70); hp.cubicTo(60, -150, 140, -40, 0, 60); hp.close()
            fill_out(c, hp, "#E74C3C")
    kinetic(c, "GẶP NHAU", W / 2, 320, t, 13.75, size=96, per=0.04)


def s06_generations(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#F2E2B5", "#D9C38E")
    if t < 17.85:
        caveperson(c, 540, 1260, 1.25, t=t, kind="sap", child=True, spear=False, mood="smile", glow=pop(t, 16.4, 0.5), look=0.2)
        label_tag(c, "con chung", W / 2, 360, pop(t, 15.8), size=40, anchor="center", bg="yellow")
        return
    # dòng người qua các thế hệ; đốm sáng cam truyền qua từng người
    off = (t - 17.85) * 260
    for k in range(-2, 12):
        x = 540 + k * 240 - off
        if -200 < x < W + 200:
            caveperson(c, x, 1260, 0.62, t=t + k, kind="sap", spear=False, look=0.5, female=(k % 2 == 0),
                       glow=1.0 if k * 240 - off < 60 else 0.0)
    n = int(lerp(1, 2000, clamp((t - 18.0) / 3.0) ** 2))
    text(c, f"{n:,}".replace(",", ".") + " thế hệ", W / 2, 420, "xbold", 74, "ink", align="center")
    label_tag(c, "ADN Neanderthal được truyền tiếp", W / 2, 520, pop(t, 18.4), size=32, anchor="center", bg="yellow")
    note_label(c, "MINH HỌA", 60, 300, 1)


def s07_lab(c, t):
    lab_bg(c)
    if t < 23.8:
        bone(c, 400, 1080, 0.9, lerp(-30, -8, pop(t, 21.4, 0.5)))
        pb = clamp((t - 22.4) / 1.2)
        helix(c, 400 + 300 * pb, 1080 - 380 * pb, 320 * pb + 1, t, 0.8, colors=lambda i: ORANGE, alpha=int(255 * clamp(pb * 3)))
        label_tag(c, "xương người Neanderthal", 400, 1210, pop(t, 23.0), size=30, anchor="center")
        mascot(c, 880, 1180, 0.6, "think", look=(-1, 0.3), t=t)
        kinetic(c, "GIẢI MÃ ADN", W / 2, 320, t, 21.4, size=88, per=0.03)
        return
    helix(c, 320, 720, 760, t, 0.85, colors=lambda i: ORANGE)
    helix(c, 760, 720, 760, t, 0.85, colors=lambda i: ORANGE if i % 9 == 4 else BLUE)
    label_tag(c, "Neanderthal", 320, 1180, pop(t, 23.9), size=32, anchor="center", bg="yellow")
    label_tag(c, "người đang sống", 760, 1180, pop(t, 24.9), size=32, anchor="center")
    pc = pop(t, 25.5, 0.4)
    if pc > 0:
        for i in range(29):
            if i % 9 == 4:
                y = 720 - 380 + i * 26 * 0.85
                c.drawLine(380, y, 700, y, paint(ORANGE, 200 * pc, stroke=4, PathEffect=skia.DashPathEffect.Make([12, 10], t * 40)))
    kinetic(c, "SO SÁNH", W / 2, 300, t, 24.8, size=88, per=0.03)


def s08_percent(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#24476B", "#13263B")
    n = 0
    if t > 28.6:
        n = lerp(0, 1.5, clamp((t - 28.6) / 0.6))
    if t > 29.4:
        n = lerp(1.5, 2.0, clamp((t - 29.4) / 0.5))
    if t > 32.6:
        n = lerp(2.0, 2.6, clamp((t - 32.6) / 1.2))
    grid100(c, 135, 470, 74, n, t, 26.8)
    kinetic(c, "NGƯỜI NGOÀI CHÂU PHI", W / 2, 290, t, 27.6, size=60, per=0.02)
    lab = "1,5 – 2%" if t < 32.6 else "cao hơn một chút"
    with Xf(c, W / 2, 1260 - 30, 0, 1, pop(t, 29.2)):
        text(c, lab, 0, 0, "xbold", 72, "#F4C430", align="center", stroke=6, stroke_color="#1A120D")
    label_tag(c, "ADN Neanderthal", 160, 400, pop(t, 29.4), size=30, bg="yellow")


def s09_asia(c, t):
    if t < 40.88:
        grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#D4BE86")
        meter(c, 330, 1100, 520, 0.62, ORANGE, "CHÂU ÂU", "", pop(t, 36.2, 0.6))
        meter(c, 750, 1100, 520, 0.78, ORANGE, "ĐÔNG Á", "", pop(t, 38.6, 0.6))
        caveperson(c, 330, 520, 0.32, t=t, kind="nea", look=0.0, mood="smile", spear=False)
        label_tag(c, "quê hương Neanderthal", 330, 360, pop(t, 36.0), size=28, anchor="center", bg="yellow")
        if t > 39.7:
            text(c, "cao hơn!", 750, 500, "xbold", 64, "#C0392B", a=255 * pop(t, 39.7), align="center", stroke=5, stroke_color="#FBF7EE")
        pm = pop(t, 37.5, 0.3)
        mascot(c, 960, 1290, 0.5, "think" if t < 39.7 else "shock", look=(-1, -0.5), t=t)
        if t > 39.7:
            text(c, "?", 1000, 960, "xbold", 120, "ink", align="center")
        kinetic(c, "ĐIỀU LẠ", W / 2, 260, t, 35.0, size=96, per=0.04)
        return
    pr = proj(-25, 60, 40, y0=260)
    world_map(c, pr, all_rings())
    ax, ay = pr(20, 2)
    c.save(); shake(c, t, 44.4, 12)
    if t < 42.65:
        text(c, "0%", ax, ay, "xbold", 140, "ink", align="center", stroke=8, stroke_color="#FBF7EE")
        stamp(c, "TỪNG ĐƯỢC CHO LÀ", ax, ay + 140, pop(t, 41.2, 0.25), size=46, color="#5A524A", rot=-6)
    else:
        text(c, "~0,3%", ax, ay, "xbold", 140, ORANGE, align="center", stroke=8, stroke_color="#1A120D")
        label_tag(c, "nghiên cứu gần đây", ax, ay + 120, pop(t, 42.7), size=34, anchor="center", bg="yellow")
    c.restore()
    kinetic(c, "CHÂU PHI", W / 2, 260, t, 40.9, size=96, per=0.04)


def s10_puzzle(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#24476B", "#13263B")
    if t < 49.92:
        person_icon(c, 540, 900, 3.0, "#C9C3B4")
        puzzle_piece(c, 540, 860, 0.6, ORANGE, rot=10)
        text(c, "1%", 540, 560, "xbold", 120, "white", a=255 * pop(t, 46.7), align="center", stroke=6, stroke_color="#1A120D")
        text(c, "nghe thì ít…", 540, 650, "bold", 50, "#F4C430", a=255 * pop(t, 47.2), align="center")
        if t > 48.0:
            for k in range(8):
                x = 140 + (k % 4) * 270; y = 1150 + (k // 4) * 200
                person_icon(c, x, y, 1.1, "#C9C3B4", a=255 * pop(t, 48.0 + k * 0.06))
                puzzle_piece(c, x, y - 20, 0.28, ORANGE, rot=k * 47)
        return
    # ghép: các mảnh bay về một hình bộ gen
    fill_out(c, rrect_path(140, 420, 800, 760, 30), "#F6F1E4", a=60)
    pieces = 25
    filled = int(pieces * 0.2) if t > 54.7 else int(pieces * 0.2 * clamp((t - 50.4) / 4.0))
    for k in range(pieces):
        r, cc = divmod(k, 5)
        x, y = 220 + cc * 160, 500 + r * 150
        if k < filled:
            q = clamp((t - 50.4 - k * 0.6) / 0.6)
            sx, sy = 540 + 500 * math.cos(k * 2.3), 1500 + 200 * math.sin(k)
            puzzle_piece(c, lerp(sx, x, ease_out(q)), lerp(sy, y, ease_out(q)), 0.9, ORANGE, rot=(1 - q) * 120)
        else:
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 50, y - 50, 100, 100), 10, 10, paint("#FFFFFF", 50, stroke=4))
    text(c, "≈ 1/5 bộ gen", 540, 1290, "xbold", 70, "#F4C430", a=255 * pop(t, 55.0), align="center", stroke=6, stroke_color="#1A120D")
    chip(c, "NGHIÊN CỨU 2014", W / 2, 330, pop(t, 52.0), size=40)


def s11_active(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#D4BE86")
    if t < 61.42:
        wig = 18 * math.sin(t * 6)
        helix(c, 540, 760, 900, t, 0.9, rot=wig, colors=lambda i: ORANGE if i % 7 == 3 else BLUE, speed=3)
        kinetic(c, "KHÔNG NẰM IM", W / 2, 270, t, 57.1, size=88, per=0.04)
        if t > 59.0:
            label_tag(c, "DA", 230, 1150, pop(t, 60.4), size=40, anchor="center", bg="yellow")
            label_tag(c, "TÓC", 850, 1150, pop(t, 60.8), size=40, anchor="center", bg="yellow")
            with Xf(c, 230, 1000, 0, back_out(pop(t, 60.4))):
                c.drawCircle(0, 0, 80, paint("#E2B48C")); c.drawCircle(0, 0, 80, paint(OUT, stroke=6))
            with Xf(c, 850, 1000, 0, back_out(pop(t, 60.8))):
                for k in range(6):
                    p = skia.Path(); p.moveTo(-60 + k * 24, 70); p.quadTo(-80 + k * 24 + 30 * math.sin(t * 3 + k), -10, -40 + k * 24, -80)
                    c.drawPath(p, paint("#5A3E2A", stroke=10))
        return
    ice_age(c, t, snow=pop(t, 61.5, 1.0))
    caveperson(c, 540, 1260, 1.05, t=t, kind="sap", look=0.0, mood="smile", glow=1.0, arm="up" if t > 64.5 else "down")
    label_tag(c, "môi trường mới, lạnh hơn", W / 2, 360, pop(t, 62.0), size=34, anchor="center", bg="white")
    label_tag(c, "giả thuyết của một số nhà khoa học", W / 2, 440, pop(t, 61.6), size=28, anchor="center", bg="yellow")


def s12_disease(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#3A2418", "#1C110B")
    kinetic(c, "NHƯNG…", W / 2, 300, t, 65.9, size=110, per=0.05, color="#E9E2CF")
    p1 = pop(t, 68.0, 0.35)
    if p1 > 0:
        with Xf(c, 300, 840, 0, back_out(p1)):
            drop = skia.Path(); drop.moveTo(0, -150); drop.quadTo(120, 20, 0, 110); drop.quadTo(-120, 20, 0, -150); drop.close()
            fill_out(c, drop, "#C0392B")
            text(c, "đường", 0, 30, "xbold", 38, "white", align="center")
        label_tag(c, "tiểu đường", 300, 1040, p1, size=34, anchor="center", bg="yellow")
    p2 = pop(t, 68.9, 0.35)
    if p2 > 0:
        with Xf(c, 780, 840, 0, back_out(p2)):
            gut = skia.Path(); gut.moveTo(-120, -80)
            for k in range(6):
                gut.quadTo(-120 + k * 48 + 24, -80 + (60 if k % 2 else -60), -120 + (k + 1) * 48, -80)
            gut.moveTo(120, 0)
            for k in range(6):
                gut.quadTo(120 - k * 48 - 24, 0 + (60 if k % 2 else -60), 120 - (k + 1) * 48, 0)
            c.drawPath(gut, paint(OUT, stroke=40)); c.drawPath(gut, paint("#E8A0A0", stroke=28))
        label_tag(c, "bệnh Crohn (ruột)", 780, 1040, p2, size=34, anchor="center", bg="yellow")
    label_tag(c, "gắn với nguy cơ", W / 2, 1150, pop(t, 66.8), size=32, anchor="center")


def s13_sunburn(c, t):
    if t < 72.78:
        grad_rect(c, skia.Rect.MakeWH(W, H), "#24476B", "#13263B")
        n = int(lerp(0, 112000, clamp((t - 70.0) / 1.8) ** 0.7))
        cols, rows = 12, 9
        shown = int(cols * rows * clamp((t - 70.0) / 1.8))
        for k in range(shown):
            r, cc = divmod(k, cols)
            person_icon(c, 120 + cc * 76, 640 + r * 70, 0.55, "#C9C3B4")
        text(c, f"{n:,}".replace(",", ".") + " người", W / 2, 470, "xbold", 80, "white", align="center", stroke=6, stroke_color="#1A120D")
        label_tag(c, "nghiên cứu ở Anh", W / 2, 560, pop(t, 70.4), size=34, anchor="center", bg="yellow")
        return
    grad_rect(c, skia.Rect.MakeWH(W, H), "#7FC4E8", "#E9F4F8")
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, 800), paint("#F2DDA4"))
    c.drawRect(skia.Rect.MakeXYWH(0, 1050, W, 110), paint("#3F9FCF"))
    sun(c, 860, 470, 90, t)
    red = pop(t, 75.6, 0.8)
    with Xf(c, 380, 1300, 0, 1):
        pass
    mascot(c, 400, 1300, 0.9, "worried" if t > 75.5 else "smile", t=t, arm="down")
    if red > 0:
        g = paint("#E74C3C", 130 * red); c.drawCircle(400, 1150, 95, g)
        for k in range(5):
            st = 75.8 + k * 0.2; a = t - st
            if a > 0:
                c.drawCircle(400 + 60 * math.cos(k), 1050 - a * 80, 8, paint("#FFFFFF", 200 * clamp(1 - a)))
    label_tag(c, "biến thể gen Neanderthal", W / 2, 360, pop(t, 72.9), size=34, anchor="center", bg="yellow")
    label_tag(c, "liên quan: dễ cháy nắng khi còn nhỏ", W / 2, 440, pop(t, 75.4), size=32, anchor="center")
    note_label(c, "MINH HỌA", 60, 520, 1)


def s14_gone(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#8FA7B6", "#D6E2E8")
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, 800), paint("#BFCCD2"))
    p = clamp((t - 77.3) / 3.0)
    caveperson(c, lerp(540, 900, p), 1260, lerp(1.0, 0.7, p), t=t, kind="nea", walk=phase(t, 77.3, 5), look=0.6, alpha=1 - 0.8 * p, female=False)
    fog = paint("#FFFFFF", 150 * p); fog.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 80))
    c.drawRect(skia.Rect.MakeXYWH(600, 600, 600, 900), fog)
    with Xf(c, 250, 760, -4, 1, pop(t, 79.2)):
        fill_out(c, rrect_path(-150, -110, 300, 220, 8), "#E9E2CF")
        c.drawLine(-100, -40, 100, -40, paint("#C9C3B4", stroke=8)); c.drawLine(-100, 10, 60, 10, paint("#C9C3B4", stroke=8))
        stamp(c, "KHÔNG CHỮ VIẾT", 0, 0, pop(t, 79.4, 0.25), size=34, color="#5A524A", rot=-10)
    kinetic(c, "BIẾN MẤT", W / 2, 300, t, 77.5, size=100, per=0.05, color="#2E2A25", stroke_color="#F6F1E4")


def s15_inside(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#24476B", "#0B1622")
    z = math.exp(lerp(math.log(3.2), math.log(0.6), ease_in_out(clamp((t - 80.3) / 3.6))))
    c.save(); c.translate(540, 820); c.scale(z, z)
    c.drawCircle(0, 0, 160, paint("#F6C9C0", 200)); c.drawCircle(0, 0, 160, paint(OUT, stroke=6))
    c.drawCircle(0, 0, 60, paint("#C98A80")); c.drawCircle(0, 0, 60, paint(OUT, stroke=5))
    g = paint(ORANGE, 200); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
    c.drawCircle(18, -8, 16, g); c.drawCircle(18, -8, 7, paint("#FFD27A"))
    for k in range(30):
        a = k * 0.7; r = 260 + (k % 5) * 90
        x, y = r * math.cos(a), r * math.sin(a)
        c.drawCircle(x, y, 60, paint("#F6C9C0", 120)); c.drawCircle(x, y, 60, paint(OUT, 120, stroke=4))
        c.drawCircle(x + 6, y - 4, 6, paint(ORANGE, 200))
    c.restore()
    if t > 82.0:
        n = int(lerp(1, 6, clamp((t - 82.0) / 1.5)))
        text(c, f"hàng tỉ người", W / 2, 1180, "xbold", 74, "#F4C430", a=255 * pop(t, 82.0), align="center", stroke=6, stroke_color="#1A120D")
    kinetic(c, "VẪN CÒN", W / 2, 300, t, 80.4, size=110, per=0.05)
    pm = pop(t, 83.0, 0.4)
    if pm > 0:
        mascot(c, 880, lerp(1600, 1300, back_out(pm)), 0.55, "smile", t=t, arm="up")
    if t > 84.3:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 255 * prog(t, 84.3, 85.2, lambda q: q)))


SHOTS = [
    (0.00, 4.80, s01_hook), (4.80, 5.97, s02_reveal), (5.97, 8.55, s03_range), (8.55, 11.96, s04_branch),
    (11.96, 15.69, s05_meet), (15.69, 21.29, s06_generations), (21.29, 26.78, s07_lab), (26.78, 34.95, s08_percent),
    (34.95, 46.70, s09_asia), (46.70, 57.00, s10_puzzle), (57.00, 65.87, s11_active), (65.87, 69.92, s12_disease),
    (69.92, 77.32, s13_sunburn), (77.32, 80.29, s14_gone), (80.29, 85.30, s15_inside),
]
WHIP = {4.80, 8.55, 11.96, 21.29, 26.78, 34.95, 46.70, 57.00, 69.92}
FADE = {65.87, 77.32, 80.29}
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
