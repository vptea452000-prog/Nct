"""Bảng dựng tập Petrov (phong cách Midway v2). Mốc giây theo MP3, xem build/words.json (ước lượng).
Quy tắc ảnh: chỉ dùng ảnh đã xác minh (xem BAN_GIAO.md); không dùng ảnh Alamy có dấu nước hoặc ảnh phim dựng lại."""
import math
import skia
from lib import *  # noqa

PH = ROOT / "assets/photos"
CHIP_Y = 250
_assets = {}


def A(key):
    if key not in _assets:
        _assets[key] = Photo(PH / f"{key}.jpg")
    return _assets[key]


def caption(c, s, y=1225, size=27, x=60):
    text(c, s, x, y, "semi", size, "white", a=235, stroke=3, stroke_color="ink")


def caption_dark(c, s, y, size=27, x=60):
    text(c, s, x, y, "semi", size, "grey")


def pop_in(t, t0, d=0.3):
    return prog(t, t0, t0 + d)


DARK = "#10161C"
GREEN = "#7CE38B"
RED = "#E5483A"


def night(c):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(DARK))


def crt(c, x, y, w, h):
    """Màn hình máy tính kiểu thập niên 1980."""
    c.drawRoundRect(skia.Rect.MakeXYWH(x - 24, y - 24, w + 48, h + 48), 28, 28, paint("#2C3138"))
    c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 22, 22, paint("#081210"))
    for k in range(int(h / 6)):
        c.drawLine(x + 10, y + k * 6, x + w - 10, y + k * 6, paint("#000000", 40, stroke=2, cap=False))


def glow_text(c, s, x, y, size, color, a=255, align="center", name="mono"):
    for r, al in ((10, 50), (5, 90)):
        p = paint(color, a * al / 255)
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r))
        f = font(name, size)
        s2 = nfc(s)
        w = f.measureText(s2)
        xx = x - w / 2 if align == "center" else x
        c.drawString(s2, xx, y, f, p)
    text(c, s, x, y, name, size, color, a=a, align=align)


def ring_box(c, x, y, w, h, p, color="yellow", stroke=6):
    if p <= 0:
        return
    pth = skia.Path(); pth.addRect(skia.Rect.MakeXYWH(x, y, w, h))
    pm = skia.PathMeasure(pth, False); d = skia.Path(); pm.getSegment(0, pm.getLength() * clamp(p), d, True)
    c.drawPath(d, paint(color, stroke=stroke, cap=False))


def missile_icon(c, x, y, ang=0, s=1.0, color=RED, a=255):
    with Xf(c, x, y, ang, s):
        p = skia.Path()
        p.moveTo(0, -40); p.lineTo(9, -22); p.lineTo(9, 26); p.lineTo(18, 40); p.lineTo(-18, 40); p.lineTo(-9, 26); p.lineTo(-9, -22); p.close()
        c.drawPath(p, paint(color, a))


def phone(c, x, y, s=1.0, a=1.0, lift=0.0):
    """Điện thoại bàn quay số kiểu Liên Xô."""
    with Xf(c, x, y, 0, s, a):
        base = skia.Path(); base.moveTo(-190, 150); base.lineTo(-140, -60); base.lineTo(140, -60); base.lineTo(190, 150); base.close()
        shadow_begin(c, skia.Rect.MakeXYWH(-260, -300, 520, 520))
        c.drawPath(base, paint("#B7372E"))
        c.restore()
        c.drawCircle(0, 50, 80, paint("#E9E2CF"))
        for k in range(10):
            ang = math.radians(-60 + k * 28)
            c.drawCircle(56 * math.cos(ang), 50 + 56 * math.sin(ang), 13, paint("#2C3138"))
        c.drawCircle(0, 50, 24, paint("#B7372E"))
        with Xf(c, 0, -110 - 80 * lift, -10 * lift):
            hs = skia.Path(); hs.moveTo(-210, 20); hs.cubicTo(-160, -60, 160, -60, 210, 20)
            c.drawPath(hs, paint("#8E2A23", stroke=46))
            for side in (-1, 1):
                c.drawRoundRect(skia.Rect.MakeXYWH(side * 200 - 45, 0, 90, 60), 26, 26, paint("#8E2A23"))


def satellite_icon(c, x, y, s=1.0, a=255):
    with Xf(c, x, y, 0, s, a / 255):
        c.drawRect(skia.Rect.MakeXYWH(-24, -30, 48, 60), paint("#C9C3B4"))
        for side in (-1, 1):
            c.drawRect(skia.Rect.MakeXYWH(side * 34 - (60 if side < 0 else 0), -16, 60, 32), paint("#3E5A8A"))
            c.drawLine(side * 24, 0, side * 34, 0, paint("#C9C3B4", stroke=5))
        c.drawCircle(0, 40, 14, paint("#8E959B"))


# ------------------------------------------------------------------ CẢNH
def s01_night(c, t):
    if t < 4.15:
        night(c)
        chip(c, "26 THÁNG 9 · 1983", W / 2, CHIP_Y, pop_in(t, 0.6))
        crt(c, 160, 460, 760, 560)
        glow_text(c, "00:15", 540, 640, 120, GREEN, a=255 * pop_in(t, 0.9))
        glow_text(c, typed("HỆ THỐNG CẢNH BÁO SỚM", prog(t, 2.5, 3.6, lambda q: q)), 540, 800, 40, GREEN)
        note_label(c, "MINH HỌA", 760, 1060, 1)
        label_tag(c, "hơn nửa đêm · giờ Moskva", W / 2, 1150, pop_in(t, 1.2), size=32, anchor="center")
        return
    ph = A("minuteman_launch")
    z = lerp(1.0, 1.08, prog(t, 4.15, 5.6, lambda q: q))
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.5, 0.45, z)
    label_tag(c, "\"MỸ PHÓNG TÊN LỬA\"", W / 2, 420, pop_in(t, 4.2), size=44, anchor="center", bg="red", fg="white")
    caption(c, "Ảnh minh họa: tên lửa Minuteman III của Mỹ (một lần phóng thử)", 1190)


def s02_decide(c, t):
    night(c)
    phone(c, 540, 660, 1.0, pop_in(t, 5.6))
    label_tag(c, "báo lên cấp trên?", W / 2, 920, pop_in(t, 7.3), size=42, anchor="center", bg="yellow")
    ph = pop_in(t, 8.6)
    if ph > 0:
        label_tag(c, "CÓ", 360, 1040, ph, size=44, anchor="center", bg="red", fg="white")
        label_tag(c, "KHÔNG", 720, 1040, ph, size=44, anchor="center", bg="white")


def s03_petrov(c, t):
    draw_paper(c)
    pe = pop_in(t, 9.92, 0.35)
    A("petrov_late").framed(c, W / 2, 640, 600, rot=lerp(-4, -2, pe), scale=lerp(0.94, 1, pe) + 0.005 * max(0, t - 10.3))
    name_tag(c, 60, 1010, "Trung tá Stanislav Petrov", "44 tuổi năm 1983 · kỹ sư quân đội", pop_in(t, 10.8, 0.4), size=44, role_size=30)
    caption_dark(c, "Ảnh: Petrov những năm cuối đời (Wikimedia Commons)", 1205)


def s04_bunker(c, t):
    if t < 16.5:
        ph = A("serpukhov15_sat")
        ph.blur_bg(c, 120)
        pe = pop_in(t, 14.0, 0.35)
        ph.framed(c, W / 2, 640, 1000, rot=lerp(-2, -1, pe), scale=lerp(0.95, 1, pe) + 0.006 * max(0, t - 14.3))
        label_tag(c, "SERPUKHOV-15", W / 2, 360, pop_in(t, 14.3), size=44, anchor="center", bg="yellow")
        label_tag(c, "boong-ke bí mật · phía nam Moskva", W / 2, 960, pop_in(t, 15.0), size=32, anchor="center")
        caption(c, "Ảnh vệ tinh khu Serpukhov-15 (55,068°B · 37,041°Đ), chụp sau này", 1060)
        return
    ph = A("molniya_orbit")
    night(c)
    pe = pop_in(t, 16.5, 0.35)
    w = 1020
    h = ph.framed(c, W / 2, 640, w, scale=lerp(0.95, 1, pe), alpha=pe)
    x0, y0 = W / 2 - w / 2, 640 - h / 2
    for k, (u, v, t0) in enumerate([(0.22, 0.05, 18.4), (0.73, 0.05, 18.7)]):
        sx, sy = x0 + u * w, y0 - 110 + 20 * math.sin(t * 1.5 + k)
        satellite_icon(c, sx, sy, 1.0, 255 * pop_in(t, t0))
    usx, usy = x0 + 0.20 * w, y0 + 0.33 * h
    if t > 20.7:
        rings(c, usx, usy, t, 20.7, 22.5, GREEN, max_r=160, period=0.35, width=4)
        label_tag(c, "căn cứ tên lửa Mỹ", usx, usy + 120, pop_in(t, 20.8), size=30, anchor="center", bg="yellow")
    label_tag(c, "vệ tinh cảnh báo sớm", W / 2, 300, pop_in(t, 18.4), size=36, anchor="center")
    caption(c, "Sơ đồ quỹ đạo kiểu Molniya, loại quỹ đạo vệ tinh Oko dùng", 1080)


def s05_role(c, t):
    draw_paper(c)
    for k, (lab, t0, ok) in enumerate([("BẤM NÚT ĐÁNH TRẢ", 22.6, False), ("BÁO LÊN TRÊN", 24.7, True)]):
        p = pop_in(t, t0, 0.35)
        if p <= 0:
            continue
        y = 520 + k * 400
        with Xf(c, 540, y, 0, max(0.01, back_out(p)), clamp(p * 3)):
            card(c, -380, -120, 760, 240, "white", r=10)
            c.drawCircle(-260, 0, 70, paint(RED if not ok else "navy"))
            text(c, lab, 60, 18, "xbold", 46, "ink", align="center")
        if not ok and t > 23.6:
            stamp(c, "KHÔNG PHẢI", 720, y + 150, prog(t, 23.6, 23.8), size=50, rot=-8)
        if ok and t > 25.6:
            stamp(c, "NHIỆM VỤ", 720, y + 150, prog(t, 25.6, 25.8), size=50, color="navy", rot=-8)


def s06_kal(c, t):
    ph = A("kal007_map")
    ph.blur_bg(c, 120)
    pe = pop_in(t, 26.9, 0.35)
    ph.framed(c, W / 2, 660, 960, rot=lerp(-2, -1, pe), scale=lerp(0.95, 1, pe) + 0.005 * max(0, t - 27.3))
    label_tag(c, "căng thẳng Mỹ – Liên Xô", W / 2, 300, pop_in(t, 27.2), size=36, anchor="center", bg="red", fg="white")
    chip(c, "1 THÁNG 9 · 1983", W / 2, 400, pop_in(t, 29.1), size=38)
    label_tag(c, "chuyến bay KAL 007 bị bắn rơi", W / 2, 1110, pop_in(t, 30.4), size=32, anchor="center", bg="yellow")
    caption(c, "Bản đồ đường bay KAL 007 (Wikimedia Commons)", 1180)


def s07_alarm(c, t):
    flash = (int((t - 32.6) * 3) % 2 == 0) if t > 32.6 else False
    night(c)
    if flash:
        c.drawRect(skia.Rect.MakeWH(W, H), paint(RED, 70))
    crt(c, 140, 380, 800, 640)
    if t > 33.75:
        glow_text(c, "СТАРТ", 540, 560, 130, RED, a=255 if flash or t > 35.2 else 160)
        text(c, "= \"PHÓNG\"", 540, 630, "bold", 34, "white", a=200, align="center")
    n = 0
    if t > 35.2:
        n = 1
    for k in range(4):
        if t > 36.5 + k * 0.22:
            n = 2 + k
    for k in range(n):
        missile_icon(c, 290 + k * 125, 780, 0, 0.9)
    if n:
        glow_text(c, f"TÊN LỬA: {n}", 540, 900, 50, GREEN)
    if t > 38.75:
        glow_text(c, "ĐỘ TIN CẬY: CAO NHẤT", 540, 975, 42, RED)
    note_label(c, "DIỄN Ý", 770, 1050, 1)
    label_tag(c, "còi báo động", W / 2, 300, pop_in(t, 32.7), size=36, anchor="center", bg="red", fg="white")


def s08_reason(c, t):
    draw_paper(c)
    if t < 46.3:
        label_tag(c, "Petrov không tin", W / 2, 330, pop_in(t, 40.65), size=40, anchor="center", bg="yellow")
        pl = pop_in(t, 42.2, 0.6)
        if pl > 0:
            text(c, "đánh thật", 290, 470, "bold", 34, "grey", align="center")
            for k in range(int(36 * pl)):
                r, cc = divmod(k, 6)
                missile_icon(c, 140 + cc * 60, 560 + r * 90, 0, 0.55, "#9A9284")
        pf = pop_in(t, 44.6, 0.4)
        if pf > 0:
            text(c, "báo động", 790, 470, "bold", 34, "grey", align="center")
            for k in range(5):
                missile_icon(c, 690 + (k % 3) * 100, 600 + (k // 3) * 120, 0, 0.8, RED, 255 * pf)
            label_tag(c, "chỉ 5 quả?", 790, 900, pf, size=40, anchor="center", bg="red", fg="white")
        return
    if t < 50.84:
        ph = A("pechora_radar")
        ph.blur_bg(c, 120)
        pe = pop_in(t, 46.3, 0.35)
        ph.framed(c, W / 2, 640, 1000, rot=lerp(-2, -1, pe), scale=lerp(0.95, 1, pe) + 0.006 * max(0, t - 46.6))
        label_tag(c, "radar mặt đất", W / 2, 330, pop_in(t, 46.4), size=40, anchor="center", bg="yellow")
        label_tag(c, "chỉ thấy tên lửa khi đã bay gần", W / 2, 990, pop_in(t, 47.8), size=32, anchor="center")
        label_tag(c, "lúc đó: chưa thấy gì", W / 2, 1070, pop_in(t, 49.4), size=32, anchor="center", bg="red", fg="white")
        caption(c, "Ảnh: radar Daryal của Liên Xô ở Pechora, chụp sau này", 1160)
        return
    night(c)
    crt(c, 140, 420, 800, 520)
    glow_text(c, typed("LỖI HỆ THỐNG", prog(t, 51.5, 52.5, lambda q: q)), 540, 700, 80, GREEN)
    label_tag(c, "Petrov báo lên trên", W / 2, 330, pop_in(t, 50.9), size=36, anchor="center", bg="yellow")
    note_label(c, "MINH HỌA", 770, 980, 1)


def s09_wait(c, t):
    night(c)
    p = prog(t, 53.2, 59.4, lambda q: q)
    mins = int(23 * p)
    cx, cy = 540, 680
    c.drawCircle(cx, cy, 260, paint("#2C3138"))
    c.drawCircle(cx, cy, 260, paint("white", 200, stroke=8))
    arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(cx - 230, cy - 230, 460, 460), -90, 360 * 23 / 60 * p)
    c.drawPath(arc, paint("yellow", stroke=26, cap=False))
    glow_text(c, f"{mins}", cx, cy + 40, 150, "#F4C430", name="xbold")
    text(c, "phút", cx, cy + 110, "bold", 40, "white", a=200, align="center")
    label_tag(c, "Rồi ông chờ", W / 2, 330, pop_in(t, 53.05), size=40, anchor="center")
    label_tag(c, "nếu sai: tên lửa tới trong vài phút", W / 2, 1040, pop_in(t, 55.1) * (1 - prog(t, 57.0, 57.2)), size=32, anchor="center", bg="red", fg="white")
    label_tag(c, "không có gì xảy ra", W / 2, 1040, pop_in(t, 58.4), size=36, anchor="center", bg="yellow")
    stamp(c, "ÔNG ĐÃ ĐÚNG", 540, 1150, prog(t, 59.8, 60.0), size=60, color="navy", rot=-6)


def s10_cause(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#0E1A2B"))
    # Trái Đất (mép dưới), mây cao, Mặt Trời, vệ tinh
    c.drawCircle(540, 2050, 1200, paint("#2F5D8A"))
    c.drawCircle(540, 2050, 1200, paint("#8FB6D9", 120, stroke=10))
    for k in range(5):
        x = 260 + k * 150
        cl = paint("white", 230)
        cl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
        c.drawOval(skia.Rect.MakeXYWH(x - 90, 880 + (k % 2) * 16, 180, 60), cl)
    sun = pop_in(t, 63.0, 0.4)
    sp = paint("#FFD764", 255 * sun)
    sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    c.drawCircle(130, 360, 70, sp)
    pr = prog(t, 63.6, 64.6, ease_in_out)
    if pr > 0:
        path_partial(c, [(170, 400), (560, 880)], pr, paint("#FFD764", 220, stroke=8))
    pb = prog(t, 64.7, 65.5, ease_in_out)
    if pb > 0:
        path_partial(c, [(560, 880), (820, 420)], pb, paint("#FFD764", 220, stroke=8))
        fl = paint("white", 255 * clamp(pb * 2))
        fl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
        c.drawCircle(560, 880, 40, fl)
    satellite_icon(c, 840, 390, 1.3)
    label_tag(c, "ánh nắng phản chiếu trên mây cao", W / 2, 1060, pop_in(t, 63.4), size=32, anchor="center", bg="yellow")
    pm = pop_in(t, 65.6)
    if pm > 0:
        label_tag(c, "= \"lửa phụt từ tên lửa\"", 820, 280, pm, size=32, anchor="center", bg="red", fg="white")
    label_tag(c, "nguyên nhân", W / 2, 1140, pop_in(t, 61.9), size=30, anchor="center")
    note_label(c, "MINH HỌA", 60, 1180, 1)


def s11_aftermath(c, t):
    draw_paper(c)
    if t < 73.9:
        label_tag(c, "không được khen thưởng", W / 2, 330, pop_in(t, 67.5), size=36, anchor="center")
        p = pop_in(t, 68.8, 0.35)
        with Xf(c, 540, 700, -2, lerp(0.9, 1, ease_out(p)), clamp(p * 2)):
            card(c, -340, -260, 680, 520, "#F1EAD7", r=4)
            text(c, "SỔ TRỰC", -300, -190, "mono", 40, "ink")
            for k in range(7):
                c.drawLine(-300, -120 + k * 50, 300 - (k % 3) * 70, -120 + k * 50, paint("grey", 140, stroke=4))
        stamp(c, "KHIỂN TRÁCH", 560, 760, prog(t, 69.7, 69.9), size=62, rot=-8)
        note_label(c, "MINH HỌA", 770, 470, 1)
        chip(c, "1984 · RỜI QUÂN ĐỘI", W / 2, 1110, pop_in(t, 72.4), size=38)
        return
    if t < 81.59:
        n = int(lerp(1983, 1998, prog(t, 74.0, 75.7)))
        if t < 77.85:
            text(c, str(n), W / 2, 760, "xbold", 220, "ink", align="center")
            label_tag(c, "giữ kín 15 năm", W / 2, 480, pop_in(t, 74.0), size=40, anchor="center", bg="yellow")
            return
        pe = pop_in(t, 77.85, 0.35)
        A("votintsev").framed(c, W / 2, 640, 520, rot=lerp(-3, -1.5, pe), scale=lerp(0.94, 1, pe))
        name_tag(c, 60, 1010, "Tướng Yury Votintsev", "cấp trên cũ · kể lại trong hồi ký năm 1998", pop_in(t, 78.3, 0.4), size=44, role_size=28)
        caption_dark(c, "Ảnh: Wikipedia tiếng Nga", 1205)
        return
    ph = A("petrov_dresden_2013")
    ph.blur_bg(c, 120)
    pe = pop_in(t, 81.59, 0.35)
    ph.framed(c, W / 2, 640, 1000, rot=lerp(-2, -1, pe), scale=lerp(0.95, 1, pe) + 0.006 * max(0, t - 82.0))
    label_tag(c, "\"người đã cứu thế giới\"", W / 2, 1040, pop_in(t, 83.4), size=40, anchor="center", bg="yellow")
    caption(c, "Ảnh: Petrov được vinh danh tại nhà hát Semperoper, Dresden", 1120)


def s12_end(c, t):
    if t < 88.59:
        ph = A("fryazino_2010")
        z = lerp(1.0, 1.06, prog(t, 85.12, 88.59, lambda q: q))
        ph.cover(c, skia.Rect.MakeWH(W, H), 0.5, 0.5, z)
        label_tag(c, "FRYAZINO · gần Moskva", 60, 1100, pop_in(t, 86.8), size=36, bg="yellow")
        caption(c, "Ảnh: Fryazino, 19/5/2010 (Wikimedia Commons)", 1180)
        return
    if t < 94.05:
        draw_paper(c)
        pe = pop_in(t, 88.59, 0.35)
        A("petrov_late").framed(c, W / 2, 620, 520, rot=lerp(3, 1.5, pe), scale=lerp(0.94, 1, pe), alpha=lerp(1, 0.85, prog(t, 91.0, 92.0)))
        chip(c, "19 THÁNG 5 · 2017", W / 2, CHIP_Y, pop_in(t, 88.65))
        label_tag(c, "gần bốn tháng không ai biết", W / 2, 1000, pop_in(t, 92.0), size=36, anchor="center", bg="yellow")
        return
    if t < 100.8:
        night(c)
        chip(c, "7 THÁNG 9 · 2017 · SINH NHẬT ÔNG", W / 2, CHIP_Y, pop_in(t, 94.1), size=34)
        sh = 6 * math.sin(t * 60) if 96.4 < t < 98.4 else 0
        phone(c, 540 + sh, 660, 1.0, pop_in(t, 95.9), lift=prog(t, 98.5, 98.9))
        if 96.4 < t < 98.4:
            rings(c, 540, 600, t, 96.4, 98.4, "white", max_r=300, period=0.4, width=4, a=150)
        label_tag(c, "Karl Schumacher · người bạn Đức", W / 2, 960, pop_in(t, 96.4), size=32, anchor="center")
        label_tag(c, "Dmitry · con trai ông nghe máy", W / 2, 1040, pop_in(t, 98.6), size=32, anchor="center", bg="yellow")
        return
    ph = A("memorial_stone_pl")
    z = lerp(1.0, 1.06, prog(t, 100.8, 104.1, lambda q: q))
    ph.cover(c, skia.Rect.MakeWH(W, H), 0.5, 0.45, z)
    caption(c, "Đá tưởng niệm Stanislav Petrov (1939–2017), khắc tiếng Ba Lan", 1190)
    if t > 102.9:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("ink", 255 * prog(t, 102.9, 104.0, lambda q: q)))


TIMELINE = [
    (0.00, 5.60, s01_night),
    (5.60, 9.92, s02_decide),
    (9.92, 14.00, s03_petrov),
    (14.00, 22.55, s04_bunker),
    (22.55, 26.89, s05_role),
    (26.89, 32.59, s06_kal),
    (32.59, 40.60, s07_alarm),
    (40.60, 53.00, s08_reason),
    (53.00, 60.85, s09_wait),
    (60.85, 67.46, s10_cause),
    (67.46, 85.12, s11_aftermath),
    (85.12, 104.20, s12_end),
]


def draw_frame(c, t):
    for a, b, fn in TIMELINE:
        if a <= t < b:
            fn(c, t)
            break
