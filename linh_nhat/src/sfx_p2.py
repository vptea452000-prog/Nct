"""Hiệu ứng tiếng phần 2 — trộn với giọng đọc chủ kênh (p1/audio/voice.mp3), tự hạ tiếng khi có lời."""
import sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
PART = HERE.parent / "p2"
sys.path.insert(0, str(HERE.parent.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa

DUR = 69.97
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


# PHẦN 2
ev(0.0, sea(5.6), -16); ev(0.0, gull(2, 5.0), -26)
ev(0.0, amb(5.5, 60, 200, 0.2), -22)                    # máy tàu ì ì
ev(5.5, sea(4.2), -20)
ev(9.6, rustle(0.6), -16)
ev(11.6, sea(8.4), -24)
for k in range(4):
    ev(11.9 + k * 0.7, thud(220, 0.12), -26)             # muôi gõ bát
for k in range(8):
    ev(14.7 + k * 0.22, thud(90, 0.15), -24)             # chân chạy trên cát
ev(16.5, S.s_pop(1.2), -16)
ev(16.8, amb(3.1, 80, 350), -18)                         # lửa trại
for i, t0 in enumerate((0.6, 2.0, 3.2)):
    ev(19.9 + t0, boom(1.4, 50 + 6 * i), -12 - 2 * i)
ev(24.3, amb(6.1, 150, 500, 0.1), -30)
ev(26.84, thud(260, 0.12), -22); ev(27.98, thud(240, 0.12), -22); ev(28.7, norm(lp(noise(0.5), 1200) * env_ad(int(0.5 * SR), 0.05, 0.3)), -24)
ev(30.4, amb(6.4, 1500, 4000, 0.3), -32)                 # rừng
for k in range(4):
    ev(32.0 + k * 1.2, rustle(0.35), -20)
for k in range(3):
    ev(38.6 + k * 0.6, thud(300, 0.1), -14)              # đục lỗ thắt lưng
ev(40.9, amb(4.4, 2000, 6000, 0.6), -34)                 # ve sầu nóng nực (nền rất nhỏ)
ev(45.3, amb(4.4, 100, 500, 0.4), -24)                   # bùn lép nhép
for k in range(5):
    ev(47.6 + k * 0.5, norm(lp(noise(0.25), 500) * env_ad(int(0.25 * SR), 0.03, 0.18)), -22)
ev(49.7, sea(4.0), -26); ev(51.9, boom(2.0, 46), -12)
ev(53.7, amb(4.0, 150, 600, 0.15), -28)
ev(57.7, amb(9.6, 300, 1200, 0.1), -32)                  # đêm trong lều
ev(62.95, chime(520, 2.5), -24)
ev(67.4, gull(2, 2.5), -26)

if __name__ == "__main__":
    S.export(PART / "build" / "P2_nosfx.mp4", PART / "build" / "P2.mp4", pre_gain_db=2.0, limit=0.70)
