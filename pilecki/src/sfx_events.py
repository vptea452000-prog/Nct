"""Hiệu ứng tiếng cho tập Pilecki — tiết chế, trang nghiêm (không tiếng 'bật' vui tai).

Mỗi hiệu ứng bám mốc chuyển động trong scenes.py. Chạy sau render.py full:
  python3 src/sfx_events.py   → build/Pilecki_v1.mp4 (có hiệu ứng), build/sfx_stem.wav
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, typing, rng, noise, bp, lp, hp, env_exp, env_ad, t_, norm, sweep, SR  # noqa

S.configure(ROOT, 102.432)


# ---------------------------------------------------------------- âm riêng của tập
def shutter():
    """Màn trập máy ảnh hồ sơ: tách – xoẹt – tách."""
    d = 0.25
    n = int(d * SR)
    x = np.zeros(n)
    c1 = hp(noise(0.006), 3000) * env_exp(int(0.006 * SR), 0.0015)
    x[:len(c1)] += c1 * 1.0
    mech = bp(noise(0.12), 600, 3000) * env_ad(int(0.12 * SR), 0.01, 0.03) * 0.5
    a = int(0.015 * SR)
    x[a:a + len(mech)] += mech
    c2 = hp(noise(0.006), 2500) * env_exp(int(0.006 * SR), 0.002)
    b = int(0.075 * SR)
    x[b:b + len(c2)] += c2 * 0.8
    return norm(x)


def knock():
    """Búa gỗ phiên tòa."""
    d = 0.18
    n = int(d * SR)
    x = np.sin(2 * np.pi * 190 * t_(d)) * env_exp(n, 0.035) + bp(noise(d), 700, 2600) * env_exp(n, 0.008) * 0.8
    return norm(x)


def clang():
    """Cửa sắt nhà tù đóng: các họa âm kim loại không hài hòa, tắt dần."""
    d = 2.2
    n = int(d * SR)
    tt = t_(d)
    parts = [(98, 1.0, 0.9), (231, 0.6, 0.7), (347, 0.45, 0.55), (512, 0.3, 0.45), (811, 0.2, 0.3), (1130, 0.12, 0.2)]
    x = sum(a * np.sin(2 * np.pi * f * tt + rng.uniform(0, 6)) * np.exp(-tt / tau) for f, a, tau in parts)
    hit = lp(noise(d), 2500) * env_exp(n, 0.02) * 1.5
    thud = sweep(80, 45, d) * env_exp(n, 0.12)
    return norm(lp(x, 3000) + hit + thud)


def shot_far():
    """Tiếng súng vọng xa (đã làm đục)."""
    d = 1.0
    n = int(d * SR)
    crack = lp(noise(d), 2200) * env_exp(n, 0.012)
    body = lp(noise(d), 400) * env_exp(n, 0.08) * 0.8
    tail = lp(noise(d), 900) * env_ad(n, 0.04, 0.35) * 0.25
    return norm(crack + body + tail)


def wind(d):
    n = int(d * SR)
    x = bp(noise(d), 180, 900, 2)
    x *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * t_(d) + 1.3) * np.sin(2 * np.pi * 0.07 * t_(d))
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.6 * SR), (n - np.arange(n)) / (0.8 * SR)))
    return norm(x * fade)


def drone(d, f=55):
    n = int(d * SR)
    tt = t_(d)
    x = np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.5 * tt) + 0.3 * lp(noise(d), 200)
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.5 * SR), (n - np.arange(n)) / (0.7 * SR)))
    return norm(x * fade)


def snip():
    d = 0.2
    n = int(d * SR)
    x = hp(noise(d), 3500) * env_exp(n, 0.004) + np.sin(2 * np.pi * 2900 * t_(d)) * env_exp(n, 0.03) * 0.4
    return norm(x)


def creak(d=0.6):
    n = int(d * SR)
    tt = t_(d)
    f = 260 + 220 * np.sin(np.pi * tt / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    fr = (np.sin(ph) > 0.6).astype(float)
    x = bp(fr + 0.2 * noise(d), 400, 2500) * env_ad(n, 0.1, 0.25)
    return norm(x)


def steps(t0, n_steps, gap, g, pan=0.0):
    for i in range(n_steps):
        d = 0.09
        x = lp(noise(d), 700) * env_exp(int(d * SR), 0.015) + np.sin(2 * np.pi * 90 * t_(d)) * env_exp(int(d * SR), 0.02) * 0.5
        ev(t0 + i * gap + rng.uniform(-0.02, 0.02), norm(x), g + rng.uniform(-2, 1), pan + rng.uniform(-0.2, 0.2))


T = -16  # tiếng gõ nhẹ cho chip/nhãn (thay cho tiếng "bật")

# 0–8,05 Warsaw
ev(0.0, S.s_rumble(4.6), -18)
ev(0.40, S.s_tick(0.8), T)
ev(4.0, S.s_paper(0.2), -18, -0.4)
steps(4.95, 9, 0.13, -20)
ev(6.40, S.s_rumble(1.2), -16, 0.5)
ev(6.5, S.s_tick(0.8), T)
steps(6.65, 5, 0.26, -18, 0.2)
# 8,05 bản đồ
ev(8.02, S.s_paper(0.3), -16)
ev(8.6, S.s_marker(0.65), -20)
ev(8.95, S.s_tick(0.9), T)
# 9,67 chân dung
ev(9.62, S.s_whoosh(0.45, 150, 1400, 0.3), -20)
ev(10.35, S.s_paper(0.25), -16, -0.5)
# 13,27 cổng trại
ev(13.27, wind(2.4), -22)
ev(13.4, S.s_tick(0.8), T)
ev(14.6, S.s_paper(0.2), -18, -0.4)
# 15,6 hàng rào + nhiệm vụ
ev(15.6, S.s_zip(0.6), -24)
ev(18.6, S.s_paper(0.25), -16, -0.5)
for ts in (19.85, 20.55, 22.80):
    ev(ts, S.s_tick(0.9), -14, -0.4)
for i in range(5):
    ev(20.6 + i * 0.18, S.s_tick(1.1), -22, 0.4)
ev(22.9, S.s_paper(0.4), -17, -0.3)
# 24,2 giấy tờ giả
ev(24.18, S.s_paper(0.35), -12)
ev(24.55, S.s_stamp(), -8)
# 25,3 hai ngày
for i in range(3):
    ev(25.45 + i * 0.12, S.s_clock(), -16)
ev(26.0, S.s_tick(0.8), T)
# 28,7 chuyển tới Auschwitz
ev(28.68, S.s_paper(0.3), -16)
ev(28.80, S.s_rumble(1.4), -15)
ev(29.25, S.s_tick(0.9), T)
# 30,3 ảnh hồ sơ 4859
ev(30.29, shutter(), -6)
ev(31.9, S.s_marker(0.5), -16)
ev(32.0, S.s_tick(0.8), T)
typing("TOMASZ SERAFIŃSKI", 33.25, 34.4, -6)
ev(35.0, S.s_marker(0.4), -12)
ev(35.5, S.s_paper(0.2), -16, 0.4)
# 36,3 mạng lưới trong trại
ev(36.30, S.s_drop(), -12)
for i in range(9):
    ev(36.6 + i * 0.16, S.s_tick(1.1), -22, rng.uniform(-0.4, 0.4))
ev(38.4, S.s_marker(1.5), -22)
ev(42.9, S.s_paper(0.4), -17, -0.5)
# 44,5 Gestapo
ev(44.55, S.s_tick(0.8), T)
ev(46.3, drone(3.4, 48), -15)
for ts in (48.75, 48.95, 49.15, 49.3):
    ev(ts, S.s_drop(), -16)
# 49,75 quyết định
ev(49.72, S.s_drop(), -12)
# 52,2–64,6 đêm
ev(52.17, wind(12.6), -20)
ev(52.9, S.s_tick(0.8), T)
ev(53.4, S.s_tick(0.8), T)
ev(55.1, S.s_tick(0.8), T)
ev(58.55, snip(), -10, 0.5)
ev(59.7, creak(0.6), -14, 0.2)
steps(59.9, 10, 0.14, -16, 0.4)
for ts in (62.3, 62.75, 63.1, 63.6):
    ev(ts, shot_far(), -11, -0.5)
# 64,6 ngày tháng
ev(64.65, S.s_tick(0.8), T)
ev(65.6, S.s_tick(0.8), T)
# 67,4 báo cáo
ev(67.36, S.s_paper(0.3), -14)
for i in range(16):
    for k in range(3):
        ev(67.45 + i * 1.0 / 16 + k * 0.018, S.s_key(), -12, rng.uniform(-0.2, 0.2))
ev(68.7, S.s_whoosh(0.9, 200, 2000, 0.5), -18)
ev(70.6, S.s_paper(0.2), -20, -0.5)
# 72,3 sau chiến tranh
ev(72.35, S.s_tick(0.8), T)
ev(73.3, drone(1.8, 52), -19)
ev(75.4, S.s_paper(0.2), -18, -0.5)
ev(78.2, S.s_whoosh(0.8, 150, 1500, 0.6), -18)
# 80,2 bị bắt, phiên tòa
ev(80.19, shutter(), -6)
ev(80.25, S.s_tick(0.8), T)
ev(83.15, S.s_tick(0.8), T)
ev(84.7, knock(), -10)
ev(84.95, knock(), -12)
# 85,9 thi hành án
ev(85.88, S.s_paper(0.3), -13)
ev(86.6, S.s_marker(0.5), -17)
ev(88.36, wind(2.6), -24)
ev(89.4, clang(), -9)
# 91,0 chôn bí mật
ev(91.03, drone(1.6, 44), -20)
# 92,5 vô tội
ev(92.52, S.s_drop(), -13)
ev(94.4, S.s_paper(0.2), -18)
ev(95.6, S.s_stamp(), -7)
# 96,5 báo cáo còn lại / 98,8 mộ tượng trưng
ev(96.48, S.s_paper(0.3), -14)
ev(98.83, wind(3.5), -21)

# cả lớp hiệu ứng +5 dB: tiết chế nhưng vẫn nghe được trên loa điện thoại (~10–15 dB dưới giọng)
S.EVENTS[:] = [(t, x, g + 5, p) for t, x, g, p in S.EVENTS]

if __name__ == "__main__":
    B = ROOT / "build"
    S.export(B / "Pilecki_v1_nosfx.mp4", B / "Pilecki_v1.mp4", pre_gain_db=1.4)
