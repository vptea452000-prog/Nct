"""Hiệu ứng tiếng cho tập Petrov — căng thẳng, kiểu phòng trực đêm thời Chiến tranh Lạnh.

Chạy sau render.py full:
  python3 src/sfx_events.py   → build/Petrov_v1.mp4 (có hiệu ứng), build/sfx_stem.wav
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, typing, rng, noise, bp, lp, hp, env_exp, env_ad, t_, norm, sweep, SR  # noqa

S.configure(ROOT, 104.088)


def hum(d, f=50):
    """Tiếng ù của máy móc trong boong-ke."""
    n = int(d * SR)
    tt = t_(d)
    x = np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * 2 * f * tt) + 0.25 * np.sin(2 * np.pi * 3 * f * tt) + 0.2 * lp(noise(d), 300)
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.5 * SR), (n - np.arange(n)) / (0.6 * SR)))
    return norm(x * fade)


def siren(d):
    """Còi báo động lên xuống."""
    n = int(d * SR)
    tt = t_(d)
    f = 650 + 300 * np.sin(2 * np.pi * 0.75 * tt - np.pi / 2)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * 0.5 + np.sin(ph)
    x = lp(x, 3000)
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.15 * SR), (n - np.arange(n)) / (0.4 * SR)))
    return norm(x * fade)


def beep(f=1400, d=0.12):
    n = int(d * SR)
    x = np.sin(2 * np.pi * f * t_(d)) * np.minimum(1, np.minimum(np.arange(n) / 200, (n - np.arange(n)) / 400))
    return norm(x)


def ring_phone(d):
    """Chuông điện thoại cơ: hai tần số rung nhanh, ngắt quãng."""
    n = int(d * SR)
    tt = t_(d)
    bell = (np.sin(2 * np.pi * 1700 * tt) + np.sin(2 * np.pi * 2100 * tt)) * (np.sin(2 * np.pi * 20 * tt) > 0)
    gate = ((tt % 1.0) < 0.6).astype(float)
    return norm(bell * gate * np.exp(-0 * tt))


def heartbeat(t0, n_beats, gap, g):
    for i in range(n_beats):
        d = 0.18
        x = lp(noise(d), 90, 4) * env_exp(int(d * SR), 0.05) + np.sin(2 * np.pi * 50 * t_(d)) * env_exp(int(d * SR), 0.06)
        ev(t0 + i * gap, norm(x), g)
        ev(t0 + i * gap + 0.22, norm(x), g - 4)


def clunk():
    d = 0.3
    n = int(d * SR)
    return norm(lp(noise(d), 900) * env_exp(n, 0.03) + np.sin(2 * np.pi * 120 * t_(d)) * env_exp(n, 0.05))


P = -12
# 0–5,6 phòng trực đêm
ev(0.0, hum(14.0), -24)
ev(0.6, S.s_tick(0.8), P)
ev(0.9, beep(900, 0.2), -12)
typing("HỆ THỐNG CẢNH BÁO SỚM", 2.5, 3.6, -9)
ev(4.15, S.s_boom(), -10)
ev(4.2, S.s_pop(0.9), P)
# 5,6 có báo lên không
ev(5.6, clunk(), -10)
ev(7.3, S.s_pop(1.0), P)
ev(8.6, S.s_pop(1.1), P - 2, -0.4)
ev(8.7, S.s_pop(1.2), P - 2, 0.4)
# 9,9 Petrov
ev(9.9, S.s_drop(), -11)
ev(10.8, S.s_paper(0.25), -15, -0.4)
# 14 Serpukhov-15, vệ tinh
ev(14.0, S.s_drop(), -11)
ev(14.3, S.s_pop(1.0), P)
ev(16.5, S.s_whoosh(0.5, 150, 1500, 0.4), -18)
ev(18.4, beep(1200, 0.1), -14, -0.4)
ev(18.7, beep(1300, 0.1), -14, 0.4)
for k in range(5):
    ev(20.7 + k * 0.35, beep(1800, 0.06), -18, -0.3)
# 22,6 nhiệm vụ
ev(22.6, S.s_pop(1.0), P)
ev(23.6, S.s_stamp(), -7)
ev(24.7, S.s_pop(1.0), P)
ev(25.6, S.s_stamp(), -7)
# 26,9 KAL 007
ev(26.87, S.s_drop(), -11)
ev(27.2, S.s_pop(0.9), P)
ev(29.1, S.s_pop(1.0), P)
ev(30.4, S.s_boom(), -15)
# 32,6 BÁO ĐỘNG
ev(32.6, siren(8.0), -15)
ev(33.75, S.s_impact(), -5)
ev(35.2, beep(1500, 0.15), -8)
for k in range(4):
    ev(36.5 + k * 0.22, beep(1500 + k * 80, 0.12), -8)
ev(38.75, S.s_impact(), -6)
# 40,6 Petrov không tin
heartbeat(40.7, 6, 0.9, -12)
ev(40.65, S.s_pop(0.9), P)
ev(44.6, S.s_pop(0.8), P)
ev(46.3, S.s_drop(), -11)
ev(46.4, S.s_pop(1.0), P)
ev(49.4, S.s_pop(0.8), P)
ev(50.84, S.s_pop(1.0), P)
typing("LỖI HỆ THỐNG", 51.5, 52.5, -6)
# 53 chờ 23 phút
for k in range(int((59.4 - 53.2) / 0.27)):
    ev(53.2 + k * 0.27, S.s_clock(), -12)
heartbeat(53.4, 6, 1.0, -15)
ev(58.4, S.s_pop(1.0), P)
ev(59.8, S.s_stamp(), -5)
# 60,9 nguyên nhân
ev(61.9, S.s_pop(0.9), P)
ev(63.0, S.s_riser(0.4), -16)
ev(64.7, S.s_ding(), -14)
ev(65.6, S.s_pop(0.9), P, 0.4)
# 67,5 hậu quả
ev(67.5, S.s_pop(0.9), P)
ev(68.8, S.s_paper(0.35), -12)
ev(69.7, S.s_stamp(), -5)
ev(72.4, S.s_pop(1.0), P)
for k in range(10):
    ev(74.0 + k * 0.17, S.s_clock(), -14)
ev(74.0, S.s_pop(1.0), P)
ev(77.85, S.s_drop(), -11)
ev(78.3, S.s_paper(0.25), -15, -0.4)
ev(81.6, S.s_drop(), -11)
ev(83.4, S.s_ding(), -12)
# 85 Fryazino, 2017
ev(86.8, S.s_pop(1.0), P)
ev(88.6, S.s_drop(), -12)
ev(88.65, S.s_pop(0.9), P)
ev(92.0, S.s_pop(0.9), P)
ev(94.1, S.s_pop(1.0), P)
ev(96.4, ring_phone(2.0), -11)
ev(98.5, clunk(), -10)
ev(98.6, S.s_pop(0.9), P - 2)

if __name__ == "__main__":
    B = ROOT / "build"
    S.export(B / "Petrov_v1_nosfx.mp4", B / "Petrov_v1.mp4", pre_gain_db=0.3)
