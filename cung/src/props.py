"""Đạo cụ dùng chung (tách từ Tập 4): dây thừng, bó củi, rừng, khe núi, thỏ, gãi chấy…"""
from common import *  # noqa

GS = 0.95


def hand_world(who, x, y, s, face, hand, side=1, crouch=0.0):
    st = rig.STYLES[who]
    sh_y = -150 - st["torso_h"] + 22 + crouch * 60
    sx = side * (st["torso_w"] / 2 - 10)
    return x + face * (sx + hand[0]) * s, y + (sh_y + hand[1]) * s


# ---------------------------------------------------------------- dây thừng & đạo cụ
ROPE = "#C9A86A"
ROPE_D = "#9C7E48"


def rope_line(c, pts, w=12, a=255):
    if len(pts) < 2:
        return
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p, P(OUT, a, stroke=w + 6)); c.drawPath(p, P(ROPE, a, stroke=w))
    # vân xoắn
    acc = 0.0
    step = w * 0.9
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        L = math.hypot(x1 - x0, y1 - y0)
        if L < 1e-3:
            continue
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        d = (step - acc) % step
        while d < L:
            cx_, cy_ = x0 + ux * d, y0 + uy * d
            nx, ny = -uy, ux
            c.drawLine(cx_ - nx * w * 0.45 - ux * w * 0.3, cy_ - ny * w * 0.45 - uy * w * 0.3,
                       cx_ + nx * w * 0.45 + ux * w * 0.3, cy_ + ny * w * 0.45 + uy * w * 0.3, P(ROPE_D, a, stroke=max(2, w * 0.22)))
            d += step
        acc = (acc + L) % step


def sag_pts(x0, y0, x1, y1, sag=0.0, n=16, wav=0.0, t=0.0):
    out = []
    for k in range(n + 1):
        q = k / n
        out.append((lerp(x0, x1, q) + wav * math.sin(q * 9 + t * 8) * q, lerp(y0, y1, q) + sag * 4 * q * (1 - q)))
    return out


def rope_coil(c, x, y, s=1.0, rot=0.0):
    with Xf(c, x, y, rot, s):
        for k in range(4):
            r = 60 - k * 9
            p = skia.Path(); p.addOval(skia.Rect.MakeXYWH(-r, -r * 0.75 + k * 3, 2 * r, 1.5 * r))
            c.drawPath(p, P(OUT, stroke=18)); c.drawPath(p, P(ROPE if k % 2 == 0 else ROPE_D, stroke=12))


def coil_prop(c):
    rope_coil(c, 0, 10, 0.6)


def log_piece(c, x, y, rot=0.0, s=1.0):
    with Xf(c, x, y, rot, s):
        fo(c, rrect_path(-80, -20, 160, 40, 18), "#8A6040", ow=5)
        c.drawOval(skia.Rect.MakeXYWH(58, -18, 26, 36), P("#D9B07A")); c.drawOval(skia.Rect.MakeXYWH(58, -18, 26, 36), P(OUT, stroke=4))


BUNDLE = [(-40, 0), (40, 0), (0, -34), (-40, -68), (40, -68), (0, -102), (0, 34)]


def wood_bundle(c, x, y, s=1.0, n=7, tied=False, wobble=0.0, t=0.0):
    with Xf(c, x, y, wobble * 4 * math.sin(t * 7), s):
        for k in range(min(n, len(BUNDLE))):
            dx, dy = BUNDLE[k]
            log_piece(c, dx, dy, 3 * math.sin(k * 2.3), 0.9)
        if tied:
            for bx_ in (-50, 50):
                rope_line(c, [(bx_, -130), (bx_ + 6, 60)], w=10)


GROUND_LOGS = [(-150, 0, 12), (-60, 6, -20), (40, -2, 35), (120, 8, -8), (-110, -26, 70), (70, -28, -50), (180, -6, 15)]


def logs_ground(c, x, y, n=7, s=1.0):
    for k in range(min(n, len(GROUND_LOGS))):
        dx, dy, r = GROUND_LOGS[k]
        log_piece(c, x + dx * s, y + dy * s, r, 0.85 * s)


def forest_bg(c, t, tone="morning"):
    sky = {"morning": ("#9FD3F0", "#F2F6E2"), "after": ("#E9B97A", "#F6E2B0")}[tone]
    grad_rect(c, skia.Rect.MakeXYWH(-800, -800, W + 1600, H + 1600), *sky)
    for k, (yy, colr) in enumerate([(880, "#7FA36A"), (980, "#5E8A4E")]):
        p = skia.Path(); p.moveTo(-800, 1500)
        for i in range(0, 26):
            p.lineTo(-800 + i * 110, yy - 120 * abs(math.sin(i * 0.8 + k)))
        p.lineTo(W + 800, 1500); p.close()
        c.drawPath(p, paint(colr))
    for x in (-60, 180, 980, 1180):
        fo(c, rrect_path(x - 34, 700, 68, GROUND - 700, 16), "#6E5236", ow=6)
        for dx, dy, r in [(-90, 640, 120), (40, 580, 140), (110, 680, 110)]:
            c.drawCircle(x + dx, dy, r, P("#3E6A3A")); c.drawCircle(x + dx, dy, r, P(OUT, 110, stroke=5))
    c.drawRect(skia.Rect.MakeXYWH(-800, GROUND, W + 1600, 900), paint("#8A9A52"))
    c.drawRect(skia.Rect.MakeXYWH(-800, GROUND, W + 1600, 12), paint(OUT, 110))
    for k in range(10):
        x = (k * 157) % W
        c.drawLine(x, GROUND + 40 + k * 18, x + 40, GROUND + 40 + k * 18, P("#6E7A3A", stroke=5))


def bark_closeup(c, t, peel=0.0, crumble=0.0, strips=0.0):
    """Cận cảnh thân cây: vỏ ngoài sần sùi bị lột, lộ lớp vỏ trong có thớ dài."""
    grad_rect(c, skia.Rect.MakeWH(W, H), "#3E5A34", "#22341E")
    trunk = skia.Rect.MakeXYWH(180, -100, 720, H + 200)
    c.drawRect(trunk, P("#5A4030"))
    # lớp vỏ trong (lộ ra theo peel)
    top = lerp(1500, 300, peel)
    inner = skia.Rect.MakeXYWH(300, top, 480, 1500 - top)
    if peel > 0:
        c.drawRect(inner, P("#E9D6A8"))
        for k in range(12):
            x = 320 + k * 40
            c.drawLine(x, top, x + 4, 1500, P("#CDB27E", stroke=5))
        if strips > 0:
            for k in range(4):
                x = 360 + k * 110
                L = strips * 600
                sinew(c, x, 700, x + 30 * math.sin(k), 700 + L, w=10, col="#F1E2B8", sag=30)
    # vỏ ngoài: các mảng nứt
    for r in range(10):
        for k in range(6):
            x = 185 + k * 122 + (r % 2) * 50 + 14 * math.sin(r * 3.1 + k)
            y = -80 + r * 220 + 30 * math.sin(k * 2.3 + r)
            w_, h_ = 96 + 18 * math.sin(k + r), 200 + 30 * math.cos(k * 1.7 + r)
            if peel > 0 and 270 < x + w_ / 2 < 810 and y + h_ > top:
                continue
            pl = skia.Path(); pl.moveTo(x + w_ * 0.2, y); pl.lineTo(x + w_ * 0.85, y + 12); pl.lineTo(x + w_, y + h_ * 0.6)
            pl.lineTo(x + w_ * 0.8, y + h_); pl.lineTo(x + w_ * 0.1, y + h_ - 14); pl.lineTo(x, y + h_ * 0.4); pl.close()
            fo(c, pl, "#6E5040", ow=5)
            c.drawLine(x + w_ * 0.45, y + 30, x + w_ * 0.55, y + h_ - 30, P("#4A3428", stroke=5))
    c.drawRect(trunk, P(OUT, stroke=10))
    if peel > 0 and peel < 1:
        # dải vỏ đang cong lên
        cur = skia.Path(); cur.moveTo(300, top); cur.cubicTo(360, top - 160, 720, top - 160, 780, top)
        cur.lineTo(780, top - 30); cur.cubicTo(720, top - 200, 360, top - 200, 300, top - 30); cur.close()
        fo(c, cur, "#6E5040", ow=6)
    if crumble > 0:
        for k in range(8):
            q = clamp(crumble - k * 0.05)
            c.drawCircle(250 + k * 80, 560 + q * 900 + k * 10, 14, P("#6E5040", 255 * (1 - q)))


def strand(c, x0, x1, y, w, twist, phase, col="#E3C48E", dark="#B8955E", direction=1, n=None):
    """Bó sợi xoắn: vân chéo nghiêng theo chiều xoắn, chạy theo phase."""
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y - w / 2, x1 - x0, w), w / 2, w / 2))
    c.drawPath(p, P(col))
    c.save(); c.clipPath(p, skia.ClipOp.kIntersect, True)
    step = w * 0.7
    k0 = int((x1 - x0) / step) + 3
    for k in range(-2, k0):
        xx = x0 + (k + (phase % 1)) * step
        c.drawLine(xx - direction * w * 0.4 * twist, y - w / 2, xx + direction * w * 0.4 * twist, y + w / 2, P(dark, stroke=w * 0.16))
    c.restore()
    c.drawPath(p, P(OUT, stroke=6))


def curl_arrow(c, x, y, r, ccw, t, col="#F4C430", p=1.0):
    if p <= 0:
        return
    sweep = 280 * p
    start = -90 + (t * 160 % 360) * (-1 if ccw else 1)
    rect = skia.Rect.MakeXYWH(x - r, y - r * 0.45, 2 * r, r * 0.9)
    path = skia.Path(); path.addArc(rect, start, -sweep if ccw else sweep)
    c.drawPath(path, P(OUT, stroke=20)); c.drawPath(path, P(col, stroke=12))
    end = start + (-sweep if ccw else sweep)
    a = math.radians(end)
    ex, ey = x + r * math.cos(a), y + r * 0.45 * math.sin(a)
    tang = a + (-math.pi / 2 if ccw else math.pi / 2)
    tri = skia.Path()
    tri.moveTo(ex + 34 * math.cos(tang), ey + 34 * 0.45 * math.sin(tang) * 2)
    tri.lineTo(ex + 22 * math.cos(tang + 2.3), ey + 22 * math.sin(tang + 2.3))
    tri.lineTo(ex + 22 * math.cos(tang - 2.3), ey + 22 * math.sin(tang - 2.3)); tri.close()
    fo(c, tri, col, ow=5)


def cocoon(c, x, y, s, p, t, wob=0.0):
    """Dây quấn kín người Gầm từ vai xuống chân (p = 0..1)."""
    n = int(14 * p)
    for k in range(n):
        yy = y - (330 - k * 23) * s
        w = (130 if k < 11 else 110 - (k - 11) * 12) * s
        rope_line(c, [(x - w + wob, yy + 8 * s), (x + w + wob, yy - 8 * s)], w=16 * s)


def rabbit(c, x, y, s, t, face=1, hop=0.0, look_back=False):
    with Xf(c, x, y - 60 * s * math.sin(math.pi * hop) if hop else y, 0, s):
        c.scale(face, 1)
        fo(c, oval(0, -40, 60, 40), "#B8A898", ow=5)
        fo(c, oval(50, -80, 34, 30), "#B8A898", ow=5)
        for dx, rot in [(36, -12), (58, 8)]:
            with Xf(c, dx, -100, rot + 6 * math.sin(t * 6), 1):
                fo(c, oval(0, -40, 12, 40), "#B8A898", ow=4)
                c.drawOval(skia.Rect.MakeXYWH(-5, -70, 10, 50), P("#E8A0A0"))
        c.drawCircle(-60, -46, 16, P("#FFFFFF")); c.drawCircle(-60, -46, 16, P(OUT, stroke=4))
        c.drawCircle(62, -86, 7, P(OUT)); c.drawCircle(64, -88, 2.5, P("#FFFFFF"))
        c.drawCircle(84, -76, 5, P("#E8746B"))
        fo(c, oval(-10, -4, 30, 10), "#A89888", ow=4)


# khe núi
EDGE_L, EDGE_R, PLAT_Y = 560, 900, 1100
LEDGE_Y, LEDGE_X = 1720, 640
TREE_X = 250


def ravine_bg(c, t, tone="after", rope_on_ledge=True, anchor=0.0, rope_down=False):
    sky = {"after": ("#E9B97A", "#F6E2B0"), "dusk": ("#F08A4B", "#F6C67A")}[tone]
    grad_rect(c, skia.Rect.MakeXYWH(-900, -900, W + 1800, 4200), *sky)
    for k, (yy, colr) in enumerate([(820, "#B98A6A"), (900, "#9A6E52")]):
        p = skia.Path(); p.moveTo(-900, 1300)
        for i in range(0, 30):
            p.lineTo(-900 + i * 110, yy - 140 * abs(math.sin(i * 0.9 + k)))
        p.lineTo(W + 900, 1300); p.close()
        c.drawPath(p, paint(colr))
    # lòng vực
    grad_rect(c, skia.Rect.MakeXYWH(EDGE_L - 40, PLAT_Y, EDGE_R - EDGE_L + 80, 2200), "#6A5040", "#0E0A08")
    # vách trái (có mỏm đá)
    lw = skia.Path(); lw.moveTo(-900, PLAT_Y); lw.lineTo(EDGE_L, PLAT_Y); lw.lineTo(EDGE_L - 10, LEDGE_Y - 40)
    lw.lineTo(LEDGE_X + 120, LEDGE_Y - 10); lw.lineTo(LEDGE_X + 110, LEDGE_Y + 40); lw.lineTo(EDGE_L - 20, LEDGE_Y + 70)
    lw.lineTo(EDGE_L - 40, 3400); lw.lineTo(-900, 3400); lw.close()
    fo(c, lw, "#8A7060", ow=8)
    rw = skia.Path(); rw.moveTo(W + 900, PLAT_Y); rw.lineTo(EDGE_R, PLAT_Y); rw.lineTo(EDGE_R + 20, 2000); rw.lineTo(EDGE_R + 40, 3400)
    rw.lineTo(W + 900, 3400); rw.close()
    fo(c, rw, "#8A7060", ow=8)
    for k in range(12):
        c.drawLine(-200 + k * 70, PLAT_Y + 120 + (k * 97) % 600, -150 + k * 70, PLAT_Y + 160 + (k * 97) % 600, P("#6E5848", stroke=6))
    c.drawRect(skia.Rect.MakeXYWH(-900, PLAT_Y - 16, EDGE_L + 900, 30), P("#8A9A52"))
    c.drawRect(skia.Rect.MakeXYWH(EDGE_R, PLAT_Y - 16, W + 900, 30), P("#8A9A52"))
    # cây to bên trái
    fo(c, rrect_path(TREE_X - 46, PLAT_Y - 700, 92, 700, 20), "#6E5236", ow=7)
    for dx, dy, r in [(-120, -760, 150), (60, -840, 180), (180, -720, 140)]:
        c.drawCircle(TREE_X + dx, PLAT_Y + dy, r, P("#4F7F45")); c.drawCircle(TREE_X + dx, PLAT_Y + dy, r, P(OUT, 110, stroke=5))
    if rope_on_ledge:
        rope_coil(c, LEDGE_X + 70, LEDGE_Y - 22, 0.55, 10)
    if anchor > 0:
        for k in range(int(3 * anchor)):
            yy = PLAT_Y - 90 - k * 26
            rope_line(c, [(TREE_X - 50, yy + 8), (TREE_X + 50, yy - 8)], w=12)
    if rope_down:
        rope_line(c, [(TREE_X + 46, PLAT_Y - 90), (EDGE_L, PLAT_Y - 6), (EDGE_L + 4, LEDGE_Y - 30)], w=12)


def tree_trunk_front(c, x, y, s=1.0):
    fo(c, rrect_path(x - 60 * s, y - 900 * s, 120 * s, 900 * s, 24 * s), "#6E5236", ow=7)
    for dx, dy, r in [(-160, -980, 190), (60, -1060, 220), (220, -940, 170)]:
        c.drawCircle(x + dx * s, y + dy * s, r * s, P("#4F7F45")); c.drawCircle(x + dx * s, y + dy * s, r * s, P(OUT, 110, stroke=5))


def scratch_hands(ta, speed=1.0):
    k = int(ta * 2.5 * speed) % 3
    w = 20 * math.sin(ta * 40)
    return [((-100, 120 + w), (40, 40 - w)), ((120, -20 + w), (-40, 80)), ((60, 160 + w), (-90, -40 - w))][k]


def lice_on(c, x, y, s, t, n=3):
    for k in range(n):
        louse(c, x + 110 * s * math.cos(k * 2.1 + t * 0.5), y - 300 * s + 90 * s * math.sin(k * 1.7), 0.3 * s / 0.95, t, seed=k)


