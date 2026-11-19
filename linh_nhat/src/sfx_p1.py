"""Hiệu ứng tiếng phần 1 — trộn với giọng đọc chủ kênh (p1/audio/voice.mp3), tự hạ tiếng khi có lời."""
import sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
PART = HERE.parent / "p1"
sys.path.insert(0, str(HERE.parent.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa

DUR = 75.69
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


# CẢNH: làng chài
ev(0.0, sea(4.4), -18); ev(0.0, gull(3, 4.0), -24)
ev(4.0, amb(2.8, 80, 350), -20)                       # lửa bếp
ev(5.3, slide(), -16)
ev(6.6, sea(3.8), -24)
for k in range(5):
    ev(10.4 + k * 0.42, thud(80, 0.2), -26)             # bước chân trưởng làng
ev(12.5, rustle(), -16)
ev(13.0, S.s_whoosh(0.35, 800, 4000, 0.3), -12); ev(13.4, boom(), -8)
ev(14.5, amb(1.7, 80, 300), -26)
ev(16.2, amb(1.9, 150, 600, 0.15), -26)               # đêm, gió nhẹ
# đầu ngõ, khâu chỉ
ev(18.0, amb(6.1, 1500, 4000, 0.4), -32)
for k in range(4):
    ev(18.6 + k * 1.5, S.s_pop(1.0 + 0.05 * k), -22)
ev(24.1, chime(660, 2.0), -18)
ev(26.3, norm(fade(sum(np.sin(2 * np.pi * f * t_(3.0)) for f in (330, 495, 660)) * 0.3, 0.8, 1.0)), -22)  # vầng sáng
ev(29.3, rustle(0.6), -20); ev(30.6, rustle(0.5), -22)
ev(33.6, thud(200, 0.15), -24)
# sân ga
ev(35.2, chug(7.5), -18); ev(35.4, whistle(), -16)
for k in range(10):
    ev(35.4 + k * 0.48, rustle(0.25), -28)              # cờ phần phật
ev(40.2, amb(2.5, 150, 600, 0.2), -24)
# doanh trại
for k in range(8):
    ev(42.9 + k * 0.5, thud(70, 0.25), -18)
ev(47.3, S.s_whoosh(0.5, 200, 1200, 0.5), -18)
ev(48.84, slap(), -6)
for k in range(8):
    ev(51.8 + k * 0.45, thud(75, 0.22), -20)
ev(49.8, S.s_ding(), -20)
ev(57.8, amb(6.0, 100, 300, 0.1), -26)
ev(63.9, boom(2.0, 48), -10)
ev(65.9, chew(), -18)
ev(68.1, norm(np.sin(2 * np.pi * 420 * t_(0.6)) * np.exp(-t_(0.6) / 0.2)), -20)   # tiếng xô kim loại
for k in range(6):
    ev(70.6 + k * 0.45, rustle(0.3), -26)               # chăn rung vì nín cười
ev(73.5, slam(), -4)

if __name__ == "__main__":
    S.export(PART / "build" / "P1_nosfx.mp4", PART / "build" / "P1.mp4", pre_gain_db=2.0, limit=0.70)
