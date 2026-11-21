"""Đếm đỉnh âm tiết (hạt nhân nguyên âm) trong một đoạn MP3 để ước lượng số âm tiết."""
import numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SR = 16000
_a = None

def audio():
    global _a
    if _a is None:
        _a = np.fromfile(ROOT / "build/voice16k.raw", dtype=np.int16).astype(np.float32) / 32768
    return _a

def count(t0, t1, hop=0.01, prom=5.0, min_gap=0.085):
    a = audio()[int(t0 * SR):int(t1 * SR)]
    n = int(len(a) / (hop * SR))
    if n < 3:
        return 0
    fr = a[: n * int(hop * SR)].reshape(n, -1)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-6)
    k = np.ones(5) / 5
    db = np.convolve(db, k, mode="same")
    peaks = []
    for i in range(1, n - 1):
        if db[i] >= db[i - 1] and db[i] > db[i + 1] and db[i] > -30:
            lo = i
            while lo > 0 and db[lo - 1] <= db[lo] + 0.01 and i - lo < 25:
                lo -= 1
            hi = i
            while hi < n - 1 and db[hi + 1] <= db[hi] + 0.01 and hi - i < 25:
                hi += 1
            if db[i] - max(db[lo], db[hi]) >= prom:
                if peaks and (i - peaks[-1]) * hop < min_gap:
                    if db[i] > db[peaks[-1]]:
                        peaks[-1] = i
                    continue
                peaks.append(i)
    return len(peaks)
