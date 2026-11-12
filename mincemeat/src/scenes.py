"""Bảng dựng tập Mincemeat (phong cách Midway v2). Mốc giây theo MP3, xem build/words.json (ước lượng).
Màu: đỏ = phía Đức, navy = phía Anh/Đồng minh, vàng = chi tiết đáng nhìn.
Quy tắc ảnh: chỉ dùng ảnh đã xác minh; Glyndwr Michael không có ảnh xác minh được → hình bóng trung tính."""
import math
import skia
from lib import *  # noqa

PH = ROOT / "assets/photos"
CHIP_Y = 250
_assets = {}

PLACES.update({"huelva": (-6.95, 37.26), "madrid": (-3.70, 40.42), "sicily": (14.2, 37.5), "sardinia": (9.0, 40.1),
               "greece": (22.0, 39.3), "tunis": (10.2, 36.8), "paris": (2.35, 48.86)})


def A(key):
    if key not in _assets:
        _assets[key] = Map() if key == "map" else Photo(PH / f"{key}.jpg")
    return _assets[key]


def caption(c, s, y=1225, size=27, x=60):
    text(c, s, x, y, "semi", size, "white", a=235, stroke=3, stroke_color="ink")


def caption_dark(c, s, y, size=27, x=60):
    text(c, s, x, y, "semi", size, "grey")


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


def tint_country(c, cam, name, color, a):
    if a <= 0:
        return
    for ring in RINGS.get(name, []):
        path = skia.Path()
        for j, (lon, lat) in enumerate(ring):
            (path.moveTo if j == 0 else path.lineTo)(*mp(lon, lat, cam))
        path.close()
        c.drawPath(path, paint(color, 110 * a))
        c.drawPath(path, paint(color, 220 * a, stroke=3))


def briefcase(c, x, y, s=1.0, open_=0.0, chain=True):
    with Xf(c, x, y, 0, s):
        shadow_begin(c, skia.Rect.MakeXYWH(-260, -220, 520, 420))
        c.drawRoundRect(skia.Rect.MakeXYWH(-200, -110, 400, 230), 18, 18, paint("#5B3E2A"))
        lid_h = 70 * (1 - open_)
        c.drawRoundRect(skia.Rect.MakeXYWH(-200, -110 - 40 * open_, 400, 60), 14, 14, paint("#6E4C34"))
        c.drawRoundRect(skia.Rect.MakeXYWH(-60, -150, 120, 50), 18, 18, paint("#3E2A1C", stroke=12))
        c.drawRect(skia.Rect.MakeXYWH(-30, -60, 60, 26), paint("#C9A55A"))
        c.restore()
        if chain:
            for k in range(7):
                c.drawOval(skia.Rect.MakeXYWH(200 + k * 26, -10 + k * 14, 30, 18), paint("#8D8D8D", stroke=5))


def silhouette(c, x, y, s=1.0, cap=False, a=255):
    """Hình bóng trung tính (đầu và vai) — dùng khi không có ảnh xác minh được."""
    with Xf(c, x, y, 0, s, a / 255):
        c.drawCircle(0, -120, 95, paint("#6E675B"))
        body = skia.Path()
        body.moveTo(-230, 200); body.cubicTo(-220, 40, -120, -10, 0, -10); body.cubicTo(120, -10, 220, 40, 230, 200); body.close()
        c.drawPath(body, paint("#6E675B"))
        if cap:
            c.drawRoundRect(skia.Rect.MakeXYWH(-110, -250, 220, 70), 30, 30, paint("#3F3A33"))
            c.drawRect(skia.Rect.MakeXYWH(-125, -195, 250, 22), paint("#2E2A25"))


# ------------------------------------------------------------------ máy quay bản đồ
CAM_SP = (-5.2, 38.4, 75.0)      # bán đảo Iberia, có Huelva
CAM_MED = (15.5, 38.6, 46.0)     # Địa Trung Hải: Sardinia – Sicily – Hy Lạp
CAM_EUR = (12.0, 43.5, 30.0)     # Pháp – Hy Lạp – Sardinia
CAM_SIC = (13.6, 37.2, 100.0)    # Sicily, hướng đổ bộ từ phía nam


# ------------------------------------------------------------------ CẢNH
def s01_found(c, t):
    m = A("map")
    cam = drift_cam(CAM_SP, t, 0, 0.008)
    m.draw(c, cam)
    chip(c, "30 THÁNG 4 · 1943", W / 2, CHIP_Y, pop_in(t, 0.45))
    hx, hy = mp(*PLACES["huelva"], cam)
    pb = pop_in(t, 2.4, 0.5)
    if pb > 0:
        bx, by = hx - 70 + 6 * math.sin(t * 2), hy + 70
        with Xf(c, bx, by, 3 * math.sin(t * 1.7), 1, clamp(pb * 2)):
            hull = skia.Path(); hull.moveTo(-60, 0); hull.lineTo(60, 0); hull.lineTo(42, 22); hull.lineTo(-44, 22); hull.close()
            c.drawPath(hull, paint("#7A5A3C"))
            c.drawLine(0, 0, 0, -50, paint("#5A4630", stroke=4))
        label_tag(c, "ngư dân Tây Ban Nha", hx - 90, hy + 150, pb, size=30, anchor="center")
    map_pin(c, cam, "huelva", "HUELVA", t, 5.85, "right", bg="yellow")
    label_tag(c, "TÂY BAN NHA", hx + 260, hy - 260, pop_in(t, 2.6), size=30, anchor="center")


def s02_case(c, t):
    draw_paper(c)
    p = pop_in(t, 6.7, 0.4)
    op = prog(t, 8.3, 8.8, ease_in_out)
    with Xf(c, 0, (1 - ease_out(p)) * 600, 0, 1, clamp(p * 2)):
        briefcase(c, 470, 820, 1.0, open_=op)
    label_tag(c, "chiếc cặp gắn vào người", W / 2, 1110, pop_in(t, 7.3), size=34, anchor="center")
    pl = prog(t, 8.7, 9.3, ease_out)
    if pl > 0:
        for k in range(2):
            with Xf(c, 470 + k * 60 - 30, lerp(760, 520 - k * 30, pl), -4 + k * 6, 1, clamp(pl * 2)):
                card(c, -170, -110, 340, 220, "white", r=4)
                for i in range(5):
                    c.drawLine(-130, -60 + i * 30, 120 - (i % 2) * 60, -60 + i * 30, paint("grey", 120, stroke=6))
    stamp(c, "MẬT", 560, 520, prog(t, 9.4, 9.6), size=64, rot=-8)
    label_tag(c, "kế hoạch tấn công tiếp theo", W / 2, 1190, pop_in(t, 10.0), size=32, anchor="center", bg="yellow")


def s03_card(c, t):
    ph = A("id_card_martin")
    ph.blur_bg(c, 120)
    pe = pop_in(t, 11.6, 0.35)
    ph.framed(c, W / 2, 680, 1000, rot=lerp(-3, -1, pe), scale=lerp(0.95, 1, pe) + 0.005 * max(0, t - 12.0))
    caption(c, "Thẻ quân nhân giả của \"William Martin\"", 1000, 28)
    caption(c, "(ảnh trên thẻ là một sĩ quan MI5, không phải người chết)", 1040, 27)
    stamp(c, "GIẢ", 760, 560, prog(t, 12.6, 12.8), size=90, rot=-10)
    label_tag(c, "cái bẫy của tình báo Anh", W / 2, 1150, pop_in(t, 14.4), size=36, anchor="center", bg="navy", fg="white")


def s04_med(c, t):
    m = A("map")
    cam = drift_cam(CAM_MED, t, 16.07, 0.008)
    m.draw(c, cam)
    chip(c, "ĐỒNG MINH · 1943", W / 2, CHIP_Y, pop_in(t, 16.15))
    sx, sy = mp(*PLACES["sicily"], cam)
    tx, ty = mp(*PLACES["tunis"], cam)
    dim = prog(t, 21.6, 22.2)
    pin(c, sx, sy, pop_in(t, 18.1), color="yellow")
    label_tag(c, "SICILY", sx + 24, sy - 44, pop_in(t, 18.1) * (1 - 0.5 * dim), size=34, bg="yellow")
    pa = prog(t, 19.2, 20.2, ease_in_out)
    if pa > 0:
        r = path_partial(c, [(tx, ty + 30), (sx - 10, sy + 20)], pa, paint("navy", 230 * (1 - 0.6 * dim), stroke=8), curve=-0.15)
        if r:
            arrow_head(c, *r, size=28, color="navy", a=255 * (1 - 0.6 * dim))
        label_tag(c, "ai cũng đoán được", tx - 20, ty + 120, pa * (1 - dim), size=32, anchor="center", bg="white")
    label_tag(c, "BẮC PHI · Đồng minh", tx - 20, ty + 60, pop_in(t, 18.9) * (1 - dim), size=28, anchor="center", bg="navy", fg="white")
    gx, gy = map_pin(c, cam, "greece", "HY LẠP", t, 24.7, "right", color="red", bg="red", fg="white", size=34)
    dx, dy = map_pin(c, cam, "sardinia", "SARDINIA", t, 25.35, "left", color="red", bg="red", fg="white", size=34)
    label_tag(c, "mục tiêu giả cho Đức tin", W / 2, 1160, pop_in(t, 24.9), size=32, anchor="center", bg="yellow")


def s05_michael(c, t):
    draw_paper(c)
    p = pop_in(t, 26.25, 0.4)
    silhouette(c, W / 2, 700, 1.0, a=255 * p)
    name_tag(c, 90, 960, "Glyndwr Michael", "người xứ Wales vô gia cư · mất ở London, 1/1943", pop_in(t, 28.95, 0.4), size=48, role_size=28)
    caption_dark(c, "Không có ảnh nào được xác nhận là của ông", 1180, 28, x=90)


def s06_identity(c, t):
    draw_paper(c)
    silhouette(c, W / 2, 700, 1.0, cap=t > 33.2)
    po = 1 - prog(t, 31.9, 32.3)
    if po > 0:
        name_tag(c, 90, 960, "Glyndwr Michael", "người xứ Wales vô gia cư · mất ở London, 1/1943", po, size=48, role_size=28)
    label_tag(c, "danh tính mới", W / 2, 360, pop_in(t, 32.2), size=36, anchor="center", bg="yellow")
    name_tag(c, 90, 960, "Thiếu tá William Martin", "Thủy quân Lục chiến Hoàng gia (danh tính giả)", pop_in(t, 33.3, 0.4), size=46, role_size=28)


ITEMS = [(40.05, "thẻ quân nhân"), (40.85, "ảnh \"Pam\""), (42.25, "hai lá thư tình"),
         (43.2, "hóa đơn nhẫn đính hôn"), (44.5, "cuống vé xem kịch"), (45.45, "thư ngân hàng: chi quá số dư")]


def pocket_item(c, i, x, y, t):
    if i == 0:
        A("id_card_martin").framed(c, x, y, 330, rot=-3, border=8)
    elif i == 1:
        A("pam_jean_leslie").framed(c, x, y, 330, rot=3, border=8)
    elif i == 2:
        for k in range(2):
            with Xf(c, x - 20 + k * 40, y - 10 + k * 20, -6 + k * 10):
                card(c, -130, -90, 260, 180, "#F6EFE0", r=3)
                for j in range(4):
                    path = skia.Path(); path.moveTo(-100, -50 + j * 30)
                    for q in range(8):
                        path.lineTo(-100 + q * 28, -50 + j * 30 + (6 if q % 2 else -6))
                    c.drawPath(path, paint("#4A5A8A", stroke=3))
    elif i == 3:
        with Xf(c, x, y, 2):
            card(c, -140, -100, 280, 200, "white", r=3)
            text(c, "HÓA ĐƠN", -110, -55, "mono", 30, "ink")
            c.drawCircle(70, 30, 34, paint("#C9A55A", stroke=10))
            c.drawCircle(70, -4, 12, paint("#E6F0F5"))
            c.drawLine(-110, 0, 10, 0, paint("grey", 120, stroke=5)); c.drawLine(-110, 40, -10, 40, paint("grey", 120, stroke=5))
    elif i == 4:
        for k in range(2):
            with Xf(c, x - 30 + k * 60, y + k * 16, -8 + k * 14):
                card(c, -120, -55, 240, 110, "#E9D9A6", r=3)
                text(c, "VÉ", -95, 15, "xbold", 40, "#7B3B2E")
                c.drawLine(40, -50, 40, 50, paint("#7B3B2E", 150, stroke=3, PathEffect=skia.DashPathEffect.Make([8, 6], 0)))
    else:
        with Xf(c, x, y, -2):
            card(c, -140, -100, 280, 200, "white", r=3)
            text(c, "NGÂN HÀNG", -110, -55, "mono", 28, "ink")
            text(c, "– £", -110, 40, "xbold", 54, "red")
            c.drawLine(0, 10, 110, 10, paint("grey", 120, stroke=5)); c.drawLine(0, 45, 90, 45, paint("grey", 120, stroke=5))


def s07_pocket(c, t):
    draw_paper(c)
    label_tag(c, "trong túi \"William Martin\"", W / 2, 330, pop_in(t, 37.5), size=36, anchor="center", bg="yellow")
    pos = [(290, 560), (790, 560), (290, 830), (790, 830), (290, 1090), (790, 1090)]
    for i, ((ts, lab), (x, y)) in enumerate(zip(ITEMS, pos)):
        p = pop_in(t, ts - 0.1, 0.35)
        if p <= 0:
            continue
        with Xf(c, x, y, 0, max(0.01, back_out(p)), clamp(p * 3)):
            pocket_item(c, i, 0, 0, t)
        label_tag(c, lab, x, y + 130, p, size=28, anchor="center")


def s08_pam(c, t):
    ph = A("pam_jean_leslie")
    ph.blur_bg(c, 120)
    pe = pop_in(t, 48.22, 0.35)
    ph.framed(c, W / 2, 680, 980, rot=lerp(3, 1, pe), scale=lerp(0.95, 1, pe) + 0.006 * max(0, t - 48.6))
    label_tag(c, "\"Pam\" = Jean Leslie, nhân viên MI5", 60, 1080, pop_in(t, 49.6), size=34, bg="navy", fg="white")
    caption(c, "Ảnh trong hồ sơ chiến dịch, Lưu trữ Quốc gia Anh (WO 106/5921)", 1160)


def s09_generals(c, t):
    draw_paper(c)
    if t < 55.46:
        p1 = pop_in(t, 52.9, 0.4)
        if p1 > 0:
            A("nye").framed(c, 290, 660, 400, rot=-3, scale=lerp(0.9, 1, ease_out(p1)), alpha=clamp(p1 * 2))
            label_tag(c, "Tướng Archibald Nye", 290, 980, p1, size=30, anchor="center")
        p2 = pop_in(t, 54.2, 0.4)
        if p2 > 0:
            A("alexander").framed(c, 790, 660, 400, rot=3, scale=lerp(0.9, 1, ease_out(p2)), alpha=clamp(p2 * 2))
            label_tag(c, "Tướng Harold Alexander", 790, 980, p2, size=30, anchor="center")
        pl = prog(t, 53.6, 54.4, ease_in_out)
        if pl > 0:
            with Xf(c, lerp(290, 790, pl), 1080 - 50 * math.sin(math.pi * pl), lerp(-8, 8, pl)):
                card(c, -70, -45, 140, 90, "white", r=3)
                c.drawLine(-70, -45, 0, 5, paint("grey", 150, stroke=3)); c.drawLine(70, -45, 0, 5, paint("grey", 150, stroke=3))
        label_tag(c, "lá thư quan trọng nhất", W / 2, 360, pop_in(t, 50.9), size=36, anchor="center", bg="yellow")
        return
    # nhiều bản nháp → Nye tự viết
    for k in range(4):
        st = 55.5 + k * 0.28
        a = (t - st) / 0.9
        if a > 0:
            x = lerp(540, 160 + k * 250, ease_out(min(1, a)))
            y = lerp(700, 1050 + (k % 2) * 60, ease_out(min(1, a)))
            with Xf(c, x, y, 40 * k + a * 30, 0.6):
                c.drawCircle(0, 0, 70, paint("#F1EAD7"))
                for q in range(5):
                    c.drawLine(-50 + q * 18, -40, -30 + q * 14, 40, paint("grey", 120, stroke=3))
    label_tag(c, "nhiều bản nháp", 80, 430, pop_in(t, 55.6) * (1 - prog(t, 57.0, 57.3)), size=34)
    pw = pop_in(t, 57.1, 0.4)
    if pw > 0:
        with Xf(c, 540, 700, -1.5, lerp(0.9, 1, ease_out(pw)), clamp(pw * 2)):
            card(c, -330, -300, 660, 600, "white", r=4)
            pl = prog(t, 57.3, 58.6, lambda q: q)
            for i in range(int(9 * pl)):
                path = skia.Path(); path.moveTo(-280, -230 + i * 50)
                for q in range(14):
                    path.lineTo(-280 + q * 40, -230 + i * 50 + (5 if q % 2 else -5))
                c.drawPath(path, paint("#2E3550", stroke=3))
        label_tag(c, "tướng Nye tự viết", W / 2, 1100, pw, size=36, anchor="center", bg="navy", fg="white")


def s10_letter(c, t):
    draw_paper(c)
    p = pop_in(t, 58.69, 0.35)
    w, h = 940, 520
    with Xf(c, 70, 360 + (1 - ease_out(p)) * 400, 0.8, 1, clamp(p * 2)):
        card(c, 0, 0, w, h, "white", r=4)
        text(c, "NYE → ALEXANDER", 36, 58, "mono", 28, "grey")
        note_label(c, "DIỄN Ý", w - 150, 26, 1)
        c.drawLine(36, 86, w - 36, 86, paint("grey", 120, stroke=2))
        fm = font("mono", 46)
        L = [("ĐỨC ĐANG TĂNG QUÂN Ở HY LẠP.", 58.8, 60.2), ("ĐỒNG MINH PHẢI TĂNG", 60.6, 61.4), ("LỰC LƯỢNG TẤN CÔNG.", 61.4, 62.2),
             ("SICILY: CHỈ ĐỂ ĐÁNH LẠC HƯỚNG.", 62.5, 64.4)]
        for i, (ln, a, b) in enumerate(L):
            if i == 3:
                highlight(c, 36, 150 + i * 90 - 46, fm.measureText(nfc(ln)), 60, prog(t, 63.6, 64.3))
            text(c, typed(ln, prog(t, a, b, lambda q: q)), 36, 150 + i * 90, "mono", 46)


def s11_seraph(c, t):
    if t < 66.87:
        draw_paper(c)
        p = pop_in(t, 64.9, 0.4)
        with Xf(c, 540, 720, 0, lerp(0.9, 1, ease_out(p)), clamp(p * 2)):
            shadow_begin(c, skia.Rect.MakeXYWH(-200, -420, 400, 840))
            c.drawRoundRect(skia.Rect.MakeXYWH(-120, -360, 240, 720), 60, 60, paint("#8E959B"))
            c.restore()
            for k in range(5):
                c.drawLine(-120, -280 + k * 140, 120, -280 + k * 140, paint("#6F767C", stroke=6))
        for k in range(6):
            st = 65.3 + k * 0.2
            a = t - st
            if a > 0:
                sp = paint("white", 160 * clamp(1 - a / 1.4))
                sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10 + a * 12))
                c.drawCircle(540 + math.sin(k * 2) * 60 + a * 30, 340 - a * 120, 30 + a * 40, sp)
        label_tag(c, "hộp thép chứa băng khô", W / 2, 1160, pop_in(t, 65.6), size=34, anchor="center")
        return
    ph = A("seraph_crew")
    ph.blur_bg(c, 120)
    pe = pop_in(t, 66.87, 0.35)
    ph.framed(c, W / 2, 680, 1000, rot=lerp(-2.5, -1, pe), scale=lerp(0.95, 1, pe) + 0.006 * max(0, t - 67.2))
    label_tag(c, "TÀU NGẦM HMS SERAPH", 60, 1090, pop_in(t, 67.2), size=36, bg="navy", fg="white")
    caption(c, "Tên tàu thấy rõ trên tháp; ảnh thủy thủ đoàn HMS Seraph", 1170)


def s12_spain(c, t):
    m = A("map")
    cam = drift_cam(CAM_SP, t, 70.38, 0.008)
    m.draw(c, cam)
    tint_country(c, cam, "Spain", "grey", pop_in(t, 70.45, 0.4) * (1 - prog(t, 71.4, 71.8)))
    tint_country(c, cam, "Spain", "red", prog(t, 71.4, 71.8) * 0.8)
    label_tag(c, "trung lập", W / 2, 420, pop_in(t, 70.5) * (1 - prog(t, 71.4, 71.6)), size=36, anchor="center")
    label_tag(c, "nhưng thân Đức", W / 2, 420, pop_in(t, 71.4), size=36, anchor="center", bg="red", fg="white")
    hx, hy = map_pin(c, cam, "huelva", "HUELVA", t, -10, "left", bg="yellow")
    mx, my = mp(*PLACES["madrid"], cam)
    pf = prog(t, 72.3, 73.6, ease_in_out)
    if pf > 0:
        r = path_partial(c, [(hx, hy), (mx, my)], pf, paint("red", 220, stroke=5, PathEffect=skia.DashPathEffect.Make([16, 10], 0)), curve=-0.2)
        with Xf(c, r[0][0], r[0][1] - 50, -4):
            card(c, -50, -34, 100, 68, "white", r=3)
            c.drawLine(-36, -12, 36, -12, paint("grey", stroke=3)); c.drawLine(-36, 6, 20, 6, paint("grey", stroke=3))
        label_tag(c, "tình báo Đức", mx + 20, my - 60, pop_in(t, 73.4), size=32, bg="red", fg="white")


def s13_return(c, t):
    draw_paper(c)
    chip(c, "GIỮA THÁNG 5 · 1943", W / 2, CHIP_Y, pop_in(t, 74.6))
    mv = prog(t, 75.3, 76.4, ease_in_out)
    briefcase(c, lerp(470, 600, mv), 760 - 30 * math.sin(math.pi * mv), 0.9, chain=False)
    label_tag(c, "trả về cho Anh", W / 2, 1100, pop_in(t, 75.6), size=36, anchor="center", bg="navy", fg="white")


def s14_decrypt(c, t):
    draw_paper(c)
    chip(c, "14 THÁNG 5 · 1943", W / 2, CHIP_Y, pop_in(t, 76.95))
    p = pop_in(t, 76.9, 0.35)
    with Xf(c, 90, 380, 1.0, 1, clamp(p * 2)):
        card(c, 0, 0, 900, 380, "white", r=4)
        text(c, "ĐIỆN ĐỨC · ANH GIẢI MÃ", 36, 60, "mono", 30, "grey")
        note_label(c, "DIỄN Ý", 750, 26, 1)
        text(c, typed("MỤC TIÊU ĐỒNG MINH:", prog(t, 80.0, 80.9, lambda q: q)), 36, 170, "mono", 46)
        fm = font("mono", 64)
        highlight(c, 36, 220, fm.measureText(nfc("HY LẠP")), 76, prog(t, 81.6, 81.95))
        text(c, typed("HY LẠP", prog(t, 81.2, 81.7, lambda q: q)), 36, 280, "mono", 64)
    pk = prog(t, 78.1, 78.8)
    if pk > 0:
        gx, gy = lerp(1200, 780, pk), lerp(1000, 760, pk)
        with Xf(c, gx, gy, -25):
            c.drawCircle(0, 0, 70, paint("white", 90)); c.drawCircle(0, 0, 70, paint("navy", stroke=12))
            c.drawLine(0, 72, 0, 200, paint("navy", stroke=22))
    stamp(c, "ĐỨC ĐÃ TIN", 420, 1000, prog(t, 81.95, 82.15), size=60, color="red", rot=-8)


def tank(c, x, y, s=1.0, color="red", ang=0):
    with Xf(c, x, y, ang, s):
        shadow_begin(c, skia.Rect.MakeXYWH(-70, -50, 140, 100), dy=3, blur=3, a=80)
        c.drawRoundRect(skia.Rect.MakeXYWH(-40, -8, 80, 26), 12, 12, paint(color))
        c.drawRect(skia.Rect.MakeXYWH(-22, -26, 40, 20), paint(color))
        c.drawRect(skia.Rect.MakeXYWH(14, -20, 40, 6), paint(color))
        c.restore()


def s15_moves(c, t):
    m = A("map")
    cam = drift_cam(CAM_EUR, t, 82.17, 0.008)
    m.draw(c, cam)
    gx, gy = map_pin(c, cam, "greece", "HY LẠP", t, -10, "right", color="red", bg="red", fg="white")
    sx, sy = map_pin(c, cam, "sardinia", "SARDINIA", t, -10, "left", color="red", bg="red", fg="white")
    for k, (dst, t0) in enumerate([((sx, sy), 82.9), ((gx, gy), 83.4)]):
        pr = prog(t, t0, t0 + 0.8, ease_in_out)
        if pr > 0:
            src = (dst[0] - 40, dst[1] - 330) if k == 0 else (dst[0] - 260, dst[1] - 280)
            r = path_partial(c, [src, dst], pr, paint("red", 220, stroke=7), curve=0.15)
            if r:
                arrow_head(c, *r, size=26, color="red")
    px, py = mp(*PLACES["paris"], cam)
    pt = prog(t, 84.6, 87.2, ease_in_out)
    if pt > 0:
        r = path_partial(c, [(px, py), (gx, gy)], pt, paint("red", 160, stroke=5, PathEffect=skia.DashPathEffect.Make([16, 10], 0)), curve=-0.1)
        tank(c, r[0][0], r[0][1] - 20, 1.1, "red")
        label_tag(c, "PHÁP", px - 24, py - 44, pop_in(t, 84.5), size=30, anchor="right")
        label_tag(c, "một sư đoàn thiết giáp", W / 2, 1160, pop_in(t, 84.7), size=34, anchor="center", bg="yellow")
    label_tag(c, "Đức điều thêm quân", W / 2, 420, pop_in(t, 82.25), size=36, anchor="center", bg="red", fg="white")


def s16_sicily(c, t):
    m = A("map")
    cam = drift_cam(CAM_SIC, t, 87.61, 0.008)
    m.draw(c, cam)
    chip(c, "THÁNG 7 · 1943", W / 2, CHIP_Y, pop_in(t, 87.7))
    sx, sy = map_pin(c, cam, "sicily", "SICILY", t, 87.8, "right", bg="yellow")
    tx, ty = mp(*PLACES["tunis"], cam)
    for k in range(3):
        pr = prog(t, 89.5 + k * 0.15, 90.6 + k * 0.15, ease_in_out)
        if pr > 0:
            dst = (sx - 110 + k * 110, sy + 50 + (k % 2) * 10)
            r = path_partial(c, [(sx - 220 + k * 150, sy + 360), dst], pr, paint("navy", stroke=8), curve=0.06)
            if r:
                arrow_head(c, *r, size=28, color="navy")
    label_tag(c, "Đồng minh đổ bộ", W / 2, 1160, pop_in(t, 89.6), size=36, anchor="center", bg="navy", fg="white")


def s17_grave(c, t):
    ph = A("grave_huelva")
    z = lerp(1.0, 1.06, prog(t, 91.52, 96.43, lambda q: q))
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.55, 0.45, z)
    label_tag(c, "NGHĨA TRANG HUELVA", 60, 1100, pop_in(t, 92.6), size=36)
    caption(c, "Ảnh: mộ \"William Martin\" ở Huelva, chụp sau này", 1190)
    pb = pop_in(t, 95.0)
    if pb > 0:
        r = skia.Rect.MakeXYWH(70, 840, 580, 82)
        c.drawRect(r, paint("yellow", 255 * pb, stroke=6, cap=False))
        label_tag(c, "WILLIAM MARTIN", 360, 790, pb, size=34, anchor="center", bg="yellow")


def s18_1998(c, t):
    ph = A("grave_huelva_close")
    z = lerp(1.25, 1.29, prog(t, 96.43, 104.6, lambda q: q))
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.55, 0.72, z)  # đẩy ba dòng khắc năm 1998 lên trên vùng phụ đề
    chip(c, "1998", W / 2, CHIP_Y, pop_in(t, 96.6))
    pb = pop_in(t, 100.1)
    if pb > 0:
        r = skia.Rect.MakeXYWH(90, 860, 900, 390)
        c.drawRect(r, paint("yellow", 255 * pb, stroke=7, cap=False))
    with Xf(c, 0, 0, 0, 1, pop_in(t, 100.4, 0.4)):
        card(c, 60, 360, 960, 150, "white", r=6)
        text(c, "\"Glyndwr Michael, đã phục vụ với", W / 2, 420, "bold", 36, "ink", align="center")
        text(c, "tư cách Thiếu tá William Martin\"", W / 2, 475, "bold", 36, "ink", align="center")
    caption(c, "Dòng chữ khắc thêm năm 1998 (CWGC); ảnh chụp sau này", 560)
    if t > 103.4:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("ink", 255 * prog(t, 103.4, 104.6, lambda q: q)))


RINGS = {"Spain": country_rings("Spain")}

TIMELINE = [
    (0.00, 6.65, s01_found),
    (6.65, 11.59, s02_case),
    (11.59, 16.07, s03_card),
    (16.07, 26.23, s04_med),
    (26.23, 31.84, s05_michael),
    (31.84, 35.92, s06_identity),
    (35.92, 48.22, s07_pocket),
    (48.22, 50.82, s08_pam),
    (50.82, 58.69, s09_generals),
    (58.69, 64.84, s10_letter),
    (64.84, 70.38, s11_seraph),
    (70.38, 74.57, s12_spain),
    (74.57, 76.87, s13_return),
    (76.87, 82.17, s14_decrypt),
    (82.17, 87.61, s15_moves),
    (87.61, 91.52, s16_sicily),
    (91.52, 96.43, s17_grave),
    (96.43, 104.70, s18_1998),
]


def draw_frame(c, t):
    for a, b, fn in TIMELINE:
        if a <= t < b:
            fn(c, t)
            break
