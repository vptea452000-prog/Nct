"""Âm thanh Hitler: nền trầm u tối (pad dây), tiếng đám đông ở cảnh mít tinh, trống ở mốc lớn, lửa, kính vỡ, máy bay.
Giọng đọc đã lùi 4,5 s (audio/voice.mp3). Hiệu ứng tự hạ khi có lời (sfx_lib)."""
import sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, noise, bp, lp, hp, env_exp, t_, norm, SR  # noqa

OFF = 4.5
DUR = OFF + 435.65 + 1.5
S.configure(ROOT, DUR)
import json
SEGS = json.load(open(ROOT / "audio" / "segments.json"))


def T(x):
    """giây kịch bản (giọng đã sắp) → giây video trên giọng gốc (giọng gốc giữ nguyên, câu có thể đọc lệch thứ tự)."""
    for i, o0, o1, r0, r1 in SEGS:
        if r0 <= x < r1:
            return x - r0 + o0 + OFF
    return x + OFF


def fade(x, a=1.0, b=1.0):
    n = len(x); i = np.arange(n)
    return x * np.minimum(1, np.minimum(i / max(1, a * SR), (n - i) / max(1, b * SR)))


def pad(d, root=55.0, chord=(1, 1.5, 2, 3), bright=0.2, mod=0.06):
    tt = t_(d); x = np.zeros(len(tt))
    for i, m in enumerate(chord):
        for det in (-0.12, 0.0, 0.12):
            f = root * m * (1 + det / 100)
            ph = np.random.default_rng(i * 7 + int(det * 100) + 50).uniform(0, 6.28)
            x += np.sin(2 * np.pi * f * tt + ph) / (i + 1) + bright * np.sin(4 * np.pi * f * tt + ph) / (i + 2)
    x *= 0.7 + 0.3 * np.sin(2 * np.pi * mod * tt)
    return norm(fade(lp(x, 1400), 3.0, 3.0))


def crowd(d, angry=1.0):
    tt = t_(d); out = np.zeros(len(tt)); r = np.random.default_rng(5)
    for k in range(40):
        f0 = r.uniform(110, 260); ph = r.uniform(0, 6.28)
        f = f0 * (1 + 0.08 * np.sin(2 * np.pi * r.uniform(0.3, 1.2) * tt + ph))
        env = np.clip(np.sin(2 * np.pi * r.uniform(0.15, 0.5) * tt + ph), 0, 1) ** 2
        out += np.sin(2 * np.pi * np.cumsum(f) / SR) * env
    return norm(fade(bp(out, 200, 2200) * 0.6 + bp(noise(d), 300, 2500) * 0.5 * angry, 0.8, 1.5))


def drum(f=55, d=1.6):
    tt = t_(d)
    return norm(np.sin(2 * np.pi * f * tt * (1 - 0.25 * tt / d)) * np.exp(-tt / 0.35) + lp(noise(d), 180) * np.exp(-tt / 0.12) * 0.6)


def whoosh(d=1.0):
    return S.s_whoosh(d, 200, 1600, 0.6)


def chime(f=440, d=3.0):
    tt = t_(d)
    return norm(sum(np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * (0.8 + k)) / k for k in (1, 2, 3)))


def fire(d):
    n = noise(d); r = np.random.default_rng(9)
    cr = np.zeros(len(n))
    for p in r.integers(0, len(n) - 400, int(d * 25)):
        cr[p:p + 300] += hp(noise(300 / SR), 2000) * np.exp(-np.arange(300) / 40) * r.uniform(0.3, 1)
    return norm(fade(lp(n, 500) * 0.8 + cr, 1.0, 1.5))


def glass(d=0.9):
    tt = t_(d); r = np.random.default_rng(3)
    x = hp(noise(d), 3500) * np.exp(-tt / 0.18)
    for k in range(8):
        x += np.sin(2 * np.pi * r.uniform(2500, 6000) * tt) * np.exp(-tt / r.uniform(0.05, 0.25)) * 0.3
    return norm(x)


def planes(d):
    tt = t_(d)
    x = sum(np.sin(2 * np.pi * f * tt + 0.3 * np.sin(2 * np.pi * 0.7 * tt)) for f in (82, 86, 164))
    return norm(fade(lp(x + bp(noise(d), 80, 400) * 2, 900) * np.sin(np.pi * tt / d) ** 1.5, 0.5, 0.5))


# nền: lớp dây trầm đổi hợp âm êm theo thời gian (không theo chương vì giọng gốc đọc lệch thứ tự)
PADS = [(55.0, (1, 1.5, 2, 2.4)), (49.0, (1, 1.2, 1.5, 2)), (46.2, (1, 1.5, 2, 2.4)), (43.6, (1, 1.2, 1.5, 2)),
        (41.2, (1, 1.2, 1.5, 2)), (38.9, (1, 1.5, 2, 2.4)), (41.2, (1, 1.2, 1.5, 1.9)), (43.6, (1, 1.5, 2, 2.4))]
step = DUR / len(PADS)
for k, (root, chord) in enumerate(PADS):
    ev(k * step, pad(step + 3.0, root, chord), -27)
# mở đầu & tiết lộ tên
ev(1.0, chime(330, 4.0), -26); ev(T(25.80), drum(41, 3.0), -6)
ev(T(25.80), norm(S.sweep(60, 30, 2.0) * np.linspace(1, 0, int(2.0 * SR))), -16)
# đám đông: 1914, quán bia, Heldenplatz
ev(T(95.09), crowd(5.5), -24); ev(T(153.06), crowd(15.0), -26); ev(T(313.40), crowd(6.0), -24)
# chiến tranh 1914–1918: pháo xa
for k, tv in enumerate((101.19, 103.69, 106.06, 108.39)):
    ev(T(tv), drum(38 + k * 3, 2.0), -24)
# chuyển cảnh bản đồ
for tv in (31.57, 203.85, 316.82, 336.92, 343.73, 378.86, 382.61):
    ev(T(tv) - 0.3, whoosh(1.2), -26)
# lên nắm quyền, cháy Reichstag
ev(T(249.41), drum(46, 2.2), -16)
ev(T(255.28), fire(5.0), -20)
# Đêm pha lê: kính vỡ
for k in range(4):
    ev(T(302.70) + k * 0.9, glass(0.9), -24)
# 1939: cắt cứng, trống lớn; máy bay
ev(T(324.78), drum(38, 3.0), -5)
ev(T(333.68), planes(4.0), -22)
# Holocaust: lặng, một tiếng chuông trầm
ev(T(353.99), chime(220, 6.0), -26)
# sụp đổ & cái chết
ev(T(375.19), drum(41, 2.2), -16)
ev(T(401.59), drum(36, 3.0), -14)
ev(T(426.79), chime(294, 6.0), -24)

if __name__ == "__main__":
    S.export(ROOT / "build" / "Hitler_nosfx.mp4", ROOT / "build" / "Hitler_v1.mp4", pre_gain_db=1.5, limit=0.70)
