"""Ghép kịch bản với kết quả nhận dạng giọng (audio/asr_words.json) → thời điểm chính xác từng chữ của kịch bản.
Chữ khớp lấy đúng thời điểm Whisper; chữ không khớp (đọc lệch, số viết khác) nội suy theo âm tiết giữa hai chữ khớp.
  python3 tools/align_asr.py <thư mục tập>   → audio/voice_align.json (câu), audio/voice_words.json (chữ)
"""
import json, re, sys, unicodedata, difflib
from pathlib import Path

root = Path(sys.argv[1])
asr = json.load(open(root / "audio" / "asr_words.json"))
text = open(root / "KICH_BAN.md").read().split("\n", 1)[1]
text = re.sub(r"\s+", " ", text.strip())

DIG = {"0": "không", "1": "một", "2": "hai", "3": "ba", "4": "bốn", "5": "năm", "6": "sáu", "7": "bảy", "8": "tám", "9": "chín"}


def norm(w):
    w = unicodedata.normalize("NFC", w.lower())
    return re.sub(r"[^\wÀ-ỹ]", "", w)


def syl(w):
    w = norm(w)
    return 0 if not w else (max(1, round(len(w) * 1.75)) if w.isdigit() else 1)


# câu & chữ của kịch bản
sents = re.split(r"(?:(?<=[\.\?\!…])|(?<=[\.\?\!…][\"”]))\s+(?=[\"“A-ZÀ-ỸĐ])", text)
sw, sid = [], []
for i, s in enumerate(sents):
    for w in s.split():
        sw.append(w); sid.append(i)
A = [norm(w) for w in sw]
B = [norm(w[2]) for w in asr]

sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
t = [None] * len(sw)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        t[blk.a + k] = asr[blk.b + k][0]
# con số: kịch bản "1907" có thể khớp với "1907" của Whisper (đã khớp ở trên) — số còn lại nội suy
matched = sum(x is not None for x in t)
# nội suy theo âm tiết giữa các chữ đã khớp
cum = [0]
for w in sw:
    cum.append(cum[-1] + max(1, syl(w)))
idx = [i for i, x in enumerate(t) if x is not None]
first, last = idx[0], idx[-1]
for i in range(first):
    t[i] = max(0.0, t[first] - (cum[first] - cum[i]) * 0.2)
end_t = asr[-1][1]
for i in range(last + 1, len(sw)):
    t[i] = t[last] + (cum[i] - cum[last]) * 0.2
for a, b in zip(idx, idx[1:]):
    for i in range(a + 1, b):
        t[i] = t[a] + (t[b] - t[a]) * (cum[i] - cum[a]) / (cum[b] - cum[a])
# đảm bảo tăng dần
for i in range(1, len(t)):
    t[i] = max(t[i], t[i - 1] + 0.01)

words = [[round(x, 3), w] for x, w in zip(t, sw)]
starts = {}
for i, s_ in enumerate(sid):
    starts.setdefault(s_, t[i])
al = []
for i, s in enumerate(sents):
    a = max(0.0, starts[i] - 0.12)
    b = (starts[i + 1] - 0.12) if i + 1 < len(sents) else end_t + 0.3
    al.append([round(a, 2), round(b, 2), s])
json.dump(al, open(root / "audio" / "voice_align.json", "w"), ensure_ascii=False, indent=1)
json.dump(words, open(root / "audio" / "voice_words.json", "w"), ensure_ascii=False)
print(f"{matched}/{len(sw)} chữ khớp trực tiếp ({100 * matched / len(sw):.0f}%), {len(sents)} câu")
