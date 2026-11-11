"""Hiệu ứng âm thanh tự tổng hợp cho Midway v2 (không dùng file ngoài, không vướng bản quyền).

Mỗi hiệu ứng bám đúng mốc chuyển động trên hình của bản v2 (scenes.py). Hiệu ứng được
hạ ~7 dB khi đang có giọng đọc (ducking) để lời luôn rõ.

  python3 src/sfx.py   → build/sfx_stem.wav, build/mix_voice_sfx.wav, build/Midway_v2_sfx.mp4
"""
import subprocess
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
DUR = 99.816
N = int(DUR * SR) + SR
rng = np.random.default_rng(42)


# ---------------------------------------------------------------- công cụ
def t_(d):
    return np.arange(int(d * SR)) / SR


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "bandpass", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "lowpass", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "highpass", fs=SR, output="sos"), x)


def env_exp(n, tau):
    return np.exp(-np.arange(n) / SR / tau)


def env_ad(n, a, d):
    """Lên trong a giây, tắt dần trong phần còn lại (hình chuông)."""
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-4), np.exp(-(t - a) / max(d, 1e-4)))
    return e


def noise(d):
    return rng.normal(0, 1, int(d * SR))


def sweep(f0, f1, d, kind="exp"):
    t = t_(d)
    if kind == "exp":
        f = f0 * (f1 / f0) ** (t / d)
    else:
        f = f0 + (f1 - f0) * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def norm(x, peak=1.0):
    m = np.max(np.abs(x)) + 1e-9
    return x / m * peak


def db(g):
    return 10 ** (g / 20)


# ---------------------------------------------------------------- âm cơ bản
def s_pop(pitch=1.0):
    d = 0.07
    x = sweep(1100 * pitch, 380 * pitch, d) * env_exp(int(d * SR), 0.018)
    x[:60] += noise(60 / SR) * np.linspace(1, 0, 60) * 0.5
    return norm(x)


def s_tick(bright=1.0):
    x = hp(noise(0.012), 2500 * bright) * env_exp(int(0.012 * SR), 0.0025)
    return norm(x)


def s_key():
    """Phím máy chữ: tiếng gõ kim loại + thân máy trầm, ngẫu nhiên nhẹ."""
    d = 0.06
    n = int(d * SR)
    click = bp(noise(d), 1800 + rng.uniform(-300, 600), 5200, 2) * env_exp(n, 0.004)
    body = np.sin(2 * np.pi * rng.uniform(110, 150) * t_(d)) * env_exp(n, 0.012) * 0.6
    slap = lp(noise(d), 900) * env_exp(n, 0.008) * 0.5
    return norm(click + body + slap)


def s_stamp():
    d = 0.45
    n = int(d * SR)
    thump = sweep(95, 45, d) * env_exp(n, 0.07)
    hit = lp(noise(d), 1400) * env_exp(n, 0.02) * 0.9
    paper = bp(noise(d), 2000, 6000) * env_exp(n, 0.01) * 0.35
    return norm(thump + hit + paper)


def s_whoosh(d=0.38, lo=300, hi=3000, peak_at=0.6):
    n = int(d * SR)
    x = noise(d)
    out = np.zeros(n)
    # quét bộ lọc theo từng khối nhỏ để có tiếng gió lướt
    blocks = 24
    for b in range(blocks):
        a0, a1 = b * n // blocks, (b + 1) * n // blocks
        fc = lo * (hi / lo) ** (np.sin(np.pi * min(1, (b + 0.5) / blocks / peak_at * 0.5)) )
        seg = bp(x[max(0, a0 - 2000):a1], max(80, fc * 0.6), min(SR / 2 - 100, fc * 1.6))[-(a1 - a0):]
        out[a0:a1] = seg
    t = np.arange(n) / n
    e = np.where(t < peak_at, (t / peak_at) ** 2, ((1 - t) / (1 - peak_at)) ** 1.5)
    return norm(out * e)


def s_paper(d=0.28):
    n = int(d * SR)
    x = bp(noise(d), 900, 5000) * env_ad(n, 0.05, 0.09)
    grain = (rng.random(n) < 0.004) * rng.normal(0, 3, n)
    return norm(x + bp(grain, 1500, 7000) * env_ad(n, 0.05, 0.1))


def s_drop():
    """Ảnh/giấy đặt xuống bàn."""
    d = 0.22
    n = int(d * SR)
    x = lp(noise(d), 1800) * env_exp(n, 0.018) + np.sin(2 * np.pi * 85 * t_(d)) * env_exp(n, 0.03) * 0.7
    return norm(x)


def s_marker(d=0.22):
    n = int(d * SR)
    x = bp(noise(d), 2500, 4500, 3) * env_ad(n, 0.02, 0.12)
    x *= 1 + 0.4 * np.sin(2 * np.pi * 38 * t_(d))
    return norm(x)


def s_impact():
    """Cú nhấn AF: tiếng trầm + đập + đuôi ngắn."""
    d = 0.9
    n = int(d * SR)
    sub = sweep(70, 38, d) * env_exp(n, 0.22)
    hit = lp(noise(d), 2500) * env_exp(n, 0.03)
    tail = lp(noise(d), 600) * env_exp(n, 0.25) * 0.25
    return norm(sub * 1.2 + hit * 0.8 + tail)


def s_riser(d=0.3):
    n = int(d * SR)
    x = s_whoosh(d, 400, 5000, 0.95)
    return norm(x * np.linspace(0.2, 1, n))


def s_boom():
    """Tiếng nổ xa (đã làm đục, không chói)."""
    d = 2.2
    n = int(d * SR)
    body = lp(noise(d), 220, 4) * env_ad(n, 0.01, 0.55)
    sub = sweep(55, 28, d) * env_exp(n, 0.5)
    crack = lp(noise(d), 3000) * env_exp(n, 0.04) * 0.5
    rumble = lp(noise(d), 90, 4) * env_ad(n, 0.2, 0.9) * 0.8
    return norm(body * 1.4 + sub + crack + rumble)


def s_radio(d, beeps=True):
    """Nhiễu vô tuyến + tiếng bíp kiểu điện báo."""
    n = int(d * SR)
    st = bp(noise(d), 900, 3200, 2) * 0.35
    crack = (rng.random(n) < 0.0015) * rng.normal(0, 4, n)
    st += bp(crack, 1500, 6000)
    st *= 0.7 + 0.3 * np.sin(2 * np.pi * 0.7 * t_(d) + rng.uniform(0, 6))
    if beeps:
        tt = t_(d)
        pat = np.zeros(n)
        pos = 0.05
        while pos < d - 0.1:
            L = rng.choice([0.06, 0.06, 0.18])
            a, b = int(pos * SR), int(min(d, pos + L) * SR)
            pat[a:b] = 1
            pos += L + rng.choice([0.06, 0.06, 0.18])
        pat = lp(pat, 120)
        st += np.sin(2 * np.pi * 760 * tt) * pat * 0.8
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.15 * SR), (n - np.arange(n)) / (0.25 * SR)))
    return norm(st * fade)


def s_plane(d=1.3):
    """Máy bay lướt qua: tiếng máy cánh quạt + gió, có hiệu ứng Doppler."""
    n = int(d * SR)
    tt = t_(d)
    f = 95 * (1.08 - 0.16 * (tt / d))
    ph = 2 * np.pi * np.cumsum(f) / SR
    eng = sum(np.sin(k * ph) / k for k in range(1, 9))
    eng *= 1 + 0.5 * np.sin(2 * np.pi * 24 * tt)
    wind = bp(noise(d), 300, 2000) * 0.5
    e = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 1.5
    return norm(lp(eng, 1800) * e + wind * e)


def s_rumble(d=0.9):
    n = int(d * SR)
    return norm(lp(noise(d), 120, 4) * env_ad(n, 0.25, 0.35) + np.sin(2 * np.pi * 48 * t_(d)) * env_ad(n, 0.25, 0.35) * 0.4)


def s_rattle(d):
    n = int(d * SR)
    out = np.zeros(n)
    k = s_tick(0.6)
    pos = 0
    while pos < n - len(k):
        g = rng.uniform(0.4, 1.0)
        out[pos:pos + len(k)] += k * g
        pos += int(SR / rng.uniform(26, 38))
    out += lp(noise(d), 300) * 0.25 * (1 + np.sin(2 * np.pi * 31 * t_(d)))
    return norm(out * np.minimum(1, (n - np.arange(n)) / (0.1 * SR)))


def s_hiss(d=0.9):
    n = int(d * SR)
    return norm(hp(noise(d), 3000) * env_ad(n, 0.08, 0.35))


def s_zip(d=1.1):
    """Đường cáp vẽ dần: tiếng điện kéo dài, cao dần."""
    n = int(d * SR)
    tt = t_(d)
    f = 180 + 260 * tt / d
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + 0.5 * np.sign(np.sin(ph)) * 0.3) * (0.6 + 0.4 * np.sin(2 * np.pi * 50 * tt))
    x = lp(x, 2500) + bp(noise(d), 2000, 6000) * 0.12
    return norm(x * np.minimum(1, np.minimum(np.arange(n) / (0.05 * SR), (n - np.arange(n)) / (0.1 * SR))))


def s_ding():
    d = 0.6
    n = int(d * SR)
    tt = t_(d)
    x = (np.sin(2 * np.pi * 1320 * tt) + 0.4 * np.sin(2 * np.pi * 2640 * tt) + 0.2 * np.sin(2 * np.pi * 3960 * tt)) * env_exp(n, 0.16)
    return norm(x)


def s_scramble(d=0.25):
    """Nhóm mã nhảy số khi giải mã: chuỗi tích-tắc cơ khí nhanh."""
    n = int(d * SR)
    out = np.zeros(n)
    pos = 0
    while pos < n - 700:
        k = s_tick(rng.uniform(0.7, 1.3)) * rng.uniform(0.5, 1)
        out[pos:pos + len(k)] += k
        pos += int(SR * rng.uniform(0.018, 0.03))
    return norm(out)


def s_clock():
    d = 0.05
    n = int(d * SR)
    x = bp(noise(d), 1200, 4000) * env_exp(n, 0.006) + np.sin(2 * np.pi * 1800 * t_(d)) * env_exp(n, 0.008) * 0.5
    return norm(x)


# ---------------------------------------------------------------- dòng thời gian (mốc v2)
EVENTS = []  # (giây, âm, gain dB, pan -1..1)


def ev(t, x, g=0.0, pan=0.0):
    EVENTS.append((t, x, g, pan))


def typing(text, t0, t1, g=-4):
    s = list(text)
    for i, ch in enumerate(s):
        if ch.strip() == "":
            continue
        ev(t0 + (i + 0.5) / len(s) * (t1 - t0), s_key(), g + rng.uniform(-2, 1), rng.uniform(-0.25, 0.25))


def build_events():
    P = -10  # pop / tag
    # 0–2.65 ảnh đảo
    ev(0.02, s_whoosh(0.45, 200, 2500, 0.3), -14)
    ev(0.42, s_pop(1.0), P)
    ev(0.92, s_paper(0.2), -16, -0.4)
    # 2.65 bản đồ Midway–Hawaii
    ev(2.62, s_paper(0.3), -14)
    ev(3.28, s_pop(1.1), P, -0.4)
    ev(3.98, s_pop(0.95), P, 0.4)
    ev(3.68, s_marker(0.7), -20, 0.1)
    ev(4.30, s_paper(0.35), -11)
    typing("NƯỚC NGỌT CHỈ CÒN ĐỦ DÙNG HAI TUẦN.", 4.89, 6.15)
    ev(5.85, s_marker(0.3), -14)
    typing("XIN TIẾP TẾ NGAY.", 6.56, 7.31)
    ev(9.36, s_stamp(), -4)
    ev(9.98, s_whoosh(0.5, 300, 4000), -12)
    ev(10.69, s_radio(1.7), -8, -0.2)
    ev(11.32, s_pop(0.8), P, -0.6)
    # 12.45 Rochefort
    ev(12.42, s_drop(), -9)
    ev(12.97, s_pop(1.0), P)
    ev(15.40, s_paper(0.25), -13, -0.5)
    # 18.28 điện mật
    ev(18.25, s_drop(), -10)
    for tf in (18.70, 19.30, 19.75, 20.20):
        ev(tf, s_scramble(0.25), -12, rng.uniform(-0.3, 0.3))
    ev(23.75, s_marker(0.3), -13)
    ev(24.50, s_marker(0.3), -13)
    ev(25.0, s_whoosh(0.6, 150, 1500, 0.5), -18)
    t = 25.17
    while t < 29.2:  # ô MỤC TIÊU nhấp nháy
        ev(t, s_tick(0.8), -22)
        t += 0.4
    ev(28.96, s_riser(0.28), -12)
    ev(29.24, s_impact(), -3)
    # 29.96 bản đồ AF = ?
    ev(29.93, s_paper(0.3), -14)
    ev(30.02, s_pop(1.0), P)
    ev(31.98, s_whoosh(0.45, 400, 3500), -12)
    ev(32.42, s_pop(1.2), P - 2)
    ev(33.40, s_whoosh(1.0, 120, 800, 0.5), -20)
    # 34.69 Trân Châu Cảng
    ev(34.66, s_drop(), -10)
    ev(34.77, s_pop(1.0), P)
    ev(36.22, s_paper(0.2), -16)
    ev(36.93, s_pop(0.85), -7)
    # 37.69 Nimitz
    ev(37.66, s_whoosh(0.4, 200, 2000, 0.3), -15)
    ev(38.05, s_paper(0.25), -13, -0.5)
    # 40.66 nếu đoán nhầm
    ev(40.72, s_pop(0.9), P)
    ev(42.25, s_rumble(1.0), -11, 0.4)
    ev(43.08, s_tick(1.0), -14, 0.4)
    ev(44.32, s_pop(0.8), P - 2, -0.5)
    ev(44.45, s_plane(1.0), -9, -0.4)
    ev(45.26, s_boom(), -9, -0.2)
    ev(45.52, s_pop(0.9), P - 2)
    # 46.36 AF = MIDWAY ?
    ev(46.40, s_pop(1.0), P, -0.4)
    ev(46.48, s_pop(1.15), P, 0.4)
    ev(47.80, s_whoosh(0.45, 300, 2500), -15)
    ev(50.42, s_pop(0.7), -12)
    # 51.26 đảo / 53.56 máy chưng cất
    ev(51.23, s_whoosh(0.4, 200, 1800, 0.3), -17)
    ev(53.58, s_pop(1.0), P)
    ev(53.78, s_rattle(0.85), -12)
    ev(54.00, s_hiss(0.9), -17, 0.3)
    ev(54.61, s_stamp(), -4)
    # 55.28 hai đường liên lạc
    ev(55.25, s_paper(0.3), -14)
    ev(55.92, s_paper(0.22), -14, -0.3)
    ev(56.07, s_paper(0.22), -14, 0.3)
    ev(57.05, s_pop(1.0), P, 0.4)
    ev(58.10, s_zip(1.1), -16, 0.2)
    ev(59.20, s_ding(), -16, -0.3)
    ev(59.82, s_pop(0.9), P - 2, -0.3)
    ev(61.30, s_whoosh(1.0, 120, 900, 0.5), -20)
    ev(61.72, s_pop(1.0), P)
    ev(63.13, s_radio(3.6), -9, -0.1)
    ev(64.10, s_pop(1.1), P - 2, 0.4)
    ev(65.32, s_pop(0.8), P, -0.6)
    # 67.6 nghe điện Nhật
    ev(67.57, s_drop(), -10)
    ev(67.75, s_radio(2.1), -8, -0.5)
    ev(68.35, s_paper(0.22), -15, -0.4)
    # 69.86 Melbourne
    ev(69.83, s_whoosh(0.5, 150, 1500, 0.4), -16)
    ev(69.92, s_pop(1.0), P)
    ev(71.44, s_pop(1.1), P - 2, -0.4)
    ev(72.42, s_pop(0.95), P, -0.4)
    ev(73.13, s_whoosh(0.6, 300, 3500), -12, -0.3)
    typing("PHÍA NHẬT BÁO:", 76.1, 76.9, -8)
    typing("ĐƠN VỊ KHÔNG QUÂN Ở AF", 77.2, 78.1)
    ev(78.00, s_marker(0.25), -13)
    typing("XIN TIẾP TẾ NƯỚC.", 78.56, 79.3)
    ev(79.75, s_paper(0.35), -11, 0.4)
    typing("NƯỚC CÒN LẠI", 81.82, 82.4)
    typing("CHỈ ĐỦ CHO HAI TUẦN.", 82.4, 83.25)
    ev(83.00, s_marker(0.3), -12)
    ev(83.08, s_ding(), -15)
    # 83.59 Midway = AF
    ev(83.56, s_drop(), -9)
    ev(84.22, s_pop(1.0), P, -0.4)
    ev(87.05, s_riser(0.28), -12)
    ev(87.33, s_impact(), -3)
    # 87.97 ngày 4/6
    ev(87.96, s_impact(), -8)
    ev(88.02, s_plane(2.2), -12, 0.3)
    ev(89.57, s_pop(0.9), P - 2, -0.4)
    ev(90.43, s_boom(), -4)
    ev(90.57, s_pop(1.0), P - 4, -0.4)
    # 91.37 ba tàu sân bay
    for i in range(3):
        ev(91.79 + i * 0.19, s_paper(0.3), -11, -0.4 if i % 2 == 0 else 0.4)
        ev(92.00 + i * 0.19, s_pop(1.1), P - 4, -0.3)
    # 94.95 lịch 15 ngày
    for k in range(16):
        ev(94.95 + k * 0.02, s_tick(1.2), -20)
    ev(95.65, s_pop(1.2), P)
    for k in range(1, 15):
        ev(95.9 + (k - 1) * 0.055, s_clock(), -15)
    ev(96.76, s_stamp(), -7)
    ev(98.00, s_riser(0.25), -13)
    ev(98.22, s_impact(), -4)


# ---------------------------------------------------------------- trộn
def load_voice():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ROOT / "audio/voice.mp3"), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    v = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    out = np.zeros((N, 2))
    out[:len(v)] = v[:N]
    return out


def voice_env(v):
    m = np.abs(v).mean(1)
    win = int(0.03 * SR)
    e = np.sqrt(np.convolve(m ** 2, np.ones(win) / win, mode="same"))
    active = (20 * np.log10(e + 1e-9) > -38).astype(float)
    # giữ 150 ms sau lời, mượt 80 ms
    hold = int(0.15 * SR)
    active = np.convolve(active, np.ones(hold), mode="full")[:len(active)] > 0
    sm = int(0.08 * SR)
    return np.convolve(active.astype(float), np.ones(sm) / sm, mode="same")


def mix():
    build_events()
    sfx = np.zeros((N, 2))
    for t, x, g, pan in EVENTS:
        a = int(t * SR)
        x = x * db(g)
        L, R = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        b = min(N, a + len(x))
        sfx[a:b, 0] += x[: b - a] * L * 1.41
        sfx[a:b, 1] += x[: b - a] * R * 1.41
    # phòng nhỏ: đuôi vang rất ngắn cho các hiệu ứng hoà vào nhau
    ir = rng.normal(0, 1, int(0.25 * SR)) * np.exp(-np.arange(int(0.25 * SR)) / SR / 0.06) * 0.015
    from scipy.signal import fftconvolve
    for ch in range(2):
        sfx[:, ch] += fftconvolve(sfx[:, ch], ir)[:N]
    v = load_voice()
    env = voice_env(v)
    duck = 1 - 0.55 * env  # ~ -7 dB khi có lời
    sfx *= duck[:, None]
    sfx *= db(-5)  # mức chung của bus hiệu ứng so với giọng
    out = v + sfx
    # không uốn sóng ở đây: đỉnh được xử lý bằng limiter nhìn trước của ffmpeg khi xuất
    return v, sfx, out


def write_wav(path, x):
    import wave
    y = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(y[: int(DUR * SR)].tobytes())


if __name__ == "__main__":
    v, sfx, out = mix()
    B = ROOT / "build"
    write_wav(B / "sfx_stem.wav", sfx)
    from scipy.io import wavfile
    wavfile.write(B / "mix_float.wav", SR, out[: int(DUR * SR)].astype(np.float32))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(B / "mix_float.wav"),
                    "-af", "alimiter=limit=0.84:attack=3:release=60:level=disabled", "-c:a", "pcm_s16le",
                    str(B / "mix_voice_sfx.wav")], check=True)
    (B / "mix_float.wav").unlink()
    # so sánh mức: hiệu ứng so với giọng trong lúc đang nói
    env = voice_env(v)
    sp = env > 0.5
    vr = 20 * np.log10(np.sqrt((v[sp] ** 2).mean()) + 1e-9)
    sr_ = 20 * np.log10(np.sqrt((sfx[sp] ** 2).mean()) + 1e-9)
    sq = 20 * np.log10(np.sqrt((sfx[~sp] ** 2).mean()) + 1e-9)
    print(f"{len(EVENTS)} hiệu ứng · giọng {vr:.1f} dBFS · hiệu ứng lúc có lời {sr_:.1f} dBFS ({sr_ - vr:.1f} dB) · lúc nghỉ {sq:.1f} dBFS")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(B / "Midway_v2.mp4"), "-i", str(B / "mix_voice_sfx.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR:.3f}",
                    "-movflags", "+faststart", str(B / "Midway_v2_sfx.mp4")], check=True)
    print("xong:", B / "Midway_v2_sfx.mp4")
