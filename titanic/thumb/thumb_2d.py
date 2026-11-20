"""Thử ảnh thu nhỏ kiểu hoạt hình 2D thông thường (bộ khung chibi tools/rig.py) cho video Titanic."""
import math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "cung" / "src"))
import skia
import rig
from rig import Pose, draw_char, P, fo, oval, OUT
from lib import text

W, H = 1280, 720
rig.STYLES["ir_boy"] = dict(rig.STYLES["npc_man"], skin="#F0C8A8", skin_d="#D8A888", hair="#6A4426", head=(122, 116), torso_w=170, nose="small")
rig.STYLES["ir_girl"] = dict(rig.STYLES["npc_gran"], skin="#F4D2B6", skin_d="#DDB496", hair="#B4552A", head=(112, 120), eye_scale=1.12, brow_w=9)


def grad(c, r, a, b):
    def col(h):
        h = h.lstrip("#"); return skia.ColorSetRGB(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    c.drawRect(r, skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0, r.top()), skia.Point(0, r.bottom())], [col(a), col(b)])))


def ship(c, x, y, s, tilt):
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    hull = skia.Path(); hull.moveTo(-760, -130); hull.lineTo(700, -130); hull.lineTo(780, -160); hull.lineTo(740, 30); hull.quadTo(600, 70, 400, 70)
    hull.lineTo(-640, 70); hull.quadTo(-760, 40, -770, -30); hull.close()
    fo(c, hull, "#16161A", ow=6)
    c.drawRect(skia.Rect.MakeXYWH(-750, 30, 1460, 34), P("#7A2A22"))
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-560, -220, 1060, 90)) or skia.Path(), "#F2EEE4", ow=5)
    for k in range(26):
        g = P("#F8D880", 230); c.drawCircle(-700 + k * 55, -80, 7, g)
        gl = P("#F8D880", 70); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)); c.drawCircle(-700 + k * 55, -80, 16, gl)
    for i in range(4):
        fx = -360 + i * 200
        f = skia.Path(); f.moveTo(fx - 36, -220); f.lineTo(fx - 26, -420); f.lineTo(fx + 36, -420); f.lineTo(fx + 46, -220); f.close()
        fo(c, f, "#D89A3A", ow=5); c.drawRect(skia.Rect.MakeXYWH(fx - 27, -420, 64, 34), P("#1A1A1A"))
    c.restore()


surf = skia.Surface(W, H); c = surf.getCanvas()
grad(c, skia.Rect.MakeWH(W, H), "#070B1C", "#22325A")
for k in range(120):
    x = (k * 173) % W; y = (k * 97) % 420
    c.drawCircle(x, y, 1 + (k % 3) * 0.8, P("#FFFFFF", 150 + (k % 4) * 25))
# tảng băng phát sáng nhẹ
ib = skia.Path(); ib.moveTo(860, 470); ib.lineTo(930, 300); ib.lineTo(1010, 250); ib.lineTo(1080, 120); ib.lineTo(1150, 230); ib.lineTo(1220, 210); ib.lineTo(1300, 470); ib.close()
gl = P("#BFE6FF", 90); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40)); c.drawPath(ib, gl)
fo(c, ib, "#DCEFF8", ow=5)
c.drawLine(1080, 120, 1110, 460, P("#FFFFFF", 120, stroke=8))
ship(c, 760, 470, 0.62, 9)
# mặt biển
c.drawRect(skia.Rect.MakeXYWH(0, 470, W, 260), P("#0C1630"))
for k in range(18):
    y = 490 + (k % 6) * 38; x = (k * 211) % W
    c.drawLine(x, y, x + 120, y, P("#5A7AB0", 90, stroke=4))
# hai anh em ở tiền cảnh
draw_char(c, Pose("ir_boy", 250, 760, 0.95, 0.3, face=1, outfit="modern", shirt="#6A5A48", pants="#3A3A44", shoes="#2A2018", sleeves="long",
                  eyes="wide", look=(1, -0.4), brow=0.9, brow_tilt=-0.6, mouth="o", hand_r=(150, -40), hand_l=(60, 40), sway=0.0))
draw_char(c, Pose("ir_girl", 470, 760, 0.85, 0.3, face=1, outfit="modern", shirt="#4E7A5A", pants="#3E6248", shoes="#2A2018", sleeves="long",
                  eyes="wide", look=(1, -0.3), brow=1.0, brow_tilt=-1.0, mouth="o", hand_l=(-30, -60), hand_r=(-10, -40), sweat=1.0, sway=0.0))
# khăn đỏ của Nora
c.drawLine(420, 514, 520, 514, P(OUT, stroke=28)); c.drawLine(420, 514, 520, 514, P("#C8402E", stroke=20))
# chữ
text(c, "BẠN CÓ", 980, 560, "xbold", 74, "#FFFFFF", align="center", stroke=10, stroke_color="#0A0A10")
text(c, "SỐNG SÓT?", 980, 650, "xbold", 92, "#F4C430", align="center", stroke=12, stroke_color="#0A0A10")
surf.makeImageSnapshot().save(str(Path(__file__).with_name("thumb_2d_thu.png")))
