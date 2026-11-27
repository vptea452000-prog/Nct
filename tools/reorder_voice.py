"""Sắp lại file giọng đọc theo đúng thứ tự câu của kịch bản (khi file giọng bị đảo câu).
Dùng thời điểm Whisper (audio/asr_words.json) để tìm vị trí từng câu, cắt ở giữa khoảng lặng, ghép lại theo thứ tự kịch bản.
  python3 tools/reorder_voice.py <thư mục tập>   (đọc audio/voice_raw_goc.mp3 → ghi audio/voice_raw.mp3)"""
import json, re, sys, subprocess, difflib, unicodedata
from pathlib import Path
import numpy as np
root = Path(sys.argv[1]); SR = 48000
src = root / "audio" / "voice_raw_goc.mp3"
a = json.load(open(root / "audio" / "asr_words.json"))
txt = re.sub(r"\s+", " ", open(root / "KICH_BAN.md").read().split("\n", 1)[1].strip())
sents = re.split(r"(?:(?<=[\.\?\!…])|(?<=[\.\?\!…][\"”]))\s+(?=[\"“A-ZÀ-ỸĐ])", txt)
n = lambda w: re.sub(r"[^\wÀ-ỹ]", "", unicodedata.normalize("NFC", w.lower()))
B = [n(w[2]) for w in a]
starts = []
for s in sents:
    A = [n(w) for w in s.split()]; L = len(A); best = (0, 0)
    for j in range(0, len(B) - 3):
        r = difflib.SequenceMatcher(None, A, B[j:j + L], autojunk=False).ratio()
        if r > best[0]:
            best = (r, j)
    starts.append(a[best[1]][0])
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy(); dur = len(x) / SR
out = subprocess.run(["ffmpeg", "-i", str(src), "-af", "silencedetect=n=-35dB:d=0.1", "-f", "null", "-"], capture_output=True, text=True).stderr
sil = list(zip([float(v) for v in re.findall(r"silence_start: ([\d.]+)", out)], [float(v) for v in re.findall(r"silence_end: ([\d.]+)", out)]))

def cut_before(t):
    c = [(s, e) for s, e in sil if t - 0.9 <= e <= t + 0.35]
    if not c:
        return max(0.0, t - 0.15)
    s, e = min(c, key=lambda q: abs(q[1] - t))
    return (s + e) / 2

order = sorted(range(len(sents)), key=lambda i: starts[i])           # thứ tự câu trong file gốc
cuts = {i: cut_before(starts[i]) for i in order}
cuts[order[0]] = 0.0
seg = {}
for k, i in enumerate(order):
    t0 = cuts[i]; t1 = cuts[order[k + 1]] if k + 1 < len(order) else dur
    seg[i] = x[int(t0 * SR):int(t1 * SR)].copy()
    f = min(int(0.008 * SR), len(seg[i]) // 4)
    ramp = np.linspace(0, 1, f)[:, None]
    seg[i][:f] *= ramp; seg[i][-f:] *= ramp[::-1]
y = np.concatenate([seg[i] for i in range(len(sents))])
# bảng ánh xạ thời gian: câu i nằm ở [o0, o1) trong file gốc và [r0, r1) trong file đã sắp
segs, r = [], 0.0
for i in range(len(sents)):
    L = len(seg[i]) / SR; o0 = cuts[i]
    segs.append([i, round(o0, 4), round(o0 + L, 4), round(r, 4), round(r + L, 4)]); r += L
json.dump(segs, open(root / "audio" / "segments.json", "w"), indent=1)
moved = [i + 1 for k, i in enumerate(order) if i != k]
if "--map-only" in sys.argv:
    sys.exit(print("đã ghi audio/segments.json"))
p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-b:a", "256k",
                      str(root / "audio" / "voice_raw.mp3")], stdin=subprocess.PIPE)
p.stdin.write(y.astype(np.float32).tobytes()); p.stdin.close(); p.wait()
print(f"{len(sents)} câu · {len(moved)} câu bị đảo đã sắp lại · {dur:.2f}s → {len(y) / SR:.2f}s")
