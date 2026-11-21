"""Hiệu ứng tiếng cho tập Mona Lisa — chuyện phá án nhẹ nhàng, có chút hài hước.

Chạy sau render.py full:
  python3 src/sfx_events.py   → build/MonaLisa_v1.mp4 (có hiệu ứng), build/sfx_stem.wav
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, typing, rng, noise, bp, lp, hp, env_exp, env_ad, t_, norm, sweep, SR  # noqa

S.configure(ROOT, 111.336)


def shutter():
    d = 0.25
    n = int(d * SR)
    x = np.zeros(n)
    c1 = hp(noise(0.006), 3000) * env_exp(int(0.006 * SR), 0.0015)
    x[:len(c1)] += c1
    mech = bp(noise(0.12), 600, 3000) * env_ad(int(0.12 * SR), 0.01, 0.03) * 0.5
    a = int(0.015 * SR); x[a:a + len(mech)] += mech
    c2 = hp(noise(0.006), 2500) * env_exp(int(0.006 * SR), 0.002)
    b = int(0.075 * SR); x[b:b + len(c2)] += c2 * 0.8
    return norm(x)


def steps(t0, n_steps, gap, g, pan=0.0):
    for i in range(n_steps):
        d = 0.09
        x = lp(noise(d), 700) * env_exp(int(d * SR), 0.015) + np.sin(2 * np.pi * 90 * t_(d)) * env_exp(int(d * SR), 0.02) * 0.5
        ev(t0 + i * gap + rng.uniform(-0.02, 0.02), norm(x), g + rng.uniform(-2, 1), pan + rng.uniform(-0.2, 0.2))


def drawer(d=0.5):
    n = int(d * SR)
    x = bp(noise(d), 300, 2500) * env_ad(n, 0.05, 0.2) * (1 + 0.5 * np.sin(2 * np.pi * 30 * t_(d)))
    th = lp(noise(0.08), 600) * env_exp(int(0.08 * SR), 0.015)
    thud = np.zeros(n); k = max(0, n - len(th) - int(0.01 * SR))  # tiếng "cạch" khi ngăn kéo đóng hết
    thud[k:k + len(th)] = th[: n - k]
    return norm(x + thud * 1.5)


def creak(d=0.7):
    n = int(d * SR)
    tt = t_(d)
    f = 240 + 200 * np.sin(np.pi * tt / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    fr = (np.sin(ph) > 0.6).astype(float)
    return norm(bp(fr + 0.2 * noise(d), 400, 2500) * env_ad(n, 0.1, 0.3))


def knock():
    d = 0.18
    n = int(d * SR)
    return norm(np.sin(2 * np.pi * 190 * t_(d)) * env_exp(n, 0.035) + bp(noise(d), 700, 2600) * env_exp(n, 0.008) * 0.8)


def murmur(d):
    """Tiếng đám đông xì xào (nhiều 'giọng' nhiễu lọc dải tiếng nói)."""
    n = int(d * SR)
    x = np.zeros(n)
    for k in range(8):
        v = bp(noise(d), rng.uniform(250, 400), rng.uniform(900, 1600))
        v *= 0.4 + 0.6 * (np.sin(2 * np.pi * rng.uniform(2, 5) * t_(d) + rng.uniform(0, 6)) > 0.2)
        x += lp(v, 2000)
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.5 * SR), (n - np.arange(n)) / (0.7 * SR)))
    return norm(x * fade)


def clock_run(t0, t1, g=-8):
    t = t0
    while t < t1:
        ev(t, S.s_clock(), g)
        t += 0.12


P = -12
# 0–6,8 Louvre
ev(0.6, S.s_pop(1.0), P)
ev(3.8, S.s_marker(0.6), -16)
ev(4.0, S.s_pop(1.1), P - 2)
ev(5.6, S.s_paper(0.2), -16, -0.4)
# 6,8 hơn một ngày
clock_run(7.0, 9.6)
ev(7.8, S.s_pop(0.9), P)
# 10,1 Béroud, bức tường trống
ev(10.05, S.s_whoosh(0.4, 200, 1800, 0.3), -18)
ev(10.6, S.s_paper(0.25), -15, -0.4)
ev(12.2, S.s_pop(1.0), P)
ev(14.25, S.s_whoosh(0.4, 150, 1200, 0.3), -18)
for k in range(4):
    ev(15.1 + k * 0.12, S.s_tick(1.1), -14)
ev(15.3, S.s_pop(1.0), P - 2)
# 16,3 lính gác, bên chụp ảnh
ev(16.4, S.s_pop(1.0), P)
ev(16.6, shutter(), -4, 0.4)
ev(18.7, S.s_pop(1.1), P - 3, 0.4)
for k in range(3):
    ev(21.1 + k * 0.35, S.s_pop(1.2 + k * 0.08), P, -0.5)
ev(23.9, S.s_stamp(), -6, 0.4)
# 25,2 Peruggia
ev(25.15, S.s_drop(), -11)
ev(25.6, S.s_paper(0.25), -15, -0.4)
ev(29.8, S.s_stamp(), -7, 0.4)
ev(30.6, S.s_pop(1.0), P - 2, 0.4)
# 31,8 vụ trộm
ev(31.76, S.s_paper(0.3), -14)
ev(34.1, S.s_drop(), -14)
steps(35.25, 6, 0.16, -16)
ev(36.25, S.s_rattle(0.5), -16)
ev(37.45, creak(0.6), -15, 0.4)
steps(37.7, 5, 0.2, -18, 0.4)
ev(39.3, S.s_pop(1.0), P)
ev(39.7, S.s_marker(0.4), -16)
# 41,4 vân tay, hồ sơ
ev(41.4, S.s_drop(), -12)
ev(43.1, S.s_whoosh(0.5, 400, 3000), -16)
ev(43.2, S.s_pop(1.0), P - 2)
ev(44.6, S.s_drop(), -12)
ev(44.9, S.s_marker(0.5), -16)
ev(46.6, S.s_marker(0.6), -16)
ev(47.95, S.s_pop(1.0), P - 2)
for k in range(6):
    ev(48.1 + k * 0.12, drawer(0.45), -16, rng.uniform(-0.4, 0.4))
ev(50.1, S.s_pop(0.8), P)
# 51,5 Apollinaire, Picasso
ev(51.45, S.s_drop(), -11)
ev(52.3, S.s_paper(0.25), -15, -0.4)
ev(54.38, S.s_drop(), -11)
ev(54.8, S.s_paper(0.25), -15, -0.4)
ev(57.6, S.s_stamp(), -6)
# 59 phòng trọ
steps(59.05, 4, 0.22, -16, -0.4)
ev(59.6, S.s_pop(1.0), P - 2, -0.4)
ev(61.5, S.s_pop(0.9), P)
ev(63.3, creak(0.6), -15, 0.3)
ev(64.0, S.s_pop(1.1), P - 2, 0.3)
# 66,6 báo chí, đám đông
for k in range(3):
    ev(66.6 + k * 0.4, S.s_paper(0.3), -12, (k - 1) * 0.4)
ev(68.4, murmur(3.0), -16)
# 71,3 hai năm, lá thư
for k in range(6):
    ev(71.4 + k * 0.12, S.s_clock(), -15)
ev(72.3, S.s_pop(1.0), P)
ev(74.6, S.s_pop(1.0), P, 0.4)
ev(76.5, S.s_paper(0.35), -12)
ev(78.3, S.s_marker(1.4), -21)
ev(79.9, S.s_marker(0.9), -21)
# 81,1 khách sạn
ev(81.2, S.s_paper(0.25), -15, -0.4)
ev(84.4, S.s_paper(0.25), -15, -0.4)
ev(85.8, S.s_pop(1.0), P - 2)
ev(86.8, creak(0.7), -12)
ev(88.0, S.s_drop(), -12)
ev(88.6, S.s_ding(), -16)
ev(89.14, S.s_drop(), -12)
ev(89.9, S.s_stamp(), -6)
# 91,1 Uffizi, báo
ev(91.06, S.s_drop(), -11)
ev(91.6, S.s_pop(1.0), P - 2, -0.4)
ev(93.8, S.s_paper(0.35), -11)
ev(94.1, S.s_marker(0.5), -15)
ev(94.3, S.s_pop(0.9), P)
# 95,7 phiên tòa
ev(95.72, S.s_drop(), -11)
ev(97.7, S.s_pop(1.0), P - 2)
ev(100.6, knock(), -9)
ev(100.85, knock(), -11)
ev(101.6, S.s_pop(0.9), P - 2)
ev(103.0, S.s_marker(0.3), -12)
ev(103.3, S.s_pop(1.2), P)
# 104,7 trở về Louvre
ev(104.64, S.s_drop(), -11)
ev(104.75, S.s_pop(1.0), P)
ev(105.2, murmur(4.5), -20)
ev(108.6, S.s_ding(), -13)

# cả lớp +4 dB cho bằng mức đã chuẩn ở các tập trước (dấu/cú nhấn ~8 dB dưới giọng)
S.EVENTS[:] = [(t, x, g + 4, p) for t, x, g, p in S.EVENTS]

if __name__ == "__main__":
    B = ROOT / "build"
    S.export(B / "MonaLisa_v1_nosfx.mp4", B / "MonaLisa_v1.mp4", pre_gain_db=0.0)
