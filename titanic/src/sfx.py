"""Hiệu ứng tiếng Titanic — trộn với giọng đọc chủ kênh (audio/voice.mp3), tự hạ tiếng khi có lời."""
import sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
PART = HERE.parent
sys.path.insert(0, str(HERE.parent.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa

DUR = 404.25
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



def creak(d=1.2, f=90):
    tt = t_(d)
    x = np.sin(2 * np.pi * np.cumsum(f + 25 * np.sin(2 * np.pi * 1.7 * tt)) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 13 * tt))
    return norm(bp(x, 60, 800) * env_ad(int(d * SR), 0.2, d * 0.5))


def scrape(d=2.0):
    tt = t_(d)
    return norm(bp(noise(d), 200, 1800) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * tt) ** 2) * env_ad(int(d * SR), 0.3, d * 0.5))


def tune(d=7.0):   # nhạc cụ ban nhạc chơi nhẹ (tiếng đàn đơn giản, không lời)
    tt = t_(d)
    notes = [392, 440, 494, 440, 392, 330, 349, 392]
    out = np.zeros(len(tt))
    seg = len(tt) // len(notes)
    for i, f in enumerate(notes):
        a, b = i * seg, (i + 1) * seg
        u = t_(seg / SR)[: b - a]
        out[a:b] = (np.sin(2 * np.pi * f * u) + 0.4 * np.sin(4 * np.pi * f * u)) * env_ad(b - a, 0.05, 0.25)
    return norm(lp(out, 3000))


def bagpipe(d=7.0):
    tt = t_(d)
    drone = sum(np.sin(2 * np.pi * f * tt) for f in (116, 233)) * 0.5
    mel = np.sin(2 * np.pi * np.cumsum(466 + 60 * np.sign(np.sin(2 * np.pi * 2 * tt))) / SR)
    return norm(fade(bp(drone + mel, 150, 3000), 0.5, 0.8))


# A. Ireland
ev(0.0, amb(14.0, 150, 600, 0.1), -32); ev(8.5, amb(5.5, 80, 350), -24)            # gió đồng / bếp than bùn
for k in range(4):
    ev(1.0 + k * 1.3, thud(110, 0.18), -26)                                        # nhát xẻng
ev(14.0, amb(5.8, 1500, 4000, 0.4), -34)                                           # mưa ngoài cửa sổ
ev(15.0, rustle(0.5), -22)
ev(19.75, chime(523, 3.0), -26)
for k in range(9):
    ev(29.0 + k * 0.45, thud(900, 0.06), -30)                                      # tiếng đồng xu
ev(32.1, chime(660, 2.0), -22)
ev(41.6, rustle(0.6), -20); ev(46.0, boom(2.4, 55), -14)
# B. bến cảng
ev(48.66, sea(15.2), -26); ev(48.66, gull(4, 15.0), -30)
ev(63.8, sea(6.0), -22); ev(63.8, amb(6.0, 50, 160, 0.2), -26)
ev(69.82, sea(9.8), -24); ev(71.0, whistle(2.6), -18)                               # còi tàu Titanic
ev(79.56, amb(12.5, 150, 600, 0.1), -32); ev(89.9, thud(180, 0.2), -16)            # dấu "ĐẠT"
# C. trên tàu
ev(92.11, amb(6.3, 50, 140, 0.2), -30)                                             # máy tàu
for k in range(4):
    ev(94.7 + k * 0.25, thud(1200, 0.04), -28)                                     # bật tắt công tắc
for k in range(6):
    ev(98.9 + k * 1.1, thud(700, 0.08), -30)                                       # thìa chạm bát
ev(105.67, bagpipe(7.2), -22)
ev(112.82, amb(12.8, 50, 140, 0.2), -32)
ev(125.58, sea(13.8), -30)
ev(139.34, scrape(2.8), -14); ev(139.6, creak(1.6, 70), -18)                        # cọ vào tảng băng
ev(142.5, amb(2.4, 50, 140, 0.2), -24)                                             # máy chạy thêm… rồi im bặt (144,9)
ev(151.5, amb(15.4, 150, 600, 0.1), -32)
for k in range(5):
    ev(152.8 + k * 1.25, thud(500, 0.08), -26)                                     # cục băng rơi
# D. nước tràn → xuồng
ev(166.91, amb(13.7, 100, 600, 0.6), -24)                                          # nước chảy
ev(170.6, norm(lp(noise(5.8), 900) * 0.8), -26)
ev(180.62, amb(15.6, 300, 1400, 0.5), -26)                                         # hành lang ồn (tiếng động, không lời)
for k in range(10):
    ev(181.0 + k * 1.1, thud(80, 0.2), -26)
ev(192.6, norm(np.sin(2 * np.pi * 220 * t_(0.5)) * np.exp(-t_(0.5) / 0.15)), -18)  # cửa sắt rung
for k in range(8):
    ev(202.4 + k * 0.7, thud(120, 0.15), -24)                                      # bước cầu thang
ev(208.29, amb(15.0, 300, 2000, 0.3), -22)                                          # gió đêm
for k in range(4):
    ev(210.0 + k * 1.7, creak(1.2, 140), -26)                                      # ròng rọc hạ xuồng
ev(217.7, S.s_pop(0.9), -20)
ev(223.23, amb(17.4, 300, 2000, 0.3), -28)
ev(235.6, rustle(1.0), -22)
ev(240.66, creak(4.0, 120), -24); ev(240.66, amb(9.9, 150, 600, 0.1), -30)
ev(247.9, chime(392, 2.6), -24)
# E. chìm
ev(250.51, creak(3.0, 55), -20); ev(250.51, sea(6.5), -26)
ev(257.02, tune(7.0), -22)
for k in range(10):
    ev(264.2 + k * 0.28, thud(90, 0.2), -24)
ev(267.0, creak(3.0, 50), -20)
for k in range(4):
    ev(270.94 + k * 0.33, thud(1500, 0.05), -26)                                   # đèn chớp tắt
ev(275.59, boom(3.0, 38), -6); ev(278.96, boom(2.4, 45), -6); ev(279.0, creak(3.0, 40), -12)
ev(282.0, norm(lp(noise(2.3), 500) * env_ad(int(2.3 * SR), 0.5, 1.5)), -14)
ev(284.9, S.s_whoosh(0.8, 300, 2000, 0.5), -14); ev(285.9, norm(lp(noise(0.6), 2000) * env_exp(int(0.6 * SR), 0.12)), -8)   # tõm
ev(286.51, norm(fade(lp(noise(15.5), 250))), -24)                                   # dưới nước, lạnh
ev(302.06, sea(13.8), -28)
for k in range(6):
    ev(303.0 + k * 1.2, norm(lp(noise(0.4), 900) * env_ad(int(0.4 * SR), 0.05, 0.3)), -26)   # sải bơi
ev(315.85, sea(21.3), -30)
# F. bình minh → kết
ev(337.2, sea(12.5), -28); ev(338.4, whistle(2.0), -24); ev(345.0, whistle(1.6), -22)
ev(349.66, amb(10.9, 150, 600, 0.1), -32)
ev(365.2, chime(523, 3.2), -22)
ev(372.4, amb(14.5, 1500, 5000, 0.4), -24)                                          # mưa New York
ev(386.92, boom(2.4, 42), -16)
ev(396.64, sea(7.6), -30); ev(397.0, chime(392, 4.0), -24)

if __name__ == "__main__":
    S.export(PART / "build" / "Titanic_nosfx.mp4", PART / "build" / "Titanic_v1.mp4", pre_gain_db=2.0, limit=0.70)
