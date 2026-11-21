"""3 mẫu avatar lượt 2: ấn triện, đồng hồ cát, huy hiệu điện ảnh. 2048×2048.
  python3 brand/su_thi/make_avatar2.py
"""
import math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cung" / "src"))
import skia
import shapefile
from lib import text

S = 2048
OUT = Path(__file__).resolve().parent
INK = "#14100C"


def P(col, a=255, stroke=None, blur=0):
    h = col.lstrip("#")
    p = skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke); p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


def col4(h):
    h = h.lstrip("#"); return skia.Color4f.FromColor(skia.ColorSetRGB(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))


def radial(c, a, b, cy=0.45, r=0.72):
    c.drawRect(skia.Rect.MakeWH(S, S), skia.Paint(Shader=skia.GradientShader.MakeRadial((S / 2, S * cy), S * r, [col4(a), col4(b)])))


def linear(c, rect, a, b):
    c.drawRect(rect, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, rect.top()), skia.Point(0, rect.bottom())], [col4(a), col4(b)])))


def world_path(cx, cy, w, h):
    sf = shapefile.Reader(str(ROOT / "midway_v2" / "assets" / "map" / "naturalearth_lowres.shp"))
    p = skia.Path()
    for shp in sf.shapes():
        pts = shp.points; parts = list(shp.parts) + [len(pts)]
        for i in range(len(parts) - 1):
            seg = pts[parts[i]:parts[i + 1]]
            for j, (lon, lat) in enumerate(seg):
                x = cx + lon / 180 * w / 2; y = cy - lat / 90 * h / 2
                (p.moveTo if j == 0 else p.lineTo)(x, y)
            p.close()
    return p


def paper(c):
    radial(c, "#F2E6C8", "#C8AE7E", 0.5, 0.75)
    for k in range(400):     # hạt giấy
        x = (k * 7919) % S; y = (k * 104729) % S
        c.drawCircle(x, y, 2 + k % 4, P("#8A6A3A", 25))


def a4_seal(c):
    """Ấn triện đỏ — dấu son 'SỬ THI' trên giấy cổ, có vệt mực quanh."""
    paper(c)
    ring = skia.Path(); ring.addCircle(S / 2, S / 2, 820)
    c.drawPath(ring, P("#2A1A10", 200, stroke=60))
    c.drawPath(ring, P("#2A1A10", 60, stroke=110, blur=20))
    c.save(); c.translate(S / 2, S / 2); c.rotate(-4)
    sq = skia.Path(); sq.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-560, -560, 1120, 1120), 70, 70))
    c.drawPath(sq, P("#B8261C"))
    for k in range(60):      # vân mực dấu không đều
        x = -540 + (k * 389) % 1080; y = -540 + (k * 677) % 1080
        c.drawCircle(x, y, 10 + k % 18, P("#F2E6C8", 70))
    c.drawRoundRect(skia.Rect.MakeXYWH(-500, -500, 1000, 1000), 40, 40, P("#F2E6C8", stroke=26))
    text(c, "SỬ", 0, -40, "xbold", 430, "#F2E6C8", align="center")
    text(c, "THI", 0, 400, "xbold", 330, "#F2E6C8", align="center")
    c.restore()


def a5_hourglass(c):
    """Đồng hồ cát vàng: cát rơi xuống thành bản đồ thế giới — thời gian và lịch sử. Không chữ."""
    radial(c, "#1C2A44", "#05080F")
    c.drawCircle(S / 2, S / 2, 860, P("#D8B04A", stroke=26))
    c.drawCircle(S / 2, S / 2, 800, P("#D8B04A", 120, stroke=8))
    for k in range(48):
        a = k * 2 * math.pi / 48
        r0, r1 = (860, 900) if k % 4 else (840, 940)
        c.drawLine(S / 2 + r0 * math.cos(a), S / 2 + r0 * math.sin(a), S / 2 + r1 * math.cos(a), S / 2 + r1 * math.sin(a), P("#D8B04A", stroke=10))
    cx, cy = S / 2, S / 2
    glass = skia.Path(); glass.moveTo(cx - 380, cy - 620); glass.lineTo(cx + 380, cy - 620)
    glass.cubicTo(cx + 380, cy - 220, cx + 60, cy - 120, cx + 60, cy); glass.cubicTo(cx + 60, cy + 120, cx + 380, cy + 220, cx + 380, cy + 620)
    glass.lineTo(cx - 380, cy + 620); glass.cubicTo(cx - 380, cy + 220, cx - 60, cy + 120, cx - 60, cy); glass.cubicTo(cx - 60, cy - 120, cx - 380, cy - 220, cx - 380, cy - 620)
    glass.close()
    c.drawPath(glass, P("#9FC8E8", 40))
    c.save(); c.clipPath(glass, skia.ClipOp.kIntersect, True)
    top = skia.Path(); top.moveTo(cx - 300, cy - 330); top.quadTo(cx, cy - 290, cx + 300, cy - 330); top.lineTo(cx + 40, cy - 30); top.lineTo(cx - 40, cy - 30); top.close()
    c.drawPath(top, P("#E8C86A"))
    c.drawLine(cx, cy - 40, cx, cy + 420, P("#E8C86A", stroke=12))
    linear(c, skia.Rect.MakeXYWH(cx - 400, cy + 200, 800, 440), "#E8C86A", "#B88A30")
    wp = world_path(cx, cy + 410, 720, 360)
    c.drawPath(wp, P("#6A4A1A", 220))
    c.restore()
    c.drawPath(glass, P("#F2E6C8", stroke=14))
    for y, sgn in ((cy - 640, 1), (cy + 640, -1)):
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - 470, y - 40, 940, 80), 30, 30, P("#D8B04A"))
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - 470, y - 40, 940, 80), 30, 30, P(INK, stroke=10))
    for sx in (-430, 430):
        c.drawLine(cx + sx, cy - 600, cx + sx, cy + 600, P("#D8B04A", stroke=34))
        c.drawLine(cx + sx, cy - 600, cx + sx, cy + 600, P(INK, stroke=6))


def a6_badge(c):
    """Huy hiệu điện ảnh: hoàng hôn, bóng người lính cắm cờ trên đồi, dải băng chữ 'SỬ THI'."""
    c.drawRect(skia.Rect.MakeWH(S, S), P("#120C08"))
    disc = skia.Path(); disc.addCircle(S / 2, S / 2, 900)
    c.save(); c.clipPath(disc, skia.ClipOp.kIntersect, True)
    linear(c, skia.Rect.MakeWH(S, S), "#3A1E3A", "#F09040")
    c.drawCircle(S / 2, S * 0.56, 330, P("#FFD890"))
    c.drawCircle(S / 2, S * 0.56, 460, P("#FFD890", 70, blur=60))
    for k in range(5):
        c.drawLine(0, S * 0.5 + k * 34, S, S * 0.5 + k * 34, P("#F8C070", 60, stroke=6))
    hill = skia.Path(); hill.moveTo(0, S); hill.lineTo(0, S * 0.74); hill.quadTo(S * 0.45, S * 0.58, S, S * 0.72); hill.lineTo(S, S); hill.close()
    c.drawPath(hill, P("#120C08"))
    # bóng người lính cầm cờ
    c.save(); c.translate(S * 0.52, S * 0.62)
    c.drawCircle(0, -330, 46, P("#120C08"))
    body = skia.Path(); body.moveTo(-50, -280); body.lineTo(50, -280); body.lineTo(70, -60); body.lineTo(-60, -60); body.close(); c.drawPath(body, P("#120C08"))
    c.drawLine(-30, -70, -70, 40, P("#120C08", stroke=36)); c.drawLine(30, -70, 60, 40, P("#120C08", stroke=36))
    c.drawLine(40, -250, 150, -360, P("#120C08", stroke=30))
    c.drawLine(150, 60, 150, -620, P("#120C08", stroke=18))
    flag = skia.Path(); flag.moveTo(150, -620); flag.quadTo(290, -660, 420, -600); flag.quadTo(300, -560, 420, -470); flag.quadTo(290, -520, 150, -480); flag.close()
    c.drawPath(flag, P("#120C08"))
    c.restore()
    c.restore()
    c.drawPath(disc, P("#D8B04A", stroke=34)); c.drawCircle(S / 2, S / 2, 860, P("#D8B04A", 140, stroke=8))
    rib = skia.Path(); rib.moveTo(S * 0.18, S * 0.78); rib.quadTo(S / 2, S * 0.86, S * 0.82, S * 0.78); rib.lineTo(S * 0.82, S * 0.9)
    rib.quadTo(S / 2, S * 0.98, S * 0.18, S * 0.9); rib.close()
    c.drawPath(rib, P("#8A1E16")); c.drawPath(rib, P("#D8B04A", stroke=14))
    text(c, "SỬ THI", S / 2, S * 0.905, "xbold", 180, "#F2E6C8", align="center", stroke=14, stroke_color=INK)


def save(name, draw):
    surf = skia.Surface(S, S); c = surf.getCanvas()
    draw(c)
    surf.makeImageSnapshot().save(str(OUT / f"avatar_{name}.png"))


items = [("4_an_trien", a4_seal), ("5_dong_ho_cat", a5_hourglass), ("6_huy_hieu", a6_badge)]
for n, f in items:
    save(n, f)

from PIL import Image, ImageDraw
sh = Image.new("RGB", (3 * 560, 860), "white")
for i, (n, _) in enumerate(items):
    im = Image.open(OUT / f"avatar_{n}.png").convert("RGB")
    sh.paste(im.resize((512, 512)), (i * 560 + 24, 10))
    m = Image.new("L", (256, 256), 0); ImageDraw.Draw(m).ellipse((0, 0, 255, 255), fill=255)
    sh.paste(im.resize((256, 256)), (i * 560 + 60, 560), m)
    m2 = Image.new("L", (72, 72), 0); ImageDraw.Draw(m2).ellipse((0, 0, 71, 71), fill=255)
    sh.paste(im.resize((72, 72)), (i * 560 + 380, 740), m2)
sh.save(OUT / "xem_truoc_2.png")
