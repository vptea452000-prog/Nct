"""Bối cảnh và cảnh dựng sẵn từ bản thử (rừng, hiệu sách, máy bay, biển) — dùng lại cho cả tập."""
import math
import skia
from lib import *  # noqa
from toon import *  # noqa

DUR = 17.5


def cam(c, cx, cy, z):
    """Máy quay: phóng z quanh điểm (cx, cy) của cảnh, đưa điểm đó về giữa khung."""
    c.translate(W / 2, H / 2)
    c.scale(z, z)
    c.translate(-cx, -cy)


def grad_rect(c, rect, top, bottom):
    sh = skia.GradientShader.MakeLinear([skia.Point(0, rect.top()), skia.Point(0, rect.bottom())], [col(top), col(bottom)])
    c.drawRect(rect, skia.Paint(Shader=sh))


def vignette(c, a=150):
    sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42), 1250, [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(a, 15, 8, 4)], [0.5, 1.0])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=sh))


def blurred(c, sigma, fn):
    c.saveLayer(None, skia.Paint(ImageFilter=skia.ImageFilters.Blur(sigma, sigma)))
    fn()
    c.restore()


def frond(c, x, y, L, ang, color, w=1.0):
    """Lá cọ/lá rừng: cuống cong + các lá chét."""
    with Xf(c, x, y, ang, 1):
        stem = skia.Path(); stem.moveTo(0, 0); stem.quadTo(L * 0.5, -L * 0.15, L, 0)
        c.drawPath(stem, paint(color, stroke=8 * w))
        for k in range(1, 12):
            u = k / 12
            px, py = L * u, -L * 0.15 * 4 * u * (1 - u) * 0.5
            ll = L * 0.32 * (1 - abs(u - 0.4))
            for side in (-1, 1):
                lf = skia.Path()
                lf.moveTo(px, py)
                lf.quadTo(px + ll * 0.4, py + side * ll * 0.6, px + ll * 0.7, py + side * ll * 0.9)
                lf.quadTo(px + ll * 0.2, py + side * ll * 0.4, px, py)
                c.drawPath(lf, paint(color))


def jungle(c, t, light=1.0):
    grad_rect(c, skia.Rect.MakeXYWH(-600, -400, W + 1200, 1500), "#F2B36B", "#E9D9A6")
    c.drawCircle(760, 420, 110, paint("#FFE7A8", 230))
    for k, (yy, colr) in enumerate([(820, "#8FA79A"), (900, "#6F8C7C"), (980, "#4F6F5F")]):
        p = skia.Path(); p.moveTo(-600, 1400)
        for i in range(0, 25):
            x = -600 + i * 120
            p.lineTo(x, yy - 120 * abs(math.sin(i * 0.9 + k)) - 40 * k)
        p.lineTo(W + 600, 1400); p.close()
        c.drawPath(p, paint(colr))
    # thân cây và tán rừng giữa
    for i, x in enumerate([-200, 80, 330, 640, 900, 1180]):
        c.drawRect(skia.Rect.MakeXYWH(x, 760, 40, 700), paint("#3B4A36"))
        c.drawCircle(x + 20, 760, 170, paint("#2F4A33"))
        c.drawCircle(x - 90, 820, 120, paint("#3A5A3C"))
        c.drawCircle(x + 130, 830, 130, paint("#355437"))
    grad_rect(c, skia.Rect.MakeXYWH(-600, 1150, W + 1200, 900), "#3E5A34", "#253A22")
    for x in range(-500, W + 600, 160):
        frond(c, x, 1180 + (x % 3) * 20, 260, -150 + (x % 5) * 12, "#2C4A2A")


def fg_leaves(c, t, alpha=255):
    for x, y, L, a in [(-80, 300, 520, 20), (1160, 520, 560, 160), (-60, 1500, 600, -15), (1180, 1650, 620, 200)]:
        frond(c, x + 8 * math.sin(t * 1.2 + x), y, L, a + 3 * math.sin(t * 1.5 + y), "#1B2E19", w=1.6)


def bookshop(c, t):
    grad_rect(c, skia.Rect.MakeXYWH(-600, -400, W + 1200, 2400), "#E2B77A", "#B98A52")
    for r in range(6):
        y = 300 + r * 190
        c.drawRect(skia.Rect.MakeXYWH(-500, y + 150, W + 1000, 26), paint("#5E3F26"))
        x = -480
        k = 0
        while x < W + 500:
            w_ = 26 + (k * 37 % 30)
            h_ = 110 + (k * 53 % 40)
            colr = ["#7B3B2E", "#2E4A62", "#3E5A3C", "#8A6A3A", "#5A3E5E", "#A4532E"][k % 6]
            c.drawRect(skia.Rect.MakeXYWH(x, y + 150 - h_, w_, h_), paint(colr))
            c.drawRect(skia.Rect.MakeXYWH(x, y + 150 - h_, w_, h_), paint(OUT, 120, stroke=3, cap=False))
            x += w_ + 3
            k += 1
    c.drawRect(skia.Rect.MakeXYWH(-600, 1290, W + 1200, 800), paint("#6B4A30"))
    sign = rrect_path(300, 170, 480, 110, 14)
    fill_out(c, sign, "#2E2A25")
    text(c, "HIỆU SÁCH CŨ", 540, 245, "xbold", 54, "#F4C430", align="center")


def plane(c, x, y, s=1.0):
    with Xf(c, x, y, -6, s):
        body = skia.Path(); body.moveTo(-160, 0); body.quadTo(-170, -26, -120, -30); body.lineTo(150, -24); body.quadTo(190, -10, 150, 6); body.lineTo(-120, 10); body.close()
        fill_out(c, body, "#E9E2CF", ow=6)
        wing = skia.Path(); wing.moveTo(-20, -6); wing.lineTo(60, 70); wing.lineTo(90, 70); wing.lineTo(40, -6); wing.close()
        fill_out(c, wing, "#C9C3B4", ow=5)
        tail = skia.Path(); tail.moveTo(-140, -26); tail.lineTo(-170, -90); tail.lineTo(-140, -90); tail.lineTo(-100, -28); tail.close()
        fill_out(c, tail, "#C0392B", ow=5)
        for k in range(6):
            c.drawCircle(-80 + k * 36, -12, 6, paint("#2E4A62"))


def sea_sky(c, t):
    grad_rect(c, skia.Rect.MakeXYWH(-600, -400, W + 1200, 1400), "#7FB3D5", "#D6EAF2")
    for k in range(4):
        cl = paint("white", 220)
        x = (k * 380 - t * 40) % (W + 600) - 300
        c.drawOval(skia.Rect.MakeXYWH(x, 300 + k * 90, 300, 70), cl)
    grad_rect(c, skia.Rect.MakeXYWH(-600, 1000, W + 1200, 1000), "#3F7FA6", "#24506E")
    isl = skia.Path(); isl.moveTo(560, 1040); isl.quadTo(760, 900, 960, 1040); isl.close()
    fill_out(c, isl, "#3E6A3A", ow=5)


# ---------------------------------------------------------------- các cảnh (mốc giây ước lượng)
def sc1_jungle(c, t):
    """0–3,6: Năm 1974, trong rừng núi của một hòn đảo Philippines."""
    z = lerp(1.0, 1.18, ease_in_out(clamp(t / 3.6)))
    c.save(); cam(c, 540, 880, z); jungle(c, t); c.restore()
    blurred(c, 10, lambda: fg_leaves(c, t))
    vignette(c)
    big_title(c, "1974", "PHILIPPINES", 560, prog(t, 0.3, 0.75), size=150, bsize=56)
    # linh vật thò ra với ống nhòm
    pm = prog(t, 1.8, 2.4, back_out)
    mascot(c, 880, lerp(1500, 1260, pm), 0.85, "smile", t=t, arm="binoc", rot=-6)


def sc2_soldier(c, t):
    """3,6–6,6: vẫn còn một sĩ quan Nhật mặc quân phục, mang súng."""
    c.save(); cam(c, 540, 900, 1.2 + 0.02 * (t - 3.6)); jungle(c, t); c.restore()
    pe = prog(t, 3.7, 4.5, ease_out)
    soldier(c, lerp(-200, 470, pe), 1250, 1.2, "alert", t=t, look=0.6, beard=0.0)
    blurred(c, 12, lambda: fg_leaves(c, t))
    vignette(c)
    label_tag(c, "sĩ quan Nhật · quân phục · súng", W / 2, 330, prog(t, 4.6, 4.9), size=34, anchor="center", bg="yellow")


def sc3_believe(c, t):
    """6,6–9,4: và tin rằng Thế chiến thứ hai chưa kết thúc."""
    if t < 8.0:
        c.save(); cam(c, 470, 700, lerp(1.6, 1.9, clamp((t - 6.6) / 1.4))); jungle(c, t)
        soldier(c, 470, 1290, 1.25, "salute", t=t, look=0.0, mouth="shout", beard=0.0)
        c.restore()
        vignette(c, 170)
        pb = prog(t, 6.8, 7.2, back_out)
        if pb > 0:
            with Xf(c, 640, 420, -4, max(0.01, pb)):
                b = rrect_path(-300, -80, 600, 160, 70); fill_out(c, b, "white")
                text(c, "CHIẾN TRANH", 0, -6, "xbold", 54, "ink", align="center")
                text(c, "CHƯA KẾT THÚC!", 0, 52, "xbold", 46, "#C0392B", align="center")
        return
    # phản ứng của linh vật — cận mặt
    grad_rect(c, skia.Rect.MakeWH(W, H), "#3A2418", "#1C110B")
    rings(c, 540, 820, t, 8.0, 9.4, "#F4C430", max_r=900, period=0.35, width=6, a=90)
    sq = 1 + 0.08 * math.sin(clamp((t - 8.0) / 0.25) * math.pi)
    mascot(c, 540, 1500, 2.6, "shock", t=t, arm="up", squash=sq)
    big_title(c, "KHOAN ĐÃ…", "CHIẾN TRANH HẾT TỪ 1945 MÀ??", 470, prog(t, 8.1, 8.4), size=110, bsize=46)


def sc4_bookshop(c, t):
    """9,4–12,0: Ông chỉ chịu buông súng khi chỉ huy cũ, lúc ấy đã thành người bán sách."""
    c.save(); cam(c, 540, 900, lerp(1.25, 1.1, ease_out(clamp((t - 9.4) / 1.0)))); bookshop(c, t)
    bookseller(c, 640, 1290, 1.15, t=t, pose="read", look=-0.5)
    mascot(c, 230, 1020, 0.75, "think", look=(1, 0), t=t)
    c.restore()
    vignette(c, 120)
    label_tag(c, "chỉ huy cũ", W / 2, 330, prog(t, 9.9, 10.2), size=36, anchor="center", bg="white")
    label_tag(c, "nay bán sách", W / 2, 410, prog(t, 10.9, 11.2), size=36, anchor="center", bg="yellow")


def sc5_flight(c, t):
    """12,0–14,4: bay sang đọc lệnh cho ông nghe."""
    if t < 13.2:
        c.save(); cam(c, 540, 900, 1.1); sea_sky(c, t)
        p = clamp((t - 12.0) / 1.2)
        plane(c, lerp(-200, 1300, p), lerp(700, 560, p), 1.4)
        c.restore()
        label_tag(c, "bay sang Philippines", W / 2, 330, prog(t, 12.1, 12.4), size=36, anchor="center", bg="yellow")
        return
    c.save(); cam(c, 540, 900, 1.15); jungle(c, t)
    soldier(c, 330, 1250, 1.05, "attention", t=t, look=0.6, beard=0.0)
    bookseller(c, 760, 1250, 1.05, t=t, pose="read", look=-0.6)
    c.restore()
    blurred(c, 12, lambda: fg_leaves(c, t))
    vignette(c)
    pb = prog(t, 13.4, 13.8, back_out)
    if pb > 0:
        with Xf(c, 720, 400, 3, max(0.01, pb)):
            b = rrect_path(-260, -70, 520, 140, 60); fill_out(c, b, "white")
            text(c, "\"MIỄN NHIỆM VỤ\"", 0, 18, "xbold", 50, "ink", align="center")


def sc6_name(c, t):
    """14,4–17,5: Người lính ấy là thiếu úy Hiroo Onoda."""
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#D4BE86")
    for k in range(14):
        a = k * math.pi / 7 + t * 0.15
        p = skia.Path(); p.moveTo(540, 760)
        p.lineTo(540 + 1600 * math.cos(a), 760 + 1600 * math.sin(a)); p.lineTo(540 + 1600 * math.cos(a + 0.18), 760 + 1600 * math.sin(a + 0.18)); p.close()
        c.drawPath(p, paint("#F4C430", 70))
    pe = prog(t, 14.4, 14.9, back_out)
    soldier(c, 540, 1300, lerp(0.6, 1.15, pe), "stand", t=t, look=0.0, mouth="flat", beard=0.0)
    pn = prog(t, 15.4, 15.8)
    if pn > 0:
        with Xf(c, W / 2, 1110 + (1 - ease_out(pn)) * 60, -2, 1, clamp(pn * 2)):
            b = rrect_path(-400, -80, 800, 170, 18); fill_out(c, b, "#2E2A25")
            text(c, "HIROO ONODA", 0, 10, "xbold", 72, "#F4C430", align="center")
            text(c, "thiếu úy · Lục quân Đế quốc Nhật", 0, 64, "semi", 32, "white", align="center")
    mascot(c, 930, 1300, 0.6, "smile", look=(-1, 0), t=t, arm="point")
    note_label(c, "HOẠT HÌNH MINH HỌA", 60, 330, 1)


TIMELINE = [(0.0, 3.6, sc1_jungle), (3.6, 6.6, sc2_soldier), (6.6, 9.4, sc3_believe), (9.4, 12.0, sc4_bookshop),
            (12.0, 14.4, sc5_flight), (14.4, 17.6, sc6_name)]


def draw_frame(c, t):
    for a, b, fn in TIMELINE:
        if a <= t < b:
            fn(c, t)
            break
