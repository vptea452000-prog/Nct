"""Bảng dựng tập Garbo (phong cách Midway v2). Mốc giây theo MP3, xem build/words.json (ước lượng).
Màu: đỏ = phía Đức, navy = phía Anh, vàng = chi tiết đáng nhìn."""
import math
import skia
from lib import *  # noqa

PH = ROOT / "assets/photos"
CHIP_Y = 250
_assets = {}

PLACES.update({"lisbon": (-9.14, 38.72), "madrid": (-3.70, 40.42), "glasgow": (-4.25, 55.86),
               "normandy": (-0.75, 49.35), "calais": (1.86, 50.95), "dover": (1.31, 51.13)})


def A(key):
    if key not in _assets:
        _assets[key] = Map() if key == "map" else Photo(PH / f"{key}.jpg")
    return _assets[key]


def caption(c, s, y=1225, size=27, x=60):
    text(c, s, x, y, "semi", size, "white", a=235, stroke=3, stroke_color="ink")


def mp(lon, lat, cam):
    return A("map").proj(lon, lat, cam)


def pop_in(t, t0, d=0.3):
    return prog(t, t0, t0 + d)


def map_pin(c, cam, key, label, t, t0, side="right", color="yellow", bg="white", fg="ink", size=32):
    x, y = mp(*PLACES[key], cam)
    p = pop_in(t, t0)
    pin(c, x, y, p, color=color)
    if side == "right":
        label_tag(c, label, x + 24, y - 44, p, size=size, bg=bg, fg=fg)
    elif side == "left":
        label_tag(c, label, x - 24, y - 44, p, size=size, anchor="right", bg=bg, fg=fg)
    else:
        label_tag(c, label, x, y + 58, p, size=size, anchor="center", bg=bg, fg=fg)
    return x, y


def tape(c, x0, y0, x1, y1, p, t, color="ink"):
    """Dải băng điện báo chạy chấm–gạch giữa hai điểm."""
    if p <= 0:
        return
    L = math.hypot(x1 - x0, y1 - y0)
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    with Xf(c, x0, y0, ang):
        w = L * clamp(p)
        card(c, 0, -26, w, 52, "white", r=3, shadow=True)
        pat = [1, 0, 3, 0, 1, 0, 1, 0, 3, 0, 3, 0, 0, 1, 0, 3, 0, 1, 0, 0]
        x = 14 - (t * 60) % 40
        k = 0
        while x < w - 14:
            u = pat[k % len(pat)]
            if u == 1 and x > 8:
                c.drawCircle(x, 0, 6, paint(color))
            elif u == 3 and x > 8:
                c.drawRoundRect(skia.Rect.MakeXYWH(x - 6, -5, 26, 10), 5, 5, paint(color))
            x += 22 if u != 3 else 34
            k += 1


# ------------------------------------------------------------------ máy quay bản đồ
CAM_IB = (-4.5, 45.3, 52.0)     # Bán đảo Iberia – Anh: London và Lisbon đều trong vùng 200–1250 px
CAM_CH = (0.6, 50.2, 210.0)     # eo biển Manche: Normandy – Pas-de-Calais


# ------------------------------------------------------------------ CẢNH
def s01_medals(c, t):
    draw_paper(c)
    chip(c, "THẾ CHIẾN II", W / 2, CHIP_Y, pop_in(t, 0.55))
    p1 = pop_in(t, 2.35, 0.4)
    if p1 > 0:
        A("iron_cross").framed(c, 290, 690, 380, rot=lerp(-8, -3, ease_out(p1)), scale=lerp(0.85, 1, ease_out(p1)), alpha=clamp(p1 * 2))
        label_tag(c, "ĐỨC", 290, 1035, p1, size=40, anchor="center", bg="red", fg="white")
    p2 = pop_in(t, 4.95, 0.4)
    if p2 > 0:
        A("mbe").framed(c, 800, 690, 400, rot=lerp(8, 3, ease_out(p2)), scale=lerp(0.85, 1, ease_out(p2)), alpha=clamp(p2 * 2))
        label_tag(c, "ANH", 800, 1035, p2, size=40, anchor="center", bg="navy", fg="white")
    # cùng một chuỗi bức điện
    tape(c, 300, 1135, 800, 1135, prog(t, 6.95, 7.6), t)
    label_tag(c, "cùng một chuỗi bức điện", W / 2, 1210, pop_in(t, 7.1), size=34, anchor="center", bg="yellow")


def s03_pujol(c, t):
    draw_paper(c)
    pe = pop_in(t, 8.15, 0.35)
    A("pujol_beard").framed(c, W / 2, 680, 640, rot=lerp(-5, -2, pe), scale=lerp(0.94, 1, pe) + 0.006 * max(0, t - 8.5))
    name_tag(c, 60, 1060, "Juan Pujol", "người Tây Ban Nha · ghét Hitler", pop_in(t, 8.75, 0.4), size=50, role_size=32)


def desk_card(c, x, y, title, colr, p):
    if p <= 0:
        return
    with Xf(c, x, y, 0, max(0.01, back_out(p)), clamp(p * 3)):
        card(c, -200, -150, 400, 300, "white", r=8)
        c.drawRect(skia.Rect.MakeXYWH(-200, -150, 400, 64), paint(colr))
        text(c, title, 0, -105, "xbold", 34, "white", align="center")
        for i in range(4):
            c.drawLine(-160, -40 + i * 40, 120 - (i % 2) * 70, -40 + i * 40, paint("grey", 120, stroke=6))


def s04_apply(c, t):
    draw_paper(c)
    chip(c, "1941", W / 2, CHIP_Y, pop_in(t, 11.2))
    desk_card(c, 290, 600, "NGƯỜI ANH", "navy", pop_in(t, 12.9))
    desk_card(c, 790, 600, "TÌNH BÁO ĐỨC", "red", pop_in(t, 17.2))
    stamp(c, "TỪ CHỐI", 290, 640, prog(t, 14.85, 15.05), size=56, color="navy", rot=-10)
    # ảnh Pujol đi từ bàn này sang bàn kia
    mv = prog(t, 15.8, 16.8, ease_in_out)
    x = lerp(290, 790, mv)
    y = 1000 - 60 * math.sin(math.pi * mv)
    A("pujol_young").framed(c, x, y, 190, rot=lerp(-6, 6, mv), alpha=pop_in(t, 12.5))
    label_tag(c, "đổi cách", W / 2, 1180, prog(t, 15.9, 16.2) * (1 - prog(t, 17.6, 17.8)), size=34, anchor="center", bg="yellow")
    label_tag(c, "hứa sang Anh do thám", 790, 1180, pop_in(t, 18.0), size=32, anchor="center", bg="red", fg="white")


def s05_lisbon(c, t):
    m = A("map")
    cam = drift_cam(CAM_IB, t, 18.46, 0.008)
    m.draw(c, cam)
    mx, my = map_pin(c, cam, "madrid", "MADRID", t, 18.46, "right")
    lx, ly = mp(*PLACES["london"], cam)
    pr = prog(t, 18.6, 19.6, ease_in_out)
    r = path_partial(c, [(mx, my), (lx, ly)], pr, paint("red", 220, stroke=6, PathEffect=skia.DashPathEffect.Make([18, 12], 0)), curve=-0.15)
    if r and 0.05 < pr:
        arrow_head(c, *r, size=24, color="red")
    map_pin(c, cam, "london", "LONDON", t, 19.2, "right", color="white")
    # không sang Anh
    px = prog(t, 20.4, 20.7)
    if px > 0:
        cx, cy = (mx + lx) / 2 - 40, (my + ly) / 2
        c.drawLine(cx - 50 * px, cy - 50 * px, cx + 50 * px, cy + 50 * px, paint("ink", stroke=12))
        c.drawLine(cx + 50 * px, cy - 50 * px, cx - 50 * px, cy + 50 * px, paint("ink", stroke=12))
    sx, sy = map_pin(c, cam, "lisbon", "LISBON · BỒ ĐÀO NHA", t, 21.85, "right", bg="yellow", size=30)
    # báo cáo gửi tình báo Đức (trạm Madrid), giả như từ London
    pf = prog(t, 23.5, 24.4, ease_in_out)
    if pf > 0:
        r2 = path_partial(c, [(sx, sy), (mx, my)], pf, paint("ink", 200, stroke=4), curve=0.25)
        ex, ey = r2[0]
        # phong bì bay lên đặt phía trên-phải Madrid, không che nhãn
        ex, ey = lerp(ex, mx + 170, pf), lerp(ey, my - 80, pf)
        with Xf(c, ex, ey - 70, -6):
            card(c, -110, -62, 220, 124, "#F3EBD8", r=4)
            c.drawLine(-110, -62, 0, 4, paint("grey", 150, stroke=3)); c.drawLine(110, -62, 0, 4, paint("grey", 150, stroke=3))
            pst = prog(t, 24.9, 25.15)
            if pst > 0:
                with Xf(c, 50, 26, -14, lerp(1.6, 1, pst), clamp(pst * 2)):
                    c.drawCircle(0, 0, 40, paint("red", 220, stroke=4))
                    text(c, "LONDON", 0, 8, "xbold", 20, "red", align="center")
    label_tag(c, "như thể đang ở London", mx + 170, my - 250, pop_in(t, 25.0), size=32, anchor="center", bg="yellow")


def s06_sources(c, t):
    draw_paper(c)
    label_tag(c, "TƯ LIỆU CỦA PUJOL", W / 2, 360, pop_in(t, 26.3), size=40, anchor="center")
    items = [(27.3, "sách du lịch", 290, 620), (28.25, "bản đồ", 790, 620), (28.95, "bảng giờ tàu", 290, 960), (29.75, "phim thời sự", 790, 960)]
    for i, (ts, lab, x, y) in enumerate(items):
        p = pop_in(t, ts - 0.15, 0.35)
        if p <= 0:
            continue
        with Xf(c, x, y, [-4, 3, 2, -3][i], max(0.01, back_out(p)), clamp(p * 3)):
            if i == 0:  # sách
                card(c, -130, -160, 260, 320, "#7B3B2E", r=8)
                c.drawRect(skia.Rect.MakeXYWH(-100, -110, 200, 70), paint("#E9D9A6"))
                text(c, "GUIDE", 0, -62, "xbold", 40, "#7B3B2E", align="center")
                text(c, "BRITAIN", 0, 40, "xbold", 34, "#E9D9A6", align="center")
            elif i == 1:  # bản đồ gấp
                for k in range(3):
                    card(c, -150 + k * 100, -120, 100, 240, ["#DCE4D2", "#E6E0C8", "#D6E0DF"][k], r=2, shadow=k == 0)
                c.drawLine(-120, 60, -40, -20, paint("red", stroke=5)); c.drawLine(-40, -20, 60, 30, paint("red", stroke=5)); c.drawLine(60, 30, 120, -70, paint("red", stroke=5))
            elif i == 2:  # bảng giờ tàu
                card(c, -150, -150, 300, 300, "white", r=4)
                text(c, "TIMETABLE", -120, -100, "mono", 30, "ink")
                for k in range(5):
                    text(c, f"{8 + k:02d}.{(k * 17) % 60:02d}", -120, -40 + k * 42, "mono", 30, "grey")
                    c.drawLine(-10, -50 + k * 42, 120, -50 + k * 42, paint("grey", 120, stroke=4))
            else:  # cuộn phim
                c.drawCircle(0, 0, 130, paint("#3A3632"))
                for k in range(6):
                    a = k * math.pi / 3 + t * 2
                    c.drawCircle(70 * math.cos(a), 70 * math.sin(a), 26, paint("#E6DCC5"))
                c.drawCircle(0, 0, 22, paint("#E6DCC5"))
        label_tag(c, lab, x, y + 200, p, size=34, anchor="center", bg="yellow" if i == 0 else "white")


def s07_glasgow(c, t):
    draw_paper(c)
    p = pop_in(t, 30.62, 0.35)
    w, h = 940, 520
    with Xf(c, 70, 330 + (1 - ease_out(p)) * 500, -1.0, 1, clamp(p * 2)):
        card(c, 0, 0, w, h, "white", r=4)
        text(c, "BÁO CÁO GỬI ĐỨC · \"TỪ LONDON\"", 36, 58, "mono", 28, "grey")
        note_label(c, "DIỄN Ý", w - 150, 26, 1)
        c.drawLine(36, 86, w - 36, 86, paint("grey", 120, stroke=2))
        lines = ["Ở GLASGOW CÓ NHỮNG NGƯỜI", "CHỊU LÀM MỌI THỨ", "ĐỂ ĐỔI LẤY MỘT LÍT", "RƯỢU VANG."]
        full = " ".join(lines)
        pt = prog(t, 31.8, 34.9, lambda q: q)
        s = typed(full, pt)
        pos = 0
        fm = font("mono", 50)
        for i, ln in enumerate(lines):
            seg = s[pos:pos + len(ln)]
            pos += len(ln) + 1
            if "LÍT" in ln and len(seg) >= len(ln):
                pre = fm.measureText(nfc("ĐỂ ĐỔI LẤY MỘT "))
                pc = prog(t, 35.32, 35.7)
                if pc > 0:
                    r = skia.Rect.MakeXYWH(36 + pre - 18, 150 + i * 90 - 52, fm.measureText(nfc("LÍT")) + 36, 74)
                    pth = skia.Path(); pth.addOval(r)
                    pm = skia.PathMeasure(pth, False); d = skia.Path(); pm.getSegment(0, pm.getLength() * pc, d, True)
                    c.drawPath(d, paint("red", stroke=6))
            text(c, seg, 36, 150 + i * 90, "mono", 50)
    label_tag(c, "người Anh đong bằng pint, không dùng lít", W / 2, 960, pop_in(t, 35.5), size=32, anchor="center", bg="yellow")
    stamp(c, "ĐỨC VẪN TIN", 560, 1110, prog(t, 36.95, 37.2), size=58, color="red", rot=-8)


def s08_found(c, t):
    draw_paper(c)
    p = pop_in(t, 37.9, 0.35)
    with Xf(c, 90, 360, 1.0, 1, clamp(p * 2)):
        card(c, 0, 0, 900, 330, "white", r=4)
        text(c, "ĐIỆN ĐỨC BỊ ANH GIẢI MÃ", 36, 60, "mono", 30, "grey")
        note_label(c, "MINH HỌA", 740, 26, 1)
        text(c, "...ĐIỆP VIÊN CỦA TA Ở ANH BÁO:", 36, 150, "mono", 40)
        text(c, "...", 36, 220, "mono", 40, "grey")
    pk = prog(t, 38.7, 39.4)
    if pk > 0:
        gx, gy = lerp(1200, 700, pk), lerp(900, 560, pk)
        with Xf(c, gx, gy, -25):
            c.drawCircle(0, 0, 70, paint("white", 90)); c.drawCircle(0, 0, 70, paint("navy", stroke=12))
            c.drawLine(0, 72, 0, 200, paint("navy", stroke=22))
    label_tag(c, "tình báo Anh nhận ra: báo cáo bịa", 90, 790, pop_in(t, 39.4), size=32, bg="navy", fg="white")
    pf = pop_in(t, 40.55, 0.4)
    if pf > 0:
        A("pujol_young").framed(c, 790, 1040, 210, rot=4, scale=lerp(0.8, 1, ease_out(pf)), alpha=clamp(pf * 2))
        r = path_partial(c, [(300, 1060), (660, 1050)], pf, paint("navy", stroke=6), curve=0.1)
        if r:
            arrow_head(c, *r, size=24, color="navy")


def s09_garbo(c, t):
    draw_paper(c)
    chip(c, "1942 · LONDON", W / 2, CHIP_Y, pop_in(t, 41.45))
    pe = pop_in(t, 41.4, 0.35)
    A("pujol_young").framed(c, W / 2, 690, 520, rot=lerp(-5, -2, pe), scale=lerp(0.93, 1, pe) + 0.005 * max(0, t - 41.8))
    label_tag(c, "điệp viên hai mang", 70, 1080, pop_in(t, 43.6), size=36, bg="yellow")
    label_tag(c, "MI5 · cơ quan an ninh Anh", 70, 1160, pop_in(t, 45.8), size=32, bg="navy", fg="white")
    stamp(c, "GARBO", 700, 1000, prog(t, 46.85, 47.05), size=84, color="navy", rot=-9)


def s10_network(c, t):
    ph = A("garbo_network")
    ph.blur_bg(c, 120)
    pe = pop_in(t, 47.75, 0.35)
    ph.framed(c, W / 2, 640, 1010, rot=lerp(2.5, 1, pe), scale=lerp(0.95, 1, pe) + 0.005 * max(0, t - 48.1))
    caption(c, "Sơ đồ mạng lưới Garbo trong hồ sơ MI5", 1030)
    chip(c, "27 ĐIỆP VIÊN KHÔNG CÓ THẬT", W / 2, CHIP_Y, pop_in(t, 49.3), size=38)
    # tiền Đức chảy vào mạng lưới
    if t > 51.0:
        for k in range(9):
            st = 51.0 + k * 0.13
            a = (t - st) / 0.8
            if 0 < a < 1:
                x = lerp(-60, 540 + (k % 3 - 1) * 200, ease_out(a))
                y = lerp(1150, 640 + (k % 2) * 80, ease_out(a))
                with Xf(c, x, y, 12 * k):
                    card(c, -46, -24, 92, 48, "#C9D3B5", r=3)
                    text(c, "£", 0, 12, "xbold", 30, "#4E5E3A", align="center")
        label_tag(c, "Đức trả lương cho tất cả", W / 2, 1160, pop_in(t, 51.2), size=34, anchor="center", bg="red", fg="white")


def s11_plan(c, t):
    if t < 55.5:
        ph = A("overlord_map")
        ph.blur_bg(c, 110)
        pe = pop_in(t, 53.0, 0.35)
        ph.framed(c, W / 2, 680, 980, rot=lerp(-2.5, -1, pe), scale=lerp(0.95, 1, pe) + 0.006 * max(0, t - 53.35))
        chip(c, "1944", W / 2, CHIP_Y, pop_in(t, 53.1))
        caption(c, "Bản đồ kế hoạch đổ bộ Overlord, đóng dấu TOP SECRET", 1150)
        return
    m = A("map")
    cam = drift_cam(CAM_CH, t, 55.5, 0.006)
    m.draw(c, cam)
    map_pin(c, cam, "normandy", "NORMANDY · đổ bộ thật", t, 55.6, "below", color="white", bg="navy", fg="white", size=32)
    cx, cy = map_pin(c, cam, "calais", "PAS-DE-CALAIS", t, 58.4, "left", color="red", bg="red", fg="white", size=32)
    dx, dy = mp(*PLACES["dover"], cam)
    pg = prog(t, 58.6, 59.5)
    if pg > 0:
        r = path_partial(c, [(dx, dy - 40), (cx + 10, cy - 10)], pg, paint("red", 200, stroke=6, PathEffect=skia.DashPathEffect.Make([16, 12], 0)), curve=0.2)
        if r:
            arrow_head(c, *r, size=26, color="red")
        label_tag(c, "điều Đức phải tin", cx - 40, cy + 100, pg, size=30, anchor="right", bg="yellow")


def s12_count(c, t):
    draw_paper(c)
    n = int(lerp(0, 500, prog(t, 60.0, 62.5, lambda q: q) ** 0.8))
    label_tag(c, "THÁNG 1 → 6/6/1944", W / 2, 360, pop_in(t, 59.85), size=38, anchor="center")
    # chồng điện cao dần
    k = int(n / 25)
    for i in range(k):
        with Xf(c, W / 2 + ((i * 37) % 9 - 4) * 3, 1050 - i * 14, ((i * 53) % 7 - 3) * 0.8):
            card(c, -220, -14, 440, 28, "white" if i % 2 else "#F1EAD7", r=2, shadow=i == 0)
    text(c, f"{n}", W / 2, 700, "xbold", 200, "ink", align="center")
    if t > 62.3:
        text(c, "+", W / 2 + tw(f"{n}", "xbold", 200) / 2 + 40, 640, "xbold", 120, "red", a=255 * pop_in(t, 62.3), align="center")
    label_tag(c, "bức điện", W / 2, 790, pop_in(t, 61.3), size=40, anchor="center", bg="yellow")


def s13_dday(c, t):
    if t < 66.0:
        ph = A("omaha_jaws")
        z = lerp(1.0, 1.07, prog(t, 62.9, 66.0, lambda q: q))
        ph.cover(c, skia.Rect.MakeWH(W, H), 0.45, 0.5, z)
        chip(c, "6 THÁNG 6 · 1944", W / 2, CHIP_Y, pop_in(t, 62.95))
        caption(c, "Ảnh: đổ bộ lên bãi Omaha, Normandy, 6/6/1944 (NARA)", 1190)
        label_tag(c, "Garbo được phép báo trước", 60, 1110, pop_in(t, 64.2), size=36, bg="yellow")
        return
    draw_paper(c)
    label_tag(c, "SÁNG 6/6/1944", W / 2, 360, 1, size=38, anchor="center")
    x0, x1, y = 120, 960, 760
    c.drawLine(x0, y, x1, y, paint("ink", stroke=6))
    hours = list(range(0, 10))
    for hh in hours:
        x = lerp(x0, x1, hh / 9)
        c.drawLine(x, y - 14, x, y + 14, paint("ink", stroke=4))
        text(c, f"{hh}h", x, y + 56, "bold", 28, "grey", align="center")
    # giờ gửi (≈3h) và đổ bộ (≈6h30)
    xs, xl, xa = lerp(x0, x1, 3 / 9), lerp(x0, x1, 6.5 / 9), lerp(x0, x1, 8 / 9)
    ps = pop_in(t, 66.1)
    if ps > 0:
        pin(c, xs, y, ps, color="yellow")
        label_tag(c, "Garbo gửi điện", xs, y - 100, ps, size=30, anchor="center", bg="yellow")
    pl = pop_in(t, 66.7)
    if pl > 0:
        pin(c, xl, y, pl, color="white")
        label_tag(c, "đổ bộ", xl, y + 130, pl, size=30, anchor="center", bg="navy", fg="white")
    pa = prog(t, 67.4, 68.4, ease_in_out)
    if pa > 0:
        r = path_partial(c, [(xs, y - 30), (xa, y - 30)], pa, paint("red", stroke=6), curve=-0.25)
        if r:
            arrow_head(c, *r, size=24, color="red")
        label_tag(c, "tin tới quá muộn", xa, y - 240, pop_in(t, 68.2), size=30, anchor="center", bg="red", fg="white")
    stamp(c, "ĐỨC CÀNG TIN", 540, 1080, prog(t, 70.4, 70.6), size=60, color="red", rot=-7)


def s14_key(c, t):
    draw_paper(c)
    chip(c, "9 THÁNG 6 · 1944", W / 2, CHIP_Y, pop_in(t, 71.5))
    w, h = 940, 520
    p = pop_in(t, 71.43, 0.35)
    with Xf(c, 70, 340 + (1 - ease_out(p)) * 500, 0.8, 1, clamp(p * 2)):
        card(c, 0, 0, w, h, "white", r=4)
        text(c, "GARBO → ĐỨC · 9/6/1944", 36, 58, "mono", 28, "grey")
        note_label(c, "DIỄN Ý", w - 150, 26, 1)
        c.drawLine(36, 86, w - 36, 86, paint("grey", 120, stroke=2))
        fm = font("mono", 48)
        L = [("NORMANDY CHỈ LÀ NGHI BINH.", 73.76, 75.1), ("ĐỪNG ĐIỀU QUÂN TỚI ĐÓ.", 75.48, 76.3),
             ("TRẬN CHÍNH:", 76.62, 77.2), ("PAS-DE-CALAIS.", 77.2, 78.0)]
        for i, (ln, a, b) in enumerate(L):
            s = typed(ln, prog(t, a, b, lambda q: q))
            if i == 3:
                highlight(c, 36, 150 + i * 90 - 46, fm.measureText(nfc(ln)), 60, prog(t, 77.6, 78.0))
            text(c, s, 36, 150 + i * 90, "mono", 48)
    ph = pop_in(t, 78.45, 0.35)
    if ph > 0:
        r = path_partial(c, [(540, 900), (540, 1060)], ph, paint("red", stroke=7))
        if r:
            arrow_head(c, *r, size=26, color="red")
        label_tag(c, "LÊN TỚI HITLER", W / 2, 1140, ph, size=44, anchor="center", bg="red", fg="white")


def tank(c, x, y, s=1.0, color="red", ang=0):
    with Xf(c, x, y, ang, s):
        shadow_begin(c, skia.Rect.MakeXYWH(-70, -50, 140, 100), dy=3, blur=3, a=80)
        c.drawRoundRect(skia.Rect.MakeXYWH(-40, -8, 80, 26), 12, 12, paint(color))
        c.drawRect(skia.Rect.MakeXYWH(-22, -26, 40, 20), paint(color))
        c.drawRect(skia.Rect.MakeXYWH(14, -20, 40, 6), paint(color))
        c.restore()


def s15_halt(c, t):
    m = A("map")
    cam = drift_cam(CAM_CH, t, 79.9, 0.006)
    m.draw(c, cam)
    nx, ny = map_pin(c, cam, "normandy", "NORMANDY", t, -10, "below", color="white", bg="navy", fg="white")
    cx, cy = map_pin(c, cam, "calais", "PAS-DE-CALAIS", t, -10, "left", color="red", bg="red", fg="white")
    # xe tăng Đức rời Pas-de-Calais về Normandy rồi dừng lại, quay về
    go = prog(t, 80.1, 81.2, ease_in_out)
    back = prog(t, 81.6, 82.5, ease_in_out)
    f = go * (1 - back * 0.85)
    for k in range(4):
        sx, sy = cx - 40 + k * 60, cy + 110 + k * 44
        ex, ey = lerp(sx, nx + 200, 0.55), lerp(sy, ny - 40, 0.55)
        tank(c, lerp(sx, ex, f), lerp(sy, ey, f), 0.9, "red", 180 if back < 0.5 else 0)
    if t > 81.4:
        sp = pop_in(t, 81.4)
        with Xf(c, lerp(cx, nx, 0.66), lerp(cy, ny, 0.66) + 40, 0, max(0.01, back_out(sp))):
            c.drawCircle(0, 0, 54, paint("red")); c.drawCircle(0, 0, 54, paint("white", stroke=6))
            text(c, "DỪNG", 0, 12, "xbold", 30, "white", align="center")
    # cuộc đổ bộ không bao giờ đến
    dx, dy = mp(*PLACES["dover"], cam)
    pg = prog(t, 82.3, 83.4)
    if pg > 0:
        r = path_partial(c, [(dx, dy - 40), (cx + 10, cy - 10)], pg, paint("grey", 200 * (1 - prog(t, 83.4, 84.0)), stroke=6, PathEffect=skia.DashPathEffect.Make([16, 12], 0)), curve=0.2)
        label_tag(c, "không bao giờ đến", dx - 10, dy - 110, pop_in(t, 83.0), size=30, anchor="right", bg="white", fg="grey")


def s16_awards(c, t):
    draw_paper(c)
    chip(c, "29 THÁNG 7 · 1944", W / 2, CHIP_Y, pop_in(t, 84.1))
    pe = pop_in(t, 84.03, 0.35)
    A("iron_cross").framed(c, 330, 700, 420, rot=lerp(-6, -3, pe), scale=lerp(0.93, 1, pe))
    rings(c, 330, 420, t, 84.6, 86.2, "red", max_r=420, period=0.4, width=5)
    label_tag(c, "Hitler trao · Thập tự Sắt", 330, 1080, pop_in(t, 86.6), size=32, anchor="center", bg="red", fg="white")
    p2 = pop_in(t, 88.85, 0.4)
    if p2 > 0:
        A("mbe").framed(c, 790, 720, 400, rot=lerp(8, 3, ease_out(p2)), scale=lerp(0.8, 1, ease_out(p2)), alpha=clamp(p2 * 2))
        label_tag(c, "Anh trao · MBE", 790, 1080, p2, size=32, anchor="center", bg="navy", fg="white")
    label_tag(c, "CUỐI 1944", 790, 420, pop_in(t, 88.15), size=34, anchor="center", bg="yellow")


def s17_dead(c, t):
    draw_paper(c)
    p = pop_in(t, 90.2, 0.35)
    with Xf(c, 540, 700, -1.5, lerp(0.9, 1, ease_out(p)), clamp(p * 2)):
        card(c, -380, -330, 760, 660, "#F4EEDF", r=2)
        c.drawRect(skia.Rect.MakeXYWH(-350, -300, 700, 600), paint("ink", stroke=8, cap=False))
        text(c, "CÁO PHÓ", 0, -200, "xbold", 64, "ink", align="center")
        text(c, "JUAN PUJOL", 0, -100, "xbold", 56, "ink", align="center")
        text(c, typed("chết vì sốt rét ở châu Phi", prog(t, 93.6, 95.2, lambda q: q)), 0, 30, "semi", 40, "ink", align="center")
        text(c, typed("1949", prog(t, 95.5, 95.9, lambda q: q)), 0, 130, "xbold", 60, "ink", align="center")
    label_tag(c, "sợ bị trả thù", 80, 300 + 60, pop_in(t, 91.1), size=34, bg="yellow")
    stamp(c, "TIN GIẢ", 640, 1060, prog(t, 92.3, 92.55), size=64, color="red", rot=-10)


def s18_venezuela(c, t):
    ph = A("venezuela_passport")
    ph.blur_bg(c, 110)
    pe = pop_in(t, 96.61, 0.35)
    ph.framed(c, W / 2, 700, 1000, rot=lerp(-3, -1, pe), scale=lerp(0.94, 1, pe) + 0.006 * max(0, t - 97.0))
    chip(c, "VENEZUELA", W / 2, CHIP_Y, pop_in(t, 96.7))
    caption(c, "Hộ chiếu Venezuela mang tên Juan Pujol García", 1060)
    label_tag(c, "mở một cửa hàng nhỏ", 60, 1130, pop_in(t, 98.35), size=34, bg="yellow")


def s19_found(c, t):
    draw_paper(c)
    n = int(lerp(1949, 1984, prog(t, 99.5, 100.6, lambda q: q)))
    text(c, str(n), W / 2, 760, "xbold", 210, "ink", align="center")
    label_tag(c, "35 năm sau", W / 2, 470, pop_in(t, 99.55), size=40, anchor="center", bg="yellow")
    label_tag(c, "nhà sử học Anh Nigel West lần ra ông", W / 2, 960, pop_in(t, 100.9), size=32, anchor="center", bg="navy", fg="white")


def s20_beach(c, t):
    # bãi biển giấy cắt: trời, biển, cát
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#DCE3E2"))
    c.drawRect(skia.Rect.MakeXYWH(0, 820, W, 400), paint("#8FA5AA"))
    for k in range(3):
        y = 900 + k * 90 + 10 * math.sin(t * 1.5 + k)
        c.drawLine(0, y, W, y + 6, paint("white", 140, stroke=4))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, 770), paint("#E6D8B4"))
    chip(c, "THÁNG 6 · 1984", W / 2, CHIP_Y, pop_in(t, 102.25))
    pe = pop_in(t, 102.2, 0.4)
    A("pujol_beard").framed(c, W / 2, 680, 470, rot=lerp(-5, -2, pe), scale=lerp(0.93, 1, pe) + 0.006 * max(0, t - 102.6))
    label_tag(c, "\"đã chết\" năm 1949", 70, 1060, pop_in(t, 104.6), size=34, bg="white")
    label_tag(c, "BÃI BIỂN NORMANDY", W - 70, 1130, pop_in(t, 105.9), size=34, anchor="right", bg="navy", fg="white")
    label_tag(c, "40 năm sau ngày đổ bộ", W / 2, 1210, pop_in(t, 107.6), size=32, anchor="center", bg="yellow")
    if t > 108.9:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("ink", 255 * prog(t, 108.9, 110.0, lambda q: q)))


TIMELINE = [
    (0.00, 8.15, s01_medals),
    (8.15, 11.14, s03_pujol),
    (11.14, 18.46, s04_apply),
    (18.46, 26.24, s05_lisbon),
    (26.24, 30.62, s06_sources),
    (30.62, 37.91, s07_glasgow),
    (37.91, 41.40, s08_found),
    (41.40, 47.75, s09_garbo),
    (47.75, 53.01, s10_network),
    (53.01, 59.80, s11_plan),
    (59.80, 62.90, s12_count),
    (62.90, 71.43, s13_dday),
    (71.43, 79.90, s14_key),
    (79.90, 84.03, s15_halt),
    (84.03, 90.17, s16_awards),
    (90.17, 96.61, s17_dead),
    (96.61, 99.47, s18_venezuela),
    (99.47, 102.17, s19_found),
    (102.17, 110.10, s20_beach),
]


def draw_frame(c, t):
    for a, b, fn in TIMELINE:
        if a <= t < b:
            fn(c, t)
            break
