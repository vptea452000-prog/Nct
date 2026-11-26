"""Kịch bản hình — Adolf Hitler. Theo quy tắc đã chốt:
  · bản đồ thật (NASA Blue Marble), không kẻ đường, chỉ hiện tên đúng lúc được nhắc;
  · chữ lớn ở năm, tên riêng, địa danh, con số;
  · mỗi ảnh camera zoom dứt khoát một hướng, đều tay.
Giây trong danh sách = giây giọng đọc; video = giọng + OFF.
"""
import json, re, unicodedata
from doc import *  # noqa

OFF = 4.5
ALIGN = json.load(open(ROOT / "audio" / "voice_align.json"))
WORDS = json.load(open(ROOT / "audio" / "voice_words.json"))
VEND = 435.62
DUR = OFF + VEND + 1.5


def _norm(w):
    return re.sub(r"[^\wÀ-ỹ]", "", unicodedata.normalize("NFC", w.lower()))


NW = [(t, _norm(w)) for t, w in WORDS]


def when(phrase, after=0.0):
    toks = [_norm(x) for x in phrase.split()]
    for i in range(len(NW) - len(toks) + 1):
        if NW[i][0] >= after and all(NW[i + j][1] == toks[j] for j in range(len(toks))):
            return NW[i][0]
    raise KeyError(phrase)


def KB(code, cx=0.5, cy=0.5, mode="in", base=1.0, amt=0.18, dim=0.0):
    """Một hướng zoom duy nhất. base < 1 → ảnh nhỏ đặt giữa nền mờ (không phóng vỡ hạt)."""
    z0, z1 = (base, base + amt) if mode == "in" else (base + amt, base)

    def f(c, t, a, b):
        ken_burns(c, code, clamp((t - a) / (b - a)), (cx, cy, z0), (cx, cy, z1), dim=dim)
    return f


# ---------------------------------------------------------------- chữ lớn
KEYWORDS = [  # (cụm từ trong lời, chữ lớn, dòng phụ, tìm sau giây)
    ("năm 1907", "1907", "Vienna, Áo – Hung", 0),
    ("20 tháng 4 năm 1889", "20 · 4 · 1889", "Braunau am Inn", 28),
    ("Alois", "ALOIS HITLER", "người cha", 37),
    ("bà Klara", "KLARA HITLER", "người mẹ", 42),
    ("Năm 1913", "MUNICH · 1913", None, 89),
    ("Thế chiến thứ nhất", "THẾ CHIẾN I", "1914", 96),
    ("tháng 10 năm 1918", "10 · 1918", "mù tạm thời vì khí độc", 108),
    ("Huân chương", "THẬP TỰ SẮT", "hạng Nhất", 115),
    ("Hiệp ước Versailles", "VERSAILLES", "1919", 131),
    ("năm 1919", "1919", "Đảng Công nhân Đức", 145),
    ("Đảng Quốc xã", "ĐẢNG QUỐC XÃ", "NSDAP · 1920", 156),
    ("tháng 11 năm 1923", "11 · 1923", "Đảo chính Nhà hàng Bia", 178),
    ("năm năm tù", "5 NĂM TÙ", None, 189),
    ("Landsberg", "LANDSBERG", "chưa đầy 9 tháng", 194),
    ("Mein Kampf", "MEIN KAMPF", "“Cuộc đấu tranh của tôi”", 198),
    ("Năm 1929", "1929", "Đại khủng hoảng", 229),
    ("năm 1932", "1932", "đảng lớn nhất quốc hội", 244),
    ("Ngày 30 tháng 1 năm 1933", "30 · 1 · 1933", "Hitler làm Thủ tướng", 251),
    ("Đạo luật Ủy quyền", "ĐẠO LUẬT ỦY QUYỀN", "3 · 1933", 268),
    ("Ernst Röhm", "ERNST RÖHM", "Đêm của những con dao dài · 1934", 283),
    ("Quốc trưởng", "QUỐC TRƯỞNG", "Führer", 290),
    ("Năm 1935", "LUẬT NUREMBERG", "1935", 301),
    ("Đêm pha lê", "ĐÊM PHA LÊ", "11 · 1938", 305),
    ("Ngày 1 tháng 9 năm 1939", "1 · 9 · 1939", None, 327),
    ("Thế chiến thứ hai", "THẾ CHIẾN II", None, 331),
    ("sáu triệu", "6.000.000", "người Do Thái bị sát hại", 359),
    ("năm 1943", "1943", None, 373),
    ("mùa xuân năm 1945", "BERLIN · 1945", None, 384),
    ("Eva Braun", "EVA BRAUN", "29 · 4 · 1945", 393),
    ("ngày 30 tháng 4", "30 · 4 · 1945", None, 398),
    ("bảy mươi triệu", "70.000.000+", "người thiệt mạng", 413),
]
KW = sorted([(when(p, after=a), big, sub) for p, big, sub, a in KEYWORDS])


def keyword_overlay(c, tv, suppress):
    if suppress:
        return
    for t0, big, sub in reversed(KW):
        if t0 - 0.05 <= tv < t0 + 2.0:
            q = (tv - t0) / 2.0
            al = ease(q / 0.12) * ease((1 - q) / 0.18)
            c.drawCircle(W / 2, H * 0.44, 720, P("#000000", 120 * al, blur=170))
            s_ = 1.0 + 0.05 * (1 - ease(q / 0.25))
            size = 128 if len(big) < 14 else 100
            c.save(); c.translate(W / 2, H * 0.44); c.scale(s_, s_)
            draw_text(c, big, 0, 46, "serif", size, "#FFF6E2", a=255 * al, spacing=14)
            wl = text_w(big, "serif", size) / 2 + len(big) * 7
            c.drawLine(-wl * ease(q / 0.3), 84, wl * ease(q / 0.3), 84, P("#D8B66A", 220 * al, stroke=2.5))
            if sub:
                draw_text(c, sub, 0, 136, "serif_i", 42, "#E2C27E", a=230 * al)
            c.restore()
            return


# ---------------------------------------------------------------- bản đồ thật
def map_scene(v0, v1, labels):
    """labels: (lon, lat, chữ, cụm từ kích hoạt | giây tương đối, cỡ, là_thành_phố)."""
    def f(c, t, a, b):
        v = view_lerp(v0, v1, clamp((t - a) / (b - a)))
        map_base(c, v, t)
        tv, av = t - OFF, a - OFF
        for lon, lat, txt, trig, size, dot in labels:
            t0 = (av + trig) if isinstance(trig, (int, float)) else when(trig, after=av - 0.5)
            map_label(c, v, lon, lat, txt, ease((tv - t0) / 0.45), size=size, dot=dot, italic=dot)
    f.is_map = True
    return f


GER = (10.4, 51.2)
MAPS = {
    "braunau": map_scene((12.5, 49.0, 24.0), (13.0, 48.6, 17.0), [
        (*GER, "ĐỨC", 0.3, 56, False), (15.2, 47.4, "ÁO – HUNG", 0.9, 50, False), (13.03, 48.26, "Braunau am Inn", 1.8, 40, True)]),
    "lebensraum": map_scene((20.0, 52.0, 30.0), (24.0, 52.5, 38.0), [
        (*GER, "ĐỨC", 0.2, 54, False), (30.0, 54.5, "“KHÔNG GIAN SINH TỒN”", "không gian sinh tồn", 54, False),
        (31.0, 51.8, "phía Đông", "phía Đông", 40, True)]),
    "expand": map_scene((14.0, 49.5, 18.0), (14.5, 49.2, 14.0), [
        (*GER, "ĐỨC", 0.2, 52, False), (14.6, 47.5, "ÁO", "sáp nhập Áo", 56, False),
        (14.2, 50.7, "SUDETENLAND", "Sudetenland", 40, False), (17.6, 49.2, "TIỆP KHẮC", "Tiệp Khắc", 40, False)]),
    "conquest": map_scene((9.0, 53.0, 30.0), (8.0, 53.0, 36.0), [
        (19.5, 52.0, "BA LAN", "Ba Lan", 50, False), (9.5, 61.0, "NA UY", "Na Uy", 50, False),
        (5.6, 52.4, "HÀ LAN", "Hà Lan", 40, False), (4.6, 50.6, "BỈ", "Bỉ", 40, False), (2.4, 47.0, "PHÁP", "Pháp", 60, False)]),
    "barbarossa": map_scene((24.0, 52.0, 34.0), (28.0, 53.0, 42.0), [
        (*GER, "ĐỨC", 0.2, 46, False), (40.0, 56.0, "LIÊN XÔ", "Liên Xô", 66, False),
        (37.6, 55.75, "Moskva", "Liên Xô", 36, True), (28.0, 50.5, "BARBAROSSA", "Barbarossa", 46, False)]),
    "stalingrad": map_scene((38.0, 51.0, 30.0), (42.0, 49.5, 22.0), [(44.5, 48.7, "Stalingrad", "Stalingrad", 48, True)]),
    "allies": map_scene((6.0, 47.0, 26.0), (6.0, 47.0, 22.0), [
        (12.8, 42.6, "Ý", "Ý", 56, False), (-0.6, 49.3, "Normandy", "Normandy", 44, True), (2.4, 47.0, "PHÁP", "Pháp", 44, False)]),
}


# ---------------------------------------------------------------- cảnh đặc biệt
def intro(c, t, a, b):
    q = clamp(t / OFF)
    ken_burns(c, "K03b", q, (0.5, 0.48, 1.0), (0.5, 0.48, 1.18))
    c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 255 * (1 - ease(t / 1.5)) * 0.85 + 80))
    al = ease((t - 0.9) / 0.8) * ease((OFF + 0.3 - t) / 0.7)
    draw_text(c, "CHÀNG HỌA SĨ BỊ TỪ CHỐI", W / 2, H / 2 + 10, "serif", 92, "#F6EBD2", a=255 * al, spacing=10)
    c.drawLine(W / 2 - 330 * al, H / 2 + 50, W / 2 + 330 * al, H / 2 + 50, P("#D8B66A", 220 * al, stroke=2))
    draw_text(c, "VIENNA · 1907", W / 2, H / 2 + 108, "serif", 36, "#E2C27E", a=230 * al, spacing=8)


def reveal(c, t, a, b):
    """'Tên của anh là Adolf Hitler.' — cắt cứng vào chân dung, tên hiện lớn."""
    ken_burns(c, "K04", clamp((t - a) / (b - a + 2)), (0.5, 0.36, 1.05), (0.5, 0.36, 1.2), dim=0.25)
    t0 = when("Adolf Hitler", after=26) + OFF
    al = ease((t - t0) / 0.25)
    draw_text(c, "ADOLF HITLER", W / 2, H * 0.80, "serif", 140, "#FFF6E2", a=255 * al, spacing=18)
    if 0 <= t - t0 < 0.12:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#FFF4DC", 120 * (1 - (t - t0) / 0.12)))


def finale(c, t, a, b):
    q = clamp((t - a) / (b - a))
    ken_burns(c, "K03b", q, (0.5, 0.48, 1.3), (0.5, 0.48, 1.0), dim=0.2 + 0.55 * ease((q - 0.55) / 0.45))
    al = ease((q - 0.62) / 0.15) * ease((b - t) / 1.2)
    draw_text(c, "ADOLF HITLER", W / 2, H / 2 - 10, "serif", 86, "#F6EBD2", a=255 * al, spacing=12)
    draw_text(c, "1889 – 1945", W / 2, H / 2 + 64, "serif", 40, "#E2C27E", a=230 * al, spacing=8)


# ---------------------------------------------------------------- danh sách cảnh
S = [
    (0.00, 6.00, KB("K01", 0.5, 0.45, "in", 1.0, 0.18)),
    (6.00, 11.50, KB("K02", 0.5, 0.42, "out", 1.0, 0.2)),
    (11.50, 16.66, KB("K03a", 0.5, 0.5, "in", 1.0, 0.2)),
    (16.66, 20.50, KB("K11", 0.5, 0.5, "out", 1.0, 0.18)),
    (20.50, 26.79, KB("K01", 0.4, 0.4, "in", 1.25, 0.3, dim=0.25)),
    (26.79, 28.95, reveal),
    (28.95, 33.20, KB("K05b", 0.5, 0.35, "in", 1.0, 0.15)),
    (33.20, 37.70, MAPS["braunau"]),
    (37.70, 42.44, KB("K06", 0.5, 0.25, "in", 1.0, 0.25)),
    (42.44, 47.76, KB("K07", 0.5, 0.4, "out", 1.0, 0.18)),
    (47.76, 54.86, KB("K08", 0.5, 0.3, "in", 1.0, 0.3)),
    (54.86, 59.32, KB("K03b", 0.6, 0.5, "out", 1.0, 0.25)),
    (59.32, 64.65, KB("K09", 0.5, 0.55, "in", 1.0, 0.25)),
    (64.65, 70.00, KB("K10", 0.5, 0.45, "out", 1.0, 0.2)),
    (70.00, 75.53, KB("K11", 0.5, 0.45, "in", 1.0, 0.25)),
    (75.53, 83.24, KB("K12", 0.5, 0.35, "in", 0.85, 0.12)),
    (83.24, 90.06, KB("K04", 0.5, 0.33, "out", 1.1, 0.25, dim=0.2)),
    (90.06, 96.58, KB("K13", 0.5, 0.5, "in", 1.0, 0.2)),
    (96.58, 99.60, KB("K14", 0.5, 0.5, "in", 0.92, 0.08)),
    (99.60, 101.89, KB("K14b", 0.5, 0.5, "out", 1.0, 0.15)),
    (101.89, 104.90, KB("K15a", 0.5, 0.45, "in", 1.0, 0.15)),
    (104.90, 108.14, KB("K15b", 0.5, 0.5, "out", 1.0, 0.18)),
    (108.14, 115.90, KB("K16", 0.5, 0.5, "in", 1.0, 0.22)),
    (115.90, 123.78, KB("K17", 0.5, 0.5, "out", 1.0, 0.2)),
    (123.78, 131.30, KB("K18", 0.5, 0.5, "in", 1.0, 0.2, dim=0.1)),
    (131.30, 139.28, KB("K19", 0.5, 0.65, "in", 1.0, 0.3)),
    (139.28, 145.63, KB("K20", 0.5, 0.5, "out", 1.0, 0.2)),
    (145.63, 150.50, KB("K13", 0.5, 0.6, "out", 1.3, 0.25, dim=0.1)),
    (150.50, 156.05, KB("K21", 0.5, 0.5, "in", 0.95, 0.12)),
    (156.05, 163.61, KB("K23", 0.5, 0.5, "in", 1.0, 0.25)),
    (163.61, 171.14, KB("K22a", 0.5, 0.35, "in", 1.0, 0.2)),
    (171.14, 178.62, KB("K24b", 0.5, 0.5, "out", 1.0, 0.25)),
    (178.62, 189.26, KB("K24a", 0.5, 0.45, "in", 1.0, 0.25)),
    (189.26, 194.35, KB("K25", 0.5, 0.45, "out", 1.0, 0.2)),
    (194.35, 198.20, KB("K26", 0.5, 0.45, "in", 1.0, 0.2)),
    (198.20, 204.75, KB("K27", 0.5, 0.5, "in", 1.0, 0.25)),
    (204.75, 215.08, MAPS["lebensraum"]),
    (215.08, 221.24, KB("K04", 0.5, 0.33, "in", 1.0, 0.2, dim=0.1)),
    (221.24, 227.71, KB("K29", 0.5, 0.5, "out", 1.0, 0.25)),
    (227.71, 233.50, KB("K30", 0.5, 0.45, "in", 0.95, 0.15)),
    (233.50, 239.75, KB("K31a", 0.5, 0.5, "out", 1.0, 0.2)),
    (239.75, 244.32, KB("K32", 0.5, 0.35, "in", 1.0, 0.2)),
    (244.32, 251.57, KB("K33", 0.5, 0.5, "out", 1.0, 0.2)),
    (251.57, 254.60, KB("K34b", 0.5, 0.28, "in", 1.0, 0.15)),
    (254.60, 257.35, KB("K34a", 0.45, 0.5, "in", 1.0, 0.15)),
    (257.35, 261.38, KB("K36", 0.5, 0.45, "in", 1.0, 0.2)),
    (261.38, 268.50, KB("K35", 0.5, 0.5, "out", 1.0, 0.2)),
    (268.50, 275.03, KB("K37", 0.5, 0.45, "in", 1.0, 0.25)),
    (275.03, 283.01, KB("K31b", 0.5, 0.5, "out", 1.0, 0.2, dim=0.15)),
    (283.01, 290.45, KB("K38", 0.6, 0.35, "in", 1.0, 0.25)),
    (290.45, 298.11, KB("K39", 0.5, 0.55, "in", 1.0, 0.3)),
    (298.11, 301.63, KB("K24b", 0.4, 0.55, "in", 1.2, 0.2, dim=0.25)),
    (301.63, 305.68, KB("K40", 0.5, 0.45, "in", 1.0, 0.2)),
    (305.68, 311.50, KB("K41a", 0.5, 0.5, "in", 1.0, 0.2)),
    (311.50, 316.57, KB("K41b", 0.5, 0.45, "out", 1.0, 0.18)),
    (316.57, 318.52, KB("K42", 0.5, 0.45, "in", 1.0, 0.12)),
    (318.52, 323.00, MAPS["expand"]),
    (323.00, 327.27, KB("K43a", 0.5, 0.45, "out", 1.0, 0.2)),
    (327.27, 331.26, KB("K44", 0.5, 0.5, "in", 1.0, 0.25)),
    (331.26, 336.25, KB("K45", 0.5, 0.45, "out", 1.0, 0.25)),
    (336.25, 339.06, KB("K46", 0.5, 0.5, "in", 1.0, 0.2)),
    (339.06, 344.15, MAPS["conquest"]),
    (344.15, 350.62, MAPS["barbarossa"]),
    (350.62, 354.08, KB("K49", 0.5, 0.5, "in", 1.0, 0.2)),
    (354.08, 359.12, KB("K50", 0.5, 0.55, "in", 1.0, 0.15, dim=0.1)),
    (359.12, 363.00, KB("K51", 0.5, 0.5, "in", 1.0, 0.15)),
    (363.00, 366.94, KB("K52a", 0.5, 0.5, "out", 1.0, 0.15)),
    (366.94, 373.44, KB("K53", 0.5, 0.4, "in", 1.0, 0.15)),
    (373.44, 376.87, KB("K54a", 0.5, 0.5, "out", 1.0, 0.2)),
    (376.87, 381.09, MAPS["stalingrad"]),
    (381.09, 384.60, MAPS["allies"]),
    (384.60, 389.17, KB("K56b", 0.5, 0.45, "in", 1.0, 0.2)),
    (389.17, 393.38, KB("K57", 0.5, 0.5, "in", 1.0, 0.2, dim=0.15)),
    (393.38, 398.43, KB("K58", 0.5, 0.4, "in", 1.0, 0.18)),
    (398.43, 405.34, KB("K59", 0.5, 0.35, "in", 1.0, 0.25)),
    (405.34, 408.57, KB("K60", 0.5, 0.5, "out", 1.0, 0.15, dim=0.15)),
    (408.57, 413.38, KB("K56a", 0.5, 0.5, "in", 1.0, 0.2)),
    (413.38, 418.46, KB("K61", 0.5, 0.5, "out", 1.0, 0.2)),
    (418.46, 423.60, KB("K61b", 0.5, 0.5, "in", 1.0, 0.2, dim=0.1)),
    (423.60, VEND + 1.5, finale),
]
HARD_CUT = {26.79, 327.27}
BUSY = {reveal, finale}


def draw(c, t):
    tv = t - OFF
    if tv < 0:
        intro(c, t, 0.0, OFF)
        return
    for i, (a, b, fn) in enumerate(S):
        if a <= tv < b or (i == len(S) - 1 and tv >= a):
            fn(c, t, a + OFF, b + OFF)
            if i > 0 and a not in HARD_CUT and tv - a < 0.4:
                pa, pb, pf = S[i - 1]
                c.saveLayerAlpha(None, int(255 * (1 - ease((tv - a) / 0.4))))
                pf(c, t, pa + OFF, pb + OFF)
                c.restore()
            elif i == 0 and tv < 0.4:
                c.saveLayerAlpha(None, int(255 * (1 - ease(tv / 0.4))))
                intro(c, t, 0, OFF)
                c.restore()
            keyword_overlay(c, tv, getattr(fn, "is_map", False) or fn in BUSY)
            return
