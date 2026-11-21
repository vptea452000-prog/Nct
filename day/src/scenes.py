"""Tập 4: Dây thừng — Bộp và Gầm (phim hài không lời, bộ khung nhân vật v2)."""
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


# ================================================================ CẢNH 1 — bìa rừng
BXF, GXF = 640, 330


def carry_bop(c, t, x, n, crouch=0.0, walk=None, eyes="open", mouth="flat", **kw):
    kw.setdefault("look", (-1, 0.3))
    ch(c, "bop", x, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, crouch=crouch, walk=walk,
       hand_l=(70, 80 + crouch * 60), hand_r=(-30, 90 + crouch * 60), eyes=eyes, mouth=mouth, **kw)
    if n > 0:
        wood_bundle(c, x - 60 * GS, GROUND - (230 - crouch * 60) * GS, 0.8, n=n, wobble=1.0 if walk is not None else 0.3, t=t)


def sc_open(c, t):
    ta, u = loc("open", t)
    K = Cam(560, 1000, 1.1); K.on(c)
    forest_bg(c, t)
    carry_bop(c, t, lerp(980, BXF, ease_out(u)), 7, walk=ta * 6, eyes="squint", mouth="wavy")
    K.off(c)
    kinetic(c, "TẬP 4", W / 2, 400, t, T["open"][0] + 0.3, size=70, per=0.04)
    kinetic(c, "DÂY THỪNG", W / 2, 540, t, T["open"][0] + 0.6, size=140, color="#F4C430", per=0.06)


def sc_drop(c, t):
    ta, u = loc("drop", t)
    K = Cam(600, 1000, 1.3); K.on(c)
    forest_bg(c, t)
    gx_ = BXF - 160
    if ta < 0.3:
        n, crouch, ground = 7, 0, []
    elif ta < 0.9:
        n, crouch, ground = 6, ease_in_out(clamp((ta - 0.5) / 0.3)), [0]
    elif ta < 1.25:
        n, crouch, ground = 7, 1 - ease_in_out(clamp((ta - 0.9) / 0.3)), []
    elif ta < 1.8:
        n, crouch, ground = 5, ease_in_out(clamp((ta - 1.45) / 0.3)), [1, 2]
    elif ta < 2.15:
        n, crouch, ground = 7, 1 - ease_in_out(clamp((ta - 1.8) / 0.3)), []
    else:
        n, crouch, ground = 0, 0, list(range(7))
    for k in ground:
        dx, dy, r = GROUND_LOGS[k]
        log_piece(c, gx_ + dx * 0.9, GROUND - 20 + dy, r, 0.8)
    for t0, idx in ((0.3, [0]), (1.25, [1, 2]), (2.15, list(range(7)))):
        q = (ta - t0) / 0.25
        if 0 <= q < 1:
            for k in idx:
                dx, dy, r = GROUND_LOGS[k]
                log_piece(c, lerp(BXF - 60, gx_ + dx * 0.9, q), lerp(GROUND - 230 * GS, GROUND - 20 + dy, q * q), r * q, 0.8)
    carry_bop(c, t, BXF, n, crouch=crouch, eyes="closed" if ta > 2.15 else "wide", mouth="o" if ta > 2.15 else "flat", look=(-1, 1))
    K.off(c)
    sfx_word(c, "CỘP", 380, 1400, t, T["drop"][0] + 0.55, size=80, color="white", dur=0.4)
    sfx_word(c, "CỘP CỘP", 380, 1400, t, T["drop"][0] + 1.5, size=80, color="white", dur=0.4)
    sfx_word(c, "ÀO!", 440, 1350, t, T["drop"][0] + 2.3, size=140, color="#F4C430", dur=0.6)


def sc_sigh(c, t):
    ta, u = loc("sigh", t)
    K = Cam(600, 980, 1.5); K.on(c)
    forest_bg(c, t)
    logs_ground(c, BXF - 160, GROUND - 20, 7, 0.9)
    ch(c, "bop", BXF, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, eyes="open", look=(-1, 1), brow_tilt=-1.0, mouth="frown",
       hand_l=(60, 110), hand_r=(-20, 110), head_tilt=-6, crouch=0.2)
    K.off(c)
    hx, hy = K.map(BXF - 30, GROUND - 330 * GS)
    breath(c, hx, hy, t, T["sigh"][0] + 1.9, dirx=-1, a=150)
    say(c, "sigh", K, BXF, GROUND, GS, t, who="bop", bx=540)


def gam_walk_spear(c, t, x, walk=None, scratch=True, **kw):
    ta = t
    hr, hl = scratch_hands(ta, 1.0)
    kw.setdefault("eyes", "squint"); kw.setdefault("mouth", "wavy")
    ch(c, "gam", x, GROUND, GS, t, face=1, outfit="bigcoat", walk=walk, hold="spear", hold_side="l", hand_l=(-40, -60),
       hold_ang=70, hold_len=480, hand_r=hr if scratch else (60, 40), **kw)


def sc_pass(c, t):
    ta, u = loc("pass", t)
    K = Cam(500, 1000, 1.15); K.on(c)
    forest_bg(c, t)
    logs_ground(c, BXF - 160, GROUND - 20, 7, 0.9)
    gx = lerp(-200, GXF, ease_out(u))
    gam_walk_spear(c, t, gx, walk=ta * 6)
    lice_on(c, gx, GROUND, GS, t)
    ch(c, "bop", BXF + 60, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, eyes="open", look=(-1, 0), brow_tilt=-0.6,
       mouth="flat", hand_l=(60, 110), hand_r=(-20, 110))
    K.off(c)
    sfx_word(c, "SỒN SỘT", 300, 1500, t, T["pass"][0] + 0.4, size=80, color="white", dur=1.4)


def sc_weak(c, t):
    ta, u = loc("weak", t)
    K = Cam(500, 1000, 1.15); K.on(c)
    forest_bg(c, t)
    logs_ground(c, BXF - 160, GROUND - 20, 7, 0.9)
    ch(c, "gam", GXF, GROUND, GS, t, face=1, outfit="bigcoat", hold="spear", hold_side="l", hand_l=(-40, -60), hold_ang=70, hold_len=480,
       hand_r=(180, -80 + 10 * math.sin(ta * 12)), eyes="squint", mouth="grin", lean=-8 + 3 * math.sin(ta * 14), brow=0.6)
    ch(c, "bop", BXF + 60, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, eyes="open", look=(-1, 0), brow_tilt=-0.8,
       mouth="frown", hand_l=(60, 110), hand_r=(-20, 110))
    K.off(c)
    say(c, "weak", K, GXF, GROUND, GS, t, bx=480)


def sc_double(c, t):
    ta, u = loc("double", t)
    K = Cam(500, 1000, 1.15); K.on(c)
    forest_bg(c, t)
    logs_ground(c, BXF - 160, GROUND - 20, 7, 0.9)
    stone_spear_v(c, 120, GROUND, 480, 0.9, ang=-70)
    ch(c, "bop", BXF + 140, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, eyes="open", look=(-1, 0), mouth="flat",
       hand_l=(60, 110), hand_r=(-20, 110))
    if ta < 1.6:
        lift = ease_out(clamp(ta / 0.4))
        x = lerp(GXF, GXF + 150, clamp((ta - 0.4) / 1.2))
        ch(c, "gam", x, GROUND, GS, t, face=1, outfit="bigcoat", walk=(ta - 0.4) * 5 if ta > 0.4 else None, stride=0.7,
           crouch=0.5 * (1 - lift), squash=1 - 0.08 * lift, hand_l=(80, -60), hand_r=(60, -40), eyes="squint", mouth="chatter",
           blush=0.8, lean=6 * math.sin(ta * 5), shiver=0.4)
        for sc_x in (-50, 60):
            wood_bundle(c, x + 70 * GS + sc_x * 0.5, GROUND - 330 * GS - (20 if sc_x > 0 else 0), 0.75, n=7, wobble=1.5, t=t)
    else:
        x = GXF + 150
        q = clamp((ta - 1.6) / 0.15)
        hop = abs(math.sin((ta - 1.75) * 9)) if ta > 1.75 else 0
        logs_ground(c, x + 60, GROUND - 20, 7, 1.0)
        logs_ground(c, x + 10, GROUND - 40, 5, 0.8)
        ch(c, "gam", x, GROUND, GS, t, face=1, outfit="bigcoat", feet_air=50 * hop, hand_l=(40, 220), hand_r=(80, 200),
           eyes="wide", mouth="shout", brow=1.0, sweat=1.0, squash=1 - 0.1 * (1 - q))
    K.off(c)
    sfx_word(c, "1… 2… 3…", 400, 620, t, T["double"][0] + 0.5, size=80, color="white", dur=1.1)
    c.save(); shake(c, t, T["double"][0] + 1.65, 16)
    sfx_word(c, "CỐP!", 560, 1180, t, T["double"][0] + 1.65, size=150, color="#F4C430", dur=0.7)
    c.restore()


def sc_slippery(c, t):
    ta, u = loc("slippery", t)
    K = Cam(560, 960, 1.45); K.on(c)
    forest_bg(c, t)
    x = GXF + 150
    logs_ground(c, x + 60, GROUND - 20, 7, 1.0)
    hop = abs(math.sin(ta * 7))
    ch(c, "gam", x, GROUND, GS, t, face=1, outfit="bigcoat", feet_air=35 * hop, hand_l=(40, 220), hand_r=(80, 200),
       eyes="squint", brow_tilt=-0.4, mouth="frown", look=(1, 0.5), head_tilt=-6)
    # giọt nước mắt nhỏ
    c.drawCircle(x + 70, GROUND - 400 * GS + (ta * 120 % 50), 9, P("#9FD3F0"))
    K.off(c)
    say(c, "slippery", K, x, GROUND, GS, t, bx=540)


# ================================================================ CẢNH 2 — Bộp làm dây
def sc_bark(c, t, n="bark"):
    ta, u = loc(n, t)
    if n == "bark":
        p = ease_in_out(clamp(ta / 2.0))
        bark_closeup(c, t, peel=p)
        big_hand(c, 220 + 40 * math.sin(ta * 10), lerp(1500, 330, p) + 120, 1.5, 120)
        sfx_word(c, "RÈN RẸT", 760, 520, t, T[n][0] + 0.3, size=90, color="white", dur=1.8)
    elif n == "bark1":
        bark_closeup(c, t, peel=1.0, crumble=clamp(ta / 1.2))
        sfx_word(c, "RẮC", 300, 520, t, T[n][0] + 0.2, size=110, color="white", dur=0.6)
        say_at(c, n, t, 540, 380, (300, 560))
    else:
        bark_closeup(c, t, peel=1.0, strips=ease_out(clamp(ta / 1.2)))
        say_at(c, n, t, 540, 380, (540, 640))


def sc_one(c, t):
    ta, u = loc("one", t)
    bench(c, t)
    br = ta > 0.9
    pull = ease_in_out(clamp(ta / 0.9)) if not br else 1.0
    ext = 60 * ease_out(clamp((ta - 0.9) / 0.2)) if br else 0
    lx, rx_ = lerp(320, 200, pull) - ext, lerp(760, 880, pull) + ext
    col = "#F1E2B8"
    if not br:
        sinew(c, lx + 60, 1040, rx_ - 60, 1040, w=6, col=col)
    else:
        e = 40 * math.sin(ta * 30) * math.exp(-(ta - 0.9) * 5)
        sinew(c, lx + 60, 1040, 520, 1080 + e, w=6, col=col)
        sinew(c, 560, 1080 - e, rx_ - 60, 1040, w=6, col=col)
    big_hand(c, lx, 1080, 1.4, 90)
    with Xf(c, rx_, 1080, 0, 1):
        c.scale(-1, 1); big_hand(c, 0, 0, 1.4, 90)
    sfx_word(c, "PHỰT!", 540, 760, t, T["one"][0] + 0.9, size=150, color="#F4C430", dur=0.8)


def sc_weak1(c, t):
    ta, u = loc("weak1", t)
    K = Cam(600, 980, 1.6); K.on(c)
    forest_bg(c, t)
    def broken(c_):
        sinew(c_, -40, 0, 40, 40, w=5, col="#F1E2B8", sag=10)
    ch(c, "bop", BXF, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, hand_r=(60, -90), prop_r=broken, hand_l=(-60, -80),
       prop_l=broken, eyes="open", look=(-0.6, 0.4), brow_tilt=-1.0, mouth="frown")
    K.off(c)
    say(c, "weak1", K, BXF, GROUND, GS, t, who="bop", bx=540)


def braid_scene(c, t, ta, mode, show_text=True):
    bench(c, t)
    if mode == "bundles":
        for k in range(3):
            p = clamp((ta - k * 0.6) / 0.5)
            if p <= 0:
                continue
            y = 820 + k * 200
            strand(c, 220, 220 + 640 * ease_out(p), y, 70, 1.0, ta * 1.2, direction=1)
            curl_arrow(c, 960, y, 56, True, t, p=pop(t, T["twist1"][0] + k * 0.6 + 0.3))
        if show_text:
            text(c, "XOẮN TỪNG BÓ ↺", W / 2, 580, "xbold", 80, "#F4C430", align="center", stroke=8, stroke_color="#1A120D")
    elif mode == "braid":
        q = ease_in_out(clamp(ta / 1.4))
        for k in range(3):
            y = lerp(820 + k * 200, 1020 + (k - 1) * 26, q)
            if q < 0.98:
                strand(c, 220, 860, y, lerp(70, 40, q), 1.0, ta * 0.4, direction=1)
        if q > 0.6:
            a = clamp((q - 0.6) / 0.4)
            strand(c, 200, 880, 1020, 110, 1.6, -ta * 1.5, col="#D8B878", dark="#8C6E3E", direction=-1)
            curl_arrow(c, 540, 1020, 360, False, t, col="#5DADE2", p=a)
        if show_text:
            text(c, "BỆN NGƯỢC CHIỀU ↻", W / 2, 580, "xbold", 80, "#5DADE2", align="center", stroke=8, stroke_color="#1A120D")
    else:  # tổng kết: trên = một bó ↺, dưới = dây ↻
        strand(c, 200, 700, 820, 70, 1.0, ta * 1.2, direction=1)
        curl_arrow(c, 850, 820, 80, True, t)
        strand(c, 200, 700, 1180, 110, 1.6, -ta * 1.5, col="#D8B878", dark="#8C6E3E", direction=-1)
        curl_arrow(c, 850, 1180, 100, False, t, col="#5DADE2")
        text(c, "1 bó: ↺", 860, 960, "xbold", 54, "#F4C430", align="center", stroke=6, stroke_color="#1A120D")
        text(c, "3 bó: ↻", 860, 1340, "xbold", 54, "#5DADE2", align="center", stroke=6, stroke_color="#1A120D")


def sc_twist(c, t, n):
    ta, u = loc(n, t)
    if n == "twist1":
        braid_scene(c, t, ta, "bundles")
    elif n == "twist2":
        braid_scene(c, t, ta, "braid")
    else:
        braid_scene(c, t, ta, "sum")
        say_at(c, n, t, 540, 420, (450, 760))


def sc_grip(c, t):
    ta, u = loc("grip", t)
    bench(c, t)
    sq = 1 - 0.12 * (0.5 + 0.5 * math.sin(ta * 6))
    strand(c, 140, 940, 1040, 130 * sq, 1.6, -ta * 0.6, col="#D8B878", dark="#8C6E3E", direction=-1)
    for sd in (-1, 1):
        for k in range(3):
            x = 300 + k * 240
            y0 = 1040 + sd * 150
            c.drawLine(x, y0, x, y0 - sd * 50, P("#F4C430", stroke=12))
            tri = skia.Path(); tri.moveTo(x - 20, y0 - sd * 50); tri.lineTo(x + 20, y0 - sd * 50); tri.lineTo(x, y0 - sd * 80); tri.close()
            fo(c, tri, "#F4C430", ow=4)
    say_at(c, "grip", t, 540, 520, (540, 900))


def sc_pull(c, t):
    ta, u = loc("pull", t)
    K = Cam(600, 980, 1.5); K.on(c)
    forest_bg(c, t)
    k = ease_out(clamp(ta / 0.5))
    shake_ = 4 * math.sin(ta * 40) * k
    ch(c, "bop", BXF, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, hand_l=(-170 + shake_, 40), hand_r=(190 - shake_, 40),
       eyes="squint", mouth="chatter", brow_tilt=0.8, blush=0.6, crouch=0.3, lean=-4 * k, shiver=0.3 * k)
    lx, ly = hand_world("bop", BXF, GROUND, GS, -1, (-170, 40), side=-1, crouch=0.3)
    rx_, ry_ = hand_world("bop", BXF, GROUND, GS, -1, (190, 40), side=1, crouch=0.3)
    rope_line(c, [(lx, ly), (rx_, ry_)], w=14)
    K.off(c)
    if ta > 1.0:
        text(c, "KHÔNG ĐỨT!", W / 2, 620, "xbold", 110, "#F4C430", a=255 * pop(t, T["pull"][0] + 1.0), align="center", stroke=10,
             stroke_color="#1A120D")
    stars_burst(c, 540, 900, t, T["pull"][0] + 1.0)


def sc_share(c, t, n):
    ta, u = loc(n, t)
    bench(c, t)
    if n == "share1":
        # một sợi: mũi tên to (đứt) | nhiều sợi: chia nhỏ lực
        panel(c, 540, 1080, 960, 760, 1.0, col="#FBF7EE")
        sinew(c, 160, 900, 480, 900, w=6, col="#E3C48E")
        c.drawLine(480, 900, 520, 900, P("#C0392B", stroke=16))
        tri = skia.Path(); tri.moveTo(520, 870); tri.lineTo(570, 900); tri.lineTo(520, 930); tri.close(); fo(c, tri, "#C0392B", ow=4)
        check_mark(c, 330, 800, False, pop(t, T[n][0] + 0.4))
        for k in range(6):
            y = 1150 + k * 36
            sinew(c, 160, y, 760, y, w=6, col="#E3C48E")
            c.drawLine(760, y, 800, y, P("#2E8B57", stroke=8))
            tr = skia.Path(); tr.moveTo(800, y - 12); tr.lineTo(824, y); tr.lineTo(800, y + 12); tr.close(); fo(c, tr, "#2E8B57", ow=3)
        check_mark(c, 900, 1150, True, pop(t, T[n][0] + 0.9))
    else:
        strand(c, 140, 940, 1040, 130, 1.6, -ta * 0.3, col="#D8B878", dark="#8C6E3E", direction=-1)
        for k in range(5):
            x = 240 + k * 150
            zz = skia.Path(); zz.moveTo(x - 20, 1000)
            for j in range(4):
                zz.lineTo(x - 20 + j * 14, 1000 + (16 if j % 2 else -16) + 6 * math.sin(t * 20 + k))
            c.drawPath(zz, P("#FFFFFF", stroke=6))
        text(c, "BÁM CHẶT", W / 2, 1300, "xbold", 90, "#F4C430", a=255 * pop(t, T[n][0] + 0.6), align="center", stroke=8,
             stroke_color="#1A120D")
    say_at(c, n, t, 540, 470, (540, 700))


def sc_tie(c, t):
    ta, u = loc("tie", t)
    K = Cam(600, 980, 1.35); K.on(c)
    forest_bg(c, t)
    if ta < 1.2:
        wood_bundle(c, BXF - 140, GROUND - 60, 0.85, n=7, tied=ta > 0.8)
        ch(c, "bop", BXF + 40, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, crouch=1.0,
           hand_r=(110 + 40 * math.sin(ta * 14), 120), hand_l=(60, 140), eyes="squint", look=(-1, 1), mouth="tongue")
    else:
        up = back_out(clamp((ta - 1.2) / 0.4))
        hx, hy = hand_world("bop", BXF + 40, GROUND, GS, -1, (90, lerp(100, -170, up)), side=1)
        ch(c, "bop", BXF + 40, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, hand_r=(90, lerp(100, -170, up)), hand_l=(-60, 60),
           eyes="happy", mouth="grin")
        rope_line(c, [(hx, hy), (hx, hy + 80)], w=8)
        wood_bundle(c, hx, hy + 170, 0.85, n=7, tied=True, wobble=0.6, t=t)
    K.off(c)
    sfx_word(c, "THẮT!", 360, 640, t, T["tie"][0] + 0.8, size=100, color="white", dur=0.5)
    if ta > 1.4:
        text(c, "KHÔNG RƠI KHÚC NÀO!", W / 2, 520, "xbold", 74, "#F4C430", a=255 * pop(t, T["tie"][0] + 1.5), align="center", stroke=8,
             stroke_color="#1A120D")
        stars_burst(c, 540, 800, t, T["tie"][0] + 1.5)


# ================================================================ CẢNH 3 — Gầm phát hiện
TG, TB = 330, 760


def two(c, t, gkw, bkw, K=None, tied_bundle=True):
    K = K or Cam(545, 1000, 1.15)
    K.on(c)
    forest_bg(c, t)
    if tied_bundle:
        wood_bundle(c, 900, GROUND - 60, 0.75, n=7, tied=True)
    bkw = dict(bkw); gkw = dict(gkw)
    ch(c, "bop", TB, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, **bkw)
    gx = gkw.pop("x", TG)
    gface = gkw.pop("face", 1)
    ch(c, "gam", gx, GROUND, GS, t, face=gface, outfit="bigcoat", **gkw)
    return K


def sc_worm(c, t):
    ta, u = loc("worm", t)
    K = two(c, t, dict(hand_r=(170, -60), eyes="squint", mouth="grin", brow=0.6, lean=-4),
            dict(hand_r=(60, -60), prop_r=coil_prop, eyes="open", look=(-1, 0), mouth="flat"))
    K.off(c)
    say(c, "worm", K, TG, GROUND, GS, t, bx=500)


def sc_rope(c, t):
    ta, u = loc("rope", t)
    K = two(c, t, dict(hand_l=(60, 60), hand_r=(40, 60), eyes="squint", mouth="smirk", look=(1, 0)),
            dict(hand_r=(80, -120), prop_r=coil_prop, hand_l=(-80, -100 + 20 * math.sin(ta * 5)), eyes="open", look=(-1, 0), brow=0.4))
    K.off(c)
    p = pop(t, T["rope"][0] + 0.6, 0.4)
    panel(c, 540, 1560, 900, 330, p)
    if p > 0.5:
        icons = [("BUỘC", lambda: wood_bundle(c, 260, 1580, 0.5, n=7, tied=True)),
                 ("KÉO", lambda: rope_line(c, [(470, 1560), (620, 1560)], w=12)),
                 ("TREO", lambda: (rope_line(c, [(820, 1440), (820, 1540)], w=10), hide_sheet(c, 820, 1600, 120, 90)))]
        for i, (lab, fn) in enumerate(icons):
            if t > T["rope"][0] + 0.8 + i * 0.4:
                fn()
                text(c, lab, 260 + i * 280, 1690, "xbold", 44, "#7A3A1A", align="center")
    say(c, "rope", K, TB, GROUND, GS, t, who="bop", bx=600)


def sc_stomp(c, t):
    ta, u = loc("stomp", t)
    st = abs(math.sin(ta * 8)) if ta < 1.0 else 0
    grab = ta > 1.2
    K = two(c, t, dict(feet_air=30 * st, hand_r=(260, -60) if grab else (100, 40), prop_r=coil_prop if ta > 1.5 else None,
                       eyes="angry", brow_tilt=1.0, mouth="shout", vein=1.0, lean=10 * grab),
            dict(hand_r=(60, -60), prop_r=None if ta > 1.5 else coil_prop, eyes="wide", look=(-1, 0), mouth="o"))
    K.off(c)
    sfx_word(c, "DẬM! DẬM!", 340, 1520, t, T["stomp"][0] + 0.2, size=80, color="white", dur=0.9)
    say(c, "stomp", K, TG, GROUND, GS, t, bx=500)


def sc_tug(c, t):
    ta, u = loc("tug", t)
    hard = ta > 1.3
    k = 4 * math.sin(ta * 40)
    hl, hr = (-170 + k, 50), (190 - k, 50)
    K = two(c, t, dict(hand_l=hl, hand_r=hr, eyes="squint", mouth="chatter", brow_tilt=1.0, blush=0.6 + 0.4 * hard, vein=1.0 if hard else 0.0,
                       crouch=0.3 + 0.3 * hard, shiver=0.3 + 0.5 * hard, squash=1 - 0.05 * hard),
            dict(hand_l=(60, 110), hand_r=(-20, 110), eyes="open", look=(-1, 0), mouth="flat"))
    lx, ly = hand_world("gam", TG, GROUND, GS, 1, hl, side=-1, crouch=0.3 + 0.3 * hard)
    rx_, ry_ = hand_world("gam", TG, GROUND, GS, 1, hr, side=1, crouch=0.3 + 0.3 * hard)
    rope_line(c, [(lx, ly), (rx_, ry_)], w=14)
    K.off(c)
    sfx_word(c, "HỰỰỰ!", 340, 600, t, T["tug"][0] + 0.3, size=100, color="white", dur=1.0)
    sfx_word(c, "HỰỰỰỰỰ!!", 380, 600, t, T["tug"][0] + 1.4, size=120, color="#F4C430", dur=1.1)


def sc_wrap(c, t, n="wrap"):
    ta, u = loc(n, t)
    if n == "wrap":
        p = ease_in_out(clamp(ta / 2.8))
        face = 1 if int(ta * 6) % 2 == 0 else -1
        bk = dict(eyes="open", look=(-1, 0), mouth="flat", hand_l=(60, 110), hand_r=(-20, 110))
    else:
        p = 1 - ease_in_out(clamp(ta / 1.4))
        face = 1 if int(ta * 8) % 2 == 0 else -1
        bk = dict(eyes="squint", mouth="flat", hand_r=(160 + 40 * math.sin(ta * 16), -80), hand_l=(-40, 60))
    K = two(c, t, dict(face=face, turn=0.0, hand_l=(-30, 140), hand_r=(30, 140), eyes="squint" if n == "wrap" else "dizzy",
                       mouth="chatter" if n == "wrap" else "wavy", crouch=0.1), bk)
    cocoon(c, TG, GROUND, GS, p, t)
    if n == "free":
        rope_coil(c, TG + 200, GROUND - 20, 0.5 + 0.5 * (1 - p))
    else:
        rope_line(c, sag_pts(TG + 120, GROUND - 200 * GS, TG + 300, GROUND - 10, sag=40), w=12)
    K.off(c)
    sfx_word(c, "VÒNG… VÒNG…" if n == "wrap" else "GỠ… GỠ…", 380, 600, t, T[n][0] + 0.3, size=90, color="white", dur=2.2)


def sc_cocoon(c, t, n):
    ta, u = loc(n, t)
    K = two(c, t, dict(turn=0.0, hand_l=(-30, 140), hand_r=(30, 140), eyes="wide" if n == "cocoon" else "open", look=(1, 0),
                       mouth="flat" if n == "cocoon" else "frown", brow_tilt=-0.8, sweat=1.0 if n == "kidnap" else 0.0,
                       feet_air=20 * abs(math.sin(ta * 6)) if n == "kidnap" else 0),
            dict(eyes="open", look=(-1, 0), mouth="flat", brow=-0.4, hand_l=(60, 110), hand_r=(-20, 110)), K=Cam(500, 980, 1.35))
    cocoon(c, TG, GROUND - (20 * abs(math.sin(ta * 6)) if n == "kidnap" else 0), GS, 1.0, t)
    K.off(c)
    if n == "cocoon":
        text(c, "…", 760, 600, "xbold", 140, "white", a=255 * pop(t, T[n][0] + 0.8), align="center", stroke=10, stroke_color="#1A120D")
    else:
        say(c, n, K, TG, GROUND, GS, t, bx=500)


def sc_throw(c, t):
    ta, u = loc("throw", t)
    wind = ta < 0.5
    K = two(c, t, dict(hand_r=(-120, -160) if wind else (220, -150), prop_r=coil_prop if wind else None, eyes="angry", mouth="shout",
                       lean=-12 if wind else 14, brow_tilt=1.0),
            dict(eyes="wide", look=(1, -1), mouth="o", hand_l=(60, 110), hand_r=(-20, 110)))
    if not wind:
        q = clamp((ta - 0.5) / 0.9)
        rope_coil(c, lerp(TG + 200, 1300, q), lerp(GROUND - 450, 400, q) + 400 * q * q, 0.6, q * 720)
    K.off(c)
    sfx_word(c, "VÚT!", 760, 520, t, T["throw"][0] + 0.5, size=120, color="white", dur=0.6)


def sc_useless(c, t):
    ta, u = loc("useless", t)
    K = two(c, t, dict(hand_r=(160, -150), hand_l=(-60, -150), eyes="angry", brow_tilt=1.0, mouth="shout", vein=1.0,
                       feet_air=20 * abs(math.sin(ta * 8))),
            dict(eyes="open", brow_tilt=-1.0, mouth="frown", look=(-1, 0), hand_l=(60, 110), hand_r=(-20, 110)))
    K.off(c)
    c.save(); shake(c, t, T["useless"][0] + 0.15, 14)
    say(c, "useless", K, TG, GROUND, GS, t, bx=420)
    c.restore()


def sc_fall(c, t):
    ta, u = loc("fall", t)
    K = Cam(640, 1450, 0.85); K.on(c)
    ravine_bg(c, t, tone="morning" if False else "after", rope_on_ledge=ta > 1.5)
    if ta < 1.5:
        q = ta / 1.5
        rope_coil(c, lerp(900, LEDGE_X + 70, q), lerp(700, LEDGE_Y - 22, q * q), 0.55, q * 900)
    K.off(c)
    text(c, "…", W / 2, 520, "xbold", 140, "white", a=255 * pop(t, T["fall"][0] + 1.5), align="center", stroke=10, stroke_color="#1A120D")


def sc_lost(c, t):
    ta, u = loc("lost", t)
    K = Cam(760, 920, 1.9); K.on(c)
    forest_bg(c, t)
    lf = ease_out(clamp(ta / 0.6))
    ch(c, "bop", TB, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, head_squash=1 + 0.45 * lf, eyes="open",
       look=(-0.5, 1), brow=0.6 * lf, brow_tilt=-1.2, mouth="frown", head_tilt=-4)
    cx_, cy_ = TB, GROUND - 780 - 20 * math.sin(ta * 2)
    for dx, r in [(-40, 40), (0, 54), (44, 38)]:
        c.drawCircle(cx_ + dx, cy_, r * lf, P("#6A7280"))
    for k in range(4):
        q = (ta * 1.8 + k / 4) % 1
        c.drawLine(cx_ - 40 + k * 26, cy_ + 40 + q * 120, cx_ - 44 + k * 26, cy_ + 60 + q * 120, P("#5DADE2", 255 * lf * (1 - q), stroke=5))
    K.off(c)
    say(c, "lost", K, TB, GROUND, GS, t, who="bop", bx=540, by=320)


# ================================================================ CẢNH 4 — chiều, khe núi
RS = 0.8  # tỉ lệ nhân vật ở khe núi


def gam_r(c, t, x, y, **kw):
    kw.setdefault("outfit", "bigcoat")
    kw.setdefault("face", 1)
    return ch(c, "gam", x, y, RS, t, **kw)


def bop_edge(c, t, x=470, **kw):
    kw.setdefault("face", 1)
    return ch(c, "bop", x, PLAT_Y, RS, t, outfit="coat", collar_up=1.0, **kw)


def sc_rabbit(c, t):
    ta, u = loc("rabbit", t)
    K = Cam(440, 1000, 1.1); K.on(c)
    ravine_bg(c, t)
    hp = (ta * 1.6) % 1
    rabbit(c, lerp(-60, 420, u), PLAT_Y - 10, 1.0, t, face=1, hop=hp)
    gam_r(c, t, 120, PLAT_Y, eyes="wide", look=(1, 0), mouth="tongue", brow=0.8, hand_l=(60, 40), hand_r=(40, 40))
    K.off(c)
    sfx_word(c, "TƯNG TƯNG", 600, 640, t, T["rabbit"][0] + 0.3, size=80, color="white", dur=1.5)


def sc_dinner(c, t):
    ta, u = loc("dinner", t)
    K = Cam(440, 1000, 1.1); K.on(c)
    ravine_bg(c, t)
    rabbit(c, lerp(420, 520, u), PLAT_Y - 10, 1.0, t, face=1, hop=(ta * 2.4) % 1)
    gam_r(c, t, lerp(120, 360, u), PLAT_Y, walk=ta * 14, stride=1.6, lean=16, hand_l=(150, -80), hand_r=(180, -40), eyes="wide",
          mouth="shout", look=(1, 0), lag=-30)
    K.off(c)
    say(c, "dinner", K, lerp(120, 360, u), PLAT_Y, RS, t, bx=480)


def sc_leap(c, t):
    ta, u = loc("leap", t)
    K = Cam(640, 1000, 1.0); K.on(c)
    ravine_bg(c, t)
    q = clamp(ta / 0.9)
    rabbit(c, lerp(520, 1010, ease_in_out(q)), PLAT_Y - 10 - 260 * math.sin(math.pi * q), 1.0, t, face=1)
    gam_r(c, t, lerp(360, 540, u), PLAT_Y, walk=ta * 14, stride=1.6, lean=16, hand_l=(150, -80), hand_r=(180, -40), eyes="wide",
          mouth="shout", look=(1, -0.5), lag=-30)
    K.off(c)
    sfx_word(c, "VÚT!", 760, 640, t, T["leap"][0] + 0.2, size=100, color="white", dur=0.6)


def sc_air(c, t):
    ta, u = loc("air", t)
    K = Cam(660, 1100, 1.25); K.on(c)
    ravine_bg(c, t)
    rabbit(c, 1010, PLAT_Y - 10, 1.0, t, face=-1)
    x = lerp(600, 690, ease_out(clamp(ta / 0.4)))
    gulp = ta > 1.3
    gam_r(c, t, x, PLAT_Y, walk=ta * 22 if not gulp else ta * 30, stride=1.3, eyes="wide", look=(0, 1) if not gulp else (0.3, 0.2),
          mouth="o" if not gulp else "wavy", brow=1.0, hand_l=(60, 40), hand_r=(40, 40), sweat=1.0 * gulp)
    for k in range(5):
        q = (ta * 2 + k / 5) % 1
        c.drawCircle(x - 60 - q * 120, PLAT_Y - 20 - q * 30, 20 * (1 - q) + 6, P("#FFFFFF", 160 * (1 - q)))
    K.off(c)
    if gulp:
        sfx_word(c, "ỰC…", 760, 700, t, T["air"][0] + 1.4, size=100, color="white", dur=0.8)


def sc_aaa(c, t):
    ta, u = loc("aaa", t)
    q = clamp((ta - 0.25) / 1.55)
    y = PLAT_Y + (LEDGE_Y - 120 - PLAT_Y) * q * q
    K = Cam(660, lerp(1100, 1500, q), lerp(1.25, 1.0, q)); K.on(c)
    ravine_bg(c, t)
    gam_r(c, t, 690, y, squash=1 + 0.18 * q, hand_l=(-120, -230), hand_r=(120, -230), eyes="wide", mouth="shout", brow=1.0, lag=40 * q,
          feet_air=10)
    for k in range(6):
        c.drawLine(640 + k * 22, y - 520 * RS - k * 30, 640 + k * 22, y - 520 * RS - 140 - k * 30, P("#FFFFFF", 150 * q, stroke=6))
    K.off(c)
    sx, sy = K.map(690, y - 560 * RS)
    comic_bubble(c, 540, 380, T["aaa"][2][5], "shout", (sx, sy), pop(t, T["aaa"][0] + 0.1))


def sc_ledge(c, t):
    ta, u = loc("ledge", t)
    out = ease_in_out(clamp((ta - 0.9) / 0.9))
    K = Cam(lerp(660, 620, out), lerp(1550, 1500, out), lerp(1.1, 0.8, out)); K.on(c)
    c.save(); shake(c, t, T["ledge"][0], 18, 0.4)
    ravine_bg(c, t)
    k = ta
    gam_r(c, t, LEDGE_X, LEDGE_Y - 20, squash=1 - 0.3 * math.exp(-k * 7) * math.cos(k * 25), eyes="dizzy", mouth="wavy",
          crouch=0.6 * math.exp(-k * 3))
    stars(c, LEDGE_X, LEDGE_Y - 520 * RS, t, T["ledge"][0] + 0.1) if False else stars_burst(c, LEDGE_X, LEDGE_Y - 500 * RS, t, T["ledge"][0] + 0.1)
    dust(c, LEDGE_X, LEDGE_Y - 20, t, T["ledge"][0], n=10, col="#C9BBA6")
    c.restore()
    K.off(c)
    sfx_word(c, "BỊCH!", 540, 700, t, T["ledge"][0] + 0.02, size=150, color="#F4C430", dur=0.7)
    if ta > 1.2:
        ux, uy = K.map(EDGE_L - 120, PLAT_Y - 60)
        dx, dy = K.map(EDGE_L + 160, 2300)
        text(c, "↑ không với tới", ux, uy, "xbold", 50, "white", a=255 * pop(t, T["ledge"][0] + 1.3), align="center", stroke=6,
             stroke_color="#1A120D")
        text(c, "↓ sâu hun hút", dx, min(dy, 1820), "xbold", 50, "white", a=255 * pop(t, T["ledge"][0] + 1.6), align="center", stroke=6,
             stroke_color="#1A120D")


WIDE = Cam(560, 1420, 0.82)


def sc_help(c, t):
    ta, u = loc("help", t)
    K = WIDE; K.on(c)
    ravine_bg(c, t)
    w = math.sin(ta * 12)
    gam_r(c, t, LEDGE_X, LEDGE_Y - 20, hand_l=(-80 + 30 * w, -260), hand_r=(80 - 30 * w, -260), eyes="wide", look=(-0.5, -1),
          mouth="shout", brow_tilt=-1.0, sweat=1.0, feet_air=15 * abs(w))
    if ta > 1.1:
        bop_edge(c, t, x=lerp(150, 470, ease_out(clamp((ta - 1.1) / 0.8))), walk=ta * 12, eyes="wide", mouth="o", look=(1, 1))
    K.off(c)
    say(c, "help", K, LEDGE_X, LEDGE_Y - 20, RS, t, bx=760, by=980)


def sc_look(c, t):
    ta, u = loc("look", t)
    K = WIDE; K.on(c)
    ravine_bg(c, t)
    gam_r(c, t, LEDGE_X, LEDGE_Y - 20, eyes="wide", look=(-0.5, -1), mouth="frown", brow_tilt=-1.0, sweat=0.6, hand_l=(60, 40), hand_r=(40, 40))
    bop_edge(c, t, crouch=0.6, lean=14, eyes="open", look=(1, 1), mouth="flat", hand_r=(90, 20), hand_l=(-60, 40))
    K.off(c)
    say(c, "look", K, 470, PLAT_Y, RS, t, who="bop", crouch=0.6, bx=480, by=420)


def sc_spot(c, t, n="spot"):
    ta, u = loc(n, t)
    K = Cam(LEDGE_X + 20, LEDGE_Y - 220, 2.1); K.on(c)
    ravine_bg(c, t, rope_on_ledge=n == "spot")
    if n == "spot":
        g = paint("#FFF6C8", 150 * (0.5 + 0.5 * math.sin(ta * 8)) * (ta > 1.0)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 20))
        c.drawCircle(LEDGE_X + 70, LEDGE_Y - 22, 60, g)
        lk = (math.sin(ta * 4), 0.2) if ta < 1.0 else (0.8, 1.0)
        gam_r(c, t, LEDGE_X - 20, LEDGE_Y - 20, eyes="open" if ta < 1.0 else "wide", look=lk, mouth="frown" if ta < 1.0 else "o",
              hand_l=(60, 40), hand_r=(40, 40), head_tilt=8 * (ta > 1.0))
    else:
        gam_r(c, t, LEDGE_X - 20, LEDGE_Y - 20, eyes="squint", look=(0.3, 0.5), mouth="smile", blush=0.8, sweat=1.0,
              hand_r=(60, -40), prop_r=coil_prop, hand_l=(40, 40))
    K.off(c)
    if n == "spot" and ta > 1.0:
        text(c, "!", 540, 700, "xbold", 200, "#F4C430", a=255 * pop(t, T[n][0] + 1.0), align="center", stroke=12, stroke_color="#1A120D")
    if n == "worm2":
        say(c, n, K, LEDGE_X - 20, LEDGE_Y - 20, RS, t, bx=540, by=520)


def sc_toss(c, t):
    ta, u = loc("toss", t)
    K = WIDE; K.on(c)
    ravine_bg(c, t, rope_on_ledge=False)
    gam_r(c, t, LEDGE_X, LEDGE_Y - 20, hand_r=(60, -40), prop_r=coil_prop, eyes="open", look=(-0.5, -1), mouth="flat", hand_l=(40, 40))
    bop_edge(c, t, crouch=0.4, lean=10, eyes="open", look=(1, 1), mouth="shout", hand_r=(40, -200), hand_l=(-40, -200))
    K.off(c)
    say(c, "toss", K, 470, PLAT_Y, RS, t, who="bop", crouch=0.4, bx=480, by=420)


def sc_miss(c, t):
    ta, u = loc("miss", t)
    K = WIDE; K.on(c)
    ravine_bg(c, t, rope_on_ledge=False)
    hx, hy = LEDGE_X + 60, LEDGE_Y - 330 * RS
    if ta < 1.0:
        q = ta / 1.0
        ex, ey = lerp(hx, 540, q), hy - 520 * math.sin(math.pi * q)
        bop_kw = dict(hand_r=(120, -60), hand_l=(-40, 40), eyes="wide", mouth="o")
        gam_kw = dict(hand_r=(60, -200), eyes="open", look=(-0.3, -1), mouth="shout")
    elif ta < 2.3:
        q = clamp((ta - 1.0) / 0.9)
        ex, ey = lerp(hx, LEDGE_X + 10, q), hy - 560 * math.sin(math.pi * min(q, 0.999)) + (0 if q < 1 else 0) - (120 if q >= 1 else 0)
        hit = ta > 1.9
        bop_kw = dict(hand_r=(-20, -200), hand_l=(-90, -200), eyes="closed" if hit else "open", mouth="frown")
        gam_kw = dict(hand_r=(60, -200) if not hit else (40, 40), eyes="dizzy" if hit else "open", look=(-0.3, -1), mouth="wavy" if hit else "shout",
                      head_squash=1 - 0.2 * math.exp(-(ta - 1.9) * 6) if hit else 1.0)
    else:
        q = clamp((ta - 2.3) / 0.6)
        cx_, cy_ = hand_world("bop", 470, PLAT_Y, RS, 1, (120, -80), side=1, crouch=0.3)
        ex, ey = lerp(hx, cx_, ease_out(q)), lerp(hy, cy_, ease_out(q)) - 240 * math.sin(math.pi * q)
        caught = q >= 1
        bop_kw = dict(hand_r=(120, -80), hand_l=(-40, 40), eyes="happy" if caught else "wide", mouth="grin" if caught else "o", crouch=0.3)
        gam_kw = dict(hand_r=(60, -200), eyes="wide", look=(-0.3, -1), mouth="o")
    gam_r(c, t, LEDGE_X, LEDGE_Y - 20, hand_l=(40, 40), **gam_kw)
    bop_edge(c, t, lean=8, **bop_kw)
    rope_coil(c, LEDGE_X + 80, LEDGE_Y - 30, 0.4)
    rope_line(c, sag_pts(LEDGE_X + 80, LEDGE_Y - 40, ex, ey, sag=60, n=18), w=10)
    K.off(c)
    sfx_word(c, "HỤT!", 760, 700, t, T["miss"][0] + 0.8, size=110, color="white", dur=0.5)
    sfx_word(c, "BỘP!", 760, 1240, t, T["miss"][0] + 1.9, size=120, color="#F4C430", dur=0.6)
    sfx_word(c, "CHỘP!", 360, 600, t, T["miss"][0] + 2.9, size=120, color="#F4C430", dur=0.6)


def sc_anchor(c, t):
    ta, u = loc("anchor", t)
    K = Cam(420, 1250, 0.95); K.on(c)
    p = clamp(ta / 1.8)
    ravine_bg(c, t, rope_on_ledge=False, anchor=p, rope_down=False)
    rope_line(c, [(TREE_X + 46, PLAT_Y - 90), (EDGE_L, PLAT_Y - 6), (EDGE_L + 4, LEDGE_Y - 30)], w=12)
    side = 1 if int(ta * 5) % 2 == 0 else -1
    ch(c, "bop", TREE_X + 120 * side if ta < 1.8 else TREE_X + 140, PLAT_Y, RS, t, face=-side if ta < 1.8 else 1, outfit="coat",
       collar_up=1.0, hand_r=(90, -40), hand_l=(-40, -20), eyes="squint", mouth="tongue" if ta < 1.8 else "grin")
    K.off(c)
    sfx_word(c, "QUẤN… QUẤN…", 560, 520, t, T["anchor"][0] + 0.2, size=80, color="white", dur=1.6)
    sfx_word(c, "THẮT!", 560, 640, t, T["anchor"][0] + 1.9, size=110, color="#F4C430", dur=0.5)


def sc_fric(c, t):
    ta, u = loc("fric", t)
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9B97A", "#F6E2B0")
    fo(c, rrect_path(330, -100, 420, H + 200, 60), "#6E5236", ow=10)
    for k in range(8):
        c.drawLine(380 + k * 45, -100, 390 + k * 45, H + 100, P("#5A4230", stroke=6))
    for k in range(3):
        yy = 1000 + k * 120
        rope_line(c, [(300, yy + 40), (780, yy - 40)], w=40)
    rope_line(c, [(780, 1040), (1200, 1180)], w=40)
    for k in range(4):
        x = 420 + k * 90
        zz = skia.Path(); zz.moveTo(x, 900)
        for j in range(4):
            zz.lineTo(x + j * 14, 900 + (14 if j % 2 else -14) + 5 * math.sin(t * 20 + k))
        c.drawPath(zz, P("#FFFFFF", stroke=6))
    text(c, "BÁM CHẶT, KHÔNG TRƯỢT", W / 2, 1520, "xbold", 70, "#F4C430", a=255 * pop(t, T["fric"][0] + 0.8), align="center", stroke=8,
         stroke_color="#1A120D")
    say_at(c, "fric", t, 540, 460, (540, 860))


def rope_scene(c, t, K):
    K.on(c)
    ravine_bg(c, t, rope_on_ledge=False, anchor=1.0, rope_down=True)


def sc_climb1(c, t):
    ta, u = loc("climb1", t)
    K = WIDE; rope_scene(c, t, K)
    gam_r(c, t, LEDGE_X - 20, LEDGE_Y - 20, face=-1, hand_r=(70, -200), hand_l=(40, -160), eyes="open", look=(1, -1), mouth="frown",
          brow_tilt=-0.8)
    bop_edge(c, t, crouch=0.4, lean=10, eyes="happy", mouth="grin", hand_r=(40, -200), hand_l=(-40, -200))
    K.off(c)
    say(c, "climb1", K, 470, PLAT_Y, RS, t, who="bop", crouch=0.4, bx=480, by=420)


def climber(c, t, y, ta, scratch=False, grit=False):
    alt = math.sin(ta * 6)
    hr = (lerp(10, 40, alt), -230 - 40 * alt)
    hl = (lerp(-10, 30, -alt), -200 + 40 * alt)
    if scratch:
        hr = scratch_hands(ta, 2.0)[0]
    gam_r(c, t, EDGE_L + 90, y, face=-1, hand_r=hr, hand_l=hl, walk=ta * 4 if not scratch else None, stride=0.5,
          eyes="wide" if scratch else ("squint" if grit else "open"), look=(0, -1), mouth="grin" if grit else ("o" if scratch else "frown"),
          brow_tilt=1.0 if grit else -0.6, sweat=1.0, vein=1.0 if grit else 0.0, lean=-6)
    if scratch:
        lice_on(c, EDGE_L + 90, y, RS, t, n=3)


def sc_climb(c, t, n="climb"):
    ta, u = loc(n, t)
    K = Cam(620, 1450, 1.0); rope_scene(c, t, K)
    bop_edge(c, t, crouch=0.6, lean=14, eyes="open", look=(1, 1), mouth="flat", hand_r=(90, 20), hand_l=(-60, 40))
    if n == "climb":
        climber(c, t, lerp(LEDGE_Y - 20, 1500, ease_in_out(u)), ta)
    else:
        slip = ease_out(clamp((ta - 0.8) / 0.3)) * 80
        climber(c, t, 1500 + slip, ta, scratch=True)
    K.off(c)
    if n == "itchy":
        sfx_word(c, "SỘT SỘT", 760, 1000, t, T[n][0] + 0.2, size=80, color="white", dur=0.7)
        sfx_word(c, "TUỘT!", 760, 1200, t, T[n][0] + 0.85, size=110, color="#F4C430", dur=0.6)


def sc_dont(c, t):
    ta, u = loc("dont", t)
    K = Cam(560, 1350, 1.0); rope_scene(c, t, K)
    bop_edge(c, t, crouch=0.3, lean=14, eyes="wide", mouth="shout", brow=1.0, hand_r=(120, -120), hand_l=(-40, -200), sweat=1.0)
    climber(c, t, 1580, 0.0)
    K.off(c)
    c.save(); shake(c, t, T["dont"][0] + 0.1, 16)
    say(c, "dont", K, 470, PLAT_Y, RS, t, who="bop", crouch=0.3, bx=480, by=420)
    c.restore()


def sc_grit(c, t):
    ta, u = loc("grit", t)
    K = Cam(560, lerp(1350, 1100, ease_in_out(clamp(ta / 1.4))), 1.0); rope_scene(c, t, K)
    if ta < 1.3:
        climber(c, t, lerp(1580, PLAT_Y + 40, ease_in(clamp(ta / 1.3)) if False else clamp(ta / 1.3) ** 1.3), ta * 1.8, grit=True)
        bop_edge(c, t, crouch=0.6, lean=14, eyes="open", look=(1, 1), mouth="o", hand_r=(90, 20), hand_l=(-60, 40))
    else:
        bop_edge(c, t, x=300, eyes="happy", mouth="smile", hand_r=(40, 40), hand_l=(-40, 40))
        c.save(); c.translate(440, PLAT_Y - 20); c.rotate(-80)
        ch(c, "gam", 0, 0, RS, t, face=1, outfit="bigcoat", eyes="closed", mouth="o", talk=0.5 + 0.4 * math.sin(ta * 10), sweat=1.0,
           hand_l=(-60, 40), hand_r=(60, 40))
        c.restore()
        hx, hy = 440 + 300, PLAT_Y - 120
        if int(ta * 3) % 2 == 0:
            breath(c, *K.map(hx, hy), t, T["grit"][0] + 1.3 + int((ta - 1.3) * 1.5) / 1.5, dirx=1, a=170)
    K.off(c)
    sfx_word(c, "HỘC… HỘC…", 560, 640, t, T["grit"][0] + 1.5, size=90, color="white", dur=1.0)


# ================================================================ CẢNH 5 — hoàng hôn, trước hang
CG, CB = 560, 860


def dusk(c, t):
    cave_exterior(c, t, night=0.0, morning=0.0, wind=False)


def sash(c, x, y, s, face=1):
    a = hand_world("gam", x, y, s, face, (0, 0), side=-1)
    b = hand_world("gam", x, y, s, face, (-10, 170), side=1)
    rope_line(c, [a, b], w=14 * s)
    rope_coil(c, b[0], b[1], 0.45 * s / 0.95)


def sc_coil(c, t):
    ta, u = loc("coil", t)
    K = Cam(620, 1000, 1.3); K.on(c)
    dusk(c, t)
    if ta < 1.2:
        sp = ta * 12
        ch(c, "gam", CG, GROUND, GS, t, face=1, outfit="bigcoat", hand_l=(80, -20), hand_r=(120 + 40 * math.cos(sp), -40 + 40 * math.sin(sp)),
           eyes="squint", mouth="tongue", look=(1, 0.5))
        rope_coil(c, *hand_world("gam", CG, GROUND, GS, 1, (80, -20), side=-1), 0.3 + 0.3 * u)
    else:
        ch(c, "gam", CG, GROUND, GS, t, face=1, outfit="bigcoat", hand_l=(40, 60), hand_r=(60, 60), eyes="happy", mouth="grin", lean=-6)
        sash(c, CG, GROUND, GS)
    K.off(c)


def sc_lifeline(c, t):
    ta, u = loc("lifeline", t)
    K = Cam(620, 1000, 1.2); K.on(c)
    dusk(c, t)
    ch(c, "bop", CB, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, eyes="open", look=(-1, 0), mouth="flat", brow_tilt=-0.6)
    ch(c, "gam", CG, GROUND, GS, t, face=1, outfit="bigcoat", hand_l=(-110, -220), hand_r=(140, -230), eyes="happy", mouth="grin",
       lean=-8, feet_air=25 * abs(math.sin(ta * 5)))
    sash(c, CG, GROUND - 25 * abs(math.sin(ta * 5)), GS)
    K.off(c)
    say(c, "lifeline", K, CG, GROUND, GS, t, bx=540)


def sc_mine(c, t):
    ta, u = loc("mine", t)
    K = Cam(620, 1000, 1.2); K.on(c)
    dusk(c, t)
    ch(c, "gam", CG, GROUND, GS, t, face=1, outfit="bigcoat", hand_l=(40, 60), hand_r=(60, 60), eyes="happy", mouth="smile")
    sash(c, CG, GROUND, GS)
    ch(c, "bop", CB, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, hand_r=(120, -60), eyes="open", look=(-1, 0),
       brow_tilt=-1.0, mouth="frown")
    K.off(c)
    say(c, "mine", K, CB, GROUND, GS, t, who="bop", bx=660)


def sc_allmine(c, t):
    ta, u = loc("allmine", t)
    k = min(2, int(ta / 0.9))
    hands = [((-60, 60), (40, -40)), ((200, -120), (-60, 40)), ((-170, -200), (170, -200))][k]
    K = Cam(620, 1000, 1.2); K.on(c)
    dusk(c, t)
    ch(c, "bop", CB, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, eyes="open", look=(-1, 0), brow_tilt=-1.0, mouth="frown")
    ch(c, "gam", CG, GROUND, GS, t, face=1, outfit="bigcoat", hand_l=hands[0], hand_r=hands[1], eyes="closed" if k == 2 else "happy",
       mouth="grin", head_tilt=-10 * (k == 2))
    sash(c, CG, GROUND, GS)
    K.off(c)
    say(c, "allmine", K, CG, GROUND, GS, t, bx=540)


def sc_tieall(c, t):
    ta, u = loc("tieall", t)
    k = min(2, int(ta / 1.0))
    q = (ta % 1.0)
    K = Cam(560, 1000, 1.35); K.on(c)
    dusk(c, t)
    if k == 0:
        stone_spear_v(c, CG - 60, GROUND - 120, 520, 0.9, ang=35)
        ch(c, "gam", CG, GROUND, GS, t, face=1, outfit="bigcoat", hand_l=(40, 60), hand_r=(60, 60), eyes="happy", mouth="grin")
        rope_line(c, [hand_world("gam", CG, GROUND, GS, 1, (0, 0), side=1), hand_world("gam", CG, GROUND, GS, 1, (-10, 160), side=-1)], w=14)
    elif k == 1:
        tree_trunk_front(c, 760, GROUND, 0.9)
        hide_sheet(c, 760, GROUND - 450, 220, 260, rot=-3, hole=True, col="#7A5A3A", dark="#3A2A1A")
        rope_line(c, [(640, GROUND - 520), (880, GROUND - 540)], w=14)
        ch(c, "gam", 430, GROUND, GS, t, face=1, outfit="bigcoat", hand_r=(160, -80), hand_l=(40, 60), eyes="happy", mouth="grin")
    else:
        wood_bundle(c, 640, GROUND - 60, 0.9, n=7, tied=True)
        ch(c, "gam", 400, GROUND, GS, t, face=1, outfit="bigcoat", hand_r=(150, 60 + 30 * math.sin(ta * 14)), hand_l=(40, 60), crouch=0.6,
           eyes="happy", mouth="grin")
    K.off(c)
    with Xf(c, 540, 520, -6, back_out(clamp(q / 0.25))):
        text(c, "BUỘC!", 0, 0, "xbold", 140, "#F4C430", align="center", stroke=12, stroke_color="#1A120D")


def tied_bop(c, t, angry=0.0, struggle=0.0):
    tree_trunk_front(c, CB, GROUND, 0.9)
    ch(c, "bop", CB, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, hand_l=(30, 120), hand_r=(-10, 120),
       eyes="angry" if angry else "wide", brow_tilt=1.0 if angry else -0.5, mouth="shout" if angry else "o",
       shiver=struggle, vein=angry)
    for k in range(3):
        yy = GROUND - (380 - k * 70) * GS
        rope_line(c, [(CB - 140, yy + 10), (CB + 140, yy - 10)], w=14)


def sc_tiebop(c, t):
    ta, u = loc("tiebop", t)
    K = Cam(700, 1000, 1.25); K.on(c)
    dusk(c, t)
    tied_bop(c, t)
    clap = math.sin(ta * 14)
    ch(c, "gam", CG, GROUND, GS, t, face=1, outfit="bigcoat", hand_l=(100 + 20 * clap, -40), hand_r=(80 - 20 * clap, -40), eyes="happy",
       mouth="grin")
    K.off(c)
    sfx_word(c, "PHỦI PHỦI", 360, 640, t, T["tiebop"][0] + 0.6, size=80, color="white", dur=1.0)


def sc_hey(c, t, n="hey"):
    ta, u = loc(n, t)
    K = Cam(700, 1000, 1.25); K.on(c)
    dusk(c, t)
    tied_bop(c, t, angry=1.0 if n == "hey" else 0.4, struggle=0.8 if n == "hey" else 0.3)
    if n == "hey":
        ch(c, "gam", CG, GROUND, GS, t, face=1, outfit="bigcoat", hand_l=(40, 60), hand_r=(60, 60), eyes="happy", mouth="smile")
    else:
        ch(c, "gam", CG + 60, GROUND, GS, t, face=1, outfit="bigcoat", hand_r=(150, -60 + 15 * math.sin(ta * 8)), hand_l=(40, 60), eyes="squint",
           mouth="smirk", brow=0.6)
    K.off(c)
    if n == "hey":
        say(c, n, K, CB, GROUND, GS, t, who="bop", bx=700)
    else:
        say(c, n, K, CG + 60, GROUND, GS, t, who="gam", bx=520)


def sc_trophy(c, t):
    ta, u = loc("trophy", t)
    K = Cam(560, 1000, 1.25); K.on(c)
    cave_in(c, t, door="morning", snow=False, fire_x=430, fire_s=0.6)
    stone_spear_v(c, 640, GROUND, 520, 0.95, ang=4)
    hide_sheet(c, 640, GROUND - 400, 200, 260, rot=2 + 3 * math.sin(t * 2), hole=True, col="#7A5A3A", dark="#3A2A1A")
    rope_coil(c, 660, GROUND - 640, 0.55)
    ch(c, "gam", 250, GROUND, 0.95, t, face=1, outfit="bigcoat", hand_l=(40, 110), hand_r=(-30, 110), eyes="happy", mouth="grin",
       head_tilt=-6, lean=-6)
    sash(c, 250, GROUND, 0.95)
    K.off(c)
    text(c, "CHIẾN LỢI PHẨM CỦA GẦM", W / 2, 420, "xbold", 64, "white", a=255 * pop(t, T["trophy"][0] + 0.2), align="center", stroke=7,
         stroke_color="#1A120D")
    for i, w in enumerate(["LỬA", "GIÁO", "ÁO", "DÂY"]):
        p = pop(t, T["trophy"][0] + 0.5 + i * 0.35, 0.3)
        if p > 0:
            with Xf(c, 180 + i * 240, 540, 0, back_out(p)):
                text(c, w, 0, 0, "xbold", 84, "#F4C430", align="center", stroke=9, stroke_color="#1A120D")


# ================================================================ CẢNH 6 — đêm
NX = 700


def branch(c, x0, y0, x1, y1, bend, string=False, pluck=0.0, t=0.0):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - bend
    p = skia.Path(); p.moveTo(x0, y0); p.quadTo(mx, my - bend * 0.3, x1, y1)
    c.drawPath(p, P(OUT, stroke=24)); c.drawPath(p, P("#8A6A44", stroke=15))
    if string:
        vib = pluck * 18 * math.sin(t * 90)
        s_ = skia.Path(); s_.moveTo(x0, y0); s_.quadTo(mx, (y0 + y1) / 2 + vib, x1, y1)
        c.drawPath(s_, P("#E3C48E", stroke=5))


def night(c, t):
    cave_exterior(c, t, night=1.0, wind=False)
    for k in range(30):
        x = (k * 173) % W; y = (k * 97) % 600 + 80
        c.drawCircle(x, y, 2 + (k % 3), P("#FFFFFF", 200 * (0.6 + 0.4 * math.sin(t * 3 + k))))


def sc_bend(c, t, n="bend"):
    ta, u = loc(n, t)
    K = Cam(680, 1000, 1.35); K.on(c)
    night(c, t)
    bend = 30 + 70 * ease_out(clamp(ta / 1.2)) if n == "bend" else 100
    ch(c, "bop", NX, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, crouch=1.0, hand_l=(-30, 70), hand_r=(200, 70),
       eyes="squint" if n == "bend" else ("wide" if ta > 0.5 else "open"), look=(-0.6, 0.4), mouth="tongue" if n == "bend" else "o")
    lx, ly = hand_world("bop", NX, GROUND, GS, -1, (-30, 70), side=-1, crouch=1.0)
    rx_, ry_ = hand_world("bop", NX, GROUND, GS, -1, (200, 70), side=1, crouch=1.0)
    pl = 0.0
    if n == "twang":
        pl = math.exp(-max(0, ta - 0.4) * 4) * (ta > 0.4)
    branch(c, lx, ly, rx_, ry_, bend, string=(n != "bend" or ta > 1.4), pluck=pl, t=t)
    if n == "twang":
        if ta < 0.4:
            needle_like = (lerp(lx, rx_, 0.5), (ly + ry_) / 2 - 10)
            c.drawLine(needle_like[0] - 5, needle_like[1], needle_like[0] - 5, needle_like[1] - 90, P(OUT, stroke=10))
            c.drawLine(needle_like[0] - 5, needle_like[1], needle_like[0] - 5, needle_like[1] - 90, P("#C9A06A", stroke=6))
        else:
            q = clamp((ta - 0.4) / 0.9)
            sx0, sy0 = lerp(lx, rx_, 0.5), (ly + ry_) / 2 - 50
            px, py = sx0 - q * 900, sy0 - 300 * math.sin(math.pi * q * 0.8)
            for k in range(6):
                c.drawCircle(px + k * 40, py + k * 6, 6 - k * 0.8, P("#F4D03F", 200 * (1 - k / 6)))
            with Xf(c, px, py, -70 + q * 30, 1):
                c.drawLine(0, 0, 0, -90, P(OUT, stroke=10)); c.drawLine(0, 0, 0, -90, P("#C9A06A", stroke=6))
    K.off(c)
    if n == "bend":
        sfx_word(c, "UỐN…", 380, 640, t, T[n][0] + 0.3, size=90, color="white", dur=1.0)
        sfx_word(c, "BUỘC!", 380, 640, t, T[n][0] + 1.5, size=90, color="#F4C430", dur=0.7)
    else:
        sfx_word(c, "TƯNG!", 560, 620, t, T[n][0] + 0.4, size=150, color="#F4C430", dur=0.8)
        sfx_word(c, "VÚT…", 260, 900, t, T[n][0] + 0.8, size=90, color="white", dur=0.9)


def bow_icon(c, x, y, s):
    with Xf(c, x, y, 0, s):
        p = skia.Path(); p.moveTo(-40, -120); p.quadTo(60, 0, -40, 120)
        c.drawPath(p, P(OUT, stroke=18)); c.drawPath(p, P("#8A6A44", stroke=11))
        c.drawLine(-40, -120, -40, 120, P("#E3C48E", stroke=4))
        c.drawLine(-60, 0, 120, 0, P(OUT, stroke=10)); c.drawLine(-60, 0, 120, 0, P("#C9A06A", stroke=6))
        tri = skia.Path(); tri.moveTo(120, -14); tri.lineTo(150, 0); tri.lineTo(120, 14); tri.close(); fo(c, tri, "#9AA3A8", ow=4)


def sc_idea(c, t):
    ta, u = loc("idea", t)
    K = Cam(680, 1000, 1.35); K.on(c)
    night(c, t)
    ch(c, "bop", NX, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, crouch=1.0, hand_l=(-30, 70), hand_r=(200, 70),
       eyes="wide", look=(-1, -0.6), brow=1.0, mouth="o")
    lx, ly = hand_world("bop", NX, GROUND, GS, -1, (-30, 70), side=-1, crouch=1.0)
    rx_, ry_ = hand_world("bop", NX, GROUND, GS, -1, (200, 70), side=1, crouch=1.0)
    branch(c, lx, ly, rx_, ry_, 100, string=True)
    K.off(c)
    say(c, "idea", K, NX, GROUND, GS, t, who="bop", crouch=1.0, bx=620, by=420, d=0.2)
    if ta > 0.9:
        bow_icon(c, 600, 430, 0.7 * back_out(pop(t, T["idea"][0] + 0.9)))


def sc_useless2(c, t):
    ta, u = loc("useless2", t)
    K = Cam(500, 1000, 1.2); K.on(c)
    night(c, t)
    for sd in (-1, 1):
        c.drawOval(skia.Rect.MakeXYWH(240 + sd * 30 - 12, 1000 - 8, 24, 16), P("#F4D03F"))
    ch(c, "bop", NX, GROUND, GS, t, face=-1, outfit="coat", collar_up=1.0, crouch=1.0, hand_l=(-30, 70), hand_r=(200, 70),
       eyes="squint", look=(-1, 0), mouth="smile")
    lx, ly = hand_world("bop", NX, GROUND, GS, -1, (-30, 70), side=-1, crouch=1.0)
    rx_, ry_ = hand_world("bop", NX, GROUND, GS, -1, (200, 70), side=1, crouch=1.0)
    branch(c, lx, ly, rx_, ry_, 100, string=True)
    tx, ty = K.map(240, 960)
    K.off(c)
    say_at(c, "useless2", t, 420, 520, (tx, ty))


def sc_black(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000"))


def sc_card(c, t):
    a, b = beat("card")
    grad_rect(c, skia.Rect.MakeWH(W, H), "#1A120D", "#0B0806")
    strand(c, 140, 940, 1560, 110, 1.6, -t * 0.4, col="#D8B878", dark="#8C6E3E", direction=-1)
    kinetic(c, "SỰ THẬT", W / 2, 300, t, a + 0.2, size=90, color="#F4C430", per=0.05)
    p1 = pop(t, a + 0.7, 0.5)
    l1 = ["Abri du Maras (Pháp): một mẩu dây", "bện ba sợi từ vỏ trong của cây,", "41.000–52.000 năm tuổi,", "do người Neanderthal làm."]
    for i, l in enumerate(l1):
        text(c, l, W / 2, 460 + i * 70, "bold", 50, "white", a=255 * p1, align="center")
    p2 = pop(t, a + 2.4, 0.5)
    l2 = ["Hohle Fels (Đức): dụng cụ bằng ngà", "voi ma mút có bốn lỗ khắc rãnh xoắn,", "~40.000 năm tuổi, dùng để bện dây."]
    for i, l in enumerate(l2):
        text(c, l, W / 2, 800 + i * 70, "bold", 50, "white" if i < 2 else "#F4C430", a=255 * p2, align="center")
    text(c, "Tập sau: cung tên", W / 2, 1150, "semi", 42, "#B9B4AA", a=255 * pop(t, a + 4.2), align="center")
    if t > b - 0.8:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 255 * prog(t, b - 0.8, b, lambda q: q)))


def _n(fn, n):
    return lambda c, t: fn(c, t, n)


FN = {
    "open": sc_open, "drop": sc_drop, "sigh": sc_sigh, "pass": sc_pass, "weak": sc_weak, "double": sc_double, "slippery": sc_slippery,
    "bark": _n(sc_bark, "bark"), "bark1": _n(sc_bark, "bark1"), "bark2": _n(sc_bark, "bark2"), "one": sc_one, "weak1": sc_weak1,
    "twist1": _n(sc_twist, "twist1"), "twist2": _n(sc_twist, "twist2"), "twist3": _n(sc_twist, "twist3"), "grip": sc_grip,
    "pull": sc_pull, "share1": _n(sc_share, "share1"), "share2": _n(sc_share, "share2"), "tie": sc_tie,
    "worm": sc_worm, "rope": sc_rope, "stomp": sc_stomp, "tug": sc_tug, "wrap": _n(sc_wrap, "wrap"), "cocoon": _n(sc_cocoon, "cocoon"),
    "kidnap": _n(sc_cocoon, "kidnap"), "free": _n(sc_wrap, "free"), "throw": sc_throw, "useless": sc_useless, "fall": sc_fall,
    "lost": sc_lost,
    "rabbit": sc_rabbit, "dinner": sc_dinner, "leap": sc_leap, "air": sc_air, "aaa": sc_aaa, "ledge": sc_ledge, "help": sc_help,
    "look": sc_look, "spot": _n(sc_spot, "spot"), "worm2": _n(sc_spot, "worm2"), "toss": sc_toss, "miss": sc_miss,
    "anchor": sc_anchor, "fric": sc_fric, "climb1": sc_climb1, "climb": _n(sc_climb, "climb"), "itchy": _n(sc_climb, "itchy"),
    "dont": sc_dont, "grit": sc_grit,
    "coil": sc_coil, "lifeline": sc_lifeline, "mine": sc_mine, "allmine": sc_allmine, "tieall": sc_tieall, "tiebop": sc_tiebop,
    "hey": _n(sc_hey, "hey"), "keep": _n(sc_hey, "keep"), "trophy": sc_trophy,
    "bend": _n(sc_bend, "bend"), "twang": _n(sc_bend, "twang"), "idea": sc_idea, "useless2": sc_useless2, "black": sc_black,
    "card": sc_card,
}
SCENE_CUT = {T["bark"][0], T["rabbit"][0], T["coil"][0], T["bend"][0]}


def draw_frame(c, t):
    for name, (a, b, row) in T.items():
        if a <= t < b:
            FN[name](c, t)
            for sc in SCENE_CUT:
                if sc - 0.3 <= t < sc + 0.3:
                    c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 255 * (1 - abs(t - sc) / 0.3)))
            return
    sc_card(c, min(t, DUR - 0.01))
