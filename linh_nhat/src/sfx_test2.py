"""Tiếng cho bản thử mở đầu — chỉ hiệu ứng (giọng đọc chủ kênh ghép sau)."""
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools"))
import sfx_lib as S  # noqa
from sfx_lib import ev, noise, bp, lp, env_exp, env_ad, t_, norm, SR  # noqa

DUR = 10.5
S.configure(ROOT, DUR)


def fade(x, a=0.4, b=0.4):
    n = len(x); i = np.arange(n)
    return x * np.minimum(1, np.minimum(i / (a * SR), (n - i) / (b * SR)))


def sea(d):
    tt = t_(d)
    return norm(fade(lp(noise(d), 700) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * tt) ** 2)))


def gulls(d):
    out = np.zeros(int(d * SR))
    for st in (0.6, 1.9, 3.1):
        L = int(0.35 * SR); tt = t_(0.35)
        f = 1500 + 700 * np.sin(np.pi * tt / 0.35)
        out[int(st * SR):int(st * SR) + L] += np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(L, 0.03, 0.2) * 0.5
    return norm(lp(out, 4000))


def hearth(d):
    return norm(fade(lp(noise(d), 300) * 0.8))


def slide():
    d = 0.5
    return norm(bp(noise(d), 300, 1500) * env_ad(int(d * SR), 0.05, 0.3))


def rustle():
    d = 0.4
    return norm(bp(noise(d), 2000, 6000) * env_ad(int(d * SR), 0.02, 0.25))


def boom():
    d = 1.4; tt = t_(d)
    return norm(np.sin(2 * np.pi * 55 * tt) * np.exp(-tt / 0.5) + lp(noise(d), 200) * np.exp(-tt / 0.3) * 0.5)


ev(0, sea(4.4), -16); ev(0, gulls(4.2), -22)
ev(4.2, hearth(2.9), -18); ev(5.65, slide(), -14); ev(3.1, S.s_whoosh(0.8, 300, 3000, 0.7), -12); ev(8.72, S.s_whoosh(0.25, 800, 4000, 0.4), -10)
for k in range(6):
    ev(7.0 + k * 0.33, norm(lp(noise(0.12), 600) * env_ad(int(0.12 * SR), 0.01, 0.08)), -24)
ev(8.1, rustle(), -12)
ev(9.4, boom(), -8)

if __name__ == "__main__":
    import subprocess
    B = ROOT / "build"
    va = ROOT / "audio/voice.mp3"; va.parent.mkdir(exist_ok=True)
    if not va.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(DUR), "-c:a", "libmp3lame", str(va)], check=True)
    S.export(B / "Test_mo_dau_v2_nosfx.mp4", B / "Test_mo_dau_v2.mp4", pre_gain_db=10.0, limit=0.70)
