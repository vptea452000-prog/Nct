"""Dựng thử 10 giây đầu "Nếu bạn là người lính Nhật" bằng người que v2 (16:9).
  python3 linh_nhat/src/test_open.py preview 1 5 9   → linh_nhat/build/pv_<t>.png
  python3 linh_nhat/src/test_open.py full            → linh_nhat/build/Test_mo_dau.mp4
"""
import math, subprocess, sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools")); sys.path.insert(0, str(ROOT.parent / "cung" / "src"))
import skia  # noqa
from PIL import Image  # noqa
from lib import text  # noqa
from stick2 import Stick, draw_stick, P, fo, oval, clamp, lerp, ease_out, ease_in_out, back_out, INK  # noqa

W, H, FPS = 1920, 1080, 30
DUR = 10.5
BUILD = ROOT / "build"


def grad(c, rect, top, bot):
    def col(h):
        h = h.lstrip("#"); return skia.ColorSetRGB(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, rect.top()), skia.Point(0, rect.bottom())], [col(top), col(bot)])
    c.drawRect(rect, skia.Paint(Shader=sh))


class Cam:
    def __init__(self, cx=W / 2, cy=H / 2, z=1.0):
        self.cx, self.cy, self.z = cx, cy, z

    def on(self, c):
        c.save(); c.translate(W / 2, H / 2); c.scale(self.z, self.z); c.translate(-self.cx, -self.cy)

    def off(self, c):
        c.restore()


def wave_band(c, y, t, col, amp=14, speed=60, a=255):
    p = skia.Path(); p.moveTo(-400, H + 400)
    for k in range(0, 60):
        x = -400 + k * 50
        p.lineTo(x, y + amp * math.sin(x * 0.012 + t * speed * 0.02))
    p.lineTo(W + 400, H + 400); p.close()
    c.drawPath(p, P(col, a))


def boat(c, x, y, s, t):
    c.save(); c.translate(x, y + 6 * math.sin(t * 2)); c.rotate(2 * math.sin(t * 1.6)); c.scale(s, s)
    hull = skia.Path(); hull.moveTo(-340, -40); hull.lineTo(340, -40); hull.quadTo(300, 60, 220, 70); hull.lineTo(-240, 70)
    hull.quadTo(-320, 50, -340, -40); hull.close()
    fo(c, hull, "#8A5E3A", ow=7)
    c.drawLine(-320, -10, 320, -10, P("#6E4A2E", stroke=6))
    c.restore()


# ---------------------------------------------------------------- 0–4,2: biển lúc bình minh, kéo lưới cùng cha
def sh_sea(c, t):
    K = Cam(W / 2, H / 2, lerp(1.0, 1.08, ease_in_out(t / 4.2))); K.on(c)
    grad(c, skia.Rect.MakeXYWH(-400, -400, W + 800, 1000), "#F6B98A", "#FCE6C8")
    c.drawCircle(1450, 520, 110, P("#FFD9A0"))
    for k, (yy, col) in enumerate([(560, "#9DB7C2"), (600, "#7FA1B0")]):
        wave_band(c, yy, t + k, col, amp=6)
    # làng chài xa
    for k in range(5):
        x = 120 + k * 90
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(x, 520, 70, 46)) or skia.Path(), "#C9B79A", ow=4)
        roof = skia.Path(); roof.moveTo(x - 10, 522); roof.lineTo(x + 35, 492); roof.lineTo(x + 80, 522); roof.close(); fo(c, roof, "#6E4E3A", ow=4)
    pull = math.sin(t * 2.4)
    by = 760
    draw_stick(c, Stick("father", 820, by, 0.9, t, face=1, hand_f=(120 + 30 * pull, 40 - 20 * pull), hand_b=(150 + 30 * pull, 60 - 20 * pull),
                        lean=8 + 6 * pull, eyes="dot", mouth="smile"))
    draw_stick(c, Stick("you", 1080, by, 0.9, t + 0.4, face=1, hand_f=(110 + 30 * pull, 50 - 20 * pull), hand_b=(140 + 30 * pull, 70 - 20 * pull),
                        lean=8 + 6 * pull, eyes="happy" if t > 2.2 else "dot", mouth="grin" if t > 2.2 else "smile"))
    # lưới kéo lên, cá nhảy
    net = skia.Path(); net.moveTo(1220 + 30 * pull, by - 260 - 20 * pull); net.quadTo(1400, by - 60, 1480, by + 40)
    c.drawPath(net, P(INK, stroke=4))
    boat(c, 980, by + 20, 1.0, t)
    wave_band(c, by + 70, t, "#6A92A4", amp=12)
    wave_band(c, by + 120, t + 1.3, "#5A8294", amp=14)
    if t > 2.0:
        q = ((t - 2.0) * 1.1) % 1
        fx, fy = 1460 + 60 * q, by + 40 - 220 * math.sin(math.pi * q)
        c.save(); c.translate(fx, fy); c.rotate(-40 + 80 * q)
        fo(c, oval(0, 0, 34, 14), "#B8C8D0", ow=4)
        tl = skia.Path(); tl.moveTo(30, 0); tl.lineTo(52, -14); tl.lineTo(52, 14); tl.close(); fo(c, tl, "#A0B4BE", ow=4)
        c.restore()
    K.off(c)


# ---------------------------------------------------------------- 4,2–7: bếp, mẹ nấu cơm, bạn bước vào
def sh_kitchen(c, t):
    lt = t - 4.2
    K = Cam(W / 2, H / 2 + 20, 1.0); K.on(c)
    grad(c, skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), "#5A4636", "#3A2C22")
    c.drawRect(skia.Rect.MakeXYWH(-400, 860, W + 800, 500), P("#6E5642"))
    c.drawLine(-400, 860, W + 400, 860, P(INK, stroke=6))
    # cửa trượt sáng phía phải
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(1500, 300, 300, 560)) or skia.Path(), "#F6E7C0", ow=6)
    for k in range(1, 3):
        c.drawLine(1500 + k * 100, 300, 1500 + k * 100, 860, P(INK, stroke=4))
    for k in range(1, 4):
        c.drawLine(1500, 300 + k * 140, 1800, 300 + k * 140, P(INK, stroke=4))
    # bếp lửa + nồi
    glow = P("#F39C12", 90); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60))
    c.drawCircle(760, 820, 200, glow)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(620, 760, 280, 100)) or skia.Path(), "#8A7A6A", ow=6)
    for k, colr in enumerate(["#C0392B", "#F39C12", "#F4D03F"]):
        fl = skia.Path(); h = 70 - k * 18; w = 50 - k * 12
        fl.moveTo(760 - w, 770); fl.quadTo(760 - w, 770 - h * 0.6, 760 + 6 * math.sin(t * 12 + k), 770 - h); fl.quadTo(760 + w, 770 - h * 0.6, 760 + w, 770); fl.close()
        c.drawPath(fl, P(colr))
    pot = skia.Path(); pot.moveTo(660, 640); pot.lineTo(860, 640); pot.quadTo(850, 740, 760, 745); pot.quadTo(670, 740, 660, 640); pot.close()
    fo(c, pot, "#3A3A3A", ow=6)
    fo(c, oval(760, 640, 110, 22), "#2A2A2A", ow=5)
    for k in range(4):
        q = (lt * 0.6 + k / 4) % 1
        stp = P("#FFFFFF", 170 * (1 - q)); stp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
        c.drawCircle(740 + 30 * math.sin(q * 6 + k), 610 - q * 260, 24 + q * 30, stp)
    stir = math.sin(lt * 4)
    draw_stick(c, Stick("mother", 520, 860, 1.0, t, face=1, hand_f=(150 + 20 * stir, 10 + 10 * math.cos(lt * 4)), hand_b=(110, 60),
                        lean=6, eyes="dot", mouth="smile", look=(1, 0.3)))
    # bạn bước vào từ cửa
    q = ease_out(clamp(lt / 1.6))
    x = lerp(1700, 1180, q)
    walking = q < 0.98
    draw_stick(c, Stick("you", x, 860, 1.0, t, face=-1, walk=abs(x - 1700) / 70 * math.pi if walking else None,
                        hand_f=None if walking else (60, -180 + 10 * math.sin(lt * 8)), eyes="happy", mouth="grin"))
    if not walking:
        # cầm xâu cá giơ lên khoe
        fx, fy = x - 60, 860 - 420
        for k in range(3):
            fo(c, oval(fx - 10 + k * 8, fy + 60 + k * 30, 14, 30), "#B8C8D0", ow=4)
    K.off(c)


# ---------------------------------------------------------------- 7–10,5: trưởng làng mang tờ giấy đỏ
def sh_paper(c, t):
    lt = t - 7.0
    if lt < 2.2:
        K = Cam(W / 2, H / 2 + 20, 1.0); K.on(c)
        grad(c, skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), "#C9D6DA", "#EDEAE2")
        c.drawRect(skia.Rect.MakeXYWH(-400, 860, W + 800, 500), P("#CDBF9E"))
        c.drawLine(-400, 860, W + 400, 860, P(INK, stroke=6))
        for k in range(4):
            x = 100 + k * 480
            fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(x, 520, 300, 340)) or skia.Path(), "#D8C8A8", ow=6)
            roof = skia.Path(); roof.moveTo(x - 50, 530); roof.lineTo(x + 150, 400); roof.lineTo(x + 350, 530); roof.close()
            fo(c, roof, "#5A4A3E", ow=6)
        q = ease_out(clamp(lt / 1.2))
        cx = lerp(-200, 760, q)
        walking = q < 0.98
        give = ease_out(clamp((lt - 1.2) / 0.5))
        draw_stick(c, Stick("chief", cx, 860, 1.0, t, face=1, walk=abs(cx + 200) / 70 * math.pi if walking else None,
                            hand_f=(lerp(60, 170, give), lerp(120, -20, give)), eyes="dot", mouth="flat", brow=-0.3))
        hx = cx + lerp(60, 170, give) + 20
        hy = 860 - 2 * 108 - 150 + lerp(120, -20, give)
        c.save(); c.translate(hx, hy); c.rotate(-8)
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-10, -40, 70, 90)) or skia.Path(), "#C0392B", ow=4)
        c.restore()
        draw_stick(c, Stick("you", 1120, 860, 1.0, t, face=-1, eyes="wide" if lt > 1.4 else "dot", mouth="o" if lt > 1.4 else "smile",
                            hand_f=(70, lerp(140, 30, give)), look=(-1, 0.3)))
        K.off(c)
    else:
        # cận cảnh tờ giấy đỏ giữa khung xám — màu duy nhất
        q = back_out(clamp((lt - 2.2) / 0.5))
        grad(c, skia.Rect.MakeWH(W, H), "#6E6E6E", "#4A4A4A")
        c.save(); c.translate(W / 2, H / 2 + 20); c.rotate(-3); c.scale(q, q)
        c.drawRect(skia.Rect.MakeXYWH(-330, -420, 660, 840), P("#000000", 60))
        fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(-320, -430, 640, 840)) or skia.Path(), "#C83A2E", ow=8)
        for k in range(9):
            w = 460 if k % 3 else 300
            c.drawLine(-w / 2, -300 + k * 70, w / 2, -300 + k * 70, P("#3A1410", stroke=12))
        c.drawCircle(200, 300, 60, P("#3A1410", stroke=8))
        c.restore()


SHOTS = [(0, 4.2, sh_sea), (4.2, 7.0, sh_kitchen), (7.0, DUR, sh_paper)]
VO = [(0.3, 2.0, "Bạn mười chín tuổi."), (2.1, 4.1, "Bạn sống ở một làng chài nhỏ bên bờ biển Nhật Bản."),
      (4.3, 6.9, "Mỗi tối mẹ bạn nấu một nồi cơm trắng…"), (7.2, 9.0, "Rồi một hôm, ông trưởng làng mang tới một tờ giấy màu đỏ."),
      (9.3, 10.4, "Người ta gọi nó là “giấy đỏ”.")]


def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas(); c.clear(skia.ColorWHITE)
    for a, b, fn in SHOTS:
        if a <= t < b:
            c.save(); fn(c, t); c.restore(); break
    for a, b, s in VO:
        if a <= t < b:
            al = 255 * clamp(min(t - a, b - t) / 0.2)
            text(c, s, W / 2, 1040, "bold", 44, "#FFFFFF", a=al, align="center", stroke=8, stroke_color="#111111")
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def chunk(args):
    k, f0, f1 = args
    out = BUILD / f"tc_{k:02d}.mp4"
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
        (BUILD / "tc.txt").write_text("".join(f"file '{x.name}'\n" for x in chs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(BUILD / "tc.txt"), "-c", "copy",
                        str(BUILD / "Test_mo_dau.mp4")], check=True)
        for x in chs:
            x.unlink()
        (BUILD / "tc.txt").unlink()
        print("xong")
