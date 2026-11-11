"""Hiệu ứng tiếng cho tập Garbo — nhịp lém, sinh động hơn tập Pilecki nhưng luôn thấp hơn giọng.

Chạy sau render.py full:
  python3 src/sfx_events.py   → build/Garbo_v1.mp4 (có hiệu ứng), build/sfx_stem.wav
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, typing, rng, noise, bp, lp, hp, env_exp, env_ad, t_, norm, sweep, SR  # noqa

S.configure(ROOT, 110.016)


def medal(pitch=1.0):
    """Huân chương kim loại: tiếng ngân ngắn, không hài hòa."""
    d = 1.0
    n = int(d * SR)
    tt = t_(d)
    parts = [(1480, 1.0, 0.35), (2210, 0.6, 0.25), (3170, 0.4, 0.18), (4420, 0.25, 0.12)]
    x = sum(a * np.sin(2 * np.pi * f * pitch * tt) * np.exp(-tt / tau) for f, a, tau in parts)
    x += hp(noise(d), 3000) * env_exp(n, 0.004) * 0.6
    return norm(x)


def coin():
    d = 0.4
    tt = t_(d)
    f = rng.uniform(2400, 3400)
    x = (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.48 * tt)) * np.exp(-tt / 0.09)
    return norm(x + hp(noise(d), 4000) * env_exp(int(d * SR), 0.003) * 0.5)


def surf(d):
    n = int(d * SR)
    x = lp(noise(d), 1200) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.4 * t_(d)) ** 2)
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.4 * SR), (n - np.arange(n)) / (0.6 * SR)))
    return norm(x * fade)


def tracks(d):
    """Xích xe tăng: động cơ trầm + tiếng lạch cạch đều."""
    n = int(d * SR)
    tt = t_(d)
    eng = lp(noise(d), 160, 4) + 0.5 * np.sin(2 * np.pi * 42 * tt)
    clank = np.zeros(n)
    k = S.s_tick(0.5)
    pos = 0
    while pos < n - len(k):
        clank[pos:pos + len(k)] += k * rng.uniform(0.3, 0.7)
        pos += int(SR / 11)
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.3 * SR), (n - np.arange(n)) / (0.4 * SR)))
    return norm((eng + clank * 0.6) * fade)


P = -11  # tiếng bật cho chip/nhãn
# 0–8 hai huân chương
ev(0.57, S.s_pop(1.0), P)
ev(2.37, medal(1.0), -6, -0.4)
ev(4.97, medal(1.12), -6, 0.4)
ev(6.95, S.s_radio(0.9), -11)
ev(7.12, S.s_pop(1.1), P - 2)
# 8,15 Pujol
ev(8.12, S.s_drop(), -11)
ev(8.75, S.s_paper(0.25), -14, -0.5)
# 11,1 xin việc
ev(11.2, S.s_pop(1.0), P)
ev(12.5, S.s_drop(), -14, -0.4)
ev(12.9, S.s_pop(0.9), P, -0.4)
ev(14.85, S.s_stamp(), -6, -0.4)
ev(15.8, S.s_whoosh(1.0, 250, 2200, 0.5), -15)
ev(17.2, S.s_pop(0.9), P, 0.4)
ev(18.0, S.s_pop(1.15), P - 2, 0.4)
# 18,5 bản đồ Madrid – London – Lisbon
ev(18.44, S.s_paper(0.3), -15)
ev(18.5, S.s_pop(1.0), P - 2)
ev(18.6, S.s_marker(1.0), -19)
ev(19.2, S.s_pop(1.1), P - 2, 0.3)
ev(20.4, S.s_marker(0.3), -12)
ev(21.87, S.s_pop(0.95), P, -0.4)
ev(23.5, S.s_whoosh(0.9, 300, 2600, 0.5), -15)
ev(24.9, S.s_stamp(), -9, 0.3)
ev(25.0, S.s_pop(1.1), P - 2)
# 26,2 tư liệu
ev(26.3, S.s_pop(1.0), P)
for ts in (27.15, 28.1, 28.8, 29.6):
    ev(ts, S.s_paper(0.25), -13, rng.uniform(-0.4, 0.4))
ev(29.6, S.s_rattle(0.6), -20, 0.4)
# 30,6 lít rượu vang
ev(30.6, S.s_paper(0.35), -12)
typing("Ở GLASGOW CÓ NHỮNG NGƯỜI CHỊU LÀM MỌI THỨ ĐỂ ĐỔI LẤY MỘT LÍT RƯỢU VANG.", 31.8, 34.9, -6)
ev(35.32, S.s_marker(0.4), -12)
ev(35.5, S.s_pop(1.0), P - 2)
ev(36.95, S.s_stamp(), -6)
# 37,9 Anh phát hiện
ev(37.9, S.s_paper(0.3), -13)
ev(38.7, S.s_whoosh(0.5, 300, 2500), -15)
ev(39.4, S.s_pop(1.0), P - 2, -0.4)
ev(40.55, S.s_drop(), -13, 0.4)
# 41,4 Garbo
ev(41.38, S.s_drop(), -11)
ev(41.45, S.s_pop(1.0), P)
ev(43.6, S.s_pop(1.1), P - 2, -0.4)
ev(45.8, S.s_pop(1.0), P - 2, -0.4)
ev(46.85, S.s_stamp(), -5, 0.3)
# 47,75 mạng lưới 27 điệp viên
ev(47.72, S.s_drop(), -11)
ev(49.3, S.s_pop(1.0), P)
for k in range(9):
    ev(51.05 + k * 0.13 + 0.55, coin(), -10, rng.uniform(-0.5, 0.5))
ev(51.2, S.s_pop(0.9), P - 2)
# 53 kế hoạch đổ bộ
ev(52.98, S.s_drop(), -11)
ev(53.1, S.s_pop(1.0), P)
ev(55.45, S.s_paper(0.3), -14)
ev(55.6, S.s_pop(0.95), P, -0.4)
ev(58.4, S.s_pop(1.1), P, 0.4)
ev(58.6, S.s_marker(0.9), -18, 0.4)
# 59,8 hơn 500 bức điện
ev(59.85, S.s_pop(1.0), P)
ev(60.0, S.s_radio(2.5), -10)
ev(62.3, S.s_pop(1.2), P)
# 62,9 ngày D
ev(62.9, surf(3.1), -13)
for ts in (63.3, 64.4, 65.3):
    ev(ts, S.s_boom(), -13, rng.uniform(-0.5, 0.5))
ev(62.95, S.s_pop(1.0), P - 2)
ev(64.2, S.s_pop(1.1), P - 2, -0.4)
ev(66.0, S.s_paper(0.3), -14)
ev(66.1, S.s_pop(1.0), P - 2, -0.3)
ev(66.7, S.s_pop(0.9), P - 2, 0.3)
ev(67.4, S.s_whoosh(1.0, 300, 2500, 0.6), -15)
for k in range(8):
    ev(67.4 + k * 0.125, S.s_clock(), -16)
ev(68.2, S.s_pop(1.0), P - 2, 0.4)
ev(70.4, S.s_stamp(), -6)
# 71,4 bức điện 9/6
ev(71.4, S.s_paper(0.35), -12)
ev(71.5, S.s_pop(1.0), P)
typing("NORMANDY CHỈ LÀ NGHI BINH.", 73.76, 75.1, -5)
typing("ĐỪNG ĐIỀU QUÂN TỚI ĐÓ.", 75.48, 76.3, -5)
typing("TRẬN CHÍNH: PAS-DE-CALAIS.", 76.62, 78.0, -5)
ev(77.6, S.s_marker(0.4), -12)
ev(78.2, S.s_riser(0.28), -12)
ev(78.45, S.s_impact(), -5)
# 79,9 xe tăng dừng lại
ev(79.9, tracks(2.6), -11, 0.3)
ev(81.4, S.s_stamp(), -9)
ev(82.3, S.s_whoosh(1.2, 120, 900, 0.5), -19)
# 84 huân chương
ev(84.05, S.s_drop(), -11)
ev(84.1, S.s_pop(1.0), P)
ev(84.6, S.s_radio(1.6), -12, -0.3)
ev(86.6, medal(1.0), -6, -0.4)
ev(88.15, S.s_pop(1.0), P, 0.4)
ev(88.85, medal(1.12), -6, 0.4)
# 90,2 cáo phó giả
ev(90.2, S.s_paper(0.35), -12)
ev(91.1, S.s_pop(0.9), P - 2, -0.4)
ev(92.3, S.s_stamp(), -6, 0.3)
typing("chết vì sốt rét ở châu Phi", 93.6, 95.2, -9)
typing("1949", 95.5, 95.9, -7)
# 96,6 Venezuela
ev(96.58, S.s_drop(), -11)
ev(96.7, S.s_pop(1.0), P)
ev(98.35, S.s_pop(1.1), P - 2, -0.4)
# 99,5 35 năm sau
for k in range(12):
    ev(99.5 + k * 0.09, S.s_clock(), -15)
ev(99.55, S.s_pop(1.0), P)
ev(100.9, S.s_pop(1.1), P - 2)
# 102,2 bãi biển 1984
ev(102.17, surf(7.8), -16)
ev(102.25, S.s_pop(1.0), P)
ev(104.6, S.s_paper(0.2), -16, -0.4)
ev(105.9, S.s_pop(1.0), P - 2, 0.4)
ev(107.6, S.s_ding(), -13)

if __name__ == "__main__":
    B = ROOT / "build"
    S.export(B / "Garbo_v1_nosfx.mp4", B / "Garbo_v1.mp4", pre_gain_db=0.5)
