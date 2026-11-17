"""Hiệu ứng tiếng cho tập Neanderthal. Chạy sau render.py full."""
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, rng, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa

S.configure(ROOT, 85.248)


def boing(f0=700, f1=300, d=0.3):
    return norm(S.sweep(f0, f1, d) * env_exp(int(d * SR), 0.12))


def sparkle():
    d = 0.6; tt = t_(d)
    x = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.18) for f in (1800, 2400, 3200))
    return norm(x)


def wind(d):
    n = int(d * SR)
    x = bp(noise(d), 200, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t_(d)))
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.4 * SR), (n - np.arange(n)) / (0.5 * SR))))


def blip(f=900):
    d = 0.08
    return norm(np.sin(2 * np.pi * f * t_(d)) * env_exp(int(d * SR), 0.03))


def steps(t0, k, gap, g):
    for i in range(k):
        d = 0.09
        ev(t0 + i * gap, norm(lp(noise(d), 700) * env_exp(int(d * SR), 0.015)), g + rng.uniform(-2, 1))


P = -11
ev(0.0, S.s_whoosh(0.6, 200, 2000, 0.5), -14)
ev(0.4, S.s_pop(1.0), P)
ev(0.5, boing(500, 800, 0.25), -13, 0.4)
ev(2.6, sparkle(), -9)
ev(2.65, boing(900, 300, 0.35), -12, 0.4)
ev(4.8, S.s_impact(), -7)
ev(4.85, S.s_riser(0.2), -14)
ev(5.1, S.s_pop(1.0), P)
ev(5.97, S.s_paper(0.3), -14)
ev(6.2, S.s_marker(0.8), -16)
ev(6.9, S.s_pop(1.0), P, -0.3)
ev(7.7, S.s_pop(1.1), P, 0.3)
steps(6.0, 10, 0.24, -19)
ev(8.6, S.s_whoosh(1.0, 200, 1500, 0.7), -15)
ev(9.6, S.s_pop(1.0), P, -0.4)
ev(9.75, S.s_pop(1.1), P, 0.4)
ev(12.0, S.s_marker(1.5), -16)
ev(13.7, wind(2.0), -18)
steps(13.7, 6, 0.13, -17)
ev(14.7, sparkle(), -10)
ev(15.8, S.s_pop(1.0), P)
ev(16.4, sparkle(), -11)
for k in range(10):
    ev(18.0 + k * 0.3, blip(700 + k * 60), -16)
ev(21.4, S.s_drop(), -11)
ev(22.4, S.s_riser(1.0), -15)
ev(24.8, S.s_pop(1.0), P)
for k in range(4):
    ev(25.5 + k * 0.15, blip(1200), -14)
ev(26.8, S.s_whoosh(0.4, 300, 2000), -15)
for k in range(30):
    ev(26.8 + k * 0.026, S.s_tick(1.2), -22)
ev(28.6, S.s_marker(0.6), -14)
ev(29.2, S.s_pop(1.0), P)
ev(32.6, S.s_marker(1.0), -15)
ev(35.0, S.s_pop(1.0), P)
ev(36.2, S.s_riser(0.6), -16, -0.3)
ev(38.6, S.s_riser(0.6), -16, 0.3)
ev(39.7, boing(800, 300, 0.35), -10, 0.4)
ev(40.9, S.s_paper(0.3), -14)
ev(41.2, S.s_stamp(), -7)
ev(42.65, sparkle(), -9)
ev(44.4, S.s_impact(), -12)
ev(46.7, S.s_pop(0.9), P)
for k in range(8):
    ev(48.0 + k * 0.06, S.s_pop(1.0 + k * 0.05), -15)
for k in range(5):
    ev(50.4 + k * 0.6 + 0.5, S.s_drop(), -14, rng.uniform(-0.4, 0.4))
ev(52.0, S.s_pop(1.0), P)
ev(55.0, S.s_ding(), -11)
ev(57.0, S.s_rattle(1.2), -16)
ev(60.4, S.s_pop(1.0), P, -0.4)
ev(60.8, S.s_pop(1.1), P, 0.4)
ev(61.5, wind(4.3), -15)
ev(64.5, sparkle(), -12)
ev(65.9, S.s_impact(), -10)
ev(68.0, S.s_pop(0.9), P, -0.4)
ev(68.9, S.s_pop(0.85), P, 0.4)
for k in range(14):
    ev(70.0 + k * 0.13, S.s_tick(1.1), -18)
ev(72.8, S.s_whoosh(0.4, 200, 2000), -15)
ev(75.6, S.s_hiss(0.8), -13)
ev(75.7, boing(600, 250, 0.35), -12)
ev(77.3, wind(3.0), -16)
steps(77.3, 10, 0.3, -20)
ev(79.4, S.s_stamp(), -8)
ev(80.4, S.s_whoosh(3.6, 2500, 200, 0.2), -17)
ev(82.0, sparkle(), -10)
ev(83.0, boing(500, 800, 0.25), -14, 0.4)

if __name__ == "__main__":
    B = ROOT / "build"
    S.export(B / "Neanderthal_v1_nosfx.mp4", B / "Neanderthal_v1.mp4", pre_gain_db=0.2)
