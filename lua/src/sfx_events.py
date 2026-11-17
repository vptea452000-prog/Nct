"""Âm thanh Tập 1: Lửa — giọng ú ớ tổng hợp (formant) + hiệu ứng tiếng. Không có giọng đọc.
  python3 src/sfx_events.py → build/Lua_v1.mp4
"""
import sys
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfilt
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "tools")); sys.path.insert(0, str(ROOT / "src"))
import sfx_lib as S  # noqa
from sfx_lib import ev, rng, noise, bp, lp, hp, env_exp, env_ad, t_, norm, SR  # noqa
from beats import T, DUR

S.configure(ROOT, DUR)

VOWELS = {"a": (800, 1200, 2500), "e": (500, 1900, 2600), "i": (320, 2300, 3000), "o": (500, 900, 2400), "u": (350, 800, 2300), "ơ": (550, 1300, 2500)}
VOICE = {
    "bop": dict(f0=235, rate=7.5, bright=1.15, rough=0.0, gain=0.0),
    "gam": dict(f0=118, rate=5.6, bright=0.85, rough=0.35, gain=1.5),
}
EMO = {  # (hệ số cao độ, hệ số tốc độ, âm lượng dB, kiểu ngữ điệu)
    "calm": (1.0, 1.0, 0, "flat"), "happy": (1.12, 1.1, 1, "up"), "angry": (1.25, 1.15, 3, "punch"), "worried": (1.15, 1.2, 0, "wobble"),
    "sad": (0.9, 0.8, -3, "down"), "cold": (1.05, 0.9, -1, "tremble"), "grumpy": (0.95, 1.0, 0, "down"), "shy": (1.1, 0.8, -6, "down"),
    "scared": (1.2, 1.0, -6, "flat"), "panic": (1.6, 1.6, 4, "wobble"), "wonder": (1.0, 0.85, -1, "up"), "proud": (1.15, 1.0, 3, "punch"),
}


def formant(x, f, bw):
    lo, hi = max(60, f - bw / 2), min(SR / 2 - 200, f + bw / 2)
    return sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)


def babble(spk, dur, emo, kind, seed=0):
    """Giọng ú ớ liền mạch: nguồn hài âm (không răng cưa), cao độ trượt mượt, nguyên âm chuyển dần, không chèn tiếng phụ âm."""
    r = np.random.default_rng(seed)
    v = VOICE[spk]
    pf, rf, gdb, shape = EMO.get(emo, EMO["calm"])
    if kind == "shout":
        pf *= 1.1; gdb += 2
    n = int(dur * SR)
    tt = np.arange(n) / SR
    rate = v["rate"] * rf
    # ranh giới âm tiết
    bounds = [0.0]
    while bounds[-1] < dur:
        bounds.append(bounds[-1] + r.uniform(0.8, 1.25) / rate)
    bounds = np.array(bounds)
    # đường cao độ: mỗi âm tiết một đích, nội suy mượt
    u = tt / dur
    base = v["f0"] * pf
    contour = {"up": 1 + 0.25 * u ** 2, "down": 1 - 0.18 * u, "punch": 1.1 - 0.15 * u, "wobble": 1 + 0.1 * np.sin(u * 18)}.get(shape, np.ones(n))
    targets = base * r.uniform(0.9, 1.12, len(bounds))
    f0 = np.interp(tt, bounds, targets) * contour
    f0 = np.convolve(f0, np.ones(int(0.04 * SR)) / int(0.04 * SR), mode="same")
    f0 *= 1 + 0.025 * np.sin(2 * np.pi * 5.5 * tt)
    if shape == "tremble":
        f0 *= 1 + 0.05 * np.sin(2 * np.pi * 9 * tt)
    ph = 2 * np.pi * np.cumsum(f0) / SR
    if kind == "whisper":
        src = bp(r.normal(0, 1, n), 300, 4000) * 0.7
    else:
        src = sum(np.sin(k * ph) / k ** 1.2 for k in range(1, 14) if k * base < 7000)
        if v["rough"] > 0:
            src *= 1 + v["rough"] * 0.5 * np.sin(2 * np.pi * 30 * tt)
    # nguyên âm chuyển dần giữa các âm tiết
    keys = list(VOWELS)
    seq = [VOWELS[r.choice(keys)] for _ in bounds]
    y = np.zeros(n)
    for i in range(len(bounds) - 1):
        a0, a1 = int(bounds[i] * SR), min(n, int(bounds[i + 1] * SR))
        if a1 - a0 < 200:
            continue
        lo, hi = max(0, a0 - int(0.03 * SR)), min(n, a1 + int(0.03 * SR))
        seg = src[lo:hi]
        F = seq[i]
        out_seg = sum(formant(seg, F[j] * v["bright"], [110, 150, 220][j] * 1.3) * [1.0, 0.55, 0.25][j] for j in range(3))
        L = hi - lo
        w = np.sin(np.pi * np.arange(L) / L) ** 1.5      # vào ra mềm, chồng lấn nhẹ giữa âm tiết
        y[lo:hi] += out_seg * w
    # nhịp nói: hạ âm lượng nhẹ giữa các âm tiết thay vì ngắt cụt
    gate = 0.55 + 0.45 * np.interp(tt, (bounds[:-1] + bounds[1:]) / 2, np.ones(len(bounds) - 1))
    y *= gate
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.05 * SR), (n - np.arange(n)) / (0.08 * SR)))
    y = lp(y * fade, 5500, 4)
    return norm(y) * (10 ** ((gdb + v["gain"]) / 20))


# ----------------------------------------------------------------- lời ú ớ theo nhịp
for i, (name, (a, b, row)) in enumerate(T.items()):
    spk, kind, txt, emo = row[3], row[4], row[5], row[6]
    if spk and kind != "think" and txt:
        st, en = a + 0.12, b - 0.45
        if name == "hot":
            st = a + 0.62
        if name in ("afraid",):
            st = a + 0.62
        if name == "useless2":
            pass
        d = max(0.35, en - st)
        x = babble(spk, d, emo, kind, seed=i)
        g = -3 if kind == "shout" else (-12 if kind == "whisper" else -6)
        if name == "useless2":
            x = lp(x, 1800); g -= 4  # vọng ra từ trong hang
        ev(st, x, g, -0.25 if spk == "gam" else 0.25)


def boing(f0=700, f1=300, d=0.3):
    return norm(S.sweep(f0, f1, d) * env_exp(int(d * SR), 0.12))


def wind(d, g=1.0):
    n = int(d * SR)
    x = bp(noise(d), 200, 1200) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t_(d)) ** 2)
    x += bp(noise(d), 600, 900, 3) * (np.sin(2 * np.pi * 0.17 * t_(d)) > 0.6) * 0.6
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.5 * SR), (n - np.arange(n)) / (0.6 * SR))))


def rain(d):
    n = int(d * SR)
    x = bp(noise(d), 800, 6000) * 0.7 + lp(noise(d), 300) * 0.3
    drops = (rng.random(n) < 0.002) * rng.normal(0, 3, n)
    x += bp(drops, 2000, 7000)
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.5 * SR), (n - np.arange(n)) / (0.6 * SR))))


def crackle(d, dens=0.0004):
    """Lửa: chủ yếu tiếng ù ấm, tí tách rất thưa và nhẹ."""
    n = int(d * SR)
    x = bp((rng.random(n) < dens) * rng.normal(0, 1, n), 800, 3000) * 0.25 + lp(noise(d), 350) * 0.8
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.3 * SR), (n - np.arange(n)) / (0.4 * SR))))


def stomp():
    d = 0.35; n = int(d * SR)
    return norm(lp(noise(d), 400) * env_exp(n, 0.05) + S.sweep(90, 40, d) * env_exp(n, 0.08))


def whoosh_fire():
    d = 0.9; n = int(d * SR)
    return norm(bp(noise(d), 200, 2500) * env_ad(n, 0.05, 0.4) + lp(noise(d), 200) * env_ad(n, 0.05, 0.4))


def cough():
    out = np.zeros(int(0.9 * SR))
    for k in range(3):
        d = 0.18; n = int(d * SR)
        c = formant(noise(d), 700, 600) * env_exp(n, 0.05) + lp(noise(d), 300) * env_exp(n, 0.04)
        a = int(k * 0.26 * SR); out[a:a + n] += c
    return norm(out)


def growl(d):
    n = int(d * SR); tt = t_(d)
    x = lp(noise(d), 300, 4) * (1 + 0.8 * np.sin(2 * np.pi * 28 * tt)) + np.sin(2 * np.pi * 70 * tt) * 0.4
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.3 * SR), (n - np.arange(n)) / (0.4 * SR))))


def tummy(d=1.3):
    n = int(d * SR); tt = t_(d)
    f = 110 + 60 * np.sin(2 * np.pi * 2.2 * tt)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * tt)) + lp(noise(d), 200) * 0.4
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.1 * SR), (n - np.arange(n)) / (0.3 * SR))))


def yelp():
    d = 0.35
    return norm(S.sweep(1200, 600, d) * env_exp(int(d * SR), 0.12) + formant(noise(d), 1200, 500) * env_exp(int(d * SR), 0.05) * 0.4)


def chatter(d):
    out = np.zeros(int(d * SR))
    k = S.s_tick(1.2)
    pos = 0
    while pos < len(out) - len(k):
        out[pos:pos + len(k)] += k * rng.uniform(0.4, 1)
        pos += int(SR / 18)
    return norm(out)


def bird():
    d = 0.35; tt = t_(d)
    f = 3000 + 900 * np.sin(2 * np.pi * 9 * tt)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(int(d * SR), 0.02, 0.12))


def bt(name):
    return T[name][0], T[name][1]


# CẢNH 1
a, b = bt("open"); ev(0, wind(T["sigh"][1] + T["sigh"][0], 1), -16)
ev(a + 0.3, S.s_impact(), -8); ev(a + 0.6, S.s_impact(), -6)
a, b = bt("drill"); ev(a, norm(bp(noise(b - a), 300, 1500) * (0.6 + 0.4 * np.sin(2 * np.pi * 6 * t_(b - a)))), -18)
for k in range(int((b - a) / 0.3)):
    ev(a + k * 0.3, S.s_whoosh(0.25, 800, 2500, 0.5), -20)
a, b = bt("spark"); ev(a + 0.7, S.s_hiss(0.6), -14); ev(a + 1.7, whoosh_fire(), -6)
ev(a + 1.8, crackle(T["stomp"][0] + 1.2 - (a + 1.8)), -16)
a, b = bt("jump"); ev(a, S.s_impact(), -5); ev(a, boing(400, 900, 0.25), -10, -0.4)
a, b = bt("name"); ev(a + 0.9, S.s_ding(), -14)
a, b = bt("red"); ev(a + 1.4, crackle(1.0, 0.003), -14)
a, b = bt("useless"); ev(a + 0.1, S.s_impact(), -12)
a, b = bt("stomp")
for k, ts in enumerate([a + 0.2, a + 0.6, a + 1.0, a + 1.4]):
    ev(ts, stomp(), -6, (-1) ** k * 0.2)
ev(a + 1.5, S.s_hiss(0.9), -10)
ev(a + 2.0, cough(), -6, -0.2)
a, b = bt("danger"); ev(a, cough(), -14, -0.3)
for k in range(5):
    ev(a + 0.2 + k * 0.3, stomp(), -16, -0.4)
a, b = bt("sigh"); ev(a + 0.5, S.s_whoosh(0.8, 600, 200, 0.3), -16)
# CẢNH 2
a = T["cold"][0]; ev(a, rain(T["wolves"][0] - a), -16)
a, b = bt("glow"); ev(a, crackle(T["wolves"][0] - a, 0.002), -18, 0.3)
ev(a + 1.0, S.s_whoosh(0.3, 3000, 4000, 0.5), -16); ev(a + 1.3, S.s_whoosh(0.3, 3000, 4000, 0.5), -16)
a, b = bt("nope"); ev(a, boing(300, 200, 0.2), -14)
a, b = bt("growl"); ev(a + 0.2, tummy(1.3), -4)
# CẢNH 3
a = T["wolves"][0]; ev(a, crackle(T["stone"][0] - a, 0.002), -18)
ev(a + 0.2, growl(2.4), -8, 0.5)
a, b = bt("letme"); ev(a + 0.3, S.s_whoosh(0.4, 300, 2500), -10)
a, b = bt("hot"); ev(a + 0.2, boing(500, 200, 0.3), -12); ev(a + 0.5, whoosh_fire(), -5)
for k in range(4):
    ev(a + 0.8 + k * 0.35, S.s_whoosh(0.3, 400, 2500), -12)
a, b = bt("flee"); ev(a + 0.3, yelp(), -8, 0.4); ev(a + 0.55, yelp(), -10, 0.5)
ev(a + 0.4, norm(lp(noise(1.0), 900) * np.linspace(1, 0, int(1.0 * SR))), -18, 0.6)
a, b = bt("invent"); ev(a, S.s_impact(), -8); ev(a + 0.1, S.s_ding(), -12)
a, b = bt("allmine"); ev(a + 0.1, S.s_impact(), -12)
a, b = bt("hog"); ev(a + 0.3, S.s_whoosh(0.4, 200, 1500), -14); ev(a + 0.5, stomp(), -12)
# CẢNH 4
a = T["stone"][0]
for k in range(6):
    ev(a + 0.2 + k * 0.7, bird(), -16, rng.uniform(-0.5, 0.5))
ev(a + 0.6, S.s_pop(1.0), -12)
a, b = bt("idea"); ev(a + 1.6, S.s_ding(), -10)
a, b = bt("useless2"); ev(a, boing(600, 300, 0.25), -18)
a, b = bt("card"); ev(a + 0.2, S.s_impact(), -12); ev(a, crackle(b - a, 0.002), -18)

if __name__ == "__main__":
    import subprocess
    B = ROOT / "build"
    va = ROOT / "audio/voice.mp3"
    if not va.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(DUR), "-c:a", "libmp3lame", str(va)], check=True)
    S.EVENTS[:] = [(t, x, g + 4, p) for t, x, g, p in S.EVENTS]
    S.export(B / "Lua_v1_nosfx.mp4", B / "Lua_v1.mp4", pre_gain_db=float(sys.argv[1]) if len(sys.argv) > 1 else 1.8, limit=0.70)
