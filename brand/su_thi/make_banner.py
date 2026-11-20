"""Ảnh bìa kênh 2560×1440, vùng an toàn giữa 1546×423 (hiện trên mọi thiết bị).
Hai bản: theo mẫu đồng hồ cát (xanh đêm – vàng) và theo mẫu ấn triện (giấy cổ – son đỏ).
  python3 brand/su_thi/make_banner.py
"""
import math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cung" / "src")); sys.path.insert(0, str(Path(__file__).resolve().parent))
import skia
from lib import text, tw
from make_avatar2 import P, col4, world_path, INK

W, H = 2560, 1440
SAFE = skia.Rect.MakeXYWH((W - 1546) / 2, (H - 423) / 2, 1546, 423)
OUT = Path(__file__).resolve().parent


def linear(c, rect, a, b, horiz=False):
    pts = [skia.Point(rect.left(), 0), skia.Point(rect.right(), 0)] if horiz else [skia.Point(0, rect.top()), skia.Point(0, rect.bottom())]
    c.drawRect(rect, skia.Paint(Shader=skia.GradientShader.MakeLinear(pts, [col4(a), col4(b)])))


def mini_hourglass(c, cx, cy, s):
    c.save(); c.translate(cx, cy); c.scale(s, s)
    g = skia.Path(); g.moveTo(-380, -620); g.lineTo(380, -620); g.cubicTo(380, -220, 60, -120, 60, 0); g.cubicTo(60, 120, 380, 220, 380, 620)
    g.lineTo(-380, 620); g.cubicTo(-380, 220, -60, 120, -60, 0); g.cubicTo(-60, -120, -380, -220, -380, -620); g.close()
    c.drawPath(g, P("#9FC8E8", 40))
    c.save(); c.clipPath(g, skia.ClipOp.kIntersect, True)
    top = skia.Path(); top.moveTo(-300, -330); top.quadTo(0, -290, 300, -330); top.lineTo(40, -30); top.lineTo(-40, -30); top.close()
    c.drawPath(top, P("#E8C86A")); c.drawLine(0, -40, 0, 420, P("#E8C86A", stroke=12))
    linear(c, skia.Rect.MakeXYWH(-400, 200, 800, 440), "#E8C86A", "#B88A30")
    c.drawPath(world_path(0, 410, 720, 360), P("#6A4A1A", 220))
    c.restore()
    c.drawPath(g, P("#F2E6C8", stroke=14))
    for y in (-640, 640):
        c.drawRoundRect(skia.Rect.MakeXYWH(-470, y - 40, 940, 80), 30, 30, P("#D8B04A"))
    for sx in (-430, 430):
        c.drawLine(sx, -600, sx, 600, P("#D8B04A", stroke=34))
    c.restore()


def banner_hourglass():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    linear(c, skia.Rect.MakeWH(W, H), "#0A1222", "#1C2E4C")
    # bản đồ thế giới mờ làm nền, lưới kinh vĩ tuyến
    c.drawPath(world_path(W / 2, H / 2 + 40, 2600, 1300), P("#2E4A72", 130))
    for k in range(-6, 7):
        c.drawLine(W / 2 + k * 216, 0, W / 2 + k * 216, H, P("#3A5A86", 40, stroke=3))
        c.drawLine(0, H / 2 + k * 108, W, H / 2 + k * 108, P("#3A5A86", 40, stroke=3))
    # đường hành trình chấm vàng ngang qua bản đồ
    pth = skia.Path(); pth.moveTo(160, 1180); pth.cubicTo(700, 1300, 1300, 1060, 1900, 1120); pth.cubicTo(2200, 1150, 2350, 1040, 2420, 980)
    pe = P("#D8B04A", 150, stroke=8); pe.setPathEffect(skia.DashPathEffect.Make([30, 22], 0)); c.drawPath(pth, pe)
    for x, y in ((160, 1180), (1900, 1120), (2420, 980)):
        c.drawCircle(x, y, 16, P("#D8B04A"))
    # vệt sáng giữa
    c.drawOval(skia.Rect.MakeXYWH(W / 2 - 900, H / 2 - 260, 1800, 520), P("#F2D28A", 40, blur=120))
    mini_hourglass(c, SAFE.left() + 170, H / 2, 0.27)
    text(c, "SỬ THI", SAFE.left() + 360, H / 2 + 40, "xbold", 190, "#F2E6C8", stroke=14, stroke_color=INK)
    text(c, "Những câu chuyện làm nên lịch sử", SAFE.left() + 370, H / 2 + 140, "semi", 62, "#D8B04A")
    px = SAFE.left() + 380 + tw("SỬ THI", "xbold", 190) + 60
    c.drawRoundRect(skia.Rect.MakeXYWH(px, H / 2 - 100, 270, 96), 48, 48, P("#C8402E"))
    text(c, "Đăng ký", px + 135, H / 2 - 33, "xbold", 50, "#FFFFFF", align="center")
    return surf


def banner_seal():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, H / 2), W * 0.6, [col4("#F2E6C8"), col4("#C8AE7E")])))
    for k in range(700):
        c.drawCircle((k * 7919) % W, (k * 104729) % H, 2 + k % 4, P("#8A6A3A", 22))
    c.drawPath(world_path(W / 2, H / 2 + 40, 2600, 1300), P("#8A6A3A", 50))
    # nét bút lông quét ngang
    br = skia.Path(); br.moveTo(SAFE.left() - 80, H / 2 + 10); br.cubicTo(W / 2 - 300, H / 2 - 60, W / 2 + 400, H / 2 + 70, SAFE.right() + 80, H / 2 - 10)
    c.drawPath(br, P("#2A1A10", 40, stroke=220, blur=10))
    c.save(); c.translate(SAFE.left() + 190, H / 2); c.rotate(-4)
    c.drawRoundRect(skia.Rect.MakeXYWH(-170, -170, 340, 340), 22, 22, P("#B8261C"))
    for k in range(25):
        c.drawCircle(-160 + (k * 389) % 320, -160 + (k * 677) % 320, 4 + k % 8, P("#F2E6C8", 70))
    c.drawRoundRect(skia.Rect.MakeXYWH(-150, -150, 300, 300), 14, 14, P("#F2E6C8", stroke=9))
    text(c, "SỬ", 0, -14, "xbold", 130, "#F2E6C8", align="center"); text(c, "THI", 0, 118, "xbold", 100, "#F2E6C8", align="center")
    c.restore()
    text(c, "Lịch sử thế giới,", SAFE.left() + 420, H / 2 - 20, "xbold", 84, "#2A1A10")
    text(c, "kể bằng những câu chuyện", SAFE.left() + 420, H / 2 + 80, "semi", 56, "#7A1E16")
    px = SAFE.left() + 420 + max(tw("Lịch sử thế giới,", "xbold", 84), tw("kể bằng những câu chuyện", "semi", 56)) + 40
    c.drawRoundRect(skia.Rect.MakeXYWH(px, H / 2 - 48, 250, 96), 48, 48, P("#B8261C"))
    text(c, "Đăng ký", px + 125, H / 2 + 19, "xbold", 48, "#F2E6C8", align="center")
    return surf


for name, fn in (("banner_dong_ho_cat", banner_hourglass), ("banner_an_trien", banner_seal)):
    s = fn(); s.makeImageSnapshot().save(str(OUT / f"{name}.png"))

# xem trước: toàn ảnh (TV) + khung an toàn (điện thoại)
from PIL import Image, ImageDraw
prev = Image.new("RGB", (1280 * 2 + 40, 720 + 260), "white")
for i, name in enumerate(("banner_dong_ho_cat", "banner_an_trien")):
    im = Image.open(OUT / f"{name}.png").convert("RGB")
    full = im.resize((1280, 720)); d = ImageDraw.Draw(full)
    d.rectangle([SAFE.left() / 2, SAFE.top() / 2, SAFE.right() / 2, SAFE.bottom() / 2], outline=(255, 80, 80), width=3)
    prev.paste(full, (i * 1320, 0))
    phone = im.crop((int(SAFE.left()), int(SAFE.top()), int(SAFE.right()), int(SAFE.bottom()))).resize((773, 212))
    prev.paste(phone, (i * 1320 + 250, 740))
prev.save(OUT / "xem_truoc_banner.png")
