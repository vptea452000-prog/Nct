"""Nhân vật hoạt hình có chuyển động (đi, nói, quay đầu, già đi) cho phong cách hoạt hình thuần.
Mọi nhân vật đều vẽ đơn giản, không mô phỏng khuôn mặt người thật."""
import math
import skia
from lib import paint, text, clamp, lerp, ease_out, ease_in_out, back_out, Xf
from toon import OUT, OW, fill_out, rrect_path, oval_path, limb, blink, KHAKI, KHAKI_D, SKIN, SKIN_D, mascot  # noqa


def _rot(px, py, ang):
    a = math.radians(ang)
    return px * math.cos(a) - py * math.sin(a), px * math.sin(a) + py * math.cos(a)


def flipx(c, x, flip):
    if flip:
        c.translate(x, 0); c.scale(-1, 1); c.translate(-x, 0)


def legs(c, walk, color, boot="#4A3526", puttee=True):
    """walk: pha bước (radian) hoặc None."""
    for side in (-1, 1):
        lift = 0.0 if walk is None else max(0.0, math.sin(walk + (0 if side < 0 else math.pi)))
        hx, hy = side * 30, -250
        foot = (hx + side * 4, hy + 210 - 34 * lift)
        knee = (hx + side * (6 + 26 * lift), hy + 105 - 22 * lift)
        limb(c, [(hx, hy), knee, foot], 44, color)
        if puttee:
            for k in range(4):
                t = 0.35 + k * 0.15
                px = lerp(knee[0], foot[0], t); py = lerp(knee[1], foot[1], t)
                c.drawLine(px - 22, py - 6, px + 22, py + 6, paint(KHAKI_D, stroke=5))
        fill_out(c, rrect_path(foot[0] - 30 + side * 6, foot[1] - 14, 66, 40, 16), boot)


def face(c, cx, cy, t, look=0.0, mood="flat", talk=False, age=0.0, variant=0, glasses=False, brows=True):
    bl = blink(t, cx * 0.003 + variant)
    eye_y = cy
    for side in (-1, 1):
        ex = cx + side * 30 + look * 10
        c.save(); c.translate(ex, eye_y); c.scale(1, bl)
        c.drawOval(skia.Rect.MakeXYWH(-8, -9, 16, 18), paint(OUT)); c.restore()
        if brows:
            k = {"flat": 0, "angry": 9, "sad": -8, "surprise": -2, "smile": -2}.get(mood, 0)
            dy = -8 if mood == "surprise" else 0
            c.drawLine(ex - side * 20 + look * 2, eye_y - 22 + k + dy, ex + side * 20 + look * 2, eye_y - 22 - k + dy, paint(OUT, stroke=9))
        if glasses:
            c.drawCircle(ex, eye_y, 24, paint(OUT, stroke=5))
    if glasses:
        c.drawLine(cx - 6, eye_y, cx + 6, eye_y, paint(OUT, stroke=5))
    c.drawLine(cx + 4 + look * 6, cy + 10, cx + look * 6, cy + 34, paint(SKIN_D, stroke=6))
    my = cy + 55
    if talk:
        o = 6 + 12 * abs(math.sin(t * 17))
        fill_out(c, oval_path(cx + look * 6, my, 18, o), "#5A1E16", ow=5)
    elif mood == "surprise":
        fill_out(c, oval_path(cx + look * 6, my, 14, 16), "#5A1E16", ow=5)
    elif mood == "sad":
        m = skia.Path(); m.moveTo(cx - 20, my + 6); m.quadTo(cx, my - 8, cx + 20, my + 6); c.drawPath(m, paint(OUT, stroke=7))
    elif mood == "smile":
        m = skia.Path(); m.moveTo(cx - 22, my - 4); m.quadTo(cx, my + 14, cx + 22, my - 4); c.drawPath(m, paint(OUT, stroke=7))
    else:
        c.drawLine(cx - 20 + look * 6, my, cx + 20 + look * 6, my + 2, paint(OUT, stroke=7))
    if age > 0:
        a = int(200 * age)
        for side in (-1, 1):
            c.drawLine(cx + side * 52, cy + 30, cx + side * 40, cy + 60, paint(SKIN_D, a, stroke=4))
        c.drawLine(cx - 24, cy - 48, cx + 24, cy - 48, paint(SKIN_D, a, stroke=4))
        # râu lún phún
        for k in range(18):
            px = cx - 34 + (k * 37 % 68); py = my + 6 + (k * 23 % 30)
            c.drawCircle(px, py, 2.4, paint("#3A2E26", int(170 * age)))


def soldier2(c, x, y, s=1.0, t=0.0, pose="stand", walk=None, flip=False, look=0.0, mood="flat", talk=False, age=0.0,
             variant=0, rifle=True, rot=0.0, worn=0.0):
    """Lính Nhật hoạt hình có chuyển động. variant: 0 Onoda, 1–3 đồng đội (khác dáng mặt). worn: áo sờn, vá."""
    bob = 0 if walk is None else -abs(math.sin(walk)) * 14
    breathe = 1 + 0.012 * math.sin(t * 2.2)
    with Xf(c, x, y + bob * s, rot, s):
        flipx(c, 0, flip)
        legs(c, walk, KHAKI)
        c.save(); c.scale(1, breathe)
        torso = skia.Path(); torso.moveTo(-85, -520); torso.lineTo(85, -520); torso.lineTo(95, -240); torso.lineTo(-95, -240); torso.close()
        fill_out(c, torso, KHAKI)
        c.save(); c.clipPath(torso, skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect.MakeXYWH(20, -520, 90, 300), paint(KHAKI_D, 110))
        if worn > 0:
            fill_out(c, rrect_path(-60, -430, 50, 60, 6), "#8A7A48", a=int(255 * worn), ow=4)
            fill_out(c, rrect_path(20, -330, 46, 40, 6), "#6E6038", a=int(255 * worn), ow=4)
        c.restore(); c.drawPath(torso, paint(OUT, stroke=OW))
        fill_out(c, rrect_path(-96, -300, 192, 30, 6), "#5A4030")
        for k in range(3):
            c.drawCircle(0, -480 + k * 60, 7, paint("#4A3526"))
        sw = 0 if walk is None else 30 * math.sin(walk)
        if rifle and pose in ("stand", "alert", "aim") and pose != "aim":
            gx = 135
            gun = skia.Path(); gun.moveTo(gx, -40); gun.lineTo(gx + 20, -40); gun.lineTo(gx + 30, -620); gun.lineTo(gx + 16, -620); gun.close()
            if walk is not None:
                c.save(); c.rotate(-8 + sw * 0.15, gx, -330)
            fill_out(c, gun, "#6B4A30", ow=5)
            c.drawRect(skia.Rect.MakeXYWH(gx + 16, -700, 8, 90), paint("#3A3632"))
            if walk is not None:
                c.restore()
        if pose == "salute":
            limb(c, [(-85, -500), (-110, -380), (-95, -270)], 34, KHAKI)
            limb(c, [(85, -500), (150, -560), (60, -660)], 34, KHAKI)
            fill_out(c, oval_path(55, -665, 22, 16), SKIN, ow=5)
        elif pose == "attention":
            for side in (-1, 1):
                limb(c, [(side * 85, -500), (side * 100, -380), (side * 95, -270)], 34, KHAKI)
                c.drawCircle(side * 95, -262, 18, paint(SKIN)); c.drawCircle(side * 95, -262, 18, paint(OUT, stroke=5))
        elif pose == "aim":
            gun = skia.Path(); gun.moveTo(-40, -470); gun.lineTo(330, -500); gun.lineTo(330, -484); gun.lineTo(-40, -440); gun.close()
            fill_out(c, gun, "#6B4A30", ow=5)
            limb(c, [(-85, -500), (-20, -430), (60, -470)], 32, KHAKI)
            limb(c, [(85, -500), (170, -470), (220, -490)], 32, KHAKI)
        elif pose == "cross":
            limb(c, [(-85, -500), (-100, -400), (60, -400)], 34, KHAKI)
            limb(c, [(85, -500), (100, -380), (-50, -380)], 34, KHAKI)
        elif pose == "read":
            limb(c, [(-85, -500), (-90, -400), (-30, -380)], 32, KHAKI)
            limb(c, [(85, -500), (90, -400), (30, -380)], 32, KHAKI)
            fill_out(c, rrect_path(-60, -470, 120, 150, 4), "#F1EAD7", ow=4)
        elif pose == "swat":
            limb(c, [(-85, -500), (-115, -380), (-100, -270)], 34, KHAKI)
            a = math.sin(t * 14) * 30
            ex, ey = 85 + _rot(0, -120, 60 + a)[0], -500 + _rot(0, -120, 60 + a)[1]
            limb(c, [(85, -500), (ex, ey), (ex + 50, ey - 80)], 32, KHAKI)
        else:
            for side in (-1, 1):
                sa = side * (4 + 8 * (math.sin(walk + (0 if side < 0 else math.pi)) if walk is not None else 0))
                hx, hy = side * 85, -500
                ex, ey = hx + _rot(side * 20, 120, sa)[0], hy + _rot(side * 20, 120, sa)[1]
                wx, wy = ex + _rot(side * 6, 110, sa)[0], ey + _rot(side * 6, 110, sa)[1]
                limb(c, [(hx, hy), (ex, ey), (wx, wy)], 34, KHAKI)
                c.drawCircle(wx, wy + 8, 18, paint(SKIN)); c.drawCircle(wx, wy + 8, 18, paint(OUT, stroke=5))
        c.restore()
        # đầu (không co giãn theo nhịp thở)
        hy = -650 * breathe
        fill_out(c, rrect_path(-26, hy + 90, 52, 50, 10), SKIN_D, ow=5)
        hw, hh = [(78, 92), (84, 86), (72, 96), (80, 90)][variant % 4]
        head = oval_path(0, hy, hw, hh); fill_out(c, head, SKIN)
        c.save(); c.clipPath(head, skia.ClipOp.kIntersect, True); c.drawCircle(70, hy + 30, 80, paint(SKIN_D, 120)); c.restore()
        c.drawPath(head, paint(OUT, stroke=OW))
        for side in (-1, 1):
            flap = skia.Path(); flap.moveTo(side * 82, hy - 50); flap.lineTo(side * 98, hy + 66); flap.lineTo(side * 60, hy + 50); flap.lineTo(side * 50, hy - 50); flap.close()
            fill_out(c, flap, KHAKI_D, ow=5)
        cap = skia.Path(); cap.moveTo(-84, hy - 50); cap.quadTo(0, hy - 150, 84, hy - 50); cap.close(); fill_out(c, cap, KHAKI)
        visor = skia.Path(); visor.moveTo(-90, hy - 50); visor.lineTo(90 + look * 20, hy - 50); visor.lineTo(60 + look * 20, hy - 30); visor.lineTo(-60, hy - 30); visor.close()
        fill_out(c, visor, "#5A4A2A", ow=5)
        star = skia.Path()
        for k in range(10):
            r = 14 if k % 2 == 0 else 6
            a = -math.pi / 2 + k * math.pi / 5
            (star.moveTo if k == 0 else star.lineTo)(r * math.cos(a), hy - 88 + r * math.sin(a))
        star.close(); fill_out(c, star, "#F4C430", ow=3)
        if variant == 1:
            c.drawLine(-28, hy + 46, 28, hy + 46, paint("#3A2E26", stroke=8))
        face(c, 0, hy, t, look=look, mood=mood, talk=talk, age=age, variant=variant)


def civilian(c, x, y, s=1.0, t=0.0, walk=None, flip=False, look=0.0, mood="flat", talk=False, kind="suzuki", pose="arms",
             hands_up=0.0, prop=None):
    """kind: suzuki (áo phông, ba lô), taniguchi (áo khoác nâu, tóc bạc, kính), president (barong trắng), official (vest xám)."""
    pal = {"suzuki": ("#E9E2CF", "#3E5A8A", "#2A2420"), "taniguchi": ("#7B5A44", "#4A4640", "#B9B4AA"),
           "president": ("#F6F1E4", "#2E2A25", "#1F1A16"), "official": ("#6E6A64", "#3A3632", "#2A2420")}[kind]
    top, pants, hair = pal
    bob = 0 if walk is None else -abs(math.sin(walk)) * 12
    with Xf(c, x, y + bob * s, 0, s):
        flipx(c, 0, flip)
        legs(c, walk, pants, boot="#2E2A25", puttee=False)
        if kind == "suzuki":
            fill_out(c, rrect_path(-125, -500, 72, 220, 24), "#C0392B")
        torso = skia.Path(); torso.moveTo(-85, -510); torso.lineTo(85, -510); torso.lineTo(92, -240); torso.lineTo(-92, -240); torso.close()
        fill_out(c, torso, top)
        if kind == "president":
            for k in range(4):
                c.drawLine(-40 + k * 26, -490, -40 + k * 26, -260, paint("#D8CDB4", stroke=4))
        if kind == "taniguchi":
            c.save(); c.clipPath(torso, skia.ClipOp.kIntersect, True)
            c.drawRect(skia.Rect.MakeXYWH(-28, -510, 56, 270), paint("#E9E2CF")); c.restore(); c.drawPath(torso, paint(OUT, stroke=OW))
        sw = 0 if walk is None else 30 * math.sin(walk)
        for side in (-1, 1):
            hx, hy = side * 85, -490
            if hands_up > 0:
                ang = lerp(0, 160, hands_up) * side * -1
                ex, ey = hx + _rot(side * 10, 120, ang)[0], hy + _rot(side * 10, 120, ang)[1]
                wx, wy = ex + _rot(0, 110, ang)[0], ey + _rot(0, 110, ang)[1]
            elif pose == "hold" and side > 0 or (pose == "read"):
                ex, ey = hx + side * 30, hy + 100; wx, wy = side * 40, -380
            elif pose == "give" and side > 0:
                ex, ey = hx + 70, hy + 40; wx, wy = hx + 160, hy + 20
            else:
                sa = side * (4 + 8 * (math.sin(walk + (0 if side < 0 else math.pi)) if walk is not None else 0))
                ex, ey = hx + _rot(side * 20, 120, sa)[0], hy + _rot(side * 20, 120, sa)[1]
                wx, wy = ex + _rot(side * 6, 110, sa)[0], ey + _rot(side * 6, 110, sa)[1]
            limb(c, [(hx, hy), (ex, ey), (wx, wy)], 32, top)
            c.drawCircle(wx, wy + 6, 18, paint(SKIN)); c.drawCircle(wx, wy + 6, 18, paint(OUT, stroke=5))
        if pose == "read" or prop == "paper":
            fill_out(c, rrect_path(-75, -440, 150, 120, 4), "#F6EFE0", ow=4)
            for k in range(3):
                c.drawLine(-50, -410 + k * 28, 50, -410 + k * 28, paint("#8E846F", stroke=4))
        if prop == "camera":
            fill_out(c, rrect_path(-60, -470, 120, 80, 10), "#2E2A25", ow=5)
            c.drawCircle(0, -430, 24, paint("#8E959B")); c.drawCircle(0, -430, 24, paint(OUT, stroke=4))
        fill_out(c, rrect_path(-24, -550, 48, 46, 10), SKIN_D, ow=5)
        skin = "#D9AE84" if kind == "president" else SKIN
        hy = -630
        head = oval_path(0, hy, 74, 86); fill_out(c, head, skin)
        hr = skia.Path()
        if kind == "taniguchi":
            hr.moveTo(-76, hy + 10); hr.quadTo(-70, hy - 90, 0, hy - 90); hr.quadTo(70, hy - 90, 76, hy + 10); hr.lineTo(60, hy - 40); hr.quadTo(0, hy - 60, -60, hy - 40); hr.close()
        elif kind == "suzuki":
            hr.moveTo(-82, hy + 30); hr.quadTo(-88, hy - 92, 0, hy - 90); hr.quadTo(88, hy - 92, 82, hy + 30); hr.lineTo(66, hy - 20); hr.quadTo(0, hy - 60, -66, hy - 20); hr.close()
        else:
            hr.moveTo(-76, hy - 10); hr.quadTo(-70, hy - 100, 0, hy - 98); hr.quadTo(70, hy - 100, 76, hy - 10); hr.lineTo(62, hy - 50); hr.quadTo(0, hy - 70, -62, hy - 50); hr.close()
        fill_out(c, hr, hair, ow=5)
        face(c, 0, hy, t, look=look, mood=mood, talk=talk, glasses=(kind == "taniguchi"), variant=7)
        if kind == "taniguchi":
            mus = skia.Path(); mus.moveTo(-30, hy + 44); mus.quadTo(0, hy + 26, 30, hy + 44); mus.quadTo(0, hy + 52, -30, hy + 44); mus.close()
            fill_out(c, mus, "#CFCAC0", ow=4)


def kinetic(c, s, x, y, t, t0, size=120, color="white", stroke_color="#1A120D", per=0.05, rot=0.0, name="xbold"):
    """Chữ bật từng ký tự (kinetic typography)."""
    from lib import font, nfc, tw
    s = nfc(s)
    total = tw(s, name, size)
    cx = x - total / 2
    f = font(name, size)
    for i, ch in enumerate(s):
        w = f.measureText(ch)
        p = clamp((t - t0 - i * per) / 0.25)
        if p > 0:
            sc = back_out(p) if p < 1 else 1
            with Xf(c, cx + w / 2, y, rot, max(0.01, sc), clamp(p * 3)):
                text(c, ch, -w / 2, size * 0.35, name, size, color, stroke=size * 0.08, stroke_color=stroke_color)
        cx += w
