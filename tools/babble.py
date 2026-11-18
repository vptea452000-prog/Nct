"""Giọng ú ớ chuẩn của kênh (chốt sau Tập 1: Lửa, 17/11/2026) — liền mạch, không tiếng lách cách.

Dùng:  from babble import babble, VOICE, EMO
       x = babble("bop", 2.0, "happy", "say")     # spk, giây, cảm xúc, loại bóng (say/shout/whisper)
Thêm nhân vật mới: thêm vào VOICE (f0 = cao độ Hz, rate = âm tiết/giây, bright = độ sáng giọng, rough = độ khàn, gain = dB).
"""
import numpy as np
from scipy.signal import butter, sosfilt
from sfx_lib import bp, lp, norm, SR

VOWELS = {"a": (800, 1200, 2500), "e": (500, 1900, 2600), "i": (320, 2300, 3000), "o": (500, 900, 2400), "u": (350, 800, 2300), "ơ": (550, 1300, 2500)}
VOICE = {
    "bop": dict(f0=235, rate=7.5, bright=1.15, rough=0.0, gain=0.0),
    "gam": dict(f0=118, rate=5.6, bright=0.85, rough=0.35, gain=1.5),
}
EMO = {  # (hệ số cao độ, hệ số tốc độ, âm lượng dB, kiểu ngữ điệu)
    "calm": (1.0, 1.0, 0, "flat"), "happy": (1.12, 1.1, 1, "up"), "angry": (1.25, 1.15, 3, "punch"), "worried": (1.15, 1.2, 0, "wobble"),
    "sad": (0.9, 0.8, -3, "down"), "cold": (1.05, 0.9, -1, "tremble"), "grumpy": (0.95, 1.0, 0, "down"), "shy": (1.1, 0.8, -6, "down"),
    "scared": (1.2, 1.0, -6, "flat"), "sleepy": (0.85, 0.6, -6, "down"), "sing": (1.2, 0.7, 0, "wobble"), "smug": (1.05, 0.9, 1, "up"), "panic": (1.6, 1.6, 4, "wobble"), "wonder": (1.0, 0.85, -1, "up"), "proud": (1.15, 1.0, 3, "punch"),
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


