"""Bảng dựng tập Mona Lisa (phong cách Midway v2). Mốc giây theo MP3, xem build/words.json (ước lượng).
Quy tắc ảnh: chỉ dùng ảnh đã xác minh qua trang Commons trong ảnh chụp màn hình (xem BAN_GIAO.md)."""
import math
import skia
from lib import *  # noqa

PH = ROOT / "assets/photos"
CHIP_Y = 250
_assets = {}

PLACES.update({"paris": (2.35, 48.86), "florence": (11.25, 43.77)})


def A(key):
    if key not in _assets:
        _assets[key] = Map() if key == "map" else Photo(PH / f"{key}.jpg")
    return _assets[key]


def caption(c, s, y=1225, size=27, x=60):
    text(c, s, x, y, "semi", size, "white", a=235, stroke=3, stroke_color="ink")


def caption_dark(c, s, y, size=27, x=60):
    text(c, s, x, y, "semi", size, "grey")


def pop_in(t, t0, d=0.3):
    return prog(t, t0, t0 + d)


def mp(lon, lat, cam):
    return A("map").proj(lon, lat, cam)


def framed_crop_rect(ph, cx, cy, w, crop, rot=0.0, scale=1.0, alpha=1.0, border=16):
    """Như Photo.framed nhưng trả về (x0, y0, w, h) để đặt khung vàng theo toạ độ ảnh."""
    return ph.framed(c=None, cx=cx, cy=cy, w=w) if False else None


def ring_box(c, x, y, w, h, p, color="yellow", stroke=6):
    if p <= 0:
        return
    pth = skia.Path(); pth.addRect(skia.Rect.MakeXYWH(x, y, w, h))
    pm = skia.PathMeasure(pth, False); d = skia.Path(); pm.getSegment(0, pm.getLength() * clamp(p), d, True)
    c.drawPath(d, paint(color, stroke=stroke, cap=False))


def ring_oval(c, x, y, rx, ry, p, color="yellow", stroke=6):
    if p <= 0:
        return
    pth = skia.Path(); pth.addOval(skia.Rect.MakeXYWH(x - rx, y - ry, 2 * rx, 2 * ry))
    pm = skia.PathMeasure(pth, False); d = skia.Path(); pm.getSegment(0, pm.getLength() * clamp(p), d, True)
    c.drawPath(d, paint(color, stroke=stroke))


def mona(c, x, y, w, rot=0.0, alpha=1.0):
    A("mona_lisa_small").framed(c, x, y, w, rot=rot, alpha=alpha, border=6)


def trunk(c, x, y, s=1.0, lid=0.0, bottom=0.0, painting=0.0):
    """Rương gỗ cắt ngang: nắp mở (lid), đáy giả nhấc lên (bottom), tranh lộ ra (painting)."""
    with Xf(c, x, y, 0, s):
        shadow_begin(c, skia.Rect.MakeXYWH(-330, -320, 660, 560))
        c.drawRect(skia.Rect.MakeXYWH(-280, -120, 560, 300), paint("#6B4A2F"))
        c.restore()
        c.drawRect(skia.Rect.MakeXYWH(-260, -100, 520, 260), paint("#3E2A1C"))
        # ngăn bí mật dưới đáy giả
        c.drawRect(skia.Rect.MakeXYWH(-260, 110, 520, 50), paint("#2A1C12"))
        if painting > 0:
            with Xf(c, 0, 135 - 160 * painting, 90 if painting < 0.6 else lerp(90, 0, (painting - 0.6) / 0.4)):
                mona(c, 0, 0, 120 if painting < 0.6 else lerp(120, 230, (painting - 0.6) / 0.4))
        # đáy giả
        with Xf(c, 0, 100 - 160 * bottom, -12 * bottom):
            c.drawRect(skia.Rect.MakeXYWH(-255, -6, 510, 16), paint("#8A6542"))
        for k in range(3):
            c.drawRect(skia.Rect.MakeXYWH(-280, -60 + k * 90, 560, 10), paint("#4E3522"))
        # nắp
        with Xf(c, -280, -120, -100 * lid):
            c.drawRect(skia.Rect.MakeXYWH(0, -60, 560, 60), paint("#7A5636"))
            c.drawRect(skia.Rect.MakeXYWH(0, -60, 560, 60), paint("#4E3522", stroke=4, cap=False))


def camera_icon(c, x, y, s=1.0):
    with Xf(c, x, y, 0, s):
        c.drawRect(skia.Rect.MakeXYWH(-70, -50, 90, 100), paint("#3A3632"))
        bel = skia.Path(); bel.moveTo(20, -40); bel.lineTo(90, -25); bel.lineTo(90, 25); bel.lineTo(20, 40); bel.close()
        c.drawPath(bel, paint("#5A524A"))
        c.drawCircle(100, 0, 20, paint("#3A3632"))
        c.drawLine(-40, 50, -70, 160, paint("#3A3632", stroke=6)); c.drawLine(-20, 50, -20, 165, paint("#3A3632", stroke=6))
        c.drawLine(0, 50, 30, 160, paint("#3A3632", stroke=6))


def bubble(c, x, y, s, p, w=None, size=34, bg="white"):
    if p <= 0:
        return
    w = w or tw(s, "bold", size) + 60
    with Xf(c, x, y, 0, max(0.01, back_out(clamp(p))), clamp(p * 3)):
        card(c, -w / 2, -45, w, 90, bg, r=40)
        tail = skia.Path(); tail.moveTo(-20, 40); tail.lineTo(-50, 80); tail.lineTo(10, 42); tail.close()
        c.drawPath(tail, paint(bg))
        text(c, s, 0, 12, "bold", size, "ink", align="center")


# ------------------------------------------------------------------ CẢNH
def s01_louvre(c, t):
    ph = A("beroud_mona_lisa_au_louvre_1911")
    ph.blur_bg(c, 110)
    pe = pop_in(t, 0.0, 0.5)
    w = 1040
    h = ph.framed(c, W / 2, 680, w, rot=lerp(-2, -1, pe), scale=lerp(0.96, 1, pe) + 0.004 * t)
    chip(c, "THỨ HAI · 21.8.1911", W / 2, CHIP_Y, pop_in(t, 0.6))
    x0, y0 = W / 2 - w / 2, 680 - h / 2
    ring_box(c, x0 + 0.455 * w, y0 + 0.17 * h, 0.17 * w, 0.42 * h, prog(t, 3.8, 4.4))
    label_tag(c, "MONA LISA", x0 + 0.54 * w, y0 + 0.13 * h - 10, pop_in(t, 4.0), size=32, anchor="center", bg="yellow")
    label_tag(c, "LOUVRE · PARIS", 60, 1100, pop_in(t, 5.6), size=36)
    caption(c, "Tranh của Louis Béroud, \"Mona Lisa au Louvre\", 1911", 1180)


def s02_clock(c, t):
    draw_paper(c)
    p = prog(t, 7.0, 9.6, ease_in_out)
    cx, cy = 540, 700
    c.drawCircle(cx, cy, 250, paint("white"))
    c.drawCircle(cx, cy, 250, paint("ink", stroke=10))
    for k in range(12):
        a = k * math.pi / 6
        c.drawLine(cx + 215 * math.sin(a), cy - 215 * math.cos(a), cx + 238 * math.sin(a), cy - 238 * math.cos(a), paint("ink", stroke=6))
    hours = 7.5 + 28 * p  # khoảng 7 giờ 30 sáng thứ Hai → khoảng 11 giờ 30 sáng thứ Ba
    ah = hours / 12 * 2 * math.pi
    am = (hours % 1) * 2 * math.pi
    c.drawLine(cx, cy, cx + 130 * math.sin(ah), cy - 130 * math.cos(ah), paint("ink", stroke=14))
    c.drawLine(cx, cy, cx + 200 * math.sin(am), cy - 200 * math.cos(am), paint("red", stroke=7))
    c.drawCircle(cx, cy, 14, paint("ink"))
    day = "THỨ HAI" if hours < 24 else "THỨ BA"
    chip(c, day, W / 2, 360, 1, size=44, bg="yellow" if hours < 24 else "white")
    label_tag(c, "hơn một ngày", W / 2, 1060, pop_in(t, 7.8), size=40, anchor="center", bg="red", fg="white")


def s03_beroud(c, t):
    if t < 14.27:
        ph = A("beroud_mona_lisa_au_louvre_1911")
        z = lerp(1.0, 1.06, prog(t, 10.07, 14.27, lambda q: q))
        ph.cover(c, skia.Rect.MakeWH(W, H), 0.55, 0.5, z)
        name_tag(c, 60, 1000, "Louis Béroud", "họa sĩ · hay tới Louvre vẽ tranh", pop_in(t, 10.6, 0.4), size=48, role_size=30)
        chip(c, "THỨ BA · 22.8.1911", W / 2, CHIP_Y, pop_in(t, 12.2))
        caption(c, "Tranh của chính Béroud vẽ phòng trưng bày này, 1911", 1190)
        return
    ph = A("empty_wall_1911")
    z = lerp(1.0, 1.05, prog(t, 14.27, 16.31, lambda q: q))
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.47, 0.32, z)
    chip(c, "THỨ BA · 22.8.1911", W / 2, CHIP_Y, 1)
    for k, (hx, hy) in enumerate(HOOKS):
        ring_oval(c, hx, hy, 34, 34, prog(t, 15.1 + k * 0.12, 15.4 + k * 0.12))
    label_tag(c, "bốn cái móc sắt", W / 2, 1060, pop_in(t, 15.3), size=38, anchor="center", bg="yellow")
    caption(c, "Ảnh: chỗ treo Mona Lisa sau vụ trộm, 1911", 1190)


HOOKS = [(425, 695), (640, 692), (345, 965), (688, 952)]  # căn theo ảnh bức tường trống (xem bản xem thử)


def s04_guards(c, t):
    draw_paper(c)
    with Xf(c, 0, 0, 0, 1, pop_in(t, 16.4)):
        card(c, 560, 560, 420, 420, "white", r=8)
        camera_icon(c, 740, 740, 1.4)
        text(c, "BÊN CHỤP ẢNH", 770, 615, "xbold", 30, "ink", align="center")
    person(c, 400, 980, 1.6, "navy")
    bubble(c, 470, 520, "\"đi chụp ảnh rồi\"", pop_in(t, 16.4), size=36)
    label_tag(c, "lính gác", 400, 1030, pop_in(t, 16.5), size=32, anchor="center", bg="navy", fg="white")
    person(c, 150, 980, 1.5, "#7A715E")
    label_tag(c, "Béroud", 150, 1030, pop_in(t, 21.0), size=30, anchor="center")
    label_tag(c, "Louvre đang chụp lại các tác phẩm", 770, 1040, pop_in(t, 18.7) * (1 - prog(t, 20.9, 21.1)), size=28, anchor="center")
    for k in range(3):
        bubble(c, 120 + k * 70, 640 - k * 70, "!", pop_in(t, 21.1 + k * 0.35), w=90, size=46, bg="yellow")
    label_tag(c, "giục mấy lần", 40, 1110, pop_in(t, 21.2) * (1 - prog(t, 23.0, 23.2)), size=32, bg="yellow")
    stamp(c, "KHÔNG GIỮ", 770, 800, prog(t, 23.9, 24.1), size=62, rot=-8)


def s05_peruggia(c, t):
    draw_paper(c)
    pe = pop_in(t, 25.18, 0.35)
    A("peruggia_bertillon_card").framed(c, W / 2, 650, 560, rot=lerp(-4, -2, pe), scale=lerp(0.94, 1, pe) + 0.005 * max(0, t - 25.5),
                                         crop=(0.50, 0.20, 0.96, 0.82))
    name_tag(c, 60, 1000, "Vincenzo Peruggia", "thợ người Ý · từng làm việc ở Louvre", pop_in(t, 25.6, 0.4), size=48, role_size=30)
    stamp(c, "ĐÓNG CỬA", 800, 400, prog(t, 29.8, 30.0), size=56, color="red", rot=-10)
    label_tag(c, "chỉ nhân viên ra vào", 800, 490, pop_in(t, 30.6), size=30, anchor="center")


PANELS = [  # (x0, y0, x1, y1) theo tỉ lệ ảnh minh họa, thời điểm vào
    ((0.00, 0.00, 1.00, 1.00), 31.76),
    ((0.00, 0.00, 0.28, 0.30), 34.10),   # gỡ tranh
    ((0.27, 0.00, 0.53, 0.30), 35.25),   # mang đi
    ((0.52, 0.00, 0.78, 0.30), 36.25),   # bỏ khung
    ((0.77, 0.00, 1.00, 0.30), 37.45),   # ra ngoài
]


def s06_theft(c, t):
    if t >= 39.3:
        draw_paper(c)
        p = pop_in(t, 39.3, 0.4)
        mona(c, 600, 700, 330, rot=-2, alpha=clamp(p * 2))
        x = 400
        c.drawLine(x, 700 - 250, x, 700 + 250, paint("ink", stroke=6))
        for k in range(9):
            c.drawLine(x - 18, 700 - 250 + k * 62.5, x, 700 - 250 + k * 62.5, paint("ink", stroke=4))
        label_tag(c, "77 cm", x - 30, 700, p, size=44, anchor="right", bg="yellow")
        label_tag(c, "chưa tới tám mươi phân", W / 2, 1110, pop_in(t, 39.7), size=36, anchor="center")
        return
    ph = A("press_illustration_theft")
    ph.blur_bg(c, 130)
    # camera đi qua từng khung theo động tác
    cur = PANELS[0][0]
    for k in range(1, len(PANELS)):
        if t >= PANELS[k][1] - 0.3:
            pk = prog(t, PANELS[k][1] - 0.3, PANELS[k][1] + 0.2, ease_in_out)
            cur = tuple(lerp(a, b, pk) for a, b in zip(cur, PANELS[k][0]))
    x0, y0, x1, y1 = cur
    pw, phh = ph.w * (x1 - x0), ph.h * (y1 - y0)
    s = min(1000 / pw, 1000 / phh)
    dw, dh = pw * s, phh * s
    with Xf(c, W / 2, 680, -1, 1, pop_in(t, 31.76)):
        card(c, -dw / 2 - 14, -dh / 2 - 14, dw + 28, dh + 28, "white", r=3)
        c.drawImageRect(ph.img, skia.Rect.MakeXYWH(x0 * ph.w, y0 * ph.h, pw, phh), skia.Rect.MakeXYWH(-dw / 2, -dh / 2, dw, dh), SAMP, None, skia.Canvas.kStrict_SrcRectConstraint)
    labels = [(32.0, "áo khoác trắng như thợ"), (34.1, "gỡ tranh xuống"), (35.25, "mang ra cầu thang"), (36.25, "tháo khung và kính"), (37.45, "giấu dưới áo, đi ra")]
    cur_lab = None
    for ts, lab in labels:
        if t >= ts:
            cur_lab = (ts, lab)
    if cur_lab:
        label_tag(c, cur_lab[1], W / 2, 1110, pop_in(t, cur_lab[0]), size=36, anchor="center", bg="yellow")
    caption(c, "Tranh minh họa báo chí tái hiện vụ trộm (không phải ảnh chụp)", 1190)


def s07_print(c, t):
    if t < 44.6:
        draw_paper(c)
        p = pop_in(t, 41.4, 0.4)
        with Xf(c, 540, 700, -3, lerp(0.9, 1, ease_out(p)), clamp(p * 2)):
            card(c, -260, -340, 520, 680, "#C9A55A", r=6)
            c.drawRect(skia.Rect.MakeXYWH(-210, -290, 420, 580), paint("#E8EEF0", 230))
            c.drawLine(-180, -250, 150, 240, paint("white", 160, stroke=6))
        label_tag(c, "khung và kính bỏ lại", W / 2, 300, pop_in(t, 41.6), size=34, anchor="center")
        pf = pop_in(t, 43.1, 0.4)
        if pf > 0:
            for k in range(7):
                c.drawOval(skia.Rect.MakeXYWH(590 - k * 10, 640 - k * 12, 40 + k * 20, 56 + k * 24), paint("ink", 180 * pf, stroke=3))
            ring_oval(c, 620, 680, 120, 130, pf)
            label_tag(c, "DẤU VÂN TAY", 620, 860, pf, size=36, anchor="center", bg="yellow")
        return
    if t < 47.89:
        ph = A("peruggia_bertillon_card")
        ph.blur_bg(c, 120)
        w = 1000
        h = ph.framed(c, W / 2, 680, w, rot=-1, scale=1 + 0.004 * (t - 44.6))
        x0, y0 = W / 2 - w / 2, 680 - h / 2
        ring_box(c, x0 + 0.06 * w, y0 + 0.62 * h, 0.21 * w, 0.06 * h, prog(t, 44.9, 45.4))
        label_tag(c, "từng bị bắt: hồ sơ 1909", 60, 1090, pop_in(t, 45.0), size=32, bg="yellow")
        ring_box(c, x0 + 0.01 * w, y0 + 0.78 * h, 0.98 * w, 0.21 * h, prog(t, 46.6, 47.2))
        caption(c, "Thẻ hồ sơ cảnh sát của Peruggia, có vân tay tay phải", 1170)
        return
    draw_paper(c)
    label_tag(c, "kho hồ sơ xếp theo số đo cơ thể", W / 2, 330, pop_in(t, 47.95), size=34, anchor="center")
    labs = ["CHIỀU CAO", "VÒNG ĐẦU", "CHIỀU DÀI TAI", "SẢI TAY", "BÀN CHÂN", "NGÓN GIỮA"]
    for k, lab in enumerate(labs):
        pk = pop_in(t, 48.1 + k * 0.12)
        if pk <= 0:
            continue
        r, col_ = divmod(k, 2)
        x, y = 290 + col_ * 500, 520 + r * 190
        with Xf(c, x, y, 0, max(0.01, back_out(pk)), clamp(pk * 3)):
            card(c, -220, -70, 440, 140, "#B9AE96", r=6)
            c.drawRoundRect(skia.Rect.MakeXYWH(-60, -18, 120, 36), 12, 12, paint("#8E846F"))
            text(c, lab, 0, 56, "bold", 26, "ink", align="center")
    pq = pop_in(t, 50.1, 0.35)
    if pq > 0:
        for k in range(5):
            c.drawOval(skia.Rect.MakeXYWH(510 - k * 9, 1050 - k * 10, 30 + k * 18, 42 + k * 20), paint("ink", 180 * pq, stroke=3))
        label_tag(c, "chỉ có dấu vân tay → không dò ra", W / 2, 1180, pq, size=32, anchor="center", bg="red", fg="white")


def s08_suspects(c, t):
    draw_paper(c)
    if t < 57.12:
        if t < 54.4:
            pe = pop_in(t, 51.47, 0.35)
            A("apollinaire_sept_1911").framed(c, W / 2, 660, 560, rot=lerp(-4, -2, pe), scale=lerp(0.94, 1, pe) + 0.005 * max(0, t - 51.8))
            name_tag(c, 60, 1010, "Guillaume Apollinaire", "nhà thơ · bị bắt giam mấy ngày", pop_in(t, 52.3, 0.4), size=44, role_size=30)
            caption_dark(c, "Ảnh chụp tháng 9/1911", 1200)
        else:
            pe = pop_in(t, 54.4, 0.35)
            A("picasso_studio_1908").framed(c, W / 2, 660, 560, rot=lerp(4, 2, pe), scale=lerp(0.94, 1, pe) + 0.005 * max(0, t - 54.7))
            name_tag(c, 60, 1010, "Pablo Picasso", "họa sĩ · bị gọi lên thẩm vấn", pop_in(t, 54.8, 0.4), size=44, role_size=30)
            caption_dark(c, "Ảnh: Picasso trong xưởng vẽ ở Montmartre, 1908", 1200)
        return
    A("apollinaire_sept_1911").framed(c, 300, 680, 400, rot=-3)
    A("picasso_studio_1908").framed(c, 780, 680, 400, rot=3)
    stamp(c, "KHÔNG LIÊN QUAN", 540, 1060, prog(t, 57.6, 57.85), size=60, color="navy", rot=-6)


def s09_room(c, t):
    draw_paper(c)
    c.drawRect(skia.Rect.MakeXYWH(0, 980, W, 300), paint("#B9AE96"))
    trunk(c, 640, 860, 0.9, painting=0.0)
    # cắt ngang: thấy tranh nằm dưới đáy giả
    pr = pop_in(t, 63.3, 0.5)
    if pr > 0:
        with Xf(c, 640, 860 + 0.9 * 135, 90, 1, pr):
            mona(c, 0, 0, 108)
        ring_box(c, 640 - 240, 860 + 0.9 * 108, 480, 0.9 * 55, prog(t, 63.6, 64.2))
        label_tag(c, "đáy giả", 640, 860 + 0.9 * 230, pop_in(t, 64.0), size=34, anchor="center", bg="yellow")
    person(c, 200, 980, 1.1, "navy")
    label_tag(c, "cảnh sát", 200, 760, pop_in(t, 59.2), size=30, anchor="center", bg="navy", fg="white")
    bubble(c, 300, 600, "hỏi chuyện…", pop_in(t, 59.6), size=32)
    label_tag(c, "không khám xét kỹ", W / 2, 360, pop_in(t, 61.5), size=36, anchor="center", bg="red", fg="white")
    label_tag(c, "phòng trọ của Peruggia", W / 2, 440, pop_in(t, 59.3), size=30, anchor="center")


def person(c, x, y, s=1.0, color="grey"):
    with Xf(c, x, y, 0, s):
        c.drawCircle(0, -150, 22, paint(color))
        body = skia.Path()
        body.moveTo(-30, -120); body.lineTo(30, -120); body.lineTo(26, -40); body.lineTo(16, 0)
        body.lineTo(4, 0); body.lineTo(0, -40); body.lineTo(-4, 0); body.lineTo(-16, 0); body.lineTo(-26, -40); body.close()
        c.drawPath(body, paint(color))
        c.drawRect(skia.Rect.MakeXYWH(-30, -182, 60, 14), paint(color))


def s10_press(c, t):
    if t < 68.46:
        draw_paper(c)
        heads = ["MONA LISA BIẾN MẤT", "LOUVRE MẤT TRANH", "AI LẤY MONA LISA?"]
        for k, hd in enumerate(heads):
            p = pop_in(t, 66.6 + k * 0.4, 0.35)
            if p <= 0:
                continue
            with Xf(c, 540 + (k - 1) * 120, 520 + k * 230, (k - 1) * 6, max(0.01, back_out(p)), clamp(p * 3)):
                card(c, -330, -110, 660, 220, "#F1EAD7", r=2)
                text(c, hd, 0, -30, "xbold", 44, "ink", align="center")
                for q in range(3):
                    c.drawLine(-290, 20 + q * 28, 290 - q * 40, 20 + q * 28, paint("grey", 140, stroke=5))
        note_label(c, "MINH HỌA", 820, 330, 1)
        return
    ph = A("empty_wall_1911")
    z = lerp(1.0, 1.05, prog(t, 68.46, 71.34, lambda q: q))
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.47, 0.40, z)
    label_tag(c, "người ta xếp hàng để nhìn khoảng tường trống", W / 2, 1100, pop_in(t, 69.0), size=30, anchor="center", bg="yellow")


def s11_letter(c, t):
    if t < 72.25:
        draw_paper(c)
        n = int(lerp(1911, 1913, prog(t, 71.4, 72.1)))
        text(c, str(n), W / 2, 760, "xbold", 220, "ink", align="center")
        label_tag(c, "hai năm trôi qua", W / 2, 480, pop_in(t, 71.4), size=38, anchor="center", bg="yellow")
        return
    m = A("map")
    cam = drift_cam((7.0, 46.4, 70.0), t, 72.25, 0.008)
    m.draw(c, cam)
    chip(c, "CUỐI 1913", W / 2, CHIP_Y, pop_in(t, 72.3))
    px, py = mp(*PLACES["paris"], cam)
    fx, fy = mp(*PLACES["florence"], cam)
    pin(c, px, py, 1, color="white")
    label_tag(c, "PARIS", px - 24, py - 44, 1, size=32, anchor="right")
    pin(c, fx, fy, pop_in(t, 74.6))
    label_tag(c, "FLORENCE", fx + 24, fy - 44, pop_in(t, 74.6), size=32, bg="yellow")
    label_tag(c, "Alfredo Geri · người bán đồ cổ", fx - 30, fy + 70, pop_in(t, 75.3), size=28, anchor="center")
    pl = pop_in(t, 76.5, 0.45)
    if pl > 0:
        with Xf(c, 540, 1000, 2, lerp(0.85, 1, ease_out(pl)), clamp(pl * 2)):
            card(c, -360, -150, 720, 300, "#F6EFE0", r=4)
            note_label(c, "DIỄN Ý", 210, -130, 1)
            text(c, typed("Tôi đang giữ Mona Lisa", prog(t, 78.3, 79.7, lambda q: q)), -320, -50, "ital", 40, "#2E3550")
            text(c, typed("và muốn đưa nó về Ý.", prog(t, 79.9, 80.8, lambda q: q)), -320, 10, "ital", 40, "#2E3550")
            text(c, "— \"Leonardo\"", 330, 110, "ital", 44, "#2E3550", align="right")


def s12_hotel(c, t):
    draw_paper(c)
    if t < 85.73:
        p1 = pop_in(t, 81.2, 0.4)
        p2 = pop_in(t, 84.4, 0.4)
        name_tag(c, 90, 520, "Alfredo Geri", "người bán đồ cổ ở Florence", p1, size=46, role_size=30)
        name_tag(c, 90, 760, "Giovanni Poggi", "giám đốc bảo tàng Uffizi", p2, size=46, role_size=30)
        label_tag(c, "hẹn gặp \"Leonardo\"", W / 2, 1060, pop_in(t, 81.4), size=34, anchor="center", bg="yellow")
        return
    if t < 89.14:
        label_tag(c, "phòng khách sạn ở Florence", W / 2, 330, pop_in(t, 85.8), size=34, anchor="center")
        trunk(c, 540, 780, 1.0, lid=prog(t, 86.8, 87.4, ease_in_out), bottom=prog(t, 88.0, 88.6, ease_in_out),
              painting=prog(t, 88.4, 89.1, ease_in_out))
        label_tag(c, "nhấc đáy giả", W / 2, 1110, pop_in(t, 88.0), size=34, anchor="center", bg="yellow")
        return
    # mặt sau bức tranh có dấu Louvre (minh họa)
    with Xf(c, 540, 700, -2, lerp(0.9, 1, pop_in(t, 89.14, 0.4))):
        card(c, -250, -360, 500, 720, "#B48A5C", r=4)
        for k in range(9):
            c.drawLine(-230, -330 + k * 80, 230, -320 + k * 80, paint("#9A7448", stroke=3))
    with Xf(c, 540, 640, -12, lerp(1.6, 1, pop_in(t, 89.9, 0.25)), pop_in(t, 89.9, 0.25)):
        c.drawCircle(0, 0, 110, paint("ink", 220, stroke=6))
        c.drawCircle(0, 0, 90, paint("ink", 220, stroke=3))
        text(c, "MUSÉE", 0, -12, "xbold", 34, "ink", a=220, align="center")
        text(c, "DU LOUVRE", 0, 32, "xbold", 30, "ink", a=220, align="center")
    note_label(c, "MINH HỌA", 820, 330, 1)
    label_tag(c, "mặt sau tranh: dấu của Louvre", W / 2, 1150, pop_in(t, 89.5), size=34, anchor="center", bg="yellow")


def s13_found(c, t):
    if t < 93.82:
        ph = A("uffizi_1913")
        ph.blur_bg(c, 120)
        pe = pop_in(t, 91.08, 0.35)
        ph.framed(c, W / 2, 660, 760, rot=lerp(-3, -1, pe), scale=lerp(0.95, 1, pe) + 0.006 * max(0, t - 91.4))
        label_tag(c, "giữ lại để kiểm tra", 60, 1110, pop_in(t, 91.6), size=34, bg="yellow")
        caption(c, "Ảnh: Mona Lisa ở Uffizi, Florence, 12/1913", 1190)
        return
    ph = A("petit_parisien_13dec1913")
    ph.blur_bg(c, 120)
    w = 860
    h = ph.framed(c, W / 2, 690, w, rot=1, scale=1 + 0.006 * (t - 93.82))
    x0, y0 = W / 2 - w / 2, 690 - h / 2
    ring_box(c, 392, 212, 446, 66, prog(t, 94.1, 94.6))
    label_tag(c, "Peruggia bị bắt tại khách sạn", W / 2, 1180, pop_in(t, 94.3), size=32, anchor="center", bg="red", fg="white")
    caption(c, "Le Petit Parisien, 13/12/1913: \"La Joconde est retrouvée\"", 1240)


def s14_trial(c, t):
    draw_paper(c)
    ph = A("press_illustration_theft")
    pe = pop_in(t, 95.74, 0.35)
    ph.framed(c, W / 2, 620, 520, rot=lerp(-4, -2, pe), scale=lerp(0.94, 1, pe), crop=(0.30, 0.31, 0.72, 0.73))
    label_tag(c, "\"trả tranh về quê hương Leonardo\"", W / 2, 960, pop_in(t, 97.7), size=32, anchor="center", bg="yellow")
    pv = pop_in(t, 100.6, 0.3)
    if pv > 0:
        chip(c, "TÒA XỬ NHẸ", W / 2, 330, pv, size=40, bg="navy", fg="white")
    p1 = pop_in(t, 101.6, 0.3)
    if p1 > 0:
        w1 = tw("hơn 1 năm tù", "xbold", 56)
        text(c, "hơn 1 năm tù", W / 2, 1110, "xbold", 56, "ink", a=255 * p1, align="center")
        ps = prog(t, 103.0, 103.3)
        if ps > 0:
            c.drawLine(W / 2 - w1 / 2 - 10, 1090, W / 2 - w1 / 2 - 10 + (w1 + 20) * ps, 1090, paint("red", stroke=8))
    chip(c, "còn 7 tháng", W / 2, 1200, pop_in(t, 103.3), size=44)
    caption_dark(c, "Chân dung Peruggia trong tranh minh họa báo chí", 1250 - 2, 25)


def s15_return(c, t):
    ph = A("return_louvre_1914")
    ph.blur_bg(c, 120)
    pe = pop_in(t, 104.66, 0.35)
    ph.framed(c, W / 2, 660, 1010, rot=lerp(-2, -1, pe), scale=lerp(0.95, 1, pe) + 0.005 * max(0, t - 105.0))
    chip(c, "4 THÁNG 1 · 1914", W / 2, CHIP_Y, pop_in(t, 104.75))
    caption(c, "Ảnh: Mona Lisa trở về Louvre, 1914", 1020)
    label_tag(c, "28 tháng biến mất", W / 2, 1110, pop_in(t, 108.6), size=40, anchor="center", bg="yellow")
    if t > 110.0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("ink", 255 * prog(t, 110.0, 111.3, lambda q: q)))


TIMELINE = [
    (0.00, 6.84, s01_louvre),
    (6.84, 10.07, s02_clock),
    (10.07, 16.31, s03_beroud),
    (16.31, 25.18, s04_guards),
    (25.18, 31.76, s05_peruggia),
    (31.76, 41.38, s06_theft),
    (41.38, 51.47, s07_print),
    (51.47, 59.05, s08_suspects),
    (59.05, 66.58, s09_room),
    (66.58, 71.34, s10_press),
    (71.34, 81.14, s11_letter),
    (81.14, 91.08, s12_hotel),
    (91.08, 95.74, s13_found),
    (95.74, 104.66, s14_trial),
    (104.66, 111.40, s15_return),
]


def draw_frame(c, t):
    for a, b, fn in TIMELINE:
        if a <= t < b:
            fn(c, t)
            break
