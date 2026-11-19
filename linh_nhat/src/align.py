"""Căn câu kịch bản vào file giọng không cần nhận dạng giọng nói:
đếm âm tiết qua đỉnh năng lượng giọng, so với số âm tiết từng câu (tiếng Việt: mỗi chữ = 1 âm tiết),
rồi bám mốc mỗi câu vào khoảng lặng gần nhất.
  python3 src/align.py audio/voice_1.mp3 <câu đầu> <câu cuối>  → in bảng thời gian từng câu
"""
import re, subprocess, sys, json
import numpy as np
from scipy.signal import butter, sosfiltfilt, find_peaks

SR = 16000


def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32)


def sentences(text):
    text = re.sub(r"\s+", " ", text.strip())
    parts = re.split(r"(?<=[\.\?\!…][\"”]?)\s+(?=[\"“A-ZÀ-Ỹ])", text) if False else re.split(r"(?:(?<=[\.\?\!…])|(?<=[\.\?\!…][\"”]))\s+(?=[\"“A-ZÀ-ỸĐ])", text)
    return [p.strip() for p in parts if p.strip()]


def syl(s):
    return len([w for w in re.split(r"\s+", re.sub(r"[^\wÀ-ỹ\s]", " ", s)) if w])


def analyse(x):
    sos = butter(4, [250, 3500], "bandpass", fs=SR, output="sos")
    y = sosfiltfilt(sos, x)
    hop = SR // 100
    n = len(y) // hop
    env = np.sqrt(np.mean(y[: n * hop].reshape(n, hop) ** 2, axis=1))
    env = np.convolve(env, np.ones(5) / 5, mode="same")
    db = 20 * np.log10(env + 1e-6)
    thr = np.percentile(db, 30) + 6
    voiced = db > thr
    peaks, _ = find_peaks(env, distance=9, prominence=np.percentile(env, 70) * 0.12)
    peaks = [p for p in peaks if voiced[p]]
    return np.array(peaks) / 100.0, voiced


def silences(voiced, min_len=0.25):
    out, i, n = [], 0, len(voiced)
    while i < n:
        if not voiced[i]:
            j = i
            while j < n and not voiced[j]:
                j += 1
            if (j - i) / 100 >= min_len:
                out.append(((i) / 100, (j) / 100))
            i = j
        else:
            i += 1
    return out


def align(path, sents):
    x = load(path)
    dur = len(x) / SR
    peaks, voiced = analyse(x)
    sil = silences(voiced)
    counts = [syl(s) for s in sents]
    total = sum(counts)
    # tỉ lệ đỉnh/âm tiết, rồi ánh xạ chỉ số âm tiết → thời gian
    k = len(peaks) / total
    cum = np.concatenate([[0], np.cumsum(counts)])
    res = []
    gaps = [(a + b) / 2 for a, b in sil]
    for i, s in enumerate(sents):
        def t_of(idx):
            pi = idx * k
            if pi <= 0:
                return float(peaks[0]) - 0.1
            if pi >= len(peaks) - 1:
                return float(peaks[-1]) + 0.2
            lo = int(pi); fr = pi - lo
            return float(peaks[lo] + (peaks[lo + 1] - peaks[lo]) * fr)
        res.append([t_of(cum[i]), t_of(cum[i + 1]), s])
    # bám ranh giới câu vào khoảng lặng gần nhất (trong 0,9 s)
    used = set()
    for i in range(1, len(res)):
        b = res[i][0]
        cand = sorted([q for q in gaps if q not in used and res[i - 1][0] + 0.3 < q], key=lambda q: abs(q - b))
        if cand and abs(cand[0] - b) < 0.8:
            g = cand[0]; used.add(g)
            res[i][0] = g; res[i - 1][1] = g
    res[0][0] = max(0.0, sil[0][1] - 0.05 if sil and sil[0][0] < 0.05 else 0.0)
    res[-1][1] = dur
    return res, dur, len(peaks), total, sil


if __name__ == "__main__":
    path, script, first, last = sys.argv[1:5]
    txt = open(script).read().split("\n", 1)[1]
    txt = re.sub(r"\s+", " ", txt)
    a = txt.index(first); b = txt.index(last) + len(last)
    sents = sentences(txt[a:b])
    res, dur, npk, nsyl, sil = align(path, sents)
    print(f"dài {dur:.2f}s · {npk} đỉnh / {nsyl} âm tiết")
    for s0, s1, s in res:
        print(f"{s0:6.2f} {s1:6.2f}  {s}")
    json.dump(res, open(path.rsplit(".", 1)[0] + "_align.json", "w"), ensure_ascii=False, indent=1)
