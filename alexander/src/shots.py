"""Kịch bản hình: các cảnh theo mốc câu trong voice (giây của giọng đọc; video = giọng + OFF)."""
import json
from doc import *  # noqa

OFF = 4.5                       # mở đầu 4,5 giây trước khi giọng vào (intro)
ALIGN = json.load(open(ROOT / "audio" / "voice_align.json"))
DUR = OFF + 387.71 + 1.5


def KB(code, r0, r1, dim=0.0):
    def f(c, t, a, b):
        ken_burns(c, code, clamp((t - a) / (b - a)), r0, r1, dim=dim)
    f.kind = "img"
    return f


def label(text_, t, a, b, y=H - 170, size=44, delay=0.6, hold=None):
    """Nhãn địa danh/mốc thời gian: chữ serif giãn cách, có gạch mảnh, hiện rồi tắt êm."""
    end = a + (hold if hold else (b - a)) - 0.2
    al = ease((t - a - delay) / 0.6) * ease((end - t) / 0.6)
    if al <= 0:
        return
    w = text_w(text_, "serif", size) + len(text_) * size * 0.12
    draw_text(None or _c[0], text_, 150, y, "serif", size, "#F2E6CC", a=255 * al, align="left", spacing=size * 0.12)
    _c[0].drawLine(150, y + 22, 150 + w * ease((t - a - delay) / 1.0), y + 22, P("#E8C878", 200 * al, stroke=2))


_c = [None]


def quote(c, text_lines, t, a, b, size=58):
    al = ease((t - a - 0.3) / 0.7) * ease((b - t - 0.1) / 0.5)
    if al <= 0:
        return
    c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 120 * al))
    y0 = H / 2 - (len(text_lines) - 1) * size * 0.7
    draw_text(c, "“", W / 2, y0 - size * 1.1, "serif", size * 2, "#E8C878", a=200 * al)
    for i, l in enumerate(text_lines):
        draw_text(c, l, W / 2, y0 + i * size * 1.4, "serif_i", size, "#FBF3E2", a=255 * al)


# ---------------------------------------------------------------- bản đồ động
V_ALL = (46.0, 33.0, 54.0)          # toàn đế chế
V_GREECE = (25.5, 39.5, 24.0)       # Hy Lạp – Macedonia
V_WEST = (33.0, 34.0, 28.0)         # Tiểu Á – Ai Cập – Lưỡng Hà


def map_journey(c, t, a, b):        # mười năm, từ Macedonia → cả đế chế Ba Tư
    q = (t - a) / (b - a)
    v = view_lerp(V_GREECE, V_ALL, ease(q / 0.35))
    map_base(c, v, t)
    empire_tint(c, v, ease((q - 0.75) / 0.25))
    draw_route(c, v, ROUTE, ease((q - 0.12) / 0.8))
    for n in ("Pella", "Babylon", "Persepolis", "Alexandria", "Bactra", "Taxila", "Opis"):
        city_dot(c, v, n, a=ease((q - 0.05) / 0.2) if n == "Pella" else ease((q - 0.3) / 0.2))
    region_glow(c, v, "Macedonia", ease(q / 0.15) * ease((0.4 - q) / 0.1))


def map_macedonia(c, t, a, b):      # Macedonia, 334 TCN
    q = (t - a) / (b - a)
    v = view_lerp((25.0, 40.0, 32.0), V_GREECE, ease(q))
    map_base(c, v, t)
    region_glow(c, v, "Macedonia", ease(q / 0.4))
    city_dot(c, v, "Pella", ease((q - 0.2) / 0.3))
    label("MACEDONIA · 334 TCN", t, a, b, delay=0.4)


def map_philip(c, t, a, b):         # Thrace, cảng, mỏ → Thessaly
    q = (t - a) / (b - a)
    v = view_lerp(V_GREECE, (25.0, 40.3, 21.0), ease(q))
    map_base(c, v, t)
    region_glow(c, v, "Macedonia", 1.0, label=True, size=30)
    region_glow(c, v, "Thrace", ease((q - 0.05) / 0.2), size=30)
    for k, (lon, lat) in enumerate([(24.4, 40.9), (25.9, 40.85), (23.4, 40.6)]):       # cảng (neo)
        x, y = lonlat(lon, lat, v); al = ease((q - 0.25 - k * 0.06) / 0.15)
        c.drawCircle(x, y, 12, P("#1E2A30", 230 * al)); draw_text(c, "⚓", x, y + 8, "serif", 22, "#F2E2B8", a=255 * al, shadow=False)
    for k, (lon, lat) in enumerate([(24.0, 41.0), (23.0, 41.4)]):                       # mỏ (búa)
        x, y = lonlat(lon, lat, v); al = ease((q - 0.42 - k * 0.06) / 0.15)
        c.drawRect(skia.Rect.MakeXYWH(x - 9, y - 9, 18, 18), P("#C8A040", 240 * al))
    region_glow(c, v, "Thessaly", ease((q - 0.68) / 0.15), color="#D88A4A", size=30)


def map_greece_to_asia(c, t, a, b):  # "chừng ấy vẫn còn nhỏ bé" — kéo từ Hy Lạp ra cả châu Á
    q = (t - a) / (b - a)
    v = view_lerp((24.5, 39.0, 22.0), V_ALL, ease(q))
    map_base(c, v, t)
    region_glow(c, v, "Greece", 1 - ease(q), label=False)
    region_glow(c, v, "Macedonia", 1 - ease(q), label=False)
    empire_tint(c, v, ease((q - 0.5) / 0.5))


def map_asia_minor(c, t, a, b):     # Ionia, Phrygia, Lydia
    q = (t - a) / (b - a)
    v = view_lerp((30.0, 38.8, 24.0), (30.5, 38.6, 22.0), q)
    map_base(c, v, t)
    city_dot(c, v, "Granicus", 1.0); city_dot(c, v, "Sardis", 1.0)
    for i, k in enumerate(("Ionia", "Lydia", "Phrygia")):
        region_glow(c, v, k, ease((q - i * 0.22) / 0.2), size=32)


def map_levant(c, t, a, b):         # Syria, Palestine, Lưỡng Hà, Babylon
    q = (t - a) / (b - a)
    v = view_lerp((38.5, 32.5, 28.0), (40.5, 32.8, 25.0), q)
    map_base(c, v, t)
    for i, k in enumerate(("Syria", "Palestine", "Mesopotamia")):
        region_glow(c, v, k, ease((q - i * 0.2) / 0.2), size=32)
    city_dot(c, v, "Babylon", ease((q - 0.6) / 0.2))


def map_conquests(c, t, a, b):      # "người đã chinh phục người Ba Tư, Media, Bactria, Scythia… Hindu Kush… Indus… Gedrosia"
    q = (t - a) / (b - a)
    v = view_lerp((50.0, 33.0, 44.0), (54.0, 33.0, 50.0), q)
    fade = 1 - ease((q - 0.86) / 0.14) * 0.75
    map_base(c, v, t, dim=1 - fade)
    keys = [("Persia", 0.06), ("Media", 0.13), ("Bactria", 0.20), ("Scythia", 0.27), ("India", 0.47), ("Gedrosia", 0.66)]
    for k, s0 in keys:
        region_glow(c, v, k, ease((q - s0) / 0.06) * fade, size=34)
    draw_route(c, v, ["Babylon", "Susa", "Persepolis", "Ecbatana", "Bactra", "Maracanda", "Bactra", "Taxila", "Patala", "Pura", "Persepolis", "Susa"],
               ease((q - 0.05) / 0.75), color=GOLD)
    if 0.36 < q:                                        # dãy Hindu Kush: hàng tam giác núi
        al = ease((q - 0.36) / 0.06) * fade
        for k in range(7):
            x, y = lonlat(66.5 + k * 1.1, 35.2 + 0.25 * (k % 2), v)
            tri = skia.Path(); tri.moveTo(x - 16, y + 10); tri.lineTo(x, y - 18); tri.lineTo(x + 16, y + 10); tri.close()
            c.drawPath(tri, P("#6A5A44", 230 * al)); c.drawLine(x - 5, y - 9, x, y - 18, P("#FFFFFF", 200 * al, stroke=3))
        x, y = lonlat(69.5, 34.0, v)
        draw_text(c, "HINDU KUSH", x, y + 46, "serif_i", 26, "#3A2A1A", a=230 * al, shadow=False)


def map_veterans(c, t, a, b):       # 10.000 cựu binh về Macedonia
    q = (t - a) / (b - a)
    v = view_lerp((36.0, 37.0, 30.0), (34.0, 37.5, 30.0), q)
    map_base(c, v, t)
    draw_route(c, v, ["Opis", "Issus", "Sardis", "Hellespont", "Pella"], ease((q - 0.1) / 0.75), color="#F2E2B8", width=4)
    city_dot(c, v, "Opis", 1.0); city_dot(c, v, "Pella", ease((q - 0.75) / 0.15))
    al = ease((q - 0.25) / 0.2)
    x, y = lonlat(36.0, 40.2, v)
    draw_text(c, "10.000 cựu binh", x, y, "serif_b", 46, "#2A1A0E", a=255 * al, shadow=False)


def map_divided(c, t, a, b):        # đế chế bị chia cắt giữa các tướng
    q = (t - a) / (b - a)
    v = view_lerp(V_ALL, (44.0, 33.5, 56.0), q)
    map_base(c, v, t)
    kingdoms(c, v, ease((q - 0.05) / 0.7))
    city_dot(c, v, "Babylon", 1.0)


# ---------------------------------------------------------------- cảnh đặc biệt
def intro(c, t, a, b):              # 0–4,5: đẩy chậm vào tranh Opis trong bóng tối, tiêu đề hiện gọn
    q = (t - a) / (b - a)
    ken_burns(c, "K14a", q, (0.44, 0.36, 1.45), (0.44, 0.34, 1.8))
    c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 255 * (1 - ease(t / 1.6)) * 0.9 + 60))
    g = P("#F6D08A", 70 * ease((t - 0.8) / 1.2) * ease((b - t) / 1.0), blur=180)
    c.drawCircle(W * 0.62, H * 0.42, 420, g)
    al = ease((t - 1.3) / 0.9) * ease((b + 1.2 - t) / 0.8)
    draw_text(c, "BÀI DIỄN VĂN Ở OPIS", W / 2, H / 2 + 10, "serif", 92, "#F6EBD2", a=255 * al, spacing=10)
    c.drawLine(W / 2 - 300 * al, H / 2 + 48, W / 2 + 300 * al, H / 2 + 48, P("#E8C878", 220 * al, stroke=2))
    draw_text(c, "ALEXANDER ĐẠI ĐẾ · 324 TCN", W / 2, H / 2 + 104, "serif", 34, "#E8C878", a=230 * al, spacing=8)


def tigris_open(c, t, a, b):        # sông Tigris hoàng hôn, tiêu đề còn mờ dần
    ken_burns(c, "K01b", (t - a) / (b - a), (0.40, 0.55, 1.05), (0.58, 0.52, 1.18))
    intro(c, t, -999, a) if False else None
    al = ease((a + 2.0 - t) / 1.2)
    if al > 0:
        draw_text(c, "BÀI DIỄN VĂN Ở OPIS", W / 2, H / 2 + 10, "serif", 92, "#F6EBD2", a=255 * al, spacing=10)
        c.drawLine(W / 2 - 300 * al, H / 2 + 48, W / 2 + 300 * al, H / 2 + 48, P("#E8C878", 220 * al, stroke=2))
        draw_text(c, "ALEXANDER ĐẠI ĐẾ · 324 TCN", W / 2, H / 2 + 104, "serif", 34, "#E8C878", a=230 * al, spacing=8)
    label("OPIS · BÊN BỜ SÔNG TIGRIS", t, a, b, delay=2.2)


def thirty_k(c, t, a, b):
    ken_burns(c, "K09", (t - a) / (b - a), (0.15, 0.5, 1.15), (0.85, 0.5, 1.15))
    al = ease((t - a - 4.6) / 0.6)
    if al > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 90 * al))
        draw_text(c, "30.000", W / 2, H / 2 + 20, "serif", 150, "#F6EBD2", a=255 * al, spacing=6)
        draw_text(c, "thanh niên Ba Tư được huấn luyện kiểu Macedonia", W / 2, H / 2 + 90, "serif_i", 38, "#E8C878", a=230 * al)


def climax(c, t, a, b):             # "thì tất cả hãy đi đi!" — đẩy nhanh vào mặt, rung nhẹ, chớp sáng
    q = (t - a) / (b - a)
    hit = a + 2.6
    z = 1.15 + 0.15 * ease(q / 0.6) + (0.35 * ease((t - hit) / 0.25) if t > hit else 0)
    c.save()
    if t > hit:
        k = math.exp(-(t - hit) * 5)
        c.translate(9 * k * math.sin(t * 70), 7 * k * math.cos(t * 60))
    ken_burns(c, "K16a", 0, (0.5, 0.42, z), (0.5, 0.42, z), dim=0.1)
    c.restore()
    if 0 <= t - hit < 0.12:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#FFF4DC", 150 * (1 - (t - hit) / 0.12)))


def go_card(c, t, a, b):            # "Đi đi!" — chữ lớn trên nền đen
    c.drawRect(skia.Rect.MakeWH(W, H), P("#000000"))
    al = ease((t - a) / 0.15) * ease((b + 0.8 - t) / 0.6)
    s = 1.0 + 0.04 * (t - a)
    c.save(); c.translate(W / 2, H / 2); c.scale(s, s)
    draw_text(c, "ĐI ĐI!", 0, 50, "serif_b", 170, "#F6EBD2", a=255 * al, spacing=14)
    c.restore()


def objects(c, t, a, b):
    objects_row(c, ["K35a", "K35b", "K35c"], a + 0.2, t)
    for i, w in enumerate(["kiếm", "tên", "đá"]):
        al = ease((t - a - 0.4 - i * 0.9) / 0.6)
        draw_text(c, w, W / (3.4) * (i + 0.7), H - 150, "serif_i", 40, "#E8C878", a=230 * al)


def kin_quote(c, t, a, b):
    ken_burns(c, "K11a", (t - a) / (b - a), (0.32, 0.30, 1.6), (0.32, 0.29, 1.75), dim=0.3)
    quote(c, ["Từ giờ trở đi, ta coi tất cả", "các ngươi là họ hàng của ta."], t, a, b)


def speech_quote(c, t, a, b):
    ken_burns(c, "K16a", (t - a) / (b - a), (0.5, 0.45, 1.05), (0.5, 0.42, 1.2), dim=0.15)
    quote(c, ["Các ngươi muốn đi đâu thì cứ việc đi,", "ta sẽ không ngăn cản."], t, 72.29 + OFF, 75.34 + OFF)


def death(c, t, a, b):
    ken_burns(c, "K52a", (t - a) / (b - a), (0.5, 0.5, 1.05), (0.42, 0.48, 1.2))
    label("BABYLON · 323 TCN", t, a, b, delay=1.2)


def finale(c, t, a, b):
    q = (t - a) / (b - a)
    ken_burns(c, "K14a", q, (0.44, 0.35, 1.5), (0.5, 0.4, 1.0), dim=0.25 + 0.5 * ease((q - 0.6) / 0.4))
    al = ease((q - 0.62) / 0.15) * ease((b - t) / 1.2)
    draw_text(c, "ALEXANDER ĐẠI ĐẾ", W / 2, H / 2 - 10, "serif", 76, "#F6EBD2", a=255 * al, spacing=10)
    draw_text(c, "356 – 323 TCN", W / 2, H / 2 + 60, "serif", 36, "#E8C878", a=230 * al, spacing=8)


# ---------------------------------------------------------------- danh sách cảnh (giây của giọng đọc)
S = [
    (0.00, 5.20, tigris_open),
    (5.20, 9.11, KB("K03", (0.5, 0.45, 1.15), (0.5, 0.62, 1.3))),
    (9.11, 13.01, map_macedonia),
    (13.01, 20.60, map_journey),
    (20.60, 24.80, KB("K06", (0.5, 0.40, 1.05), (0.5, 0.35, 1.22))),
    (24.80, 31.23, KB("K14b", (0.75, 0.40, 1.5), (0.70, 0.38, 1.7), dim=0.1)),
    (31.23, 39.80, thirty_k),
    (39.80, 44.19, KB("K11b", (0.70, 0.30, 1.6), (0.72, 0.29, 1.85))),
    (44.19, 50.00, KB("K11a", (0.5, 0.33, 1.0), (0.42, 0.31, 1.2))),
    (50.00, 54.59, KB("K14a", (0.40, 0.38, 1.1), (0.55, 0.36, 1.3))),
    (54.59, 61.21, KB("K13", (0.30, 0.5, 1.05), (0.25, 0.5, 1.35))),
    (61.21, 64.98, KB("K14b", (0.45, 0.34, 1.6), (0.45, 0.33, 1.9))),
    (64.98, 69.41, KB("K14a", (0.5, 0.40, 1.0), (0.5, 0.38, 1.15), dim=0.15)),
    (69.41, 81.91, speech_quote),
    (81.91, 85.66, KB("K18", (0.5, 0.38, 1.0), (0.5, 0.35, 1.15))),
    (85.66, 97.24, KB("K19", (0.30, 0.50, 1.15), (0.62, 0.48, 1.3))),
    (97.24, 102.60, KB("K20a", (0.40, 0.5, 1.05), (0.6, 0.5, 1.2))),
    (102.60, 108.05, KB("K20b", (0.5, 0.35, 1.25), (0.5, 0.35, 1.5))),
    (108.05, 121.50, map_philip),
    (121.50, 125.00, KB("K22a", (0.4, 0.5, 1.05), (0.6, 0.45, 1.2))),
    (125.00, 127.94, KB("K23", (0.5, 0.35, 1.1), (0.5, 0.3, 1.3))),
    (127.94, 132.30, KB("K24", (0.45, 0.5, 1.05), (0.55, 0.5, 1.2))),
    (132.30, 136.62, KB("K18b", (0.5, 0.30, 1.3), (0.5, 0.30, 1.6))),
    (136.62, 143.45, map_greece_to_asia),
    (143.45, 146.00, KB("K26a", (0.5, 0.5, 1.05), (0.5, 0.42, 1.2))),
    (146.00, 148.63, KB("K26b", (0.4, 0.5, 1.05), (0.55, 0.5, 1.15))),
    (148.63, 152.50, KB("K27", (0.35, 0.5, 1.05), (0.6, 0.5, 1.15))),
    (152.50, 156.44, map_asia_minor),
    (156.44, 160.50, KB("K28b", (0.4, 0.5, 1.05), (0.55, 0.5, 1.15))),
    (160.50, 164.39, map_levant),
    (164.39, 168.50, KB("K30a", (0.5, 0.5, 1.1), (0.5, 0.5, 1.35))),
    (168.50, 172.51, KB("K30b", (0.5, 0.5, 1.1), (0.5, 0.45, 1.3))),
    (172.51, 177.26, KB("K31", (0.5, 0.35, 1.15), (0.5, 0.32, 1.35))),
    (177.26, 183.72, KB("K32", (0.5, 0.55, 1.2), (0.5, 0.52, 1.5))),
    (183.72, 189.27, KB("K16b", (0.45, 0.45, 1.1), (0.45, 0.42, 1.3), dim=0.1)),
    (189.27, 196.25, KB("K33", (0.35, 0.5, 1.1), (0.55, 0.5, 1.25))),
    (196.25, 201.78, KB("K16a", (0.48, 0.42, 1.3), (0.48, 0.40, 1.55), dim=0.2)),
    (201.78, 206.50, KB("K34a", (0.5, 0.35, 1.15), (0.5, 0.5, 1.3))),
    (206.50, 211.25, KB("K34b", (0.4, 0.5, 1.05), (0.6, 0.5, 1.2))),
    (211.25, 218.98, objects),
    (218.98, 226.61, KB("K36", (0.35, 0.5, 1.05), (0.6, 0.5, 1.15))),
    (226.61, 234.70, KB("K45c", (0.25, 0.5, 1.05), (0.75, 0.5, 1.1))),
    (234.70, 239.86, KB("K37", (0.5, 0.5, 1.1), (0.5, 0.48, 1.35))),
    (239.86, 248.24, KB("K38", (0.5, 0.40, 1.1), (0.5, 0.35, 1.35))),
    (248.24, 252.78, KB("K39", (0.35, 0.5, 1.1), (0.6, 0.5, 1.2))),
    (252.78, 258.27, KB("K14a", (0.45, 0.36, 1.2), (0.45, 0.34, 1.4), dim=0.1)),
    (258.27, 262.27, climax),
    (262.27, 282.40, map_conquests),
    (282.40, 286.75, KB("K11a", (0.30, 0.30, 2.0), (0.30, 0.28, 2.3), dim=0.25)),
    (286.75, 292.20, KB("K16b", (0.45, 0.42, 1.3), (0.45, 0.40, 1.6), dim=0.3)),
    (292.20, 293.18, go_card),
    (293.18, 298.28, KB("K45b", (0.5, 0.5, 1.05), (0.5, 0.48, 1.2), dim=0.35)),
    (298.28, 303.30, KB("K45a", (0.5, 0.5, 1.05), (0.5, 0.5, 1.2))),
    (303.30, 308.31, KB("K09", (0.80, 0.5, 1.2), (0.30, 0.5, 1.2))),
    (308.31, 315.00, KB("K14a", (0.70, 0.38, 1.6), (0.62, 0.36, 1.8), dim=0.2)),
    (315.00, 321.41, KB("K11b", (0.75, 0.30, 1.6), (0.68, 0.29, 1.8), dim=0.15)),
    (321.41, 328.94, KB("K11a", (0.32, 0.30, 1.6), (0.32, 0.28, 1.9))),
    (328.94, 335.40, KB("K11b", (0.82, 0.29, 1.9), (0.82, 0.27, 2.2))),
    (335.40, 339.28, kin_quote),
    (339.28, 341.00, KB("K11a", (0.4, 0.32, 1.2), (0.4, 0.31, 1.3))),
    (341.00, 347.40, KB("K50", (0.5, 0.5, 1.05), (0.5, 0.45, 1.2))),
    (347.40, 353.29, KB("K36", (0.6, 0.5, 1.15), (0.35, 0.5, 1.15))),
    (353.29, 359.15, map_veterans),
    (359.15, 361.42, KB("K16b", (0.45, 0.42, 1.2), (0.45, 0.42, 1.3), dim=0.2)),
    (361.42, 368.88, death),
    (368.88, 374.48, map_divided),
    (374.48, 389.20, finale),
]
HARD_CUT = {258.27, 292.20, 293.18}      # cắt thẳng ở cao trào; còn lại hòa mờ


def draw(c, t):
    _c[0] = c
    tv = t - OFF
    if tv < 0:
        intro(c, t, 0.0, OFF)
        return
    for i, (a, b, fn) in enumerate(S):
        if a <= tv < b or (i == len(S) - 1 and tv >= a):
            fn(c, t, a + OFF, b + OFF)
            if i > 0 and a not in HARD_CUT and tv - a < 0.6:
                pa, pb, pf = S[i - 1]
                lay = 1 - ease((tv - a) / 0.6)
                c.saveLayerAlpha(None, int(255 * lay))
                pf(c, t, pa + OFF, pb + OFF)
                c.restore()
            return
