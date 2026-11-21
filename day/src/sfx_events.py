"""Âm thanh Tập 4: Dây thừng — giọng ú ớ chuẩn (tools/babble.py) + hiệu ứng hoạt hình.
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
        if name == "worm2":
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


def creak(d=0.6):
    tt = t_(d)
    f = 180 + 60 * np.sin(2 * np.pi * 3 * tt)
    return norm(bp(np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + 0.5 * np.sin(2 * np.pi * 30 * tt)), 150, 1500) * env_ad(int(d * SR), 0.05, d * 0.6))


def log_thud(p=1.0):
    d = 0.35; n = int(d * SR); tt = t_(d)
    return norm(lp(noise(d), 700) * env_exp(n, 0.04) + np.sin(2 * np.pi * 160 * p * tt) * np.exp(-tt / 0.06) * 0.6)


def twang():
    d = 0.9; tt = t_(d)
    return norm(sum(np.sin(2 * np.pi * 196 * k * tt) * np.exp(-tt * (3 + k)) / k for k in range(1, 6)) * (1 + 0.3 * np.sin(2 * np.pi * 6 * tt)))


# CẢNH 1
a = T["open"][0]; ev(a, birds(T["bark"][0] - a), -20)
ev(a + 0.3, S.s_impact(), -10); ev(a + 0.6, S.s_impact(), -8)
a, b = bt("drop"); ev(a + 0.55, log_thud(1.1), -8); ev(a + 1.5, log_thud(1.0), -8); ev(a + 1.58, log_thud(0.9), -9)
for k in range(6):
    ev(a + 2.35 + k * 0.06, log_thud(0.8 + k * 0.08), -7, (-1) ** k * 0.3)
a, b = bt("sigh"); ev(a + 1.9, soft(0.8, 400, 220, 0.4), -18)
a, b = bt("pass")
for k in range(4):
    ev(a + 0.3 + k * 0.4, norm(bp(noise(0.2), 800, 3000) * env_ad(int(0.2 * SR), 0.04, 0.12)), -20, -0.3)
a, b = bt("double"); ev(a + 0.2, soft(0.5, 200, 400), -14)
for k in range(3):
    ev(a + 0.5 + k * 0.4, thud(), -16)
ev(a + 1.65, bonk(), -4)
for k in range(5):
    ev(a + 1.7 + k * 0.05, log_thud(0.7 + k * 0.1), -8)
for k in range(3):
    ev(a + 1.9 + k * 0.22, boing(400, 700, 0.18), -16)
# CẢNH 2
a = T["bark"][0]; ev(a, birds(T["worm"][0] - a), -24)
a, b = bt("bark")
for k in range(3):
    ev(a + 0.2 + k * 0.6, norm(bp(noise(0.5), 400, 2500) * env_ad(int(0.5 * SR), 0.05, 0.3)), -14)
a, b = bt("bark1"); ev(a + 0.2, crack(), -8)
a, b = bt("bark2"); ev(a + 0.1, whoosh(0.8, 600, 2500), -18)
a, b = bt("one"); ev(a + 0.9, pluck(), -4)
a, b = bt("twist1")
for k in range(3):
    ev(a + k * 0.6, S.s_pop(1.0 + k * 0.1), -12); ev(a + k * 0.6 + 0.2, creak(0.5), -20)
a, b = bt("twist2"); ev(a + 0.1, creak(1.3), -16); ev(a + 1.0, whoosh(1.0, 300, 1500), -18)
a, b = bt("pull"); ev(a + 0.1, creak(0.9), -12); ev(a + 1.0, ding_soft(), -10)
a, b = bt("share1"); ev(a + 0.4, S.s_pop(0.8), -14); ev(a + 0.9, S.s_pop(1.2), -12)
a, b = bt("tie"); ev(a + 0.8, zip_(0.2), -12); ev(a + 1.3, whoosh(0.4, 300, 2000), -14); ev(a + 1.5, ding_soft(), -10)
# CẢNH 3
a, b = bt("stomp")
for k in range(3):
    ev(a + 0.15 + k * 0.4, thud(), -10)
ev(a + 1.2, whoosh(0.3, 600, 3000), -10)
a, b = bt("tug"); ev(a + 0.1, creak(1.2), -12); ev(a + 1.3, creak(1.2), -8)
a, b = bt("wrap")
for k in range(8):
    ev(a + 0.1 + k * 0.33, whoosh(0.3, 400, 2000), -16, (-1) ** k * 0.3)
a, b = bt("cocoon"); ev(a + 0.8, soft(0.4, 900, 1000), -20)
a, b = bt("free")
for k in range(5):
    ev(a + 0.1 + k * 0.25, whoosh(0.25, 400, 2000), -18, (-1) ** k * 0.3)
a, b = bt("throw"); ev(a + 0.5, whoosh(0.7, 300, 3000), -6)
a, b = bt("useless"); ev(a + 0.1, S.s_impact(), -12)
a, b = bt("lost"); ev(a + 0.3, soft(1.0, 500, 250, 0.5), -16)
# CẢNH 4
a = T["rabbit"][0]; ev(a, wind(T["coil"][0] - a), -24)
a, b = bt("rabbit")
for k in range(3):
    ev(a + 0.3 + k * 0.62, boing(500, 800, 0.15), -18, 0.2)
a, b = bt("dinner")
for k in range(8):
    ev(a + k * 0.22, thud(), -18, -0.2)
a, b = bt("leap"); ev(a + 0.2, whoosh(0.6, 500, 3000), -10, 0.3)
a, b = bt("air")
for k in range(10):
    ev(a + k * 0.1, soft(0.06, 300, 280), -22)
ev(a + 1.4, soft(0.3, 300, 150, 0.2), -10)
a, b = bt("aaa"); ev(a + 0.3, S.sweep(900, 200, 1.4) * env_ad(int(1.4 * SR), 0.05, 0.6), -18)
a, b = bt("ledge"); ev(a, thud(), -2); ev(a + 0.05, bonk(), -10); ev(a + 0.2, soft(1.0, 1800, 2400, 0.4), -18)
a, b = bt("spot"); ev(a + 1.0, ding_soft(), -10)
a, b = bt("miss")
ev(a + 0.05, whoosh(0.5, 400, 2500), -12); ev(a + 0.9, soft(0.3, 600, 300), -14)
ev(a + 1.05, whoosh(0.5, 400, 2500), -12); ev(a + 1.9, bonk(), -4); ev(a + 2.0, boing(500, 900, 0.3), -10)
ev(a + 2.35, whoosh(0.5, 400, 2500), -12); ev(a + 2.9, S.s_pop(0.9), -6)
a, b = bt("anchor")
for k in range(4):
    ev(a + 0.2 + k * 0.4, whoosh(0.3, 300, 1500), -16)
ev(a + 1.9, zip_(0.2), -10); ev(a + 1.95, creak(0.4), -14)
a, b = bt("climb")
for k in range(5):
    ev(a + 0.2 + k * 0.45, creak(0.3), -18)
a, b = bt("itchy")
for k in range(3):
    ev(a + 0.1 + k * 0.2, norm(bp(noise(0.15), 800, 3000) * env_ad(int(0.15 * SR), 0.03, 0.1)), -16)
ev(a + 0.8, whoosh(0.3, 1500, 600), -10); ev(a + 0.9, creak(0.4), -10)
a, b = bt("grit")
for k in range(4):
    ev(a + 0.1 + k * 0.3, creak(0.25), -16)
ev(a + 1.3, thud(), -10)
for k in range(3):
    ev(a + 1.5 + k * 0.4, soft(0.3, 300, 200, 0.2), -18)
# CẢNH 5
a = T["coil"][0]; ev(a, wind(T["bend"][0] - a), -26)
a, b = bt("coil"); ev(a + 0.1, whoosh(1.0, 400, 1500), -18); ev(a + 1.3, S.s_pop(1.0), -12)
a, b = bt("lifeline"); ev(a + 0.1, S.s_impact(), -12)
a, b = bt("allmine"); ev(a + 0.1, S.s_impact(), -12)
a, b = bt("tieall")
for k in range(3):
    ev(a + k * 1.0, zip_(0.2), -10); ev(a + k * 1.0 + 0.05, S.s_pop(1.0 + k * 0.15), -12)
a, b = bt("tiebop"); ev(a + 0.1, zip_(0.25), -10)
for k in range(4):
    ev(a + 0.6 + k * 0.22, soft(0.08, 900, 700), -20)
a, b = bt("hey"); ev(a, boing(900, 1500, 0.2), -12)
a, b = bt("trophy")
for i in range(4):
    ev(a + 0.5 + i * 0.35, S.s_pop(1.0 + i * 0.12), -10)
# CẢNH 6
a, b = bt("bend"); ev(a + 0.3, creak(1.0), -14); ev(a + 1.5, zip_(0.2), -14)
a, b = bt("twang"); ev(a + 0.4, twang(), -4); ev(a + 0.45, whoosh(0.8, 800, 4000), -12, -0.4)
a, b = bt("idea"); ev(a + 0.9, ding_soft(), -10)
a, b = bt("card"); ev(a + 0.2, S.s_impact(), -12); ev(a + 0.5, ding_soft(), -14)

if __name__ == "__main__":
    import subprocess
    B = ROOT / "build"
    va = ROOT / "audio/voice.mp3"
    if not va.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(DUR), "-c:a", "libmp3lame", str(va)], check=True)
    S.EVENTS[:] = [(t, x, g + 4, p) for t, x, g, p in S.EVENTS]
    S.export(B / "Day_v1_nosfx.mp4", B / "Day_v1.mp4", pre_gain_db=float(sys.argv[1]) if len(sys.argv) > 1 else 1.1, limit=0.70)
