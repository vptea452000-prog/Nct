"""Demo bộ khung nhân vật v2: 12,6 giây đầu Tập 2 (open → talk).
  python3 demo/demo.py preview 3.0 6.0 ...   → build/demo_pv_<t>.png
  python3 demo/demo.py full                  → build/Demo_rig_v2.mp4 (+ tiếng từ Giao_v1) và Demo_so_sanh.mp4
"""
import math, subprocess, sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT.parent / "tools"))
import skia  # noqa
from PIL import Image  # noqa
from lib import W, H, FPS, draw_grain, paint, prog, clamp, lerp  # noqa
import scenes as S  # noqa
from kit import cam, shake, sfx_word, pop  # noqa
from beats import T  # noqa
from rig import Pose, draw_char, draw_boar, ease_out, ease_in_out, noise1  # noqa
from lipsync import LipSync  # noqa

BUILD = ROOT / "build"
END = T["talk"][1]
LS = LipSync(T, BUILD / "lipsync_cache.npz", starts={"bounce": 0.32})
GS = 1.2  # tỉ lệ Gầm


def beat(n):
    return T[n][0], T[n][1]


def scr(x, y, cx, cy, z):
    return W / 2 + z * (x - cx), H / 2 + z * (y - cy)


def gam_mouth(x, y, s=GS, crouch=0.0):
    return x + 10 * s, y - (540 - crouch * 60) * s


def idle(t, seed=0.0):
    return dict(head_tilt=3 * noise1(t * 0.8, seed), head_dx=3 * noise1(t, seed + 2))


def bubble(c, n, x, y, mouth, t, d=0.1):
    S.say(c, n, x, y, (mouth[0], mouth[1]), t, d)


def bg(c, t):
    c.save(); c.translate(540, 0); c.scale(1.3, 1); c.translate(-540, 0)
    S.stream_bg(c, t, "morning")
    c.restore()


def dirt(c, x, y, t, k0=0):
    for k in range(6):
        ph = (t * 2.2 + k / 6) % 1
        c.drawCircle(x + 60 * ph + 10 * math.sin(k * 3), y - 120 * ph * (1 - ph) * 2.4, 9 * (1 - ph) + 3, paint("#6E5A3A", 220))


# ---------------------------------------------------------------- cảnh
def sc_open(c, t):
    a, b = beat("open"); ta = t - a
    z = lerp(0.95, 1.08, ease_in_out(clamp(ta / (b - a))))
    c.save(); cam(c, 540, 1050, z)
    bg(c, t)
    draw_boar(c, 700, 1230, 0.9, t, face=1, root=1.0)
    dirt(c, 950, 1225, t)
    # Gầm thò đầu lên khỏi bụi, mắt đảo
    up = ease_out(clamp((ta - 1.2) / 0.4))
    look = (math.sin(ta * 5) if ta > 1.6 else 1.0, -0.2)
    draw_char(c, Pose("gam", 230, 1290 + 300 * (1 - up), GS, t, face=1, crouch=1, eyes="open", look=look, brow=0.5, mouth="flat", **idle(t)))
    S.bush(c, 220, 1250, 1.1)
    c.restore()
    S.kinetic(c, "TẬP 2", W / 2, 420, t, a + 0.3, size=70, per=0.04)
    S.kinetic(c, "CÂY GIÁO", W / 2, 560, t, a + 0.6, size=140, color="#F4C430", per=0.06)


def sc_lunch(c, t):
    a, b = beat("lunch"); ta = t - a
    cx, cy, z = 330, 1000, 1.45
    c.save(); cam(c, cx, cy, z)
    bg(c, t)
    draw_boar(c, 760, 1230, 0.9, t, face=1, root=1.0)
    dirt(c, 1000, 1225, t)
    tk = LS.talk("gam", t)
    rub = math.sin(ta * 16)
    talking = tk > 0.02
    p = Pose("gam", 260, 1260, GS, t, face=1, crouch=1, lean=6, eyes="squint", look=(1, 0.1),
             brow=0.4 + 0.5 * max(0.0, math.sin(ta * 9)) * (ta > 1.6), brow_tilt=0.2,
             mouth="smirk" if talking or ta < 1.7 else "tongue", talk=tk * 0.6,
             hand_l=(70 + 12 * rub, 60), hand_r=(-40 - 12 * rub, 70), head_tilt=6 + 2 * math.sin(ta * 3), head_dy=4 * math.sin(ta * 16) * (ta < 0.7))
    draw_char(c, p)
    S.bush(c, 300, 1290, 1.25)
    c.restore()
    bubble(c, "lunch", 470, 360, scr(*gam_mouth(260, 1260, crouch=1), cx, cy, z), t)


def charge_pose(t):
    a, b = beat("charge"); ta = t - a
    if ta < 0.25:  # lấy đà
        k = ease_out(ta / 0.25)
        return dict(x=260 - 20 * k, y=1260, crouch=k, squash=1 - 0.15 * k, lean=-10 * k, hold_ang=-20 - 60 * k, feet_air=0, eyes="angry", mouth="grin")
    if ta < 0.8:  # bay
        p = (ta - 0.25) / 0.55
        e = ease_in_out(p)
        return dict(x=lerp(240, 600, e), y=1260 - 230 * math.sin(math.pi * p), crouch=0, squash=1 + 0.16 * math.sin(math.pi * p),
                    lean=lerp(-10, 18, e), hold_ang=lerp(-80, 115, p ** 2), feet_air=60 * math.sin(math.pi * p), eyes="angry", mouth="shout")
    k = ta - 0.8  # chạm
    return dict(x=600, y=1260, crouch=0.6 * math.exp(-k * 6), squash=1 - 0.2 * math.exp(-k * 8) * math.cos(k * 30), lean=18 * math.exp(-k * 5),
                hold_ang=115, feet_air=0, eyes="wide", mouth="o")


def sc_charge(c, t):
    a, b = beat("charge"); ta = t - a
    c.save(); cam(c, 540, 1050, 1.15)
    bg(c, t)
    draw_boar(c, 800, 1230, 0.9, t, face=1, root=1.0 if ta < 0.8 else 0.0,
              squash=1 - 0.12 * math.exp(-(ta - 0.8) * 10) if ta > 0.8 else 1.0)
    q = charge_pose(t)
    draw_char(c, Pose("gam", q["x"], q["y"], GS, t, face=1, squash=q["squash"], lean=q["lean"], crouch=q["crouch"], feet_air=q["feet_air"],
                      hand_r=(80, -90) if ta < 0.8 else (110, -20), hold="stick", hold_ang=q["hold_ang"], hold_len=430,
                      eyes=q["eyes"], brow=-0.3, brow_tilt=1.0, mouth=q["mouth"], lag=-q["lean"] * 2))
    c.restore()
    S.speedlines(c, t, 540, 900, 90 if 0.25 < ta < 0.85 else 0)
    c.save(); shake(c, t, a + 0.8, 20)
    sfx_word(c, "BỐP!", 760, 820, t, a + 0.8, size=150, dur=0.6)
    c.restore()


def sc_bounce(c, t):
    a, b = beat("bounce"); ta = t - a
    cx, cy, z = 600, 900, 1.6
    c.save(); shake(c, t, a + 0.2, 18)
    c.save(); cam(c, cx, cy, z)
    bg(c, t)
    draw_boar(c, 820, 1230, 0.9, t, face=1, root=0.0, turn_head=0.3 * clamp(ta))
    hit = a + 0.2
    if t < hit:
        ang = lerp(115, -35, ease_in_out(ta / 0.2))
    else:
        k = t - hit
        ang = -35 + 25 * math.exp(-k * 4) * math.sin(k * 14) + lerp(0, 20, clamp(k / 1.2))
    k = max(0.0, t - hit)
    hs = 1 - 0.28 * math.exp(-k * 7) * math.cos(k * 26) if t > hit else 1.0
    tk = LS.talk("gam", t)
    draw_char(c, Pose("gam", 600, 1260, GS, t, face=1, squash=1 - 0.12 * math.exp(-k * 9) if t > hit else 1.0,
                      lean=-14 * math.exp(-k * 1.4) * math.cos(k * 5) if t > hit else 4,
                      head_squash=hs, head_tilt=10 * math.sin(k * 4) * math.exp(-k * 0.8),
                      hand_r=(110, -20) if t < hit else (60, -110), hold="stick", hold_ang=ang, hold_len=430,
                      hand_l=(70, -250) if ta > 0.7 else None,
                      eyes="dizzy" if t > hit else "wide", brow=0.8, brow_tilt=-0.6, mouth="shout" if tk > 0.02 else "wavy",
                      talk=tk, sweat=1.0 if ta > 0.5 else 0.0, lag=20 * math.sin(k * 8) * math.exp(-k * 2)))
    S.stars(c, 600, 740, t, hit, r=120)
    c.restore(); c.restore()
    sfx_word(c, "CỐP!", 360, 600, t, hit, size=120, color="white", dur=0.6)
    bubble(c, "bounce", 760, 360, scr(*gam_mouth(600, 1260), cx, cy, z), t, d=0.3)


def sc_turn(c, t):
    a, b = beat("turn"); ta = t - a
    c.save(); cam(c, 800, 1050, 1.7)
    bg(c, t)
    tp = clamp((ta - 0.15) / 0.3)
    face = math.cos(math.pi * ease_in_out(tp))
    if abs(face) < 0.08:
        face = 0.08 if face >= 0 else -0.08
    sq = 1 - 0.1 * math.sin(math.pi * clamp(ta / 0.15)) if ta < 0.15 else 1 + 0.08 * math.exp(-(ta - 0.45) * 6) * (ta > 0.45)
    snort = ((ta - 0.4) * 1.6) if 0.4 < ta < 1.0 else 0.0
    draw_boar(c, 820, 1230, 0.95, t, face=face, mood="angry" if ta > 0.3 else "calm", paw=clamp((ta - 0.8) / 0.2), squash=sq, snort=snort)
    c.restore()
    sfx_word(c, "KHỊT!", 760, 560, t, a + 0.3, size=110, color="white", dur=0.7)
    sfx_word(c, "SỘT SỘT", 760, 1180, t, a + 0.9, size=80, color="#C9A06A", dur=0.8)


def sc_talk(c, t):
    a, b = beat("talk"); ta = t - a
    cx, cy, z = 540, 1050, 1.2
    c.save(); cam(c, cx, cy, z)
    bg(c, t)
    draw_boar(c, 800, 1230, 0.9, t, face=-1, mood="angry", paw=1.0, snort=(ta * 0.9) % 1 if (ta % 1.1) < 0.6 else 0.0)
    tk = LS.talk("gam", t)
    back = ease_in_out(clamp(ta / 2.0))
    x = 380 - 40 * back
    wave = math.sin(ta * 7)
    draw_char(c, Pose("gam", x, 1260, GS, t, face=1, lean=-6 * back, crouch=0.15 + 0.1 * math.sin(ta * 3),
                      hand_r=(110 + 15 * wave, -170 + 12 * wave), hand_l=(-70, 40), hold="stick", hold_side="l", hold_ang=-35, hold_len=430,
                      eyes="wide", look=(1, 0), brow=0.8, brow_tilt=-1.0, mouth="smile", talk=tk * 0.8, sweat=1.0,
                      head_tilt=-6 + 5 * math.sin(ta * 4), blush=0.2))
    c.restore()
    bubble(c, "talk", 470, 360, scr(*gam_mouth(x, 1260), cx, cy, z), t)


FN = {"open": sc_open, "lunch": sc_lunch, "charge": sc_charge, "bounce": sc_bounce, "turn": sc_turn, "talk": sc_talk}


def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas(); c.clear(skia.ColorBLACK)
    for n, f in FN.items():
        a, b = beat(n)
        if a <= t < b:
            c.save(); f(c, t); c.restore(); break
    draw_grain(c, 22)
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def chunk(args):
    k, f0, f1 = args
    out = BUILD / f"dchunk_{k:02d}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    s = skia.Surface(W, H)
    for i in range(f0, f1):
        p.stdin.write(frame(i / FPS, s).tobytes())
    p.stdin.close(); p.wait()
    return out


if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for ts in sys.argv[2:]:
            Image.fromarray(frame(float(ts))[..., :3]).save(BUILD / f"demo_pv_{float(ts):05.2f}.png")
    else:
        nfr = int(round(END * FPS)); step = math.ceil(nfr / 4)
        with Pool(4) as pool:
            chunks = pool.map(chunk, [(k, f, min(nfr, f + step)) for k, f in enumerate(range(0, nfr, step))])
        (BUILD / "dchunks.txt").write_text("".join(f"file '{c.name}'\n" for c in chunks))
        silent = BUILD / "demo_silent.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(BUILD / "dchunks.txt"), "-c", "copy", str(silent)], check=True)
        for c in chunks:
            c.unlink()
        (BUILD / "dchunks.txt").unlink()
        old = BUILD / "Giao_v1.mp4"
        new = BUILD / "Demo_rig_v2.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-t", f"{END}", "-i", str(old), "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{END}", str(new)], check=True)
        font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        lab = lambda s: f"drawtext=fontfile={font}:text='{s}':x=(w-tw)/2:y=40:fontsize=64:fontcolor=white:borderw=6:bordercolor=black"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-t", f"{END}", "-i", str(old), "-i", str(new), "-filter_complex",
                        f"[0:v]trim=0:{END},setpts=PTS-STARTPTS,scale=540:960,{lab('CŨ')}[l];[1:v]scale=540:960,{lab('MỚI')}[r];[l][r]hstack=inputs=2[v]",
                        "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                        str(BUILD / "Demo_so_sanh.mp4")], check=True)
        silent.unlink()
        print("xong")
