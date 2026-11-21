"""Ảnh đại diện kênh theo chuỗi Bộp và Gầm (bộ khung v2). Không có tên kênh.
  python3 brand/make_avatar_bopgam.py  → brand/avatar_bopgam_<màu>.png (2048×2048)
"""
import math, sys
from pathlib import Path
import skia
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rig import Pose, draw_char, P, OUT, fo, oval

S = 2048
OUTDIR = Path(__file__).resolve().parent


def bg(c, c1, c2, ray, ra=60):
    sh = skia.GradientShader.MakeRadial((S / 2, S * 0.45), S * 0.75, [skia.Color4f.FromColor(skia.Color(*c1)), skia.Color4f.FromColor(skia.Color(*c2))])
    p = skia.Paint(Shader=sh); c.drawRect(skia.Rect.MakeWH(S, S), p)
    for k in range(24):
        if k % 2:
            continue
        a0 = k * 2 * math.pi / 24
        pth = skia.Path(); pth.moveTo(S / 2, S * 0.45)
        pth.lineTo(S / 2 + 3000 * math.cos(a0), S * 0.45 + 3000 * math.sin(a0))
        pth.lineTo(S / 2 + 3000 * math.cos(a0 + 2 * math.pi / 24), S * 0.45 + 3000 * math.sin(a0 + 2 * math.pi / 24)); pth.close()
        c.drawPath(pth, P(ray, ra))


def fire(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    glow = P("#F39C12", 110); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 80))
    c.drawCircle(0, -80, 260, glow)
    for colr, sc in [("#C0392B", 1.0), ("#F39C12", 0.72), ("#F4D03F", 0.45)]:
        fl = skia.Path(); h = 260 * sc
        fl.moveTo(-80 * sc, 0); fl.quadTo(-92 * sc, -h * 0.5, 10 * sc, -h); fl.quadTo(92 * sc, -h * 0.5, 80 * sc, 0); fl.close()
        fo(c, fl, colr, ow=8)
    c.restore()


def spark(c, x, y, r):
    p = skia.Path()
    for j in range(8):
        rr = r if j % 2 == 0 else r * 0.32
        a = -math.pi / 2 + j * math.pi / 4
        (p.moveTo if j == 0 else p.lineTo)(x + rr * math.cos(a), y + rr * math.sin(a))
    p.close(); fo(c, p, "#FFF3B0", ow=10)


def make(name, c1, c2, ray, with_fire=False, ra=60, solo=False):
    surf = skia.Surface(S, S); c = surf.getCanvas()
    bg(c, c1, c2, ray, ra)
    if with_fire:
        fire(c, S / 2, S * 1.02, 2.2)
    t = 0.37  # khung đứng yên, mắt mở
    if solo:
        # Bộp — nhân vật thông minh, cận mặt
        draw_char(c, Pose("bop", S * 0.5, 3100, 5.0, t, face=1, turn=0.15, outfit="coat", collar_up=1.0, eyes="open", look=(0.15, 0.1),
                          brow=0.35, brow_tilt=-0.15, mouth="smile", blush=0.35, head_tilt=-5, hand_r=(-30, -30)))
        spark(c, S * 0.80, S * 0.20, 70)
        spark(c, S * 0.87, S * 0.31, 38)
    else:
        draw_char(c, Pose("gam", S * 0.30, 2330, 3.5, t, face=1, outfit="bigcoat", eyes="squint", brow=0.6, mouth="grin",
                          head_tilt=-6, look=(1, 0)))
        draw_char(c, Pose("bop", S * 0.72, 2400, 3.5, t, face=-1, outfit="coat", collar_up=1.0, eyes="happy", mouth="smile",
                          blush=0.6, head_tilt=6))
    out = OUTDIR / (f"avatar_bop_{name}.png" if solo else f"avatar_bopgam_{name}.png")
    surf.makeImageSnapshot().save(str(out))
    return out


if __name__ == "__main__":
    if "solo" in sys.argv:
        make("cam", (0xFF, 0xD2, 0x7A, 0xFF), (0xF0, 0x8A, 0x4B, 0xFF), "#FFFFFF", solo=True)
        make("xanh", (0xB8, 0xE6, 0xF5, 0xFF), (0x4F, 0xA3, 0xCF, 0xFF), "#FFFFFF", solo=True)
        make("dem", (0x3A, 0x4A, 0x6A, 0xFF), (0x15, 0x20, 0x3A, 0xFF), "#F4C430", ra=22, solo=True)
        sys.exit()
    make("cam", (0xFF, 0xD2, 0x7A, 0xFF), (0xF0, 0x8A, 0x4B, 0xFF), "#FFFFFF")
    make("xanh", (0xB8, 0xE6, 0xF5, 0xFF), (0x4F, 0xA3, 0xCF, 0xFF), "#FFFFFF")
    make("dem", (0x3A, 0x4A, 0x6A, 0xFF), (0x15, 0x20, 0x3A, 0xFF), "#F4C430", with_fire=True, ra=22)
