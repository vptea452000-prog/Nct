"""Hiệu ứng tiếng phần 4 — trộn với giọng đọc chủ kênh (p1/audio/voice.mp3), tự hạ tiếng khi có lời."""
import sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
PART = HERE.parent / "p4"
sys.path.insert(0, str(HERE.parent.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa

DUR = 48.06
S.configure(PART, DUR)


def fade(x, a=0.4, b=0.4):
    n = len(x); i = np.arange(n)
    return x * np.minimum(1, np.minimum(i / (a * SR), (n - i) / (b * SR)))


def amb(d, lo, hi, mod=0.3):
    tt = t_(d)
    return norm(fade(bp(noise(d), lo, hi) * (0.7 + 0.3 * np.sin(2 * np.pi * mod * tt))))


def sea(d):
    tt = t_(d)
    return norm(fade(lp(noise(d), 700) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.25 * tt) ** 2)))


def gull(n=3, d=4.0):
    out = np.zeros(int(d * SR))
    for k in range(n):
        st = int((0.4 + k * d / n) * SR); L = int(0.35 * SR); tt = t_(0.35)
        f = 1500 + 700 * np.sin(np.pi * tt / 0.35)
        out[st:st + L] += np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(L, 0.03, 0.2) * 0.5
    return norm(lp(out, 4000))


def thud(f=90, d=0.3):
    tt = t_(d); n = int(d * SR)
    return norm(lp(noise(d), 500) * env_exp(n, 0.03) + np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.06))


def boom(d=1.6, f=55):
    tt = t_(d)
    return norm(np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.5) + lp(noise(d), 200) * np.exp(-tt / 0.3) * 0.5)


def rustle(d=0.4):
    return norm(bp(noise(d), 2000, 6000) * env_ad(int(d * SR), 0.02, d * 0.6))


def slide(d=0.5):
    return norm(bp(noise(d), 300, 1500) * env_ad(int(d * SR), 0.05, 0.3))


def chime(f=880, d=1.5):
    tt = t_(d)
    return norm(sum(np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * (1.5 + k)) / k for k in (1, 2, 3)))


def whistle(d=1.6):
    tt = t_(d)
    x = sum(np.sin(2 * np.pi * f * tt) for f in (520, 660, 780)) * (1 + 0.1 * np.sin(2 * np.pi * 6 * tt))
    return norm(lp(x * env_ad(int(d * SR), 0.15, 0.8) + bp(noise(d), 800, 3000) * 0.2, 4000))


def chug(d):
    tt = t_(d)
    pulse = (np.sin(2 * np.pi * 3.0 * tt) > 0.6).astype(float)
    return norm(fade(lp(noise(d), 600) * (0.3 + 0.7 * lp(pulse, 30))))


def slap():
    d = 0.25; n = int(d * SR)
    return norm(hp(noise(d), 1500) * env_exp(n, 0.012) + lp(noise(d), 800) * env_exp(n, 0.03) * 0.6)


def slam():
    d = 0.6; tt = t_(d); n = int(d * SR)
    return norm(lp(noise(d), 400) * env_exp(n, 0.05) + np.sin(2 * np.pi * 70 * tt) * np.exp(-tt / 0.12))


def chew(n=6, gap=0.22):
    d = n * gap + 0.3; out = np.zeros(int(d * SR))
    for k in range(n):
        st = int(k * gap * SR); L = int(0.12 * SR)
        out[st:st + L] += lp(noise(0.12), 900) * env_ad(L, 0.02, 0.08)
    return norm(out)


# PHẦN 4
ev(0.0, sea(3.4), -22); ev(0.3, whistle(1.4), -24); ev(0.0, gull(2, 3.0), -28)
ev(3.12, amb(8.6, 100, 400, 0.08), -26)                                   # gió trên phố hoang
for k in range(10):
    ev(3.3 + k * 0.44, thud(75, 0.2), -28)
ev(11.75, chug(7.6), -26); ev(16.0, whistle(1.4), -26)
for k in range(8):
    ev(15.4 + k * 0.48, thud(75, 0.2), -30)
ev(19.44, sea(5.0), -26); ev(19.44, gull(2, 4.5), -30)
ev(24.43, amb(5.9, 1500, 4000, 0.3), -36)
ev(30.6, rustle(0.6), -22)
ev(33.3, chime(523, 3.0), -26)
ev(35.33, amb(0.95, 80, 350), -24)
ev(36.26, amb(8.0, 100, 400, 0.05), -32)
ev(40.68, sea(3.7), -28)
ev(44.31, chime(392, 3.5), -22)

if __name__ == "__main__":
    S.export(PART / "build" / "P4_nosfx.mp4", PART / "build" / "P4.mp4", pre_gain_db=2.0, limit=0.70)
