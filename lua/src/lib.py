"""Thư viện dựng hình cho kênh Nct official (khung dọc 1080×1920, phong cách giấy cắt kiểu Vox)."""
import math, unicodedata
from functools import lru_cache
from pathlib import Path

import numpy as np
import skia
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
W, H, FPS = 1080, 1920, 30
CY = 725  # tâm vùng nội dung (200–1250)

PAL = {
    "paper": "#EFE6D2", "paper2": "#E6DBC2", "ink": "#1E1C19", "yellow": "#F4C430",
    "red": "#C0392B", "navy": "#1F3A5F", "sea": "#8FA5AA", "sea2": "#83999E",
    "land": "#EDE3CB", "coast": "#5E5648", "grey": "#7A746A", "white": "#FBF7EE",
}


def col(name_or_hex, a=255):
    h = PAL.get(name_or_hex, name_or_hex).lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


SAMP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)

FONT_FILES = {
    "bold": "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "xbold": "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
    "semi": "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
    "med": "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
    "ital": "/usr/share/fonts/opentype/inter/Inter-SemiBoldItalic.otf",
    # font tài liệu: đã thử đủ dấu viết hoa (Ở, Ế, Ầ, Ỷ...) — DejaVu Sans Mono thì KHÔNG đủ
    "mono": "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
}


@lru_cache(None)
def _tf(name):
    return skia.Typeface.MakeFromFile(FONT_FILES[name])


@lru_cache(None)
def font(name, size):
    f = skia.Font(_tf(name), size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    f.setSubpixel(True)
    return f


def nfc(s):
    return unicodedata.normalize("NFC", s)


def tw(s, name="bold", size=40):
    return font(name, size).measureText(nfc(s))


# ---------- thời gian & easing ----------
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease_out(x):
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    return 3 * x * x - 2 * x * x * x


def back_out(x, k=1.7):
    x -= 1
    return 1 + x * x * ((k + 1) * x + k)


def prog(t, a, b, fn=ease_out):
    if b <= a:
        return 1.0 if t >= a else 0.0
    return fn(clamp((t - a) / (b - a)))


def lerp(a, b, p):
    return a + (b - a) * p


# ---------- vẽ cơ bản ----------
def paint(color="ink", a=255, stroke=None, cap=True, **kw):
    p = skia.Paint(AntiAlias=True, Color=col(color, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        if cap:
            p.setStrokeCap(skia.Paint.kRound_Cap)
            p.setStrokeJoin(skia.Paint.kRound_Join)
    for k, v in kw.items():
        getattr(p, "set" + k)(v)
    return p


def text(c, s, x, y, name="bold", size=40, color="ink", a=255, align="left", stroke=0, stroke_color="ink"):
    s = nfc(s)
    f = font(name, size)
    w = f.measureText(s)
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    if stroke:
        sp = paint(stroke_color, a, stroke=stroke * 2)
        c.drawString(s, x, y, f, sp)
    c.drawString(s, x, y, f, paint(color, a))
    return w


class Xf:
    """Ngữ cảnh biến đổi: dịch tới (x,y), xoay, co giãn, độ mờ."""

    def __init__(self, c, x, y, rot=0.0, scale=1.0, alpha=1.0):
        self.c, self.x, self.y, self.r, self.s, self.a = c, x, y, rot, scale, alpha

    def __enter__(self):
        c = self.c
        if self.a < 0.999:
            c.saveLayerAlpha(None, int(255 * clamp(self.a)))
        else:
            c.save()
        c.translate(self.x, self.y)
        if self.r:
            c.rotate(self.r)
        if self.s != 1:
            c.scale(self.s, self.s)
        return c

    def __exit__(self, *a):
        self.c.restore()


def shadow_begin(c, bounds=None, dy=8, blur=10, a=70):
    p = skia.Paint(ImageFilter=skia.ImageFilters.DropShadow(0, dy, blur, blur, skia.ColorSetARGB(a, 20, 15, 5)))
    c.saveLayer(bounds, p)


def card(c, x, y, w, h, color="white", r=6, shadow=True, a=255):
    """Mảnh giấy (toạ độ cục bộ, góc trên trái x,y)."""
    rect = skia.Rect.MakeXYWH(x, y, w, h)
    if shadow:
        shadow_begin(c, rect.makeOutset(40, 50))
    c.drawRRect(skia.RRect.MakeRectXY(rect, r, r), paint(color, a))
    if shadow:
        c.restore()


def chip(c, s, cx, cy, p, size=40, bg="yellow", fg="ink", name="xbold"):
    """Chip chữ đen nền vàng, bật vào bằng back_out. p: 0..1 tiến độ xuất hiện."""
    if p <= 0:
        return
    s = nfc(s)
    w = tw(s, name, size) + size * 1.1
    h = size * 1.75
    sc = back_out(clamp(p)) if p < 1 else 1.0
    with Xf(c, cx, cy, 0, max(0.01, sc), clamp(p * 3)):
        card(c, -w / 2, -h / 2, w, h, bg, r=8)
        text(c, s, 0, size * 0.36, name, size, fg, align="center")


def name_tag(c, x, y, name, role, p, size=46, role_size=30, side="left"):
    """Thẻ tên: tên đậm + vai trò; trượt vào từ mép."""
    if p <= 0:
        return
    w = max(tw(name, "xbold", size), tw(role, "semi", role_size)) + 56
    h = size + role_size + 58
    dx = (1 - ease_out(clamp(p))) * (-60 if side == "left" else 60)
    with Xf(c, x + dx, y, 0, 1, clamp(p * 2)):
        card(c, 0, 0, w, h, "white", r=6)
        c.drawRect(skia.Rect.MakeXYWH(0, 0, 12, h), paint("yellow"))
        text(c, name, 32, 22 + size * 0.8, "xbold", size, "ink")
        text(c, role, 32, 22 + size + 14 + role_size * 0.8, "semi", role_size, "grey")


def label_tag(c, s, x, y, p, size=34, anchor="left", bg="white", fg="ink", name="bold"):
    """Nhãn chữ trong thẻ giấy nhỏ. anchor: left/right/center theo x."""
    if p <= 0:
        return
    w = tw(s, name, size) + size * 0.9
    h = size * 1.6
    ox = {"left": 0, "center": -w / 2, "right": -w}[anchor]
    sc = back_out(clamp(p)) if p < 1 else 1
    with Xf(c, x, y, 0, max(0.01, sc), clamp(p * 3)):
        card(c, ox, -h / 2, w, h, bg, r=5)
        text(c, s, ox + size * 0.45, size * 0.36, name, size, fg)


def stamp(c, s, cx, cy, p, size=72, color="red", rot=-8):
    """Con dấu đóng xuống: phóng 1.8→1, khung đôi."""
    if p <= 0:
        return
    s = nfc(s)
    sc = lerp(1.8, 1.0, ease_out(clamp(p)))
    a = clamp(p * 2.5) * 235
    w = tw(s, "xbold", size) + size * 0.8
    h = size * 1.45
    with Xf(c, cx, cy, rot, sc):
        r = skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h)
        c.drawRRect(skia.RRect.MakeRectXY(r, 8, 8), paint(color, a, stroke=7, cap=False))
        r2 = r.makeInset(11, 11)
        c.drawRRect(skia.RRect.MakeRectXY(r2, 4, 4), paint(color, a, stroke=2.5, cap=False))
        text(c, s, 0, size * 0.36, "xbold", size, color, a=a, align="center")


def note_label(c, s, x, y, p, size=26, color="red"):
    """Nhãn nhỏ 'DIỄN Ý' / 'MINH HỌA' (≥26px)."""
    if p <= 0:
        return
    w = tw(s, "xbold", size) + 22
    with Xf(c, x, y, 0, 1, clamp(p * 3)):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(0, 0, w, size + 16), 4, 4), paint(color))
        text(c, s, 11, size * 0.88 + 7, "xbold", size, "white")


def highlight(c, x, y, w, h, p, color="yellow", a=235):
    """Bút dạ quang quét từ trái sang phải phía sau chữ."""
    if p <= 0:
        return
    c.drawRect(skia.Rect.MakeXYWH(x - 6, y, (w + 12) * clamp(p), h), paint(color, a))


def typed(s, p):
    s = nfc(s)
    return s[: int(round(len(s) * clamp(p)))]


# ---------- nền giấy ----------
@lru_cache(None)
def paper_image(seed=3, base="paper"):
    rng = np.random.default_rng(seed)
    h = PAL[base].lstrip("#")
    rgb = np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)
    small = rng.normal(0, 1, (H // 8, W // 8)).astype(np.float32)
    big = np.array(Image.fromarray(((small * 20) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) - 128
    fine = rng.normal(0, 5, (H, W)).astype(np.float32)
    # sợi giấy
    fib = np.zeros((H, W), np.float32)
    for _ in range(500):
        x, y = rng.integers(0, W), rng.integers(0, H)
        L = rng.integers(10, 40)
        ang = rng.uniform(0, np.pi)
        xs = (x + np.cos(ang) * np.arange(L)).astype(int).clip(0, W - 1)
        ys = (y + np.sin(ang) * np.arange(L)).astype(int).clip(0, H - 1)
        fib[ys, xs] -= rng.uniform(4, 9)
    v = big * 0.35 + fine + fib
    yy, xx = np.mgrid[0:H, 0:W]
    vign = -18 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2
    arr = np.clip(rgb[None, None, :] + (v + vign)[..., None], 0, 255).astype(np.uint8)
    rgba = np.dstack([arr, np.full((H, W), 255, np.uint8)])
    return skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)


def draw_paper(c, base="paper"):
    c.drawImage(paper_image(3, base), 0, 0)


@lru_cache(None)
def grain_image():
    rng = np.random.default_rng(11)
    g = rng.normal(128, 14, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)
    g = np.array(Image.fromarray(g).resize((W, H), Image.BILINEAR))
    rgba = np.dstack([g, g, g, np.full_like(g, 255)])
    return skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)


def draw_grain(c, a=40):
    p = skia.Paint(BlendMode=skia.BlendMode.kOverlay)
    p.setAlphaf(a / 255)
    c.drawImage(grain_image(), 0, 0, SAMP, p)


# ---------- ảnh tư liệu ----------
class Photo:
    """Ảnh tư liệu đen trắng → duotone mực/giấy cho hợp tông."""

    def __init__(self, path, maxdim=2600, tone=True):
        im = Image.open(path)
        im = im.convert("L")
        s = maxdim / max(im.size)
        if s < 1:
            im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        g = np.asarray(im, np.float32) / 255.0
        if tone:
            dark = np.array([28, 26, 23], np.float32)
            light = np.array([246, 240, 226], np.float32)
            rgb = dark[None, None] + g[..., None] * (light - dark)[None, None]
        else:
            rgb = np.repeat(g[..., None] * 255, 3, 2)
        arr = np.dstack([rgb.clip(0, 255).astype(np.uint8), np.full(g.shape, 255, np.uint8)])
        self.w, self.h = im.width, im.height
        self.img = skia.Image.fromarray(np.ascontiguousarray(arr), colorType=skia.ColorType.kRGBA_8888_ColorType).withDefaultMipmaps()
        # bản mờ để làm nền khi giữ nguyên khung ảnh ngang
        sm = Image.fromarray(arr[..., :3]).resize((max(1, self.w // 10), max(1, self.h // 10)), Image.BILINEAR)
        sm = sm.filter(ImageFilter.GaussianBlur(6))
        sa = np.dstack([np.asarray(sm), np.full((sm.height, sm.width), 255, np.uint8)])
        self.blur = skia.Image.fromarray(np.ascontiguousarray(sa), colorType=skia.ColorType.kRGBA_8888_ColorType)

    def cover(self, c, dst, fx=0.5, fy=0.5, zoom=1.0, img=None):
        """Vẽ phủ kín dst (Rect), lấy tâm tại (fx,fy) theo tỉ lệ ảnh, zoom>=1 phóng thêm."""
        img = img or self.img
        iw, ih = img.width(), img.height()
        da = dst.width() / dst.height()
        if iw / ih > da:
            sh = ih / zoom
            sw = sh * da
        else:
            sw = iw / zoom
            sh = sw / da
        cx = clamp(fx * iw, sw / 2, iw - sw / 2)
        cy = clamp(fy * ih, sh / 2, ih - sh / 2)
        src = skia.Rect.MakeXYWH(cx - sw / 2, cy - sh / 2, sw, sh)
        c.drawImageRect(img, src, dst, SAMP, None, skia.Canvas.kStrict_SrcRectConstraint)

    def blur_bg(self, c, darken=110):
        self.cover(c, skia.Rect.MakeWH(W, H), img=self.blur)
        c.drawRect(skia.Rect.MakeWH(W, H), paint("ink", darken))

    def framed(self, c, cx, cy, w, rot=0.0, scale=1.0, alpha=1.0, border=16, crop=None):
        """Ảnh đặt trên giấy như bản in có viền trắng. crop=(x0,y0,x1,y1) theo tỉ lệ 0..1."""
        x0, y0, x1, y1 = crop or (0, 0, 1, 1)
        sw, sh = (x1 - x0) * self.w, (y1 - y0) * self.h
        h = w * sh / sw
        with Xf(c, cx, cy, rot, scale, alpha):
            card(c, -w / 2 - border, -h / 2 - border, w + 2 * border, h + 2 * border, "white", r=3)
            src = skia.Rect.MakeXYWH(x0 * self.w, y0 * self.h, sw, sh)
            c.drawImageRect(self.img, src, skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), SAMP, None, skia.Canvas.kStrict_SrcRectConstraint)
        return h


# ---------- bản đồ ----------
def merc(lat):
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


PLACES = {"warsaw": (21.01, 52.23), "auschwitz": (19.23, 50.03), "london": (-0.13, 51.51)}


def country_rings(name):
    """Các vòng toạ độ (lon, lat) của một nước trong Natural Earth (để tô màu)."""
    import shapefile
    sf = shapefile.Reader(str(ROOT / "assets/map/naturalearth_lowres.shp"))
    fields = [f[0] for f in sf.fields[1:]]
    out = []
    for rec, shp in zip(sf.records(), sf.shapes()):
        if dict(zip(fields, rec)).get("name") == name:
            parts = list(shp.parts) + [len(shp.points)]
            out += [shp.points[parts[i]:parts[i + 1]] for i in range(len(parts) - 1)]
    sm = []
    for pts_ in out:
        for _ in range(3):
            q = []
            for k in range(len(pts_)):
                (x1, y1), (x2, y2) = pts_[k], pts_[(k + 1) % len(pts_)]
                q += [(0.75 * x1 + 0.25 * x2, 0.75 * y1 + 0.25 * y2), (0.25 * x1 + 0.75 * x2, 0.25 * y1 + 0.75 * y2)]
            pts_ = q
        sm.append(pts_)
    return sm
# chuỗi đảo Tây Bắc Hawaii, từ Oahu tới Midway (đường cáp đi dọc chuỗi đảo)
CHAIN = [(202.03, 21.35), (200.5, 22.05), (198.08, 23.06), (195.3, 23.57), (193.8, 23.75),
         (188.2, 25.77), (186.05, 26.06), (184.2, 27.83), (182.63, 28.21)]
SMALL_ISLANDS = CHAIN[2:] + [(181.7, 28.4), (166.6, 19.3)]


class Map:
    # châu Âu cho tập Pilecki; không vẽ biên giới (biên giới hiện đại khác năm 1940)
    LON0, LON1, LAT0, LAT1, B = -14.0, 36.0, 4.0, 62.0, 90.0

    def __init__(self):
        cache = ROOT / "build/map_big.png"
        if cache.exists():
            arr = np.asarray(Image.open(cache).convert("RGBA"))
        else:
            arr = self._build()
            Image.fromarray(arr).save(cache)
        self.img = skia.Image.fromarray(np.ascontiguousarray(arr), colorType=skia.ColorType.kRGBA_8888_ColorType).withDefaultMipmaps()
        self.MY1 = merc(self.LAT1)

    def XY(self, lon, lat):
        return (lon - self.LON0) * self.B, (merc(self.LAT1) - merc(lat)) * self.B

    def _build(self):
        import shapefile
        Wb = int((self.LON1 - self.LON0) * self.B)
        Hb = int((merc(self.LAT1) - merc(self.LAT0)) * self.B)
        s = skia.Surface(Wb, Hb)
        c = s.getCanvas()
        c.clear(col("sea"))
        # lưới kinh vĩ tuyến mờ
        gp = paint("white", 60, stroke=2, cap=False)
        for lon in range(int(self.LON0) // 5 * 5, int(self.LON1) + 5, 5):
            x, _ = self.XY(lon, 0)
            c.drawLine(x, 0, x, Hb, gp)
        for lat in range(int(self.LAT0) // 5 * 5, int(self.LAT1) + 5, 5):
            _, y = self.XY(0, lat)
            c.drawLine(0, y, Wb, y, gp)
        path = skia.Path()
        sf = shapefile.Reader(str(ROOT / "assets/map/naturalearth_lowres.shp"))
        for shp in sf.shapes():
            pts = shp.points
            parts = list(shp.parts) + [len(pts)]
            for i in range(len(parts) - 1):
                ring = pts[parts[i]:parts[i + 1]]
                # bản đồ lấy Thái Bình Dương làm giữa: kinh độ Tây (âm) dời sang 180..360
                lons = [p[0] for p in ring]  # châu Âu: giữ kinh độ gốc
                if max(lons) - min(lons) > 180:  # vòng vắt qua kinh tuyến gốc (châu Phi, châu Âu): ngoài khung
                    continue
                if max(lons) < self.LON0 - 5 or min(lons) > self.LON1 + 5:
                    continue
                pts_ = [(lon, lat) for lon, (_, lat) in zip(lons, ring)]
                for _ in range(3):  # bo góc Chaikin: dữ liệu 1:110 triệu gãy góc khi phóng gần
                    q = []
                    for k in range(len(pts_)):
                        (x1, y1), (x2, y2) = pts_[k], pts_[(k + 1) % len(pts_)]
                        q += [(0.75 * x1 + 0.25 * x2, 0.75 * y1 + 0.25 * y2), (0.25 * x1 + 0.75 * x2, 0.25 * y1 + 0.75 * y2)]
                    pts_ = q
                lons, ring = [p_[0] for p_ in pts_], [(None, p_[1]) for p_ in pts_]
                for j, (lon, (_, lat)) in enumerate(zip(lons, ring)):
                    x, y = self.XY(lon, max(lat, self.LAT0 - 5))
                    (path.moveTo if j == 0 else path.lineTo)(x, y)
                path.close()
        # bóng đổ kiểu giấy cắt
        sh = skia.Paint(ImageFilter=skia.ImageFilters.DropShadow(3, 6, 6, 6, skia.ColorSetARGB(110, 30, 25, 15)))
        c.saveLayer(None, sh)
        c.drawPath(path, paint("land"))
        c.drawPath(path, paint("land", stroke=9))  # lấp khe giữa các nước sau khi bo góc
        c.restore()
        arr = s.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        # vân giấy nhẹ
        rng = np.random.default_rng(5)
        n = rng.normal(0, 4, arr.shape[:2])
        arr[..., :3] = np.clip(arr[..., :3].astype(np.float32) + n[..., None], 0, 255).astype(np.uint8)
        return arr

    def proj(self, lon, lat, cam):
        clon, clat, z = cam
        return (lon - clon) * z + W / 2, (merc(clat) - merc(lat)) * z + CY

    def draw(self, c, cam):
        clon, clat, z = cam
        k = z / self.B
        c.drawRect(skia.Rect.MakeWH(W, H), paint("sea"))
        c.save()
        X0, Y0 = self.XY(clon, clat)
        c.translate(W / 2 - X0 * k, CY - Y0 * k)
        c.scale(k, k)
        c.drawImage(self.img, 0, 0, SAMP, None)
        c.restore()


def cam_lerp(a, b, p):
    return (lerp(a[0], b[0], p), lerp(a[1], b[1], p), math.exp(lerp(math.log(a[2]), math.log(b[2]), p)))


def pin(c, x, y, p, color="yellow", r=13):
    if p <= 0:
        return
    sc = back_out(clamp(p))
    with Xf(c, x, y, 0, max(0.01, sc)):
        shadow_begin(c, skia.Rect.MakeXYWH(-40, -40, 80, 90), dy=4, blur=4, a=90)
        c.drawCircle(0, 0, r, paint(color))
        c.restore()
        c.drawCircle(0, 0, r, paint("ink", stroke=4))


def rings(c, x, y, t, t0, t1, color="ink", max_r=420, period=0.9, width=5, a=200):
    """Sóng vô tuyến: các vòng lan ra từ (x,y) trong khoảng [t0,t1]."""
    if t < t0:
        return
    k = 0
    while True:
        st = t0 + k * period
        if st > min(t, t1):
            break
        age = t - st
        r = 20 + age * max_r / 1.6
        al = a * clamp(1 - age / 1.6)
        if al > 2:
            c.drawCircle(x, y, r, paint(color, al, stroke=width))
        k += 1


def path_partial(c, pts, p, pnt, curve=0.0):
    """Vẽ dần đường đi qua các điểm (đường cong bậc 2 nếu curve≠0, chỉ cho 2 điểm)."""
    if p <= 0:
        return None
    path = skia.Path()
    path.moveTo(*pts[0])
    if len(pts) == 2 and curve:
        (x0, y0), (x1, y1) = pts
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        nx, ny = -(y1 - y0), (x1 - x0)
        path.quadTo(mx + nx * curve, my + ny * curve, x1, y1)
    else:
        for q in pts[1:]:
            path.lineTo(*q)
    pm = skia.PathMeasure(path, False)
    L = pm.getLength()
    d = skia.Path()
    pm.getSegment(0, L * clamp(p), d, True)
    c.drawPath(d, pnt)
    pos, tan = pm.getPosTan(L * clamp(p))
    return (pos.x(), pos.y()), (tan.x(), tan.y())


def arrow_head(c, pos, tan, size=22, color="ink", a=255):
    x, y = pos
    ang = math.atan2(tan[1], tan[0])
    path = skia.Path()
    for i, (dx, dy) in enumerate([(0, 0), (-size, -size * 0.55), (-size * 0.7, 0), (-size, size * 0.55)]):
        px = x + dx * math.cos(ang) - dy * math.sin(ang)
        py = y + dx * math.sin(ang) + dy * math.cos(ang)
        (path.moveTo if i == 0 else path.lineTo)(px, py)
    path.close()
    c.drawPath(path, paint(color, a))


def carrier_token(c, x, y, p=1.0, color="navy", s=1.0, rot=0):
    """Ký hiệu tàu sân bay giấy cắt (nhìn ngang)."""
    if p <= 0:
        return
    with Xf(c, x, y, rot, s * max(0.01, back_out(clamp(p))), clamp(p * 3)):
        shadow_begin(c, skia.Rect.MakeXYWH(-80, -50, 160, 110), dy=4, blur=4, a=90)
        hull = skia.Path()
        hull.moveTo(-50, -6); hull.lineTo(52, -6); hull.lineTo(42, 10); hull.lineTo(-44, 10); hull.close()
        c.drawPath(hull, paint(color))
        c.drawRect(skia.Rect.MakeXYWH(-56, -11, 112, 6), paint(color))
        c.drawRect(skia.Rect.MakeXYWH(14, -25, 12, 15), paint(color))
        c.drawRect(skia.Rect.MakeXYWH(19, -33, 2.5, 9), paint(color))
        c.restore()


def plane_icon(c, x, y, ang_deg, color="red", s=1.0, a=255):
    with Xf(c, x, y, ang_deg, s):
        p = skia.Path()
        p.moveTo(18, 0); p.lineTo(-6, -4); p.lineTo(-10, -18); p.lineTo(-15, -18); p.lineTo(-13, -4)
        p.lineTo(-20, -3); p.lineTo(-24, -9); p.lineTo(-27, -9); p.lineTo(-25, 0); p.lineTo(-27, 9)
        p.lineTo(-24, 9); p.lineTo(-20, 3); p.lineTo(-13, 4); p.lineTo(-15, 18); p.lineTo(-10, 18)
        p.lineTo(-6, 4); p.close()
        c.drawPath(p, paint(color, a))


def antenna_icon(c, x, y, p, color="red", s=1.0):
    if p <= 0:
        return
    with Xf(c, x, y, 0, s * max(0.01, back_out(clamp(p))), clamp(p * 3)):
        pt = paint(color, stroke=5)
        c.drawLine(0, 0, -16, 44, pt); c.drawLine(0, 0, 16, 44, pt)
        c.drawLine(-9, 24, 9, 24, pt); c.drawLine(0, 0, 0, 44, paint(color, stroke=3))
        c.drawCircle(0, -4, 6, paint(color))
        for r in (16, 28):
            arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(-r, -4 - r, 2 * r, 2 * r), -150, 120)
            c.drawPath(arc, paint(color, stroke=4))


def drift_cam(cam, t, t0, rate=0.01):
    """Bản đồ phóng rất chậm để khung không đứng im."""
    return (cam[0], cam[1], cam[2] * (1 + rate * max(0.0, t - t0)))
