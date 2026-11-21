"""Kịch bản hình v2 — theo góp ý chủ kênh:
  · bản đồ thật (ảnh vệ tinh Blue Marble của NASA), không kẻ đường nối, chỉ hiện tên địa danh đúng lúc được nhắc;
  · chữ lớn khi có từ quan trọng (năm, tên riêng, địa điểm, con số);
  · mỗi ảnh camera chỉ zoom một hướng (vào hoặc ra), đều tay, không lia qua lại.
Giây trong danh sách = giây của giọng đọc; video = giọng + OFF.
"""
import json, re, unicodedata
from doc import *  # noqa

OFF = 4.5
ALIGN = json.load(open(ROOT / "audio" / "voice_align.json"))
WORDS = json.load(open(ROOT / "audio" / "voice_words.json"))
DUR = OFF + 387.71 + 1.5


def _norm(w):
    w = unicodedata.normalize("NFC", w.lower())
    return re.sub(r"[^\wÀ-ỹ]", "", w)


NW = [(t, _norm(w)) for t, w in WORDS]


def when(phrase, after=0.0):
    """Thời điểm (giây giọng đọc) bắt đầu cụm từ, lần xuất hiện đầu tiên sau `after`."""
    toks = [_norm(x) for x in phrase.split()]
    for i in range(len(NW) - len(toks) + 1):
        if NW[i][0] >= after and all(NW[i + j][1] == toks[j] for j in range(len(toks))):
            return NW[i][0]
    raise KeyError(phrase)


# ---------------------------------------------------------------- ảnh: zoom một hướng
def KB(code, cx, cy, mode="in", base=1.0, amt=0.20, dim=0.0):
    z0, z1 = (base, base + amt) if mode == "in" else (base + amt, base)

    def f(c, t, a, b):
        ken_burns(c, code, clamp((t - a) / (b - a)), (cx, cy, z0), (cx, cy, z1), dim=dim)
    return f


# ---------------------------------------------------------------- chữ lớn cho từ khóa
KEYWORDS = [  # (cụm từ trong lời đọc, chữ hiển thị, dòng phụ, sau giây)
    ("năm 324", "324 TCN", None, 0),
    ("Opis", "OPIS", "bên bờ sông Tigris", 0),
    ("mười năm", "10 NĂM", None, 9),
    ("vua Alexander", "ALEXANDER", None, 9),
    ("vua Philip", "VUA PHILIP II", "cha của Alexander", 80),
    ("Hellespont", "HELLESPONT", None, 140),
    ("vua Darius", "VUA DARIUS III", None, 148),
    ("Ai Cập", "AI CẬP", None, 155),
    ("Ấn Độ", "ẤN ĐỘ", None, 165),
    ("Dionysus", "DIONYSUS", None, 270),
    ("hai ngày", "2 NGÀY", None, 293),
    ("ngày thứ ba", "NGÀY THỨ BA", None, 298),
    ("năm 323", "323 TCN", None, 360),
    ("Babylon", "BABYLON", None, 362),
    ("ba mươi hai tuổi", "32 TUỔI", None, 362),
]
KW = sorted([(when(p, after=a), big, sub) for p, big, sub, a in KEYWORDS])


def keyword_overlay(c, tv, suppress):
    for t0, big, sub in KW:
        if t0 - 0.05 <= tv < t0 + 1.9 and not suppress:
            q = (tv - t0) / 1.9
            al = ease(q / 0.12) * ease((1 - q) / 0.18)
            c.drawCircle(W / 2, H * 0.44, 700, P("#000000", 110 * al, blur=160))
            s_ = 1.0 + 0.05 * (1 - ease(q / 0.25))
            c.save(); c.translate(W / 2, H * 0.44); c.scale(s_, s_)
            draw_text(c, big, 0, 46, "serif", 128, "#FFF6E2", a=255 * al, spacing=14)
            wl = text_w(big, "serif", 128) / 2 + len(big) * 7
            c.drawLine(-wl * ease(q / 0.3), 84, wl * ease(q / 0.3), 84, P("#E8C878", 220 * al, stroke=2.5))
            if sub:
                draw_text(c, sub, 0, 136, "serif_i", 42, "#E8C878", a=230 * al)
            c.restore()
            return


# ---------------------------------------------------------------- bản đồ thật: chỉ hiện tên đúng lúc
def map_scene(v0, v1, labels, kingdoms_=False):
    """labels: (lon, lat, chữ, cụm từ kích hoạt hoặc số giây tương đối, cỡ, là_thành_phố)."""
    resolved = []
    for lon, lat, txt, trig, size, dot in labels:
        resolved.append((lon, lat, txt, trig, size, dot))

    def f(c, t, a, b):
        q = clamp((t - a) / (b - a))
        v = view_lerp(v0, v1, q)                 # một hướng, đều tay
        map_base(c, v, t)
        tv = t - OFF; av = a - OFF
        if kingdoms_:
            kingdom_tints(c, v, ease((tv - av - 0.8) / 1.5))
        for lon, lat, txt, trig, size, dot in resolved:
            t0 = (av + trig) if isinstance(trig, (int, float)) else when(trig, after=av - 0.5)
            map_label(c, v, lon, lat, txt, ease((tv - t0) / 0.45), size=size, dot=dot, italic=dot)
    f.is_map = True
    return f


def kingdom_tints(c, v, a):
    if a <= 0:
        return
    for name, colr, poly in KINGDOMS:
        p = skia.Path()
        for j, (lon, lat) in enumerate(poly):
            x, y = lonlat(lon, lat, v)
            (p.moveTo if j == 0 else p.lineTo)(x, y)
        p.close()
        c.drawPath(p, P(colr, 95 * a)); c.drawPath(p, P("#F2E2B8", 120 * a, stroke=2))


V_ALL = (48.0, 31.5, 62.0)
V_GREECE = (25.5, 39.8, 22.0)

MAPS = {
    "macedonia": map_scene((25.5, 40.0, 30.0), V_GREECE, [(22.4, 40.9, "MACEDONIA", "Macedonia", 60, False)]),
    "journey": map_scene((44.0, 33.0, 52.0), V_ALL, [
        (22.4, 40.9, "MACEDONIA", 0.2, 46, False), (30.5, 27.0, "AI CẬP", 1.6, 46, False), (44.4, 32.5, "Babylon", 2.6, 38, True),
        (52.9, 29.9, "Persepolis", 3.6, 38, True), (67.0, 37.5, "BACTRIA", 4.6, 46, False), (71.5, 29.0, "ẤN ĐỘ", 5.6, 46, False),
        (53.0, 33.5, "ĐẾ CHẾ BA TƯ", "Ba Tư", 64, False)]),
    "philip": map_scene(V_GREECE, (25.0, 40.4, 18.0), [
        (22.4, 40.9, "MACEDONIA", 0.0, 50, False), (26.2, 41.9, "THRACE", "Thrace", 54, False), (22.2, 39.5, "THESSALY", "Thessaly", 50, False)]),
    "athens": map_scene((23.6, 38.6, 12.0), (23.6, 38.6, 10.0), [
        (23.73, 37.98, "Athens", "Athens", 46, True), (23.32, 38.32, "Thebes", "Thebes", 46, True)]),
    "to_asia": map_scene((24.5, 39.5, 22.0), V_ALL, [(24.0, 39.0, "HY LẠP", 0.5, 46, False), (53.0, 33.0, "CHÂU Á", 4.5, 70, False)]),
    "asia_minor": map_scene((30.0, 38.8, 18.0), (30.0, 38.8, 15.0), [
        (27.0, 38.2, "IONIA", "Ionia", 46, False), (31.8, 39.4, "PHRYGIA", "Phrygia", 46, False), (28.8, 38.8, "LYDIA", "Lydia", 46, False)]),
    "levant": map_scene((40.0, 33.0, 24.0), (41.0, 32.8, 20.0), [
        (37.6, 35.2, "SYRIA", "Syria", 46, False), (35.0, 31.5, "PALESTINE", "Palestine", 42, False),
        (43.6, 34.2, "LƯỠNG HÀ", "Lưỡng Hà", 46, False), (44.42, 32.54, "Babylon", "Babylon", 40, True)]),
    "conquests": map_scene((55.0, 33.0, 56.0), (55.0, 33.0, 48.0), [
        (53.5, 30.0, "BA TƯ", "Ba Tư", 52, False), (48.8, 35.4, "MEDIA", "Media", 48, False), (67.0, 37.0, "BACTRIA", "Bactria", 48, False),
        (64.0, 43.5, "SCYTHIA", "Scythia", 48, False), (69.5, 35.2, "HINDU KUSH", "Hindu Kush", 44, False),
        (71.5, 28.5, "SÔNG INDUS", "sông Indus", 46, False), (62.5, 26.3, "GEDROSIA", "Gedrosia", 48, False)]),
    "veterans": map_scene((36.0, 37.0, 32.0), (34.0, 38.0, 36.0), [
        (44.4, 33.9, "Opis", 0.2, 42, True), (22.4, 40.9, "MACEDONIA", "quê hương", 54, False)]),
    "divided": map_scene((46.0, 32.0, 58.0), (46.0, 32.0, 64.0), [
        (31.0, 27.0, "PTOLEMY", 1.0, 42, False), (55.0, 34.0, "SELEUCUS", 1.6, 46, False),
        (28.5, 40.6, "LYSIMACHUS", 2.2, 36, False), (21.8, 39.3, "CASSANDER", 2.8, 34, False)], kingdoms_=True),
}


# ---------------------------------------------------------------- cảnh đặc biệt
def title_block(c, al):
    draw_text(c, "BÀI DIỄN VĂN Ở OPIS", W / 2, H / 2 + 10, "serif", 96, "#F6EBD2", a=255 * al, spacing=10)
    c.drawLine(W / 2 - 320 * al, H / 2 + 50, W / 2 + 320 * al, H / 2 + 50, P("#E8C878", 220 * al, stroke=2))
    draw_text(c, "ALEXANDER ĐẠI ĐẾ · 324 TCN", W / 2, H / 2 + 108, "serif", 36, "#E8C878", a=230 * al, spacing=8)


def intro(c, t, a, b):
    q = clamp((t - a) / (b - a))
    ken_burns(c, "K14a", q, (0.44, 0.35, 1.35), (0.44, 0.35, 1.75))
    c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 255 * (1 - ease(t / 1.6)) * 0.85 + 70))
    c.drawCircle(W * 0.55, H * 0.42, 420, P("#F6D08A", 60 * ease((t - 0.8) / 1.2), blur=180))
    title_block(c, ease((t - 1.2) / 0.8))


def tigris_open(c, t, a, b):
    ken_burns(c, "K01b", clamp((t - a) / (b - a)), (0.5, 0.52, 1.25), (0.5, 0.52, 1.0))
    al = ease((a + 1.6 - t) / 1.0)
    if al > 0:
        title_block(c, al)


def thirty_k(c, t, a, b):
    ken_burns(c, "K09", clamp((t - a) / (b - a)), (0.5, 0.5, 1.0), (0.5, 0.5, 1.22))
    t0 = when("ba mươi nghìn") + OFF
    al = ease((t - t0) / 0.4) * ease((b - t) / 0.4)
    if al > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 110 * al))
        draw_text(c, "30.000", W / 2, H / 2 + 30, "serif", 170, "#FFF6E2", a=255 * al, spacing=8)
        draw_text(c, "thanh niên Ba Tư được huấn luyện kiểu Macedonia", W / 2, H / 2 + 108, "serif_i", 40, "#E8C878", a=230 * al)


def quote(c, lines, t, a, b, size=60):
    al = ease((t - a - 0.2) / 0.6) * ease((b - t) / 0.5)
    if al <= 0:
        return
    c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 120 * al))
    y0 = H / 2 - (len(lines) - 1) * size * 0.7
    draw_text(c, "“", W / 2, y0 - size * 1.1, "serif", size * 2, "#E8C878", a=200 * al)
    for i, l in enumerate(lines):
        draw_text(c, l, W / 2, y0 + i * size * 1.4, "serif_i", size, "#FBF3E2", a=255 * al)


def speech_quote(c, t, a, b):
    KB("K16a", 0.5, 0.45, "in", 1.0, 0.18, dim=0.15)(c, t, a, b)
    quote(c, ["Các ngươi muốn đi đâu thì cứ việc đi,", "ta sẽ không ngăn cản."], t, 72.29 + OFF, 75.34 + OFF)


def kin_quote(c, t, a, b):
    KB("K11a", 0.32, 0.30, "in", 1.6, 0.2, dim=0.3)(c, t, a, b)
    quote(c, ["Từ giờ trở đi, ta coi tất cả", "các ngươi là họ hàng của ta."], t, a, b)


def climax(c, t, a, b):
    hit = when("đi đi") + OFF
    z = 1.15 + 0.12 * clamp((t - a) / (hit - a)) + (0.35 * ease((t - hit) / 0.25) if t > hit else 0)
    c.save()
    if t > hit:
        k = math.exp(-(t - hit) * 5); c.translate(9 * k * math.sin(t * 70), 7 * k * math.cos(t * 60))
    ken_burns(c, "K16a", 0, (0.5, 0.42, z), (0.5, 0.42, z), dim=0.1)
    c.restore()
    if 0 <= t - hit < 0.12:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#FFF4DC", 150 * (1 - (t - hit) / 0.12)))


def go_card(c, t, a, b):
    c.drawRect(skia.Rect.MakeWH(W, H), P("#000000"))
    al = ease((t - a) / 0.15) * ease((b + 0.8 - t) / 0.6)
    c.save(); c.translate(W / 2, H / 2); s_ = 1.0 + 0.04 * (t - a); c.scale(s_, s_)
    draw_text(c, "ĐI ĐI!", 0, 50, "serif_b", 180, "#F6EBD2", a=255 * al, spacing=14)
    c.restore()


def objects(c, t, a, b):
    objects_row(c, ["K35a", "K35b", "K35c"], a + 0.2, t)
    for i, w in enumerate(["KIẾM", "TÊN", "ĐÁ"]):
        al = ease((t - a - 0.4 - i * 0.9) / 0.6)
        draw_text(c, w, W / 3.4 * (i + 0.7), H - 150, "serif", 46, "#E8C878", a=230 * al, spacing=6)


def finale(c, t, a, b):
    q = clamp((t - a) / (b - a))
    ken_burns(c, "K14a", q, (0.45, 0.38, 1.45), (0.45, 0.38, 1.0), dim=0.25 + 0.5 * ease((q - 0.6) / 0.4))
    al = ease((q - 0.62) / 0.15) * ease((b - t) / 1.2)
    draw_text(c, "ALEXANDER ĐẠI ĐẾ", W / 2, H / 2 - 10, "serif", 86, "#F6EBD2", a=255 * al, spacing=10)
    draw_text(c, "356 – 323 TCN", W / 2, H / 2 + 64, "serif", 40, "#E8C878", a=230 * al, spacing=8)


# ---------------------------------------------------------------- danh sách cảnh (giây giọng đọc) — mỗi ảnh một hướng zoom, xen kẽ vào/ra
S = [
    (0.00, 5.20, tigris_open),
    (5.20, 9.11, KB("K03", 0.5, 0.45, "in")),
    (9.11, 13.01, MAPS["macedonia"]),
    (13.01, 20.60, MAPS["journey"]),
    (20.60, 24.80, KB("K06", 0.5, 0.38, "in", 1.0, 0.25)),
    (24.80, 31.23, KB("K14b", 0.75, 0.40, "out", 1.5, 0.25, dim=0.1)),
    (31.23, 39.80, thirty_k),
    (39.80, 44.19, KB("K11b", 0.72, 0.30, "in", 1.6, 0.25)),
    (44.19, 50.00, KB("K11a", 0.45, 0.32, "out", 1.0, 0.25)),
    (50.00, 54.59, KB("K14a", 0.48, 0.37, "in", 1.1, 0.22)),
    (54.59, 61.21, KB("K13", 0.27, 0.5, "in", 1.05, 0.3)),
    (61.21, 64.98, KB("K14b", 0.45, 0.33, "out", 1.6, 0.3)),
    (64.98, 69.41, KB("K14a", 0.5, 0.39, "in", 1.0, 0.15, dim=0.15)),
    (69.41, 81.91, speech_quote),
    (81.91, 85.66, KB("K18", 0.5, 0.36, "in", 1.0, 0.18)),
    (85.66, 97.24, KB("K19", 0.45, 0.5, "out", 1.0, 0.3)),
    (97.24, 102.60, KB("K20a", 0.5, 0.5, "in")),
    (102.60, 108.05, KB("K20b", 0.5, 0.35, "out", 1.2, 0.3)),
    (108.05, 121.50, MAPS["philip"]),
    (121.50, 125.00, MAPS["athens"]),
    (125.00, 127.94, KB("K23", 0.5, 0.32, "in", 1.05, 0.2)),
    (127.94, 132.30, KB("K24", 0.5, 0.5, "out", 1.0, 0.2)),
    (132.30, 136.62, KB("K18b", 0.5, 0.30, "in", 1.3, 0.3)),
    (136.62, 143.45, MAPS["to_asia"]),
    (143.45, 146.00, KB("K26a", 0.5, 0.45, "in", 1.0, 0.15)),
    (146.00, 148.63, KB("K26b", 0.5, 0.5, "out", 1.0, 0.15)),
    (148.63, 152.50, KB("K27", 0.5, 0.5, "in", 1.0, 0.2)),
    (152.50, 156.44, MAPS["asia_minor"]),
    (156.44, 160.50, KB("K28b", 0.5, 0.5, "out", 1.0, 0.2)),
    (160.50, 164.39, MAPS["levant"]),
    (164.39, 168.50, KB("K30a", 0.5, 0.5, "in", 1.05, 0.3)),
    (168.50, 172.51, KB("K30b", 0.5, 0.48, "out", 1.05, 0.25)),
    (172.51, 177.26, KB("K31", 0.5, 0.33, "in", 1.1, 0.2)),
    (177.26, 183.72, KB("K32", 0.5, 0.53, "in", 1.2, 0.3)),
    (183.72, 189.27, KB("K16b", 0.45, 0.45, "out", 1.0, 0.2, dim=0.1)),
    (189.27, 196.25, KB("K33", 0.45, 0.5, "in", 1.05, 0.2)),
    (196.25, 201.78, KB("K16a", 0.5, 0.42, "in", 1.3, 0.25, dim=0.2)),
    (201.78, 206.50, KB("K34a", 0.5, 0.42, "out", 1.05, 0.25)),
    (206.50, 211.25, KB("K34b", 0.5, 0.5, "in", 1.0, 0.2)),
    (211.25, 218.98, objects),
    (218.98, 226.61, KB("K36", 0.5, 0.5, "out", 1.0, 0.18)),
    (226.61, 234.70, KB("K45c", 0.5, 0.5, "in", 1.0, 0.15)),
    (234.70, 239.86, KB("K37", 0.5, 0.48, "out", 1.1, 0.3)),
    (239.86, 248.24, KB("K38", 0.5, 0.37, "in", 1.1, 0.25)),
    (248.24, 252.78, KB("K39", 0.5, 0.5, "out", 1.0, 0.2)),
    (252.78, 258.27, KB("K14a", 0.45, 0.35, "in", 1.2, 0.2, dim=0.1)),
    (258.27, 262.27, climax),
    (262.27, 282.40, MAPS["conquests"]),
    (282.40, 286.75, KB("K11a", 0.30, 0.29, "in", 2.0, 0.3, dim=0.25)),
    (286.75, 292.20, KB("K16b", 0.45, 0.41, "in", 1.3, 0.3, dim=0.3)),
    (292.20, 293.18, go_card),
    (293.18, 298.28, KB("K45b", 0.5, 0.49, "in", 1.05, 0.15, dim=0.35)),
    (298.28, 303.30, KB("K45a", 0.5, 0.5, "out", 1.0, 0.2)),
    (303.30, 308.31, KB("K09", 0.5, 0.5, "in", 1.0, 0.2)),
    (308.31, 315.00, KB("K14a", 0.66, 0.37, "out", 1.6, 0.25, dim=0.2)),
    (315.00, 321.41, KB("K11b", 0.72, 0.30, "in", 1.6, 0.25, dim=0.15)),
    (321.41, 328.94, KB("K11a", 0.32, 0.29, "in", 1.5, 0.35)),
    (328.94, 335.40, KB("K11b", 0.82, 0.28, "out", 1.9, 0.3)),
    (335.40, 339.28, kin_quote),
    (339.28, 341.00, KB("K11a", 0.4, 0.31, "out", 1.2, 0.1)),
    (341.00, 347.40, KB("K50", 0.5, 0.48, "in", 1.0, 0.18)),
    (347.40, 353.29, KB("K36", 0.45, 0.5, "in", 1.1, 0.2)),
    (353.29, 359.15, MAPS["veterans"]),
    (359.15, 361.42, KB("K16b", 0.45, 0.42, "out", 1.2, 0.1, dim=0.2)),
    (361.42, 368.88, KB("K52a", 0.45, 0.48, "in", 1.0, 0.2)),
    (368.88, 374.48, MAPS["divided"]),
    (374.48, 389.20, finale),
]
HARD_CUT = {258.27, 292.20, 293.18}


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
            busy = getattr(fn, "is_map", False) or fn in (thirty_k, go_card, kin_quote, speech_quote, objects, finale, climax)
            keyword_overlay(c, tv, busy)
            return
