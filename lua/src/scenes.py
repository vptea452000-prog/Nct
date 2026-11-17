"""Tập 1: Lửa — phim hoạt hình hài không lời. Bộp (người hiện đại), Gầm (Neanderthal)."""
import math
import skia
from lib import *  # noqa
from toon import OUT, fill_out, rrect_path, oval_path, limb  # noqa
from toon2 import kinetic
from prehist import caveperson, ORANGE
from sets import grad_rect, vignette, blurred
from beats import T, DUR

# ---------------------------------------------------------------- tiện ích


def pop(t, t0, d=0.3):
    return prog(t, t0, t0 + d)


def phase(t, t0, speed=7.0):
    return (t - t0) * speed


def beat(name):
    return T[name][0], T[name][1]


def shake(c, t, t0, amp=16, dur=0.35):
    if t0 <= t < t0 + dur:
        k = 1 - (t - t0) / dur
        c.translate(amp * k * math.sin((t - t0) * 90), amp * k * math.cos((t - t0) * 70))


def cam(c, cx, cy, z):
    c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)


def wrap(s, name, size, maxw):
    words, lines, cur = nfc(s).split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if tw(test, name, size) > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def comic_bubble(c, x, y, s, kind, tail, p, size=54, maxw=760):
    """Bóng thoại truyện tranh. kind: say / shout / think / whisper. tail: (tx, ty) đầu đuôi trỏ về người nói."""
    if p <= 0 or not s:
        return
    name = "xbold"
    lines = wrap(s, name, size, maxw)
    lw = max(tw(l, name, size) for l in lines)
    w = lw + 90
    h = len(lines) * size * 1.25 + 60
    sc = back_out(clamp(p)) if p < 1 else 1.0
    tx, ty = tail
    with Xf(c, x, y, 0, max(0.01, sc)):
        rx, ry = tx - x, ty - y
        if kind == "think":
            for k, r in enumerate([16, 24, 34]):
                q = (k + 1) / 4
                c.drawCircle(rx * (1 - q) * 0.9, ry * (1 - q) * 0.9 + h * 0.2 * q, r, paint("white"))
                c.drawCircle(rx * (1 - q) * 0.9, ry * (1 - q) * 0.9 + h * 0.2 * q, r, paint(OUT, stroke=5))
            path = skia.Path()
            n = 12
            for k in range(n):
                a = k * 2 * math.pi / n
                path.addCircle((w / 2) * 0.92 * math.cos(a), (h / 2) * 0.88 * math.sin(a), min(w, h) * 0.24)
            path.addOval(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h))
            path.setFillType(skia.PathFillType.kWinding)
            c.drawPath(path, paint(OUT, stroke=12)); c.drawPath(path, paint("white"))
        else:
            body = skia.Path()
            if kind == "shout":
                n = 22
                for k in range(n * 2):
                    a = k * math.pi / n
                    r = 1.0 if k % 2 == 0 else 0.82
                    px, py = (w / 2 + 40) * r * math.cos(a), (h / 2 + 40) * r * math.sin(a)
                    (body.moveTo if k == 0 else body.lineTo)(px, py)
                body.close()
            else:
                body.addOval(skia.Rect.MakeXYWH(-w / 2 - 10, -h / 2 - 6, w + 20, h + 12))
            # đuôi
            ang = math.atan2(ry, rx)
            bx, by = (w / 2) * 0.6 * math.cos(ang), (h / 2) * 0.6 * math.sin(ang)
            nx, ny = -math.sin(ang) * 30, math.cos(ang) * 30
            tail_p = skia.Path(); tail_p.moveTo(bx + nx, by + ny); tail_p.lineTo(rx * 0.75, ry * 0.75); tail_p.lineTo(bx - nx, by - ny); tail_p.close()
            fillc = "#FFF3B0" if kind == "shout" else "white"
            dash = skia.DashPathEffect.Make([16, 10], 0) if kind == "whisper" else None
            st = paint(OUT, stroke=12); st2 = paint(OUT, stroke=6)
            if dash:
                st2.setPathEffect(dash)
            c.drawPath(tail_p, st); c.drawPath(body, st)
            c.drawPath(tail_p, paint(fillc)); c.drawPath(body, paint(fillc))
            if dash:
                c.drawPath(body, paint(fillc, stroke=12)); c.drawPath(body, st2)
        for i, l in enumerate(lines):
            yy = -h / 2 + 30 + size * 0.95 + i * size * 1.25
            text(c, l, 0, yy, name, size, "#C0392B" if kind == "shout" else "ink", align="center")


def sfx_word(c, s, x, y, t, t0, size=110, color="#F4C430", rot=-8, dur=0.9):
    a = t - t0
    if a < 0 or a > dur:
        return
    sc = back_out(clamp(a / 0.2)) if a < 0.2 else 1.0
    al = 1 - clamp((a - dur + 0.25) / 0.25)
    with Xf(c, x, y, rot, max(0.01, sc), al):
        text(c, s, 0, size * 0.35, "xbold", size, color, align="center", stroke=size * 0.1, stroke_color="#1A120D")


# ---------------------------------------------------------------- bối cảnh & đạo cụ
def dusk_sky(c, night=0.0, morning=0.0):
    if morning > 0:
        grad_rect(c, skia.Rect.MakeWH(W, H), "#9FC9E6", "#F6E7C0")
    else:
        top = "#F08A4B" if night < 0.5 else "#15203A"
        bot = "#F6C67A" if night < 0.5 else "#2E3A5A"
        grad_rect(c, skia.Rect.MakeWH(W, H), top, bot)


def cave_exterior(c, t, night=0.0, morning=0.0, wind=True):
    dusk_sky(c, night, morning)
    if morning == 0 and night < 0.5:
        c.drawCircle(820, 760, 120, paint("#FFD08A", 220))
    for k, (yy, colr) in enumerate([(900, "#B98A6A"), (980, "#9A6E52")]):
        p = skia.Path(); p.moveTo(-200, 1500)
        for i in range(0, 16):
            p.lineTo(-200 + i * 110, yy - 140 * abs(math.sin(i * 0.9 + k)))
        p.lineTo(W + 200, 1500); p.close()
        c.drawPath(p, paint(colr))
    # vách đá có miệng hang bên trái
    rock = skia.Path(); rock.moveTo(-200, 1300); rock.lineTo(-200, 300); rock.quadTo(250, 200, 520, 520); rock.quadTo(640, 900, 600, 1300); rock.close()
    fill_out(c, rock, "#7A6A5A")
    mouth = skia.Path(); mouth.moveTo(40, 1300); mouth.quadTo(40, 760, 240, 740); mouth.quadTo(440, 760, 450, 1300); mouth.close()
    fill_out(c, mouth, "#1E1712")
    c.drawRect(skia.Rect.MakeXYWH(-200, 1290, W + 400, 900), paint("#8A7A52"))
    c.drawRect(skia.Rect.MakeXYWH(-200, 1290, W + 400, 14), paint(OUT, 120))
    for k in range(9):
        x = (k * 157) % W
        c.drawLine(x, 1330 + k * 20, x + 40, 1330 + k * 20, paint("#6E6038", stroke=5))
    if wind:
        for k in range(5):
            x = (t * 600 + k * 300) % (W + 600) - 300
            y = 500 + k * 120
            pth = skia.Path(); pth.moveTo(x, y); pth.quadTo(x + 80, y - 30, x + 160, y)
            c.drawPath(pth, paint("white", 110, stroke=5))
    if night > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#0B1020", 170 * night))


def cave_interior(c, t, rain=True):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#2A211B", "#120D0A")
    # cửa hang (mưa đêm bên ngoài)
    door = skia.Path(); door.moveTo(700, 1300); door.quadTo(720, 700, 900, 680); door.quadTo(1080, 700, 1100, 1300); door.close()
    c.save(); c.clipPath(door, skia.ClipOp.kIntersect, True)
    grad_rect(c, skia.Rect.MakeXYWH(680, 650, 440, 700), "#1D2A44", "#2E3A5A")
    if rain:
        for k in range(40):
            x = 700 + (k * 53) % 420; y = 650 + ((k * 97 + t * 1600) % 700)
            c.drawLine(x, y, x - 10, y + 40, paint("#9FB3CC", 200, stroke=3))
    c.restore()
    c.drawPath(door, paint(OUT, stroke=8))
    c.drawRect(skia.Rect.MakeXYWH(-100, 1290, W + 200, 900), paint("#3A2E24"))
    for k in range(7):
        c.drawCircle(80 + k * 160, 300 + (k % 3) * 60, 50, paint("#3A2E24"))


def fire(c, x, y, s, t, strength=1.0, seed=0):
    if strength <= 0:
        return
    with Xf(c, x, y, 0, s):
        for k in range(3):
            c.drawLine(-80, 10 - k * 6, 80, -10 + k * 6, paint("#5A3E26", stroke=18))
            c.drawLine(-80, 10 - k * 6, 80, -10 + k * 6, paint(OUT, stroke=3))
        glow = paint("#F39C12", 80 * strength); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 70))
        c.drawCircle(0, -60, 260 * strength, glow)
        for k, (colr, sc) in enumerate([("#C0392B", 1.0), ("#F39C12", 0.72), ("#F4D03F", 0.45)]):
            fl = skia.Path(); wob = 12 * math.sin(t * 13 + k + seed)
            h = 210 * sc * strength
            fl.moveTo(-64 * sc, 0); fl.quadTo(-74 * sc, -h * 0.5, wob, -h); fl.quadTo(74 * sc, -h * 0.5, 64 * sc, 0); fl.close()
            c.drawPath(fl, paint(colr, 240))
        for k in range(3):
            a = (t * 1.6 + k * 0.33) % 1
            c.drawCircle(20 * math.sin(k * 3 + t * 4), -h - a * 160, 6 * (1 - a), paint("#F4D03F", 230 * (1 - a)))


def smoke(c, x, y, t, t0, n=8, a=170, spread=1.0):
    for k in range(n):
        st = t0 + k * 0.12; age = t - st
        if age <= 0:
            continue
        r = 20 + age * 40
        sp = paint("#B8B0A6", a * clamp(1 - age / 1.6))
        sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6 + age * 10))
        c.drawCircle(x + spread * 30 * math.sin(k * 2.1) + age * 30, y - age * 160, r, sp)


def wood_stick(c, x, y, ang, L=520, s=1.0, burning=0.0, t=0.0):
    with Xf(c, x, y, ang, s):
        c.drawLine(0, 0, 0, -L, paint(OUT, stroke=24)); c.drawLine(0, 0, 0, -L, paint("#8A6A44", stroke=16))
        if burning > 0:
            fire(c, 0, -L + 30, 0.55 * burning, t, 1.0)


def meat(c, x, y, s, t, cooked=1.0):
    with Xf(c, x, y, 0, s):
        c.drawLine(-160, 0, 160, 0, paint(OUT, stroke=14)); c.drawLine(-160, 0, 160, 0, paint("#8A6A44", stroke=8))
        m = skia.Path(); m.addOval(skia.Rect.MakeXYWH(-80, -50, 160, 100))
        colr = "#C0392B" if cooked < 0.5 else "#8E4A2A"
        fill_out(c, m, colr)
        c.drawLine(-40, -20, 30, -30, paint("#E9A06A", stroke=6))


def smell(c, x0, y0, x1, y1, t, a=200):
    for k in range(3):
        ph = (t * 0.6 + k * 0.33) % 1
        x = lerp(x0, x1, ph); y = lerp(y0, y1, ph) - 40 * math.sin(ph * math.pi)
        pth = skia.Path(); pth.moveTo(x - 40, y)
        for j in range(4):
            pth.quadTo(x - 30 + j * 20, y + (-20 if j % 2 else 20), x - 20 + j * 20, y)
        c.drawPath(pth, paint("#F6E7C0", a * math.sin(ph * math.pi), stroke=6))


def wolf(c, x, y, s, t, flip=False, run=None, eyes_only=False, scared=0.0):
    with Xf(c, x, y, 0, s):
        if flip:
            c.scale(-1, 1)
        if not eyes_only:
            body = skia.Path(); body.moveTo(-160, -60); body.quadTo(0, -120, 140, -70); body.lineTo(150, 10); body.quadTo(0, 30, -150, 10); body.close()
            fill_out(c, body, "#4A4E58")
            head = skia.Path(); head.moveTo(130, -80); head.lineTo(230, -60); head.lineTo(260, -30); head.lineTo(200, -10); head.lineTo(140, 0); head.close()
            fill_out(c, head, "#4A4E58")
            for ex in (150, 185):
                ear = skia.Path(); ear.moveTo(ex - 14, -76); ear.lineTo(ex, -120 + scared * 30); ear.lineTo(ex + 14, -76); ear.close()
                fill_out(c, ear, "#3A3E48", ow=5)
            tail = skia.Path(); tail.moveTo(-150, -50); tail.quadTo(-240, -100 + scared * 120, -260, -40 + scared * 120)
            c.drawPath(tail, paint(OUT, stroke=30)); c.drawPath(tail, paint("#4A4E58", stroke=20))
            ph = 0 if run is None else run
            for k, lx in enumerate([-110, -60, 70, 120]):
                a = 25 * math.sin(ph + k * 1.6)
                with Xf(c, lx, 0, a, 1):
                    c.drawLine(0, 0, 0, 90, paint(OUT, stroke=26)); c.drawLine(0, 0, 0, 90, paint("#4A4E58", stroke=16))
        for ex in (175, 205) if not eyes_only else (-25, 25):
            g = paint("#F4D03F", 255); gl = paint("#F4D03F", 120); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
            ey = -52 if not eyes_only else 0
            c.drawCircle(ex, ey, 18, gl); c.drawOval(skia.Rect.MakeXYWH(ex - 10, ey - 6, 20, 12), g)


def flat_stone(c, x, y, s, rot=0):
    with Xf(c, x, y, rot, s):
        p = skia.Path(); p.moveTo(-60, 0); p.lineTo(-10, -90); p.lineTo(40, -60); p.lineTo(60, 10); p.lineTo(0, 40); p.close()
        fill_out(c, p, "#9AA3A8")
        c.drawLine(-10, -60, 20, 10, paint("#7A8388", stroke=5))


def log(c, x, y, w=420):
    fill_out(c, rrect_path(x - w / 2, y - 70, w, 140, 60), "#7A5636")
    c.drawCircle(x + w / 2 - 50, y, 46, paint("#C9A06A")); c.drawCircle(x + w / 2 - 50, y, 46, paint(OUT, stroke=5))
    c.drawCircle(x + w / 2 - 50, y, 24, paint(OUT, stroke=3))


def bop(c, x, y, s, t, **kw):
    kw.setdefault("spear", False)
    caveperson(c, x, y, s, t=t, kind="sap", **kw)


def gam(c, x, y, s, t, stick=True, stick_ang=8, burning=0.0, **kw):
    kw.setdefault("spear", False)
    flip = kw.get("flip", False)
    caveperson(c, x, y, s, t=t, kind="nea", **kw)
    if stick:
        arm = kw.get("arm", "down")
        side = -1 if flip else 1
        if arm == "up":
            hx, hy = x + side * 158 * s * 1.18, y - 710 * s * 0.92
        else:
            hx, hy = x + side * 132 * s, y - 250 * s
        rot = kw.get("rot", 0.0)
        if rot:
            dx, dy = hx - x, hy - y
            ar = math.radians(rot)
            hx, hy = x + dx * math.cos(ar) - dy * math.sin(ar), y + dx * math.sin(ar) + dy * math.cos(ar)
        wood_stick(c, hx, hy + 140 * s, stick_ang * side, 520, s, burning, t)


# ---------------------------------------------------------------- CẢNH 1
def sc_open(c, t):
    a, b = beat("open")
    z = lerp(0.95, 1.12, ease_in_out(clamp((t - a) / (b - a))))
    c.save(); cam(c, 540, 1000, z); cave_exterior(c, t)
    bop(c, 600, 1290, 0.9, t, look=0.3)
    log(c, 640, 1300, 380)
    c.restore()
    vignette(c, 130)
    kinetic(c, "TẬP 1", W / 2, 420, t, a + 0.3, size=70, per=0.04)
    kinetic(c, "LỬA", W / 2, 560, t, a + 0.6, size=180, color="#F4C430", per=0.08)


def drill_insert(c, t, t0, spin=True):
    grad_rect(c, skia.Rect.MakeWH(W, H), "#6E5A44", "#3A2E22")
    fill_out(c, rrect_path(140, 1000, 800, 160, 20), "#A57A4A")
    for k in range(4):
        c.drawLine(180, 1040 + k * 30, 900, 1040 + k * 30, paint("#8A6036", stroke=4))
    ang = 6 * math.sin(t * 40) if spin else 0
    with Xf(c, 540, 1010, ang, 1):
        c.drawLine(0, 0, 0, -620, paint(OUT, stroke=34)); c.drawLine(0, 0, 0, -620, paint("#C9A06A", stroke=24))
    for side in (-1, 1):
        dx = 20 * math.sin(t * 40) * side
        limb(c, [(side * 520 + 540, 300), (side * 220 + 540, 520), (540 + side * 30 + dx, 640)], 60, "#8A5A3C")
        fill_out(c, oval_path(540 + side * 40 + dx, 650, 56, 44), "#8A5A3C")
    smoke(c, 540, 1000, t, t0 + 0.3, n=10)
    c.drawCircle(540, 1010, 30, paint("#C0392B", 180 * clamp((t - t0) / 2.5)))


def sc_drill(c, t):
    a, b = beat("drill")
    drill_insert(c, t, a)
    comic_bubble(c, 540, 330, T["drill"][2][5], "say", (300, 520), pop(t, a + 0.1))
    sfx_word(c, "VÈO VÈO", 820, 1250, t, a + 0.4, size=80, dur=2.2)


def sc_spark(c, t):
    a, b = beat("spark")
    c.save(); cam(c, 540, 1100, 1.6)
    cave_exterior(c, t)
    log(c, 540, 1290, 380)
    for k in range(10):
        c.drawLine(420 + k * 24, 1300, 430 + k * 24 + 10 * math.sin(k), 1240, paint("#D9B65A", stroke=6))
    st = prog(t, a + 0.6, a + 2.2)
    fire(c, 540, 1300, 0.8, t, st)
    if t < a + 0.8:
        c.drawCircle(540, 1290, 12, paint("#F4D03F"));
    c.restore()
    bop_face = pop(t, a + 1.0)
    vignette(c, 150)
    sfx_word(c, "PHÙ…", 300, 600, t, a + 0.7, size=90, color="white", dur=0.9)
    sfx_word(c, "BÙNG!", 700, 520, t, a + 1.7, size=130, dur=0.9)


def bop_by_fire(c, t, mood="smile", look=0.3, fire_s=1.0, gam_x=None, gam_kw=None, z=1.0, cx=540, cy=1000, fire_on=1.0, smoke_t0=None):
    c.save(); cam(c, cx, cy, z)
    cave_exterior(c, t)
    fire(c, 560, 1300, 0.75 * fire_s, t, fire_on)
    if smoke_t0 is not None:
        smoke(c, 560, 1250, t, smoke_t0, n=12, a=200)
    bop(c, 830, 1300, 0.95, t, mood=mood, look=-0.5, flip=True, **({} if mood is None else {}))
    if gam_x is not None:
        gam(c, gam_x, 1300, 0.95, t, **(gam_kw or {}))
    c.restore()


def sc_warm(c, t):
    a, b = beat("warm")
    c.save(); cam(c, 540, 1000, 1.0)
    cave_exterior(c, t)
    fire(c, 520, 1300, 0.75, t)
    bop(c, 800, 1300, 0.95, t, mood="smile", look=-0.5, flip=True, arm="hold", talk=a < t < a + 1.2)
    c.restore()
    comic_bubble(c, 640, 400, T["warm"][2][5], "say", (780, 640), pop(t, a + 0.1))


def sc_jump(c, t, name="jump"):
    a, b = beat(name)
    c.save(); shake(c, t, a + 0.05, 20)
    c.save(); cam(c, 540, 1000, 1.0)
    cave_exterior(c, t)
    fire(c, 520, 1300, 0.75, t)
    bop(c, 830, 1300, 0.95, t, mood="surprise", look=-0.6, flip=True, arm="up")
    jy = 1300 - (220 * math.sin(math.pi * clamp((t - a) / 0.5)) if name == "jump" else 0)
    jx = lerp(240, 240, 1)
    gam(c, jx, jy, 0.95, t, arm="up", mood="angry", look=0.6, talk=True, stick_ang=20)
    c.restore(); c.restore()
    if name == "jump":
        sfx_word(c, "BỤP!", 300, 520, t, a, size=140, dur=0.8)
    comic_bubble(c, 400, 330, T[name][2][5], "shout", (260, 560), pop(t, a + 0.15))


def two_shot(c, t, name, bop_kw=None, gam_kw=None, z=1.12, cx=540, cy=1050, fire_on=1.0, smoke_t0=None, bubble_x=None):
    a, b = beat(name)
    row = T[name][2]
    spk, kind, txt = row[3], row[4], row[5]
    talking = a + 0.1 < t < b - 0.5
    bk = dict(mood="flat", look=-0.6, flip=True)
    bk.update(bop_kw or {})
    gk = dict(mood="angry", look=0.6, arm="down")
    gk.update(gam_kw or {})
    if spk == "bop":
        bk["talk"] = talking
    if spk == "gam":
        gk["talk"] = talking
    c.save(); cam(c, cx, cy, z)
    cave_exterior(c, t)
    fire(c, 540, 1300, 0.75, t, fire_on)
    if smoke_t0 is not None:
        smoke(c, 540, 1240, t, smoke_t0, n=14, a=210)
    bop(c, 820, 1300, 0.95, t, **bk)
    gam(c, 260, 1300, 0.95, t, **gk)
    c.restore()
    if txt:
        tx, ty = ((800, 600) if spk == "bop" else (290, 600))
        bx = bubble_x or (620 if spk == "bop" else 460)
        sx = (tx - cx) * z + W / 2
        comic_bubble(c, bx, 360, txt, kind, (sx, ty), pop(t, a + 0.1))


def sc_no(c, t):
    two_shot(c, t, "no", bop_kw=dict(mood="flat", arm="up"))


def sc_name(c, t):
    a, b = beat("name")
    two_shot(c, t, "name", bop_kw=dict(mood="smile"))
    sfx_word(c, "LỬA", 540, 900, t, a + 0.9, size=120, dur=1.0)


def sc_warm2(c, t):
    two_shot(c, t, "warm2", bop_kw=dict(mood="smile", arm="hold"))


def sc_what(c, t):
    two_shot(c, t, "what", gam_kw=dict(arm="up", stick_ang=-10))


def sc_red(c, t):
    a, b = beat("red")
    two_shot(c, t, "red", gam_kw=dict(arm="down", look=0.9), z=1.25, cx=420, cy=1050)
    sfx_word(c, "TÁCH TÁCH", 700, 1100, t, a + 1.4, size=70, color="#F39C12", dur=1.1)


def sc_useless(c, t):
    a, b = beat("useless")
    c.save(); shake(c, t, a + 0.1, 14)
    two_shot(c, t, "useless", gam_kw=dict(arm="up"), z=1.5, cx=330, cy=900)
    c.restore()


def sc_stomp(c, t):
    a, b = beat("stomp")
    fire_on = 1 - prog(t, a + 1.2, a + 1.8)
    hop = abs(math.sin((t - a) * 9)) * 60 if t < a + 1.8 else 0
    c.save(); cam(c, 540, 1050, 1.15)
    cave_exterior(c, t)
    fire(c, 540, 1300, 0.75, t, fire_on)
    if t > a + 1.6:
        smoke(c, 540, 1250, t, a + 1.6, n=14, a=220, spread=0.5)
    bop(c, 860, 1300, 0.95, t, mood="surprise", look=-0.6, flip=True)
    gam(c, 520, 1300 - hop, 0.95, t, mood="angry", look=0.2, stick=t < a + 0.5)
    c.restore()
    for k, ts in enumerate([a + 0.2, a + 0.6, a + 1.0, a + 1.4]):
        sfx_word(c, "BÌNH!" if k % 2 == 0 else "BỊCH!", 300 + (k % 2) * 480, 600 + k * 40, t, ts, size=100, dur=0.5, rot=(-1) ** k * 8)
    sfx_word(c, "KHỤ KHỤ!", 540, 520, t, a + 2.0, size=96, color="white", dur=0.8)


def sc_smoke(c, t):
    a, b = beat("smoke")
    c.save(); cam(c, 400, 900, 1.5)
    cave_exterior(c, t)
    fire(c, 540, 1300, 0.75, t, 0)
    smoke(c, 520, 1150, t, a - 0.6, n=14, a=200)
    gam(c, 420, 1300, 0.95, t, mood="angry", look=0.5, talk=a + 0.1 < t < b - 0.4, stick=False, arm="up")
    c.restore()
    comic_bubble(c, 560, 330, T["smoke"][2][5], "shout", (420, 520), pop(t, a + 0.1))


def sc_danger(c, t):
    a, b = beat("danger")
    p = clamp((t - a) / (b - a))
    c.save(); cam(c, 540, 1000, 1.0)
    cave_exterior(c, t)
    fire(c, 540, 1300, 0.75, t, 0)
    smoke(c, 540, 1250, t, a - 1.2, n=6, a=120)
    bop(c, 820, 1300, 0.95, t, mood="sad", look=-0.6, flip=True)
    gam(c, lerp(300, 200, p), 1300, 0.95, t, mood="angry", look=-0.3, flip=True, walk=phase(t, a, 8), talk=a + 0.1 < t < b - 0.3)
    c.restore()
    comic_bubble(c, 420, 360, T["danger"][2][5], "shout", (260, 600), pop(t, a + 0.1))


def sc_sigh(c, t):
    a, b = beat("sigh")
    c.save(); cam(c, 640, 1150, 1.6)
    cave_exterior(c, t, night=0.2)
    fire(c, 540, 1300, 0.75, t, 0)
    for k in range(6):
        c.drawCircle(480 + k * 24, 1300, 18, paint("#5A5048"))
    smoke(c, 540, 1280, t, a, n=5, a=90)
    bop(c, 780, 1300, 0.95, t, mood="sad", look=-0.6, flip=True)
    c.restore()
    vignette(c, 160)
    comic_bubble(c, 700, 380, T["sigh"][2][5], "think", (780, 560), pop(t, a + 0.4))


# ---------------------------------------------------------------- CẢNH 2
def inside(c, t, gam_kw=None, bop_kw=None, fire_on=1.0, z=1.0, cx=540, cy=1000, meat_on=True, gx=200, smell_on=False):
    c.save(); cam(c, cx, cy, z)
    cave_interior(c, t)
    glow = paint("#F39C12", 60 * fire_on); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 200))
    c.drawCircle(720, 1150, 420, glow)
    fire(c, 720, 1300, 0.6, t, fire_on)
    if meat_on:
        meat(c, 720, 1130, 0.8, t)
    bk = dict(mood="smile", look=-0.6, flip=True)
    bk.update(bop_kw or {})
    bop(c, 940, 1300, 0.9, t, **bk)
    gk = dict(mood="flat", look=0.6, stick=False)
    gk.update(gam_kw or {})
    gam(c, gx, 1300, 0.9, t, **gk)
    if smell_on:
        smell(c, 720, 1050, gx + 60, 720, t)
    c.restore()


def sc_cold(c, t):
    a, b = beat("cold")
    c.save(); cam(c, 260, 1000, 1.5)
    cave_interior(c, t)
    jit = 5 * math.sin(t * 60)
    gam(c, 260 + jit, 1300, 0.9, t, mood="sad", look=0.0, stick=False, talk=a + 0.1 < t < b - 0.4)
    c.restore()
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#2E4A7A", 70))
    comic_bubble(c, 560, 360, T["cold"][2][5], "say", (300, 560), pop(t, a + 0.1))
    sfx_word(c, "CẬP CẬP", 760, 900, t, a + 0.5, size=80, color="#BFD3E6", dur=2.0)


def sc_glow(c, t):
    a, b = beat("glow")
    p = clamp((t - a) / (b - a))
    gx = lerp(200, 330, ease_in_out(clamp((t - a - 1.4) / 1.4)))
    inside(c, t, gam_kw=dict(mood="surprise", look=0.8, rot=20 * clamp((t - a - 1.4) / 0.5)), smell_on=True, gx=gx,
           z=lerp(1.4, 1.0, ease_out(clamp((t - a) / 1.0))), cx=lerp(720, 540, ease_out(clamp((t - a) / 1.0))))
    sfx_word(c, "KHỊT KHỊT", 300, 560, t, a + 1.0, size=80, color="white", dur=1.4)


def sc_raise(c, t):
    a, b = beat("raise")
    inside(c, t, gam_kw=dict(mood="flat", look=0.8, talk=a + 0.1 < t < b - 0.4, rot=18), gx=330)
    comic_bubble(c, 480, 380, T["raise"][2][5], "say", (360, 640), pop(t, a + 0.1))


def sc_tasty(c, t):
    a, b = beat("tasty")
    inside(c, t, bop_kw=dict(talk=a + 0.1 < t < b - 0.4, arm="hold"), gam_kw=dict(look=0.8, rot=18), gx=330, smell_on=True)
    comic_bubble(c, 640, 380, T["tasty"][2][5], "say", (920, 640), pop(t, a + 0.1))


def sc_try(c, t):
    a, b = beat("try")
    inside(c, t, bop_kw=dict(talk=a + 0.1 < t < b - 0.4, arm="wave"), gam_kw=dict(look=0.8, rot=18), gx=330, z=1.2, cx=700, cy=1000)
    comic_bubble(c, 700, 380, T["try"][2][5], "say", (900, 640), pop(t, a + 0.1))


def sc_nope(c, t):
    a, b = beat("nope")
    inside(c, t, gam_kw=dict(mood="angry", look=-0.8, flip=True, talk=a + 0.1 < t < b - 0.3), gx=330, z=1.4, cx=380, cy=950)
    comic_bubble(c, 520, 340, T["nope"][2][5], "shout", (360, 560), pop(t, a + 0.1))


def sc_growl(c, t):
    a, b = beat("growl")
    c.save(); shake(c, t, a + 0.3, 10, 0.6)
    inside(c, t, gam_kw=dict(mood="surprise", look=-0.3, flip=True), gx=330, z=1.6, cx=330, cy=1000)
    c.restore()
    sfx_word(c, "ỌC ỌC ỌC", 540, 900, t, a + 0.2, size=120, color="#F39C12", dur=1.3)
    if t > a + 1.5:
        text(c, "…", W / 2, 500, "xbold", 200, "white", a=255 * pop(t, a + 1.5), align="center", stroke=10, stroke_color="#1A120D")


def sc_onebite(c, t):
    a, b = beat("onebite")
    inside(c, t, gam_kw=dict(mood="flat", look=0.8, talk=a + 0.1 < t < b - 0.4, rot=10), gx=420, z=1.3, cx=500, cy=1000)
    comic_bubble(c, 520, 380, T["onebite"][2][5], "whisper", (420, 600), pop(t, a + 0.1))


# ---------------------------------------------------------------- CẢNH 3
def night_cave(c, t, wolves=None, gam_kw=None, bop_kw=None, fire_on=1.0, burning=0.0, z=1.0, cx=540, cy=1000, gx=330):
    gx = {330: 600, 420: 600, 440: 610}.get(gx, gx)
    c.save(); cam(c, cx, cy, z)
    cave_interior(c, t, rain=False)
    if wolves:
        wolves(c)
    glow = paint("#F39C12", 60 * fire_on); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 200))
    c.drawCircle(380, 1150, 420, glow)
    fire(c, 380, 1300, 0.6, t, fire_on)
    bk = dict(mood="flat", look=0.6)
    bk.update(bop_kw or {})
    bop(c, 160, 1300, 0.9, t, **bk)
    gk = dict(mood="flat", look=0.6)
    gk.update(gam_kw or {})
    gam(c, gx, 1300, 0.9, t, burning=burning, **gk)
    c.restore()


def eyes_at_door(c, t, t0):
    for k, (x, y) in enumerate([(820, 1050), (980, 1100)]):
        if t > t0 + k * 0.3:
            wolf(c, x, y, 1.0, t, eyes_only=True)


def sc_wolves(c, t):
    a, b = beat("wolves")
    night_cave(c, t, wolves=lambda cc: eyes_at_door(cc, t, a + 0.5), gam_kw=dict(mood="surprise", look=1.0), bop_kw=dict(mood="surprise", look=1.0), gx=420,
               z=lerp(1.0, 1.25, clamp((t - a) / (b - a))), cx=760)
    sfx_word(c, "GRỪ…", 760, 600, t, a + 0.2, size=110, color="#BFC6D0", dur=2.0)


def sc_wolf(c, t):
    a, b = beat("wolf")
    night_cave(c, t, wolves=lambda cc: eyes_at_door(cc, t, -10), bop_kw=dict(mood="surprise", look=0.8, talk=a + 0.1 < t < b - 0.3), gx=420, z=1.4, cx=300, cy=1000)
    comic_bubble(c, 420, 400, T["wolf"][2][5], "whisper", (200, 560), pop(t, a + 0.1))


def sc_letme(c, t):
    a, b = beat("letme")
    night_cave(c, t, wolves=lambda cc: eyes_at_door(cc, t, -10), gam_kw=dict(mood="angry", arm="up", talk=a + 0.1 < t < b - 0.2), gx=420)
    comic_bubble(c, 600, 380, T["letme"][2][5], "shout", (620, 560), pop(t, a + 0.1))


def sc_hot(c, t):
    a, b = beat("hot")
    slip = clamp((t - a) / 0.5)
    c.save(); shake(c, t, a + 0.5, 18)
    wave = 30 * math.sin((t - a) * 14) if t > a + 0.7 else 0
    night_cave(c, t, wolves=lambda cc: eyes_at_door(cc, t, -10),
               gam_kw=dict(mood="surprise", arm="up", talk=a + 0.6 < t < b - 0.2, stick_ang=wave if t > a + 0.7 else lerp(10, 60, slip),
                           rot=-12 * math.sin(slip * math.pi)), burning=pop(t, a + 0.55, 0.2), gx=440, fire_on=1.0)
    c.restore()
    sfx_word(c, "PHỪNG!", 820, 1000, t, a + 0.5, size=110, dur=0.7)
    comic_bubble(c, 560, 340, T["hot"][2][5], "shout", (620, 540), pop(t, a + 0.7))


def sc_flee(c, t):
    a, b = beat("flee")
    p = clamp((t - a - 0.4) / 1.4)

    def wolves(cc):
        for k, (x, y) in enumerate([(840, 1260), (1000, 1290)]):
            wolf(cc, x + 700 * p, y, 0.7, t, flip=False, run=phase(t, a, 14) if p > 0 else None, scared=pop(t, a, 0.3))
    night_cave(c, t, wolves=wolves, gam_kw=dict(mood="surprise", arm="up", stick_ang=20 * math.sin((t - a) * 10)), burning=1.0, gx=440)
    sfx_word(c, "ẲNG ẲNG!", 820, 700, t, a + 0.3, size=100, color="white", dur=1.2)


def sc_afraid(c, t):
    a, b = beat("afraid")
    night_cave(c, t, gam_kw=dict(mood="flat", arm="up", look=1.0, talk=a + 0.6 < t < b - 0.3, stick_ang=10), burning=1.0, gx=440, z=1.4, cx=620, cy=950)
    comic_bubble(c, 540, 330, T["afraid"][2][5], "say", (520, 540), pop(t, a + 0.5))


def sc_fact(c, t):
    a, b = beat("fact")
    night_cave(c, t, gam_kw=dict(mood="flat", arm="up", look=-0.6, stick_ang=10), bop_kw=dict(mood="smile", talk=a + 0.1 < t < b - 0.3), burning=1.0, gx=440)
    comic_bubble(c, 400, 380, T["fact"][2][5], "say", (170, 600), pop(t, a + 0.1))


def sc_invent(c, t):
    a, b = beat("invent")
    grad_rect(c, skia.Rect.MakeWH(W, H), "#3A2418", "#120D0A")
    for k in range(14):
        ang = k * math.pi / 7 + t * 0.4
        p = skia.Path(); p.moveTo(540, 900)
        p.lineTo(540 + 1800 * math.cos(ang), 900 + 1800 * math.sin(ang)); p.lineTo(540 + 1800 * math.cos(ang + 0.18), 900 + 1800 * math.sin(ang + 0.18)); p.close()
        c.drawPath(p, paint("#F39C12", 50))
    c.save(); cam(c, 540, 950, 1.35)
    gam(c, 540, 1300, 0.95, t, mood="smile", arm="up", stick_ang=0, burning=1.0, talk=a + 0.1 < t < b - 0.4)
    c.restore()
    comic_bubble(c, 540, 330, T["invent"][2][5], "shout", (560, 540), pop(t, a + 0.1))


def sc_mine(c, t):
    a, b = beat("mine")
    night_cave(c, t, gam_kw=dict(mood="smile", arm="up", look=0.0, stick_ang=0), bop_kw=dict(mood="sad", look=0.8, talk=a + 0.1 < t < b - 0.3, arm="up"), burning=1.0, gx=440)
    comic_bubble(c, 400, 380, T["mine"][2][5], "say", (170, 600), pop(t, a + 0.1))


def sc_allmine(c, t):
    a, b = beat("allmine")
    c.save(); shake(c, t, a + 0.1, 10)
    night_cave(c, t, gam_kw=dict(mood="angry", arm="up", look=-0.6, talk=a + 0.1 < t < b - 0.3, stick_ang=-10), bop_kw=dict(mood="surprise", look=0.8), burning=1.0, gx=440,
               z=1.25, cx=560, cy=950)
    c.restore()
    comic_bubble(c, 560, 380, T["allmine"][2][5], "shout", (600, 560), pop(t, a + 0.1))


def sc_hog(c, t):
    a, b = beat("hog")
    c.save(); cam(c, 540, 1000, 1.0)
    cave_interior(c, t, rain=False)
    fire(c, 220, 1300, 0.6, t)
    gam(c, 380, 1300, 0.9, t, mood="smile", look=-0.6, flip=True, stick=False)
    bop(c, 850, 1300, 0.9, t, mood="sad", look=-0.8, flip=True)
    c.restore()
    vignette(c, 170)
    sfx_word(c, "HỪM!", 380, 600, t, a + 0.4, size=100, dur=1.2)


# ---------------------------------------------------------------- CẢNH 4
def sc_stone(c, t):
    a, b = beat("stone")
    c.save(); cam(c, 700, 1000, 1.1)
    cave_exterior(c, t, morning=1.0, wind=False)
    pick = clamp((t - a - 0.4) / 0.6)
    bop(c, 760, 1300, 0.95, t, mood="flat", look=0.5 if t < a + 1.2 else -0.3, arm="up" if pick > 0.5 else "down")
    flat_stone(c, lerp(900, 830, pick), lerp(1290, 700, ease_out(pick)), 1.0, rot=t * 20 if pick > 0.9 else 0)
    c.restore()
    sfx_word(c, "CHIM HÓT", 300, 420, t, a, size=60, color="white", dur=2.0)


def sc_idea(c, t):
    a, b = beat("idea")
    c.save(); cam(c, 600, 1000, 1.25)
    cave_exterior(c, t, morning=1.0, wind=False)
    wood_stick(c, 330, 1300, -70, 520, 0.9)
    bop(c, 760, 1300, 0.95, t, mood="surprise" if t < a + 1.4 else "smile", look=-0.8, arm="up")
    flat_stone(c, 830, 700, 1.0)
    c.restore()
    p = pop(t, a + 0.3)
    comic_bubble(c, 520, 380, T["idea"][2][5], "think", (760, 620), p)
    if t > a + 1.6:
        with Xf(c, 820, 560, 0, back_out(pop(t, a + 1.6))):
            c.drawLine(0, 0, 0, -160, paint(OUT, stroke=14)); c.drawLine(0, 0, 0, -160, paint("#8A6A44", stroke=8))
            flat_stone(c, 0, -150, 0.7, rot=0)


def sc_useless2(c, t):
    a, b = beat("useless2")
    c.save(); cam(c, 300, 1000, 1.1)
    cave_exterior(c, t, morning=1.0, wind=False)
    bop(c, 760, 1300, 0.95, t, mood="sad", look=-0.9, arm="down")
    c.restore()
    comic_bubble(c, 380, 520, T["useless2"][2][5], "shout", (220, 900), pop(t, a + 0.1))


def sc_black(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000"))


def sc_card(c, t):
    a, b = beat("card")
    grad_rect(c, skia.Rect.MakeWH(W, H), "#1A120D", "#0B0806")
    fire(c, 540, 1500, 0.9, t, pop(t, a, 0.6))
    kinetic(c, "SỰ THẬT", W / 2, 380, t, a + 0.2, size=90, color="#F4C430", per=0.05)
    p = pop(t, a + 0.7, 0.5)
    lines = ["Con người đã dùng lửa", "từ khoảng 1 triệu năm trước.", "", "Nấu chín giúp thức ăn", "mềm và dễ tiêu hóa hơn."]
    for i, l in enumerate(lines):
        text(c, l, W / 2, 580 + i * 90, "bold", 64, "white", a=255 * p, align="center")
    text(c, "Tập sau: cây giáo", W / 2, 1120, "semi", 40, "#B9B4AA", a=255 * pop(t, a + 2.0), align="center")
    if t > b - 0.8:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 255 * prog(t, b - 0.8, b, lambda q: q)))


FN = {
    "open": sc_open, "drill": sc_drill, "spark": sc_spark, "warm": sc_warm, "jump": lambda c, t: sc_jump(c, t, "jump"),
    "bite": lambda c, t: sc_jump(c, t, "bite"), "no": sc_no, "name": sc_name, "warm2": sc_warm2, "what": sc_what, "red": sc_red,
    "useless": sc_useless, "stomp": sc_stomp, "smoke": sc_smoke, "danger": sc_danger, "sigh": sc_sigh,
    "cold": sc_cold, "glow": sc_glow, "raise": sc_raise, "tasty": sc_tasty, "try": sc_try, "nope": sc_nope, "growl": sc_growl,
    "onebite": sc_onebite, "wolves": sc_wolves, "wolf": sc_wolf, "letme": sc_letme, "hot": sc_hot, "flee": sc_flee,
    "afraid": sc_afraid, "fact": sc_fact, "invent": sc_invent, "mine": sc_mine, "allmine": sc_allmine, "hog": sc_hog,
    "stone": sc_stone, "idea": sc_idea, "useless2": sc_useless2, "black": sc_black, "card": sc_card,
}
SCENE_CUT = {T["cold"][0], T["wolves"][0], T["stone"][0]}


def draw_frame(c, t):
    for name, (a, b, row) in T.items():
        if a <= t < b:
            FN[name](c, t)
            # mờ dần khi chuyển cảnh lớn
            for sc in SCENE_CUT:
                if sc - 0.3 <= t < sc + 0.3:
                    c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 255 * (1 - abs(t - sc) / 0.3)))
            return
    sc_card(c, min(t, DUR - 0.01))
