"""Bảng dựng tập Pilecki (phong cách Midway v2). Mốc giây theo MP3, xem build/words.json (ước lượng)."""
import math
import skia
from lib import *  # noqa

PH = ROOT / "assets/photos"
CHIP_Y = 250
_assets = {}


def A(key):
    if key not in _assets:
        _assets[key] = Map() if key == "map" else Photo(PH / f"{key}.jpg")
    return _assets[key]


def caption(c, s, y=1225, size=27, x=60):
    text(c, s, x, y, "semi", size, "white", a=235, stroke=3, stroke_color="ink")


def mp(lon, lat, cam):
    return A("map").proj(lon, lat, cam)


def person(c, x, y, s=1.0, color="grey", a=255, ring=False):
    """Hình người giấy cắt (đứng), gốc ở chân."""
    with Xf(c, x, y, 0, s):
        shadow_begin(c, skia.Rect.MakeXYWH(-60, -200, 120, 220), dy=4, blur=4, a=60)
        p = paint(color, a)
        c.drawCircle(0, -150, 22, p)
        body = skia.Path()
        body.moveTo(-30, -120); body.lineTo(30, -120); body.lineTo(26, -40); body.lineTo(16, 0)
        body.lineTo(4, 0); body.lineTo(0, -40); body.lineTo(-4, 0); body.lineTo(-16, 0); body.lineTo(-26, -40); body.close()
        c.drawPath(body, p)
        c.restore()
        if ring:
            c.drawCircle(0, -80, 110, paint("yellow", 255, stroke=6))


# ------------------------------------------------------------------ máy quay bản đồ
CAM_PL = (19.6, 52.4, 105.0)    # Warsaw – Auschwitz, thấy bờ biển Baltic để định hướng
CAM_EU = (13.2, 50.5, 34.0)     # London – Warsaw, cả hai trong khung, chừa chỗ nhãn bên phải


# ------------------------------------------------------------------ CẢNH
def s01_roundup(c, t):
    ph = A("roundup_warsaw")
    z = lerp(1.0, 1.10, prog(t, 0, 4.5, lambda q: q))
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.55, 0.55, z)
    chip(c, "THÁNG 9 · 1940", W / 2, CHIP_Y, prog(t, 0.40, 0.75))
    label_tag(c, "WARSAW", 60, 1110, prog(t, 4.0, 4.3), size=40)
    caption(c, "Ảnh: một cuộc vây bắt ở Warsaw thời Đức chiếm đóng", 1190)


def s02_crowd(c, t):
    draw_paper(c)
    # đám đông bỏ chạy, một người đứng yên (4,5–6,4), rồi tự bước về phía xe (6,4–8,1)
    rngx = [130, 250, 370, 700, 820, 940, 200, 880, 470, 640]
    rngy = [900, 980, 930, 950, 900, 990, 1060, 1070, 1010, 1040]
    run = prog(t, 4.9, 6.2, ease_in_out)
    for i, (x, y) in enumerate(zip(rngx, rngy)):
        d = -1 if x < 540 else 1
        person(c, x + d * run * 420, y, 0.9, "grey", 255 * (1 - run * 0.85))
    # xe tải giấy cắt bên phải, hiện khi "bị bắt"
    pt = prog(t, 6.4, 6.9)
    if pt > 0:
        with Xf(c, lerp(1300, 820, ease_out(pt)), 1000, 0, 1):
            shadow_begin(c, skia.Rect.MakeXYWH(-320, -320, 640, 420))
            c.drawRect(skia.Rect.MakeXYWH(-240, -230, 330, 200), paint("#6B6455"))
            c.drawRect(skia.Rect.MakeXYWH(90, -170, 120, 140), paint("#575144"))
            c.drawCircle(-150, -20, 42, paint("ink")); c.drawCircle(130, -20, 42, paint("ink"))
            c.restore()
    walk = prog(t, 6.6, 7.9, ease_in_out)
    px = lerp(540, 690, walk)
    person(c, px, 1000, 1.05, "ink", 255, ring=t < 6.4)
    label_tag(c, "không trốn", 540, 720, prog(t, 5.3, 5.6) * (1 - prog(t, 6.3, 6.5)), size=36, anchor="center")
    label_tag(c, "cố ý để bị bắt", 640, 720, prog(t, 6.5, 6.8), size=36, anchor="center", bg="yellow")


def s03_map_route(c, t, t0=8.05, draw_at=8.95, chip_txt=None):
    m = A("map")
    cam = CAM_PL
    m.draw(c, cam)
    bx, by = mp(17.6, 55.6, cam)
    text(c, "BIỂN BALTIC", bx, by, "ital", 34, "ink", a=170, align="center")
    wx, wy = mp(*PLACES["warsaw"], cam)
    ax, ay = mp(*PLACES["auschwitz"], cam)
    pin(c, wx, wy, prog(t, t0, t0 + 0.3))
    label_tag(c, "WARSAW", wx + 26, wy - 44, prog(t, t0, t0 + 0.3), size=34)
    pa = prog(t, draw_at, draw_at + 0.3)
    r = path_partial(c, [(wx, wy), (ax, ay)], prog(t, draw_at - 0.35, draw_at + 0.3), paint("ink", 230, stroke=6, PathEffect=skia.DashPathEffect.Make([18, 12], 0)), curve=0.12)
    if r and prog(t, draw_at - 0.35, draw_at + 0.3) > 0.05:
        arrow_head(c, *r, size=26)
    pin(c, ax, ay, pa, color="white")
    label_tag(c, "AUSCHWITZ", ax - 26, ay + 60, pa, size=36, anchor="right", bg="ink", fg="white")
    if chip_txt:
        chip(c, chip_txt, W / 2, CHIP_Y, prog(t, t0 + 0.05, t0 + 0.4))


def s03a(c, t):
    s03_map_route(c, t, 8.05, 8.95)


def s04_portrait(c, t):
    ph = A("pilecki_color")
    z = lerp(1.08, 1.0, prog(t, 9.67, 10.1))
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.5, 0.33, z)
    name_tag(c, 60, 1010, "Witold Pilecki", "Sĩ quan Ba Lan · kháng chiến bí mật", prog(t, 10.35, 10.75), size=48, role_size=30)


def s05_gate(c, t):
    ph = A("gate_modern")
    z = lerp(1.0, 1.08, prog(t, 13.27, 15.6, lambda q: q))
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.40, 0.45, z)
    chip(c, "AUSCHWITZ", W / 2, CHIP_Y, prog(t, 13.4, 13.75))
    label_tag(c, "trại mở từ tháng 6/1940", 60, 1110, prog(t, 14.6, 14.9), size=36)
    caption(c, "Ảnh: cổng trại Auschwitz I, chụp sau này", 1190)


def wire_scene(c, t):
    """Hàng rào: bên ngoài / bên trong; nhiệm vụ 3 bước (15,6–24,2)."""
    draw_paper(c)
    # bên trong tối
    c.drawRect(skia.Rect.MakeXYWH(560, 300, 520, 900), paint("#2A2723"))
    text(c, "BÊN TRONG", 820, 360, "xbold", 34, "white", a=200, align="center")
    text(c, "BÊN NGOÀI", 270, 360, "xbold", 34, "grey", align="center")
    q = prog(t, 15.9, 16.4)
    if q > 0:
        text(c, "?", 820, 820, "xbold", 220, "grey", a=200 * q * (1 - prog(t, 21.0, 21.5)), align="center")
    # hàng rào: cột + dây thép gai
    pw = prog(t, 15.6, 16.2, lambda q_: q_)
    for k in range(9):
        y = 320 + k * 110
        if (k / 8) <= pw:
            c.drawRect(skia.Rect.MakeXYWH(548, y - 40, 22, 90), paint("#4A453C"))
    for j in range(5):
        x0 = 559 + (j - 2) * 6
        path_partial(c, [(x0, 300), (x0, 1200)], pw, paint("ink", 230, stroke=2.5))
        for k in range(int(28 * pw)):
            yy = 310 + k * 32
            c.drawLine(x0 - 7, yy - 6, x0 + 7, yy + 6, paint("ink", 200, stroke=2))
    # nhiệm vụ
    items = [("1", "VÀO TRONG", 19.85), ("2", "LẬP NHÓM KHÁNG CHIẾN", 20.55), ("3", "CHUYỂN TIN RA NGOÀI", 22.80)]
    pc = prog(t, 18.6, 19.0)
    if pc > 0:
        with Xf(c, 60, 1000, 0, 1, pc):
            card(c, 0, 0, 470, 210, "white", r=6)
            text(c, "NHIỆM VỤ", 26, 52, "xbold", 34, "ink")
            for i, (n, s, ts) in enumerate(items):
                pi = prog(t, ts, ts + 0.3)
                if pi > 0:
                    c.drawCircle(42, 92 + i * 44, 15, paint("yellow", 255 * pi))
                    text(c, n, 42, 101 + i * 44, "xbold", 22, "ink", a=255 * pi, align="center")
                    text(c, s, 70, 102 + i * 44, "bold", 26, "ink", a=255 * pi)
    # chấm vàng vào trong, nhóm, tin ra ngoài
    pin_ = prog(t, 19.85, 20.4, ease_in_out)
    if pin_ > 0:
        x = lerp(300, 760, pin_)
        c.drawCircle(x, 700, 16, paint("yellow"))
        c.drawCircle(x, 700, 16, paint("ink", stroke=3))
    nodes = [(880, 560), (960, 760), (720, 900), (900, 1000), (680, 560)]
    for i, (nx, ny) in enumerate(nodes):
        pn = prog(t, 20.6 + i * 0.18, 20.9 + i * 0.18)
        if pn > 0:
            c.drawLine(760, 700, lerp(760, nx, pn), lerp(700, ny, pn), paint("yellow", 200, stroke=3))
            c.drawCircle(nx, ny, 11 * pn, paint("yellow"))
    po = prog(t, 22.9, 23.7, ease_in_out)
    if po > 0:
        for k in range(3):
            pk = clamp(po * 1.4 - k * 0.2)
            if pk > 0:
                x = lerp(760, 200, pk)
                with Xf(c, x, 640 - k * 40, -6, 1, 1):
                    card(c, -32, -20, 64, 40, "white", r=3)
                    c.drawLine(-20, -6, 20, -6, paint("grey", stroke=3)); c.drawLine(-20, 6, 12, 6, paint("grey", stroke=3))


def s06_papers(c, t):
    draw_paper(c)
    p = prog(t, 24.2, 24.6)
    with Xf(c, 540, 700 + (1 - ease_out(p)) * 600, -3, 1, clamp(p * 2)):
        card(c, -330, -220, 660, 440, "#E9E2CF", r=8)
        c.drawRect(skia.Rect.MakeXYWH(-290, -170, 200, 250), paint("#C9BFA7"))
        person(c, -190, 70, 0.9, "#8E846F")
        text(c, "HỌ TÊN", -60, -130, "bold", 28, "grey")
        c.drawRect(skia.Rect.MakeXYWH(-60, -110, 330, 46), paint("ink", 230))
        text(c, "NGÀY SINH", -60, -20, "bold", 28, "grey")
        c.drawRect(skia.Rect.MakeXYWH(-60, 0, 230, 46), paint("ink", 230))
        for i in range(3):
            c.drawLine(-290, 120 + i * 30, 290, 120 + i * 30, paint("grey", 120, stroke=3))
    stamp(c, "GIẤY TỜ GIẢ", 560, 1010, prog(t, 24.55, 24.8), size=58, rot=-7)


def s07_two_days(c, t):
    draw_paper(c)
    label_tag(c, "doanh trại kỵ binh cũ · Warsaw", W / 2, 470, prog(t, 25.4, 25.7), size=36, anchor="center")
    days = [("19", "9"), ("20", "9"), ("21", "9")]
    for i, (d, mo) in enumerate(days):
        pk = prog(t, 25.45 + i * 0.12, 25.8 + i * 0.12)
        x = 290 + i * 250
        fill = "#D8CDB4" if i < 2 and t > 26.0 + i * 0.5 else "white"
        if pk > 0:
            with Xf(c, x, 760, 0, max(0.01, back_out(pk)), clamp(pk * 3)):
                card(c, -100, -100, 200, 200, fill, r=8)
                text(c, d, 0, 30, "xbold", 90, "ink", align="center")
                text(c, "/" + mo + "/1940", 0, 80, "semi", 28, "grey", align="center")
    chip(c, "HAI NGÀY BỊ GIAM", W / 2, 1010, prog(t, 26.0, 26.35), size=40)


def s08_transfer(c, t):
    s03_map_route(c, t, 28.75, 29.25, chip_txt="22 THÁNG 9 · 1940")


def s09_mugshot(c, t):
    draw_paper(c)
    ph = A("mugshot_4859")
    pe = prog(t, 30.29, 30.6)
    w = 1000
    h = ph.framed(c, W / 2, 640, w, rot=lerp(-3, -1, pe), scale=lerp(0.95, 1, pe))
    # khoanh số tù ở ảnh bên trái
    hx = W / 2 - w / 2 + 0.11 * w
    hy = 640 - h / 2 + 0.47 * h
    ph_ = prog(t, 31.9, 32.4)
    if ph_ > 0:
        r = skia.Rect.MakeXYWH(hx - 80, hy - 42, 160, 84)
        pth = skia.Path(); pth.addOval(r)
        pm = skia.PathMeasure(pth, False)
        d = skia.Path(); pm.getSegment(0, pm.getLength() * ph_, d, True)
        c.drawPath(d, paint("yellow", stroke=7))
    chip(c, "TÙ NHÂN SỐ 4859", W / 2, CHIP_Y, prog(t, 32.0, 32.35))
    caption(c, "Ảnh hồ sơ tù ở Auschwitz (Bảo tàng Auschwitz-Birkenau)", 900)
    # tên trong hồ sơ, đánh máy dần
    pn = prog(t, 33.25, 34.4, lambda q: q)
    if t > 33.1:
        with Xf(c, 120, 1010, 0):
            card(c, 0, 0, 840, 150, "white", r=4)
            text(c, "TÊN TRONG HỒ SƠ:", 30, 50, "mono", 30, "grey")
            w2 = text(c, typed("TOMASZ SERAFIŃSKI", pn), 30, 118, "mono", 54)
            ps = prog(t, 35.0, 35.4)
            if ps > 0:
                c.drawLine(24, 100, 24 + (w2 + 12) * ps, 100, paint("red", stroke=7))
        label_tag(c, "tên thật: WITOLD PILECKI", 960, 1210, prog(t, 35.5, 35.8), size=34, anchor="right", bg="yellow")


def s10_network(c, t):
    ph = A("aerial_1944")
    ph.blur_bg(c, 120)
    pe = prog(t, 36.33, 36.65)
    w = 1040
    h = ph.framed(c, W / 2, 680, w, rot=0, scale=lerp(0.96, 1, pe) + 0.004 * max(0, t - 36.65))
    caption(c, "Ảnh trinh sát của Đồng minh, 25/8/1944 (chú thích tiếng Anh)", 1160)
    x0, y0 = W / 2 - w / 2, 680 - h / 2
    pts = [(0.42, 0.30), (0.55, 0.28), (0.66, 0.33), (0.48, 0.45), (0.60, 0.47), (0.36, 0.52), (0.70, 0.55), (0.52, 0.62), (0.30, 0.38)]
    P = [(x0 + u * w, y0 + v * h) for u, v in pts]
    for i, (x, y) in enumerate(P):
        pk = prog(t, 36.6 + i * 0.16, 36.9 + i * 0.16)
        if pk > 0:
            c.drawCircle(x, y, 13 * back_out(pk), paint("yellow"))
            c.drawCircle(x, y, 13 * back_out(pk), paint("ink", stroke=3))
    pl = prog(t, 38.4, 40.0, lambda q: q)
    if pl > 0:
        order = [0, 1, 2, 4, 6, 7, 3, 5, 8, 0]
        path_partial(c, [P[k] for k in order], pl, paint("yellow", 230, stroke=4))
    label_tag(c, "người tin được", 70, 400, prog(t, 37.2, 37.5), size=34, bg="yellow")
    label_tag(c, "vị trí quan trọng", 70, 470, prog(t, 39.3, 39.6), size=34)
    # tin chuyển ra ngoài
    po = prog(t, 42.9, 44.2, lambda q: q)
    if po > 0:
        sx, sy = P[5]
        r = path_partial(c, [(sx, sy), (60, sy + 260)], po, paint("white", 230, stroke=5, PathEffect=skia.DashPathEffect.Make([14, 10], 0)), curve=0.1)
        if r:
            arrow_head(c, *r, size=24, color="white")
        label_tag(c, "tin ra ngoài", 70, sy + 330, prog(t, 43.2, 43.5), size=32, bg="ink", fg="white")


def s11_gestapo(c, t):
    draw_paper(c)
    chip(c, "1943", W / 2, CHIP_Y, prog(t, 44.55, 44.9))
    nodes = [(540, 640), (400, 560), (680, 560), (330, 720), (750, 720), (460, 840), (620, 840), (540, 470),
             (250, 600), (830, 600), (380, 950), (700, 950)]
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 7), (2, 7), (1, 8), (2, 9), (5, 10), (6, 11)]
    dead = {3: 48.75, 8: 48.95, 10: 49.15, 9: 49.3}
    for a, b in edges:
        al = 120 if (a in dead and t > dead[a]) or (b in dead and t > dead[b]) else 220
        c.drawLine(*nodes[a], *nodes[b], paint("ink", al, stroke=3))
    for i, (x, y) in enumerate(nodes):
        dd = i in dead and t > dead[i]
        c.drawCircle(x, y, 22, paint("#9A9284" if dd else ("yellow" if i == 0 else "white")))
        c.drawCircle(x, y, 22, paint("ink", stroke=3))
        if dd:
            k = prog(t, dead[i], dead[i] + 0.2)
            c.drawLine(x - 14 * k, y - 14 * k, x + 14 * k, y + 14 * k, paint("ink", stroke=4))
            c.drawLine(x + 14 * k, y - 14 * k, x - 14 * k, y + 14 * k, paint("ink", stroke=4))
    # vòng quét của Gestapo
    if t > 46.3:
        ang = (t - 46.3) * 120
        sh = skia.GradientShader.MakeSweep(540, 700, [skia.ColorSetARGB(0, 192, 57, 43), skia.ColorSetARGB(110, 192, 57, 43)], None)
        c.save()
        c.rotate(ang, 540, 700)
        p = skia.Paint(Shader=sh, AntiAlias=True)
        p.setAlphaf(prog(t, 46.3, 46.7))
        c.drawCircle(540, 700, 430, p)
        c.restore()
    label_tag(c, "GESTAPO TRUY LÙNG", W / 2, 1120, prog(t, 46.3, 46.6), size=40, anchor="center", bg="red", fg="white")


def s12_decide(c, t):
    draw_paper(c)
    ph = A("mugshot_4859")
    pe = prog(t, 49.75, 50.1)
    ph.framed(c, W / 2, 720, 720, rot=lerp(3, 1.5, pe), scale=lerp(0.95, 1, pe) + 0.006 * max(0, t - 50.1), crop=(0.345, 0.0, 0.665, 1.0))
    label_tag(c, "tự mình ra ngoài", 120, 1180, prog(t, 50.7, 51.0), size=38, bg="yellow")


def night_bg(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#1C2633"))
    c.drawCircle(860, 420, 46, paint("#E9E2CF", 230))
    c.drawRect(skia.Rect.MakeXYWH(0, 1060, W, 860), paint("#141B24"))


def fence_and_bakery(c, t, door_open=0.0, window=True):
    # hàng rào trại bên trái
    for k in range(7):
        x = 60 + k * 50
        c.drawRect(skia.Rect.MakeXYWH(x, 860, 8, 200), paint("#3A4655"))
    for j in range(4):
        c.drawLine(40, 890 + j * 45, 400, 890 + j * 45, paint("#55626F", stroke=2))
    # tháp canh
    c.drawRect(skia.Rect.MakeXYWH(150, 640, 16, 420), paint("#3A4655"))
    c.drawRect(skia.Rect.MakeXYWH(250, 640, 16, 420), paint("#3A4655"))
    c.drawRect(skia.Rect.MakeXYWH(120, 590, 176, 70), paint("#3A4655"))
    # lò bánh mì ngoài hàng rào
    c.drawRect(skia.Rect.MakeXYWH(520, 820, 380, 240), paint("#3B3530"))
    roof = skia.Path(); roof.moveTo(500, 820); roof.lineTo(710, 720); roof.lineTo(920, 820); roof.close()
    c.drawPath(roof, paint("#2E2925"))
    c.drawRect(skia.Rect.MakeXYWH(820, 690, 40, 90), paint("#2E2925"))
    if window:
        c.drawRect(skia.Rect.MakeXYWH(560, 880, 90, 70), paint("#E2B85A", 220))
    c.drawRect(skia.Rect.MakeXYWH(740, 930, 80 * (1 - door_open * 0.85), 130), paint("#6B5D4C"))
    if door_open > 0:
        c.drawRect(skia.Rect.MakeXYWH(740 + 80 * (1 - door_open * 0.85), 930, 80 * door_open * 0.85, 130), paint("#E2B85A", 120))


def s13_bakery(c, t):
    night_bg(c, t)
    fence_and_bakery(c, t)
    label_tag(c, "HÀNG RÀO TRẠI", 230, 560, prog(t, 52.4, 52.7), size=30, anchor="center")
    label_tag(c, "LÒ BÁNH MÌ", 710, 660, prog(t, 53.4, 53.7), size=34, anchor="center", bg="yellow")
    chip(c, "CA ĐÊM", W / 2, CHIP_Y, prog(t, 52.9, 53.25))


def s14_escape(c, t):
    night_bg(c, t)
    door = prog(t, 59.7, 60.1)
    fence_and_bakery(c, t, door_open=door)
    chip(c, "ĐÊM 26 THÁNG 4 · 1943", W / 2, CHIP_Y, prog(t, 55.1, 55.45))
    # dây điện thoại từ lò bánh mì ra cột
    cut = prog(t, 58.55, 58.75)
    c.drawRect(skia.Rect.MakeXYWH(1010, 700, 14, 360), paint("#3A4655"))
    if cut <= 0:
        c.drawLine(900, 840, 1017, 720, paint("#9AA6B2", stroke=3))
    else:
        c.drawLine(900, 840, 950, 790 + 40 * cut, paint("#9AA6B2", stroke=3))
        c.drawLine(1017, 720, 975, 770 + 50 * cut, paint("#9AA6B2", stroke=3))
    label_tag(c, "cắt dây điện thoại", 1000, 640, prog(t, 58.4, 58.7) * (1 - prog(t, 60.5, 60.8)), size=30, anchor="right", bg="yellow")
    # ba người chạy ra
    run = prog(t, 59.9, 61.3, lambda q: q)
    if t > 59.85:
        for i, col_ in enumerate(["yellow", "#B9AE96", "#B9AE96"]):
            x = 780 + run * (520 + i * 40) - i * 60
            person(c, x, 1060, 0.6, col_)
    label_tag(c, "ba người", 760, 1150, prog(t, 57.95, 58.25) * (1 - prog(t, 59.6, 59.9)), size=32, anchor="center")
    # súng bắn theo (theo lời ông kể)
    for k, ts in enumerate([62.3, 62.75, 63.1, 63.6]):
        a = t - ts
        if 0 < a < 0.18:
            c.drawCircle(208, 625, 30 * (1 - a / 0.18) + 10, paint("#F4D88A", 255 * (1 - a / 0.18)))
            c.drawLine(230, 640, 1080, 900 + k * 40, paint("#F4D88A", 160 * (1 - a / 0.18), stroke=2))
    label_tag(c, "theo lời Pilecki kể lại", W / 2, 1300 - 120, prog(t, 61.4, 61.7), size=32, anchor="center")


def s15_days(c, t):
    ph = A("gate_building_modern")
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.5, 0.5, 1.05 + 0.01 * (t - 64.58))
    c.drawRect(skia.Rect.MakeWH(W, H), paint("ink", 150))
    caption(c, "Ảnh: khu nhà trại Auschwitz I, chụp sau này", 1190)
    with Xf(c, W / 2, 620, 0, 1, prog(t, 64.65, 65.0)):
        text(c, "22.9.1940", 0, 0, "xbold", 92, "white", align="center")
    path_partial(c, [(W / 2, 660), (W / 2, 800)], prog(t, 65.1, 65.6), paint("yellow", stroke=8))
    with Xf(c, W / 2, 900, 0, 1, prog(t, 65.6, 65.95)):
        text(c, "27.4.1943", 0, 0, "xbold", 92, "yellow", align="center")
    label_tag(c, "trong Auschwitz", W / 2, 1020, prog(t, 66.0, 66.3), size=38, anchor="center")


def report_page(c, x, y, t, t_type, scale=1.0, alpha=1.0, rot=-1.5):
    with Xf(c, x, y, rot, scale, alpha):
        card(c, -330, -430, 660, 860, "white", r=4)
        text(c, "RAPORT", -290, -350, "mono", 46, "ink")
        note_label(c, "MINH HỌA", 170, -400, 1)
        p = prog(t, t_type, t_type + 1.0, lambda q: q)
        n = int(16 * p)
        rng_ = [0.92, 0.85, 0.97, 0.7, 0.9, 0.95, 0.6, 0.88, 0.93, 0.8, 0.96, 0.75, 0.9, 0.85, 0.94, 0.5]
        for i in range(n):
            c.drawRect(skia.Rect.MakeXYWH(-290, -290 + i * 40, 580 * rng_[i], 14), paint("grey", 150))


def s16_report(c, t):
    if t < 68.6:
        draw_paper(c)
        report_page(c, W / 2, 720, t, 67.45, scale=lerp(0.9, 1, prog(t, 67.38, 67.7)), alpha=prog(t, 67.38, 67.6))
        label_tag(c, "báo cáo về trại", 120, 1210, prog(t, 67.6, 67.9), size=36)
        return
    m = A("map")
    cam = drift_cam(CAM_EU, t, 68.6, 0.01)
    m.draw(c, cam)
    lx, ly = mp(*PLACES["london"], cam)
    wx, wy = mp(*PLACES["warsaw"], cam)
    pin(c, lx, ly, prog(t, 68.6, 68.9), color="white")
    label_tag(c, "LONDON", lx + 24, ly - 44, prog(t, 68.6, 68.9), size=34)
    pin(c, wx, wy, 1)
    label_tag(c, "BA LAN", wx - 24, wy - 44, 1, size=34, anchor="right")
    pf = prog(t, 68.7, 69.8, ease_in_out)
    r = path_partial(c, [(wx, wy), (lx, ly)], pf, paint("ink", 220, stroke=5, PathEffect=skia.DashPathEffect.Make([16, 10], 0)), curve=-0.18)
    if r and pf < 1:
        report_page(c, r[0][0], r[0][1] - 60, t, 0, scale=0.12, rot=0)
    if t > 69.8:
        report_page(c, lx + 110, ly - 130, t, 0, scale=0.14, rot=4, alpha=1 - 0.5 * prog(t, 70.6, 71.2))
        with Xf(c, lx + 110, ly - 220, 0, 1, prog(t, 70.6, 71.0)):
            text(c, "?", 0, 0, "xbold", 90, "ink", align="center")


def s17_postwar(c, t):
    m = A("map")
    cam = drift_cam(CAM_EU, t, 72.3, 0.008)
    m.draw(c, cam)
    # tô Ba Lan (biên giới sau 1945, gần với ngày nay)
    pa = prog(t, 73.3, 74.0)
    if pa > 0:
        for ring in RINGS_PL:
            path = skia.Path()
            for j, (lon, lat) in enumerate(ring):
                (path.moveTo if j == 0 else path.lineTo)(*mp(lon, lat, cam))
            path.close()
            c.drawPath(path, paint("red", 120 * pa))
            c.drawPath(path, paint("red", 220 * pa, stroke=3))
    chip(c, "SAU 1945", W / 2, CHIP_Y, prog(t, 72.35, 72.7))
    wx, wy = mp(*PLACES["warsaw"], cam)
    lx, ly = mp(*PLACES["london"], cam)
    label_tag(c, "chính quyền cộng sản", wx, wy + 110, pa, size=32, anchor="center", bg="red", fg="white")
    pin(c, lx, ly, prog(t, 75.2, 75.5), color="white")
    label_tag(c, "chính phủ lưu vong · LONDON", lx - 10, ly - 50, prog(t, 75.4, 75.7), size=30, bg="navy", fg="white")
    pr = prog(t, 78.2, 79.3, ease_in_out)
    if pr > 0:
        r = path_partial(c, [(wx - 360, wy + 330), (wx, wy)], pr, paint("navy", stroke=6), curve=0.1)
        if r:
            arrow_head(c, *r, size=26, color="navy")
        label_tag(c, "Pilecki trở về", wx - 380, wy + 400, prog(t, 78.3, 78.6), size=32, bg="yellow")


def s18_arrest(c, t):
    if t < 83.08:
        ph = A("mugshot_mbp_1947")
        ph.blur_bg(c, 120)
        pe = prog(t, 80.19, 80.5)
        ph.framed(c, W / 2, 700, 1000, rot=lerp(-2.5, -1, pe), scale=lerp(0.95, 1, pe) + 0.006 * max(0, t - 80.5))
        chip(c, "THÁNG 5 · 1947", W / 2, CHIP_Y, prog(t, 80.25, 80.6))
        caption(c, "Ảnh hồ sơ của Bộ Công an Ba Lan (MBP), 1947", 1100)
    else:
        ph = A("trial_1948")
        z = lerp(1.0, 1.06, prog(t, 83.08, 85.9, lambda q: q))
        ph.cover(c, skia.Rect.MakeWH(W, H), 0.30, 0.45, z)
        chip(c, "PHIÊN TÒA · 3/1948", W / 2, CHIP_Y, prog(t, 83.15, 83.5))
        label_tag(c, "Witold Pilecki", 60, 1030, prog(t, 83.4, 83.7), size=38)
        label_tag(c, "tội danh: gián điệp", 60, 1110, prog(t, 84.7, 85.0), size=36, bg="red", fg="white")


def s19_execution(c, t):
    if t < 88.36:
        draw_paper(c)
        ph = A("execution_protocol")
        pe = prog(t, 85.9, 86.2)
        w = 760
        h = ph.framed(c, W / 2, 740, w, rot=lerp(2.5, 1, pe), scale=lerp(0.95, 1, pe))
        x0, y0 = W / 2 - w / 2, 740 - h / 2
        highlight_box = prog(t, 86.6, 87.1)
        if highlight_box > 0:
            c.drawRect(skia.Rect.MakeXYWH(x0 + 0.07 * w, y0 + 0.215 * h, 0.86 * w * highlight_box, 0.04 * h), paint("yellow", 110))
        chip(c, "25 THÁNG 5 · 1948", W / 2, CHIP_Y, prog(t, 85.95, 86.3))
        caption(c, "Biên bản thi hành án tử hình, 25/5/1948", 1215)
    else:
        ph = A("mokotow_modern")
        z = lerp(1.0, 1.06, prog(t, 88.36, 91.0, lambda q: q))
        ph.cover(c, skia.Rect.MakeWH(W, H), 0.45, 0.55, z)
        label_tag(c, "NHÀ TÙ MOKOTÓW · WARSAW", 60, 1100, prog(t, 89.4, 89.7), size=36)
        caption(c, "Ảnh: nhà tù Mokotów, phố Rakowiecka, chụp sau này", 1190)


def s20_secret(c, t):
    draw_paper(c)
    # các lớp đất giấy cắt, không đánh dấu
    for k, colr in enumerate(["#B9AE96", "#A39881", "#8E846F", "#7A715E"]):
        c.drawRect(skia.Rect.MakeXYWH(0, 700 + k * 130, W, 140), paint(colr))
    with Xf(c, W / 2, 900, 0, 1, prog(t, 91.2, 91.6) * (1 - 0.6 * prog(t, 91.8, 92.4))):
        c.drawRoundRect(skia.Rect.MakeXYWH(-180, -40, 360, 80), 40, 40, paint("ink", 160, stroke=4, PathEffect=skia.DashPathEffect.Make([14, 10], 0)))
    label_tag(c, "chôn bí mật · không ghi dấu", W / 2, 560, prog(t, 91.3, 91.6), size=36, anchor="center")


def s21_innocent(c, t):
    draw_paper(c)
    pe = prog(t, 92.54, 92.9)
    A("pilecki_portrait").framed(c, W / 2, 700, 620, rot=lerp(-3, -1.5, pe), scale=lerp(0.95, 1, pe) + 0.006 * max(0, t - 92.9))
    chip(c, "1990", W / 2, CHIP_Y, prog(t, 92.6, 92.95))
    label_tag(c, "Tòa án Tối cao Ba Lan", W / 2, 1110, prog(t, 94.4, 94.7), size=36, anchor="center")
    stamp(c, "VÔ TỘI", 690, 960, prog(t, 95.6, 95.85), size=86, color="navy", rot=-8)


def s22_report(c, t):
    draw_paper(c)
    report_page(c, W / 2, 720, t, -10, scale=lerp(0.92, 1.0, prog(t, 96.51, 96.9)) + 0.006 * max(0, t - 96.9), alpha=prog(t, 96.51, 96.7))
    label_tag(c, "báo cáo vẫn còn", 120, 1210, prog(t, 97.6, 97.9), size=36, bg="yellow")


def s23_grave(c, t):
    ph = A("grave_symbolic")
    z = lerp(1.0, 1.08, prog(t, 98.83, 102.43, lambda q: q))
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.5, 0.35, z)
    label_tag(c, "mộ tượng trưng", 60, 1100, prog(t, 99.3, 99.6), size=38)
    caption(c, "Ảnh: bia mộ tượng trưng của Pilecki, chụp sau này", 1190)
    if t > 101.0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("ink", 255 * prog(t, 101.0, 102.4, lambda q: q)))


RINGS_PL = country_rings("Poland")

TIMELINE = [
    (0.00, 4.50, s01_roundup),
    (4.50, 8.05, s02_crowd),
    (8.05, 9.67, s03a),
    (9.67, 13.27, s04_portrait),
    (13.27, 15.60, s05_gate),
    (15.60, 24.18, wire_scene),
    (24.18, 25.34, s06_papers),
    (25.34, 28.70, s07_two_days),
    (28.70, 30.29, s08_transfer),
    (30.29, 36.33, s09_mugshot),
    (36.33, 44.51, s10_network),
    (44.51, 49.75, s11_gestapo),
    (49.75, 52.17, s12_decide),
    (52.17, 55.08, s13_bakery),
    (55.08, 64.58, s14_escape),
    (64.58, 67.38, s15_days),
    (67.38, 72.32, s16_report),
    (72.32, 80.19, s17_postwar),
    (80.19, 85.91, s18_arrest),
    (85.91, 91.03, s19_execution),
    (91.03, 92.54, s20_secret),
    (92.54, 96.51, s21_innocent),
    (96.51, 98.83, s22_report),
    (98.83, 102.50, s23_grave),
]


def draw_frame(c, t):
    for a, b, fn in TIMELINE:
        if a <= t < b:
            fn(c, t)
            break
