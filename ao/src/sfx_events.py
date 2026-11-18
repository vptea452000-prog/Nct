"""Âm thanh Tập 3: Kim khâu và áo da — giọng ú ớ chuẩn (tools/babble.py) + hiệu ứng hoạt hình.
Quy tắc: không đặt chuỗi tiếng gõ/tích tắc dưới lời thoại."""
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools")); sys.path.insert(0, str(ROOT / "src"))
import sfx_lib as S  # noqa
from sfx_lib import ev, rng, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa
from babble import babble
from beats import T, DUR

S.configure(ROOT, DUR)

# ---------------------------------------------------------------- lời ú ớ
for i, (name, (a, b, row)) in enumerate(T.items()):
    spk, kind, txt, emo = row[3], row[4], row[5], row[6]
    if spk and kind != "think" and txt:
        st, en = a + 0.12, b - 0.45
        if False:
            st = a + 0.32
        d = max(0.35, en - st)
        x = babble(spk, d, emo, kind, seed=100 + i)
        g = -3 if kind == "shout" else (-12 if kind == "whisper" else -6)
        if name == "check":
            x = lp(x, 1500); g += 2
        ev(st, x, g, -0.25 if spk == "gam" else 0.25)


def soft(d, f0, f1, tau=0.12):
    return norm(S.sweep(f0, f1, d) * env_exp(int(d * SR), tau))


def boing(f0=700, f1=300, d=0.35):
    tt = t_(d)
    f = f0 + (f1 - f0) * tt / d
    x = np.sin(2 * np.pi * np.cumsum(f * (1 + 0.15 * np.sin(2 * np.pi * 18 * tt))) / SR) * np.exp(-tt / 0.15)
    return norm(x)


def bonk():
    d = 0.35; n = int(d * SR); tt = t_(d)
    x = np.sin(2 * np.pi * 620 * tt) * np.exp(-tt / 0.06) + 0.6 * np.sin(2 * np.pi * 930 * tt) * np.exp(-tt / 0.04) + lp(noise(d), 1500) * np.exp(-tt / 0.01)
    return norm(x)


def thud():
    d = 0.4; n = int(d * SR)
    return norm(lp(noise(d), 400) * env_exp(n, 0.05) + S.sweep(100, 45, d) * env_exp(n, 0.08))


def snort():
    d = 0.5; n = int(d * SR)
    return norm(bp(noise(d), 300, 1500) * env_ad(n, 0.04, 0.15) * (1 + 0.6 * np.sin(2 * np.pi * 35 * t_(d))))


def oink(pitch=1.0):
    d = 0.35; tt = t_(d)
    f = 320 * pitch * (1 - 0.3 * tt / d)
    src = sum(np.sin(k * 2 * np.pi * np.cumsum(f) / SR) / k for k in range(1, 8))
    return norm(bp(src * env_ad(int(d * SR), 0.03, 0.12), 300, 2500))


def skid():
    d = 0.8; n = int(d * SR); tt = t_(d)
    f = 1800 - 900 * tt / d
    return norm((np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + bp(noise(d), 1500, 5000) * 0.8) * env_ad(n, 0.02, 0.5))


def birds(d):
    out = np.zeros(int(d * SR))
    for k in range(int(d * 1.5)):
        L = int(0.3 * SR); st = int(rng.uniform(0, d - 0.4) * SR)
        f = 2800 + 900 * np.sin(2 * np.pi * 10 * t_(0.3)) + rng.uniform(-300, 300)
        out[st:st + L] += np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(L, 0.02, 0.1) * 0.6
    return norm(out)


def stream(d):
    n = int(d * SR)
    x = bp(noise(d), 400, 3000) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.5 * t_(d)))
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.5 * SR), (n - np.arange(n)) / (0.5 * SR))))


def wind(d):
    n = int(d * SR)
    x = bp(noise(d), 200, 1000) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t_(d)))
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.5 * SR), (n - np.arange(n)) / (0.6 * SR))))


def fire_soft(d):
    n = int(d * SR)
    x = lp(noise(d), 350) * 0.8 + bp((rng.random(n) < 0.0004) * rng.normal(0, 1, n), 800, 3000) * 0.25
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.3 * SR), (n - np.arange(n)) / (0.4 * SR))))


def crack():
    d = 0.3; n = int(d * SR)
    return norm(bp(noise(d), 800, 5000) * env_exp(n, 0.02) + lp(noise(d), 600) * env_exp(n, 0.05))


def splash():
    d = 0.7; n = int(d * SR)
    return norm(bp(noise(d), 500, 4000) * env_ad(n, 0.01, 0.25) + S.sweep(300, 900, d) * env_exp(n, 0.06) * 0.3)


def ding_soft():
    d = 0.7; tt = t_(d)
    return norm(sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.25) / (i + 1) for i, f in enumerate((1320, 1980, 2640))))


def whoosh(d=0.4, lo=300, hi=2500):
    return S.s_whoosh(d, lo, hi, 0.5)


def bt(n):
    return T[n][0], T[n][1]


def zip_(d=0.25):
    return norm(bp(noise(d), 1500, 6000) * env_ad(int(d * SR), 0.02, d * 0.6))


def pluck():
    d = 0.5; tt = t_(d)
    return norm(np.sin(2 * np.pi * 220 * tt) * np.exp(-tt / 0.12) + lp(noise(d), 2000) * np.exp(-tt / 0.01) * 0.5)


def snore(d):
    tt = t_(d)
    return norm(lp(noise(d), 260) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.7 * tt)) ** 2)


def sizzle(d):
    n = int(d * SR)
    return norm(hp(noise(d), 2500) * env_ad(n, 0.05, d * 0.7) * 0.6)


def storm(d):
    n = int(d * SR)
    x = bp(noise(d), 150, 1200) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.33 * t_(d)))
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.5 * SR), (n - np.arange(n)) / (0.6 * SR))))


# CẢNH 1
a = T["open"][0]; ev(a, wind(T["grind"][0] - a), -18)
ev(a + 0.3, S.s_impact(), -10); ev(a + 0.6, S.s_impact(), -8)
a, b = bt("inside"); ev(a, fire_soft(T["grind"][0] - a), -22)
a, b = bt("warm2"); ev(a + 0.1, ding_soft(), -16)
a, b = bt("gust"); ev(a + 0.2, whoosh(1.0, 150, 2500), -4); ev(a + 0.7, zip_(0.3), -12)
for k in range(5):
    ev(a + 0.8 + k * 0.22, norm(bp(noise(0.15), 300, 1500) * env_ad(int(0.15 * SR), 0.01, 0.1)), -16, 0.3)
ev(a + 1.9, soft(0.4, 700, 400), -14, 0.4)
a, b = bt("naked"); ev(a + 0.2, soft(1.2, 520, 480, 0.6), -24)
# CẢNH 2
a = T["grind"][0]; ev(a, fire_soft(T["montage"][0] - a), -24)
a, b = bt("grind")
for k in range(4):
    ev(a + 0.15 + k * 0.55, whoosh(0.4, 1500, 5000), -14)
ev(a + 2.0, ding_soft(), -12)
a, b = bt("drill"); ev(a + 0.2, norm(lp(noise(1.4), 1200) * (0.6 + 0.4 * np.sin(2 * np.pi * 8 * t_(1.4)))), -18)
a, b = bt("hole"); ev(a + 0.3, ding_soft(), -10)
a, b = bt("thread"); ev(a + 0.2, whoosh(0.5, 800, 3000), -16); ev(a + 1.8, S.s_pop(1.2), -12)
a, b = bt("stitch")
for k in range(3):
    ev(a + k * 0.6 + 0.25, thud(), -10); ev(a + k * 0.6 + 0.35, whoosh(0.2, 1500, 4000), -18)
ev(a + 1.9, ding_soft(), -14)
# CẢNH 3
a = T["montage"][0]; ev(a, wind(T["storm"][0] - a), -22)
a, b = bt("montage")
for k in range(4):
    ev(a + k * 0.8, S.s_pop(1.0 + k * 0.12), -10); ev(a + k * 0.8 + 0.4, thud(), -16)
a, b = bt("wear"); ev(a + 0.2, whoosh(0.4, 400, 3000), -10); ev(a + 0.6, zip_(0.25), -14)
a, b = bt("nofly"); ev(a, whoosh(1.4, 150, 2000), -10); ev(a + 1.2, soft(0.6, 300, 200, 0.3), -18)
a, b = bt("fit1"); ev(a + 0.4, S.s_pop(1.0), -14)
a, b = bt("sack")
for k in range(5):
    ev(a + k * 0.16, thud(), -18, -0.4)
a, b = bt("sleeve2"); ev(a + 0.1, boing(600, 1100, 0.25), -12)
a, b = bt("fight")
for k in range(5):
    ev(a + 0.3 + k * 0.45, whoosh(0.2, 500, 2500), -16, -0.3)
a, b = bt("grab"); ev(a + 0.2, whoosh(0.25, 600, 3500), -8)
a, b = bt("useless"); ev(a + 0.1, S.s_impact(), -12)
a, b = bt("flick"); ev(a + 0.15, pluck(), -8); ev(a + 0.25, whoosh(0.6, 800, 4000), -10); ev(a + 1.3, ding_soft(), -12)
a, b = bt("long"); ev(a + 0.3, soft(1.0, 500, 250, 0.5), -16)
# CẢNH 4
a = T["storm"][0]; ev(a, storm(T["find"][0] - a), -14); ev(a, fire_soft(T["find"][0] - a), -22)
for n_, per in (("storm", 0.85), ("slip", 0.62)):
    a, b = bt(n_)
    k = 0
    while a + k * per < b:
        ev(a + k * per + 0.25, whoosh(0.3, 300, 1200), -16); ev(a + k * per + 0.55, zip_(0.15), -18)
        k += 1
a, b = bt("stay"); ev(a + 1.8, whoosh(0.4, 300, 1200), -14)
a, b = bt("burn"); ev(a + 0.1, whoosh(0.6, 150, 2500), -6); ev(a + 0.7, sizzle(1.0), -8); ev(a + 1.3, whoosh(0.3, 500, 2500), -12)
ev(a + 1.5, boing(500, 300, 0.4), -12)
a, b = bt("snore"); ev(a + 0.1, snore(b - a + T["sneak"][1] - T["sneak"][0] - 0.2), -12, -0.4)
a, b = bt("sneak")
for k in range(5):
    ev(a + 0.2 + k * 0.4, soft(0.12, 400, 300), -22)
a, b = bt("stuck"); ev(a + 0.5, S.s_pop(0.8), -8)
for k in range(6):
    ev(a + 1.0 + k * 0.25, norm(bp(noise(0.12), 200, 1200) * env_ad(int(0.12 * SR), 0.01, 0.08)), -14)
a, b = bt("wake"); ev(a + 0.05, boing(900, 1500, 0.2), -10)
# CẢNH 5
a = T["find"][0]; ev(a, wind(T["itch"][0] - a), -24)
a, b = bt("find"); ev(a + 1.2, ding_soft(), -8)
a, b = bt("sew")
for k in range(3):
    ev(a + 0.4 + k * 0.7, thud(), -10)
a, b = bt("done"); ev(a + 0.1, S.s_impact(), -12)
a, b = bt("tail")
for k in range(6):
    ev(a + 0.8 + k * 0.35, norm(lp(noise(0.3), 700) * env_ad(int(0.3 * SR), 0.05, 0.2)), -18)
ev(a + 1.6, norm(bp(noise(0.3), 400, 2000) * env_ad(int(0.3 * SR), 0.02, 0.2)), -16, 0.4)
a, b = bt("fix")
for k in range(6):
    ev(a + 0.2 + k * 0.4, S.s_pop(1.0 + k * 0.08), -14)
a, b = bt("snow"); ev(a + 1.3, ding_soft(), -12)
a, b = bt("sack2")
for k in range(4):
    ev(a + k * 0.52, boing(400, 700, 0.25), -16, -0.3)
a, b = bt("allmine"); ev(a + 0.1, S.s_impact(), -12)
a, b = bt("trophy")
for i in range(3):
    ev(a + 0.6 + i * 0.4, S.s_pop(1.0 + i * 0.15), -10)
# CẢNH 6
a, b = bt("itch")
for k in range(10):
    ev(a + 0.1 + k * 0.22, norm(bp(noise(0.18), 800, 3000) * env_ad(int(0.18 * SR), 0.03, 0.12)), -20, -0.3)
a, b = bt("home")
for k in range(5):
    ev(a + 0.2 + k * 0.45, boing(450, 750, 0.22), -16, -0.3)
a, b = bt("snap"); ev(a + 0.9, pluck(), -4); ev(a + 0.92, crack(), -10)
a, b = bt("twist"); ev(a + 0.2, norm(lp(noise(0.9), 900)), -22); ev(a + 1.2, ding_soft(), -10)
a, b = bt("idea"); ev(a + 1.2, ding_soft(), -10)
a, b = bt("useless2"); ev(a, soft(0.25, 600, 300), -18)
a, b = bt("card"); ev(a + 0.2, S.s_impact(), -12); ev(a + 0.5, ding_soft(), -14)

if __name__ == "__main__":
    import subprocess
    B = ROOT / "build"
    va = ROOT / "audio/voice.mp3"
    if not va.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(DUR), "-c:a", "libmp3lame", str(va)], check=True)
    S.EVENTS[:] = [(t, x, g + 4, p) for t, x, g, p in S.EVENTS]
    S.export(B / "Ao_v1_nosfx.mp4", B / "Ao_v1.mp4", pre_gain_db=float(sys.argv[1]) if len(sys.argv) > 1 else 1.1, limit=0.70)
