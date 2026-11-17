"""Hiệu ứng tiếng cho tập Onoda (phong cách hoạt hình). Chạy sau render.py full."""
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, typing, rng, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa

S.configure(ROOT, 120.816)


def jungle_amb(d):
    n = int(d * SR); tt = t_(d)
    x = bp(noise(d), 300, 2500) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * tt) ** 2) * 0.5
    x += bp(noise(d), 4200, 5200, 3) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt)) * 0.3
    for k in range(int(d / 2)):
        st = rng.uniform(0.3, max(0.4, d - 0.6)); a = int(st * SR); L = int(0.35 * SR)
        f = 2600 + 900 * np.sin(2 * np.pi * 7 * t_(0.35)) + rng.uniform(-300, 300)
        ch = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(L, 0.02, 0.1) * 0.5
        x[a:a + L] += ch[: max(0, n - a)]
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.4 * SR), (n - np.arange(n)) / (0.5 * SR)))
    return norm(x * fade)


def night_amb(d):
    n = int(d * SR); tt = t_(d)
    x = bp(noise(d), 3500, 4500, 3) * (0.5 + 0.5 * (np.sin(2 * np.pi * 2.2 * tt) > 0)) * 0.5 + bp(noise(d), 200, 800) * 0.2
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.4 * SR), (n - np.arange(n)) / (0.5 * SR)))
    return norm(x * fade)


def rustle(d=0.7):
    n = int(d * SR)
    return norm(bp(noise(d), 800, 5000) * env_ad(n, 0.1, 0.25) * (1 + 0.6 * np.sin(2 * np.pi * 14 * t_(d))))


def boing(f0=700, f1=300, d=0.3):
    return norm(S.sweep(f0, f1, d) * env_exp(int(d * SR), 0.12))


def jet(d):
    return norm(lp(noise(d), 1500) * np.sin(np.pi * np.clip(t_(d) / d, 0, 1)) ** 1.2)


def shot():
    d = 0.6; n = int(d * SR)
    return norm(lp(noise(d), 2400) * env_exp(n, 0.015) + lp(noise(d), 500) * env_exp(n, 0.1) * 0.7)


def crackle(d):
    n = int(d * SR)
    x = (rng.random(n) < 0.004) * rng.normal(0, 3, n)
    x = bp(x, 1500, 7000) + lp(noise(d), 400) * 0.4
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.3 * SR), (n - np.arange(n)) / (0.4 * SR)))
    return norm(x * fade)


def steps(t0, k, gap, g):
    for i in range(k):
        d = 0.09
        x = lp(noise(d), 700) * env_exp(int(d * SR), 0.015)
        ev(t0 + i * gap, norm(x), g + rng.uniform(-2, 1))


def shutter():
    d = 0.25; n = int(d * SR); x = np.zeros(n)
    c1 = hp(noise(0.006), 3000) * env_exp(int(0.006 * SR), 0.0015); x[:len(c1)] += c1
    m = bp(noise(0.12), 600, 3000) * env_ad(int(0.12 * SR), 0.01, 0.03) * 0.5; a = int(0.015 * SR); x[a:a + len(m)] += m
    c2 = hp(noise(0.006), 2500) * env_exp(int(0.006 * SR), 0.002); b = int(0.075 * SR); x[b:b + len(c2)] += c2 * 0.8
    return norm(x)


def metal_clank():
    d = 0.6; tt = t_(d)
    x = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.15) for f, a in [(420, 1), (1130, 0.5), (2200, 0.3)])
    return norm(x + lp(noise(d), 2000) * env_exp(int(d * SR), 0.01))


P = -11
# 0–15,8 mở đầu
ev(0.0, jungle_amb(8.7), -15)
ev(0.0, S.s_whoosh(2.0, 150, 2500, 0.85), -10)
ev(2.0, S.s_impact(), -8)
ev(2.7, rustle(0.6), -12, 0.4)
ev(2.2, S.s_whoosh(0.4, 300, 2000, 0.5), -14, 0.4)
ev(2.7, boing(700, 380, 0.25), -12, 0.4)
ev(4.25, rustle(0.9), -9, -0.3)
ev(4.9, S.s_pop(1.0), P)
ev(7.2, S.s_whoosh(0.3, 200, 1500, 0.4), -14)
ev(7.3, S.s_pop(0.8), -9)
ev(8.7, S.s_whoosh(0.4, 200, 1800, 0.3), -15)
ev(9.6, S.s_pop(1.0), P)
ev(11.2, S.s_pop(1.15), P)
ev(12.1, jet(1.5), -10)
ev(12.2, S.s_pop(1.0), P)
ev(13.6, S.s_drop(), -10)
ev(13.75, S.s_impact(), -9)
ev(14.4, S.s_stamp(), -8)
# 15,8 bản đồ, Lubang
ev(15.8, S.s_paper(0.3), -14)
ev(15.85, S.s_pop(1.0), P)
ev(16.3, S.s_pop(1.1), P, 0.3)
ev(17.6, S.s_pop(0.95), P, -0.3)
ev(18.0, S.s_marker(0.8), -18)
ev(18.9, S.s_drop(), -11)
ev(20.3, S.s_stamp(), -5)
ev(21.44, jungle_amb(3.0), -16)
steps(21.6, 14, 0.2, -18)
ev(21.6, S.s_pop(1.0), P)
# 24,5 Nhật đầu hàng, truyền đơn
ev(24.6, S.s_impact(), -7)
ev(27.5, jet(2.4), -11)
for k in range(8):
    ev(28.0 + k * 0.3, S.s_paper(0.2), -18, rng.uniform(-0.5, 0.5))
ev(30.2, S.s_pop(1.0), P)
ev(31.75, S.s_paper(0.35), -12)
ev(33.4, S.s_stamp(), -4)
ev(33.5, boing(500, 250, 0.3), -13, 0.4)
ev(35.02, night_amb(3.6), -16)
ev(35.7, S.s_radio(1.6), -12, -0.5)
for k in range(5):
    ev(35.6 + k * 0.4 + 0.6, boing(900, 600, 0.12), -16)
ev(37.3, S.s_pop(0.9), P)
# 38,6 du kích
ev(38.61, night_amb(5.2), -15)
ev(38.7, S.s_pop(1.0), P)
ev(39.8, S.s_pop(1.1), P)
ev(41.1, crackle(2.7), -10)
for k, ts in enumerate([41.7, 42.1, 42.5, 42.9]):
    ev(ts, shot(), -12, (k - 1.5) * 0.3)
ev(43.9, S.s_tick(0.8), -16)
ev(46.3, S.s_impact(), -12)
# 47,4 từng người rời đi
ev(47.39, jungle_amb(5.6), -17)
ev(48.7, S.s_pop(1.0), P)
steps(49.2, 8, 0.19, -17)
ev(51.1, S.s_pop(0.9), P)
ev(51.6, shot(), -13)
ev(53.1, S.s_pop(1.0), P)
ev(54.5, S.s_drop(), -11)
ev(55.2, S.s_paper(0.25), -15, -0.4)
ev(57.7, shot(), -14)
ev(60.78, night_amb(1.8), -16)
ev(60.8, bp(noise(1.8), 800, 6000) * 0 + S.s_hiss(1.8), -16)
ev(61.4, S.s_impact(), -12)
# 62,6 Nhật Bản sững sờ
ev(62.6, S.s_paper(0.35), -11)
ev(63.0, boing(900, 250, 0.4), -10)
ev(63.6, S.s_pop(1.0), P)
ev(66.6, S.s_paper(0.3), -12)
ev(68.3, S.s_stamp(), -5)
ev(69.2, S.s_drop(), -11)
ev(72.0, S.s_stamp(), -6)
# 73,3 Suzuki
ev(73.3, jungle_amb(8.4), -16)
steps(73.5, 24, 0.22, -18)
ev(73.4, S.s_pop(1.0), P)
ev(75.4, S.s_paper(0.25), -15, -0.4)
for k in range(4):
    ev(78.9 + k * 0.8, S.s_clock(), -12)
ev(80.0, rustle(0.8), -9, 0.4)
ev(81.67, shutter(), -4)
ev(80.45, boing(400, 900, 0.25), -10)
ev(80.5, S.s_impact(), -9)
ev(83.3, boing(500, 350, 0.25), -15)
ev(85.2, S.s_pop(0.9), -10)
# 87,7 tìm chỉ huy, đọc lệnh
ev(87.75, jet(1.45), -10)
ev(87.8, S.s_pop(1.0), P)
ev(89.22, S.s_whoosh(0.4, 200, 1800, 0.3), -15)
ev(91.3, S.s_paper(0.25), -15, -0.4)
ev(94.12, jungle_amb(10.0), -17)
ev(94.2, S.s_pop(1.0), P)
steps(96.4, 10, 0.22, -17)
ev(97.4, S.s_pop(1.0), P)
ev(99.0, S.s_impact(), -9)
ev(100.3, S.s_paper(0.35), -12)
ev(101.3, S.s_pop(0.9), -10)
ev(103.0, S.s_ding(), -13)
# 104,1 trình diện, nộp vũ khí, trao kiếm
ev(104.15, S.s_drop(), -11)
ev(104.9, S.s_pop(1.0), P)
ev(107.4, metal_clank(), -10)
for k in range(12):
    ev(109.1 + k * 0.1, S.s_tick(1.2), -15)
for k in range(3):
    ev(110.0 + k * 0.15, metal_clank(), -16)
ev(111.0, S.s_pop(1.0), P)
ev(112.0, S.s_whoosh(1.0, 300, 3000, 0.6), -15)
ev(113.2, metal_clank(), -10)
ev(113.4, S.s_paper(0.25), -15, -0.4)
ev(115.4, S.s_stamp(), -4)
ev(116.8, S.s_pop(1.0), P)
ev(117.0, S.s_ding(), -14)

if __name__ == "__main__":
    B = ROOT / "build"
    S.export(B / "Onoda_v2_nosfx.mp4", B / "Onoda_v2.mp4", pre_gain_db=0.4)
