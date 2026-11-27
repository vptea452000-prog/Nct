"""Tập 2: Cây giáo — Bộp và Gầm (phim hài không lời)."""
import math
import skia
from lib import *  # noqa
from toon import OUT, fill_out, rrect_path, oval_path, limb  # noqa
from toon2 import kinetic
from prehist import caveperson, SAP, NEA
from sets import grad_rect, vignette
from kit import (pop, phase, shake, cam, comic_bubble, sfx_word, cave_exterior, cave_interior, fire, smoke, wood_stick,
                 flat_stone, bop, gam)
from beats import T, DUR


def beat(n):
    return T[n][0], T[n][1]


def talking(n, t, lead=0.12, tail=0.45):
    a, b = beat(n)
    return a + lead < t < b - tail


def say(c, n, x, y, tail, t, d=0.1):
    a, b = beat(n)
    row = T[n][2]
    comic_bubble(c, x, y, row[5], row[4], tail, pop(t, a + d))


# ---------------------------------------------------------------- bối cảnh & đạo cụ
def stream_bg(c, t, tone="morning"):
    sky = {"morning": ("#9FD3F0", "#F2F6E2"), "noon": ("#7FC4E8", "#E9F4F8"), "sunset": ("#F08A4B", "#F6C67A"), "after": ("#E9B97A", "#F6E2B0")}[tone]
    grad_rect(c, skia.Rect.MakeWH(W, H), *sky)
    if tone == "sunset":
        c.drawCircle(780, 900, 140, paint("#FFD08A", 230))
    for k, (yy, colr) in enumerate([(880, "#7FA36A"), (960, "#5E8A4E")]):
        p = skia.Path(); p.moveTo(-200, 1500)
        for i in range(0, 16):
            p.lineTo(-200 + i * 110, yy - 120 * abs(math.sin(i * 0.8 + k)))
        p.lineTo(W + 200, 1500); p.close()
        c.drawPath(p, paint(colr))
    c.drawRect(skia.Rect.MakeXYWH(-200, 1040, W + 400, 260), paint("#86B86A"))
    # suối
    water = "#E9A060" if tone == "sunset" else "#4FA3CF"
    c.drawRect(skia.Rect.MakeXYWH(-200, 1300, W + 400, 260), paint(water))
    for k in range(10):
        x = (k * 150 + t * 80) % (W + 300) - 150
        y = 1340 + (k % 4) * 55
        c.drawLine(x, y, x + 70, y, paint("white", 140, stroke=5))
    c.drawRect(skia.Rect.MakeXYWH(-200, 1290, W + 400, 14), paint(OUT, 100))
    c.drawRect(skia.Rect.MakeXYWH(-200, 1560, W + 400, 600), paint("#6E8A4A"))
    for x in (90, 980):
        fill_out(c, oval_path(x, 1300, 70, 34), "#9AA3A8", ow=5)


def bush(c, x, y, s=1.0):
    with Xf(c, x, y, 0, s):
        for dx, dy, r in [(-90, -40, 90), (0, -90, 110), (90, -40, 90), (40, 0, 80), (-50, 0, 80)]:
            c.drawCircle(dx, dy, r, paint("#3E6A3A"))
        for dx, dy, r in [(-90, -40, 90), (0, -90, 110), (90, -40, 90)]:
            c.drawCircle(dx, dy, r, paint(OUT, 120, stroke=5))


def tree(c, x, y, s=1.0):
    with Xf(c, x, y, 0, s):
        fill_out(c, rrect_path(-50, -720, 100, 720, 20), "#7A5636")
        br = skia.Path(); br.moveTo(30, -560); br.lineTo(300, -640); br.lineTo(300, -610); br.lineTo(40, -520); br.close()
        fill_out(c, br, "#7A5636")
        for dx, dy, r in [(-160, -820, 170), (60, -900, 200), (240, -780, 170), (0, -720, 150)]:
            c.drawCircle(dx, dy, r, paint("#4F7F45"))
            c.drawCircle(dx, dy, r, paint(OUT, 120, stroke=5))


def boar(c, x, y, s, t, flip=False, run=None, mood="calm", big=False, eyes_cross=0.0, paw=0.0, alpha=1.0):
    """Lợn rừng hoạt hình. mood: calm / angry / scared. big: con anh (to, có sẹo)."""
    with Xf(c, x, y, 0, s * (1.45 if big else 1.0), alpha):
        if flip:
            c.scale(-1, 1)
        ph = 0 if run is None else run
        body_col, dark = ("#6B4A34", "#4E3424") if not big else ("#5A3E2C", "#3E2A1E")
        for k, lx in enumerate([-110, -60, 60, 110]):
            a = (28 * math.sin(ph + k * 1.6) if run is not None else 0) + (paw * 30 * math.sin(t * 20) if k == 3 else 0)
            with Xf(c, lx, -10, a, 1):
                c.drawLine(0, 0, 0, 80, paint(OUT, stroke=30)); c.drawLine(0, 0, 0, 80, paint(dark, stroke=20))
                fill_out(c, rrect_path(-16, 70, 32, 20, 6), "#2E2018", ow=4)
        body = skia.Path(); body.addOval(skia.Rect.MakeXYWH(-190, -150, 340, 170))
        fill_out(c, body, body_col)
        for k in range(9):
            bx = -150 + k * 32
            c.drawLine(bx, -140 + abs(k - 4) * 4, bx + 10, -175 + abs(k - 4) * 6, paint(OUT, stroke=6))
        head = skia.Path(); head.moveTo(100, -130); head.lineTo(250, -80); head.lineTo(270, -30); head.lineTo(150, 10); head.lineTo(90, -20); head.close()
        fill_out(c, head, body_col)
        fill_out(c, oval_path(266, -52, 22, 28), "#C98A80", ow=5)
        c.drawCircle(262, -60, 5, paint(OUT)); c.drawCircle(262, -44, 5, paint(OUT))
        tusk = skia.Path(); tusk.moveTo(225, -30); tusk.quadTo(250, -60, 240, -95); tusk.quadTo(232, -60, 212, -32); tusk.close()
        fill_out(c, tusk, "#F6F1E4", ow=4)
        ear = skia.Path(); ear.moveTo(120, -125); ear.lineTo(150, -175); ear.lineTo(165, -120); ear.close()
        fill_out(c, ear, dark, ow=5)
        # mắt
        ex, ey = 190, -88
        if eyes_cross > 0:
            c.drawCircle(ex, ey, 18, paint("white")); c.drawCircle(ex, ey, 18, paint(OUT, stroke=4))
            c.drawCircle(ex + 10 * eyes_cross, ey + 6, 7, paint(OUT))
            c.drawCircle(ex - 26, ey + 4, 14, paint("white")); c.drawCircle(ex - 26, ey + 4, 14, paint(OUT, stroke=4))
            c.drawCircle(ex - 16 * eyes_cross, ey + 8, 6, paint(OUT))
        else:
            c.drawCircle(ex, ey, 9, paint(OUT))
        if mood == "angry":
            c.drawLine(ex - 26, ey - 26, ex + 20, ey - 10, paint(OUT, stroke=9))
        elif mood == "scared":
            c.drawLine(ex - 20, ey - 16, ex + 20, ey - 30, paint(OUT, stroke=7))
        if big:
            c.drawLine(150, -110, 200, -60, paint("#C98A80", stroke=6)); c.drawLine(160, -70, 190, -100, paint("#C98A80", stroke=5))
        tail = skia.Path(); tail.moveTo(-185, -90)
        tail.cubicTo(-230, -120, -200, -150, -225, -165)
        c.drawPath(tail, paint(OUT, stroke=6))


def stone_spear(c, x, y, ang, L=640, s=1.0, sparkle=0.0, t=0.0, broken=False):
    """Giáo có mũi đá, buộc gân, trét nhựa."""
    with Xf(c, x, y, ang, s):
        c.drawLine(0, 0, 0, -L, paint(OUT, stroke=22)); c.drawLine(0, 0, 0, -L, paint("#A57A4A", stroke=14))
        if broken:
            return
        tip = skia.Path(); tip.moveTo(-26, -L + 20); tip.lineTo(0, -L - 110); tip.lineTo(26, -L + 20); tip.close()
        fill_out(c, tip, "#9AA3A8", ow=5)
        c.drawLine(-8, -L - 40, 10, -L - 80, paint("#C9D0D4", stroke=4))
        fill_out(c, rrect_path(-16, -L + 6, 32, 40, 8), "#C98A2A", ow=4)
        for k in range(4):
            c.drawLine(-16, -L + 14 + k * 9, 16, -L + 20 + k * 9, paint("#E9E2CF", stroke=4))
        if sparkle > 0:
            for k in range(4):
                a = k * math.pi / 2 + t * 3
                c.drawLine(30 * math.cos(a), -L - 110 + 30 * math.sin(a), 60 * math.cos(a), -L - 110 + 60 * math.sin(a), paint("white", 255 * sparkle, stroke=6))


def stars(c, x, y, t, t0, n=4, r=90):
    a = t - t0
    if a < 0 or a > 2.2:
        return
    for k in range(n):
        ang = a * 5 + k * 2 * math.pi / n
        px, py = x + r * math.cos(ang), y + r * 0.35 * math.sin(ang)
        st = skia.Path()
        for j in range(10):
            rr = 20 if j % 2 == 0 else 8
            aa = -math.pi / 2 + j * math.pi / 5
            (st.moveTo if j == 0 else st.lineTo)(px + rr * math.cos(aa), py + rr * math.sin(aa))
        st.close(); fill_out(c, st, "#F4D03F", ow=4)


def speedlines(c, t, cx=540, cy=900, a=120):
    for k in range(26):
        ang = k * 2 * math.pi / 26 + (int(t * 12) % 2) * 0.05
        r0 = 520 + (k * 37 % 80)
        c.drawLine(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang), cx + 1500 * math.cos(ang), cy + 1500 * math.sin(ang), paint("white", a, stroke=6))


def fish(c, x, y, s, rot=0, flop=0.0, t=0.0):
    with Xf(c, x, y, rot + flop * 20 * math.sin(t * 20), s):
        b = skia.Path(); b.addOval(skia.Rect.MakeXYWH(-90, -36, 180, 72))
        fill_out(c, b, "#7FB3D5")
        tl = skia.Path(); tl.moveTo(-80, 0); tl.lineTo(-140, -40); tl.lineTo(-140, 40); tl.close()
        fill_out(c, tl, "#5E93B5")
        c.drawCircle(50, -8, 9, paint("white")); c.drawCircle(52, -8, 4, paint(OUT))


def hide(c, x, y, s, rot=0):
    with Xf(c, x, y, rot, s):
        p = skia.Path(); p.moveTo(-160, -60); p.quadTo(-120, -130, -40, -100); p.quadTo(40, -150, 120, -90); p.quadTo(190, -40, 150, 40)
        p.quadTo(120, 120, 20, 90); p.quadTo(-80, 130, -140, 70); p.quadTo(-200, 10, -160, -60); p.close()
        fill_out(c, p, "#B9A37A")
        for k in range(6):
            c.drawLine(-100 + k * 40, -40, -90 + k * 40, -10, paint("#8A7A52", stroke=5))


def bug(c, x, y, s, t):
    with Xf(c, x, y, 20 * math.sin(t * 12), s):
        fill_out(c, oval_path(0, 0, 18, 12), "#2E2A25", ow=3)
        for k in (-1, 1):
            c.drawOval(skia.Rect.MakeXYWH(-14 + k * 6, -22, 14, 16), paint("#FFFFFF", 160))


def thorn(c, x, y, s, rot=0):
    with Xf(c, x, y, rot, s):
        p = skia.Path(); p.moveTo(-14, 0); p.lineTo(0, -120); p.lineTo(14, 0); p.close()
        fill_out(c, p, "#7A5636", ow=4)


def trophy_corner(c, t, x=120, y=1300):
    """Chiến lợi phẩm của Gầm trong hang (gọi lại tập trước)."""
    fire(c, x, y, 0.45, t)


# ---------------------------------------------------------------- CẢNH 1
def sc_open(c, t):
    a, b = beat("open")
    z = lerp(0.95, 1.08, ease_in_out(clamp((t - a) / (b - a))))
    c.save(); cam(c, 540, 1050, z)
    stream_bg(c, t, "morning")
    boar(c, 700, 1230, 0.9, t, flip=True)
    for k in range(4):
        c.drawCircle(560 + 20 * math.sin(t * 9 + k), 1250 - k * 8, 10, paint("#6E5A3A", 200))
    bush(c, 220, 1250, 1.1)
    c.restore()
    kinetic(c, "TẬP 2", W / 2, 420, t, a + 0.3, size=70, per=0.04)
    kinetic(c, "CÂY GIÁO", W / 2, 560, t, a + 0.6, size=140, color="#F4C430", per=0.06)


def sc_lunch(c, t):
    a, b = beat("lunch")
    c.save(); cam(c, 330, 1000, 1.45)
    stream_bg(c, t, "morning")
    boar(c, 760, 1230, 0.9, t, flip=True)
    gam(c, 260, 1260, 0.95, t, mood="smile", look=0.9, talk=talking("lunch", t), arm="down")
    bush(c, 300, 1290, 1.25)
    c.restore()
    say(c, "lunch", 470, 360, (300, 560), t)


def sc_charge(c, t):
    a, b = beat("charge")
    p = clamp((t - a) / 0.6)
    c.save(); cam(c, 540, 1050, 1.15)
    stream_bg(c, t, "morning")
    boar(c, 760, 1230, 0.9, t, flip=True)
    gam(c, lerp(260, 560, ease_out(p)), 1260 - 160 * math.sin(math.pi * p), 0.95, t, mood="angry", look=0.8, arm="up", stick_ang=lerp(-30, 70, prog(t, a + 0.5, a + 0.8)))
    c.restore()
    speedlines(c, t, 540, 900, 90)
    c.save(); shake(c, t, a + 0.8, 20)
    sfx_word(c, "BỐP!", 760, 820, t, a + 0.8, size=150, dur=0.6)
    c.restore()


def sc_bounce(c, t):
    a, b = beat("bounce")
    c.save(); shake(c, t, a + 0.1, 16)
    c.save(); cam(c, 560, 900, 1.6)
    stream_bg(c, t, "morning")
    boar(c, 820, 1230, 0.9, t, flip=True)
    gam(c, 560, 1260, 0.95, t, mood="surprise", look=0.0, arm="up", stick_ang=lerp(70, -40, prog(t, a, a + 0.25)), talk=talking("bounce", t))
    stars(c, 560, 610, t, a + 0.25)
    c.restore(); c.restore()
    sfx_word(c, "CỐP!", 360, 600, t, a + 0.1, size=120, color="white", dur=0.6)
    say(c, "bounce", 720, 360, (580, 520), t, d=0.3)


def sc_turn(c, t):
    a, b = beat("turn")
    c.save(); cam(c, 800, 1050, 1.7)
    stream_bg(c, t, "morning")
    boar(c, 820, 1230, 0.95, t, flip=True if t < a + 0.3 else False, mood="angry", paw=pop(t, a + 0.8, 0.2))
    if t > a + 0.4:
        for k in range(4):
            c.drawCircle(1010 + k * 26, 1180 - k * 10, 10 + k * 3, paint("white", 160 * clamp(1 - (t - a - 0.4))))
    c.restore()
    sfx_word(c, "KHỊT!", 760, 560, t, a + 0.3, size=110, color="white", dur=0.7)
    sfx_word(c, "SỘT SỘT", 760, 1180, t, a + 0.9, size=80, color="#C9A06A", dur=0.8)


def sc_talk(c, t):
    a, b = beat("talk")
    c.save(); cam(c, 540, 1050, 1.2)
    stream_bg(c, t, "morning")
    boar(c, 800, 1230, 0.9, t, mood="angry", paw=1.0)
    gam(c, 380, 1260, 0.95, t, mood="smile", look=0.8, arm="up", stick_ang=-20, talk=talking("talk", t))
    c.restore()
    say(c, "talk", 470, 360, (380, 560), t)


def sc_chase(c, t):
    a, b = beat("chase")
    c.save(); cam(c, 640, 980, 1.0)
    stream_bg(c, t, "morning")
    tree(c, 700, 1260, 0.95)
    if t < a + 1.8:
        ang = (t - a) * 7
        gx, gy = 700 + 260 * math.cos(ang), 1260 + 40 * math.sin(ang)
        bx, by = 700 + 260 * math.cos(ang - 1.2), 1260 + 40 * math.sin(ang - 1.2)
        front = math.sin(ang) > 0
        boar(c, bx, by, 0.75, t, flip=math.sin(ang - 1.2) > 0, run=phase(t, a, 18), mood="angry")
        gam(c, gx, gy, 0.8, t, mood="surprise", walk=phase(t, a, 18), flip=math.sin(ang) > 0, stick=False)
    else:
        sh = 8 * math.sin(t * 50) if t < a + 2.9 else 0
        c.save(); c.translate(sh, 0)
        gam(c, 880, 1260 - 610 * 0.95, 0.65, t, mood="surprise", look=0.0, stick=False, arm="up")
        c.restore()
        bk = clamp((t - a - 1.9) / 0.4)
        boar(c, lerp(500, 600, bk) - 40 * math.sin((t - a) * 14) if t < a + 2.9 else lerp(600, 1300, clamp((t - a - 2.9) / 0.5)), 1230, 0.85, t,
             mood="angry", run=phase(t, a, 14) if t > a + 2.9 else None, flip=t > a + 2.9 and False)
    c.restore()
    if t > a + 1.9:
        for k, ts in enumerate([a + 2.0, a + 2.35, a + 2.7]):
            c.save(); shake(c, t, ts, 10, 0.2); sfx_word(c, "RẦM!", 300 + k * 150, 760 + k * 60, t, ts, size=100, dur=0.35); c.restore()


def sc_skin(c, t, n="skin"):
    a, b = beat(n)
    c.save(); cam(c, 640, 950, 1.0)
    stream_bg(c, t, "morning")
    tree(c, 700, 1260, 0.95)
    gam(c, 880, 1260 - 610 * 0.95, 0.65, t, mood="sad", look=-0.6, stick=False, arm="up")
    bop(c, 230, 1260, 0.95, t, mood="flat", look=0.6, talk=talking(n, t))
    c.restore()
    say(c, n, 380, 380, (240, 640), t)


def sc_climb(c, t):
    a, b = beat("climb")
    c.save(); cam(c, 860, 760, 1.4)
    stream_bg(c, t, "morning")
    tree(c, 700, 1260, 0.95)
    gam(c, 880, 1260 - 610 * 0.95, 0.65, t, mood="angry", look=-0.6, stick=False, arm="up", talk=talking("climb", t))
    c.restore()
    say(c, "climb", 520, 400, (760, 560), t)


# ---------------------------------------------------------------- CẢNH 2
def cave_noon(c, t, gam_kw=None, bop_kw=None, z=1.0, cx=540, cy=1000, spear=None):
    c.save(); cam(c, cx, cy, z)
    cave_exterior(c, t, morning=1.0, wind=False)
    fire(c, 300, 1300, 0.5, t)
    gk = dict(mood="flat", look=0.0, stick=False, rot=-90)
    gk.update(gam_kw or {})
    gam(c, 780, 1235, 0.62, t, **gk)        # nằm ngang, đầu sát đống lửa
    fill_out(c, rrect_path(860, 1190, 200, 110, 36), "#9AA3A8")
    bk = dict(mood="flat", look=-0.3)
    bk.update(bop_kw or {})
    bop(c, 960, 1210, 0.62, t, **bk)
    if spear:
        spear(c)
    c.restore()


def zzz(c, x, y, t):
    for k in range(3):
        a = (t * 0.7 + k * 0.33) % 1
        text(c, "z", x + a * 60, y - a * 160, "xbold", 40 + k * 10, "white", a=255 * math.sin(a * math.pi), stroke=4, stroke_color="#1A120D")


def sc_hug(c, t):
    a, b = beat("hug")
    cave_noon(c, t, gam_kw=dict(mood="smile", talk=talking("hug", t)), z=1.5, cx=520, cy=1150)
    zzz(c, 420, 980, t)
    say(c, "hug", 560, 460, (420, 1000), t)


def knap_insert(c, t, a):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#B98A6A", "#7A5A44")
    hit = a + 0.6
    p = clamp((t - a) / 0.6)
    lx = lerp(200, 430, ease_in_out(p)) if t < hit else 430
    for side, (x, rot) in ((-1, (lx, -20)), (1, (680, 10))):
        with Xf(c, x, 900, rot, 1):
            limb(c, [(side * 420, 400), (side * 120, 200), (0, 60)], 70, SAP)
            fill_out(c, oval_path(0, 0, 120, 90), "#9AA3A8")
    if t > hit:
        q = clamp((t - hit) / 0.6)
        with Xf(c, lerp(560, 760, q), lerp(880, 560, q), q * 300, 1):
            fl = skia.Path(); fl.moveTo(-50, 0); fl.lineTo(0, -26); fl.lineTo(60, 4); fl.lineTo(0, 22); fl.close()
            fill_out(c, fl, "#C9D0D4", ow=4)
        for k in range(8):
            ang = k * math.pi / 4
            r = 60 + q * 120
            c.drawLine(560 + r * math.cos(ang), 900 + r * math.sin(ang), 560 + (r + 30) * math.cos(ang), 900 + (r + 30) * math.sin(ang), paint("#F4D03F", 255 * (1 - q), stroke=6))


def sc_knap(c, t):
    a, b = beat("knap")
    c.save(); shake(c, t, a + 0.6, 12)
    knap_insert(c, t, a)
    c.restore()
    sfx_word(c, "CẠCH!", 540, 520, t, a + 0.6, size=140, dur=0.7)


def sc_ouch(c, t):
    a, b = beat("ouch")
    cave_noon(c, t, bop_kw=dict(mood="surprise", look=0.0, talk=talking("ouch", t), arm="up"), z=1.7, cx=900, cy=980)
    say(c, "ouch", 480, 400, (560, 560), t)


def sc_haft(c, t):
    a, b = beat("haft")
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#C9A86A")
    steps = ["GỌT NHỌN", "XẺ KHE", "NHÉT ĐÁ", "TRÉT NHỰA", "QUẤN GÂN"]
    k = min(4, int((t - a) / ((b - a) / 5)))
    lp_ = ((t - a) % ((b - a) / 5)) / ((b - a) / 5)
    with Xf(c, 540, 1180, -25, 1.25):
        c.drawLine(0, 0, 0, -620, paint(OUT, stroke=26)); c.drawLine(0, 0, 0, -620, paint("#A57A4A", stroke=18))
        if k >= 0:
            c.drawLine(-10, -600, 0, -660, paint(OUT, stroke=10))
        if k >= 1:
            c.drawLine(0, -660, 0, -600, paint("#3A2618", stroke=6))
        if k >= 2:
            tip = skia.Path(); tip.moveTo(-26, -640); tip.lineTo(0, -760); tip.lineTo(26, -640); tip.close()
            fill_out(c, tip, "#9AA3A8", ow=5)
        if k >= 3:
            fill_out(c, rrect_path(-18, -650, 36, 50, 10), "#C98A2A", ow=4)
        if k >= 4:
            for j in range(int(5 * (lp_ if k == 4 else 1)) + 1):
                c.drawLine(-18, -640 + j * 9, 18, -634 + j * 9, paint("#E9E2CF", stroke=5))
    label_tag(c, steps[k], W / 2, 360, 1, size=50, anchor="center", bg="yellow")
    text(c, f"{k + 1}/5", W / 2, 470, "xbold", 50, "ink", align="center")


def sc_glue(c, t):
    a, b = beat("glue")
    cave_noon(c, t, bop_kw=dict(mood="smile", look=-0.6, talk=talking("glue", t), arm="hold"), z=1.5, cx=860, cy=950,
              spear=lambda cc: stone_spear(cc, 980, 1080, 20, 420, 0.7))
    say(c, "glue", 460, 400, (620, 600), t)


def sc_done(c, t):
    a, b = beat("done")
    grad_rect(c, skia.Rect.MakeWH(W, H), "#F6E7C0", "#E9C98A")
    for k in range(14):
        ang = k * math.pi / 7 + t * 0.4
        p = skia.Path(); p.moveTo(540, 800)
        p.lineTo(540 + 1800 * math.cos(ang), 800 + 1800 * math.sin(ang)); p.lineTo(540 + 1800 * math.cos(ang + 0.18), 800 + 1800 * math.sin(ang + 0.18)); p.close()
        c.drawPath(p, paint("#FFFFFF", 70))
    c.save(); cam(c, 540, 950, 1.3)
    bop(c, 540, 1300, 0.95, t, mood="smile", look=0.0, arm="up", talk=talking("done", t))
    stone_spear(c, 540 + 158 * 0.95 * 0.95, 1300 - 710 * 0.95 * 1.05 + 160, 0, 640, 0.95, sparkle=1.0, t=t)
    c.restore()
    say(c, "done", 540, 340, (540, 540), t)
    sfx_word(c, "TING!", 820, 520, t, a + 0.3, size=90, color="white", dur=0.8)


# ---------------------------------------------------------------- CẢNH 3
def sc_peek(c, t):
    a, b = beat("peek")
    cave_noon(c, t, gam_kw=dict(mood="flat", look=0.0), z=2.6, cx=420, cy=1240)
    c.save(); cam(c, 420, 1240, 2.6)
    # một mắt mở (mắt phía trên khi nằm)
    ex, ey = 780 - (650 * 0.92 - 20) * 0.62, 1235 - 30 * 0.62
    if t > a + 0.5:
        c.drawCircle(ex, ey, 14, paint("white")); c.drawCircle(ex, ey, 14, paint(OUT, stroke=4)); c.drawCircle(ex + 3, ey - 3, 6, paint(OUT))
    c.restore()
    sfx_word(c, "HÉ…", 760, 520, t, a + 0.4, size=90, color="white", dur=0.8)


def two(c, t, n, gam_kw=None, bop_kw=None, z=1.0, cx=540, cy=1030, spear_kind="whole", bx=None, tail=None):
    a, b = beat(n)
    spk = T[n][2][3]
    c.save(); cam(c, cx, cy, z)
    cave_exterior(c, t, morning=1.0, wind=False)
    trophy_corner(c, t, 110, 1300)
    gk = dict(mood="flat", look=0.6, stick=False)
    gk.update(gam_kw or {})
    if spk == "gam":
        gk["talk"] = talking(n, t)
    gam(c, 320, 1300, 0.95, t, **gk)
    bk = dict(mood="flat", look=-0.6, flip=True, arm="hold")
    bk.update(bop_kw or {})
    if spk == "bop":
        bk["talk"] = talking(n, t)
    bop(c, 780, 1300, 0.95, t, **bk)
    if spear_kind == "whole":
        stone_spear(c, 840, 1220, -12, 600, 0.9)
    c.restore()
    if T[n][2][5]:
        tx = (780 - cx) * z + W / 2 if spk == "bop" else (320 - cx) * z + W / 2
        say(c, n, bx or (600 if spk == "bop" else 480), 380, tail or (tx, 600), t)


def sc_tooth(c, t):
    two(c, t, "tooth", gam_kw=dict(mood="smile", look=0.9))


def explain_panel(c, t, a, mode):
    """mode 'club': lực tỏa ra; 'point': dồn vào một điểm."""
    grad_rect(c, skia.Rect.MakeWH(W, H), "#24476B", "#13263B")
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, 800), paint("#7A6A5A"))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, 14), paint(OUT))
    p = clamp((t - a) / 0.5)
    if mode == "club":
        with Xf(c, 540, lerp(700, 1000, ease_out(p)), 0, 1):
            fill_out(c, oval_path(0, 0, 160, 150), "#A57A4A")
        if p >= 1:
            for k in range(9):
                ang = math.pi + k * math.pi / 8
                q = clamp((t - a - 0.5) / 0.6)
                r0, r1 = 170, 170 + 160 * q
                c.drawLine(540 + r0 * math.cos(ang) * -1, 1150 - 10, 540 + r1 * math.cos(ang) * -1, 1150 - 10 + r1 * 0.3 * math.sin(ang), paint("#F4D03F", 200, stroke=8))
                arrow_head(c, (540 + r1 * math.cos(ang) * -1, 1150 - 10 + r1 * 0.3 * math.sin(ang)), (-math.cos(ang), 0.3 * math.sin(ang)), size=20, color="#F4D03F")
    else:
        with Xf(c, 540, lerp(500, 1060, ease_out(p)), 0, 1):
            tip = skia.Path(); tip.moveTo(-60, -200); tip.lineTo(0, 90); tip.lineTo(60, -200); tip.close()
            fill_out(c, tip, "#9AA3A8")
        if p >= 1:
            q = clamp((t - a - 0.5) / 0.6)
            for k in range(5):
                x = 540 + (k - 2) * 60 * (1 - q)
                c.drawLine(x, 800, lerp(x, 540, q), 1120, paint("#F4D03F", 220, stroke=8))
            c.drawCircle(540, 1150, 30 + 30 * q, paint("#F4D03F", 200 * q))


def sc_ex(c, t, n, mode):
    a, b = beat(n)
    explain_panel(c, t, a, mode)
    say(c, n, 540, 380, (540, 700), t)
    note_label(c, "MINH HỌA", 60, 1220, 1)


def sc_huh(c, t):
    a, b = beat("huh")
    c.save(); cam(c, 320, 980, 1.6)
    cave_exterior(c, t, morning=1.0, wind=False)
    gam(c, 320, 1300, 0.95, t, mood="surprise", look=0.0, stick=False, arm="up")
    for k in range(3):
        ang = t * 4 + k * 2.1
        text(c, "?", 320 + 120 * math.cos(ang), 560 + 30 * math.sin(ang), "xbold", 70, "#F4C430", stroke=5, stroke_color="#1A120D")
    c.restore()
    say(c, "huh", 600, 380, (380, 600), t, d=0.2)


def arm_closeup(c, t, a, tool):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#C9A86A")
    fill_out(c, rrect_path(-100, 1000, W + 200, 260, 120), SAP)
    p = clamp((t - a - 0.2) / 0.5)
    y = lerp(600, 1000, ease_in_out(p))
    if tool == "finger":
        fill_out(c, rrect_path(470, y - 520, 140, 540, 70), NEA)
        c.drawLine(480, y - 60, 600, y - 60, paint(NEA, stroke=1))
        if p > 0.95:
            for k in range(7):
                x = 420 + k * 40
                c.drawLine(x, 980, x + (x - 540) * 0.4, 1060, paint("#3E7FB8", 200, stroke=6))
            label_tag(c, "lực tỏa rộng", W / 2, 1380, 1, size=40, anchor="center")
    else:
        fill_out(c, rrect_path(470, y - 620, 140, 460, 70), NEA)
        thorn(c, 540, y + 10, 1.2)
        if p > 0.95:
            c.drawCircle(540, 1005, 22, paint("#C0392B"))
            for k in range(5):
                x = 540 + (k - 2) * 10
                c.drawLine(x, 900, 540, 990, paint("#C0392B", 220, stroke=6))
            label_tag(c, "lực dồn vào một điểm", W / 2, 1380, 1, size=40, anchor="center", bg="yellow")
    # khuôn mặt Bộp ở góc
    with Xf(c, 860, 520, 0, 1):
        fill_out(c, oval_path(0, 0, 150, 150), "#F6F1E4")
        c.save(); c.clipPath(oval_path(0, 0, 146, 146), skia.ClipOp.kIntersect, True)
        caveperson(c, 0, 780, 1.0, t=t, kind="sap", spear=False, mood="flat" if tool == "finger" else ("surprise" if p > 0.95 else "flat"),
                   look=-0.4)
        c.restore()


def sc_press1(c, t):
    a, b = beat("press1")
    arm_closeup(c, t, a, "finger")
    text(c, "…", 860, 760, "xbold", 80, "ink", a=255 * pop(t, a + 0.9), align="center")


def sc_press2(c, t):
    a, b = beat("press2")
    c.save(); shake(c, t, a + 0.7, 18)
    arm_closeup(c, t, a, "thorn")
    c.restore()
    sfx_word(c, "ÚI!!!", 760, 820, t, a + 0.7, size=140, color="#C0392B", dur=1.0)


def sc_finger(c, t):
    two(c, t, "finger", bop_kw=dict(arm="wave"), gam_kw=dict(mood="flat"))


def sc_thorn(c, t):
    a, b = beat("thorn")
    two(c, t, "thorn", bop_kw=dict(arm="hold"), gam_kw=dict(mood="flat"))
    c.save(); cam(c, 540, 1030, 1.0)
    thorn(c, 660, 900, 0.9, rot=-30)
    c.restore()


def sc_same(c, t):
    a, b = beat("same")
    grad_rect(c, skia.Rect.MakeWH(W, H), "#24476B", "#13263B")
    for k, (x, wdt, lab) in enumerate([(300, 180, "ngón tay"), (780, 26, "cái gai")]):
        c.drawLine(x, 560, x, 820, paint("#F4D03F", stroke=14))
        arrow_head(c, (x, 840), (0, 1), size=40, color="#F4D03F")
        text(c, "cùng 1 sức", x, 520, "bold", 38, "white", align="center")
        c.drawRect(skia.Rect.MakeXYWH(x - wdt / 2, 860, wdt, 20), paint("#9AA3A8"))
        h = (60 if k == 0 else 420) * pop(t, a + 0.6 + k * 0.4, 0.5)
        c.drawRect(skia.Rect.MakeXYWH(x - 60, 1260 - h, 120, h), paint("#C0392B" if k else "#3E7FB8"))
        c.drawRect(skia.Rect.MakeXYWH(x - 60, 840, 120, 420), paint(OUT, 160, stroke=4, cap=False))
        label_tag(c, lab, x, 1320, 1, size=36, anchor="center")
    text(c, "áp lực", W / 2, 1060, "xbold", 44, "white", a=200, align="center")
    say(c, "same", 540, 340, (780, 540), t)


def sc_strong(c, t):
    two(c, t, "strong", gam_kw=dict(mood="smile", arm="up"), z=1.15, cx=460)


def sc_useless(c, t):
    a, b = beat("useless")
    c.save(); shake(c, t, a + 0.1, 14)
    two(c, t, "useless", gam_kw=dict(mood="angry", arm="up"), z=1.5, cx=360, cy=950)
    c.restore()


def sc_snap(c, t):
    a, b = beat("snap")
    c.save(); cam(c, 540, 1000, 1.1)
    stream_bg(c, t, "noon")
    p = clamp((t - a - 0.3) / 0.3)
    gam(c, 420, 1260, 0.95, t, mood="angry", look=0.6, stick=False, arm="up")
    if p < 1:
        stone_spear(c, 420, 760, 90, 600, 0.9)
    else:
        q = clamp((t - a - 0.8) / 0.7)
        stone_spear(c, 360, 700, 60, 300, 0.9, broken=True)
        with Xf(c, lerp(560, 840, q), lerp(680, 1330, q) - 300 * math.sin(math.pi * q), q * 500, 0.7):
            tip = skia.Path(); tip.moveTo(-26, 20); tip.lineTo(0, -110); tip.lineTo(26, 20); tip.close()
            fill_out(c, tip, "#9AA3A8", ow=5)
        if t > a + 1.5:
            for k in range(3):
                r = (t - a - 1.5) * 200 + k * 30
                c.drawOval(skia.Rect.MakeXYWH(840 - r, 1340 - r * 0.25, 2 * r, r * 0.5), paint("white", 200 * clamp(1 - (t - a - 1.5)), stroke=4))
    bop(c, 880, 1260, 0.95, t, mood="surprise", look=-0.6, flip=True)
    c.restore()
    c.save(); shake(c, t, a + 0.6, 16); sfx_word(c, "RẮC!", 420, 560, t, a + 0.6, size=150, dur=0.7); c.restore()
    sfx_word(c, "TÕM.", 820, 1100, t, a + 1.5, size=90, color="white", dur=0.7)


def sc_lost(c, t):
    a, b = beat("lost")
    c.save(); cam(c, 760, 1000, 1.6)
    stream_bg(c, t, "noon")
    stone_spear(c, 620, 1290, 80, 300, 0.9, broken=True)
    bop(c, 860, 1260, 0.95, t, mood="sad", look=-0.6, flip=True, talk=talking("lost", t))
    c.restore()
    vignette(c, 150)
    say(c, "lost", 500, 400, (760, 600), t, d=0.5)


# ---------------------------------------------------------------- CẢNH 4
def sc_snort(c, t):
    a, b = beat("snort")
    pan = ease_in_out(clamp((t - a - 1.0) / 1.0))
    c.save(); cam(c, lerp(540, 760, pan), 1000, lerp(1.25, 0.95, pan))
    stream_bg(c, t, "after")
    boar(c, 640, 1230, 0.9, t, flip=True, mood="angry")
    boar(c, 1120, 1240, 0.9, t, flip=True, big=True, mood="angry", alpha=1.0)
    c.restore()
    sfx_word(c, "KHỊT KHỊT", 400, 560, t, a + 0.2, size=90, color="white", dur=1.0)
    if t > a + 1.9:
        sfx_word(c, "ỤT ỊT!!", 760, 520, t, a + 1.9, size=120, dur=0.7)


def sc_brother(c, t):
    a, b = beat("brother")
    c.save(); cam(c, 330, 950, 1.7)
    stream_bg(c, t, "after")
    gam(c, 330, 1260, 0.95, t, mood="surprise", look=0.8, arm="up", stick_ang=-15, talk=talking("brother", t))
    c.restore()
    say(c, "brother", 560, 380, (360, 560), t)
    if t > b - 0.5:
        text(c, "…", 540, 1000, "xbold", 160, "white", align="center", stroke=8, stroke_color="#1A120D")


def sc_bonk2(c, t):
    a, b = beat("bonk2")
    c.save(); shake(c, t, a + 0.5, 18)
    c.save(); cam(c, 560, 1000, 1.25)
    stream_bg(c, t, "after")
    boar(c, 760, 1230, 0.9, t, flip=True, mood="angry")
    boar(c, 1000, 1240, 0.9, t, flip=True, big=True, mood="angry")
    gam(c, 500, 1260, 0.95, t, mood="surprise", look=0.8, arm="up", stick_ang=lerp(-30, 70, prog(t, a + 0.2, a + 0.5)) if t < a + 0.6 else lerp(70, -40, prog(t, a + 0.6, a + 0.8)))
    stars(c, 500, 610, t, a + 0.8)
    c.restore(); c.restore()
    sfx_word(c, "BỐP!", 760, 700, t, a + 0.5, size=130, dur=0.5)
    sfx_word(c, "CỐP!", 300, 560, t, a + 0.8, size=110, color="white", dur=0.6)


def sc_help(c, t):
    a, b = beat("help")
    c.save(); cam(c, 300, 1000, 1.25)
    cave_exterior(c, t, morning=0.0, wind=False)
    jit = 6 * math.sin(t * 40)
    gam(c, 230 + jit, 1300, 0.95, t, mood="surprise", look=0.8, arm="up", stick=False, talk=talking("help", t))
    boar(c, 640, 1270, 0.85, t, flip=True, mood="angry", paw=1.0)
    boar(c, 900, 1280, 0.85, t, flip=True, big=True, mood="angry")
    c.restore()
    say(c, "help", 560, 360, (300, 560), t)


def sc_rebuild(c, t):
    a, b = beat("rebuild")
    grad_rect(c, skia.Rect.MakeWH(W, H), "#4FA3CF", "#2E6E9A")
    speedlines(c, t, 540, 900, 120)
    k = min(3, int((t - a) / 0.6))
    labels = ["MÒ ĐÁ!", "NHÉT!", "TRÉT!", "QUẤN!"]
    if t < a + 0.6:
        c.save(); cam(c, 540, 1300, 1.4); stream_bg(c, t, "after")
        with Xf(c, 540 + 30 * math.sin(t * 30), 1360, 180, 0.8):
            bop(c, 0, 0, 1.0, t, mood="surprise", arm="up")
        c.restore()
        for j in range(8):
            c.drawCircle(540 + 200 * math.cos(j + t * 8), 900 + 120 * math.sin(j * 1.7), 18, paint("white", 200))
    else:
        with Xf(c, 540, 1180, -25 + 10 * math.sin(t * 25), 1.15):
            c.drawLine(0, 0, 0, -520, paint(OUT, stroke=26)); c.drawLine(0, 0, 0, -520, paint("#A57A4A", stroke=18))
            if k >= 1:
                tip = skia.Path(); tip.moveTo(-26, -540); tip.lineTo(0, -660); tip.lineTo(26, -540); tip.close()
                fill_out(c, tip, "#9AA3A8", ow=5)
            if k >= 2:
                fill_out(c, rrect_path(-18, -550, 36, 50, 10), "#C98A2A", ow=4)
            if k >= 3:
                for j in range(5):
                    c.drawLine(-18, -540 + j * 9, 18, -534 + j * 9, paint("#E9E2CF", stroke=5))
    label_tag(c, labels[k], W / 2, 360, 1, size=60, anchor="center", bg="yellow")


def sc_catch(c, t):
    a, b = beat("catch")
    c.save(); cam(c, 540, 1000, 1.0)
    cave_exterior(c, t, wind=False)
    p = clamp((t - a - 0.4) / 0.8)
    bop(c, 880, 1300, 0.95, t, mood="angry", look=-0.8, flip=True, arm="up", talk=talking("catch", t))
    stone_spear(c, lerp(820, 300, p), lerp(700, 760, p) - 200 * math.sin(math.pi * p), -90 + p * 720 if p < 1 else -90, 520, 0.8)
    gam(c, 230, 1300, 0.95, t, mood="surprise", look=0.8, arm="up", stick=False)
    c.restore()
    say(c, "catch", 620, 380, (860, 560), t)
    sfx_word(c, "VÚT!", 540, 820, t, a + 0.5, size=100, color="white", dur=0.6)


def gam_aim(c, t, x, y, s, eyes_shut=True, shake_amp=6):
    jit = shake_amp * math.sin(t * 40)
    gam(c, x + jit, y, s, t, mood="flat" if eyes_shut else "surprise", look=0.0, arm="down", stick=False)
    if eyes_shut:
        hy = y - 650 * 0.92 * s + 20 * s
        for side in (-1, 1):
            c.drawLine(x + jit + side * 30 * s - 12 * s, hy, x + jit + side * 30 * s + 12 * s, hy, paint(OUT, stroke=8 * s))
    stone_spear(c, x + jit + 140 * s, y - 330 * s, 90, 560, s)


def sc_aim(c, t):
    a, b = beat("aim")
    c.save(); cam(c, 300, 1000, 1.5)
    cave_exterior(c, t, wind=False)
    gam_aim(c, t, 230, 1300, 0.95)
    c.restore()
    sfx_word(c, "RUN RUN", 300, 1100, t, a + 0.4, size=80, color="white", dur=1.0)


def sc_brake(c, t):
    a, b = beat("brake")
    p = clamp((t - a) / 0.8)
    bx = lerp(1300, 640, ease_out(p))
    c.save(); cam(c, 520, 1050, 1.15)
    cave_exterior(c, t, wind=False)
    gam_aim(c, t, 150, 1300, 0.95)
    boar(c, bx, 1270, 0.9, t, flip=True, big=True, mood="scared" if p >= 1 else "angry", run=phase(t, a, 16) if p < 1 else None,
         eyes_cross=pop(t, a + 1.0, 0.3))
    if p < 1:
        for k in range(5):
            c.drawCircle(bx + 200 + k * 30, 1290 - k * 6, 14 + k * 4, paint("#C9B48A", 200))
    c.restore()
    sfx_word(c, "KÉÉÉT!", 760, 700, t, a + 0.5, size=120, dur=0.8)
    if t > a + 1.3:
        text(c, "…", 640, 560, "xbold", 160, "white", align="center", stroke=8, stroke_color="#1A120D")


def sc_flee(c, t):
    a, b = beat("flee")
    p = clamp((t - a - 0.3) / 1.2)
    c.save(); cam(c, 540, 1050, 1.0)
    cave_exterior(c, t, wind=False)
    gam_aim(c, t, 150, 1300, 0.95, shake_amp=3)
    boar(c, lerp(640, 1500, p), 1270, 0.9, t, flip=False, big=True, mood="scared", run=phase(t, a, 18) if p > 0 else None)
    boar(c, lerp(920, 1700, p), 1280, 0.85, t, flip=False, mood="scared", run=phase(t, a, 18) if p > 0 else None)
    c.restore()
    sfx_word(c, "ỤT ỊT ỤT ỊT", 760, 760, t, a + 0.3, size=80, color="white", dur=1.2)


def sc_win(c, t):
    a, b = beat("win")
    c.save(); cam(c, 300, 950, 1.7)
    cave_exterior(c, t, wind=False)
    gam_aim(c, t, 230, 1300, 0.95, eyes_shut=t < a + 0.4, shake_amp=0)
    c.restore()
    say(c, "win", 560, 380, (340, 560), t, d=0.4)


def sc_reach(c, t, n):
    a, b = beat(n)
    grad_rect(c, skia.Rect.MakeWH(W, H), "#E9D9A6", "#D4BE86")
    c.drawRect(skia.Rect.MakeXYWH(0, 1300, W, 600), paint("#B9A37A"))
    gam(c, 180, 1300, 0.6, t, mood="smile", look=0.6, stick=False)
    stone_spear(c, 270, 1100, 90, 560, 0.75)
    boar(c, 860, 1290, 0.55, t, flip=True, mood="scared")
    c.drawLine(180, 1420, 760, 1420, paint("#C0392B", stroke=6))
    arrow_head(c, (760, 1420), (1, 0), size=26, color="#C0392B"); arrow_head(c, (180, 1420), (-1, 0), size=26, color="#C0392B")
    label_tag(c, "khoảng cách an toàn", 470, 1500, pop(t, T["reach1"][0] + 0.4), size=34, anchor="center", bg="yellow")
    note_label(c, "MINH HỌA", 60, 1180, 1)
    spk_x = 180
    say(c, n, 540, 400, (W / 2, 700), t)


# ---------------------------------------------------------------- CẢNH 5
def sc_fish(c, t):
    a, b = beat("fish")
    c.save(); cam(c, 540, 1100, 1.2)
    stream_bg(c, t, "sunset")
    stab = clamp((t - a - 1.2) / 0.25)
    lift = clamp((t - a - 1.6) / 0.5)
    gam(c, 540, 1400, 0.95, t, mood="angry" if t < a + 1.6 else "smile", look=0.4, arm="up", stick=False)
    sy = lerp(lerp(900, 1380, stab), 800, ease_out(lift))
    stone_spear(c, 690, sy + 300, 180 if lift <= 0 else 0, 600, 0.9)
    if t < a + 1.4:
        fish(c, lerp(200, 700, clamp((t - a) / 1.4)), 1440, 0.7)
    else:
        if lift > 0:
            fish(c, 690, sy - 320 + 300, 0.7, rot=90, flop=1.0, t=t)
    c.restore()
    if t > a + 1.4:
        c.save(); shake(c, t, a + 1.45, 14); sfx_word(c, "PHẬP!", 760, 820, t, a + 1.45, size=130, dur=0.7); c.restore()


def sc_fishstick(c, t):
    a, b = beat("fishstick")
    grad_rect(c, skia.Rect.MakeWH(W, H), "#F08A4B", "#F6C67A")
    for k in range(14):
        ang = k * math.pi / 7 + t * 0.4
        p = skia.Path(); p.moveTo(540, 900)
        p.lineTo(540 + 1800 * math.cos(ang), 900 + 1800 * math.sin(ang)); p.lineTo(540 + 1800 * math.cos(ang + 0.18), 900 + 1800 * math.sin(ang + 0.18)); p.close()
        c.drawPath(p, paint("#FFFFFF", 50))
    c.save(); cam(c, 540, 950, 1.35)
    gam(c, 540, 1300, 0.95, t, mood="smile", look=0.0, arm="up", stick=False, talk=talking("fishstick", t))
    stone_spear(c, 540 + 186 * 0.95, 1300 - 653 * 0.95 + 160, 0, 640, 0.95)
    fish(c, 540 + 186 * 0.95, 1300 - 653 * 0.95 + 160 - 640 * 0.95 - 20, 0.6, rot=90, flop=1.0, t=t)
    c.restore()
    say(c, "fishstick", 540, 330, (560, 540), t)


def sc_mine(c, t):
    a, b = beat("mine")
    c.save(); cam(c, 760, 1000, 1.4)
    stream_bg(c, t, "sunset")
    bop(c, 820, 1260, 0.95, t, mood="sad", look=-0.6, flip=True, talk=talking("mine", t))
    c.restore()
    say(c, "mine", 520, 400, (760, 600), t)


def sc_allmine(c, t):
    a, b = beat("allmine")
    c.save(); shake(c, t, a + 0.1, 10)
    c.save(); cam(c, 400, 950, 1.3)
    stream_bg(c, t, "sunset")
    gam(c, 380, 1300, 0.95, t, mood="angry", look=0.6, arm="up", stick=False, talk=talking("allmine", t))
    stone_spear(c, 380 + 186 * 0.95, 1300 - 653 * 0.95 + 160, 0, 640, 0.95)
    c.restore(); c.restore()
    say(c, "allmine", 580, 380, (420, 560), t)


def sc_sing(c, t):
    a, b = beat("sing")
    c.save(); cam(c, 460, 1000, 1.1)
    cave_interior(c, t, rain=False)
    fire(c, 520, 1300, 0.6, t)
    with Xf(c, 520, 1120, 0, 1):
        c.drawLine(-140, 0, 140, 0, paint(OUT, stroke=12)); c.drawLine(-140, 0, 140, 0, paint("#8A6A44", stroke=7))
    fish(c, 520, 1100, 0.55, t=t)
    stone_spear(c, 120, 1300, 10, 560, 0.75)
    gam(c, 300, 1300, 0.9, t, mood="smile", look=0.6, stick=False, talk=talking("sing", t), rot=4 * math.sin(t * 6))
    c.restore()
    for k in range(4):
        ph = (t * 0.8 + k * 0.25) % 1
        text(c, "♪" if k % 2 else "♫", 300 + ph * 260 + 30 * math.sin(ph * 8), 640 - ph * 260, "xbold", 70, "#F4C430",
             a=255 * math.sin(ph * math.pi), stroke=4, stroke_color="#1A120D", rot=0) if False else None
        c.save(); c.translate(300 + ph * 260, 640 - ph * 260); c.rotate(20 * math.sin(ph * 9))
        text(c, "♪" if k % 2 else "♫", 0, 0, "xbold", 70, "#F4C430", a=255 * math.sin(ph * math.pi), stroke=4, stroke_color="#1A120D")
        c.restore()
    say(c, "sing", 560, 380, (320, 560), t)
    label_tag(c, "chiến lợi phẩm: lửa · giáo", 60, 1460, pop(t, a + 0.6), size=30)


# ---------------------------------------------------------------- CẢNH 6
def sc_chilly(c, t):
    a, b = beat("chilly")
    c.save(); cam(c, 640, 1000, 1.3)
    cave_exterior(c, t, night=1.0, wind=True)
    jit = 5 * math.sin(t * 60)
    bop(c, 700 + jit, 1300, 0.95, t, mood="sad", look=-0.3)
    if t < a + 1.4:
        bug(c, lerp(1000, 700, clamp((t - a) / 1.2)), lerp(900, 1280, clamp((t - a) / 1.2)), 1.4, t)
    hide(c, 330, 1290, 0.8, rot=-6)
    c.restore()
    sfx_word(c, "VO VE…", 820, 640, t, a + 0.1, size=70, color="white", dur=1.2)
    c.save(); shake(c, t, a + 1.3, 10); sfx_word(c, "CHÍCH!", 640, 1100, t, a + 1.3, size=110, color="#C0392B", dur=0.7); c.restore()


def sc_idea(c, t):
    a, b = beat("idea")
    c.save(); cam(c, 560, 1000, 1.4)
    cave_exterior(c, t, night=1.0, wind=False)
    hide(c, 330, 1290, 0.8, rot=-6)
    bop(c, 700, 1300, 0.95, t, mood="surprise" if t < a + 1.0 else "smile", look=-0.6, arm="hold")
    thorn(c, 740, 900, 0.8, rot=10)
    c.restore()
    say(c, "idea", 520, 420, (700, 620), t, d=0.3)
    if t > a + 1.0:
        with Xf(c, 520, 470, 0, back_out(pop(t, a + 1.0)) * 0.7):
            hide(c, -60, 0, 0.5); thorn(c, 90, 30, 0.6, rot=30)


def sc_useless2(c, t):
    a, b = beat("useless2")
    c.save(); cam(c, 300, 1000, 1.1)
    cave_exterior(c, t, night=1.0, wind=False)
    glow = paint("#F39C12", 90); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 80))
    c.drawCircle(240, 1050, 160, glow)
    bop(c, 760, 1300, 0.95, t, mood="sad", look=-0.9)
    c.restore()
    say(c, "useless2", 400, 520, (220, 900), t)


def sc_black(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000"))


def sc_card(c, t):
    a, b = beat("card")
    grad_rect(c, skia.Rect.MakeWH(W, H), "#1A120D", "#0B0806")
    stone_spear(c, 540, 1700, 0, 600, 1.0, sparkle=pop(t, a + 0.5), t=t)
    kinetic(c, "SỰ THẬT", W / 2, 340, t, a + 0.2, size=90, color="#F4C430", per=0.05)
    p = pop(t, a + 0.7, 0.5)
    lines = ["Ở Kathu Pan, Nam Phi, có những", "mũi đá ~500.000 năm tuổi", "từng được gắn vào giáo.", "",
             "Giáo gỗ nguyên vẹn cổ nhất:", "Schöningen, Đức, ~200.000 năm."]
    for i, l in enumerate(lines):
        text(c, l, W / 2, 520 + i * 82, "bold", 56, "white", a=255 * p, align="center")
    text(c, "Tập sau: kim khâu và áo da", W / 2, 1100, "semi", 40, "#B9B4AA", a=255 * pop(t, a + 2.2), align="center")
    if t > b - 0.8:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 255 * prog(t, b - 0.8, b, lambda q: q)))


FN = {
    "open": sc_open, "lunch": sc_lunch, "charge": sc_charge, "bounce": sc_bounce, "turn": sc_turn, "talk": sc_talk, "chase": sc_chase,
    "skin": lambda c, t: sc_skin(c, t, "skin"), "skin2": lambda c, t: sc_skin(c, t, "skin2"), "climb": sc_climb,
    "hug": sc_hug, "knap": sc_knap, "ouch": sc_ouch, "haft": sc_haft, "glue": sc_glue, "done": sc_done,
    "peek": sc_peek, "tooth": sc_tooth, "ex1": lambda c, t: sc_ex(c, t, "ex1", "club"), "ex2": lambda c, t: sc_ex(c, t, "ex2", "club"),
    "ex3": lambda c, t: sc_ex(c, t, "ex3", "point"), "huh": sc_huh, "finger": sc_finger, "press1": sc_press1, "thorn": sc_thorn,
    "press2": sc_press2, "same": sc_same, "strong": sc_strong, "useless": sc_useless, "snap": sc_snap, "lost": sc_lost,
    "snort": sc_snort, "brother": sc_brother, "bonk2": sc_bonk2, "help": sc_help, "rebuild": sc_rebuild, "catch": sc_catch,
    "aim": sc_aim, "brake": sc_brake, "flee": sc_flee, "win": sc_win, "reach1": lambda c, t: sc_reach(c, t, "reach1"),
    "reach2": lambda c, t: sc_reach(c, t, "reach2"), "fish": sc_fish, "fishstick": sc_fishstick, "mine": sc_mine, "allmine": sc_allmine,
    "sing": sc_sing, "chilly": sc_chilly, "idea": sc_idea, "useless2": sc_useless2, "black": sc_black, "card": sc_card,
}
SCENE_CUT = {T["hug"][0], T["snort"][0], T["fish"][0], T["chilly"][0]}


def draw_frame(c, t):
    for name, (a, b, row) in T.items():
        if a <= t < b:
            FN[name](c, t)
            for sc in SCENE_CUT:
                if sc - 0.3 <= t < sc + 0.3:
                    c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 255 * (1 - abs(t - sc) / 0.3)))
            return
    sc_card(c, min(t, DUR - 0.01))
