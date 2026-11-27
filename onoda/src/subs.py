"""Phụ đề tiếng Việt: chia theo cụm nghĩa, tối đa 2 dòng cân nhau, xuất SRT."""
import json
from lib import ROOT, tw, nfc, text, W

SIZE = 54
MAX_LINE = 900  # px, trong vùng an toàn (chừa ~150 px mép phải)
# không tách các cặp chữ này giữa hai thẻ hoặc hai dòng
KEEP = {("năm", "1974,"), ("năm", "1944,"), ("năm", "1945,"), ("năm", "1950,"), ("năm", "1954,"), ("năm", "1972,"), ("năm", "1959"),
        ("tháng", "8"), ("tháng", "10"), ("tháng", "2"), ("tháng", "3"), ("tháng", "3,"), ("đảo", "Philippines,"), ("sĩ", "quan"),
        ("quan", "Nhật"), ("quân", "phục,"), ("mang", "súng"), ("Thế", "chiến"), ("chiến", "thứ"), ("thứ", "hai"), ("kết", "thúc."),
        ("chỉ", "huy"), ("huy", "cũ,"), ("bán", "sách,"), ("bán", "sách."), ("thiếu", "úy"), ("úy", "Hiroo"), ("Hiroo", "Onoda."),
        ("đảo", "Lubang,"), ("tây", "nam"), ("nam", "Manila,"), ("đầu", "hàng."), ("đầu", "hàng"), ("đổ", "bộ,"), ("ba", "người"),
        ("người", "lính"), ("truyền", "đơn"), ("đồ", "giả"), ("loa", "phóng"), ("phóng", "thanh"), ("lá", "thư"), ("đổi", "ý."),
        ("du", "kích."), ("lương", "thực"), ("nông", "dân,"), ("đốt", "lúa,"), ("đốt", "lúa."), ("cảnh", "sát"), ("ba", "mươi"),
        ("mươi", "người."), ("bắn", "chết."), ("bắn", "chết"), ("Kinshichi", "Kozuka"), ("một", "mình."), ("Nhật", "Bản"),
        ("sững", "sờ,"), ("chính", "phủ"), ("đã", "chết."), ("cũng", "vậy."), ("chàng", "trai"), ("Norio", "Suzuki"), ("bốn", "ngày,"),
        ("ảnh", "chung."), ("vị", "trí"), ("cấp", "trên."), ("thiếu", "tá"), ("tá", "Yoshimi"), ("Yoshimi", "Taniguchi,"),
        ("điểm", "hẹn"), ("đứng", "nghiêm"), ("nghiêm", "chào."), ("đơn", "vị"), ("nhiệm", "vụ"), ("chiến", "đấu."), ("trạm", "radar"),
        ("súng", "trường"), ("năm", "trăm"), ("viên", "đạn"), ("lựu", "đạn."), ("thanh", "kiếm"), ("Tổng", "thống"),
        ("Ferdinand", "Marcos."), ("ân", "xá"), ("tiếp", "diễn.")}


COMPOUNDS = """rừng núi|hòn đảo|người lính|rút vào|máy bay|kết luận|về sau|tiếp tục|dân làng|kể lại|sau này|từng người|
rời đi|bỏ nhóm|cuối cùng|cái chết|tuyên bố|còn sống|nói chuyện|chụp ảnh|mang ảnh|tìm ra|thành viên|toàn bộ|hôm sau|trình diện|
vẫn còn|bắn được|xét rằng|khi đó|chiến tranh|của địch|tìm ông|gặp được""".replace("\n", "")
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
