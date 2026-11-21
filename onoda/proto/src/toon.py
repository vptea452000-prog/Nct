"""Bộ vẽ hoạt hình 2D cho Nct official: nét viền dày, tô màu phẳng có đổ bóng, nhân vật đơn giản có biểu cảm.

Nhân vật đều do Nct official tự thiết kế:
- Linh vật "Bút Chì Vàng": khối vàng bo tròn, kính tròn, khăn đỏ — người dẫn chuyện phản ứng với câu chuyện.
- Lính, ông bán sách: nhân vật lịch sử vẽ đơn giản, không mô phỏng người thật theo ảnh.
"""
import math
import skia
from lib import col, paint, text, nfc, font, tw, clamp, lerp, ease_out, ease_in_out, back_out, prog, Xf, W, H

OUT = "#2A1D16"   # màu nét viền
OW = 7            # độ dày nét viền


def fill_out(c, path, fill, a=255, ow=OW):
    c.drawPath(path, paint(fill, a))
    c.drawPath(path, paint(OUT, a, stroke=ow))


def shade(c, path, color, dx, dy, a=70):
    """Đổ bóng phía trong hình: tô màu tối lệch (dx,dy) nhưng chỉ trong path."""
    c.save()
    c.clipPath(path, skia.ClipOp.kIntersect, True)
    p2 = skia.Path(path)
    p2.offset(dx, dy)
    inv = skia.Path(path)
    c.drawPath(path, paint(color, a))
    c.drawPath(p2, paint(color, 0))
    c.restore()


def rrect_path(x, y, w, h, r):
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r))
    return p


def oval_path(cx, cy, rx, ry):
    p = skia.Path()
    p.addOval(skia.Rect.MakeXYWH(cx - rx, cy - ry, 2 * rx, 2 * ry))
    return p


def limb(c, pts, width, fill):
    """Tay/chân: đường gấp khúc dày có viền."""
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p, paint(OUT, stroke=width + 2 * OW))
    c.drawPath(p, paint(fill, stroke=width))


def blink(t, seed=0.0):
    ph = (t + seed) % 3.7
    return 0.12 if ph < 0.12 else 1.0


# ---------------------------------------------------------------- linh vật
MASCOT_Y = "#F4C430"
MASCOT_D = "#D9A514"


def mascot(c, x, y, s=1.0, expr="smile", look=(0, 0), t=0.0, arm="down", rot=0.0, squash=1.0):
    """Gốc toạ độ ở chân. expr: smile / shock / squint / think / worried."""
    with Xf(c, x, y, rot, s):
        c.scale(1 / squash ** 0.5, squash)
        # chân
        for side in (-1, 1):
            limb(c, [(side * 40, -20), (side * 46, 0)], 22, MASCOT_D)
        body = rrect_path(-110, -240, 220, 220, 90)
        c.drawPath(body, paint(MASCOT_Y))
        c.save(); c.clipPath(body, skia.ClipOp.kIntersect, True)
        c.drawCircle(70, -60, 150, paint(MASCOT_D, 120))
        c.drawCircle(-50, -200, 40, paint("white", 70))
        c.restore()
        c.drawPath(body, paint(OUT, stroke=OW))
        # khăn đỏ
        sc = skia.Path(); sc.moveTo(-95, -95); sc.quadTo(0, -60, 95, -95); sc.lineTo(92, -70); sc.quadTo(0, -35, -92, -70); sc.close()
        fill_out(c, sc, "#C0392B")
        tail = skia.Path(); tail.moveTo(40, -75); tail.lineTo(70, -10); tail.lineTo(35, -20); tail.close()
        fill_out(c, tail, "#A93226")
        # tay
        if arm == "down":
            for side in (-1, 1):
                limb(c, [(side * 105, -110), (side * 135, -60)], 20, MASCOT_Y)
        elif arm == "up":
            for side in (-1, 1):
                limb(c, [(side * 105, -130), (side * 160, -200)], 20, MASCOT_Y)
        elif arm == "point":
            limb(c, [(-105, -110), (-135, -60)], 20, MASCOT_Y)
            limb(c, [(105, -130), (175, -150)], 20, MASCOT_Y)
        elif arm == "binoc":
            limb(c, [(-100, -120), (-55, -165)], 20, MASCOT_Y)
            limb(c, [(100, -120), (55, -165)], 20, MASCOT_Y)
        # kính + mắt
        ex, ey = look
        bl = blink(t, x * 0.01)
        for side in (-1, 1):
            cx = side * 45
            if arm == "binoc":
                tube = rrect_path(cx - 32, -205, 64, 70, 16)
                fill_out(c, tube, "#3A3632")
                c.drawCircle(cx, -205, 26, paint("#9FC3D9"))
                c.drawCircle(cx, -205, 26, paint(OUT, stroke=5))
                continue
            c.drawCircle(cx, -165, 38, paint("white"))
            if expr == "squint":
                c.drawLine(cx - 20, -165, cx + 20, -165, paint(OUT, stroke=8))
            elif expr == "shock":
                c.drawCircle(cx + ex * 6, -165 + ey * 6, 9, paint(OUT))
            else:
                c.save(); c.scale(1, bl);
                c.drawCircle(cx + ex * 10, (-162 + ey * 10) / bl, 15, paint(OUT))
                c.drawCircle(cx + ex * 10 + 5, (-168 + ey * 10) / bl, 5, paint("white"))
                c.restore()
            c.drawCircle(cx, -165, 38, paint(OUT, stroke=6))
        if arm != "binoc":
            c.drawLine(-7, -168, 7, -168, paint(OUT, stroke=6))
            # lông mày
            if expr in ("worried", "shock"):
                for side in (-1, 1):
                    c.drawLine(side * 25, -222, side * 62, -214 if expr == "worried" else -228, paint(OUT, stroke=7))
            elif expr == "think":
                c.drawLine(15, -222, 62, -230, paint(OUT, stroke=7))
                c.drawLine(-62, -218, -25, -216, paint(OUT, stroke=7))
        # miệng
        if expr == "smile":
            m = skia.Path(); m.moveTo(-28, -105); m.quadTo(0, -82, 28, -105)
            c.drawPath(m, paint(OUT, stroke=7))
        elif expr == "shock":
            mo = oval_path(0, -102, 22, 26)
            fill_out(c, mo, "#5A1E16", ow=6)
        elif expr in ("squint", "think"):
            c.drawLine(-20, -100, 22, -106, paint(OUT, stroke=7))
        elif expr == "worried":
            m = skia.Path(); m.moveTo(-26, -96); m.quadTo(0, -112, 26, -96)
            c.drawPath(m, paint(OUT, stroke=7))


# ---------------------------------------------------------------- lính Nhật (hoạt hình)
KHAKI = "#9C8A55"
KHAKI_D = "#7C6C3E"
SKIN = "#E7C49C"
SKIN_D = "#C99F74"


def soldier(c, x, y, s=1.0, pose="stand", t=0.0, look=0.0, mouth="flat", rot=0.0, beard=0.0):
    """Gốc ở chân. pose: stand / salute / attention / alert."""
    with Xf(c, x, y, rot, s):
        # chân + xà cạp
        for side in (-1, 1):
            limb(c, [(side * 30, -250), (side * 34, -40)], 46, KHAKI)
            for k in range(5):
                c.drawLine(side * 34 - 24, -150 + k * 22, side * 34 + 24, -138 + k * 22, paint(KHAKI_D, stroke=5))
            boot = rrect_path(side * 34 - 32 + side * 8, -46, 64, 46, 16)
            fill_out(c, boot, "#4A3526")
        # thân áo
        torso = skia.Path()
        torso.moveTo(-85, -520); torso.lineTo(85, -520); torso.lineTo(95, -240); torso.lineTo(-95, -240); torso.close()
        fill_out(c, torso, KHAKI)
        c.save(); c.clipPath(torso, skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect.MakeXYWH(20, -520, 90, 300), paint(KHAKI_D, 110))
        c.restore()
        c.drawPath(torso, paint(OUT, stroke=OW))
        belt = rrect_path(-96, -300, 192, 30, 6)
        fill_out(c, belt, "#5A4030")
        for k in range(3):
            c.drawCircle(0, -480 + k * 60, 7, paint("#4A3526"))
        # súng (dựng bên phải) — sau tay
        if pose in ("stand", "alert", "salute"):
            gun = skia.Path()
            gun.moveTo(130, -40); gun.lineTo(150, -40); gun.lineTo(160, -620); gun.lineTo(146, -620); gun.close()
            fill_out(c, gun, "#6B4A30", ow=5)
            c.drawRect(skia.Rect.MakeXYWH(146, -700, 8, 90), paint("#3A3632"))
        # tay
        if pose == "salute":
            limb(c, [(-85, -500), (-110, -380), (-95, -270)], 34, KHAKI)
            limb(c, [(85, -500), (150, -560), (60, -660)], 34, KHAKI)
            hand = oval_path(55, -665, 22, 16); fill_out(c, hand, SKIN, ow=5)
        elif pose == "attention":
            for side in (-1, 1):
                limb(c, [(side * 85, -500), (side * 100, -380), (side * 95, -270)], 34, KHAKI)
                c.drawCircle(side * 95, -262, 18, paint(SKIN)); c.drawCircle(side * 95, -262, 18, paint(OUT, stroke=5))
        else:
            limb(c, [(-85, -500), (-115, -380), (-100, -270)], 34, KHAKI)
            c.drawCircle(-100, -262, 18, paint(SKIN)); c.drawCircle(-100, -262, 18, paint(OUT, stroke=5))
            limb(c, [(85, -500), (125, -400), (145, -330)], 34, KHAKI)
            c.drawCircle(147, -322, 18, paint(SKIN)); c.drawCircle(147, -322, 18, paint(OUT, stroke=5))
        # cổ + đầu
        neck = rrect_path(-26, -560, 52, 50, 10); fill_out(c, neck, SKIN_D, ow=5)
        head = oval_path(0, -650, 78, 92)
        fill_out(c, head, SKIN)
        c.save(); c.clipPath(head, skia.ClipOp.kIntersect, True)
        c.drawCircle(70, -620, 80, paint(SKIN_D, 120))
        if beard > 0:
            c.drawRect(skia.Rect.MakeXYWH(-80, -620, 160, 70), paint("#4A3A2E", 120 * beard))
        c.restore()
        c.drawPath(head, paint(OUT, stroke=OW))
        # mũ lính có rèm che gáy
        flap = skia.Path(); flap.moveTo(-82, -700); flap.lineTo(-96, -585); flap.lineTo(-60, -600); flap.lineTo(-50, -700); flap.close()
        fill_out(c, flap, KHAKI_D, ow=5)
        flap2 = skia.Path(); flap2.moveTo(82, -700); flap2.lineTo(96, -585); flap2.lineTo(60, -600); flap2.lineTo(50, -700); flap2.close()
        fill_out(c, flap2, KHAKI_D, ow=5)
        cap = skia.Path(); cap.moveTo(-84, -700); cap.quadTo(0, -800, 84, -700); cap.close()
        fill_out(c, cap, KHAKI)
        visor = skia.Path(); visor.moveTo(-90, -700); visor.lineTo(90, -700); visor.lineTo(60, -680); visor.lineTo(-60, -680); visor.close()
        fill_out(c, visor, "#5A4A2A", ow=5)
        star = skia.Path()
        for k in range(10):
            r = 14 if k % 2 == 0 else 6
            a = -math.pi / 2 + k * math.pi / 5
            (star.moveTo if k == 0 else star.lineTo)(r * math.cos(a), -738 + r * math.sin(a))
        star.close(); fill_out(c, star, "#F4C430", ow=3)
        # mặt: lông mày quyết tâm, mắt nhỏ
        bl = blink(t, 1.3)
        for side in (-1, 1):
            ex = side * 30 + look * 8
            c.save(); c.translate(ex, -650); c.scale(1, bl)
            c.drawOval(skia.Rect.MakeXYWH(-8, -9, 16, 18), paint(OUT))
            c.restore()
            c.drawLine(side * 14 + look * 4, -672, side * 50 + look * 4, -682 + 6, paint(OUT, stroke=9))
        c.drawLine(4, -640, 0, -615, paint(SKIN_D, stroke=6))
        if mouth == "flat":
            c.drawLine(-22, -595, 22, -597, paint(OUT, stroke=7))
        elif mouth == "shout":
            mo = oval_path(0, -594, 20, 16); fill_out(c, mo, "#5A1E16", ow=5)
        elif mouth == "frown":
            m = skia.Path(); m.moveTo(-22, -588); m.quadTo(0, -604, 22, -588)
            c.drawPath(m, paint(OUT, stroke=7))


# ---------------------------------------------------------------- ông bán sách (hoạt hình)
def bookseller(c, x, y, s=1.0, t=0.0, pose="read", look=0.0):
    with Xf(c, x, y, 0, s):
        torso = skia.Path(); torso.moveTo(-95, -480); torso.lineTo(95, -480); torso.lineTo(110, -200); torso.lineTo(-110, -200); torso.close()
        fill_out(c, torso, "#7B5A44")
        c.save(); c.clipPath(torso, skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect.MakeXYWH(-30, -480, 60, 280), paint("#E9E2CF"))
        c.drawRect(skia.Rect.MakeXYWH(30, -480, 90, 280), paint("#5E4433", 120))
        c.restore(); c.drawPath(torso, paint(OUT, stroke=OW))
        neck = rrect_path(-24, -520, 48, 46, 10); fill_out(c, neck, SKIN_D, ow=5)
        head = oval_path(0, -600, 76, 86); fill_out(c, head, SKIN)
        c.save(); c.clipPath(head, skia.ClipOp.kIntersect, True); c.drawCircle(70, -570, 80, paint(SKIN_D, 110)); c.restore()
        c.drawPath(head, paint(OUT, stroke=OW))
        hair = skia.Path(); hair.moveTo(-76, -610); hair.quadTo(-70, -700, 0, -690); hair.quadTo(70, -700, 76, -610); hair.lineTo(60, -650); hair.quadTo(0, -665, -60, -650); hair.close()
        fill_out(c, hair, "#B9B4AA", ow=5)
        for side in (-1, 1):
            c.drawCircle(side * 30 + look * 6, -600, 24, paint("white", 140))
            c.drawCircle(side * 30 + look * 6, -600, 24, paint(OUT, stroke=5))
            c.drawCircle(side * 30 + look * 10, -598, 6, paint(OUT))
        c.drawLine(-6, -602, 6, -602, paint(OUT, stroke=5))
        mus = skia.Path(); mus.moveTo(-30, -555); mus.quadTo(0, -575, 30, -555); mus.quadTo(0, -548, -30, -555); mus.close()
        fill_out(c, mus, "#CFCAC0", ow=4)
        if pose == "read":
            paper = skia.Path(); paper.moveTo(-90, -420); paper.lineTo(90, -430); paper.lineTo(100, -290); paper.lineTo(-80, -280); paper.close()
            fill_out(c, paper, "#F6EFE0", ow=5)
            for k in range(4):
                c.drawLine(-60, -400 + k * 28, 70, -405 + k * 28, paint("#8E846F", stroke=4))
            for side in (-1, 1):
                limb(c, [(side * 95, -460), (side * 120, -360), (side * 95, -330)], 32, "#7B5A44")
        else:
            for side in (-1, 1):
                limb(c, [(side * 95, -460), (side * 110, -330), (side * 100, -230)], 32, "#7B5A44")
        for side in (-1, 1):
            limb(c, [(side * 40, -210), (side * 44, -30)], 52, "#4A4640")
            fill_out(c, rrect_path(side * 44 - 34, -40, 68, 40, 14), "#2E2A25")


# ---------------------------------------------------------------- chữ lớn kiểu tiêu đề
def big_title(c, top, bottom, y, p, top_color="white", bot_color="#F4C430", size=104, bsize=52):
    """Dải tối mờ ngang khung với dòng chữ lớn viền dày (dòng trên) và dòng phụ vàng (dòng dưới)."""
    if p <= 0:
        return
    a = clamp(p * 3)
    band_h = size * 1.15 + (bsize * 1.4 if bottom else 0) + 40
    c.drawRect(skia.Rect.MakeXYWH(0, y - size, W, band_h), paint("#000000", 120 * a))
    sc = back_out(clamp(p)) if p < 1 else 1.0
    with Xf(c, W / 2, y, 0, max(0.01, sc), a):
        text(c, top, 0, 0, "xbold", size, top_color, align="center", stroke=9, stroke_color="#1A120D")
        if bottom:
            text(c, bottom, 0, bsize * 1.45, "xbold", bsize, bot_color, align="center", stroke=6, stroke_color="#1A120D")
