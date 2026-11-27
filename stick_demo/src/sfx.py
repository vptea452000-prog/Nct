"""Hiệu ứng tiếng cho bản thử người que — chỉ tiếng động, không giọng, không nhạc."""
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa

DUR = 25.0
S.configure(ROOT, DUR)


def water(d):
    n = int(d * SR)
    x = bp(noise(d), 400, 3000) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.5 * t_(d)))
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.5 * SR), (n - np.arange(n)) / (0.5 * SR))))


def splash(d=0.7):
    n = int(d * SR)
    return norm(bp(noise(d), 500, 4000) * env_ad(n, 0.01, 0.25) + S.sweep(300, 900, d) * env_exp(n, 0.06) * 0.3)


def drip(f=1400):
    d = 0.15; tt = t_(d)
    return norm(np.sin(2 * np.pi * (f + 2000 * tt) * tt) * np.exp(-tt / 0.03))


def flap(d=0.25):
    return norm(lp(noise(d), 600) * env_ad(int(d * SR), 0.03, 0.15))


def thunk():
    d = 0.4; n = int(d * SR); tt = t_(d)
    return norm(lp(noise(d), 500) * env_exp(n, 0.04) + np.sin(2 * np.pi * 110 * tt) * np.exp(-tt / 0.08))


def wobble():
    d = 0.9; tt = t_(d)
    return norm(np.sin(2 * np.pi * 160 * tt + 3 * np.sin(2 * np.pi * 14 * tt)) * np.exp(-tt / 0.3))


def chomp():
    d = 0.18; n = int(d * SR)
    return norm(bp(noise(d), 300, 1500) * env_ad(n, 0.01, 0.08))


def screech():
    d = 0.6; tt = t_(d)
    f = 2400 - 900 * tt / d
    return norm(bp(np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * noise(d), 1200, 5000) * env_ad(int(d * SR), 0.03, 0.35))


ev(0, water(DUR), -20)
ev(1.2, S.s_whoosh(0.3, 400, 1500, 0.5), -22)
ev(1.95, splash(), -6)
for k in range(5):
    ev(3.2 + k * 0.45, drip(1200 + k * 150), -18)
ev(3.3, S.s_whoosh(0.6, 300, 1500, 0.5), -16)
ev(6.1, S.s_whoosh(0.5, 300, 1200, 0.5), -16)
for k in range(5):
    ev(6.4 + k * 0.6, flap(), -24, 0.4)
ev(8.7, S.s_ding(), -18)
ev(10.0, S.s_whoosh(3.0, 200, 3000, 0.7), -10)
ev(13.55, S.s_whoosh(0.3, 800, 4000, 0.4), -6)
for k in range(6):
    ev(13.8 + k * 0.25, flap(), -14, 0.3)
ev(16.0, S.s_whoosh(0.5, 200, 800, 0.5), -14)
ev(16.6, S.s_whoosh(0.9, 400, 2500, 0.5), -8)
ev(17.9, thunk(), -4); ev(17.95, wobble(), -12)
for k in range(5):
    ev(20.6 + k * 0.98, chomp(), -12)
ev(23.0, screech(), -14, 0.3)

if __name__ == "__main__":
    import subprocess
    B = ROOT / "build"
    va = ROOT / "audio/voice.mp3"
    va.parent.mkdir(exist_ok=True)
    if not va.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(DUR), "-c:a", "libmp3lame", str(va)], check=True)
    S.export(B / "Stick_demo_nosfx.mp4", B / "Stick_demo.mp4", pre_gain_db=10.0, limit=0.70)
