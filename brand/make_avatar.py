"""Ảnh avatar linh vật kênh Nct official (vuông 2048×2048, an toàn khi bị cắt tròn).
  python3 brand/make_avatar.py  → brand/avatar_*.png, brand/avatar_preview.png
"""
import math, sys
from pathlib import Path
import skia
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "onoda/proto/src"))
from lib import paint, col  # noqa
from toon import mascot  # noqa

S = 2048
BGS = {
    "navy": ("#24476B", "#13263B"),
    "brown": ("#6B4A30", "#3A2618"),
    "cream": ("#F6ECD2", "#E3CF9E"),
}


def render(name, top, bot, expr="smile", look=(0.15, 0.1), arm="down"):
    surf = skia.Surface(S, S)
    c = surf.getCanvas()
    sh = skia.GradientShader.MakeRadial(skia.Point(S / 2, S * 0.42), S * 0.75, [col(top), col(bot)], [0.0, 1.0])
    c.drawRect(skia.Rect.MakeWH(S, S), skia.Paint(Shader=sh))
    # tia sáng nhẹ phía sau
    for k in range(16):
        a = k * math.pi / 8
        p = skia.Path(); p.moveTo(S / 2, S * 0.5)
        p.lineTo(S / 2 + 2000 * math.cos(a), S * 0.5 + 2000 * math.sin(a))
        p.lineTo(S / 2 + 2000 * math.cos(a + 0.2), S * 0.5 + 2000 * math.sin(a + 0.2)); p.close()
        c.drawPath(p, paint("#FFFFFF", 14))
    # bóng dưới chân
    c.drawOval(skia.Rect.MakeXYWH(S / 2 - 440, S * 0.765, 880, 100), paint("#000000", 70))
    # linh vật: thân cao 240 đơn vị → scale để chiếm ~62% chiều cao, nằm gọn trong vòng tròn
    mascot(c, S / 2, S * 0.80, 4.7, expr, look=look, t=1.0, arm=arm)
    img = surf.makeImageSnapshot()
    img.save(str(HERE / f"avatar_{name}.png"))
    return img


imgs = [render(k, *v) for k, v in BGS.items()]
render("navy_wave", *BGS["navy"], expr="smile", look=(-0.2, 0.1), arm="point")
# xem trước: mỗi ảnh cắt tròn như trên YouTube
pv = skia.Surface(3 * 640 + 80, 720)
c = pv.getCanvas(); c.clear(skia.ColorWHITE)
for i, im in enumerate(imgs):
    x = 20 + i * 660
    c.save()
    pth = skia.Path(); pth.addCircle(x + 320, 340, 300)
    c.clipPath(pth, skia.ClipOp.kIntersect, True)
    c.drawImageRect(im, skia.Rect.MakeXYWH(x + 20, 40, 600, 600), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
    c.restore()
pv.makeImageSnapshot().save(str(HERE / "avatar_preview.png"))
print("xong")
