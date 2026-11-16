"""Hiệu ứng tiếng cho bản thử phong cách hoạt hình (chưa có giọng đọc)."""
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, rng, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa

S.configure(ROOT, 17.5)


def jungle_amb(d):
    """Rừng nhiệt đới: gió lá + côn trùng rỉ rả + chim hót thưa."""
    n = int(d * SR); tt = t_(d)
    leaves = bp(noise(d), 300, 2500) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * tt) ** 2) * 0.5
    insects = bp(noise(d), 4200, 5200, 3) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt)) * 0.35
    x = leaves + insects
    for k in range(5):
        st = rng.uniform(0.3, d - 0.6)
        a = int(st * SR); L = int(0.35 * SR)
        f = 2600 + 900 * np.sin(2 * np.pi * 7 * t_(0.35)) + rng.uniform(-300, 300)
        chirp = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(L, 0.02, 0.1) * 0.6
        x[a:a + L] += chirp[: n - a]
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.4 * SR), (n - np.arange(n)) / (0.4 * SR)))
    return norm(x * fade)


def rustle(d=0.6):
    n = int(d * SR)
    return norm(bp(noise(d), 800, 5000) * env_ad(n, 0.1, 0.25) * (1 + 0.6 * np.sin(2 * np.pi * 14 * t_(d))))


def boing(f0=500, f1=200, d=0.35):
    return norm(S.sweep(f0, f1, d) * env_exp(int(d * SR), 0.12))


def jet(d):
    n = int(d * SR)
    x = lp(noise(d), 1500) * np.sin(np.pi * np.clip(t_(d) / d, 0, 1)) ** 1.2
    return norm(x)


ev(0.0, jungle_amb(9.4), -14)
ev(0.3, S.s_impact(), -9)
ev(1.8, S.s_whoosh(0.4, 300, 2000, 0.5), -14, 0.4)
ev(2.3, boing(700, 380, 0.25), -12, 0.4)
ev(3.6, rustle(0.9), -9, -0.3)
ev(4.6, S.s_pop(1.0), -12)
ev(6.6, S.s_whoosh(0.3, 200, 1500, 0.4), -14)
ev(6.8, S.s_pop(0.8), -9)
ev(8.0, S.s_impact(), -6)
ev(8.02, boing(900, 250, 0.4), -9)
ev(8.1, S.s_riser(0.25), -14)
ev(9.4, S.s_whoosh(0.4, 200, 1800, 0.3), -15)
ev(9.9, S.s_pop(1.0), -12)
ev(10.9, S.s_pop(1.15), -12)
ev(10.2, S.s_paper(0.3), -14, 0.3)
ev(12.0, jet(1.3), -10)
ev(12.1, S.s_pop(1.0), -12)
ev(13.2, jungle_amb(1.2), -16)
ev(13.4, S.s_paper(0.35), -11)
ev(13.45, S.s_pop(0.9), -10)
ev(14.4, S.s_whoosh(0.5, 150, 2000, 0.4), -12)
ev(14.6, S.s_ding(), -12)
ev(15.4, S.s_stamp(), -8)
ev(16.0, boing(600, 900, 0.2), -14, 0.4)

if __name__ == "__main__":
    B = ROOT / "build"
    S.export(B / "Onoda_style_test_nosfx.mp4", B / "Onoda_style_test.mp4", pre_gain_db=6.0)
