"""Phụ đề tiếng Việt: chia theo cụm nghĩa, tối đa 2 dòng cân nhau, xuất SRT."""
import json
from lib import ROOT, tw, nfc, text, W

SIZE = 54
MAX_LINE = 900  # px, trong vùng an toàn (chừa ~150 px mép phải)
# không tách các cặp chữ này giữa hai thẻ hoặc hai dòng
KEEP = {("thứ", "Hai,"), ("thứ", "Ba,"), ("tháng", "8"), ("năm", "1911,"), ("năm", "1913,"), ("năm", "1914,"), ("tháng", "1"),
        ("Mona", "Lisa"), ("Mona", "Lisa."), ("bảo", "tàng"), ("tàng", "Louvre"), ("Louis", "Béroud."), ("Vincenzo", "Peruggia,"),
        ("Guillaume", "Apollinaire"), ("Pablo", "Picasso"), ("Alfredo", "Geri"), ("Giovanni", "Poggi."), ("Leonardo", "da"),
        ("da", "Vinci."), ("bốn", "cái"), ("cái", "móc"), ("móc", "sắt."), ("tám", "mươi"), ("mươi", "phân."), ("hai", "mươi"),
        ("mươi", "tám"), ("tám", "tháng"), ("bảy", "tháng."), ("đáy", "giả"), ("rương", "gỗ"), ("áo", "khoác"), ("khoác", "trắng"),
        ("vân", "tay."), ("vân", "tay"), ("dấu", "vân"), ("khách", "sạn,"), ("khách", "sạn."), ("tường", "trống."), ("khoảng", "tường"),
        ("Uffizi", "là"), ("tàng", "Uffizi")}


COMPOUNDS = """họa sĩ|phòng trưng|trưng bày|lính gác|chụp ảnh|tác phẩm|thủ phạm|làm việc|đóng cửa|nhân viên|ra vào|cầu thang|
cảnh sát|tìm thấy|hồ sơ|trước đó|nhà thơ|bắt giam|thẩm vấn|liên quan|vụ trộm|phòng trọ|hỏi chuyện|khám xét|báo chí|đưa tin|
khắp nơi|xếp hàng|trôi qua|đồ cổ|ký tên|hẹn gặp|giám đốc|mặt sau|kiểm tra|ra tòa|quê hương|xử nhẹ|biến mất|nhận ra|không còn|
giấu tranh|ra ngoài|treo tranh|mang đi|dò ra|lấy tranh|trả về|trở về|giữ tranh|tháo khung|bức tranh|chiếc rương|người thợ""".replace("\n", "")
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


def draw_sub(c, cues, t):
    for q in cues:
        if q["start"] <= t < q["end"]:
            lines = q["lines"]
            # vùng phụ đề 1300–1440
            ys = [1392] if len(lines) == 1 else [1352, 1418]
            for y, l in zip(ys, lines):
                text(c, l, W / 2, y, "bold", SIZE, "white", align="center", stroke=4, stroke_color="ink")
            return


if __name__ == "__main__":
    words = json.loads((ROOT / "build/words.json").read_text(encoding="utf-8"))
    cues = build_cues(words)
    for q in cues:
        print(f"{q['start']:6.2f}-{q['end']:6.2f}  " + " / ".join(q["lines"]))
