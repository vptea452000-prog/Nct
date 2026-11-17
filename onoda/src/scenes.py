"""Bảng dựng tập Onoda — phong cách hoạt hình 2D với linh vật kênh. Mốc giây theo MP3 (ước lượng, build/words.json).
Ảnh thật lồng vào cảnh như ảnh in có viền; chỉ dùng ảnh đã xác minh (xem BAN_GIAO.md)."""
import math
import skia
from lib import *  # noqa
from toon import *  # noqa
from sets import cam, grad_rect, vignette, blurred, frond, jungle, fg_leaves, bookshop, plane, sea_sky

PH = ROOT / "assets/photos"
_ph = {}


def P(key):
    if key not in _ph:
        _ph[key] = Photo(PH / f"{key}.jpg")
    return _ph[key]


def pop(t, t0, d=0.3):
    return prog(t, t0, t0 + d)


def photo_card(c, key, cx, cy, w, t, t0, rot=-3.0, crop=None):
    """Ảnh thật như tấm ảnh in viền trắng, nét viền hoạt hình, bật vào."""
    p = pop(t, t0, 0.4)
    if p <= 0:
        return 0
    ph = P(key)
    x0, y0, x1, y1 = crop or (0, 0, 1, 1)
    h = w * (y1 - y0) * ph.h / ((x1 - x0) * ph.w)
    sc = lerp(0.85, 1.0, back_out(p)) + 0.004 * max(0, t - t0 - 0.4)
    with Xf(c, cx, cy, rot, sc, clamp(p * 2)):
        fill_out(c, rrect_path(-w / 2 - 22, -h / 2 - 22, w + 44, h + 70, 6), "#FBF7EE")
        c.drawImageRect(ph.img, skia.Rect.MakeXYWH(x0 * ph.w, y0 * ph.h, (x1 - x0) * ph.w, (y1 - y0) * ph.h),
                        skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), SAMP, None, skia.Canvas.kStrict_SrcRectConstraint)
        c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), paint(OUT, stroke=4, cap=False))
    return h


def cap(c, s, y=1240, size=26):
    text(c, s, W / 2, y, "semi", size, "white", a=235, align="center", stroke=3, stroke_color="#1A120D")


def rays(c, t, color="#F4C430", a=60, cx=540, cy=760):
    for k in range(14):
        ang = k * math.pi / 7 + t * 0.12
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + 1700 * math.cos(ang), cy + 1700 * math.sin(ang)); p.lineTo(cx + 1700 * math.cos(ang + 0.18), cy + 1700 * math.sin(ang + 0.18)); p.close()
        c.drawPath(p, paint(color, a))


def bubble(c, x, y, l1, l2=None, t=0, t0=0, rot=-3, w=None, red2=True):
    p = pop(t, t0, 0.35)
    if p <= 0:
        return
    w = w or max(tw(l1, "xbold", 50), tw(l2 or "", "xbold", 44)) + 90
    h = 120 if not l2 else 170
    with Xf(c, x, y, rot, max(0.01, back_out(p))):
        fill_out(c, rrect_path(-w / 2, -h / 2, w, h, 60), "white")
        tail = skia.Path(); tail.moveTo(-40, h / 2 - 4); tail.lineTo(-90, h / 2 + 60); tail.lineTo(10, h / 2 - 4); tail.close()
        fill_out(c, tail, "white")
        c.drawRect(skia.Rect.MakeXYWH(-45, h / 2 - 12, 60, 14), paint("white"))
        if l2:
            text(c, l1, 0, -12, "xbold", 50, "ink", align="center")
            text(c, l2, 0, 50, "xbold", 44, "#C0392B" if red2 else "ink", align="center")
        else:
            text(c, l1, 0, 18, "xbold", 50, "ink", align="center")


def stamp_big(c, s, x, y, t, t0, color="#C0392B", rot=-10, size=80):
    stamp(c, s, x, y, prog(t, t0, t0 + 0.22), size=size, color=color, rot=rot)


def night_jungle(c, t, z=1.15, cx=540, cy=880):
    c.save(); cam(c, cx, cy, z); jungle(c, t); c.restore()
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#0E1A2B", 150))


# ---------------------------------------------------------------- nhân vật mới
def young_man(c, x, y, s=1.0, t=0.0, look=0.0, smile=True, pack=True):
    """Chàng trai đi tìm (Suzuki) — áo phông, ba lô, tóc dài."""
    with Xf(c, x, y, 0, s):
        for side in (-1, 1):
            limb(c, [(side * 30, -250), (side * 34, -40)], 46, "#3E5A8A")
            fill_out(c, rrect_path(side * 34 - 32 + side * 8, -46, 64, 46, 16), "#5A4030")
        if pack:
            fill_out(c, rrect_path(-120, -500, 70, 220, 24), "#C0392B")
        torso = skia.Path(); torso.moveTo(-85, -510); torso.lineTo(85, -510); torso.lineTo(92, -240); torso.lineTo(-92, -240); torso.close()
        fill_out(c, torso, "#E9E2CF")
        for side in (-1, 1):
            limb(c, [(side * 85, -490), (side * 112, -380), (side * 100, -290)], 32, "#E9E2CF")
            c.drawCircle(side * 100, -282, 18, paint(SKIN)); c.drawCircle(side * 100, -282, 18, paint(OUT, stroke=5))
        fill_out(c, rrect_path(-24, -550, 48, 46, 10), SKIN_D, ow=5)
        head = oval_path(0, -630, 74, 86); fill_out(c, head, SKIN)
        hair = skia.Path(); hair.moveTo(-80, -600); hair.quadTo(-86, -720, 0, -718); hair.quadTo(86, -720, 80, -600); hair.lineTo(64, -650); hair.quadTo(0, -690, -64, -650); hair.close()
        fill_out(c, hair, "#2A2420", ow=5)
        bl = blink(t, 0.7)
        for side in (-1, 1):
            c.save(); c.translate(side * 28 + look * 8, -630); c.scale(1, bl)
            c.drawOval(skia.Rect.MakeXYWH(-8, -9, 16, 18), paint(OUT)); c.restore()
        m = skia.Path(); m.moveTo(-24, -590); m.quadTo(0, -570 if smile else -596, 24, -590)
        c.drawPath(m, paint(OUT, stroke=7))


def president(c, x, y, s=1.0, t=0.0, arms="take"):
    """Tổng thống (minh họa) — áo barong trắng, không vẽ theo khuôn mặt người thật."""
    with Xf(c, x, y, 0, s):
        for side in (-1, 1):
            limb(c, [(side * 30, -250), (side * 34, -40)], 48, "#2E2A25")
            fill_out(c, rrect_path(side * 34 - 32 + side * 8, -46, 64, 46, 16), "#1C1814")
        torso = skia.Path(); torso.moveTo(-90, -520); torso.lineTo(90, -520); torso.lineTo(98, -240); torso.lineTo(-98, -240); torso.close()
        fill_out(c, torso, "#F6F1E4")
        for k in range(4):
            c.drawLine(-40 + k * 26, -500, -40 + k * 26, -260, paint("#D8CDB4", stroke=4))
        if arms == "take":
            limb(c, [(-90, -500), (-170, -420), (-230, -430)], 32, "#F6F1E4")
            limb(c, [(90, -500), (110, -380), (100, -290)], 32, "#F6F1E4")
        else:
            for side in (-1, 1):
                limb(c, [(side * 90, -500), (side * 110, -380), (side * 100, -290)], 32, "#F6F1E4")
        fill_out(c, rrect_path(-26, -560, 52, 48, 10), SKIN_D, ow=5)
        head = oval_path(0, -640, 76, 88); fill_out(c, head, "#D9AE84")
        hair = skia.Path(); hair.moveTo(-76, -640); hair.quadTo(-70, -735, 0, -730); hair.quadTo(70, -735, 76, -640); hair.lineTo(62, -680); hair.quadTo(0, -700, -62, -680); hair.close()
        fill_out(c, hair, "#1F1A16", ow=5)
        for side in (-1, 1):
            c.drawOval(skia.Rect.MakeXYWH(side * 28 - 8, -650, 16, 18), paint(OUT))
        m = skia.Path(); m.moveTo(-22, -598); m.quadTo(0, -584, 22, -598)
        c.drawPath(m, paint(OUT, stroke=7))


def sword(c, x, y, ang, s=1.0):
    with Xf(c, x, y, ang, s):
        blade = skia.Path(); blade.moveTo(0, -8); blade.quadTo(200, -26, 340, -8); blade.lineTo(340, 4); blade.quadTo(200, -10, 0, 8); blade.close()
        fill_out(c, blade, "#D6DCE0", ow=5)
        fill_out(c, rrect_path(-20, -26, 16, 52, 6), "#C9A55A", ow=5)
        fill_out(c, rrect_path(-130, -12, 112, 24, 10), "#3A2618", ow=5)


def leaflet(c, x, y, rot, s=1.0, fake=0.0):
    with Xf(c, x, y, rot, s):
        fill_out(c, rrect_path(-150, -200, 300, 400, 6), "#F1EAD7")
        text(c, "LỆNH", 0, -110, "xbold", 52, "ink", align="center")
        text(c, "ĐẦU HÀNG", 0, -50, "xbold", 44, "ink", align="center")
        for k in range(6):
            c.drawLine(-110, 10 + k * 30, 110 - (k % 2) * 40, 10 + k * 30, paint("#8E846F", stroke=6))


def fire(c, x, y, s, t, seed=0):
    with Xf(c, x, y, 0, s):
        for k, (colr, sc) in enumerate([("#C0392B", 1.0), ("#F39C12", 0.72), ("#F4D03F", 0.45)]):
            fl = skia.Path()
            wob = 10 * math.sin(t * 12 + seed + k)
            fl.moveTo(-60 * sc, 0); fl.quadTo(-70 * sc, -90 * sc, wob, -190 * sc); fl.quadTo(70 * sc, -90 * sc, 60 * sc, 0); fl.close()
            c.drawPath(fl, paint(colr, 235))


def rice(c, x0, x1, y, t):
    for k in range(int((x1 - x0) / 34)):
        x = x0 + k * 34
        for j in range(3):
            c.drawLine(x + j * 8, y, x + j * 8 + 6 * math.sin(t * 2 + k), y - 70 - (k % 3) * 10, paint("#C9A54A", stroke=5))


# ---------------------------------------------------------------- CẢNH
def s01_open(c, t):
    if t < 4.17:
        z = lerp(1.0, 1.18, ease_in_out(clamp(t / 4.0)))
        c.save(); cam(c, 540, 880, z); jungle(c, t); c.restore()
        blurred(c, 10, lambda: fg_leaves(c, t))
        vignette(c)
        big_title(c, "1974", "PHILIPPINES", 560, prog(t, 0.6, 1.0), size=150, bsize=56)
        pm = prog(t, 2.2, 2.8, back_out)
        mascot(c, 880, lerp(1500, 1260, pm), 0.85, "smile", t=t, arm="binoc", rot=-6)
        return
    if t < 7.2:
        c.save(); cam(c, 540, 900, 1.2 + 0.02 * (t - 4.17)); jungle(c, t); c.restore()
        pe = prog(t, 4.25, 5.0, ease_out)
        soldier(c, lerp(-200, 470, pe), 1250, 1.2, "alert", t=t, look=0.6)
        blurred(c, 12, lambda: fg_leaves(c, t))
        vignette(c)
        label_tag(c, "sĩ quan Nhật · quân phục · súng", W / 2, 330, pop(t, 4.9), size=34, anchor="center", bg="yellow")
        return
    c.save(); cam(c, 470, 700, lerp(1.6, 1.85, clamp((t - 7.2) / 1.5))); jungle(c, t)
    soldier(c, 470, 1290, 1.25, "salute", t=t, mouth="shout")
    c.restore()
    vignette(c, 170)
    bubble(c, 640, 420, "THẾ CHIẾN", "CHƯA KẾT THÚC!", t=t, t0=7.3)


def s02_bookshop(c, t):
    if t < 12.1:
        c.save(); cam(c, 540, 900, lerp(1.25, 1.1, ease_out(clamp((t - 8.7) / 1.0)))); bookshop(c, t)
        bookseller(c, 640, 1290, 1.15, t=t, pose="read", look=-0.5)
        mascot(c, 230, 1020, 0.75, "think", look=(1, 0), t=t)
        c.restore()
        vignette(c, 120)
        label_tag(c, "chỉ huy cũ", W / 2, 330, pop(t, 9.6), size=36, anchor="center")
        label_tag(c, "nay bán sách", W / 2, 410, pop(t, 11.2), size=36, anchor="center", bg="yellow")
        return
    c.save(); cam(c, 540, 900, 1.1); sea_sky(c, t)
    p = clamp((t - 12.1) / 1.45)
    plane(c, lerp(-200, 1300, p), lerp(700, 560, p), 1.4)
    c.restore()
    label_tag(c, "bay sang đọc lệnh", W / 2, 330, pop(t, 12.2), size=36, anchor="center", bg="yellow")


def s03_name(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#D4BE86")
    rays(c, t)
    photo_card(c, "onoda_young", W / 2, 640, 560, t, 13.6, rot=-3)
    pn = pop(t, 14.4, 0.4)
    if pn > 0:
        with Xf(c, W / 2, 1100 + (1 - ease_out(pn)) * 60, -2, 1, clamp(pn * 2)):
            fill_out(c, rrect_path(-400, -80, 800, 170, 18), "#2E2A25")
            text(c, "HIROO ONODA", 0, 10, "xbold", 72, "#F4C430", align="center")
            text(c, "thiếu úy · Lục quân Đế quốc Nhật", 0, 64, "semi", 32, "white", align="center")
    mascot(c, 930, 1290, 0.55, "smile", look=(-1, -0.4), t=t, arm="point")
    cap(c, "Ảnh: Hiroo Onoda thời trẻ (Wikimedia Commons)", 345, 26)


def ph_map(c, t, lon0=119.2, lon1=122.2, lat0=12.6, lat1=15.6):
    """Bản đồ hoạt hình Luzon – Lubang."""
    grad_rect(c, skia.Rect.MakeWH(W, H), "#7FB3D5", "#4F8FB8")
    sx = W / (lon1 - lon0)

    def pr(lon, lat):
        return (lon - lon0) * sx, 300 + (lat1 - lat) * sx

    for ring in RINGS_PH:
        p = skia.Path()
        for j, (lon, lat) in enumerate(ring):
            (p.moveTo if j == 0 else p.lineTo)(*pr(lon, lat))
        p.close()
        fill_out(c, p, "#9BC27A", ow=6)
    lx, ly = pr(120.12, 13.82)
    isl = oval_path(lx, ly, 34, 18); fill_out(c, isl, "#9BC27A", ow=5)
    return pr


def s04_lubang(c, t):
    if t < 18.88:
        pr = ph_map(c, t)
        chip(c, "CUỐI 1944", W / 2, 250, pop(t, 15.85))
        mx, my = pr(120.98, 14.6)
        lx, ly = pr(120.12, 13.82)
        pin(c, mx, my, pop(t, 16.3), color="white")
        label_tag(c, "MANILA", mx + 26, my - 44, pop(t, 16.3), size=34)
        pin(c, lx, ly, pop(t, 17.6))
        label_tag(c, "ĐẢO LUBANG", lx - 26, ly + 70, pop(t, 17.6), size=36, anchor="right", bg="yellow")
        pa = prog(t, 18.0, 18.8, ease_in_out)
        if pa > 0:
            r = path_partial(c, [(mx, my), (lx + 30, ly - 10)], pa, paint(OUT, stroke=7, PathEffect=skia.DashPathEffect.Make([18, 12], 0)), curve=0.2)
            if r:
                arrow_head(c, *r, size=26, color=OUT)
        return
    if t < 21.44:
        grad_rect(c, skia.Rect.MakeWH(W, H), "#2E4A62", "#13263B")
        photo_card(c, "lubang_aerial", W / 2, 640, 940, t, 18.9, rot=-2)
        cap(c, "Ảnh: quần đảo Lubang nhìn từ trên cao, chụp sau này", 1010, 26)
        stamp_big(c, "KHÔNG ĐẦU HÀNG", W / 2, 1120, t, 20.3, size=70, rot=-6)
        return
    c.save(); cam(c, 540, 880, 1.15); jungle(c, t)
    walk = clamp((t - 21.6) / 2.8)
    for k in range(4):
        soldier(c, lerp(180, 1200, walk) - k * 180, 1250 - (k % 2) * 10, 0.65 if k else 0.75, "stand", t=t + k, look=0.6)
    c.restore()
    blurred(c, 12, lambda: fg_leaves(c, t))
    vignette(c)
    label_tag(c, "quân Mỹ đổ bộ · Onoda và 3 lính rút vào núi", W / 2, 330, pop(t, 21.6), size=30, anchor="center", bg="yellow")


def s05_leaflets(c, t):
    if t < 27.43:
        night_jungle(c, t, 1.1)
        big_title(c, "8 · 1945", "NHẬT ĐẦU HÀNG", 620, pop(t, 24.6, 0.4), size=140, bsize=58)
        return
    if t < 31.75:
        c.save(); cam(c, 540, 880, 1.1); jungle(c, t)
        p = clamp((t - 27.5) / 2.4)
        plane(c, lerp(-250, 1300, p), lerp(420, 360, p), 1.1)
        for k in range(14):
            st = 28.0 + k * 0.17
            a = t - st
            if a > 0:
                x = lerp(-250, 1300, clamp((st - 27.5) / 2.4)) + 40 * math.sin(a * 3 + k) + a * 30
                y = 380 + a * 260
                leaflet(c, x, y, a * 140 + k * 30, 0.18)
        c.restore()
        label_tag(c, "truyền đơn in lệnh đầu hàng", W / 2, 330, pop(t, 30.2), size=34, anchor="center", bg="yellow")
        return
    if t < 35.02:
        c.save(); cam(c, 540, 900, 1.25); jungle(c, t)
        soldier(c, 330, 1290, 1.15, "attention", t=t, look=0.8, mouth="frown")
        c.restore()
        leaflet(c, 760, 760, 6, 1.1)
        note_label(c, "MINH HỌA", 650, 520, 1)
        stamp_big(c, "ĐỒ GIẢ!", 760, 760, t, 33.4, size=90)
        mascot(c, 940, 1260, 0.5, "worried", look=(-1, 0), t=t)
        return
    night_jungle(c, t, 1.15)
    soldier(c, 540, 1270, 1.15, "attention", t=t, look=0.0, mouth="flat")
    for k in range(5):
        st = 35.6 + k * 0.4
        a = t - st
        if a > 0:
            x = lerp(-150, 540 - 160 + k * 60, clamp(a / 0.6)); y = 500 + k * 70
            bounce = clamp((a - 0.6) / 0.5)
            with Xf(c, lerp(x, x - 300, bounce), lerp(y, y - 200, bounce), k * 20 + a * 60, 0.9, 1 - bounce * 0.8):
                fill_out(c, rrect_path(-60, -40, 120, 80, 6), "#F1EAD7", ow=5)
                c.drawLine(-60, -40, 0, 8, paint(OUT, stroke=4)); c.drawLine(60, -40, 0, 8, paint(OUT, stroke=4))
    with Xf(c, 170, 520, 0, 1, pop(t, 35.7)):
        fill_out(c, rrect_path(-50, -40, 60, 80, 8), "#5A524A")
        horn = skia.Path(); horn.moveTo(10, -30); horn.lineTo(110, -80); horn.lineTo(110, 80); horn.lineTo(10, 30); horn.close()
        fill_out(c, horn, "#8E959B")
    label_tag(c, "loa · thư · vẫn không đổi ý", W / 2, 330, pop(t, 37.3), size=34, anchor="center", bg="yellow")


def s06_guerrilla(c, t):
    if t < 43.76:
        night_jungle(c, t, 1.1)
        rice(c, 0, W, 1240, t)
        if t > 41.1:
            for k in range(5):
                fire(c, 150 + k * 190, 1240, lerp(0.3, 0.9, pop(t, 41.1 + k * 0.08, 0.5)), t, k)
        for k, ts in enumerate([41.7, 42.1, 42.5, 42.9]):
            a = t - ts
            if 0 < a < 0.15:
                fl = paint("#F4D88A", 255 * (1 - a / 0.15)); fl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
                c.drawCircle(200 + k * 220, 760 + (k % 2) * 80, 50, fl)
        label_tag(c, "đánh du kích", W / 2, 330, pop(t, 38.7), size=38, anchor="center", bg="yellow")
        label_tag(c, "lấy lương thực · đốt lúa · nổ súng", W / 2, 410, pop(t, 39.8), size=32, anchor="center")
        return
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#1C1612"))
    text(c, "khoảng", W / 2, 620, "bold", 54, "white", a=200 * pop(t, 45.4), align="center")
    text(c, "30", W / 2, 860, "xbold", 260, "#E9E2CF", a=255 * pop(t, 46.3, 0.5), align="center")
    text(c, "người chết", W / 2, 960, "bold", 54, "white", a=200 * pop(t, 46.5), align="center")
    label_tag(c, "theo lời dân làng kể lại", W / 2, 420, pop(t, 43.9), size=34, anchor="center")


def s07_left(c, t):
    if t < 53.01:
        c.save(); cam(c, 540, 880, 1.1); jungle(c, t); c.restore()
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#0E1A2B", 60))
        xs = [190, 420, 650, 880]
        for k, x in enumerate(xs):
            a = 1.0
            dx = 0
            if k == 1:
                dx = 600 * ease_in_out(clamp((t - 49.2) / 1.5))
            if k == 2:
                a = 1 - 0.75 * pop(t, 51.6, 0.6)
            with Xf(c, 0, 0, 0, 1, a):
                soldier(c, x + dx, 1250, 0.6, "stand", t=t + k, look=0.3)
            if k == 2 and t > 51.8:
                pk = pop(t, 51.8, 0.3)
                c.drawLine(x - 70, 760, x - 70 + 140 * pk, 900 * 1 - 0 + 140 * pk - 140, paint("#C0392B", stroke=10))
        label_tag(c, "1950 · bỏ nhóm, ra đầu hàng", W / 2, 330, pop(t, 48.7), size=32, anchor="center", bg="yellow")
        label_tag(c, "1954 · bị bắn chết", W / 2, 410, pop(t, 51.1), size=32, anchor="center", bg="red", fg="white")
        return
    if t < 60.78:
        grad_rect(c, skia.Rect.MakeWH(W, H), "#2A2420", "#15110E")
        chip(c, "10 · 1972", W / 2, 250, pop(t, 53.1))
        photo_card(c, "kozuka", W / 2, 680, 520, t, 54.5, rot=2)
        name_tag(c, 60, 1060, "Kinshichi Kozuka", "người lính cuối cùng bên Onoda", pop(t, 55.2, 0.4), size=44, role_size=28)
        cap(c, "Ảnh: Kinshichi Kozuka (Wikimedia Commons)", 345, 26)
        if t > 57.6:
            c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 90 * pop(t, 57.6, 1.0)))
            label_tag(c, "bị cảnh sát bắn chết khi đang đốt lúa", W / 2, 1180, pop(t, 57.7), size=30, anchor="center", bg="red", fg="white")
        return
    c.save(); cam(c, 540, 880, lerp(1.0, 0.92, clamp((t - 60.8) / 1.8))); jungle(c, t)
    soldier(c, 540, 1250, 0.55, "stand", t=t, look=0.0)
    c.restore()
    vignette(c, 200)
    big_title(c, "MỘT MÌNH", None, 560, pop(t, 61.4, 0.4), size=110)


def s08_japan(c, t):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#D4BE86")
    if t < 66.59:
        with Xf(c, 560, 700, -4, lerp(0.8, 1, pop(t, 62.6, 0.4)), pop(t, 62.6, 0.3)):
            fill_out(c, rrect_path(-330, -330, 660, 660, 6), "#F6F1E4")
            text(c, "TIN NÓNG", -280, -250, "xbold", 54, "#C0392B")
            text(c, "KOZUKA", -280, -150, "xbold", 80, "ink")
            text(c, "TỬ TRẬN 1972", -280, -70, "xbold", 54, "ink")
            for k in range(7):
                c.drawLine(-280, 20 + k * 40, 280 - (k % 3) * 60, 20 + k * 40, paint("#8E846F", stroke=6))
        note_label(c, "MINH HỌA", 760, 320, 1)
        mascot(c, 880, 1280, 0.75, "shock", t=t, arm="up")
        label_tag(c, "Nhật Bản sững sờ", 330, 1150, pop(t, 63.6), size=40, bg="red", fg="white")
        return
    if t < 69.16:
        with Xf(c, 540, 700, 2, 1, pop(t, 66.6, 0.3)):
            fill_out(c, rrect_path(-320, -360, 640, 720, 4), "#F6F1E4")
            text(c, "CHÍNH PHỦ NHẬT", 0, -260, "xbold", 44, "ink", align="center")
            text(c, "1959", 0, -150, "xbold", 90, "ink", align="center")
            text(c, "những người lính này", 0, -40, "semi", 38, "grey", align="center")
            text(c, "đều đã chết", 0, 10, "semi", 38, "grey", align="center")
        note_label(c, "MINH HỌA", 700, 290, 1)
        stamp_big(c, "ĐÃ CHẾT", 560, 900, t, 68.3, size=80)
        return
    rays(c, t, "#F4C430", 50)
    photo_card(c, "onoda_young", W / 2, 640, 480, t, 69.2, rot=-2)
    stamp_big(c, "CÒN SỐNG?", W / 2, 1050, t, 72.0, color="#1F3A5F", size=70, rot=-5)
    mascot(c, 900, 1290, 0.6, "think", look=(-1, -0.5), t=t)


def s09_suzuki(c, t):
    if t < 78.85:
        c.save(); cam(c, 540, 880, 1.15); jungle(c, t)
        pw = clamp((t - 73.3) / 5.5)
        young_man(c, lerp(-120, 520, pw), 1250, 1.05, t=t, look=0.6)
        c.restore()
        blurred(c, 12, lambda: fg_leaves(c, t))
        vignette(c)
        chip(c, "2 · 1974", W / 2, 250, pop(t, 73.4))
        name_tag(c, 60, 360, "Norio Suzuki", "chàng trai Nhật · một mình tới Lubang", pop(t, 75.4, 0.4), size=44, role_size=28)
        return
    if t < 81.67:
        c.save(); cam(c, 540, 900, 1.2); jungle(c, t)
        young_man(c, 330, 1250, 1.0, t=t, look=0.6)
        pe = prog(t, 80.0, 80.8, ease_out)
        soldier(c, lerp(1250, 760, pe), 1250, 1.0, "alert", t=t, look=-0.6, beard=0.0)
        c.restore()
        n = min(4, 1 + int(clamp((t - 78.9) / 0.8) * 4))
        label_tag(c, f"ngày {n}", W / 2, 330, 1, size=40, anchor="center", bg="yellow")
        return
    if t < 83.27:
        grad_rect(c, skia.Rect.MakeWH(W, H), "#2E4A62", "#13263B")
        a = t - 81.67
        if a < 0.12:
            c.drawRect(skia.Rect.MakeWH(W, H), paint("white", 255 * (1 - a / 0.12)))
        photo_card(c, "suzuki_onoda_1974", W / 2, 680, 900, t, 81.7, rot=-2)
        cap(c, "Suzuki (trái) và Onoda trên đảo Lubang, 2/1974", 1040, 28)
        return
    c.save(); cam(c, 640, 760, 1.6); jungle(c, t)
    shake = 6 * math.sin((t - 83.3) * 14) if t < 84.8 else 0
    soldier(c, 640 + shake, 1290, 1.2, "attention", t=t, mouth="flat")
    c.restore()
    vignette(c, 170)
    bubble(c, 560, 420, "CHỈ ĐI", "KHI CÓ LỆNH CẤP TRÊN", t=t, t0=85.2)


def s10_order(c, t):
    if t < 89.22:
        c.save(); cam(c, 540, 900, 1.1); sea_sky(c, t)
        p = clamp((t - 87.75) / 1.45)
        plane(c, lerp(1300, -200, p), lerp(560, 700, p), -1.4)
        c.restore()
        label_tag(c, "Suzuki mang ảnh về Nhật", W / 2, 330, pop(t, 87.8), size=34, anchor="center", bg="yellow")
        return
    if t < 94.12:
        c.save(); cam(c, 540, 900, 1.15); bookshop(c, t)
        bookseller(c, 600, 1290, 1.15, t=t, pose="stand", look=0.3)
        c.restore()
        vignette(c, 120)
        name_tag(c, 60, 360, "Thiếu tá Yoshimi Taniguchi", "chỉ huy cũ · nay bán sách", pop(t, 91.3, 0.4), size=42, role_size=28)
        return
    if t < 98.98:
        c.save(); cam(c, 540, 880, 1.12); jungle(c, t)
        pw = clamp((t - 96.4) / 2.2)
        bookseller(c, lerp(1250, 760, pw), 1250, 0.95, t=t, pose="stand", look=-0.6)
        young_man(c, lerp(1450, 960, pw), 1250, 0.9, t=t, look=-0.6, pack=False)
        c.restore()
        blurred(c, 12, lambda: fg_leaves(c, t))
        vignette(c)
        chip(c, "9 · 3 · 1974", W / 2, 250, pop(t, 94.2))
        label_tag(c, "điểm hẹn trong rừng", W / 2, 340, pop(t, 97.4), size=34, anchor="center", bg="yellow")
        return
    c.save(); cam(c, 540, 900, 1.15); jungle(c, t)
    pose = "salute" if t < 100.2 else "attention"
    soldier(c, 330, 1250, 1.05, pose, t=t, look=0.6)
    bookseller(c, 760, 1250, 1.05, t=t, pose="read" if t > 100.2 else "stand", look=-0.6)
    c.restore()
    blurred(c, 12, lambda: fg_leaves(c, t))
    vignette(c)
    if t < 100.2:
        label_tag(c, "đứng nghiêm chào", W / 2, 330, pop(t, 99.0), size=36, anchor="center", bg="yellow")
    bubble(c, 640, 420, "MIỄN TOÀN BỘ", "NHIỆM VỤ CHIẾN ĐẤU", t=t, t0=101.3, red2=False)


def s11_surrender(c, t):
    if t < 107.3:
        grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#D4BE86")
        rays(c, t, "#F4C430", 45)
        photo_card(c, "onoda_walkout_1974", W / 2, 640, 600, t, 104.15, rot=2)
        label_tag(c, "ra trình diện · trạm radar trên đảo", W / 2, 1150, pop(t, 104.9), size=32, anchor="center", bg="yellow")
        cap(c, "Ảnh: Onoda rời rừng, 3/1974", 1220, 26)
        return
    if t < 110.93:
        grad_rect(c, skia.Rect.MakeWH(W, H), "#6B4A30", "#3A2618")
        fill_out(c, rrect_path(60, 1090, 960, 60, 10), "#8A6542")
        with Xf(c, 540, 760, -4, 1, pop(t, 107.4)):
            gun = skia.Path(); gun.moveTo(-380, 0); gun.lineTo(300, -20); gun.lineTo(380, -10); gun.lineTo(380, 20); gun.lineTo(-200, 30); gun.lineTo(-380, 60); gun.close()
            fill_out(c, gun, "#6B4A30")
            c.drawRect(skia.Rect.MakeXYWH(-40, -34, 300, 14), paint("#3A3632"))
        label_tag(c, "súng trường · vẫn bắn được", W / 2, 400, pop(t, 107.6), size=34, anchor="center", bg="yellow")
        n = int(lerp(0, 500, prog(t, 109.1, 110.3, lambda q: q)))
        if t > 109.0:
            text(c, f"{n} viên đạn", W / 2, 620, "xbold", 74, "white", align="center", stroke=6, stroke_color="#1A120D")
        for k in range(3):
            pg = pop(t, 110.0 + k * 0.15)
            if pg > 0:
                with Xf(c, 640 + k * 120, 1040, 0, max(0.01, back_out(pg))):
                    fill_out(c, oval_path(0, 0, 44, 54), "#4E5E3A"); fill_out(c, rrect_path(-16, -78, 32, 30, 6), "#3A3632", ow=5)
        return
    if t < 115.28:
        grad_rect(c, skia.Rect.MakeWH(W, H), "#E2B77A", "#B98A52")
        chip(c, "11 · 3 · 1974", W / 2, 250, pop(t, 111.0))
        soldier(c, 300, 1250, 0.95, "attention", t=t, look=0.6)
        president(c, 780, 1250, 0.95, t=t, arms="take")
        pa = prog(t, 112.0, 113.2, ease_in_out)
        sword(c, lerp(360, 470, pa), lerp(990, 880, pa), -6, 1.0)
        name_tag(c, 60, 320, "Tổng thống Ferdinand Marcos", "Philippines", pop(t, 113.4, 0.4), size=40, role_size=28)
        note_label(c, "HOẠT HÌNH MINH HỌA", 640, 440, 1)
        return
    grad_rect(c, skia.Rect.MakeWH(W, H), "#F2B36B", "#E9D9A6")
    rays(c, t, "#FFFFFF", 40, cy=900)
    soldier(c, 540, 1250, 1.0, "stand", t=t, look=0.0, mouth="flat")
    stamp_big(c, "ÂN XÁ", 540, 420, t, 115.4, color="#1F3A5F", size=100, rot=-8)
    label_tag(c, "vì ông vẫn tin chiến tranh còn tiếp diễn", W / 2, 1140, pop(t, 116.8), size=30, anchor="center", bg="yellow")
    if t > 119.6:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 255 * prog(t, 119.6, 120.8, lambda q: q)))


RINGS_PH = country_rings("Philippines")

TIMELINE = [
    (0.00, 8.71, s01_open),
    (8.71, 13.57, s02_bookshop),
    (13.57, 15.77, s03_name),
    (15.77, 24.48, s04_lubang),
    (24.48, 38.61, s05_leaflets),
    (38.61, 47.39, s06_guerrilla),
    (47.39, 62.58, s07_left),
    (62.58, 73.30, s08_japan),
    (73.30, 87.73, s09_suzuki),
    (87.73, 104.10, s10_order),
    (104.10, 120.90, s11_surrender),
]


def draw_frame(c, t):
    for a, b, fn in TIMELINE:
        if a <= t < b:
            fn(c, t)
            break
