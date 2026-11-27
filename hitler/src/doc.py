"""Bộ dựng phim tài liệu kiểu tranh + bản đồ (16:9): ảnh lia/zoom êm có chỉnh màu thống nhất, bản đồ động vẽ từ Natural Earth,
thẻ chữ sang (serif), phụ đề, viền tối + hạt phim nhẹ. Hàm thuần theo thời gian t (giây trong video).
"""
import math, json, sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import skia
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
W, H, FPS = 1920, 1080, 30

FONTS = {
    "serif": "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "serif_b": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "serif_i": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "sans": "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
    "sans_m": "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
}


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, q):
    return a + (b - a) * q


def ease(x):
    x = clamp(x); return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def col(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(clamp(a, 0, 255)), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def P(h, a=255, stroke=None, blur=0):
    p = skia.Paint(AntiAlias=True, Color=col(h, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


@lru_cache(None)
def font(name, size):
    f = skia.Font(skia.Typeface.MakeFromFile(FONTS[name]), size)
    f.setEdging(skia.Font.Edging.kAntiAlias); f.setSubpixel(True)
    return f


def text_w(s, name, size):
    return font(name, size).measureText(s)


def draw_text(c, s, x, y, name="serif", size=60, color="#F2EAD8", a=255, align="center", spacing=0.0, shadow=True):
    f = font(name, size)
    if spacing:
        chars = list(s)
        widths = [f.measureText(ch) + spacing for ch in chars]
        total = sum(widths) - spacing
        x0 = x - total / 2 if align == "center" else x
        if shadow:
            cx = x0
            for ch, w in zip(chars, widths):
                c.drawString(ch, cx + 2, y + 3, f, P("#000000", a * 0.55, blur=6)); cx += w
        cx = x0
        for ch, w in zip(chars, widths):
            c.drawString(ch, cx, y, f, P(color, a)); cx += w
        return
    w = f.measureText(s)
    x0 = x - w / 2 if align == "center" else (x - w if align == "right" else x)
    if shadow:
        c.drawString(s, x0 + 2, y + 3, f, P("#000000", a * 0.6, blur=7))
    c.drawString(s, x0, y, f, P(color, a))


# ---------------------------------------------------------------- ảnh: chỉnh màu thống nhất (tông ấm như tranh cổ)
IMG_DIR = ROOT / "assets" / "k"


@lru_cache(None)
def image(code, maxw=3200):
    p = IMG_DIR / f"{code}.jpg"
    im = Image.open(p).convert("RGB")
    if max(im.size) > maxw:
        im.thumbnail((maxw, maxw), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    sat = a.std(axis=2).mean()
    if sat < 0.03:                         # tranh khắc đen trắng → sepia ấm
        g = a.mean(axis=2, keepdims=True)
        g = np.clip((g - 0.04) * 1.08, 0, 1)
        tint = np.array([1.0, 0.90, 0.74])
        a = g * tint + (1 - g) * np.array([0.08, 0.06, 0.05]) * (1 - g)
    else:                                  # ảnh màu → ấm nhẹ, giảm bão hòa một chút
        g = a.mean(axis=2, keepdims=True)
        a = g + (a - g) * 0.85
        a = a * np.array([1.04, 1.0, 0.92])
    a = np.clip(a, 0, 1)
    arr = (a * 255).astype(np.uint8)
    rgba = np.dstack([arr, np.full(arr.shape[:2], 255, np.uint8)])
    return skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)


SAMP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)


def ken_burns(c, code, q, r0, r1, alpha=1.0, dim=0.0, bg="#0C0A08"):
    """Vẽ ảnh lấp đầy khung, khung nhìn trượt từ r0 → r1 (x, y, scale) — x,y là tâm (0..1), scale ≥ 1 (1 = vừa khung)."""
    img = image(code)
    iw, ih = img.width(), img.height()
    x = lerp(r0[0], r1[0], q); y = lerp(r0[1], r1[1], q); s = lerp(r0[2], r1[2], q)
    cover = max(W / iw, H / ih)
    contain = min(W / iw, H / ih)
    k = (cover if r0[2] >= 1 else contain) * s
    vw, vh = W / k, H / k
    cx = clamp(x * iw, min(vw / 2, iw / 2), max(iw - vw / 2, iw / 2))
    cy = clamp(y * ih, min(vh / 2, ih / 2), max(ih - vh / 2, ih / 2))
    src = skia.Rect.MakeXYWH(cx - vw / 2, cy - vh / 2, vw, vh)
    c.save()
    if alpha < 0.999:
        c.saveLayerAlpha(None, int(255 * alpha))
    if iw * k < W or ih * k < H:          # ảnh hẹp: nền mờ phía sau + ảnh ở giữa
        c.drawRect(skia.Rect.MakeWH(W, H), P(bg))
        bl = skia.Paint(); bl.setImageFilter(skia.ImageFilters.Blur(40, 40)); bl.setAlphaf(0.5)
        c.drawImageRect(img, skia.Rect.MakeWH(W, H), SAMP, bl)
    c.drawImageRect(img, src, skia.Rect.MakeWH(W, H), SAMP, skia.Paint(AntiAlias=True))
    if dim > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 255 * dim))
    if alpha < 0.999:
        c.restore()
    c.restore()


def objects_row(c, codes, t0, t, bg="#14110D"):
    """Dãy cổ vật hiện lần lượt trên nền tối, có bóng đổ."""
    c.drawRect(skia.Rect.MakeWH(W, H), P(bg))
    c.drawCircle(W / 2, H / 2, 900, P("#3A2E22", 120, blur=200))
    n = len(codes); slot = W / (n + 0.4)
    for i, code in enumerate(codes):
        a = ease((t - t0 - i * 0.9) / 0.7)
        if a <= 0:
            continue
        img = image(code); iw, ih = img.width(), img.height()
        k = min(slot * 0.82 / iw, 640 / ih)
        w_, h_ = iw * k, ih * k
        cx = slot * (i + 0.7); cy = H / 2 - 20 + 20 * (1 - a)
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - w_ / 2 + 10, cy - h_ / 2 + 18, w_, h_), 8, 8, P("#000000", 160 * a, blur=24))
        pt = skia.Paint(AntiAlias=True); pt.setAlphaf(a)
        c.drawImageRect(img, skia.Rect.MakeXYWH(cx - w_ / 2, cy - h_ / 2, w_, h_), SAMP, pt)


# ---------------------------------------------------------------- bản đồ
MAP_LON0, MAP_LON1, MAP_LAT0, MAP_LAT1 = 8.0, 82.0, 12.0, 50.0


def lonlat(lon, lat, view):
    """Kinh/vĩ → toạ độ khung, view = (lon tâm, lat tâm, độ rộng kinh độ). Ảnh nền equirectangular nên tỉ lệ hai trục bằng nhau."""
    clon, clat, span = view
    k = W / span
    return W / 2 + (lon - clon) * k, H / 2 - (lat - clat) * k


R_LON0, R_LON1, R_LAT0, R_LAT1 = -12.0, 55.0, 34.0, 68.0     # châu Âu, cắt từ Blue Marble (NASA)


@lru_cache(None)
def map_raster():
    """Ảnh vệ tinh Blue Marble (NASA, qua Wikimedia Commons) — cắt vùng, chỉnh màu ấm, trầm để chữ nổi."""
    Image.MAX_IMAGE_PIXELS = None
    src = Image.open(ROOT / "assets" / "map" / "bluemarble_12000.jpg")
    Wd, Hd = src.size
    box = (int((R_LON0 + 180) / 360 * Wd), int((90 - R_LAT1) / 180 * Hd), int((R_LON1 + 180) / 360 * Wd), int((90 - R_LAT0) / 180 * Hd))
    im = src.crop(box).convert("RGB")
    a = np.asarray(im).astype(np.float32) / 255.0
    g = a.mean(axis=2, keepdims=True)
    a = g + (a - g) * 0.72                                   # giảm bão hòa
    a = a * np.array([1.04, 0.99, 0.90]) * 0.86              # ấm, trầm
    sea = (a[..., 2] > a[..., 0] + 0.08) & (g[..., 0] < 0.25)
    a[sea] = a[sea] * 0.55 + np.array([0.06, 0.09, 0.12]) * 0.45   # biển xanh đen dịu
    a = np.clip(a, 0, 1)
    arr = (a * 255).astype(np.uint8)
    rgba = np.dstack([arr, np.full(arr.shape[:2], 255, np.uint8)])
    return skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)


@lru_cache(None)
def land_rings():
    import shapefile
    sf = shapefile.Reader(str(REPO / "midway_v2" / "assets" / "map" / "naturalearth_lowres.shp"))
    rings = []
    for shp in sf.shapes():
        b = shp.bbox
        if b[2] < -30 or b[0] > 130 or b[3] < -10 or b[1] > 75:
            continue
        pts = shp.points; parts = list(shp.parts) + [len(pts)]
        for i in range(len(parts) - 1):
            rings.append(pts[parts[i]:parts[i + 1]])
    return rings


def land_path(view):
    p = skia.Path()
    for ring in land_rings():
        for j, (lon, lat) in enumerate(ring):
            x, y = lonlat(lon, lat, view)
            (p.moveTo if j == 0 else p.lineTo)(x, y)
        p.close()
    return p


RIVERS = {
    "Nile": [(31.2, 30.0), (31.0, 27.5), (32.7, 25.7), (32.9, 24.1), (31.5, 21.5), (30.6, 19.5), (32.5, 15.6)],
    "Euphrates": [(38.3, 38.9), (38.4, 37.0), (39.9, 36.0), (41.5, 34.4), (43.3, 33.0), (44.4, 32.5), (46.0, 31.0), (47.5, 30.6)],
    "Tigris": [(39.6, 38.4), (42.1, 37.2), (43.1, 36.3), (43.8, 34.6), (44.4, 33.3), (45.9, 32.1), (47.2, 31.0), (47.5, 30.6)],
    "Indus": [(75.5, 35.5), (73.0, 34.0), (72.2, 33.0), (71.2, 31.0), (70.0, 28.5), (68.6, 26.0), (67.9, 24.4)],
    "Oxus": [(72.0, 37.0), (68.5, 37.3), (66.5, 37.8), (62.5, 40.0), (60.0, 42.4), (59.0, 43.6)],
}
CITIES = {
    "Pella": (22.5, 40.76), "Athens": (23.73, 37.98), "Thebes": (23.32, 38.32), "Byzantium": (28.97, 41.01),
    "Sardis": (28.03, 38.48), "Issus": (36.2, 36.85), "Tyre": (35.2, 33.27), "Memphis": (31.25, 29.85),
    "Alexandria": (29.92, 31.2), "Siwa": (25.52, 29.2), "Gaugamela": (43.3, 36.4), "Babylon": (44.42, 32.54),
    "Susa": (48.25, 32.19), "Persepolis": (52.89, 29.93), "Ecbatana": (48.52, 34.8), "Bactra": (66.9, 36.76),
    "Maracanda": (66.96, 39.65), "Taxila": (72.83, 33.75), "Patala": (68.4, 24.7), "Pura": (60.8, 27.2),
    "Opis": (44.4, 33.9), "Granicus": (27.3, 40.25), "Hellespont": (26.4, 40.2), "Cyrene": (21.85, 32.82),
}
CITY_VN = {"Athens": "Athens", "Thebes": "Thebes", "Pella": "Pella", "Babylon": "Babylon", "Opis": "Opis", "Susa": "Susa",
           "Persepolis": "Persepolis", "Alexandria": "Alexandria", "Memphis": "Memphis", "Bactra": "Bactra", "Taxila": "Taxila"}
ROUTE = ["Pella", "Hellespont", "Granicus", "Sardis", "Issus", "Tyre", "Memphis", "Siwa", "Memphis", "Gaugamela", "Babylon", "Susa",
         "Persepolis", "Ecbatana", "Bactra", "Maracanda", "Bactra", "Taxila", "Patala", "Pura", "Persepolis", "Susa", "Opis"]

REGIONS = {   # tâm (lon, lat), bán kính (độ), tên tiếng Việt
    "Macedonia": ((22.3, 40.9), 1.6, "MACEDONIA"), "Thrace": ((26.0, 41.9), 2.0, "THRACE"),
    "Thessaly": ((22.2, 39.5), 1.0, "THESSALY"), "Greece": ((22.8, 38.2), 1.6, "HY LẠP"),
    "Ionia": ((27.4, 38.2), 1.2, "IONIA"), "Lydia": ((28.6, 38.9), 1.3, "LYDIA"), "Phrygia": ((31.5, 39.3), 2.0, "PHRYGIA"),
    "Egypt": ((31.0, 27.5), 3.2, "AI CẬP"), "Cyrene": ((21.8, 31.8), 2.0, "CYRENE"), "Syria": ((37.5, 35.0), 2.0, "SYRIA"),
    "Palestine": ((35.2, 31.6), 1.2, "PALESTINE"), "Mesopotamia": ((43.5, 33.8), 2.6, "LƯỠNG HÀ"),
    "Persia": ((53.5, 30.2), 3.0, "BA TƯ"), "Media": ((48.8, 35.4), 2.4, "MEDIA"), "Bactria": ((67.5, 36.8), 3.0, "BACTRIA"),
    "Scythia": ((66.5, 43.0), 3.4, "SCYTHIA"), "India": ((72.5, 30.5), 3.4, "ẤN ĐỘ"), "Gedrosia": ((63.0, 26.3), 3.0, "GEDROSIA"),
}

KINGDOMS = [   # các vương quốc kế tục (~301 TCN), đa giác gần đúng (lon, lat)
    ("CASSANDER", "#8C5A3C", [(19.5, 42.5), (24.5, 42.0), (24.5, 37.0), (21.0, 36.5), (19.5, 39.5)]),
    ("LYSIMACHUS", "#5C7A4A", [(24.5, 42.5), (29.5, 43.0), (33.0, 41.5), (31.0, 37.0), (26.5, 36.8), (25.5, 40.0)]),
    ("PTOLEMY", "#9A7A3A", [(21.0, 33.0), (25.0, 32.0), (32.5, 31.5), (35.5, 33.5), (35.0, 29.5), (34.0, 24.0), (31.0, 22.0), (25.0, 22.0), (20.0, 28.0)]),
    ("SELEUCUS", "#4A6A8A", [(35.8, 37.5), (40.0, 38.0), (45.0, 39.0), (50.0, 38.0), (56.0, 38.5), (62.0, 40.0), (68.0, 40.5), (71.0, 37.0),
                             (70.0, 31.0), (65.0, 26.0), (58.0, 25.5), (52.0, 27.5), (48.0, 30.0), (44.0, 30.5), (38.5, 33.0)]),
]

SEA, LAND, LAND_HI, INK, GOLD = "#1A2329", "#B7A07A", "#D8C49A", "#2A2018", "#E8C878"


def map_base(c, view, t, dim=0.0):
    img = map_raster()
    iw, ih = img.width(), img.height()
    ppd = iw / (R_LON1 - R_LON0)
    clon, clat, span = view
    vw = span; vh = span * H / W
    src = skia.Rect.MakeXYWH((clon - vw / 2 - R_LON0) * ppd, (R_LAT1 - (clat + vh / 2)) * ppd, vw * ppd, vh * ppd)
    c.drawRect(skia.Rect.MakeWH(W, H), P("#0E1418"))
    c.drawImageRect(img, src, skia.Rect.MakeWH(W, H), SAMP, skia.Paint(AntiAlias=True))
    if dim:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 255 * dim))


def map_label(c, view, lon, lat, text_, a, size=48, dot=False, italic=False):
    """Tên địa danh trên bản đồ: chữ có chân, giãn cách, bóng mờ; điểm tròn nhỏ nếu là thành phố."""
    if a <= 0:
        return
    x, y = lonlat(lon, lat, view)
    s_ = 1.0 + 0.08 * (1 - ease(a))
    if dot:
        c.drawCircle(x, y, 9, P("#000000", 160 * a, blur=4)); c.drawCircle(x, y, 7, P("#F6E7C4", 255 * a))
        y -= size * 0.55
    c.save(); c.translate(x, y); c.scale(s_, s_)
    draw_text(c, text_, 0, size * 0.35, "serif_i" if italic else "serif_b", size, "#FFF6E2", a=255 * a, spacing=size * 0.1)
    c.restore()


def region_glow(c, view, key, a, color=GOLD, label=True, size=34):
    if a <= 0:
        return
    (lon, lat), r, name = REGIONS[key]
    x, y = lonlat(lon, lat, view)
    rr = r * W / view[2]
    c.drawCircle(x, y, rr, P(color, 95 * a, blur=rr * 0.5))
    if label:
        draw_text(c, name, x, y + size * 0.35, "serif_b", size, "#FFF4DC", a=255 * a, spacing=size * 0.12)


def city_dot(c, view, name, a=1.0, label=True, size=26, right=True):
    if a <= 0:
        return
    x, y = lonlat(*CITIES[name], view)
    c.drawCircle(x, y, 7, P("#1A120A", 255 * a)); c.drawCircle(x, y, 5, P("#F2E2B8", 255 * a))
    if label:
        draw_text(c, CITY_VN.get(name, name), x + (14 if right else -14), y - 10, "serif_i", size, "#2A1A0E", a=255 * a,
                  align="left" if right else "right", shadow=False)


def route_path(view, names, upto):
    pts = [lonlat(*CITIES[n], view) for n in names]
    seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    total = sum(seg); target = total * clamp(upto)
    p = skia.Path(); p.moveTo(*pts[0]); acc = 0.0; head = pts[0]
    for i, L in enumerate(seg):
        if acc + L <= target:
            p.lineTo(*pts[i + 1]); acc += L; head = pts[i + 1]
        else:
            f = (target - acc) / L if L else 0
            head = (lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f))
            p.lineTo(*head); break
    return p, head


def draw_route(c, view, names, upto, color=GOLD, width=5):
    p, head = route_path(view, names, upto)
    c.drawPath(p, P("#000000", 120, stroke=width + 5, blur=4))
    pe = P(color, 240, stroke=width)
    c.drawPath(p, pe)
    if 0 < upto < 1:
        c.drawCircle(head[0], head[1], 11, P(color, 120, blur=10)); c.drawCircle(head[0], head[1], 6, P("#FFF6DC"))


def kingdoms(c, view, a):
    for i, (name, colr, poly) in enumerate(KINGDOMS):
        ai = ease((a * 1.6) - i * 0.25)
        if ai <= 0:
            continue
        p = skia.Path()
        for j, (lon, lat) in enumerate(poly):
            x, y = lonlat(lon, lat, view)
            (p.moveTo if j == 0 else p.lineTo)(x, y)
        p.close()
        c.drawPath(p, P(colr, 150 * ai))
        c.drawPath(p, P("#F2E2B8", 200 * ai, stroke=3))
        cx = sum(q[0] for q in poly) / len(poly); cy = sum(q[1] for q in poly) / len(poly)
        x, y = lonlat(cx, cy, view)
        draw_text(c, name, x, y, "serif_b", 30, "#FFF4DC", a=255 * ai, spacing=4)


def empire_tint(c, view, a):
    if a <= 0:
        return
    for key in ("Egypt", "Syria", "Mesopotamia", "Persia", "Media", "Bactria", "India", "Gedrosia", "Phrygia", "Lydia", "Ionia"):
        (lon, lat), r, _ = REGIONS[key]
        x, y = lonlat(lon, lat, view); rr = r * W / view[2] * 1.3
        c.drawCircle(x, y, rr, P("#C8803A", 70 * a, blur=rr * 0.6))


def view_lerp(v0, v1, q):
    return (lerp(v0[0], v1[0], q), lerp(v0[1], v1[1], q), lerp(v0[2], v1[2], q))


# ---------------------------------------------------------------- lớp hoàn thiện
@lru_cache(None)
def _vignette():
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    a = np.clip((d - 0.55) / 0.6, 0, 1) ** 1.6 * 170
    rgba = np.zeros((H, W, 4), np.uint8); rgba[..., 3] = a.astype(np.uint8)
    return skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)


@lru_cache(None)
def _grain(k):
    rng = np.random.default_rng(k)
    g = rng.normal(0, 1, (H // 2, W // 2))
    v = np.clip(128 + g * 22, 0, 255).astype(np.uint8)
    rgba = np.dstack([v, v, v, np.full_like(v, 16)])
    return skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)


def finish(c, t):
    c.drawImage(_vignette(), 0, 0)
    c.drawImageRect(_grain(int(t * 12) % 6), skia.Rect.MakeWH(W, H), SAMP, skia.Paint())


def subtitle(c, t, align, off, until):
    if t >= until:
        return
    tv = t - off
    for a, b, s in align:
        if a <= tv < b:
            al = 255 * clamp(min(tv - a, b - tv) / 0.18)
            words, lines, cur = s.split(), [], ""
            for w_ in words:
                tst = (cur + " " + w_).strip()
                if text_w(tst, "sans_m", 38) > 1480 and cur:
                    lines.append(cur); cur = w_
                else:
                    cur = tst
            lines.append(cur)
            y0 = H - 62 - 50 * (len(lines) - 1)
            for i, l in enumerate(lines):
                draw_text(c, l, W / 2, y0 + i * 50, "sans_m", 38, "#F6F0E4", a=al)
            return
