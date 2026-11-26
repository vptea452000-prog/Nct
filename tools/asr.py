"""Nhận dạng giọng (Whisper, chạy trên máy) → thời điểm từng chữ: audio/asr_words.json = [[start, end, word], ...]
  python3 tools/asr.py <thư mục tập> [model]"""
import json, sys, time
from pathlib import Path
from faster_whisper import WhisperModel
root = Path(sys.argv[1]); name = sys.argv[2] if len(sys.argv) > 2 else "small"
t = time.time()
m = WhisperModel(name, device="cpu", compute_type="int8", cpu_threads=4)
segs, info = m.transcribe(str(root / "audio" / "voice_raw.mp3"), language="vi", word_timestamps=True, beam_size=5, vad_filter=False)
out = []
for s in segs:
    for w in s.words:
        out.append([round(w.start, 3), round(w.end, 3), w.word.strip()])
    print(f"{s.start:7.2f} {s.text}", flush=True)
json.dump(out, open(root / "audio" / "asr_words.json", "w"), ensure_ascii=False)
print("xong", len(out), "chữ", round(time.time() - t), "s")
