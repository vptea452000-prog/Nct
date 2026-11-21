"""Ảnh bìa kênh Nct official 2560×1440. Chữ và linh vật nằm trong vùng an toàn 1546×423 ở giữa
(vùng hiển thị trên mọi thiết bị theo hướng dẫn YouTube).
  python3 brand/make_banner.py → brand/banner_navy.png, brand/banner_preview.png
"""
import math, sys
from pathlib import Path
import skia
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "onoda/proto/src"))
from lib import paint, col, text, tw  # noqa
from toon import mascot, OUT, fill_out, rrect_path  # noqa

BW, BH = 2560, 1440
SAFE = skia.Rect.MakeXYWH((BW - 1546) / 2, (BH - 423) / 2, 1546, 423)


def doodles(c):
    """Hoạ tiết mờ: bản đồ, la bàn, sách, phong thư, tên lửa, máy bay — gợi chủ đề lịch sử."""
    ink = paint("#FFFFFF", 26, stroke=6)
    fill = paint("#FFFFFF", 18)
    items = [(220, 260, "compass"), (420, 1180, "book"), (2330, 300, "letter"), (2200, 1150, "plane"),
             (90, 720, "globe"), (2470, 720, "hourglass"), (900, 180, "letter"), (1700, 1290, "book"), (1600, 160, "compass"),
             (700, 1300, "plane")]
    for x, y, kind in items:
        c.save(); c.translate(x, y)
        if kind == "compass":
            c.drawCircle(0, 0, 80, ink); c.drawCircle(0, 0, 60, ink)
            p = skia.Path(); p.moveTo(0, -70); p.lineTo(16, 0); p.lineTo(0, 70); p.lineTo(-16, 0); p.close(); c.drawPath(p, fill)
        elif kind == "book":
            c.rotate(-8); c.drawRect(skia.Rect.MakeXYWH(-90, -60, 180, 120), ink); c.drawLine(0, -60, 0, 60, ink)
            for k in range(3):
                c.drawLine(-70, -30 + k * 25, -15, -30 + k * 25, ink); c.drawLine(15, -30 + k * 25, 70, -30 + k * 25, ink)
        elif kind == "letter":
            c.rotate(10); c.drawRect(skia.Rect.MakeXYWH(-90, -55, 180, 110), ink)
            c.drawLine(-90, -55, 0, 10, ink); c.drawLine(90, -55, 0, 10, ink)
        elif kind == "plane":
            c.rotate(-15)
            p = skia.Path(); p.moveTo(-100, 0); p.lineTo(100, -6); p.lineTo(110, 0); p.lineTo(100, 6); p.close(); c.drawPath(p, fill)
            c.drawLine(0, 0, 40, 60, ink); c.drawLine(0, 0, 40, -60, ink)
        elif kind == "globe":
            c.drawCircle(0, 0, 90, ink); c.drawOval(skia.Rect.MakeXYWH(-40, -90, 80, 180), ink); c.drawLine(-90, 0, 90, 0, ink)
        elif kind == "hourglass":
            p = skia.Path(); p.moveTo(-50, -80); p.lineTo(50, -80); p.lineTo(-50, 80); p.lineTo(50, 80); p.close(); c.drawPath(p, ink)
        c.restore()


def render(name, top, bot):
    surf = skia.Surface(BW, BH)
    c = surf.getCanvas()
    sh = skia.GradientShader.MakeRadial(skia.Point(BW * 0.62, BH / 2), BW * 0.7, [col(top), col(bot)], [0.0, 1.0])
    c.drawRect(skia.Rect.MakeWH(BW, BH), skia.Paint(Shader=sh))
    cx, cy = SAFE.right() - 260, SAFE.centerY()
    for k in range(24):
        a = k * math.pi / 12
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + 2600 * math.cos(a), cy + 2600 * math.sin(a)); p.lineTo(cx + 2600 * math.cos(a + 0.13), cy + 2600 * math.sin(a + 0.13)); p.close()
        c.drawPath(p, paint("#FFFFFF", 12))
    doodles(c)
    # linh vật bên phải vùng an toàn
    c.drawOval(skia.Rect.MakeXYWH(cx - 175, SAFE.bottom() - 56, 310, 36), paint("#000000", 70))
    mascot(c, cx - 20, SAFE.bottom() - 30, 1.4, "smile", look=(-0.6, 0.1), t=1.0, arm="point")
    # chữ bên trái
    x0 = SAFE.left() + 20
    text(c, "Lịch sử có thật", x0, SAFE.top() + 150, "xbold", 132, "#F4C430", stroke=10, stroke_color="#1A120D")
    text(c, "Mỗi tập một câu hỏi", x0 + 4, SAFE.top() + 255, "bold", 76, "#FFFFFF", stroke=7, stroke_color="#1A120D")
    tag = "Đăng ký"
    tw_ = tw(tag, "xbold", 44) + 60
    pill = rrect_path(x0 + 6, SAFE.top() + 300, tw_ + 20, 88, 44)
    fill_out(c, pill, "#C0392B", ow=6)
    text(c, tag, x0 + 46, SAFE.top() + 360, "xbold", 50, "#FFFFFF")
    img = surf.makeImageSnapshot()
    img.save(str(HERE / f"banner_{name}.png"))
    return img


img = render("navy", "#2A527A", "#13263B")
render("brown", "#7A5538", "#3A2618")
# xem trước: khung đầy đủ (TV) + đường viền vùng hiển thị trên máy tính và vùng an toàn (điện thoại)
pv = skia.Surface(1280, 720)
c = pv.getCanvas()
c.drawImageRect(img, skia.Rect.MakeWH(1280, 720), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
s = 0.5
c.drawRect(skia.Rect.MakeXYWH(0, (BH - 423) / 2 * s, 1280, 423 * s), paint("#FFFFFF", 200, stroke=3, cap=False))
c.drawRect(skia.Rect.MakeXYWH(SAFE.left() * s, SAFE.top() * s, SAFE.width() * s, SAFE.height() * s), paint("#F4C430", 255, stroke=3, cap=False))
pv.makeImageSnapshot().save(str(HERE / "banner_preview.png"))
print("xong")
