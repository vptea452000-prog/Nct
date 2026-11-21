"""Âm thanh Tập 2: Cây giáo — giọng ú ớ chuẩn (tools/babble.py) + hiệu ứng hoạt hình.
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
        if name == "bounce":
            st = a + 0.32
        d = max(0.35, en - st)
        x = babble(spk, d, emo, kind, seed=100 + i)
        g = -3 if kind == "shout" else (-12 if kind == "whisper" else -6)
        if name == "useless2":
            x = lp(x, 1800); g -= 4
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


# CẢNH 1
a = T["open"][0]; ev(a, birds(T["hug"][0] - a), -18); ev(a, stream(T["hug"][0] - a), -20)
ev(a + 0.3, S.s_impact(), -10); ev(a + 0.6, S.s_impact(), -8)
a, b = bt("lunch"); ev(a + 0.2, S.s_paper(0.4), -18)
a, b = bt("charge"); ev(a, whoosh(0.6, 200, 3000), -10); ev(a + 0.8, bonk(), -4)
a, b = bt("bounce"); ev(a + 0.05, boing(500, 900, 0.3), -8); ev(a + 0.15, bonk(), -6)
ev(a + 0.3, soft(1.2, 1800, 2400, 0.4), -18)
a, b = bt("turn"); ev(a + 0.3, snort(), -6, 0.4); ev(a + 0.9, norm(lp(noise(0.8), 500)), -14, 0.4)
a, b = bt("chase")
for k in range(10):
    ev(a + k * 0.16, thud(), -16, (-1) ** k * 0.4)
ev(a + 1.6, soft(0.5, 400, 1200, 0.3), -12)
for k, ts in enumerate([a + 2.0, a + 2.35, a + 2.7]):
    ev(ts, thud(), -5)
ev(a + 2.9, whoosh(0.6, 200, 1500), -14)
# CẢNH 2
a = T["hug"][0]; ev(a, fire_soft(T["peek"][0] + 1.3 - a), -18); ev(a, wind(T["snort"][0] - a), -22)
a, b = bt("hug"); ev(a + 0.2, norm(lp(noise(1.6), 250) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.6 * t_(1.6)))), -18)  # ngáy
a, b = bt("knap"); ev(a + 0.6, crack(), -3)
a, b = bt("ouch"); ev(a, boing(900, 1400, 0.2), -12)
a, b = bt("haft")
for k in range(5):
    ev(a + k * 0.64, whoosh(0.25, 800, 3000), -16); ev(a + k * 0.64 + 0.2, S.s_pop(1.0 + k * 0.08), -14)
a, b = bt("done"); ev(a + 0.3, ding_soft(), -8)
# CẢNH 3
a, b = bt("peek"); ev(a + 0.4, soft(0.25, 600, 900), -14)
a, b = bt("ex1"); ev(a + 0.5, thud(), -10)
a, b = bt("ex3"); ev(a + 0.5, ding_soft(), -14)
a, b = bt("huh")
for k in range(3):
    ev(a + 0.3 + k * 0.4, soft(0.2, 700 + k * 120, 900 + k * 120), -16)
a, b = bt("press1"); ev(a + 0.6, thud(), -16)
a, b = bt("press2"); ev(a + 0.65, soft(0.15, 2200, 2600), -12); ev(a + 0.7, boing(600, 1600, 0.4), -6)
a, b = bt("same"); ev(a + 0.6, S.s_pop(0.9), -14); ev(a + 1.0, S.s_pop(1.2), -12)
a, b = bt("useless"); ev(a + 0.1, S.s_impact(), -12)
a, b = bt("snap"); ev(a + 0.6, crack(), -2); ev(a + 0.9, whoosh(0.6, 400, 2000), -14); ev(a + 1.5, splash(), -8, 0.4)
a, b = bt("lost"); ev(a + 0.3, soft(0.9, 500, 250, 0.4), -18)
# CẢNH 4
a = T["snort"][0]; ev(a, stream(T["fish"][0] - a), -22)
a, b = bt("snort"); ev(a + 0.2, snort(), -6, 0.3); ev(a + 0.6, snort(), -8, 0.3); ev(a + 1.9, oink(0.7), -4, 0.5); ev(a + 2.1, oink(0.65), -6, 0.5)
a, b = bt("brother"); ev(b - 0.45, soft(0.3, 300, 200), -18)
a, b = bt("bonk2"); ev(a + 0.2, whoosh(0.3, 300, 2500), -12); ev(a + 0.5, bonk(), -4); ev(a + 0.8, boing(500, 900, 0.3), -8)
a, b = bt("help")
for k in range(4):
    ev(a + 0.2 + k * 0.5, snort(), -14, 0.4)
a, b = bt("rebuild"); ev(a, splash(), -6); ev(a + 0.1, whoosh(2.4, 300, 3000), -16)
for k in range(4):
    ev(a + 0.6 + k * 0.5, S.s_pop(1.0 + k * 0.1), -12)
a, b = bt("catch"); ev(a + 0.5, whoosh(0.8, 300, 3000), -8)
a, b = bt("aim"); ev(a + 0.3, norm(bp(noise(1.0), 1000, 3000) * (np.sin(2 * np.pi * 9 * t_(1.0)) > 0)), -22)
a, b = bt("brake")
for k in range(6):
    ev(a + k * 0.12, thud(), -12, 0.4)
ev(a + 0.5, skid(), -4, 0.3); ev(a + 1.3, soft(0.5, 900, 600, 0.3), -14)
a, b = bt("flee"); ev(a + 0.3, oink(1.3), -6, 0.5); ev(a + 0.5, oink(1.4), -8, 0.6)
for k in range(6):
    ev(a + 0.3 + k * 0.12, thud(), -18, 0.6)
a, b = bt("win"); ev(a + 0.5, ding_soft(), -16)
# CẢNH 5
a = T["fish"][0]; ev(a, stream(T["sing"][0] - a), -20)
a, b = bt("fish"); ev(a + 1.2, whoosh(0.3, 400, 3000), -10); ev(a + 1.45, splash(), -6)
a, b = bt("fishstick"); ev(a, S.s_impact(), -10); ev(a + 0.1, ding_soft(), -12)
a, b = bt("allmine"); ev(a + 0.1, S.s_impact(), -12)
a, b = bt("sing"); ev(a, fire_soft(b - a), -18)
# CẢNH 6
a = T["chilly"][0]; ev(a, wind(T["card"][0] - a), -16)
a, b = bt("chilly"); ev(a + 0.1, norm(np.sin(2 * np.pi * 420 * t_(1.2)) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * t_(1.2)))), -22, 0.4)
ev(a + 1.3, boing(1200, 2000, 0.2), -8)
a, b = bt("idea"); ev(a + 1.0, ding_soft(), -10)
a, b = bt("useless2"); ev(a, soft(0.25, 600, 300), -18)
a, b = bt("card"); ev(a + 0.2, S.s_impact(), -12); ev(a + 0.5, ding_soft(), -14)

if __name__ == "__main__":
    import subprocess
    B = ROOT / "build"
    va = ROOT / "audio/voice.mp3"
    if not va.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(DUR), "-c:a", "libmp3lame", str(va)], check=True)
    S.EVENTS[:] = [(t, x, g + 4, p) for t, x, g, p in S.EVENTS]
    S.export(B / "Giao_v1_nosfx.mp4", B / "Giao_v1.mp4", pre_gain_db=float(sys.argv[1]) if len(sys.argv) > 1 else 1.1, limit=0.70)
