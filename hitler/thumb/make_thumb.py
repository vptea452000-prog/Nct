"""Thumbnail Hitler — 1280x720, 3 phương án (ảnh mờ dần vào nền tối, không dùng biểu tượng chữ thập ngoặc)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
import numpy as np
W, H = 1280, 720
SB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
IB = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
CREAM = (250, 240, 218); GOLD = (230, 190, 105); RED = (200, 40, 32)


def cover(im, w, h, cx=0.5, cy=0.5):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = int((im.width - w) * cx); y = int((im.height - h) * cy); return im.crop((x, y, x + w, y + h))


def bw(im, warm=0.25, contrast=1.25, bright=1.0):
    g = ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(contrast)
    a = np.asarray(g).astype(np.float32) / 255 * bright
    rgb = np.stack([a * (1 + 0.08 * warm), a * (1 - 0.02 * warm), a * (1 - 0.18 * warm)], -1)
    return Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))


def hfade(w, h, x0, x1, invert=False):
    """mặt nạ ngang: 0 trước x0, 1 sau x1."""
    xx = np.clip((np.arange(w) - x0) / max(1, x1 - x0), 0, 1); xx = xx * xx * (3 - 2 * xx)
    if invert: xx = 1 - xx
    return Image.fromarray((np.tile(xx, (h, 1)) * 255).astype(np.uint8))


def vignette(im, k=0.8):
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    v = np.clip(1 - k * np.clip(d - 0.5, 0, 1) ** 1.5, 0, 1)[..., None]
    return Image.fromarray((np.asarray(im.convert("RGB")).astype(np.float32) * v).astype(np.uint8)).convert("RGBA")


def glow_text(base, xy, text, font, fill, r=14, anchor="la"):
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, text, font=font, fill=(0, 0, 0, 255), anchor=anchor, stroke_width=8, stroke_fill=(0, 0, 0, 255))
    base.alpha_composite(lay.filter(ImageFilter.GaussianBlur(r)))
    ImageDraw.Draw(base).text(xy, text, font=font, fill=fill, anchor=anchor)


def grain(im, k=10, seed=3):
    n = (np.random.default_rng(seed).normal(0, k, (H, W, 1))).astype(np.float32)
    return Image.fromarray(np.clip(np.asarray(im.convert("RGB")).astype(np.float32) + n, 0, 255).astype(np.uint8)).convert("RGBA")


def v1():   # Tranh màu nước (trái) ↔ chân dung (phải): "TỪ HỌA SĨ… ĐẾN KẺ ĐỘC TÀI"
    paint = cover(Image.open("assets/k/K03b.jpg").convert("RGB"), W, H, 0.45, 0.5)
    paint = ImageEnhance.Brightness(ImageEnhance.Color(paint).enhance(0.85)).enhance(0.8)
    port = bw(cover(Image.open("assets/k/K04.jpg").convert("RGB"), 700, H, 0.5, 0.22), warm=0.3, contrast=1.35)
    bg = paint.convert("RGBA")
    dark = Image.new("RGBA", (W, H), (10, 8, 7, 255)); dark.putalpha(hfade(W, H, 380, 760))
    bg.alpha_composite(dark)
    p = port.convert("RGBA"); p.putalpha(hfade(700, H, 0, 260))
    bg.alpha_composite(p, (W - 700, 0))
    bg = vignette(bg, 0.7)
    glow_text(bg, (52, 120), "TỪ HỌA SĨ", ImageFont.truetype(IB, 92), CREAM)
    glow_text(bg, (52, 222), "BỊ TỪ CHỐI", ImageFont.truetype(IB, 92), CREAM)
    glow_text(bg, (56, 360), "ĐẾN KẺ ĐẨY", ImageFont.truetype(IB, 70), GOLD)
    glow_text(bg, (56, 440), "THẾ GIỚI VÀO", ImageFont.truetype(IB, 70), GOLD)
    glow_text(bg, (56, 520), "CHIẾN TRANH", ImageFont.truetype(IB, 70), RED)
    return grain(bg)


def v2():   # Ảnh diễn thuyết, nền đen-đỏ: "70.000.000 NGƯỜI CHẾT"
    port = bw(Image.open("assets/k/K22a.jpg").convert("RGB"), warm=0.2, contrast=1.3)
    port = cover(port, 560, H, 0.5, 0.15)
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W * 0.25) / W) ** 2 + ((yy - H * 0.5) / H) ** 2)
    arr = np.array([8, 5, 5]) + np.clip(1 - d * 1.7, 0, 1)[..., None] * np.array([110, 18, 14])
    bg = Image.fromarray(arr.astype(np.uint8)).convert("RGBA")
    p = port.convert("RGBA"); p.putalpha(hfade(560, H, 0, 220))
    bg.alpha_composite(p, (W - 560, 0))
    glow_text(bg, (54, 150), "70.000.000", ImageFont.truetype(IB, 128), CREAM)
    glow_text(bg, (60, 300), "NGƯỜI CHẾT", ImageFont.truetype(IB, 84), RED)
    glow_text(bg, (60, 395), "VÌ MỘT NGƯỜI", ImageFont.truetype(IB, 84), CREAM)
    ImageDraw.Draw(bg).rectangle((62, 520, 360, 526), fill=GOLD)
    glow_text(bg, (62, 548), "Cuộc đời Adolf Hitler · 1889 – 1945", ImageFont.truetype(SR, 34), CREAM, r=8)
    return grain(vignette(bg, 0.6))


def v3():   # Berlin đổ nát làm nền + chân dung: "CHÀNG HỌA SĨ BỊ TỪ CHỐI"
    ruin = bw(cover(Image.open("assets/k/K56a.jpg").convert("RGB"), W, H, 0.5, 0.45), warm=0.5, contrast=1.1, bright=0.55)
    bg = ruin.convert("RGBA")
    dark = Image.new("RGBA", (W, H), (8, 6, 5, 255)); dark.putalpha(hfade(W, H, 0, 700, invert=True).point(lambda v: int(v * 0.85)))
    bg.alpha_composite(dark)
    port = bw(cover(Image.open("assets/k/K04.jpg").convert("RGB"), 620, H, 0.5, 0.2), warm=0.35, contrast=1.35)
    p = port.convert("RGBA"); p.putalpha(hfade(620, H, 0, 240))
    bg.alpha_composite(p, (W - 620, 0))
    # tranh màu nước nhỏ như "tấm ảnh cũ" ở góc trái dưới
    th = Image.open("assets/k/K03b.jpg").convert("RGB"); th.thumbnail((300, 220))
    fr = Image.new("RGBA", (th.width + 16, th.height + 16), (238, 228, 205, 255)); fr.paste(th, (8, 8))
    fr = fr.rotate(-4, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", fr.size, (0, 0, 0, 0)); sh.putalpha(fr.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .7)))
    bg.alpha_composite(sh, (70, 440)); bg.alpha_composite(fr, (60, 430))
    glow_text(bg, (56, 90), "CHÀNG HỌA SĨ", ImageFont.truetype(SB, 96), CREAM)
    glow_text(bg, (56, 200), "BỊ TỪ CHỐI", ImageFont.truetype(SB, 96), GOLD)
    glow_text(bg, (60, 330), "...và cái giá của thế giới", ImageFont.truetype(SR, 40), CREAM, r=8)
    return grain(vignette(bg, 0.6))


for i, fn in enumerate([v1, v2, v3], 1):
    fn().convert("RGB").save(f"thumb/thumb_{i}.jpg", quality=92)
s = Image.new("RGB", (1280, 2160))
for i in range(3):
    s.paste(Image.open(f"thumb/thumb_{i + 1}.jpg"), (0, 720 * i))
s.resize((960, 1620)).save("thumb/_all.jpg")
