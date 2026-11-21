"""Bản thử 16:9 — Bộp & Gầm đồ hiện đại, diễn câm theo lời dẫn (bộ khung v2 + đồ hiện đại).
Tình huống: "Vì sao hàng mình chọn ở siêu thị luôn chậm nhất?"  ~18,5 giây.
  python3 src/demo.py preview 1.0 4.0 ...   → build/pv_<t>.png
  python3 src/demo.py full                  → build/Modern_demo_nosfx.mp4
"""
import math, subprocess, sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "cung" / "src")); sys.path.insert(0, str(ROOT.parent / "tools"))
import skia  # noqa
from PIL import Image  # noqa
from lib import paint, text, Xf, clamp, lerp, nfc, tw  # noqa
from rig import Pose, draw_char, P, OUT, fo, oval, ease_out, ease_in_out, back_out, noise1  # noqa

W, H, FPS = 1920, 1080, 30
DUR = 18.6
BUILD = ROOT / "build"

GAM = dict(outfit="modern", shirt="#5FA35A", pants="#4A6A9A")
BOP = dict(outfit="modern", shirt="#E8833A", pants="#3B4A6B")
GRAN = dict(outfit="modern", shirt="#D97AA0", pants="#7A6A8A", sleeves="long")
CASH = dict(outfit="modern", shirt="#E9463A", pants="#2A2A2A")


def grad(c, rect, top, bot):
    def col(h):
        h = h.lstrip("#"); return skia.ColorSetRGB(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, rect.top()), skia.Point(0, rect.bottom())], [col(top), col(bot)])
    c.drawRect(rect, skia.Paint(Shader=sh))


def rr(x, y, w, h, r):
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)); return p


class Cam:
    def __init__(self, cx=W / 2, cy=H / 2, z=1.0):
        self.cx, self.cy, self.z = cx, cy, z

    def on(self, c):
        c.save(); c.translate(W / 2, H / 2); c.scale(self.z, self.z); c.translate(-self.cx, -self.cy)

    def off(self, c):
        c.restore()


def ch(c, who, x, y, s, t, kw, **more):
    d = dict(kw); d.update(more)
    seed = {"bop": 0.4, "gam": 1.9}.get(who, 3.3)
    d["head_tilt"] = d.get("head_tilt", 0.0) + 2.5 * noise1(t * 0.8, seed)
    return draw_char(c, Pose(who, x, y, s, t, **d))


def walk_phase(x, x0, s):
    return abs(x - x0) / (92 * s) * math.pi


# ---------------------------------------------------------------- siêu thị
BACK_Y, FRONT_Y = 545, 1035     # chân người ở hàng sau / hàng trước
BS, FS = 0.55, 0.78             # tỉ lệ nhân vật hàng sau / trước


def store_bg(c, t):
    grad(c, skia.Rect.MakeXYWH(-600, -600, W + 1200, 1200), "#DCEFEA", "#C9E4DD")
    # kệ hàng phía sau
    for k in range(-2, 9):
        x = 140 + k * 260
        fo(c, rr(x, 150, 230, 420, 10), "#F4F1EA", ow=5)
        for r in range(4):
            y = 175 + r * 100
            c.drawLine(x + 10, y + 80, x + 220, y + 80, P(OUT, stroke=5))
            for j in range(5):
                colr = ["#E85D4A", "#F4C430", "#4FA3CF", "#7FB069", "#C77DD1"][(j + r + k) % 5]
                fo(c, rr(x + 16 + j * 41, y + 18 + (j % 2) * 10, 34, 62 - (j % 2) * 10, 5), colr, ow=3)
    # sàn
    grad(c, skia.Rect.MakeXYWH(-600, 560, W + 1200, 900), "#EDE6D8", "#D8CFBE")
    for k in range(-4, 16):
        c.drawLine(-200 + k * 170, 560, -500 + k * 230, H + 200, P("#C8BEAA", stroke=3))
    for y in (640, 760, 900):
        c.drawLine(-600, y, W + 600, y, P("#C8BEAA", stroke=3))
    # biển số quầy
    for i, (x, y) in enumerate([(330, 120), (420, 230), (520, 340)]):
        pass


def lane_sign(c, x, y, n, s=1.0, lit=False):
    with Xf(c, x, y, 0, s):
        c.drawLine(0, -200, 0, -40, P(OUT, stroke=6))
        fo(c, oval(0, 0, 46, 46), "#F4C430" if lit else "#FFFFFF", ow=6)
        text(c, str(n), 0, 18, "xbold", 52, "#1A1A1A", align="center")


def counter(c, x, y, s=1.0):
    """Quầy thu ngân nhìn ngang: thân xám, băng chuyền đen, máy tính tiền."""
    with Xf(c, x, y, 0, s):
        fo(c, rr(-260, -230, 400, 230, 14), "#8E969B", ow=6)
        fo(c, rr(-270, -250, 420, 40, 12), "#2E3338", ow=6)
        for k in range(8):
            c.drawLine(-250 + k * 50, -244, -250 + k * 50, -216, P("#4A5056", stroke=4))
        fo(c, rr(-240, -380, 120, 130, 12), "#5A6168", ow=6)
        fo(c, rr(-228, -366, 96, 54, 8), "#9FE0B0", ow=4)


def cart(c, x, y, s, t, full=0.6, rattle=0.0):
    with Xf(c, x, y - abs(math.sin(t * 30)) * 3 * rattle, 0, s):
        bask = skia.Path(); bask.moveTo(-150, -260); bask.lineTo(130, -260); bask.lineTo(100, -90); bask.lineTo(-120, -90); bask.close()
        for k in range(int(5 * full) + 1):
            colr = ["#E85D4A", "#F4C430", "#4FA3CF", "#7FB069", "#C77DD1", "#F08A4B"][k % 6]
            fo(c, rr(-120 + k * 44, -320 + (k % 2) * 30, 40, 80, 6), colr, ow=3)
        c.drawPath(bask, P("#FFFFFF", 120))
        for k in range(7):
            c.drawLine(-150 + k * 40, -260, -120 + k * 34, -90, P("#7A8288", stroke=4))
        for k in range(4):
            c.drawLine(-150 + k * 6, -260 + k * 42, 130 - k * 8, -260 + k * 42, P("#7A8288", stroke=4))
        c.drawPath(bask, P(OUT, stroke=6))
        c.drawLine(130, -260, 190, -310, P(OUT, stroke=10)); c.drawLine(180, -320, 205, -300, P("#E85D4A", stroke=16))
        c.drawLine(-110, -90, -110, -20, P(OUT, stroke=7)); c.drawLine(90, -90, 90, -20, P(OUT, stroke=7))
        c.drawLine(-120, -40, 100, -40, P(OUT, stroke=7))
        for wx in (-110, 90):
            c.drawCircle(wx, -14, 16, P("#2A2A2A")); c.drawCircle(wx, -14, 6, P("#9AA3A8"))


def jar(c, x, y, s, tilt=0.0, fill=1.0):
    with Xf(c, x, y, tilt, s):
        body = rr(-50, -110, 100, 120, 22)
        c.drawPath(body, P("#DFF3FB", 200))
        if fill > 0:
            c.save(); c.clipPath(body, skia.ClipOp.kIntersect, True)
            c.drawRect(skia.Rect.MakeXYWH(-60, 10 - 120 * fill, 120, 130), P("#E8B53A"))
            for k in range(6):
                c.drawCircle(-30 + (k % 3) * 30, 10 - 120 * fill + 14 + (k // 3) * 20, 10, P("#F6D36A"))
            c.restore()
        c.drawPath(body, P(OUT, stroke=5))
        fo(c, rr(-40, -126, 80, 20, 6), "#C9A06A", ow=4)


COINS = [(((k * 73) % 100) / 100.0, ((k * 37) % 100) / 100.0) for k in range(28)]


def coins(c, x, y, t, t0, s=1.0):
    age = t - t0
    if age < 0:
        return
    for k, (a, b) in enumerate(COINS):
        st = k * 0.025
        q = clamp((age - st) / 0.5)
        if q <= 0:
            continue
        tx, ty = x + (a - 0.5) * 300 * s, y + b * 30 * s
        px, py = lerp(x, tx, q), lerp(y - 60 * s, ty, q) - 120 * s * math.sin(math.pi * q) * (1 - b)
        c.drawOval(skia.Rect.MakeXYWH(px - 12 * s, py - 7 * s, 24 * s, 14 * s), P("#F4C430"))
        c.drawOval(skia.Rect.MakeXYWH(px - 12 * s, py - 7 * s, 24 * s, 14 * s), P(OUT, stroke=3))


def cloud(c, x, y, s, t):
    for dx, r in [(-40, 40), (0, 54), (44, 38)]:
        c.drawCircle(x + dx * s, y, r * s, P("#6A7280"))
    for k in range(4):
        q = (t * 1.8 + k / 4) % 1
        c.drawLine(x + (-40 + k * 26) * s, y + (40 + q * 120) * s, x + (-44 + k * 26) * s, y + (60 + q * 120) * s, P("#5DADE2", 255 * (1 - q), stroke=5))


# ---------------------------------------------------------------- cảnh
BACK_Q = [720, 920, 1120]          # 3 người hàng sau (đứng trước Bộp)
FRONT_GRAN = 700


def world(c, t, gam_kw, bop_x, bop_kw, gx, back_shift=0.0, gran_kw=None, coins_t0=None, jar_kw=None, extra=None):
    store_bg(c, t)
    c.drawRect(skia.Rect.MakeXYWH(-600, BACK_Y + 20, W + 1200, 26), P("#B9AE98"))
    c.drawLine(-600, BACK_Y + 20, W + 600, BACK_Y + 20, P(OUT, 120, stroke=4))
    lane_sign(c, 560, 230, 2, 0.7, lit=True)
    lane_sign(c, 600, 640, 3, 0.9, lit=True)
    # hàng sau (quầy 2) — người tiến dần lên
    counter(c, 420, BACK_Y, 0.6)
    ch(c, "npc_man", 200, BACK_Y, BS, t, CASH, face=1, eyes="happy", mouth="smile", hand_r=(80, -40))
    shoppers = [("npc_man", dict(outfit="modern", shirt="#4FA3CF", pants="#2A2A2A", sleeves="long")),
                ("npc_gran", dict(outfit="modern", shirt="#7FB069", pants="#5A4A3A")),
                ("npc_man", dict(outfit="modern", shirt="#F4C430", pants="#3B4A6B"))]
    for i, (who, kw) in enumerate(shoppers):
        x0 = BACK_Q[i]
        x = x0 - back_shift * 200
        if x < 600:
            x = 600 - (600 - x) * 3          # đi khỏi quầy, ra khỏi khung
        if x < -200:
            continue
        moving = (back_shift % 1) < 0.5 and back_shift > 0 and back_shift < 3.2
        ch(c, who, x, BACK_Y, BS, t, kw, face=-1, walk=walk_phase(x, x0, BS) if moving else None, eyes="open", mouth="flat")
    ch(c, "bop", bop_x, BACK_Y, BS, t, BOP, **bop_kw)
    # hàng trước (quầy 3)
    counter(c, 400, FRONT_Y, 0.95)
    cash_kw = dict(eyes="open", mouth="flat")
    if coins_t0 is not None and t > coins_t0 + 0.4:
        cash_kw = dict(eyes="squint", mouth="wavy", brow_tilt=-0.8, sweat=1.0)
    ch(c, "npc_man", 140, FRONT_Y, FS, t, CASH, face=1, **cash_kw)
    gk = dict(gran_kw or {})
    ch(c, "npc_gran", FRONT_GRAN, FRONT_Y, FS, t, GRAN, face=-1, **gk)
    if jar_kw:
        jar(c, **jar_kw)
    if coins_t0 is not None:
        coins(c, 360, FRONT_Y - 240, t, coins_t0)
    cart(c, gx - 210, FRONT_Y, FS, t, rattle=gam_kw.pop("_rattle", 0.0))
    ch(c, "gam", gx, FRONT_Y, FS, t, GAM, **gam_kw)
    if extra:
        extra()


def gam_entry(t):
    """0–3.6: Gầm đẩy xe vào, nhìn hai hàng, lấy đà rồi quẹo vào hàng ngắn."""
    if t < 1.4:
        x = lerp(2250, 1500, ease_out(t / 1.4))
        return x, dict(face=-1, walk=walk_phase(x, 2250, FS), hand_r=(150, -10), hand_l=(170, 20), eyes="open", look=(-1, 0), mouth="flat", _rattle=1.0)
    if t < 2.4:
        # đứng lại so hai hàng: liếc lên hàng sau, xuống hàng trước, nhếch mép
        lk = (-1, -0.8) if t < 1.85 else (-1, 0.6)
        return 1500, dict(face=-1, hand_r=(150, -10), hand_l=(170, 20), eyes="squint" if t > 1.9 else "open", look=lk,
                          mouth="smirk" if t > 2.0 else "flat", brow=0.6 if t > 2.0 else 0.0, lean=-6 * clamp((t - 2.1) / 0.3))
    q = clamp((t - 2.4) / 0.9)
    x = lerp(1500, 1050, ease_in_out(q))
    stop = clamp((t - 3.3) / 0.3)
    return x, dict(face=-1, walk=walk_phase(x, 1500, FS) if q < 1 else None, hand_r=(150, -10), hand_l=(170, 20), eyes="happy",
                   mouth="grin", lean=12 * math.sin(math.pi * q) - 6 * stop * math.exp(-stop * 3), squash=1 - 0.06 * math.sin(math.pi * stop),
                   _rattle=1.0 if q < 1 else 0.0)


def bop_entry(t):
    if t < 1.6:
        return 2200, dict(face=-1)
    q = clamp((t - 1.6) / 1.8)
    x = lerp(2200, 1320, ease_out(q))
    return x, dict(face=-1, walk=walk_phase(x, 2200, BS) if q < 0.97 else None, eyes="open", mouth="smile", hand_l=(60, 60), hand_r=(-20, 70))


def sc_a(c, t):
    K = Cam(W / 2, H / 2, 1.0); K.on(c)
    gx, gk = gam_entry(t)
    bx, bk = bop_entry(t)
    world(c, t, gk, bx, bk, gx, gran_kw=dict(eyes="open", mouth="smile", hand_r=(90, -40)))
    if 2.5 < t < 3.4:
        for k in range(4):
            c.drawLine(gx + 160 + k * 40, FRONT_Y - 30 - k * 12, gx + 260 + k * 40, FRONT_Y - 34 - k * 12, P("#FFFFFF", 200, stroke=6))
    K.off(c)


def sc_b(c, t):
    lt = t - 3.6
    K = Cam(1060, 720, 2.4); K.on(c)
    drum = math.sin(lt * 18)
    world(c, t, dict(face=-1, hand_r=(150, -10 + 8 * drum), hand_l=(170, 20 - 8 * drum), eyes="squint", look=(-1, 0), mouth="grin",
                     brow=0.5 + 0.5 * max(0, math.sin(lt * 9)), head_tilt=6), 1180, dict(face=-1), 1050,
          gran_kw=dict(eyes="open", mouth="smile"))
    K.off(c)


def sc_c(c, t):
    lt = t - 6.3
    K = Cam(560, FRONT_Y - 330, 1.9); K.on(c)
    lift = ease_out(clamp(lt / 0.5))
    tip = ease_in_out(clamp((lt - 0.9) / 0.4))
    jk = dict(x=lerp(620, 470, lift), y=lerp(FRONT_Y - 200, FRONT_Y - 330, lift) + 40 * tip, s=1.0, tilt=lerp(0, 120, tip),
              fill=1 - 0.8 * clamp((lt - 1.2) / 0.8))
    world(c, t, dict(face=-1, hand_r=(150, -10), hand_l=(170, 20), eyes="wide" if lt > 1.4 else "open", look=(-1, 0),
                     mouth="o" if lt > 1.4 else "smile", brow=1.0 if lt > 1.4 else 0.0), 1180, dict(face=-1), 1050,
          gran_kw=dict(hand_r=(lerp(40, 160, lift), lerp(60, -120, lift)), hand_l=(lerp(40, 130, lift), lerp(60, -100, lift)),
                       eyes="happy", mouth="smile"),
          coins_t0=6.3 + 1.2, jar_kw=jk)
    K.off(c)
    if lt > 1.3:
        text(c, "LẺNG XẺNG", 1300, 300, "xbold", 110, "#F4C430", a=255 * clamp((lt - 1.3) / 0.2), align="center", stroke=10,
             stroke_color="#1A120D")


def sc_d(c, t):
    lt = t - 9.2
    K = Cam(W / 2, H / 2, 1.0); K.on(c)
    shift = clamp(lt / 2.8) * 3.0
    bx = 1320 - shift * 200
    bmove = (shift % 1) < 0.5 and lt < 2.8
    count = int(lt * 2.5) % 2
    world(c, t, dict(face=-1, hand_r=(150, -10), hand_l=(170, 20), eyes="open", look=(-0.6, -1), mouth="frown", brow_tilt=-0.6,
                     head_tilt=8 * math.sin(lt * 1.5)), bx, dict(face=-1, walk=walk_phase(bx, 1320, BS) if bmove else None,
                                                                    eyes="happy", mouth="smile"), 1050, back_shift=shift,
          gran_kw=dict(hand_r=(150, 40 if count else 0), hand_l=(60, 60), eyes="squint", look=(-1, 1), mouth="flat"),
          coins_t0=-10)
    K.off(c)
    for k in range(min(3, int(lt / 0.9) + 1)):
        text(c, "TÍT!", 520, 200 - k * 4, "xbold", 70, "#7FB069", a=255 * clamp(1 - (lt - k * 0.9) / 0.6) if lt > k * 0.9 else 0,
             align="center", stroke=7, stroke_color="#1A120D")


def sc_e(c, t):
    lt = t - 12.3
    grad(c, skia.Rect.MakeWH(W, H), "#25324A", "#141B29")
    hi = int(lt * 3) % 3 if lt < 2.4 else 0
    for i in range(3):
        y = 330 + i * 200
        p = clamp((lt - i * 0.2) / 0.4)
        with Xf(c, W / 2, y, 0, back_out(p) if p < 1 else 1.0):
            lit = (i == hi)
            fo(c, rr(-620, -60, 1240, 120, 60), "#F4C430" if lit else "#3E4C66", ow=6)
            text(c, f"Hàng {i + 1}", -520, 18, "xbold", 52, "#1A1A1A" if lit else "#C9D3E0")
            for k in range(3 if i else 1):
                fo(c, rr(200 - k * 140, -36, 90, 72, 14), "#FFFFFF" if lit else "#7A879C", ow=4)
    if lt > 1.0:
        g = back_out(clamp((lt - 1.0) / 0.4))
        with Xf(c, 1650, 210, -8, g):
            text(c, "1/3", 0, 0, "xbold", 150, "#F4C430", align="center", stroke=12, stroke_color="#1A120D")


def sc_f(c, t):
    lt = t - 15.8
    K = Cam(1050, H / 2 + 150, 1.2); K.on(c)
    slump = ease_out(clamp((lt - 0.8) / 0.5))
    bx = lerp(800, 1700, clamp(lt / 2.0))

    def bop_pass():
        ch(c, "bop", bx, FRONT_Y + 40, FS, t, BOP, face=1, walk=walk_phase(bx, 800, FS), hand_r=(120, -200 + 20 * math.sin(lt * 12)),
           hand_l=(-30, 60), eyes="happy", mouth="grin")
        fo(c, rr(bx - 150, FRONT_Y - 260, 90, 110, 14), "#C9A06A", ow=5)
    world(c, t, dict(face=-1, hand_r=(150, -10), hand_l=(170, 20), eyes="closed" if slump > 0.5 else "open", mouth="frown",
                     crouch=0.6 * slump, lean=24 * slump, head_tilt=-8 * slump), 2400, dict(face=-1), 1050,
          gran_kw=dict(hand_r=(150, 20 * (int(lt * 2.5) % 2)), eyes="squint", look=(-1, 1)), coins_t0=-10, extra=bop_pass)
    if slump > 0.3:
        cloud(c, 1050, FRONT_Y - 500, 1.0 * slump, t)
    K.off(c)


SHOTS = [(0, 3.6, sc_a), (3.6, 6.3, sc_b), (6.3, 9.2, sc_c), (9.2, 12.3, sc_d), (12.3, 15.8, sc_e), (15.8, DUR, sc_f)]

VO = [
    (0.3, 3.5, "Bạn có bao giờ thấy hàng mình chọn luôn là hàng chậm nhất?"),
    (3.8, 6.1, "Gầm thì chắc chắn là có."),
    (6.4, 9.1, "Hắn chọn hàng ngắn nhất… nhưng người phía trước lôi ra cả hũ tiền xu."),
    (9.3, 12.2, "Trong khi đó, hàng bên cạnh cứ thế trôi."),
    (12.4, 15.7, "Thật ra, khi có ba hàng, khả năng hàng bạn đứng là nhanh nhất chỉ một phần ba."),
    (15.9, 18.4, "Hai phần ba còn lại… là cảm giác của Gầm."),
]


def subtitle(c, t):
    for a, b, s in VO:
        if a <= t < b:
            al = 255 * clamp(min(t - a, b - t) / 0.2)
            text(c, s, W / 2, 1050, "bold", 44, "#FFFFFF", a=al, align="center", stroke=8, stroke_color="#111111")


def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas(); c.clear(skia.ColorWHITE)
    for a, b, fn in SHOTS:
        if a <= t < b:
            c.save(); fn(c, t); c.restore(); break
    subtitle(c, t)
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def chunk(args):
    k, f0, f1 = args
    out = BUILD / f"mc_{k:02d}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    s = skia.Surface(W, H)
    for i in range(f0, f1):
        p.stdin.write(frame(i / FPS, s).tobytes())
    p.stdin.close(); p.wait()
    return out


if __name__ == "__main__":
    BUILD.mkdir(exist_ok=True)
    if sys.argv[1] == "preview":
        for ts in sys.argv[2:]:
            Image.fromarray(frame(float(ts))[..., :3]).save(BUILD / f"pv_{float(ts):05.2f}.png")
    else:
        nfr = int(DUR * FPS); step = math.ceil(nfr / 4)
        with Pool(4) as pool:
            chs = pool.map(chunk, [(k, f, min(nfr, f + step)) for k, f in enumerate(range(0, nfr, step))])
        (BUILD / "mc.txt").write_text("".join(f"file '{x.name}'\n" for x in chs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(BUILD / "mc.txt"), "-c", "copy",
                        str(BUILD / "Modern_demo_nosfx.mp4")], check=True)
        for x in chs:
            x.unlink()
        (BUILD / "mc.txt").unlink()
        print("xong")
