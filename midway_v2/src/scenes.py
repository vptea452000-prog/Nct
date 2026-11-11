"""Bảng dựng Midway v2 dưới dạng mã. Mỗi cảnh: (vào, ra, hàm vẽ). Mốc giây theo MP3 (ước lượng, xem words.json)."""
import math
import skia
from lib import *  # noqa

PH = ROOT / "assets/photos"
CHIP_Y = 250

_assets = {}


def A(key):
    if key not in _assets:
        if key == "map":
            _assets[key] = Map()
        else:
            _assets[key] = Photo(PH / f"{key}.jpg")
    return _assets[key]


def caption(c, s, y=1225, size=27, x=60):
    """Chú thích nguồn ảnh nhỏ (≥26px)."""
    text(c, s, x, y, "semi", size, "white", a=235, stroke=3, stroke_color="ink")


# ------------------------------------------------------------------ máy ảnh bản đồ
CAM_HM = (192.5, 21.0, 30.0)      # Hawaii – Midway
CAM_JP = (165.0, 30.0, 12.5)      # Nhật – Midway – Hawaii
CAM_HM2 = (190.0, 25.0, 22.0)     # kịch bản đoán nhầm
CAM_PAC = (165.0, 2.0, 10.0)      # có cả Melbourne


def mp(lon, lat, cam):
    return A("map").proj(lon, lat, cam)


def place_pins(c, cam, t, which, t_on=None):
    t_on = t_on or {}
    labels = {"midway": ("MIDWAY", 26, -44, "left"), "oahu": ("HAWAII", -26, -44, "right"),
              "tokyo": ("NHẬT BẢN", -20, -46, "left"), "melbourne": ("MELBOURNE · ÚC", 26, -44, "left")}
    for k in which:
        x, y = mp(*PLACES[k], cam)
        p = prog(t, t_on.get(k, -10), t_on.get(k, -10) + 0.35)
        pin_burst(c, x, y, t, t_on.get(k, -10) + 0.12)
        pin(c, x, y, p)
        s, dx, dy, an = labels[k]
        label_tag(c, s, x + dx, y + dy, p, size=32, anchor=an)


# ------------------------------------------------------------------ CẢNH
def s01_atoll(c, t):
    ph = A("atoll")
    z = lerp(1.50, 1.30, prog(t, 0, 0.9)) - 0.03 * clamp(t / 2.65)
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.34, 0.60, z)
    film(c, t)
    chip(c, "20 THÁNG 5 · 1942", W / 2, CHIP_Y, prog(t, 0.40, 0.75))
    label_tag(c, "ĐẢO MIDWAY", 60, 1120, prog(t, 0.9, 1.2), size=40)
    caption(c, "Ảnh: Hải quân Mỹ, chụp 11/1941", 1190)


def msg_card(c, x, y, t, t_type0, t_type1, t_hl, t_l3=None, scale=1.0, alpha=1.0, done=False):
    """Bức điện cầu cứu của Midway (tái hiện, DIỄN Ý)."""
    w, h = 900, 340
    with Xf(c, x, y, -1.2, scale, alpha):
        card(c, 0, 0, w, h, "white", r=4)
        text(c, "MIDWAY → HAWAII · 20/5/1942", 36, 54, "mono", 30, "grey")
        note_label(c, "DIỄN Ý", w - 150, 22, 1)
        l1, l2 = "NƯỚC NGỌT CHỈ CÒN", "ĐỦ DÙNG HAI TUẦN."
        full = l1 + " " + l2
        p = 1 if done else prog(t, t_type0, t_type1, lambda q: q)
        s = typed(full, p)
        a1, a2 = s[:len(l1)], s[len(l1) + 1:]
        fx = font("mono", 50)
        pre = fx.measureText(nfc("ĐỦ DÙNG "))
        hw = fx.measureText(nfc("HAI TUẦN"))
        highlight(c, 36 + pre, 186, hw, 58, 1 if done else prog(t, t_hl, t_hl + 0.3))
        w1 = text(c, a1, 36, 140, "mono", 50)
        w2 = text(c, a2, 36, 230, "mono", 50)
        p3 = 1 if done else prog(t, t_l3, t_l3 + 0.75, lambda q: q) if t_l3 is not None else 0
        if t_l3 is not None:
            w3 = text(c, typed("XIN TIẾP TẾ NGAY.", p3), 36, 310, "mono", 50)
        if not done:
            if 0 < p < 1:
                cursor(c, 36 + (w2 if a2 else w1), 230 if a2 else 140, t, 50)
            elif t_l3 is not None and 0 < p3 < 1:
                cursor(c, 36 + w3, 310, t, 50)


def s02_map_msg(c, t):
    m = A("map")
    # 2.65–10.0 Hawaii–Midway; 10.0–11.0 kéo bản đồ sang để thấy Nhật
    cam = drift_cam(cam_lerp(CAM_HM, CAM_JP, prog(t, 10.0, 11.0, ease_in_out)), t, 2.65, 0.007)
    m.draw(c, cam)
    mx, my = mp(*PLACES["midway"], cam)
    ox, oy = mp(*PLACES["oahu"], cam)
    # mũi tên Midway → Hawaii (báo về Hawaii)
    a_out = 1 - prog(t, 9.9, 10.3)
    if a_out > 0:
        r = path_partial(c, [(mx, my), (ox, oy)], prog(t, 3.68, 4.40), paint("ink", 255 * a_out, stroke=6), curve=-0.22)
        if r and prog(t, 3.68, 4.40) > 0.05:
            arrow_head(c, *r, size=24, a=255 * a_out)
    place_pins(c, cam, t, ["midway", "oahu"], {"midway": 3.25, "oahu": 3.95})
    # sóng vô tuyến từ Midway tới phía Nhật
    rings(c, mx, my, t, 10.69, 12.3, "ink", max_r=900, period=0.42, width=5)
    tx, ty = mp(*PLACES["tokyo"], cam)
    pj = prog(t, 11.30, 11.6)
    pulse = 1 + 0.25 * math.sin(clamp((t - 11.71) / 0.35) * math.pi) if t > 11.71 else 1
    antenna_icon(c, tx + 40, ty - 70, pj, "red", s=1.2 * pulse)
    label_tag(c, "QUÂN NHẬT", tx + 10, ty - 150, pj, size=32, bg="red", fg="white")
    # thẻ điện cầu cứu
    if t < 10.6:
        pin_in = prog(t, 4.30, 4.75)
        fly = prog(t, 10.0, 10.55, ease_in_out)
        x = lerp(90, mx - 45, fly)
        y = lerp(lerp(1500, 830, pin_in), my - 15, fly)
        msg_card(c, x, y, t, 4.89, 6.15, 5.85, 6.56, scale=lerp(1, 0.1, fly), alpha=clamp(pin_in * 2) * (1 - fly * 0.6))
        if fly < 0.05:
            stamp(c, "MỒI NHỬ", 790, 1135, prog(t, 9.35, 9.6), size=60, rot=-9)


def doc_tokens():
    # (mã, chữ giải được hoặc None nếu vẫn chưa đọc được, thời điểm lật)
    return [
        [("38104", "HẠM ĐỘI", 18.70), ("22063", None, 0), ("51390", "TẬP KẾT", 19.30)],
        [("70415", None, 0), ("19337", "CHIẾN DỊCH LỚN", 19.75)],
        [("44781", "THÁNG 6", 20.20), ("90562", None, 0), ("31208", None, 0)],
    ]


def s05_decrypt(c, t):
    draw_paper(c)
    z = lerp(1.0, 1.10, prog(t, 25.0, 25.7, ease_in_out))
    # phóng về hàng MỤC TIÊU (y≈1000), giữ đủ lề trái của tài liệu
    fx, fy = 540, 1000
    c.save()
    c.translate(fx, fy)  # giữ hàng MỤC TIÊU tại chỗ để tài liệu không lấn vùng 0–180 px
    c.scale(z, z)
    c.translate(-fx, -fy)
    c.rotate(lerp(-0.8, 0.4, clamp((t - 18.28) / 11.7)), 540, 760)
    x0, y0, w, h = 80, 360, 920, 760
    with Xf(c, 0, 0, 0.0):
        card(c, x0, y0, w, h, "white", r=4)
    text(c, "ĐIỆN MẬT · HẢI QUÂN NHẬT", x0 + 40, y0 + 70, "mono", 34, "grey")
    note_label(c, "MINH HỌA", x0 + w - 190, y0 + 30, 1)
    c.drawLine(x0 + 40, y0 + 100, x0 + w - 40, y0 + 100, paint("grey", 120, stroke=2))
    fm = font("mono", 46)
    y = y0 + 190
    for row in doc_tokens():
        x = x0 + 40
        for code, plain, tf in row:
            dec = plain is not None and t >= tf
            if plain is not None and tf <= t < tf + 0.25:  # chữ nhảy khi giải mã
                s = "".join("0123456789"[int((t * 40 + i * 7) % 10)] for i in range(5))
                colr = "ink"
            elif dec:
                s, colr = plain, "ink"
            else:
                s, colr = code, "grey"
            s = nfc(s)
            ww = fm.measureText(s)
            if dec and plain == "CHIẾN DỊCH LỚN":
                highlight(c, x, y - 44, ww, 58, prog(t, 23.75, 24.1))
            if dec and plain == "THÁNG 6":
                highlight(c, x, y - 44, ww, 58, prog(t, 24.50, 24.8))
            text(c, s, x, y, "mono", 46, colr, a=255 if dec else 150)
            x += ww + 46
        y += 130
    # hàng MỤC TIÊU
    yt = 1000
    if t < 25.17:
        text(c, "47215  80936", x0 + 40, yt, "mono", 46, "grey", a=150)
    else:
        text(c, "MỤC TIÊU:", x0 + 40, yt, "mono", 50, "ink")
        bx, by, bw, bh = x0 + 360, yt - 70, 300, 100
        if t < 29.26:
            blink = 255 if int((t - 25.17) * 2.5) % 2 == 0 else 110
            c.drawRect(skia.Rect.MakeXYWH(bx, by, bw, bh), paint("ink", blink, stroke=5, cap=False))
            if t > 27.2:
                text(c, "?  ?", bx + bw / 2, yt, "mono", 50, "grey", a=200 * prog(t, 27.2, 27.6), align="center")
        else:
            p = prog(t, 29.22, 29.45, back_out)
            burst(c, bx + bw / 2, by + bh / 2, t, 29.24, "yellow", r0=170, r1=330)
            with Xf(c, bx + bw / 2, by + bh / 2, 0, lerp(1.6, 1.0, clamp(p))):
                c.drawRect(skia.Rect.MakeXYWH(-bw / 2, -bh / 2, bw, bh), paint("yellow"))
                c.drawRect(skia.Rect.MakeXYWH(-bw / 2, -bh / 2, bw, bh), paint("ink", stroke=5, cap=False))
                text(c, "AF", 0, 34, "xbold", 96, "ink", align="center")
    c.restore()


def s07_map_af(c, t):
    m = A("map")
    cam = drift_cam(cam_lerp(CAM_JP, (170.0, 20.0, 10.0), prog(t, 33.4, 34.4, ease_in_out)), t, 29.96, 0.01)
    m.draw(c, cam)
    place_pins(c, cam, t, ["midway", "oahu", "tokyo"], {"midway": 29.9, "oahu": 29.9, "tokyo": 29.9})
    mx, my = mp(*PLACES["midway"], cam)
    fly = prog(t, 32.0, 32.45, ease_in_out)
    pulse = 1 + 0.15 * math.sin(clamp((t - 31.46) / 0.3) * math.pi) if 31.46 < t < 31.8 else 1
    s = "AF = ?" if fly < 0.5 else "AF"
    x = lerp(W / 2, mx, fly)
    y = lerp(470, my + 70, fly)
    with Xf(c, x, y, 0, pulse):
        chip(c, s, 0, 0, prog(t, 30.0, 30.35), size=lerp(56, 40, fly))
    pa = prog(t, 33.7, 34.1)
    if pa > 0:
        with Xf(c, 0, 0, 0, 1, pa):
            text(c, "THÁI BÌNH DƯƠNG", W / 2, 1010, "ital", 46, "ink", a=200, align="center")


def s08_pearl(c, t):
    ph = A("yorktown")
    ph.blur_bg(c)
    ph.framed(c, W / 2, 700, 1000, rot=lerp(-3.0, -1.0, prog(t, 34.69, 35.1)), scale=lerp(0.95, 1.0, prog(t, 34.69, 35.1)) + 0.008 * max(0, t - 35.1))
    chip(c, "TRÂN CHÂU CẢNG · HAWAII", W / 2, CHIP_Y, prog(t, 34.75, 35.1), size=38)
    caption(c, "Ảnh: Trân Châu Cảng, 29/5/1942 (Hải quân Mỹ)", 1160)
    label_tag(c, "AF = nơi khác?", 120, 470, prog(t, 36.2, 36.5) * (1 - prog(t, 36.85, 37.0)), size=38, bg="white", fg="grey")
    chip(c, "AF = HAWAII?", W / 2, 720, prog(t, 36.92, 37.25), size=64)


def s09_nimitz(c, t):
    ph = A("nimitz")
    z = lerp(1.12, 1.0, prog(t, 37.69, 38.2)) + 0.014 * max(0, t - 38.2)
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.5, 0.36, z)
    film(c, t)
    name_tag(c, 60, 1000, "Đô đốc Chester Nimitz", "Tư lệnh Hạm đội Thái Bình Dương", prog(t, 38.05, 38.45), size=44, role_size=30)


def s10_wrong(c, t):
    m = A("map")
    cam = drift_cam(CAM_HM2, t, 40.66, 0.01)
    m.draw(c, cam)
    place_pins(c, cam, t, ["midway", "oahu"])
    chip(c, "NẾU ĐOÁN NHẦM", W / 2, CHIP_Y, prog(t, 40.70, 41.05), size=44, bg="red", fg="white")
    ox, oy = mp(*PLACES["oahu"], cam)
    ax, ay = mp(203.5, 17.5, cam)  # nơi phục kích (giả định)
    pmv = prog(t, 42.3, 43.15, ease_in_out)
    for i, (dx, dy) in enumerate([(-40, 0), (40, 0), (0, 36)]):
        carrier_token(c, lerp(ox, ax, pmv) + dx, lerp(oy, ay, pmv) + dy, prog(t, 42.2 + i * 0.07, 42.5 + i * 0.07), s=0.8)
    pa = prog(t, 43.06, 43.35)
    if pa > 0:
        c.drawCircle(ax, ay + 12, 110, paint("navy", 200 * pa, stroke=4, PathEffect=skia.DashPathEffect.Make([16, 12], 0)))
        label_tag(c, "phục kích ở đây", ax - 120, ay + 160, pa, size=32, anchor="center")
    # máy bay Nhật đánh vào Midway
    mx, my = mp(*PLACES["midway"], cam)
    jx, jy = mp(171.5, 33.5, cam)
    carrier_token(c, jx + 40, jy, prog(t, 44.3, 44.6), color="red", s=0.8)
    pf = prog(t, 44.49, 45.26, lambda q: q)
    if pf > 0:
        for k, (ddx, ddy) in enumerate([(0, 0), (-34, 30), (30, 34)]):
            sx, sy, ex, ey = jx + ddx + 40, jy + ddy - 30, mx + ddx * 0.3, my + ddy * 0.3
            r = path_partial(c, [(sx, sy), (ex, ey)], pf, paint("red", 170, stroke=4, PathEffect=skia.DashPathEffect.Make([12, 10], 0)), curve=0.12)
            if r and pf < 1:
                plane_icon(c, r[0][0], r[0][1], math.degrees(math.atan2(r[1][1], r[1][0])), "red", 1.1)
        label_tag(c, "MÁY BAY NHẬT", jx - 20, jy - 90, prog(t, 44.55, 44.85), size=32, bg="red", fg="white")
    if t > 45.26:
        rings(c, mx, my, t, 45.26, 46.3, "red", max_r=260, period=0.3, width=6)
        label_tag(c, "đánh vào nơi khác", mx - 150, my + 200, prog(t, 45.5, 45.8), size=34, bg="red", fg="white")


def s11_check(c, t):
    draw_paper(c)
    pa = prog(t, 46.40, 46.75)
    p1 = 1 + 0.12 * math.sin(clamp((t - 49.61) / 0.35) * math.pi) if 49.61 < t < 49.96 else 1
    p2 = 1 + 0.12 * math.sin(clamp((t - 50.09) / 0.35) * math.pi) if 50.09 < t < 50.44 else 1
    with Xf(c, 300, 720, -3, back_out(pa) * p2 if pa < 1 else p2, clamp(pa * 2)):
        card(c, -170, -120, 340, 240, "yellow", r=8)
        text(c, "AF", 0, 50, "xbold", 140, "ink", align="center")
    with Xf(c, 790, 720, 2, back_out(pa) * p1 if pa < 1 else p1, clamp(pa * 2)):
        card(c, -230, -120, 460, 240, "white", r=8)
        text(c, "MIDWAY", 0, 30, "xbold", 84, "ink", align="center")
    text(c, "=", 545, 765, "xbold", 120, "ink", a=255 * pa, align="center")
    wob = math.sin(t * 9) * 8 if t > 50.4 else 0
    with Xf(c, 545, 560, wob, lerp(1, 1.3, prog(t, 50.42, 50.6)) if t < 50.9 else 1.3):
        text(c, "?", 0, 40, "xbold", 120, "red", a=255 * pa, align="center")
    # kính lúp kiểm tra
    pk = prog(t, 47.80, 48.25)
    if pk > 0:
        gx = lerp(1200, 600, pk) + math.sin(t * 3) * 16 * pk
        gy = lerp(1100, 880, pk)
        with Xf(c, gx, gy, -25):
            c.drawCircle(0, 0, 70, paint("white", 90))
            c.drawCircle(0, 0, 70, paint("ink", stroke=12))
            c.drawLine(0, 72, 0, 200, paint("ink", stroke=22))
        label_tag(c, "KIỂM TRA", 120, 1060, pk, size=40)


def s12_island(c, t):
    ph = A("atoll")
    z = lerp(1.75, 2.0, prog(t, 51.26, 53.56, lambda x: x))
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.43, 0.36, z)
    film(c, t)
    caption(c, "Ảnh: Midway, chụp 11/1941 (Hải quân Mỹ)", 1190)


def s13_distiller(c, t):
    draw_paper(c)
    note_label(c, "MINH HỌA", 830, 330, 1)
    label_tag(c, "MÁY CHƯNG CẤT NƯỚC NGỌT", W / 2, 420, prog(t, 53.6, 53.9), size=38, anchor="center")
    shake = 7 * math.sin(t * 70) * prog(t, 53.78, 53.9) * (1 - prog(t, 54.6, 54.8))
    cx, cy = 540 + shake, 790
    # khói
    for i in range(6):
        st = 54.0 + i * 0.12
        if t > st:
            age = t - st
            sp = paint("grey", 170 * clamp(1 - age / 1.2))
            sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 9 + age * 14))
            c.drawCircle(cx + 120 + math.sin(i * 2) * 30 + age * 40, cy - 260 - age * 160, 26 + age * 46, sp)
    with Xf(c, cx, cy, 0):
        shadow_begin(c, skia.Rect.MakeXYWH(-300, -400, 600, 800))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-140, -220, 280, 420), 40, 40), paint("#B9AE96"))
        c.drawRect(skia.Rect.MakeXYWH(-200, 150, 400, 60), paint("#8E846F"))
        c.drawRect(skia.Rect.MakeXYWH(140, -150, 120, 26), paint("#8E846F"))
        c.drawRect(skia.Rect.MakeXYWH(234, -150, 26, 170), paint("#8E846F"))
        c.restore()
        # ống thuỷ: mực nước hạ
        lvl = lerp(1.0, 0.12, prog(t, 54.1, 54.65))
        c.drawRect(skia.Rect.MakeXYWH(-40, -120, 80, 260), paint("white"))
        c.drawRect(skia.Rect.MakeXYWH(-40, -120 + 260 * (1 - lvl), 80, 260 * lvl), paint("#6E97A8"))
        c.drawRect(skia.Rect.MakeXYWH(-40, -120, 80, 260), paint("ink", stroke=4, cap=False))
        # đồng hồ: kim tụt
        c.drawCircle(0, -175, 52, paint("white"))
        c.drawCircle(0, -175, 52, paint("ink", stroke=5))
        ang = math.radians(lerp(-40, -150, prog(t, 54.0, 54.6)))
        c.drawLine(0, -175, 40 * math.cos(ang) * -1, -175 + 40 * math.sin(ang), paint("red", stroke=6))
        # giọt nước cuối cùng
        dp = prog(t, 54.2, 54.6, lambda q: q)
        if 0 < dp < 1:
            c.drawCircle(247, 30 + dp * 120, 9, paint("#6E97A8"))
    stamp(c, "HỎNG", 560, 820, prog(t, 54.60, 54.82), size=110, rot=-10)


def legend(c, t, active):
    items = [("1", "CÁP NGẦM", "lệnh mật", "navy"), ("2", "VÔ TUYẾN", "lời thường", "red")]
    for i, (n, a, b, colr) in enumerate(items):
        p = prog(t, 55.90 + i * 0.15, 56.3 + i * 0.15)
        if p <= 0:
            continue
        y = 930 + i * 130
        on = active == i
        with Xf(c, 90 + (1 - ease_out(p)) * -80, y, 0, 1, clamp(p * 2) * (1 if on or active is None else 0.55)):
            card(c, 0, 0, 900, 105, "white", r=6)
            c.drawCircle(56, 52, 32, paint(colr))
            text(c, n, 56, 66, "xbold", 38, "white", align="center")
            w = text(c, a, 110, 68, "xbold", 42, "ink")
            text(c, "· " + b, 130 + w, 68, "semi", 36, "grey")


def s13_cable(c, t):
    m = A("map")
    cam = drift_cam(cam_lerp(CAM_HM, CAM_JP, prog(t, 61.3, 62.3, ease_in_out)), t, 55.28, 0.006)
    m.draw(c, cam)
    pts = [mp(lon, lat, cam) for lon, lat in CHAIN]
    pc = prog(t, 58.10, 59.20, lambda q: q)
    if pc > 0:
        r = path_partial(c, pts, pc, paint("navy", stroke=7))
        if t < 59.6:
            pos = r[0]
            label_tag(c, "LỆNH MẬT", pos[0], pos[1] - 52, prog(t, 57.04, 57.3), size=30, anchor="center", bg="navy", fg="white")
    elif t > 57.04:
        x, y = pts[0]
        label_tag(c, "LỆNH MẬT", x, y - 52, prog(t, 57.04, 57.3), size=30, anchor="center", bg="navy", fg="white")
    place_pins(c, cam, t, ["midway", "oahu"] + (["tokyo"] if t > 61.8 else []), {"tokyo": 61.9})
    mx, my = mp(*PLACES["midway"], cam)
    if 59.8 < t < 61.4:
        label_tag(c, "lính đảo nhận lệnh", mx + 20, my + 70, prog(t, 59.81, 60.1) * (1 - prog(t, 61.1, 61.35)), size=32, bg="navy", fg="white")
    # vô tuyến
    rings(c, mx, my, t, 63.13, 66.9, "red", max_r=800, period=0.45, width=5)
    pb = prog(t, 61.71, 62.05) * (1 - prog(t, 66.8, 67.2))
    if pb > 0:
        with Xf(c, W - 600, my - 300, -1.5, max(0.01, back_out(clamp(pb))), clamp(pb * 3)):
            card(c, 0, 0, 560, 150, "white", r=4)
            text(c, "MÁY CHƯNG CẤT HỎNG", 28, 62, "mono", 36)
            text(c, "THIẾU NƯỚC", 28, 118, "mono", 36)
        label_tag(c, "KHÔNG MÃ HOÁ", W - 40, my - 330, prog(t, 64.09, 64.4) * (1 - prog(t, 66.8, 67.2)), size=30, bg="red", fg="white")
    tx, ty = mp(*PLACES["tokyo"], cam)
    pj = prog(t, 65.30, 65.6)
    pulse = 1 + 0.2 * math.sin(clamp((t - 65.67) / 0.35) * math.pi) if t > 65.67 else 1
    antenna_icon(c, tx + 40, ty - 70, pj, "red", s=1.2 * pulse)
    label_tag(c, "AI BẮT ĐÚNG SÓNG", tx - 60, ty + 70, pj, size=30, bg="red", fg="white")
    legend(c, t, None if t < 57.0 else (0 if t < 61.4 else 1))


def s15_listen(c, t):
    draw_paper(c)
    # sóng điện Nhật đến từ mép trái
    for k in range(8):
        st = 67.75 + k * 0.32
        if t > st:
            age = t - st
            r = 200 + age * 420
            c.drawCircle(-260, 760, r, paint("red", 190 * clamp(1 - age / 2.0), stroke=6))
    A("rochefort").framed(c, 610, 740, 600, rot=lerp(4, 2, prog(t, 67.6, 67.95)), scale=lerp(0.94, 1, prog(t, 67.6, 67.95)) + 0.01 * max(0, t - 67.95))
    label_tag(c, "NHÓM ROCHEFORT", 70, 1080, prog(t, 67.65, 67.95), size=38)
    label_tag(c, "nghe điện hải quân Nhật", 70, 1160, prog(t, 68.33, 68.6), size=34, bg="red", fg="white")


def melb_doc(c, t, x, y, scale, alpha, show_midway):
    """Bản dịch điện Nhật do trạm Melbourne đưa ra (DIỄN Ý). Toạ độ trên trái."""
    w, h = 920, 560
    with Xf(c, x, y, 0.8, scale, alpha):
        card(c, 0, 0, w, h, "white", r=4)
        text(c, "BẢN DỊCH ĐIỆN NHẬT · 22/5/1942", 36, 58, "mono", 30, "grey")
        note_label(c, "DIỄN Ý", w - 150, 26, 1)
        c.drawLine(36, 86, w - 36, 86, paint("grey", 120, stroke=2))
        text(c, typed("PHÍA NHẬT BÁO:", prog(t, 76.1, 76.9, lambda q: q)), 36, 160, "mono", 40, "grey")
        fm = font("mono", 46)
        l1 = "ĐƠN VỊ KHÔNG QUÂN Ở AF"
        pre = fm.measureText(nfc("ĐƠN VỊ KHÔNG QUÂN Ở "))
        highlight(c, 36 + pre, 196, fm.measureText("AF"), 58, prog(t, 78.0, 78.25))
        text(c, typed(l1, prog(t, 77.2, 78.1, lambda q: q)), 36, 240, "mono", 46)
        text(c, typed("XIN TIẾP TẾ NƯỚC.", prog(t, 78.56, 79.3, lambda q: q)), 36, 310, "mono", 46)
        text(c, typed("NƯỚC CÒN LẠI", prog(t, 81.82, 82.4, lambda q: q)), 36, 400, "mono", 46)
        l4 = "CHỈ ĐỦ CHO HAI TUẦN."
        pre4 = fm.measureText(nfc("CHỈ ĐỦ CHO "))
        highlight(c, 36 + pre4, 426, fm.measureText(nfc("HAI TUẦN")), 58, prog(t, 83.0, 83.3))
        w4 = text(c, typed(l4, prog(t, 82.4, 83.25, lambda q: q)), 36, 470, "mono", 46)
        for (a_, b_, yy, ww) in [(77.2, 78.1, 240, None), (78.56, 79.3, 310, None), (81.82, 82.4, 400, None), (82.4, 83.25, 470, w4)]:
            pp = prog(t, a_, b_, lambda q: q)
            if 0 < pp < 1:
                txt = {240: "ĐƠN VỊ KHÔNG QUÂN Ở AF", 310: "XIN TIẾP TẾ NƯỚC.", 400: "NƯỚC CÒN LẠI", 470: l4}[yy]
                cursor(c, 36 + fm.measureText(typed(txt, pp)), yy, t, 46)


def s16_melbourne(c, t):
    m = A("map")
    cam = cam_lerp(CAM_PAC, (162.0, -4.0, 10.5), prog(t, 69.86, 73.1, lambda q: q))
    m.draw(c, cam)
    place_pins(c, cam, t, ["midway", "tokyo", "melbourne"], {"midway": 69.8, "tokyo": 69.8, "melbourne": 72.40})
    chip(c, "22 THÁNG 5 · 1942", W / 2, CHIP_Y, prog(t, 69.90, 70.25))
    lx, ly = mp(*PLACES["melbourne"], cam)
    label_tag(c, "trạm tình báo hải quân Mỹ", lx + 26, ly + 52, prog(t, 71.42, 71.75), size=30, bg="navy", fg="white")
    # bản dịch bay ra từ Melbourne rồi lớn dần
    pf = prog(t, 73.13, 73.8, ease_in_out)
    dim = prog(t, 73.4, 73.9)
    if dim > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("paper", 200 * dim))
    if pf > 0:
        melb_doc(c, t, lerp(lx, 80, pf), lerp(ly, 330, pf), lerp(0.08, 1.0, pf), clamp(pf * 3), False)
    if t >= 79.6:
        pm = prog(t, 79.75, 80.2)
        msg_card(c, 90 + (1 - ease_out(pm)) * 600, 920, t, 0, 0, 0, None, scale=1.0, alpha=pm, done=True)
        # nối hai chữ HAI TUẦN
        pl = prog(t, 83.05, 83.35)
        if pl > 0:
            c.drawLine(590, 830, 560, 1100, paint("yellow", 255, stroke=10))
            c.drawLine(590, 830, 560, 1100, paint("ink", 255, stroke=3))


def s19_af(c, t):
    ph = A("atoll")
    ph.blur_bg(c)
    ph.framed(c, W / 2, 720, 880, rot=lerp(2.5, 1.0, prog(t, 83.59, 83.95)), scale=lerp(0.95, 1, prog(t, 83.59, 83.95)) + 0.008 * max(0, t - 83.95))
    label_tag(c, "MIDWAY", 170, 300, prog(t, 84.20, 84.5), size=44)
    pa = prog(t, 87.32, 87.55, back_out)
    burst(c, 470, 820, t, 87.34, "yellow", r0=150, r1=320)
    if t > 87.32:
        with Xf(c, 470, 820, -6, lerp(1.8, 1.0, clamp(pa))):
            chip(c, "AF", 0, 0, 1.0, size=130)


def s20_attack(c, t):
    if t < 90.43:
        ph = A("hiryu")
        z = lerp(1.0, 1.08, prog(t, 87.97, 90.43, lambda q: q))
        ph.cover(c, skia.Rect.MakeWH(W, H), 0.42, 0.42, z)
        film(c, t)
        chip(c, "4 THÁNG 6 · 1942", W / 2, CHIP_Y, prog(t, 88.0, 88.35))
        label_tag(c, "TÀU SÂN BAY NHẬT", 60, 1100, prog(t, 89.55, 89.85), size=40, bg="red", fg="white")
        caption(c, "Ảnh: tàu Hiryu, chụp từ máy bay Mỹ, 4/6/1942", 1190)
    else:
        ph = A("burning")
        z = lerp(1.16, 1.06, prog(t, 90.43, 91.4))
        dx, dy = shake(t, 90.43, 0.4, 18)
        c.save()
        c.translate(dx, dy)
        ph.cover(c, skia.Rect.MakeXYWH(-30, -30, W + 60, H + 60), 0.47, 0.42, z)
        c.restore()
        film(c, t)
        if t < 90.53:
            c.drawRect(skia.Rect.MakeWH(W, H), paint("white", 150 * (1 - (t - 90.43) / 0.1)))
        chip(c, "4 THÁNG 6 · 1942", W / 2, CHIP_Y, 1)
        label_tag(c, "MIDWAY BỊ ĐÁNH", 60, 1100, prog(t, 90.55, 90.85), size=40)
        caption(c, "Ảnh: kho dầu cháy trên Midway, 4/6/1942", 1190)


STRIPS = [  # ảnh, crop (x0,y0,x1,y1), tâm y, nhãn
    ("enterprise", (0.0, 0.30, 1.0, 0.66), 340, "USS ENTERPRISE"),
    ("hornet", (0.05, 0.30, 1.0, 0.60), 620, "USS HORNET"),
    ("yorktown", (0.30, 0.50, 0.98, 0.86), 1030, "USS YORKTOWN"),
]


def s21_carriers(c, t):
    draw_paper(c)
    for i, (key, crop, y, lab) in enumerate(STRIPS):
        p = prog(t, 91.79 + i * 0.19, 92.2 + i * 0.19)
        if p <= 0:
            continue
        side = -1 if i % 2 == 0 else 1
        x = W / 2 + side * (1 - ease_out(p)) * 700
        drift = (t - 92) * 6 * side
        h = A(key).framed(c, x + drift, y, 960, rot=side * lerp(4, 1.2, ease_out(p)), crop=crop)
        label_tag(c, lab, x - 450 + drift, y + h / 2 - 24, prog(t, 92.0 + i * 0.19, 92.3 + i * 0.19), size=32, bg="navy", fg="white")


def s22_days(c, t):
    ph = A("burning")
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.5, 0.40, 1.0 + 0.012 * (t - 94.95))
    film(c, t, 0.7)
    c.drawRect(skia.Rect.MakeWH(W, H), paint("ink", 160))
    days = list(range(20, 32)) + [1, 2, 3, 4]
    bw, gap = 104, 12
    x0 = (W - (8 * bw + 7 * gap)) / 2
    pin_ = prog(t, 94.95, 95.3)
    for k, d in enumerate(days):
        r, ccol = divmod(k, 8)
        x = x0 + ccol * (bw + gap)
        y = 520 + r * (bw + 70)
        pk = prog(t, 94.95 + k * 0.02, 95.3 + k * 0.02)
        if pk <= 0:
            continue
        fill = "white"
        if k == 0 and t > 95.64:
            fill = "yellow"
        elif k == 15 and t > 96.75:
            fill = "red"
        elif 0 < k < 15 and t > 95.9 + (k - 1) * 0.055:
            fill = "#D8CDB4"
        with Xf(c, x + bw / 2, y + bw / 2, 0, max(0.01, back_out(pk)), clamp(pk * 3)):
            card(c, -bw / 2, -bw / 2, bw, bw, fill, r=6)
            text(c, str(d), 0, 18, "xbold", 50, "white" if fill == "red" else "ink", align="center")
            text(c, "/5" if k < 12 else "/6", 0, 44, "semi", 26, "white" if fill == "red" else "grey", align="center")
    label_tag(c, "20/5: phát tin xin nước", x0, 450, prog(t, 95.64, 95.95), size=32, bg="yellow")
    label_tag(c, "4/6: máy bay Nhật tới", x0 + 8 * bw + 7 * gap, 520 + 2 * (bw + 70) - 10, prog(t, 96.75, 97.05), size=32, anchor="right", bg="red", fg="white")
    if t > 98.0:
        dx, dy = shake(t, 98.25, 0.3, 8)
        with Xf(c, W / 2 + dx, 1010 + dy, -3, lerp(1.7, 1.0, prog(t, 98.0, 98.3, back_out))):
            chip(c, "MỚI 15 NGÀY", 0, 0, 1, size=84)


TIMELINE = [
    (0.00, 2.65, s01_atoll),
    (2.65, 12.45, s02_map_msg),
    (12.45, 18.28, None),  # s04 (đặt dưới để tham chiếu Photo)
    (18.28, 29.96, s05_decrypt),
    (29.96, 34.69, s07_map_af),
    (34.69, 37.69, s08_pearl),
    (37.69, 40.66, s09_nimitz),
    (40.66, 46.36, s10_wrong),
    (46.36, 51.26, s11_check),
    (51.26, 53.56, s12_island),
    (53.56, 55.28, s13_distiller),
    (55.28, 67.60, s13_cable),
    (67.60, 69.86, s15_listen),
    (69.86, 83.59, s16_melbourne),
    (83.59, 87.97, s19_af),
    (87.97, 91.37, s20_attack),
    (91.37, 94.95, s21_carriers),
    (94.95, 99.90, s22_days),
]


def s04_rochefort(c, t):
    draw_paper(c)
    pe = prog(t, 12.45, 12.85)
    A("rochefort").framed(c, W / 2, 760, 760, rot=lerp(-6, -2, pe), scale=lerp(0.93, 1, pe) + 0.005 * max(0, t - 12.85))
    chip(c, "TRÂN CHÂU CẢNG", W / 2, CHIP_Y, prog(t, 12.95, 13.3))
    name_tag(c, 60, 1030, "Joseph Rochefort", "Sĩ quan hải quân · trưởng nhóm giải mã", prog(t, 15.40, 15.8), size=46, role_size=30)


TIMELINE[2] = (12.45, 18.28, s04_rochefort)


# kiểu chuyển cảnh tại mốc vào của cảnh (không có = cắt thẳng, giữ cho các cú nhấn)
TRANS = {2.65: "shrink", 12.45: "push", 18.28: "push", 29.96: "push", 34.69: "fade", 37.69: "pushup",
         40.66: "fade", 46.36: "push", 51.26: "fade", 53.56: "push", 55.28: "fade", 67.60: "push",
         69.86: "fade", 83.59: "push", 91.37: "push", 94.95: "fade"}
WIN = {"shrink": (0.12, 0.45), "push": (0.16, 0.26), "pushup": (0.16, 0.26), "fade": (0.2, 0.2)}
_surfs = []




def _render(fn, t, k):
    s = _surfs[k]
    cc = s.getCanvas()
    cc.clear(skia.ColorBLACK)
    fn(cc, t)
    return s.makeImageSnapshot()


def _edge_shadow(c, x, vertical=False):
    if vertical:
        sh = skia.GradientShader.MakeLinear([skia.Point(0, x - 60), skia.Point(0, x)], [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(110, 10, 8, 5)])
        c.drawRect(skia.Rect.MakeXYWH(0, x - 60, W, 60), skia.Paint(Shader=sh))
    else:
        sh = skia.GradientShader.MakeLinear([skia.Point(x - 60, 0), skia.Point(x, 0)], [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(110, 10, 8, 5)])
        c.drawRect(skia.Rect.MakeXYWH(x - 60, 0, 60, H), skia.Paint(Shader=sh))


SHAKES = [(9.42, 7), (29.27, 13), (36.95, 7), (54.66, 13), (87.38, 13)]


def draw_frame(c, t):
    for t0, amp in SHAKES:
        dx, dy = shake(t, t0, 0.32, amp)
        if dx or dy:
            c.translate(W / 2 + dx, H / 2 + dy)
            c.scale(1.03, 1.03)
            c.translate(-W / 2, -H / 2)
            break
    while len(_surfs) < 2:
        _surfs.append(skia.Surface(W, H))
    for i, (a, b, fn) in enumerate(TIMELINE):
        kind = TRANS.get(a)
        if kind and i > 0:
            pre, post = WIN[kind]
            if a - pre <= t < a + post:
                p = ease_in_out((t - (a - pre)) / (pre + post))
                old = _render(TIMELINE[i - 1][2], t, 0)
                new = _render(fn, t, 1)
                if kind == "fade":
                    c.drawImage(old, 0, 0)
                    pp = skia.Paint()
                    pp.setAlphaf(p)
                    c.drawImage(new, 0, 0, SAMP, pp)
                elif kind == "push":
                    c.drawImage(old, -0.3 * W * p, 0)
                    c.drawRect(skia.Rect.MakeWH(W, H), paint("ink", 90 * p))
                    x = W * (1 - p)
                    _edge_shadow(c, x)
                    c.drawImage(new, x, 0)
                elif kind == "pushup":
                    c.drawImage(old, 0, -0.3 * H * p)
                    c.drawRect(skia.Rect.MakeWH(W, H), paint("ink", 90 * p))
                    y = H * (1 - p)
                    _edge_shadow(c, y, vertical=True)
                    c.drawImage(new, 0, y)
                elif kind == "shrink":
                    # ảnh đảo thu nhỏ đúng vào chấm Midway trên bản đồ
                    c.drawImage(new, 0, 0)
                    cam = drift_cam(CAM_HM, t, 2.65, 0.007)
                    tx, ty = mp(*PLACES["midway"], cam)
                    sc = math.exp(lerp(0, math.log(0.035), p))
                    cx, cy = lerp(W / 2, tx, p), lerp(H / 2, ty, p)
                    with Xf(c, cx, cy, lerp(0, -4, p), sc, clamp((1 - p) * 4)):
                        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-W / 2, -H / 2, W, H), 40 * p / max(sc, 0.05) * 0.02 + 1, 40)
                        card(c, -W / 2 - 24, -H / 2 - 24, W + 48, H + 48, "white", r=6)
                        c.save()
                        c.clipRRect(rr, True)
                        c.drawImage(old, -W / 2, -H / 2)
                        c.restore()
                return
    for a, b, fn in TIMELINE:
        if a <= t < b:
            fn(c, t)
            break
