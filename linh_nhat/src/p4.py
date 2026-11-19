"""Phần 4 (voice_4, 48 s): cập cảng → thành phố cháy đen → hàng người chờ khẩu phần → chia tay Kenji ở ga →
đi bộ về làng → cái vịnh, con thuyền → mẹ tóc bạc ở đầu ngõ → trao dải vải → "Vào ăn cơm đi con." → kết.
  python3 src/p4.py sheet | preview <t…> | full
"""
import math, subprocess, sys, json
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import p1, p2, p3  # noqa
from p1 import (skia, Image, text, Stick, draw_stick, P, fo, oval, clamp, lerp, ease_out, ease_in_out, back_out, INK, LOOKS,
                Cam, grad, noise1, W, H, FPS, GROUND, head_xy, ease_shot, lerp_col, lane_bg, cloth_band, train)  # noqa
from p2 import ship, island, bowl  # noqa
import test_open2 as T2  # noqa

PART = ROOT / "p4"
BUILD = PART / "build"
ALIGN = json.load(open(ROOT / "audio" / "voice_4_align.json"))
DUR = 48.06
p1.ALIGN = ALIGN
LOOKS["civ0"] = dict(LOOKS["chief"], civ=("#6A6A6A", "#525252"), hair="short", hair_col="#3A3A3A", goatee=False)
LOOKS["civ1"] = dict(LOOKS["woman2"], civ=("#7A6A5A", "#5E5246"))
LOOKS["civ2"] = dict(LOOKS["recruit2"], civ=("#5A5A6A", "#46465A"), headband=None)


def YOU(c, x, y, s, t, **kw):
    kw.setdefault("uniform", True); kw.setdefault("cap", "soldier"); kw.setdefault("thin", 0.8)
    draw_stick(c, Stick("you", x, y, s, t, **kw))


def ruins_bg(c, K, t):
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#8A8A86", "#C8C4BA")
    K.end(c)
    K.layer(c, 0.45)
    for k in range(-6, 16):
        x = k * 170 + 40 * math.sin(k * 1.7)
        h = 220 + 140 * abs(math.sin(k * 2.3))
        c.drawRect(skia.Rect.MakeXYWH(x, GROUND - h, 34, h), P("#2A2622"))
        if k % 3 == 0:
            c.drawRect(skia.Rect.MakeXYWH(x - 40, GROUND - h * 0.6, 120, 20), P("#2A2622"))
    for k in range(5):
        q = (t * 0.1 + k / 5) % 1
        sp = P("#6A6660", 90 * (1 - q)); sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 20))
        c.drawCircle(200 + k * 400, 500 - q * 300, 60 + q * 80, sp)
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P("#5A564E"))
    c.drawLine(-3000, GROUND, W + 3000, GROUND, P(INK, stroke=6))
    for k in range(-6, 16):
        c.drawCircle(k * 230, GROUND + 30 + (k % 3) * 20, 14 + (k % 4) * 6, P("#3A3630"))
    K.end(c)


def c_port(c, t):                      # 0–3,12  gần một năm sau, tàu cập cảng Nhật Bản
    q = ease_shot(t, 0, 3.12)
    K = Cam(lerp(800, 1000, q), 540, lerp(1.05, 1.15, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#9AA4A8", "#D8D8D0")
    K.end(c)
    K.layer(c, 0.6)
    T2.wave_band(c, 700, t, "#6A7E88", amp=5, x0=-3000, x1=W + 3000)
    ship(c, 700 - 120 * (1 - q), 760, 0.8, t)
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(1100, 800, 3000, 400), P("#7A6E5A"))
    c.drawLine(1100, 800, 4000, 800, P(INK, stroke=6))
    for k in range(6):
        c.drawLine(1150 + k * 160, 800, 1150 + k * 160, 1100, P("#4A4236", stroke=14))
    for i in range(3):
        YOU(c, 1250 + i * 170 + q * 60, 800, 0.7, t + i, face=1, walk=t * 4 + i, pack=True, eyes="dot", mouth="flat") if i == 1 else \
            draw_stick(c, Stick(f"recruit{i}", 1250 + i * 170 + q * 60, 800, 0.7, t + i, face=1, walk=t * 4 + i, uniform=True, cap="soldier",
                                thin=0.8, pack=True))
    K.end(c)


def c_ruins(c, t):                     # 3,12–7,7  đất nước không còn như ngày ra đi · những dãy cột cháy đen
    q = ease_shot(t, 3.12, 7.7)
    K = Cam(lerp(600, 1300, q), 540, 1.1, t=t)
    ruins_bg(c, K, t)
    K.layer(c, 1.0)
    YOU(c, 500 + (t - 3.12) * 170, GROUND, 0.9, t, face=1, walk=(t - 3.12) * 4.5, pack=True, eyes="dot", look=(0.6, -0.4), mouth="flat")
    K.end(c)


def c_queue(c, t):                     # 7,7–11,75  xếp hàng chờ khẩu phần, gầy gò như lính trên đảo năm nào
    q = ease_shot(t, 7.7, 11.75)
    K = Cam(lerp(1100, 900, q), 540, 1.15, t=t)
    ruins_bg(c, K, t)
    K.layer(c, 1.0)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(260, 720, 260, 140)) or skia.Path(), "#7A6A50", ow=6)
    for i, who in enumerate(["civ0", "civ1", "mother", "civ2", "woman0", "civ0", "woman3"]):
        x = 640 + i * 190
        draw_stick(c, Stick(who, x, GROUND, 0.85, t + i * 0.4, face=-1, thin=1.0, hand_f=(80, 40), eyes="dot", mouth="flat", idle=0.6))
        bowl(c, x - 0.85 * 110, GROUND - 0.85 * 330, 0.14, mode="gruel")
    YOU(c, lerp(2100, 1500, q), GROUND + 120, 0.95, t, face=-1, walk=t * 4, pack=True, eyes="sad", look=(0, -0.2), mouth="flat")
    K.end(c)


def c_station(c, t):                   # 11,75–19,44  chia tay ở ga · ôm thật chặt · quay đi vẫy tay, không ngoái lại · giống hệt bạn ngày xưa
    lt = t - 11.75
    K = Cam(lerp(980, 1060, ease_shot(t, 11.75, 18.12)), 540, lerp(1.3, 1.15, ease_shot(t, 11.75, 18.12)), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#A8B0B4", "#E2E0D8")
    K.end(c)
    K.layer(c, 0.5)
    for k in range(-1, 6):
        c.drawLine(k * 480, 860, k * 480, 280, P("#5A5A5A", stroke=16))
    c.drawRect(skia.Rect.MakeXYWH(-1500, 260, 4800, 40), P("#4A4A4A"))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P("#9A9488"))
    hug = 1.5 < lt < 3.6
    if lt < 1.9:       # đứng đối diện
        YOU(c, 900, GROUND, 1.0, t, face=1, eyes="dot", look=(1, 0), mouth="flat")
        draw_stick(c, Stick("kenji", 1120, GROUND, 1.05, t, face=-1, uniform=True, cap="soldier", thin=0.8, eyes="dot", look=(-1, 0), mouth="smile"))
    elif hug:          # ôm thật chặt
        YOU(c, 960, GROUND, 1.0, t, face=1, hand_f=(150, -20), hand_b=(140, 0), eyes="closed", mouth="flat", lean=6)
        draw_stick(c, Stick("kenji", 1040, GROUND, 1.05, t, face=-1, uniform=True, cap="soldier", thin=0.8, hand_f=(160, -30), hand_b=(150, -10),
                            eyes="closed", mouth="smile", lean=6))
    else:              # quay đi, vừa đi vừa vẫy tay, không ngoái lại
        k = lt - 3.6
        kx = 1060 + k * 200
        YOU(c, 940, GROUND, 1.0, t, face=1, eyes="dot", look=(1, 0), mouth="flat", tears=0.6 if lt > 5.2 else 0.0)
        draw_stick(c, Stick("kenji", kx, GROUND, 1.05, t, face=1, uniform=True, cap="soldier", thin=0.8, walk=k * 4.2,
                            hand_b=(-120, -200 + 20 * math.sin(k * 9)), eyes="dot", mouth="smile"))
    K.end(c)
    if lt > 6.4:      # hồi ức mờ: chính bạn vẫy tay trên tàu năm xưa
        a = clamp((lt - 6.4) / 0.3) * 0.5
        c.saveLayerAlpha(None, int(255 * a))
        p1.c_station(c, 37.0 + (lt - 6.4) * 0.6)
        c.restore()


def c_walk(c, t):                      # 19,44–21,41  đi bộ suốt buổi chiều về làng chài
    q = ease_shot(t, 19.44, 21.41)
    K = Cam(lerp(800, 1100, q), 540, 1.05, t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#E8946A", "#FAD9B0")
    K.end(c)
    K.layer(c, 0.4)
    T2.wave_band(c, 640, t, "#8AA4B0", amp=4, x0=-3000, x1=W + 3000)
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P("#C8B48A"))
    c.drawLine(-3000, GROUND, W + 3000, GROUND, P(INK, stroke=6))
    x = 600 + (t - 19.44) * 200
    sh = skia.Path(); sh.moveTo(x - 30, GROUND); sh.lineTo(x - 360, GROUND + 60); sh.lineTo(x - 330, GROUND + 80); sh.lineTo(x + 10, GROUND + 10); sh.close()
    c.drawPath(sh, P("#000000", 50))
    YOU(c, x, GROUND, 0.95, t, face=1, walk=(t - 19.44) * 4.5, pack=True, eyes="dot", mouth="flat")
    K.end(c)


def c_bay(c, t):                       # 21,41–24,43  cái vịnh vẫn ở đó · con thuyền của cha vẫn nằm trên bãi cát
    if t < 22.43:
        p1.c_bay(c, 6.6 + (t - 21.41) * 2.0)
        return
    q = ease_shot(t, 22.43, 24.43)
    K = Cam(lerp(900, 980, q), 620, lerp(1.4, 1.55, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#E8946A", "#FAD9B0")
    K.end(c)
    K.layer(c, 0.5)
    T2.wave_band(c, 660, t, "#8AA4B0", amp=4, x0=-3000, x1=W + 3000)
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, 760, W + 6000, 900), P("#E0CCA0"))
    c.save(); c.translate(960, 820); c.rotate(-4)
    T2.boat(c, 0, 0, 0.8, 0.0)
    c.restore()
    c.drawLine(1180, 790, 1380, 880, P(INK, stroke=4))
    K.end(c)


def c_mother(c, t):                    # 24,43–30,41  đầu ngõ, người phụ nữ tóc bạc đứng đó như chưa từng rời đi
    lt = t - 24.43
    q = ease_shot(t, 24.43, 30.41)
    K = Cam(lerp(1150, 900, q), lerp(540, 480, q), lerp(1.0, 1.55, q), t=t)
    lane_bg(c, K, t, sun=0.85)
    K.layer(c, 1.0)
    draw_stick(c, Stick("mother_old", 820, GROUND, 1.0, t, face=1, hand_f=(40, 150), hand_b=(10, 160), eyes="dot", look=(1, 0),
                        mouth="flat", idle=0.5))
    yx = lerp(1900, 1250, ease_out(clamp(lt / 4.5)))
    YOU(c, yx, GROUND, 1.0, t, face=-1, walk=(1900 - yx) / 70 * math.pi if lt < 4.4 else None, pack=True, eyes="dot", mouth="flat")
    K.end(c)


def c_give(c, t):                      # 30,41–33,22  tháo dải vải sờn rách, đặt vào tay mẹ
    lt = t - 30.41
    q = ease_shot(t, 30.41, 33.22)
    K = Cam(lerp(1020, 1040, q), lerp(560, 540, q), lerp(2.0, 2.3, q), t=t)
    lane_bg(c, K, t, sun=0.9)
    K.layer(c, 1.0)
    give = ease_in_out(clamp((lt - 0.8) / 1.4))
    draw_stick(c, Stick("mother_old", 860, GROUND, 1.0, t, face=1, hand_f=(lerp(60, 150, give), lerp(150, 60, give)), hand_b=(lerp(30, 130, give), lerp(160, 70, give)),
                        eyes="dot", look=(1, 0.5), mouth="flat"))
    YOU(c, 1200, GROUND, 1.0, t, face=-1, hand_f=(lerp(30, 140, give), lerp(130, 60, give)), hand_b=(lerp(0, 120, give), lerp(130, 70, give)),
        eyes="dot", look=(-1, 0.5), mouth="flat", belt=lt < 0.8)
    if lt >= 0.8:
        bx = lerp(1110, 1040, give)
        cloth_band(c, bx - 80, GROUND - 300 + 10 * (1 - give), bx + 80, GROUND - 300, dots=24)
    K.end(c)


def c_look(c, t):                      # 33,22–34,33  bà nhìn nó rất lâu
    q = ease_shot(t, 33.22, 34.33)
    K = Cam(880, lerp(430, 425, q), lerp(2.6, 2.8, q), t=t)
    lane_bg(c, K, t, sun=0.9)
    K.layer(c, 1.0)
    draw_stick(c, Stick("mother_old", 860, GROUND, 1.0, t, face=1, hand_f=(150, 60), hand_b=(130, 70), eyes="dot", look=(0.6, 1), mouth="flat",
                        tears=1.0, head_tilt=10, idle=0.3))
    cloth_band(c, 960, GROUND - 300, 1120, GROUND - 300, dots=24)
    K.end(c)


def c_rice(c, t):                      # 34,33–36,26  "Vào ăn cơm đi con."
    lt = t - 34.33
    if lt < 1.0:
        K = Cam(900, 440, 2.4, t=t)
        lane_bg(c, K, t, sun=0.9)
        K.layer(c, 1.0)
        draw_stick(c, Stick("mother_old", 860, GROUND, 1.0, t, face=1, hand_f=(150, 60), hand_b=(130, 70), eyes="happy", mouth="smile", tears=0.5))
        K.end(c)
        return
    q = ease_shot(t, 35.33, 36.26)
    K = Cam(760, lerp(650, 600, q), lerp(2.4, 2.1, q), t=t)
    p1.house_in(c, K, t, night=False, lamp=False)
    K.layer(c, 1.0)
    fo(c, skia.Path().addRect(skia.Rect.MakeXYWH(620, 760, 280, 100)) or skia.Path(), "#8A7A6A", ow=6)
    pot = skia.Path(); pot.moveTo(660, 640); pot.lineTo(860, 640); pot.quadTo(850, 740, 760, 745); pot.quadTo(670, 740, 660, 640); pot.close()
    fo(c, pot, "#3A3A3A", ow=6)
    fo(c, oval(760, 640, 110, 22), "#2A2A2A", ow=5)
    for k in range(5):
        qq = (t * 0.6 + k / 5) % 1
        stp = P("#FFFFFF", 180 * (1 - qq)); stp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
        c.drawCircle(740 + 30 * math.sin(qq * 6 + k), 610 - qq * 300, 24 + qq * 34, stp)
    K.end(c)


def c_many(c, t):                      # 36,26–40,68  hàng triệu thanh niên đã ra đi · rất nhiều người không trở về
    lt = t - 36.26
    q = ease_shot(t, 36.26, 40.68)
    K = Cam(960, lerp(560, 500, q), lerp(1.2, 0.9, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#C88A6A", "#F0D2AA")
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, 760, W + 6000, 900), P("#8A7A5A"))
    for i in range(60):
        row = i // 15
        x = -300 + (i % 15) * 180 + row * 60
        y = 780 + row * 70
        fade = 1.0 if lt < 2.3 else clamp(1 - (lt - 2.3) / 1.6 * (1 + (i * 37 % 10) / 3))
        if (i * 13) % 9 == 0:
            fade = 1.0                       # vài người còn lại
        if fade <= 0.02:
            continue
        draw_stick(c, Stick(f"recruit{i % 4}", x - lt * 30, y, 0.45 + row * 0.05, t + i * 0.2, face=-1, uniform=True, cap="soldier",
                            walk=t * 3 + i, alpha=fade, idle=0.5))
    K.end(c)


def c_islands(c, t):                   # 40,68–44,31  có người nằm lại trên những hòn đảo ít ai còn nhớ tên
    q = ease_shot(t, 40.68, 44.31)
    K = Cam(lerp(800, 1100, q), 560, 1.0, t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#5A6E8A", "#E8B88A")
    K.end(c)
    K.layer(c, 0.6)
    T2.wave_band(c, 640, t * 0.5, "#4A6278", amp=4, x0=-3000, x1=W + 3000)
    for i, (x, s) in enumerate([(300, 0.25), (900, 0.4), (1500, 0.3), (2000, 0.2)]):
        c.save(); c.translate(x, 650); c.scale(s, s)
        m = skia.Path(); m.moveTo(-700, 40); m.quadTo(-300, -220, 0, -300); m.quadTo(300, -220, 700, 40); m.close()
        c.drawPath(m, P("#2A3A3A"))
        c.restore()
    K.end(c)
    K.layer(c, 1.0)
    T2.wave_band(c, 820, t * 0.6, "#3A5266", amp=8, x0=-3000, x1=W + 3000)
    K.end(c)


def c_question(c, t):                  # 44,31–48,06  nếu là bạn, bạn sẽ mang theo điều gì về nhà?
    lt = t - 44.31
    grad(c, skia.Rect.MakeWH(W, H), "#1A1612", "#0A0806")
    c.save(); c.translate(W / 2, 640); c.rotate(-2)
    a = clamp(lt / 0.8)
    c.saveLayerAlpha(None, int(255 * a))
    cloth_band(c, -420, 0, 420, 0, dots=40, w=60)
    c.restore()
    c.restore()
    if lt > 1.0:
        al = 255 * clamp((lt - 1.0) / 0.6) * clamp((DUR - t) / 0.6)
        text(c, "Nếu là bạn,", W / 2, 330, "xbold", 70, "#F2E8D0", a=al, align="center")
        text(c, "bạn sẽ mang theo điều gì về nhà?", W / 2, 430, "xbold", 70, "#F2E8D0", a=al, align="center")


SHOTS = [(0.0, 3.12, c_port), (3.12, 7.70, c_ruins), (7.70, 11.75, c_queue), (11.75, 19.44, c_station), (19.44, 21.41, c_walk),
         (21.41, 24.43, c_bay), (24.43, 30.41, c_mother), (30.41, 33.22, c_give), (33.22, 34.33, c_look), (34.33, 36.26, c_rice),
         (36.26, 40.68, c_many), (40.68, 44.31, c_islands), (44.31, DUR, c_question)]
FADE = {11.75, 19.44, 36.26, 44.31}


def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas(); c.clear(skia.ColorBLACK)
    for a, b, fn in SHOTS:
        if a <= t < b:
            c.save(); fn(c, t); c.restore()
            for f in FADE:
                if abs(t - f) < 0.3:
                    c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 255 * (1 - abs(t - f) / 0.3)))
            break
    if t < 44.31:
        p1.subtitle(c, t)
    if t > DUR - 0.8:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 255 * clamp((t - (DUR - 0.8)) / 0.8)))
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def chunk(args):
    k, f0, f1 = args
    out = BUILD / f"c_{k:02d}.mp4"
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    s = skia.Surface(W, H)
    for i in range(f0, f1):
        pr.stdin.write(frame(i / FPS, s).tobytes())
    pr.stdin.close(); pr.wait()
    return out


if __name__ == "__main__":
    BUILD.mkdir(parents=True, exist_ok=True)
    if sys.argv[1] == "preview":
        for ts in sys.argv[2:]:
            Image.fromarray(frame(float(ts))[..., :3]).save(BUILD / f"pv_{float(ts):05.2f}.png")
    elif sys.argv[1] == "sheet":
        ts = [a + (b - a) * 0.6 for a, b, _ in SHOTS]
        ims = [Image.fromarray(frame(x)[..., :3]).resize((480, 270)) for x in ts]
        sh = Image.new("RGB", (480 * 4, 270 * math.ceil(len(ims) / 4)))
        for i, im in enumerate(ims):
            sh.paste(im, ((i % 4) * 480, (i // 4) * 270))
        sh.save(BUILD / "sheet.png")
    else:
        nfr = int(DUR * FPS); step = math.ceil(nfr / 8)
        with Pool(4) as pool:
            chs = pool.map(chunk, [(k, f, min(nfr, f + step)) for k, f in enumerate(range(0, nfr, step))])
        (BUILD / "c.txt").write_text("".join(f"file '{x.name}'\n" for x in chs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(BUILD / "c.txt"), "-c", "copy",
                        str(BUILD / "P4_nosfx.mp4")], check=True)
        for x in chs:
            x.unlink()
        (BUILD / "c.txt").unlink()
        print("xong")
