"""Căn kịch bản vào giọng đọc (không cần nhận dạng giọng nói), bản 2 — chính xác hơn, không trôi:
  · tách kịch bản thành cụm (ngắt ở . , : ? ! …);
  · dò mọi khoảng lặng trong giọng (silencedetect);
  · quy hoạch động: gán mỗi ranh giới cụm vào một khoảng lặng, sao cho tốc độ nói từng cụm gần tốc độ trung bình,
    ranh giới câu ưu tiên khoảng lặng dài, và hạn chế bỏ qua khoảng lặng dài nằm giữa cụm;
  · thời điểm từng chữ = nội suy theo âm tiết trong cụm.
  python3 tools/align2.py audio/voice_raw.mp3 KICH_BAN.md   → audio/voice_align.json, audio/voice_words.json
"""
import json, math, re, subprocess, sys, bisect
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "linh_nhat" / "src"))
import align as A1  # đếm đỉnh năng lượng (âm tiết)

def silences(path, db=-35, d=0.12):
    out = subprocess.run(["ffmpeg", "-i", path, "-af", f"silencedetect=n={db}dB:d={d}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)
    if len(en) < len(st):
        en.append(dur)
    return list(zip(st, en)), dur


def syl(w):
    w = re.sub(r"[^\wÀ-ỹ]", "", w)
    if not w:
        return 0
    return max(1, round(len(w) * 1.75)) if w.isdigit() else 1


def phrases(text):
    """→ list of (words, ends_sentence)."""
    text = re.sub(r"\s+", " ", text.strip())
    toks = text.split(" ")
    out, cur = [], []
    for tk in toks:
        cur.append(tk)
        core = tk.rstrip("\"”’)")
        if re.search(r"[\.\?\!…]$", core):
            out.append((cur, True)); cur = []
        elif re.search(r"[,:;]$", core):
            out.append((cur, False)); cur = []
    if cur:
        out.append((cur, True))
    return out


def align(path, text, R=None):
    sil, dur = silences(path)
    ph = phrases(text)
    n = [sum(syl(w) for w in p[0]) for p in ph]
    # điểm bắt đầu nói: đầu file hoặc cuối mỗi khoảng lặng; điểm hết nói: đầu khoảng lặng kế tiếp
    onsets = [0.0] + [e for s, e in sil if e < dur - 0.05]
    if sil and sil[0][0] < 0.05:
        onsets = onsets[1:]
    sil_len = {round(e, 4): e - s for s, e in sil}
    speech_end = lambda j: next((s for s, e in sil if s > onsets[j] + 0.05), dur)
    speech = dur - sum(e - s for s, e in sil)
    R = R or sum(n) / speech                              # âm tiết / giây nói
    peaks = list(A1.analyse(A1.load(path))[0])
    kpk = len(peaks) / sum(n)                             # đỉnh / âm tiết (toàn bài)
    npk = lambda a, b: bisect.bisect_left(peaks, b) - bisect.bisect_left(peaks, a)
    M = len(onsets); N = len(ph); INF = 1e18
    # dp[k][j]: cụm k bắt đầu tại onset j
    dp = [[INF] * (M + 1) for _ in range(N + 1)]; bk = [[-1] * (M + 1) for _ in range(N + 1)]
    dp[0][0] = 0.0
    nxt_on = onsets + [dur]

    def seg_cost(k, i, j):
        # cụm k nói từ onsets[i] tới hết lời trước onsets[j] (j = M nghĩa là hết file)
        t0 = onsets[i]; t1 = nxt_on[j]
        skipped = [ (e - s) for s, e in sil if t0 + 0.05 < e < t1 - 0.05 ]   # khoảng lặng bị nuốt vào trong cụm
        talk = (t1 - t0) - sum(skipped) - (sil_len.get(round(t1, 4), 0) if j < M else 0)
        talk = max(talk, 0.15)
        c = math.log(talk * R / max(n[k], 1)) ** 2 * (6 + min(n[k], 30) * 1.2)
        P = npk(t0, t1) / kpk
        c += 0.5 * (P - n[k]) ** 2 / (0.35 * n[k] + 2)
        c += sum(max(0, s - 0.3) for s in skipped) * 12          # nuốt khoảng lặng dài trong cụm là đáng ngờ
        if j < M:                                                # ranh giới câu ↔ khoảng lặng dài, dấu phẩy ↔ lặng ngắn
            L = sil_len.get(round(nxt_on[j], 4), 0)
            if ph[k][1]:
                c += 10 * max(0, 0.42 - L) - 2 * min(L, 0.7)
            else:
                c += -1.5 * min(L, 0.45) + 4 * max(0, L - 0.5)
        return c

    WIN = 14
    for k in range(N):
        for i in range(M):
            if dp[k][i] >= INF:
                continue
            for j in range(i + 1, min(M, i + WIN) + 1):
                if k < N - 1 and j == M:
                    continue
                v = dp[k][i] + seg_cost(k, i, j)
                if v < dp[k + 1][j]:
                    dp[k + 1][j] = v; bk[k + 1][j] = i
    j = M; idx = [M]
    for k in range(N, 0, -1):
        j = bk[k][j]; idx.append(j)
    idx = idx[::-1]                         # idx[k] = onset index bắt đầu cụm k
    words, bounds = [], []
    for k in range(N):
        t0 = onsets[idx[k]]
        t1 = nxt_on[idx[k + 1]] if idx[k + 1] < M else dur
        t1 = min(t1, next((s for s, e in sil if s > t0 + 0.05), dur)) if idx[k + 1] - idx[k] == 1 else t1 - sil_len.get(round(t1, 4), 0)
        tot = max(n[k], 1); acc = 0
        for w in ph[k][0]:
            words.append([round(t0 + (t1 - t0) * acc / tot, 3), w]); acc += syl(w)
        bounds.append((t0, t1, ph[k][1]))
    # gộp cụm thành câu
    sents, cur, s0 = [], [], None
    for (t0, t1, end), p in zip(bounds, ph):
        if s0 is None:
            s0 = t0
        cur += p[0]
        if end:
            sents.append([round(s0, 2), round(t1, 2), " ".join(cur)]); cur, s0 = [], None
    for a, b in zip(sents, sents[1:]):     # phụ đề liền mạch tới câu sau
        a[1] = b[0]
    return sents, words, R


if __name__ == "__main__":
    path, script = sys.argv[1:3]
    txt = open(script).read().split("\n", 1)[1]
    sents, words, R = align(path, txt)
    for _ in range(2):                      # ước lượng lại tốc độ nói từ kết quả (trung vị theo câu)
        rates = sorted(sum(syl(w) for w in s.split()) / max(0.3, b - a - 0.4) for a, b, s in sents)
        sents, words, R = align(path, txt, rates[len(rates) // 2])
    print(f"{len(sents)} câu · {len(words)} chữ · {R:.2f} âm tiết/giây")
    for a, b, s in sents:
        print(f"{a:7.2f} {b:7.2f}  {s[:70]}")
    base = path.rsplit("/", 1)[0]
    json.dump(sents, open(base + "/voice_align.json", "w"), ensure_ascii=False, indent=1)
    json.dump(words, open(base + "/voice_words.json", "w"), ensure_ascii=False)
