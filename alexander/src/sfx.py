"""Âm thanh Alexander: nền trầm (pad dây kiểu điện ảnh, không giai điệu), gió sa mạc, đám đông, trống ở cao trào.
Giọng đọc đã lùi 4,5 s (audio/voice.mp3). Hiệu ứng tự hạ khi có lời (sfx_lib)."""
import sys, json
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa

OFF = 4.5
DUR = OFF + 387.71 + 1.5
S.configure(ROOT, DUR)
T = lambda tv: tv + OFF


def fade(x, a=1.0, b=1.0):
    n = len(x); i = np.arange(n)
    return x * np.minimum(1, np.minimum(i / max(1, a * SR), (n - i) / max(1, b * SR)))


def pad(d, root=55.0, chord=(1, 1.5, 2, 3), bright=0.25, mod=0.07):
    """Lớp dây trầm: tổng sóng hài lệch nhẹ, lọc thấp, mở/đóng chậm."""
    tt = t_(d)
    x = np.zeros(len(tt))
    for i, m in enumerate(chord):
        for det in (-0.12, 0.0, 0.12):
            f = root * m * (1 + det / 100)
            ph = np.random.default_rng(i * 7 + int(det * 100) + 50).uniform(0, 6.28)
            x += np.sin(2 * np.pi * f * tt + ph) * (1.0 / (i + 1)) + bright * np.sin(4 * np.pi * f * tt + ph) / (i + 2)
    x *= 0.7 + 0.3 * np.sin(2 * np.pi * mod * tt)
    return norm(fade(lp(x, 1600), 3.0, 3.0))


def wind(d):
    tt = t_(d)
    return norm(fade(bp(noise(d), 150, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * tt) ** 2), 2, 2))


def crowd(d, angry=1.0):
    tt = t_(d); out = np.zeros(len(tt)); r = np.random.default_rng(5)
    for k in range(40):           # nhiều "giọng" đám đông (tiếng ồn có cao độ, không lời)
        f0 = r.uniform(110, 260); ph = r.uniform(0, 6.28)
        f = f0 * (1 + 0.08 * np.sin(2 * np.pi * r.uniform(0.3, 1.2) * tt + ph))
        env = np.clip(np.sin(2 * np.pi * r.uniform(0.15, 0.5) * tt + ph), 0, 1) ** 2
        out += np.sin(2 * np.pi * np.cumsum(f) / SR) * env
    x = bp(out, 200, 2200) * 0.6 + bp(noise(d), 300, 2500) * 0.5 * angry
    return norm(fade(x, 0.6, 1.2))


def drum(f=55, d=1.6):
    tt = t_(d)
    return norm(np.sin(2 * np.pi * f * tt * (1 - 0.25 * tt / d)) * np.exp(-tt / 0.35) + lp(noise(d), 180) * np.exp(-tt / 0.12) * 0.6)


def whoosh(d=1.0):
    return S.s_whoosh(d, 200, 1600, 0.6)


def chime(f=440, d=3.0):
    tt = t_(d)
    return norm(sum(np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * (0.8 + k)) / k for k in (1, 2, 3)))


# nền xuyên suốt: pad theo từng chương (đổi hợp âm êm), gió nhẹ
for a, b, root, chord in [(0.0, T(69.4), 55.0, (1, 1.5, 2, 2.4)), (T(69.4), T(143.4), 49.0, (1, 1.5, 2, 3)),
                          (T(143.4), T(258.3), 55.0, (1, 1.5, 2, 3)), (T(258.3), T(293.2), 41.2, (1, 1.5, 2, 2.4)),
                          (T(293.2), T(353.3), 46.2, (1, 1.2, 1.5, 2)), (T(353.3), DUR, 41.2, (1, 1.5, 2, 2.4))]:
    ev(a, pad(b - a + 3.0, root, chord), -27)
ev(0.0, wind(DUR), -32)
# intro: đám đông la ó rồi tắt; một nhịp trống khi tiêu đề hiện
ev(0.0, crowd(4.6), -16); ev(1.3, drum(49, 2.4), -12); ev(1.3, chime(330, 4.0), -26)
# đám đông ở cảnh nổi loạn
ev(T(50.0), crowd(11.2), -22)
ev(T(61.2), drum(62, 1.2), -18)
# chuyển cảnh bản đồ: tiếng lướt nhẹ
for tv in (9.11, 13.01, 108.05, 136.62, 152.5, 160.5, 262.27, 353.29, 368.88):
    ev(T(tv) - 0.3, whoosh(1.2), -26)
# cao trào "thì tất cả hãy đi đi!" và "Đi đi!"
ev(T(258.27), norm(S.sweep(80, 160, 2.6) * np.linspace(0, 1, int(2.6 * SR)) ** 2), -22)
ev(T(258.27) + 2.6, drum(45, 2.4), -6)
ev(T(292.20), drum(41, 3.0), -4); ev(T(292.20) + 0.02, norm(lp(noise(1.2), 300) * env_exp(int(1.2 * SR), 0.3)), -14)
# cửa cung điện đóng
ev(T(293.6), norm(lp(noise(0.8), 260) * env_exp(int(0.8 * SR), 0.12) + np.sin(2 * np.pi * 60 * t_(0.8)) * np.exp(-t_(0.8) / 0.2)), -12)
# lính ném vũ khí, khóc xin (tiếng kim loại rơi + đám đông nhỏ)
for k in range(6):
    ev(T(312.5) + k * 0.35, norm(np.sin(2 * np.pi * (900 + k * 70) * t_(0.5)) * np.exp(-t_(0.5) / 0.08) + hp(noise(0.5), 3000) * np.exp(-t_(0.5) / 0.03) * 0.4), -22)
ev(T(311.5), crowd(9.0, angry=0.3), -28)
# hòa giải, cái chết, kết
ev(T(339.3), chime(523, 3.5), -26)
ev(T(361.4), drum(41, 3.0), -16)
ev(T(374.5), chime(392, 5.0), -24)

if __name__ == "__main__":
    S.export(ROOT / "build" / "Alexander_nosfx.mp4", ROOT / "build" / "Alexander_v1.mp4", pre_gain_db=1.5, limit=0.70)
