"""Nếu bạn là hành khách hạng ba trên tàu Titanic — dựng người que 16:9 theo voice (404 s).
Mốc câu: audio/voice_align.json (linh_nhat/src/align.py). Nhịp máy vừa phải, chỉ nhanh ở cao trào.
"""
import math, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT.parent / "tools")); sys.path.insert(0, str(ROOT.parent / "cung" / "src"))
sys.path.insert(0, str(ROOT.parent / "linh_nhat" / "src"))
import skia  # noqa
from lib import text, tw  # noqa
import stick2  # noqa
from stick2 import Stick, draw_stick, P, fo, oval, clamp, lerp, ease_out, ease_in_out, back_out, INK, LOOKS  # noqa
from test_open2 import Cam, grad, noise1, wave_band, W, H, FPS  # noqa

ALIGN = json.load(open(ROOT / "audio" / "voice_align.json"))
DUR = 404.25
GROUND = 860

LOOKS["ir_you"] = dict(LOOKS["you"], headband=None, hair_col="#5A3A22", civ=("#6A5A48", "#52463A"), cap="flat", cap_col="#5A4E40")
LOOKS["nora"] = dict(LOOKS["mother"], hair_col="#8A4A26", civ=("#4E7A5A", "#3E6248"), apron="#EDE6D4", head=66, body=0.86)
LOOKS["patrick"] = dict(LOOKS["kenji"], hair="short", hair_col="#C0602A", civ=("#7A6A5A", "#5E5246"), cheeks=True, body=1.22, head=80)
LOOKS["ir_mom"] = dict(LOOKS["mother_old"], hair_col="#8A8A8A", civ=("#5A4A5A", "#463A46"), apron="#D8D0C0")
LOOKS["sailor"] = dict(LOOKS["you"], civ=("#24304A", "#1A2238"), headband=None, cap="flat", cap_col="#1A2238")
LOOKS["doctor"] = dict(LOOKS["chief"], civ=("#E8E8E2", "#C8C8C2"), mustache=True)
LOOKS["band"] = dict(LOOKS["you"], civ=("#22283A", "#181C2A"), headband=None)
for i, (a, b, hc) in enumerate([("#7A5A3A", "#5E4630", "#3A2A1A"), ("#5A6A7A", "#46525E", "#2A2A2A"), ("#8A4A3A", "#6E3A2E", "#4A3020"),
                               ("#6A7A4A", "#52603A", "#2A2A2A"), ("#5A4A6A", "#463A52", "#6A4A2A")]):
    LOOKS[f"pax{i}"] = dict(LOOKS["you"], civ=(a, b), hair_col=hc, headband=None)
    LOOKS[f"paxw{i}"] = dict(LOOKS["mother"], civ=(a, b), hair_col=hc)


def ease_shot(t, a, b):
    return ease_in_out(clamp((t - a) / max(1e-3, b - a)))


def lerp_col(a, b, q):
    a = a.lstrip("#"); b = b.lstrip("#")
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]; cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{int(lerp(x, y, clamp(q))):02X}" for x, y in zip(ca, cb))


def ST(c, who, x, y, s, t, **kw):
    draw_stick(c, Stick(who, x, y, s, t, **kw))


def YOU(c, x, y, s, t, **kw):
    ST(c, "ir_you", x, y, s, t, **kw)


def NORA(c, x, y, s, t, **kw):
    ST(c, "nora", x, y, s, t, **kw)


def PAT(c, x, y, s, t, **kw):
    ST(c, "patrick", x, y, s, t, **kw)


def head_xy(x, y, s, who="ir_you", crouch=0.0):
    L = LOOKS[who]
    tor = 150 * min(1.15, L["body"] ** 0.5)
    return x + 4 * s, y - (216 - crouch * 70 + tor + L["head"] - 4) * s


def rect(x, y, w, h):
    return skia.Path().addRect(skia.Rect.MakeXYWH(x, y, w, h)) or skia.Path()


def rrect(x, y, w, h, r):
    return skia.Path().addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)) or skia.Path()


def label(c, s, x, y, size=64, col="#F4C430", a=255):
    text(c, s, x, y, "xbold", size, col, a=a, align="center", stroke=max(5, size // 10), stroke_color="#111111")


def blur(col, a, r):
    p = P(col, a); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r)); return p


# ---------------------------------------------------------------- đạo cụ & bối cảnh
def titanic(c, x, y, s, t, lights=1.0, tilt=0.0, broken=0.0, stern_up=0.0, smoke=True, night=False):
    """Tàu Titanic nhìn ngang (mũi bên phải). Gốc = giữa thân, mặt nước."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rotate(tilt)
    hull_col = "#1A1A1E"
    # thân tàu
    hull = skia.Path(); hull.moveTo(-1500, -260); hull.lineTo(1420, -260); hull.lineTo(1560, -300); hull.lineTo(1500, 40)
    hull.quadTo(1300, 120, 900, 120); hull.lineTo(-1300, 120); hull.quadTo(-1500, 80, -1520, -60); hull.close()
    if broken > 0:
        c.save(); c.clipRect(skia.Rect.MakeXYWH(-80, -2000, 4000, 4000))
    fo(c, hull, hull_col, ow=8)
    c.drawRect(skia.Rect.MakeXYWH(-1500, 60, 2900, 60), P("#7A2A22"))
    c.drawRect(skia.Rect.MakeXYWH(-1480, -260, 2900, 40), P("#F2EEE4"))
    fo(c, rect(-1100, -420, 2100, 160), "#F2EEE4", ow=6)
    fo(c, rect(-900, -520, 1500, 100), "#F2EEE4", ow=6)
    for k in range(30):
        wx = -1400 + k * 95
        on = lights * (0.75 + 0.25 * math.sin(k * 3.1))
        c.drawCircle(wx, -150, 12, P("#F6D88A" if night else "#3A3A3A", 255 * (on if night else 1)))
        if night and lights > 0:
            c.drawCircle(wx, -150, 26, blur("#F6D88A", 80 * on, 10))
    for k in range(22):
        wx = -1060 + k * 95
        c.drawRect(skia.Rect.MakeXYWH(wx, -390, 50, 40), P("#F6D88A" if night and lights > 0 else "#3A4A5A", 255 * (lights if night else 1)))
    for i in range(4):
        fx = -700 + i * 400
        fun = skia.Path(); fun.moveTo(fx - 70, -520); fun.lineTo(fx - 50, -880); fun.lineTo(fx + 70, -880); fun.lineTo(fx + 90, -520); fun.close()
        fo(c, fun, "#D89A3A", ow=7)
        c.drawRect(skia.Rect.MakeXYWH(fx - 52, -880, 122, 70), P("#1A1A1A"))
        if smoke and i < 3:
            for k in range(5):
                q = (t * 0.2 + k / 5 + i * 0.13) % 1
                c.drawCircle(fx - q * 400, -900 - q * 260, 50 + q * 90, blur("#CFCAC0", 170 * (1 - q), 14))
    c.drawLine(-1450, -560, -1450, -1100, P(INK, stroke=10)); c.drawLine(1300, -560, 1300, -1100, P(INK, stroke=10))
    c.drawLine(-1450, -1080, 1300, -1080, P(INK, 160, stroke=3))
    if broken > 0:
        c.restore()
        # nửa sau (đuôi) tách ra, dựng đứng
        c.save(); c.translate(-80, 0); c.rotate(-80 * stern_up); c.translate(80, 0)
        c.clipRect(skia.Rect.MakeXYWH(-4000, -2000, 3920, 4000))
        fo(c, hull, hull_col, ow=8)
        c.drawRect(skia.Rect.MakeXYWH(-1500, 60, 2900, 60), P("#7A2A22"))
        c.drawRect(skia.Rect.MakeXYWH(-1480, -260, 2900, 40), P("#F2EEE4"))
        fo(c, rect(-1100, -420, 2100, 160), "#F2EEE4", ow=6)
        for i in range(2):
            fx = -700 + i * 400
            fun = skia.Path(); fun.moveTo(fx - 70, -520); fun.lineTo(fx - 50, -880); fun.lineTo(fx + 70, -880); fun.lineTo(fx + 90, -520); fun.close()
            fo(c, fun, "#D89A3A", ow=7)
        c.restore()
    c.restore()


def sea_bg(c, K, t, night=0.0, dawn=0.0, calm=False):
    K.layer(c, 0.0)
    top = lerp_col(lerp_col("#8FB8D0", "#0A1022", night), "#E8A07A", dawn)
    bot = lerp_col(lerp_col("#DCE8EC", "#18223A", night), "#F8D8B0", dawn)
    grad(c, skia.Rect.MakeXYWH(-4000, -4000, W + 8000, H + 8000), top, bot)
    K.end(c)
    if night > 0.5 and dawn < 0.5:
        K.layer(c, 0.05)
        for k in range(90):
            x = (k * 173) % (W + 600) - 300; y = (k * 97) % 620 - 100
            c.drawCircle(x, y, 1.5 + (k % 3), P("#FFFFFF", 200 * (0.6 + 0.4 * math.sin(t * 2 + k)) * night))
        K.end(c)
    K.layer(c, 0.5)
    amp = 2 if calm else 6
    wave_band(c, 620, t * (0.3 if calm else 1), lerp_col(lerp_col("#5A8098", "#141C30", night), "#C08060", dawn), amp=amp, x0=-4000, x1=W + 4000)
    K.end(c)


def sea_front(c, K, t, night=0.0, y=900, dawn=0.0, calm=False):
    K.layer(c, 1.2)
    wave_band(c, y, t * (0.4 if calm else 1.2), lerp_col(lerp_col("#3E6A84", "#0E1426", night), "#8A5A4A", dawn), amp=4 if calm else 14,
              x0=-4000, x1=W + 4000)
    K.end(c)


def cottage_field(c, K, t, dawn=1.0):
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), lerp_col("#8A9AAA", "#F2C49A", dawn), lerp_col("#C8D0C8", "#FBE6CC", dawn))
    K.end(c)
    K.layer(c, 0.25)
    c.drawCircle(1500, 560, 90, P("#FFE8B8", 200 * dawn))
    for k in range(-3, 9):
        hp = skia.Path(); hp.moveTo(k * 360 - 200, 760); hp.quadTo(k * 360, 600 - (k % 3) * 40, k * 360 + 380, 760); hp.close()
        c.drawPath(hp, P("#6E8A5A"))
    K.end(c)
    K.layer(c, 0.6)
    fo(c, rect(240, 560, 360, 240), "#D8D0B8", ow=6)
    roof = skia.Path(); roof.moveTo(200, 580); roof.quadTo(420, 430, 640, 580); roof.close()
    fo(c, roof, "#B89A5A", ow=6)
    fo(c, rect(380, 680, 80, 120), "#5A3E2A", ow=5)
    c.drawRect(skia.Rect.MakeXYWH(260, 760, 2000, 10), P("#4A3A2A", 0))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P("#5E6E42"))
    c.drawLine(-3000, GROUND, W + 3000, GROUND, P(INK, stroke=6))
    for k in range(-6, 20):
        c.drawLine(k * 160, GROUND + 30, k * 160 + 80, GROUND + 30, P("#4A5A34", stroke=8))
    K.end(c)


def cottage_in(c, K, t, fire=1.0):
    K.layer(c, 0.7)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, H + 4000), "#3A2E26", "#221A14")
    fo(c, rect(1300, 300, 300, 240), "#26324A", ow=6)
    for k in range(6):
        y = 320 + (k * 37 + t * 300) % 220
        c.drawLine(1320 + k * 45, y, 1316 + k * 45, y + 24, P("#8AA0C0", 180, stroke=3))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-2000, GROUND, W + 4000, 900), P("#4A3C30"))
    c.drawLine(-2000, GROUND, W + 2000, GROUND, P(INK, stroke=6))
    if fire > 0:
        c.drawCircle(960, 780, 260, blur("#F39C12", 110 * fire, 70))
        for k, colr in enumerate(["#C0392B", "#F39C12", "#F4D03F"]):
            fl = skia.Path(); h = 90 - k * 22; w = 50 - k * 12
            fl.moveTo(960 - w, 840); fl.quadTo(960 - w, 840 - h * 0.6, 960 + 6 * math.sin(t * 10 + k), 840 - h); fl.quadTo(960 + w, 840 - h * 0.6, 960 + w, 840); fl.close()
            c.drawPath(fl, P(colr))
        fo(c, rrect(880, 836, 160, 30, 10), "#3A2A1E", ow=5)
    K.end(c)


def letter(c, x, y, s, rot=0.0, a=255):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    fo(c, rect(-120, -80, 240, 160), "#F2EAD6", ow=5, a=a)
    for k in range(5):
        c.drawLine(-90, -50 + k * 26, 90 - (k % 2) * 30, -50 + k * 26, P("#8A7A5A", a, stroke=4))
    c.restore()


def skyline(c, x, y, s, col="#3A4250", a=255):
    c.save(); c.translate(x, y); c.scale(s, s)
    for k, (w, h) in enumerate([(90, 300), (70, 420), (110, 360), (80, 520), (120, 330), (90, 460), (70, 280), (100, 390)]):
        bx = -440 + sum(v[0] + 14 for v in [(90, 300), (70, 420), (110, 360), (80, 520), (120, 330), (90, 460), (70, 280), (100, 390)][:k])
        c.drawRect(skia.Rect.MakeXYWH(bx, -h, w, h), P(col, a))
        for j in range(int(h / 50)):
            c.drawRect(skia.Rect.MakeXYWH(bx + 14, -h + 20 + j * 50, w - 28, 14), P("#F6D88A", a * 0.5))
    c.restore()


def liberty(c, x, y, s, a=255):
    c.save(); c.translate(x, y); c.scale(s, s)
    col = P("#6FA89A", a)
    c.drawRect(skia.Rect.MakeXYWH(-60, -120, 120, 120), P("#8A8A7A", a))
    body = skia.Path(); body.moveTo(-40, -120); body.lineTo(-30, -360); body.lineTo(30, -360); body.lineTo(44, -120); body.close()
    c.drawPath(body, col)
    c.drawCircle(0, -390, 34, col)
    c.drawLine(24, -350, 70, -520, P("#6FA89A", a, stroke=18))
    c.drawCircle(72, -540, 22, P("#F4C430", a))
    for k in range(5):
        aa = -math.pi / 2 + (k - 2) * 0.4
        c.drawLine(0, -410, 40 * math.cos(aa), -410 + 40 * math.sin(aa), P("#6FA89A", a, stroke=8))
    c.restore()


def ticket(c, x, y, s, rot=0.0, a=255):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    fo(c, rrect(-200, -110, 400, 220, 16), "#EFE4C8", ow=6, a=a)
    c.drawRect(skia.Rect.MakeXYWH(-200, -110, 400, 50), P("#7A2A22", a))
    text(c, "WHITE STAR LINE", 0, -74, "xbold", 26, "#F2EAD6", a=a, align="center")
    text(c, "HẠNG BA", 0, 10, "xbold", 54, "#2A1A10", a=a, align="center")
    text(c, "Queenstown → New York", 0, 70, "bold", 26, "#5A4A3A", a=a, align="center")
    c.restore()


def deck_bg(c, K, t, night=0.0, tilt=0.0, lights=1.0):
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-4000, -4000, W + 8000, H + 8000), lerp_col("#9AB4C8", "#060A18", night), lerp_col("#DCE6EA", "#141A2E", night))
    if night > 0.5:
        for k in range(80):
            x = (k * 173) % (W + 600) - 300; y = (k * 97) % 560
            c.drawCircle(x, y, 1.5 + (k % 3), P("#FFFFFF", 180))
    K.end(c)
    K.layer(c, 1.0)
    c.save(); c.translate(960, GROUND); c.rotate(tilt); c.translate(-960, -GROUND)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P(lerp_col("#B89A6A", "#3A3226", night)))
    for k in range(-20, 40):
        c.drawLine(k * 90, GROUND, k * 90 - 60, GROUND + 900, P("#000000", 40, stroke=3))
    c.drawLine(-3000, GROUND, W + 3000, GROUND, P(INK, stroke=6))
    c.drawLine(-3000, GROUND - 160, W + 3000, GROUND - 160, P(INK, stroke=8))     # lan can
    for k in range(-20, 40):
        c.drawLine(k * 80, GROUND - 160, k * 80, GROUND, P(INK, stroke=4))
    for k in range(-2, 6):   # đèn boong
        lx = k * 520 + 100
        c.drawLine(lx, GROUND - 160, lx, GROUND - 380, P(INK, stroke=8))
        if lights > 0:
            c.drawCircle(lx, GROUND - 400, 18, P("#F6D88A", 255 * lights))
            c.drawCircle(lx, GROUND - 400, 60, blur("#F6D88A", 90 * lights, 20))
    c.restore()
    K.end(c)


def lifeboat(c, x, y, s, people=(), t=0.0, sway=0.0):
    c.save(); c.translate(x, y); c.rotate(sway); c.scale(s, s)
    hull = skia.Path(); hull.moveTo(-320, -60); hull.lineTo(320, -60); hull.quadTo(300, 60, 0, 70); hull.quadTo(-300, 60, -320, -60); hull.close()
    fo(c, hull, "#F2EEE4", ow=7)
    c.drawLine(-310, -40, 310, -40, P("#C0392B", stroke=6))
    c.restore()
    for i, (who, kw) in enumerate(people):
        ST(c, who, x + (-220 + i * 110) * s, y - 40 * s, 0.6 * s, t + i, sit=1.0, **kw)


def corridor(c, K, t, water=0.0, crowd=False, gate=False):
    K.layer(c, 0.8)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, H + 4000), "#E8E2D2", "#C8C0AC")
    for k in range(-3, 10):
        x = k * 300
        fo(c, rect(x + 40, 360, 160, 500), "#A88A5A", ow=5)
        c.drawCircle(x + 180, 620, 10, P("#D8B04A"))
    for k in range(-3, 10):
        c.drawCircle(k * 300 + 260, 300, 14, P("#F6E8A8"))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-2000, GROUND, W + 4000, 900), P("#8A7A62"))
    c.drawLine(-2000, GROUND, W + 2000, GROUND, P(INK, stroke=6))
    if gate:
        for k in range(9):
            c.drawLine(1300 + k * 40, 380, 1300 + k * 40, GROUND, P("#3A3A3A", stroke=10))
        c.drawLine(1290, 400, 1630, 400, P("#3A3A3A", stroke=12)); c.drawLine(1290, GROUND - 40, 1630, GROUND - 40, P("#3A3A3A", stroke=12))
    K.end(c)


def water_over(c, K, t, level, col="#2E6A88", a=200):
    if level <= 0:
        return
    K.layer(c, 1.0)
    y = GROUND - level
    wave_band(c, y, t * 2, col, amp=6, x0=-2000, x1=W + 2000, a=a)
    K.end(c)


def iceberg(c, x, y, s, night=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    ib = skia.Path(); ib.moveTo(-420, 0); ib.lineTo(-300, -260); ib.lineTo(-160, -320); ib.lineTo(-40, -520); ib.lineTo(120, -380)
    ib.lineTo(260, -420); ib.lineTo(420, 0); ib.close()
    fo(c, ib, lerp_col("#E8F2F6", "#8AA0B8", night), ow=6)
    c.drawLine(-40, -520, 20, -60, P("#FFFFFF", 90, stroke=10))
    c.restore()


def subtitle(c, t):
    for a, b, s in ALIGN:
        if a <= t < b:
            al = 255 * clamp(min(t - a, b - t) / 0.15)
            words, lines, cur = s.split(), [], ""
            for w_ in words:
                tst = (cur + " " + w_).strip()
                if tw(tst, "bold", 42) > 1500 and cur:
                    lines.append(cur); cur = w_
                else:
                    cur = tst
            lines.append(cur)
            y0 = 1040 - 54 * (len(lines) - 1)
            for i, l in enumerate(lines):
                text(c, l, W / 2, y0 + i * 54, "bold", 42, "#FFFFFF", a=al, align="center", stroke=8, stroke_color="#111111")
            return
