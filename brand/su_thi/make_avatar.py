"""Mẫu avatar cho kênh lịch sử kể chuyện hùng tráng (thiết kế riêng). 2048×2048, an toàn khi cắt tròn.
  python3 brand/su_thi/make_avatar.py
"""
import math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cung" / "src"))
import skia
from lib import text

S = 2048
OUT = Path(__file__).resolve().parent
INK = "#14100C"


def P(col, a=255, stroke=None):
    h = col.lstrip("#")
    p = skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke); p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def radial(c, a, b):
    def col(h):
        h = h.lstrip("#"); return skia.Color4f.FromColor(skia.ColorSetRGB(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    c.drawRect(skia.Rect.MakeWH(S, S), skia.Paint(Shader=skia.GradientShader.MakeRadial((S / 2, S * 0.45), S * 0.72, [col(a), col(b)])))


def laurel(c, cx, cy, r, col, side):
    stem = skia.Path(); stem.addArc(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), 90 + side * 10, side * 150)
    c.drawPath(stem, P(col, stroke=26))
    for k in range(9):
        a = math.radians(100 + side * (20 + k * 16)) if side > 0 else math.radians(80 - (20 + k * 16))
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        c.save(); c.translate(x, y); c.rotate(math.degrees(a) + (60 if side > 0 else 120))
        lf = skia.Path(); lf.moveTo(0, 0); lf.quadTo(55, -40, 120, 0); lf.quadTo(55, 40, 0, 0); lf.close()
        c.drawPath(lf, P(col))
        c.restore()


def helmet(c, cx, cy, s, col, crest):
    c.save(); c.translate(cx, cy); c.scale(s, s)
    cr = skia.Path(); cr.moveTo(-60, -330); cr.quadTo(0, -470, 260, -420); cr.quadTo(160, -360, 60, -300); cr.close()
    c.drawPath(cr, P(crest))
    h = skia.Path(); h.moveTo(-230, 160); h.lineTo(-240, -60); h.quadTo(-230, -330, 0, -340); h.quadTo(230, -330, 240, -60); h.lineTo(230, 160)
    h.lineTo(110, 160); h.lineTo(100, 40); h.lineTo(40, 30); h.lineTo(30, 240); h.lineTo(-30, 240); h.lineTo(-40, 30); h.lineTo(-100, 40)
    h.lineTo(-110, 160); h.close()
    c.drawPath(h, P(col))
    c.drawPath(h, P(INK, stroke=14))
    c.drawLine(-200, -80, 200, -80, P(INK, 120, stroke=10))
    c.restore()


def compass_map(c, cx, cy, r, col):
    c.drawCircle(cx, cy, r, P(col, stroke=30)); c.drawCircle(cx, cy, r * 0.82, P(col, stroke=10))
    for k in range(4):
        a = k * math.pi / 2
        p = skia.Path(); p.moveTo(cx + r * 1.05 * math.cos(a), cy + r * 1.05 * math.sin(a))
        p.lineTo(cx + 70 * math.cos(a + math.pi / 2), cy + 70 * math.sin(a + math.pi / 2))
        p.lineTo(cx + 70 * math.cos(a - math.pi / 2), cy + 70 * math.sin(a - math.pi / 2)); p.close()
        c.drawPath(p, P(col if k % 2 else "#C8402E"))
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        c.drawLine(cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a), cx + r * 0.8 * math.cos(a), cy + r * 0.8 * math.sin(a), P(col, stroke=14))


def swords(c, cx, cy, s, col):
    for side in (-1, 1):
        c.save(); c.translate(cx, cy); c.rotate(side * 38); c.scale(s, s)
        bl = skia.Path(); bl.moveTo(-30, 260); bl.lineTo(-30, -520); bl.lineTo(0, -600); bl.lineTo(30, -520); bl.lineTo(30, 260); bl.close()
        c.drawPath(bl, P("#D8D2C4")); c.drawPath(bl, P(INK, stroke=10))
        c.drawRect(skia.Rect.MakeXYWH(-130, 250, 260, 44), P(col)); c.drawRect(skia.Rect.MakeXYWH(-26, 294, 52, 170), P("#5A3A22"))
        c.drawCircle(0, 490, 34, P(col))
        c.restore()


def save(name, draw):
    surf = skia.Surface(S, S); c = surf.getCanvas()
    draw(c)
    surf.makeImageSnapshot().save(str(OUT / f"avatar_{name}.png"))


def a1(c):   # mũ chiến binh + vòng nguyệt quế, nền đỏ thẫm
    radial(c, "#8A2A1E", "#2A0A08")
    laurel(c, S / 2, S * 0.5, 640, "#D8B04A", -1); laurel(c, S / 2, S * 0.5, 640, "#D8B04A", 1)
    helmet(c, S / 2, S * 0.5, 1.7, "#D8B04A", "#C8402E")
    text(c, "SỬ THI", S / 2, S * 0.86, "xbold", 210, "#F2E6C8", align="center", stroke=18, stroke_color=INK)


def a2(c):   # la bàn + bản đồ cổ, nền xanh đêm
    radial(c, "#1E3A5A", "#08121E")
    for k in range(12):
        y = 300 + k * 130
        c.drawLine(200, y, S - 200, y, P("#3A5A7A", 70, stroke=4))
        c.drawLine(300 + k * 130, 200, 300 + k * 130, S - 200, P("#3A5A7A", 70, stroke=4))
    compass_map(c, S / 2, S * 0.46, 560, "#E8D29A")
    text(c, "BẢN ĐỒ SỬ", S / 2, S * 0.86, "xbold", 190, "#F2E6C8", align="center", stroke=16, stroke_color=INK)


def a3(c):   # hai thanh kiếm bắt chéo + khiên, nền giấy cổ
    radial(c, "#E8D6A8", "#A8865A")
    shield = skia.Path(); shield.moveTo(S / 2, S * 0.2); shield.quadTo(S * 0.72, S * 0.24, S * 0.74, S * 0.3); shield.quadTo(S * 0.74, S * 0.58, S / 2, S * 0.74)
    shield.quadTo(S * 0.26, S * 0.58, S * 0.26, S * 0.3); shield.quadTo(S * 0.28, S * 0.24, S / 2, S * 0.2); shield.close()
    c.drawPath(shield, P("#7A1E16")); c.drawPath(shield, P(INK, stroke=24))
    swords(c, S / 2, S * 0.47, 1.25, "#D8B04A")
    text(c, "CHIẾN SỬ", S / 2, S * 0.88, "xbold", 200, "#2A1A10", align="center", stroke=0, stroke_color=INK)


for n, f in (("1_su_thi", a1), ("2_ban_do_su", a2), ("3_chien_su", a3)):
    save(n, f)

# xem trước: vuông + cắt tròn cỡ vừa và cỡ nhỏ
from PIL import Image, ImageDraw
names = ["avatar_1_su_thi.png", "avatar_2_ban_do_su.png", "avatar_3_chien_su.png"]
sh = Image.new("RGB", (3 * 560, 860), "white")
for i, n in enumerate(names):
    im = Image.open(OUT / n).convert("RGB")
    sh.paste(im.resize((512, 512)), (i * 560 + 24, 10))
    m = Image.new("L", (256, 256), 0); ImageDraw.Draw(m).ellipse((0, 0, 255, 255), fill=255)
    sh.paste(im.resize((256, 256)), (i * 560 + 60, 560), m)
    m2 = Image.new("L", (72, 72), 0); ImageDraw.Draw(m2).ellipse((0, 0, 71, 71), fill=255)
    sh.paste(im.resize((72, 72)), (i * 560 + 380, 740), m2)
sh.save(OUT / "xem_truoc.png")
