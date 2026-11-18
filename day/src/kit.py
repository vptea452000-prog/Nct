"""Bộ công cụ dùng chung cho chuỗi Bộp và Gầm: bóng thoại, tượng thanh, bối cảnh, lửa, gậy, nhân vật."""
import math
import skia
from lib import *  # noqa
from toon import OUT, fill_out, rrect_path, oval_path, limb  # noqa
from toon2 import kinetic
from prehist import caveperson, ORANGE
from sets import grad_rect, vignette, blurred

# ---------------------------------------------------------------- tiện ích


def pop(t, t0, d=0.3):
    return prog(t, t0, t0 + d)


def phase(t, t0, speed=7.0):
    return (t - t0) * speed




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
    big = skia.Rect.MakeXYWH(-800, -800, W + 1600, H + 1600)
    if morning > 0:
        grad_rect(c, big, "#9FC9E6", "#F6E7C0")
    else:
        top = "#F08A4B" if night < 0.5 else "#15203A"
        bot = "#F6C67A" if night < 0.5 else "#2E3A5A"
        grad_rect(c, big, top, bot)


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


