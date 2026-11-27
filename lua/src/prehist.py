"""Nhân vật và đạo cụ thời tiền sử (phong cách hoạt hình của kênh). Không vẽ kiểu "người vượn"."""
import math
import skia
from lib import paint, text, clamp, lerp, ease_out, back_out, Xf
from toon import OUT, OW, fill_out, rrect_path, oval_path, limb, blink
from toon2 import legs, flipx, _rot

NEA = "#C8946A"      # da người Neanderthal
NEA_D = "#A87650"
SAP = "#8A5A3C"      # da người hiện đại (tổ tiên rời châu Phi)
SAP_D = "#6E452C"
HIDE = "#8A6A44"     # da thuộc
HIDE_D = "#6B5032"
FUR = "#B9A37A"
ORANGE = "#E67E22"   # màu ADN Neanderthal
BLUE = "#3E7FB8"     # màu ADN người hiện đại


def _eyes(c, cx, cy, t, look, mood, seed, brow_ridge):
    bl = blink(t, seed)
    for side in (-1, 1):
        ex = cx + side * 30 + look * 10
        c.save(); c.translate(ex, cy); c.scale(1, bl)
        c.drawOval(skia.Rect.MakeXYWH(-8, -9, 16, 18), paint(OUT)); c.restore()
        k = {"flat": 0, "angry": 8, "sad": -8, "surprise": -4, "smile": -2}.get(mood, 0)
        w = 13 if brow_ridge else 8
        c.drawLine(ex - side * 22, cy - 20 + k, ex + side * 22, cy - 20 - k, paint(OUT, stroke=w))


def _mouth(c, cx, my, t, mood, talk):
    if talk:
        o = 6 + 12 * abs(math.sin(t * 17))
        fill_out(c, oval_path(cx, my, 18, o), "#5A1E16", ow=5)
    elif mood == "smile":
        m = skia.Path(); m.moveTo(cx - 24, my - 4); m.quadTo(cx, my + 16, cx + 24, my - 4); c.drawPath(m, paint(OUT, stroke=7))
    elif mood == "surprise":
        fill_out(c, oval_path(cx, my, 14, 16), "#5A1E16", ow=5)
    elif mood == "sad":
        m = skia.Path(); m.moveTo(cx - 20, my + 6); m.quadTo(cx, my - 8, cx + 20, my + 6); c.drawPath(m, paint(OUT, stroke=7))
    else:
        c.drawLine(cx - 20, my, cx + 20, my + 2, paint(OUT, stroke=7))


def caveperson(c, x, y, s=1.0, t=0.0, kind="nea", walk=None, flip=False, look=0.0, mood="flat", talk=False,
               spear=True, female=False, arm="down", glow=0.0, alpha=1.0, child=False, rot=0.0):
    """kind: 'nea' = Neanderthal (thấp, vạm vỡ, mũi to, gờ mày), 'sap' = người hiện đại thời tiền sử (cao, mảnh)."""
    nea = kind == "nea"
    skin, skin_d = (NEA, NEA_D) if nea else (SAP, SAP_D)
    wide = 1.18 if nea else 0.95
    tall = 0.92 if nea else 1.05
    if child:
        wide, tall = wide * 0.9, tall * 0.62
    bob = 0 if walk is None else -abs(math.sin(walk)) * 12
    with Xf(c, x, y + bob * s, rot, s, alpha):
        flipx(c, 0, flip)
        c.save(); c.scale(wide, tall)
        legs(c, walk, skin, boot=HIDE_D, puttee=False)
        # áo da thuộc có viền lông
        torso = skia.Path(); torso.moveTo(-90, -520); torso.lineTo(90, -520); torso.lineTo(108, -220); torso.lineTo(-108, -220); torso.close()
        fill_out(c, torso, HIDE)
        c.save(); c.clipPath(torso, skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect.MakeXYWH(20, -520, 100, 320), paint(HIDE_D, 110))
        for k in range(7):
            c.drawLine(-100 + k * 30, -225, -90 + k * 30, -250, paint(HIDE_D, stroke=6))
        c.restore(); c.drawPath(torso, paint(OUT, stroke=OW))
        fur = skia.Path(); fur.moveTo(-95, -520)
        for k in range(9):
            fur.quadTo(-95 + k * 23.75 + 12, -548 if k % 2 else -532, -95 + (k + 1) * 23.75, -520)
        fur.close(); fill_out(c, fur, FUR, ow=5)
        c.drawLine(-70, -470, 40, -300, paint(HIDE_D, stroke=8))
        # tay
        sw = 0 if walk is None else math.sin(walk)
        for side in (-1, 1):
            hx, hy = side * 88, -500
            if arm == "wave" and side > 0:
                ex, ey = hx + 60, hy - 90; wx, wy = hx + 70 + 20 * math.sin(t * 9), hy - 200
            elif arm == "hold" and side > 0:
                ex, ey = hx + 40, hy + 90; wx, wy = 40, -360
            elif arm == "up":
                ex, ey = hx + side * 50, hy - 100; wx, wy = hx + side * 70, hy - 210
            else:
                sa = side * (5 + 9 * sw * (1 if side < 0 else -1))
                ex, ey = hx + _rot(side * 18, 115, sa)[0], hy + _rot(side * 18, 115, sa)[1]
                wx, wy = ex + _rot(side * 6, 105, sa)[0], ey + _rot(side * 6, 105, sa)[1]
            limb(c, [(hx, hy), (ex, ey), (wx, wy)], 36, skin)
            c.drawCircle(wx, wy + 6, 20, paint(skin)); c.drawCircle(wx, wy + 6, 20, paint(OUT, stroke=5))
        c.restore()
        # giáo đá
        if spear and not child:
            gx = 150 * wide
            with Xf(c, gx, -40, -6 + (0 if walk is None else 4 * sw), 1):
                c.drawLine(0, 0, 0, -620 * tall, paint(OUT, stroke=16)); c.drawLine(0, 0, 0, -620 * tall, paint("#7A5A3A", stroke=10))
                tip = skia.Path(); tip.moveTo(-18, -620 * tall); tip.lineTo(0, -700 * tall); tip.lineTo(18, -620 * tall); tip.close()
                fill_out(c, tip, "#8E959B", ow=5)
        # đầu
        hy = -650 * tall + (20 if nea else 0)
        hw, hh = (88, 84) if nea else (74, 90)
        fill_out(c, rrect_path(-30, hy + 70, 60, 60, 10), skin_d, ow=5)
        head = oval_path(0, hy, hw, hh); fill_out(c, head, skin)
        c.save(); c.clipPath(head, skia.ClipOp.kIntersect, True); c.drawCircle(70, hy + 30, 85, paint(skin_d, 110)); c.restore()
        c.drawPath(head, paint(OUT, stroke=OW))
        # tóc
        hair = skia.Path()
        col = "#5A3E2A" if nea else "#1F1712"
        if female:
            hair.moveTo(-hw - 6, hy + 70); hair.quadTo(-hw - 20, hy - hh - 20, 0, hy - hh - 12); hair.quadTo(hw + 20, hy - hh - 20, hw + 6, hy + 70)
            hair.lineTo(hw - 14, hy - 10); hair.quadTo(0, hy - hh + 20, -hw + 14, hy - 10); hair.close()
        else:
            hair.moveTo(-hw, hy - 10); hair.quadTo(-hw - 6, hy - hh - 16, 0, hy - hh - 10); hair.quadTo(hw + 6, hy - hh - 16, hw, hy - 10)
            hair.lineTo(hw - 16, hy - 40); hair.quadTo(0, hy - hh + 10, -hw + 16, hy - 40); hair.close()
        fill_out(c, hair, col, ow=5)
        if nea:
            ridge = skia.Path(); ridge.moveTo(-70, hy - 26); ridge.quadTo(0, hy - 50, 70, hy - 26); ridge.quadTo(0, hy - 34, -70, hy - 26); ridge.close()
            fill_out(c, ridge, skin_d, ow=5)
        _eyes(c, 0, hy, t, look, mood, x * 0.002, nea)
        nose_w = 26 if nea else 14
        nose = skia.Path(); nose.moveTo(look * 6, hy + 4); nose.quadTo(look * 6 + nose_w, hy + 38, look * 6, hy + 44); nose.quadTo(look * 6 - nose_w, hy + 40, look * 6 - 6, hy + 30)
        c.drawPath(nose, paint(OUT, stroke=6))
        if nea and not female and not child:
            beard = skia.Path(); beard.moveTo(-hw + 10, hy + 30); beard.quadTo(0, hy + hh + 30, hw - 10, hy + 30); beard.quadTo(0, hy + 60, -hw + 10, hy + 30); beard.close()
            fill_out(c, beard, col, ow=5)
        _mouth(c, look * 6, hy + 62, t, mood, talk)
        if glow > 0:
            g = paint(ORANGE, 170 * glow); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 20))
            c.drawCircle(0, -380 * tall, 40, g)
            c.drawCircle(0, -380 * tall, 14, paint("#FFD27A", 255 * glow))


def helix(c, x, y, length, t, s=1.0, rot=0.0, colors=None, speed=1.5, thick=1.0, alpha=255):
    """Chuỗi xoắn kép ADN nằm dọc. colors(i) → màu thanh ngang thứ i."""
    with Xf(c, x, y, rot, s, alpha / 255):
        n = int(length / 26)
        for i in range(n):
            yy = -length / 2 + i * 26
            ph = t * speed + i * 0.38
            x1, x2 = 90 * math.sin(ph), 90 * math.sin(ph + math.pi)
            depth = math.cos(ph)
            colr = colors(i) if colors else BLUE
            c.drawLine(x1, yy, x2, yy, paint(OUT, stroke=12 * thick)); c.drawLine(x1, yy, x2, yy, paint(colr, stroke=7 * thick))
            for xx, d in ((x1, depth), (x2, -depth)):
                r = (12 + 4 * d) * thick
                c.drawCircle(xx, yy, r, paint("#F6F1E4" if d > 0 else "#C9C3B4")); c.drawCircle(xx, yy, r, paint(OUT, stroke=4))


def bone(c, x, y, s=1.0, rot=0.0):
    with Xf(c, x, y, rot, s):
        p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-160, -26, 320, 52), 26, 26))
        for sx in (-1, 1):
            for sy in (-1, 1):
                p.addCircle(sx * 170, sy * 30, 42)
        p.setFillType(skia.PathFillType.kWinding)
        c.drawPath(p, paint(OUT, stroke=12)); c.drawPath(p, paint("#EDE3C8"))


def puzzle_piece(c, x, y, s, color, rot=0.0):
    with Xf(c, x, y, rot, s):
        p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-50, -50, 100, 100), 10, 10))
        p.addCircle(0, -58, 20); p.addCircle(58, 0, 20)
        p.setFillType(skia.PathFillType.kWinding)
        c.drawPath(p, paint(OUT, stroke=10)); c.drawPath(p, paint(color))


def person_icon(c, x, y, s, color="#C9C3B4", a=255):
    with Xf(c, x, y, 0, s, a / 255):
        c.drawCircle(0, -70, 24, paint(color)); c.drawCircle(0, -70, 24, paint(OUT, stroke=4))
        b = skia.Path(); b.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-34, -42, 68, 80), 26, 26))
        c.drawPath(b, paint(color)); c.drawPath(b, paint(OUT, stroke=4))
