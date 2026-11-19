"""Hiệu ứng tiếng phần 3 — trộn với giọng đọc chủ kênh (p1/audio/voice.mp3), tự hạ tiếng khi có lời."""
import sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
PART = HERE.parent / "p3"
sys.path.insert(0, str(HERE.parent.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa

DUR = 63.69
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


# PHẦN 3
ev(0.0, sea(5.9), -24)
for k in range(9):
    ev(0.3 + k * 0.45, norm(lp(noise(0.2), 600) * env_ad(int(0.2 * SR), 0.03, 0.15)), -28)   # bước chân trên cát
ev(5.84, sea(5.3), -20); ev(5.84, amb(5.3, 50, 160, 0.2), -24)           # máy tàu trầm
for k in range(4):
    ev(6.4 + k * 0.9, norm(lp(noise(0.4), 900) * env_ad(int(0.4 * SR), 0.05, 0.3)), -26)   # mái chèo
ev(11.12, sea(4.7), -24)
ev(15.78, amb(5.9, 150, 500, 0.1), -32)
ev(16.9, chime(440, 3.0), -26)
ev(21.66, rustle(0.6), -18)
for k in range(4):
    ev(22.2 + k * 0.9, S.s_pop(0.9 + 0.1 * k), -24)
ev(26.39, amb(4.4, 1500, 4000, 0.3), -32)
for k in range(5):
    ev(26.5 + k * 0.42, thud(80, 0.2), -26)
ev(30.77, amb(3.3, 60, 200, 0.1), -24); ev(31.5, boom(2.4, 40), -22)
ev(34.1, amb(6.3, 1500, 4000, 0.3), -34)
for k in range(4):
    ev(34.4 + k * 0.5, thud(75, 0.22), -24)
ev(37.8, rustle(0.5), -20)
ev(40.39, amb(4.9, 1000, 4000, 0.5), -30)                                 # tiếng rè radio
ev(45.31, amb(2.5, 100, 300, 0.1), -34); ev(45.6, rustle(0.8), -24)
ev(51.55, boom(2.5, 44), -18)
ev(56.4, thud(140, 0.4), -10)                                             # súng rơi xuống đất
ev(58.2, amb(5.5, 1500, 4000, 0.3), -34); ev(62.25, chime(660, 1.6), -24)

if __name__ == "__main__":
    S.export(PART / "build" / "P3_nosfx.mp4", PART / "build" / "P3.mp4", pre_gain_db=2.0, limit=0.70)
