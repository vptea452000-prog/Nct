"""Hiệu ứng tiếng bản thử 16:9 — chỉ tiếng động (giọng dẫn chủ kênh gửi sau)."""
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa

DUR = 18.6
S.configure(ROOT, DUR)


def room(d):
    n = int(d * SR)
    x = lp(noise(d), 500) * 0.6 + bp(noise(d), 800, 2000) * 0.15
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.5 * SR), (n - np.arange(n)) / (0.5 * SR))))


def roll(d):
    n = int(d * SR); tt = t_(d)
    return norm(lp(noise(d), 300) * (0.8 + 0.2 * np.sin(2 * np.pi * 9 * tt)) * np.minimum(1, np.minimum(np.arange(n) / (0.1 * SR), (n - np.arange(n)) / (0.2 * SR))))


def squeak():
    d = 0.35; tt = t_(d)
    f = 1800 + 500 * np.sin(2 * np.pi * 6 * tt)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(int(d * SR), 0.02, 0.2) * 0.6 + bp(noise(d), 2000, 5000) * env_ad(int(d * SR), 0.01, 0.15) * 0.3)


def beep():
    d = 0.14; tt = t_(d)
    return norm(np.sin(2 * np.pi * 1760 * tt) * env_ad(int(d * SR), 0.005, 0.08))


def coin_pour(d=1.4):
    out = np.zeros(int(d * SR)); r = np.random.default_rng(3)
    for k in range(34):
        st = int((k / 34) ** 1.3 * (d - 0.2) * SR); L = int(0.12 * SR)
        f = r.uniform(3200, 5200); tt = t_(0.12)
        out[st:st + L] += np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.03) * r.uniform(0.3, 0.8)
    return norm(lp(out, 6000))


def tap(n=6, gap=0.11):
    d = n * gap + 0.2; out = np.zeros(int(d * SR))
    for k in range(n):
        st = int(k * gap * SR); L = int(0.06 * SR); tt = t_(0.06)
        out[st:st + L] += lp(noise(0.06), 900) * np.exp(-tt / 0.012)
    return norm(out)


ev(0, room(DUR), -26)
ev(0.0, roll(1.4), -16, 0.4); ev(1.35, squeak(), -14, 0.3)
ev(2.4, roll(0.9), -16, 0.2); ev(2.35, S.s_whoosh(0.5, 300, 2000, 0.5), -14); ev(3.25, squeak(), -12)
ev(4.0, tap(8), -20); ev(5.0, tap(8), -20)
ev(6.5, S.s_whoosh(0.4, 300, 1500, 0.5), -16); ev(7.5, coin_pour(1.4), -10); ev(7.4, S.s_impact(), -20)
for k in range(3):
    ev(9.2 + k * 0.9, beep(), -12, -0.4)
ev(12.3, S.s_whoosh(0.6, 200, 1500, 0.5), -16)
for i in range(3):
    ev(12.3 + i * 0.2, S.s_pop(1.0 + i * 0.1), -14)
ev(13.3, S.s_ding(), -14)
ev(16.7, norm(S.sweep(420, 260, 1.0) * env_ad(int(1.0 * SR), 0.05, 0.6)), -18)

if __name__ == "__main__":
    import subprocess
    B = ROOT / "build"
    va = ROOT / "audio/voice.mp3"
    va.parent.mkdir(exist_ok=True)
    if not va.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(DUR), "-c:a", "libmp3lame", str(va)], check=True)
    S.export(B / "Modern_demo_nosfx.mp4", B / "Modern_demo.mp4", pre_gain_db=10.0, limit=0.70)
