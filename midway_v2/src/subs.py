"""Phụ đề tiếng Việt: chia theo cụm nghĩa, tối đa 2 dòng cân nhau, xuất SRT."""
import json
from lib import ROOT, tw, nfc, text, W, clamp, ease_out

SIZE = 54
MAX_LINE = 900  # px, trong vùng an toàn (chừa ~150 px mép phải)
# không tách các cặp chữ này giữa hai thẻ hoặc hai dòng
KEEP = {("Joseph", "Rochefort"), ("Chester", "Nimitz"), ("Đô", "đốc"), ("đốc", "Chester"),
        ("Trân", "Châu"), ("Châu", "Cảng,"), ("Thái", "Bình"), ("Bình", "Dương,"), ("Bình", "Dương."),
        ("Hạm", "đội"), ("tàu", "sân"), ("sân", "bay"), ("hai", "tuần."), ("máy", "bay"),
        ("tháng", "5"), ("tháng", "5,"), ("tháng", "6,"), ("năm", "1942,"), ("hải", "quân"), ("chưng", "cất"),
        ("tiếp", "tế"), ("mười", "lăm"), ("lăm", "ngày."), ("Melbourne,", "Úc,"), ("vô", "tuyến,"), ("hai", "chữ"), ("chữ", "cái:")}


COMPOUNDS = """đồng nghiệp|xác định|chuẩn bị|chiến dịch|địa danh|hạm đội|xuất hiện|bức điện|giải mã|sĩ quan|
đối phương|mục tiêu|tấn công|tình báo|không quân|đơn vị|cầu viện|liên lạc|mệnh lệnh|thông thường|vô tuyến|
nước ngọt|tiếp tế|bí mật|kiểm tra|thực sự|phục kích|căn cứ|chưng cất|đường cáp|hòn đảo|vị trí|chi tiết|
kế hoạch|bản dịch|người Mỹ|quân Nhật|người Nhật|lính Mỹ|lính đảo|nơi khác|hai tuần|trên đảo|đáng lẽ|
lượng nước|nhóm giải|phía Nhật|phía Mỹ|dịch điện|thiếu nước|xin nước|chữ cái|Thái Bình|Bình Dương|mười lăm|cố tình|dễ tin""".replace("\n", "")
for cw in COMPOUNDS.split("|"):
    a, b = cw.split()
    for pb in ("", ",", ".", ":"):
        KEEP.add((a, b + pb))


def _ok_break(words, i):
    """Được ngắt sau chữ i?"""
    return i + 1 >= len(words) or (words[i]["w"], words[i + 1]["w"]) not in KEEP


def _sentences(words):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if w["punct"] and w["punct"][-1] in ".?!":
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def _fits(toks):
    s = " ".join(toks)
    if tw(s, "bold", SIZE) <= MAX_LINE:
        return True
    return len(split_lines(toks, None)) == 2 and all(tw(l, "bold", SIZE) <= MAX_LINE for l in split_lines(toks, None))


def _chunk(sent):
    """Chia một câu thành các thẻ bằng quy hoạch động."""
    toks = [w["w"] for w in sent]
    n = len(toks)
    INF = 1e18
    best = [INF] * (n + 1)
    back = [0] * (n + 1)
    best[0] = 0
    for j in range(1, n + 1):
        for i in range(max(0, j - 16), j):
            if best[i] >= INF:
                continue
            if j < n and (toks[j - 1], toks[j]) in KEEP:
                continue
            seg = toks[i:j]
            if "AF." in seg and len(seg) > 1:  # "AF." luôn đứng riêng, không hiện trước lời đọc
                continue
            L = len(" ".join(seg))
            if L > 60 or not _fits(seg):
                continue
            c = (L - 44) ** 2 * 0.05
            if j < n:
                p = toks[j - 1][-1]
                c += 0 if p in ",:;" else 260
            if L < 16 and " ".join(seg) != "AF.":
                c += 400
            v = best[i] + c + 30
            if v < best[j]:
                best[j], back[j] = v, i
    cuts, j = [], n
    while j > 0:
        cuts.append((back[j], j))
        j = back[j]
    return [sent[a:b] for a, b in reversed(cuts)]


def build_cues(words):
    chunks = []
    for sent in _sentences(words):
        chunks.extend(_chunk(sent))
    out = []
    for k, cq in enumerate(chunks):
        start = cq[0]["start"] - 0.05
        end = cq[-1]["end"] + 0.5
        if k + 1 < len(chunks):
            end = min(end, chunks[k + 1][0]["start"] - 0.06)
        out.append({"start": round(max(0, start), 3), "end": round(end, 3), "lines": split_lines([x["w"] for x in cq], cq)})
    return out


def split_lines(toks, cq):
    s = " ".join(toks)
    if tw(s, "bold", SIZE) <= MAX_LINE and len(s) <= 30:
        return [s]
    best, bi = 1e9, None
    for i in range(1, len(toks)):
        if (toks[i - 1], toks[i]) in KEEP:
            continue
        a, b = " ".join(toks[:i]), " ".join(toks[i:])
        wa, wb = tw(a, "bold", SIZE), tw(b, "bold", SIZE)
        if max(wa, wb) > MAX_LINE:
            continue
        cost = abs(wa - wb)
        if toks[i - 1][-1] in ",:":
            cost -= 120  # thích ngắt ở dấu phẩy
        if i == 1 or i == len(toks) - 1:
            cost += 600  # tránh một chữ lẻ dòng
        if cost < best:
            best, bi = cost, i
    if bi is None:
        return [s]
    return [" ".join(toks[:bi]), " ".join(toks[bi:])]


def srt_time(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def write_srt(cues, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, q in enumerate(cues, 1):
            f.write(f"{i}\n{srt_time(q['start'])} --> {srt_time(q['end'])}\n" + "\n".join(nfc(l) for l in q["lines"]) + "\n\n")


KEYWORDS = [("af",), ("hai", "tuần"), ("mười", "lăm", "ngày")]


def _bare(w):
    return w.strip(".,:;?!").lower()


def draw_line_kw(c, line, y):
    """Một dòng phụ đề, tô vàng từ khoá của tập (AF, hai tuần, mười lăm ngày)."""
    toks = line.split(" ")
    mark = [False] * len(toks)
    for kw in KEYWORDS:
        for i in range(len(toks) - len(kw) + 1):
            if tuple(_bare(x) for x in toks[i:i + len(kw)]) == kw:
                for j in range(i, i + len(kw)):
                    mark[j] = True
    sp = tw(" ", "bold", SIZE)
    total = tw(line, "bold", SIZE)
    x = W / 2 - total / 2
    for tok, m in zip(toks, mark):
        w = text(c, tok, x, y, "bold", SIZE, "yellow" if m else "white", stroke=4, stroke_color="ink")
        x += w + sp


def draw_sub(c, cues, t):
    for q in cues:
        if q["start"] <= t < q["end"]:
            lines = q["lines"]
            # vùng phụ đề 1300–1440
            ys = [1392] if len(lines) == 1 else [1352, 1418]
            age = t - q["start"]
            k = clamp(age / 0.14)
            sc = 0.94 + 0.06 * ease_out(k)
            c.saveLayerAlpha(None, int(255 * clamp(0.25 + k)))
            c.translate(W / 2, 1380)
            c.scale(sc, sc)
            c.translate(-W / 2, -1380)
            for y, l in zip(ys, lines):
                draw_line_kw(c, l, y)
            c.restore()
            return


if __name__ == "__main__":
    words = json.loads((ROOT / "build/words.json").read_text(encoding="utf-8"))
    cues = build_cues(words)
    for q in cues:
        print(f"{q['start']:6.2f}-{q['end']:6.2f}  " + " / ".join(q["lines"]))
