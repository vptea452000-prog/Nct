"""Ước lượng mốc thời gian từng chữ khi chưa có SRT.

Chia MP3 thành các đoạn nói (giữa các khoảng lặng), rồi dùng quy hoạch động
gán từng chuỗi chữ liên tiếp vào từng đoạn nói sao cho tốc độ đọc đều nhất,
ưu tiên ranh giới đoạn rơi vào dấu câu. Trong mỗi đoạn, chữ được rải theo số
âm tiết đọc. Kết quả là mốc ƯỚC LƯỢNG, cần nghe lại trước khi chốt.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
DUR = 104.616
MERGE_AT = []
ANCHORS = []

# số âm tiết khi đọc của các từ không phải tiếng Việt thuần / chữ số
SPOKEN = {
    "30": 3, "4": 1, "1943,": 8, "1943": 8, "5,": 1, "14": 3, "5": 1, "7": 1, "1998,": 8, "1998": 8,
    "Huelva": 3, "Huelva.": 3, "Sicily": 3, "Sardinia": 4, "Wales": 1, "Glyndwr": 2, "Michael": 2, "London": 2,
    "William": 2, "Martin": 2, "Pam": 1, "MI5": 3, "Archibald": 3, "Nye": 1, "Harold": 2, "Alexander": 4,
}


def load_words():
    text = (ROOT / "src/script.txt").read_text(encoding="utf-8").strip().split("\n")
    body = " ".join(l for l in text[1:] if l.strip())
    words = []
    for tok in body.split():
        core = re.sub(r"[^\wÀ-ỹ]", "", tok)
        punct = tok[len(tok.rstrip(".,:;?!")):]
        words.append({"w": tok, "syl": SPOKEN.get(core, 1), "punct": punct})
    return words


def load_segments():
    sil = [tuple(map(float, l.split())) for l in (ROOT / "build/silences.tsv").read_text().split("\n") if l.strip()]
    segs, t = [], 0.0
    for s, e in sil:
        if s - t > 0.05:
            segs.append((t, s))
        t = e
    if DUR - t > 0.05:
        segs.append((t, DUR))
    # gộp các khoảng lặng ngắn là chỗ lấy hơi giữa câu (đã nghe/đối chiếu mốc v1)
    for t in MERGE_AT:
        for k in range(len(segs) - 1):
            if segs[k][1] <= t <= segs[k + 1][0]:
                segs[k:k + 2] = [(segs[k][0], segs[k + 1][1])]
                break
    # bỏ đoạn quá ngắn (tiếng thở, click)
    return [s for s in segs if s[1] - s[0] > 0.12]


def align(words, segs):
    n, m = len(words), len(segs)
    syl = [0]
    for w in words:
        syl.append(syl[-1] + w["syl"])
    total_t = sum(e - s for s, e in segs)
    rate = syl[-1] / total_t  # âm tiết / giây

    def bpen(j):  # phạt khi ranh giới đoạn nằm sau chữ j-1 mà không có dấu câu
        if j == n:
            return 0.0
        p = words[j - 1]["punct"]
        if any(c in p for c in ".?!"):
            return 0.0
        if any(c in p for c in ",:;"):
            return 0.3
        return 6.0

    anchor = {}
    plain = [w["w"] for w in words]
    for phrase, t0 in ANCHORS:
        toks = phrase.split()
        wi = next(i for i in range(n) if plain[i:i + len(toks)] == toks)
        k0 = min(range(m), key=lambda k: abs(segs[k][0] - t0))
        anchor[k0 + 1] = wi  # đoạn thứ k0+1 (1-based) phải bắt đầu từ chữ wi

    INF = float("inf")
    cost = [[INF] * (n + 1) for _ in range(m + 1)]
    back = [[0] * (n + 1) for _ in range(m + 1)]
    cost[0][0] = 0.0
    for k in range(1, m + 1):
        d = segs[k - 1][1] - segs[k - 1][0]
        for j in range(1, n + 1):
            best, arg = INF, -1
            for i in range(max(0, j - 40), j):
                if cost[k - 1][i] == INF:
                    continue
                if k in anchor and i != anchor[k]:
                    continue
                s = syl[j] - syl[i]
                exp = s / rate
                c = ((d - exp) / (0.35 + 0.12 * exp)) ** 2 + bpen(j)
                v = cost[k - 1][i] + c
                if v < best:
                    best, arg = v, i
            cost[k][j], back[k][j] = best, arg
    # dựng lại
    j, spans = n, []
    for k in range(m, 0, -1):
        i = back[k][j]
        spans.append((i, j))
        j = i
    spans.reverse()
    out = []
    for (i, j), (s, e) in zip(spans, segs):
        tot = syl[j] - syl[i]
        t = s
        for wi in range(i, j):
            dt = (e - s) * words[wi]["syl"] / tot
            out.append({**words[wi], "start": round(t, 3), "end": round(t + dt, 3)})
            t += dt
    return out, spans, rate


if __name__ == "__main__":
    words = load_words()
    segs = load_segments()
    timed, spans, rate = align(words, segs)
    (ROOT / "build/words.json").write_text(json.dumps(timed, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{len(words)} chữ, {len(segs)} đoạn nói, tốc độ {rate:.2f} âm tiết/s")
    for (i, j), (s, e) in zip(spans, segs):
        print(f"{s:6.2f}-{e:6.2f}  {' '.join(w['w'] for w in words[i:j])}")
