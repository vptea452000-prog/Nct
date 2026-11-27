"""Hiệu ứng tiếng cho tập Mincemeat — bí ẩn, chừng mực (có người đã khuất trong câu chuyện).

Chạy sau render.py full:
  python3 src/sfx_events.py   → build/Mincemeat_v1.mp4 (có hiệu ứng), build/sfx_stem.wav
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, typing, rng, noise, bp, lp, hp, env_exp, env_ad, t_, norm, sweep, SR  # noqa

S.configure(ROOT, 104.616)


def surf(d):
    n = int(d * SR)
    x = lp(noise(d), 1100) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.33 * t_(d)) ** 2)
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.5 * SR), (n - np.arange(n)) / (0.7 * SR)))
    return norm(x * fade)


def chain():
    d = 0.5
    out = np.zeros(int(d * SR))
    for k in range(6):
        tt = t_(0.12)
        f = rng.uniform(2600, 4200)
        c = np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.02) + hp(noise(0.12), 3000) * np.exp(-tt / 0.004) * 0.5
        a = int((0.03 + k * 0.06 + rng.uniform(0, 0.02)) * SR)
        out[a:a + len(c)] += c * rng.uniform(0.5, 1.0)
    return norm(out)


def latch():
    d = 0.15
    n = int(d * SR)
    x = bp(noise(d), 1500, 6000) * env_exp(n, 0.006) + np.sin(2 * np.pi * 1700 * t_(d)) * env_exp(n, 0.02) * 0.5
    return norm(x)


def pen(d):
    n = int(d * SR)
    x = bp(noise(d), 2500, 7000) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 3.2 * t_(d))))
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.05 * SR), (n - np.arange(n)) / (0.1 * SR)))
    return norm(x * fade)


def hiss_vapor(d):
    n = int(d * SR)
    return norm(hp(noise(d), 2500) * env_ad(n, 0.15, d * 0.5))


def sub_drone(d):
    n = int(d * SR)
    tt = t_(d)
    x = np.sin(2 * np.pi * 46 * tt) + 0.4 * np.sin(2 * np.pi * 69 * tt) + 0.3 * lp(noise(d), 180)
    x += np.sin(2 * np.pi * 1200 * tt) * (np.sin(2 * np.pi * 0.7 * tt) > 0.995) * 0.5  # tiếng sonar thưa
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.4 * SR), (n - np.arange(n)) / (0.6 * SR)))
    return norm(x * fade)


def wind(d):
    n = int(d * SR)
    x = bp(noise(d), 180, 900, 2) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.2 * t_(d)))
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.6 * SR), (n - np.arange(n)) / (1.0 * SR)))
    return norm(x * fade)


def tracks(d):
    n = int(d * SR)
    eng = lp(noise(d), 160, 4) + 0.5 * np.sin(2 * np.pi * 42 * t_(d))
    clank = np.zeros(n)
    k = S.s_tick(0.5)
    pos = 0
    while pos < n - len(k):
        clank[pos:pos + len(k)] += k * rng.uniform(0.3, 0.7)
        pos += int(SR / 11)
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.3 * SR), (n - np.arange(n)) / (0.4 * SR)))
    return norm((eng + clank * 0.6) * fade)


T = -13
# 0–6,65 Huelva
ev(0.0, surf(6.6), -14)
ev(0.45, S.s_tick(0.8), T)
ev(2.4, S.s_paper(0.25), -18, -0.4)
ev(5.85, S.s_pop(0.9), -12, 0.3)
# 6,65 chiếc cặp
ev(6.7, S.s_drop(), -10)
ev(7.25, chain(), -10, 0.4)
ev(8.3, latch(), -8)
ev(8.7, S.s_paper(0.4), -12)
ev(9.4, S.s_stamp(), -6)
ev(10.0, S.s_tick(0.8), T)
# 11,6 thẻ giả
ev(11.58, S.s_drop(), -11)
ev(12.6, S.s_stamp(), -6, 0.3)
ev(14.4, S.s_tick(0.8), T)
# 16 Địa Trung Hải
ev(16.05, S.s_paper(0.3), -14)
ev(16.15, S.s_tick(0.8), T)
ev(18.1, S.s_pop(1.0), -12, 0.2)
ev(19.2, S.s_marker(1.0), -18)
ev(24.7, S.s_pop(0.9), -12, 0.5)
ev(25.35, S.s_pop(1.0), -12, -0.5)
# 26 Glyndwr Michael
ev(26.25, S.s_whoosh(0.6, 120, 900, 0.4), -20)
ev(28.95, S.s_paper(0.25), -16, -0.4)
# 31,8 danh tính mới
ev(32.2, S.s_tick(0.8), T)
ev(33.3, S.s_paper(0.3), -14, -0.4)
# 35,9 đồ trong túi
ev(37.5, S.s_tick(0.8), T)
for ts, _ in [(40.05, 0), (40.85, 0), (42.25, 0), (43.2, 0), (44.5, 0), (45.45, 0)]:
    ev(ts - 0.1, S.s_paper(0.22), -13, rng.uniform(-0.4, 0.4))
# 48,2 Pam
ev(48.2, S.s_drop(), -12)
ev(49.6, S.s_tick(0.8), T)
# 50,8 hai vị tướng, bản nháp, Nye tự viết
ev(50.9, S.s_tick(0.8), T)
ev(52.9, S.s_drop(), -13, -0.4)
ev(54.2, S.s_drop(), -13, 0.4)
ev(53.6, S.s_whoosh(0.8, 300, 2500), -16)
for k in range(4):
    ev(55.5 + k * 0.28, S.s_paper(0.35), -14, rng.uniform(-0.5, 0.5))
ev(57.3, pen(1.3), -14)
# 58,7 nội dung thư
ev(58.7, S.s_paper(0.3), -13)
typing("ĐỨC ĐANG TĂNG QUÂN Ở HY LẠP.", 58.8, 60.2, -6)
typing("ĐỒNG MINH PHẢI TĂNG LỰC LƯỢNG TẤN CÔNG.", 60.6, 62.2, -6)
typing("SICILY: CHỈ ĐỂ ĐÁNH LẠC HƯỚNG.", 62.5, 64.4, -6)
ev(63.6, S.s_marker(0.6), -12)
# 64,8 hộp thép, tàu ngầm
ev(64.9, S.s_drop(), -9)
ev(65.3, hiss_vapor(1.6), -14)
ev(66.85, sub_drone(3.5), -12)
# 70,4 Tây Ban Nha
ev(70.45, S.s_tick(0.8), T)
ev(71.4, S.s_tick(1.0), T)
ev(72.3, S.s_whoosh(1.2, 250, 2200, 0.5), -16)
# 74,6 chiếc cặp trả về
ev(74.6, S.s_tick(0.8), T)
ev(75.3, S.s_whoosh(1.0, 200, 1800, 0.5), -16)
ev(75.6, S.s_tick(0.9), T)
# 76,9 giải mã 14/5
ev(76.95, S.s_tick(0.8), T)
ev(77.0, S.s_radio(1.6), -12)
ev(78.1, S.s_whoosh(0.6, 300, 2500), -16)
typing("MỤC TIÊU ĐỒNG MINH:", 80.0, 80.9, -7)
typing("HY LẠP", 81.2, 81.7, -5)
ev(81.95, S.s_stamp(), -6)
# 82,2 Đức điều quân
ev(82.25, S.s_tick(0.8), T)
ev(82.9, S.s_marker(0.8), -16, -0.4)
ev(83.4, S.s_marker(0.8), -16, 0.4)
ev(84.6, tracks(2.7), -12)
# 87,6 đổ bộ Sicily
ev(87.7, S.s_tick(0.8), T)
ev(89.5, surf(2.0), -14)
ev(89.6, S.s_whoosh(1.2, 200, 1800, 0.6), -15)
# 91,5 Huelva, 1998
ev(91.5, wind(13.1), -21)
ev(95.0, S.s_marker(0.4), -16)
ev(96.6, S.s_tick(0.8), T)
ev(100.1, S.s_marker(0.6), -15)
ev(100.4, S.s_paper(0.3), -16)

if __name__ == "__main__":
    B = ROOT / "build"
    S.export(B / "Mincemeat_v1_nosfx.mp4", B / "Mincemeat_v1.mp4", pre_gain_db=0.2)
