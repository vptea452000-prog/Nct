"""Thumbnail Alexander — 1280x720, 3 phương án."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import numpy as np
Image.MAX_IMAGE_PIXELS = None
W, H = 1280, 720
SB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
IB = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
GOLD = (236, 196, 110); CREAM = (250, 240, 218)

def cover(im, w, h, cx=0.5, cy=0.5):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width*s)+1, int(im.height*s)+1), Image.LANCZOS)
    x = int((im.width - w) * cx); y = int((im.height - h) * cy); return im.crop((x, y, x+w, y+h))

def sepia(im, dark=0.55):
    g = np.asarray(ImageOps.grayscale(im)).astype(np.float32) / 255
    rgb = np.stack([g*1.08, g*0.92, g*0.70], -1) * dark
    return Image.fromarray((np.clip(rgb, 0, 1)*255).astype(np.uint8))

def grade_head(head):
    rgb = head.convert("RGB"); a = head.getchannel("A")
    arr = np.asarray(rgb).astype(np.float32) / 255
    arr = arr ** 1.15 * np.array([1.10, 0.98, 0.82])          # ấm, tương phản
    h_, w_ = arr.shape[:2]
    xx = np.linspace(0, 1, w_)[None, :, None]
    arr = arr * (0.55 + 0.75 * xx)                             # ánh sáng từ phải
    rgb = Image.fromarray((np.clip(arr, 0, 1)*255).astype(np.uint8))
    out = rgb.convert("RGBA"); out.putalpha(a); return out

def vignette(im, k=0.75):
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx-W/2)/(W/2))**2 + ((yy-H/2)/(H/2))**2)
    v = np.clip(1 - k * np.clip(d - 0.45, 0, 1) ** 1.4, 0, 1)[..., None]
    return Image.fromarray((np.asarray(im).astype(np.float32) * v).astype(np.uint8))

def glow_text(base, xy, text, font, fill, anchor="la", glow=(0,0,0), r=14, stroke=0, sfill=(0,0,0)):
    lay = Image.new("RGBA", base.size, (0,0,0,0)); d = ImageDraw.Draw(lay)
    d.text(xy, text, font=font, fill=glow+(255,), anchor=anchor, stroke_width=stroke+6, stroke_fill=glow+(255,))
    base.alpha_composite(lay.filter(ImageFilter.GaussianBlur(r)))
    ImageDraw.Draw(base).text(xy, text, font=font, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)

HEAD = grade_head(Image.open("thumb/head_cut.png"))

def place_head(base, hgt, x, y, rim=GOLD):
    hd = HEAD.resize((int(HEAD.width*hgt/HEAD.height), hgt), Image.LANCZOS)
    a = hd.getchannel("A")
    halo = Image.new("RGBA", hd.size, rim+(0,)); halo.putalpha(a.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v*0.55)))
    base.alpha_composite(halo, (x, y))
    sh = Image.new("RGBA", hd.size, (0,0,0,0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v*0.7)))
    base.alpha_composite(sh, (x-30, y+10)); base.alpha_composite(hd, (x, y))

def v1():   # đám lính nổi loạn phía sau + ĐI ĐI!
    bg = sepia(cover(Image.open("assets/k/K14a.jpg").convert("RGB"), W, H, 0.5, 0.42), 0.62).filter(ImageFilter.GaussianBlur(1.5))
    bg = vignette(bg, 0.9).convert("RGBA")
    grad = Image.linear_gradient("L").rotate(90).resize((W, H)); dark = Image.new("RGBA", (W, H), (8,6,4,0)); dark.putalpha(grad.point(lambda v: int(v*0.85)))
    bg.alpha_composite(dark)
    place_head(bg, 840, 640, -40)
    glow_text(bg, (60, 150), "ĐI ĐI!", ImageFont.truetype(SB, 210), CREAM, glow=(0,0,0), r=18)
    glow_text(bg, (68, 405), "BÀI DIỄN VĂN", ImageFont.truetype(IB, 58), GOLD, r=10)
    glow_text(bg, (68, 475), "Ở OPIS", ImageFont.truetype(IB, 58), GOLD, r=10)
    ImageDraw.Draw(bg).rectangle((68, 560, 360, 566), fill=GOLD)
    glow_text(bg, (68, 590), "ALEXANDER ĐẠI ĐẾ · 324 TCN", ImageFont.truetype(SR, 32), CREAM, r=8)
    return bg

def v2():   # nền đỏ sẫm tối giản + câu hỏi
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx-W*0.68)/W)**2 + ((yy-H*0.45)/H)**2)
    c = np.clip(1 - d*1.6, 0, 1)[..., None]
    arr = np.array([12, 6, 4]) + c * np.array([120, 34, 18])
    bg = Image.fromarray(arr.astype(np.uint8)).convert("RGBA")
    noise = Image.fromarray((np.random.default_rng(3).normal(0, 9, (H, W))+128).clip(0,255).astype(np.uint8)).convert("RGBA"); noise.putalpha(28)
    bg.alpha_composite(noise)
    place_head(bg, 860, 560, -30, rim=(255, 170, 90))
    f = ImageFont.truetype(IB, 96)
    glow_text(bg, (60, 170), "BỊ CHÍNH", f, CREAM, r=14)
    glow_text(bg, (60, 280), "QUÂN MÌNH", f, CREAM, r=14)
    glow_text(bg, (60, 390), "BỎ RƠI?", ImageFont.truetype(IB, 96), GOLD, r=14)
    glow_text(bg, (64, 545), "Alexander Đại đế · Opis, 324 TCN", ImageFont.truetype(SR, 34), CREAM, r=8)
    return bg

def v3():   # bản đồ vệ tinh đế chế + trích dẫn
    import sys; sys.path.insert(0, "src")
    m = Image.open("assets/map/bluemarble_12000.jpg")  # 24000x12000
    def px(lon, lat): return (lon+180)/360*m.width, (90-lat)/180*m.height
    x0, y0 = px(14, 50); x1, y1 = px(82, 12)
    bg = m.crop((int(x0), int(y0), int(x1), int(y1))).resize((W, int(W*(y1-y0)/(x1-x0))), Image.LANCZOS)
    bg = cover(bg, W, H, 0.5, 0.4)
    bg = ImageEnhance.Color(bg).enhance(0.6); bg = ImageEnhance.Brightness(bg).enhance(0.55)
    bg = vignette(bg, 0.9).convert("RGBA")
    grad = Image.linear_gradient("L").rotate(90).resize((W, H)); dark = Image.new("RGBA", (W, H), (6,6,8,0)); dark.putalpha(grad.point(lambda v: int(v*0.7)))
    bg.alpha_composite(dark)
    place_head(bg, 820, 650, -20)
    f = ImageFont.truetype(SB, 92)
    glow_text(bg, (60, 140), "“TA ĐÃ CHO", f, CREAM, r=16)
    glow_text(bg, (60, 250), "CÁC NGƯƠI", f, CREAM, r=16)
    glow_text(bg, (60, 360), "TẤT CẢ”", f, GOLD, r=16)
    ImageDraw.Draw(bg).rectangle((66, 500, 330, 506), fill=GOLD)
    glow_text(bg, (66, 530), "ALEXANDER ĐẠI ĐẾ", ImageFont.truetype(IB, 40), CREAM, r=8)
    return bg

for i, fn in enumerate([v1, v2, v3], 1):
    fn().convert("RGB").save(f"thumb/thumb_{i}.jpg", quality=92)
