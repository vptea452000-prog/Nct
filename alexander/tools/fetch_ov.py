"""Tìm và tải tư liệu qua Openverse (gộp Wikimedia, Flickr, bảo tàng…). Openverse tự lấy ảnh gốc về rồi trả lại,
nên không bị Wikimedia giới hạn. Mỗi mã tải tối đa 2 phương án (a, b), ưu tiên ảnh lớn.
  python3 tools/fetch_ov.py            → assets/src/<mã><a|b>.jpg + assets/src/nguon_ov.tsv
"""
import json, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "src"
UA = {"User-Agent": "NctVideoResearch/1.0 (https://github.com/vptea452000-prog/nct)"}
API = "https://api.openverse.org/v1/images/"
GOOD_SRC = {"wikimedia": 3, "rawpixel": 3, "smithsonian_cooper_hewitt_museum": 2, "met": 2, "europeana": 1, "flickr": 1}

QUERIES = {
    "K01": ["Tigris river", "Tigris sunset"],
    "K03": ["Macedonian phalanx", "phalanx sarissa"],
    "K04": ["Middle East topographic map blank", "Middle East relief map"],
    "K05": ["Hindu Kush mountains", "Makran desert", "Indus river"],
    "K06": ["Alexander mosaic Naples Darius", "Battle of Issus mosaic"],
    "K07": ["ancient soldiers resting painting", "wounded soldier ancient painting"],
    "K08": ["Alexander the Great Persian court painting", "Alexander proskynesis"],
    "K09": ["Persepolis soldiers relief", "Persian Immortals relief"],
    "K11": ["Alexander the Great addressing army", "Alexander speech soldiers engraving"],
    "K12": ["mutiny soldiers ancient engraving", "Opis mutiny"],
    "K13": ["Lysimachus tetradrachm Alexander", "Zeus Ammon coin"],
    "K14": ["Alexander the Great angry painting", "Alexander Castaigne"],
    "K16": ["Alexander the Great bust Louvre", "Alexander the Great marble head"],
    "K18": ["Philip II of Macedon bust", "Philip II Vergina ivory"],
    "K19": ["shepherd sheep mountains Greece", "ancient shepherd painting"],
    "K20": ["Pella mosaic lion hunt", "Pella ancient city"],
    "K29": ["Entry of Alexander into Babylon Le Brun", "Alexander Babylon triumph"],
    "K36": ["Susa weddings Alexander", "wedding of Alexander and Stateira"],
    "K52": ["Death of Alexander the Great Piloty", "death of Alexander painting"],
}


def call(url, tries=4, raw=False):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                data = r.read()
            return data if raw else json.loads(data)
        except Exception as e:
            time.sleep(15 * (k + 1))
    return None


def search(q):
    d = call(API + "?" + urllib.parse.urlencode(dict(q=q, page_size=20, mature="false")))
    time.sleep(6)
    return d.get("results", []) if d else []


def score(r):
    w, h = r.get("width") or 0, r.get("height") or 0
    return GOOD_SRC.get(r.get("source"), 0) * 1000 + min(w, 6000) / 4 + (200 if w >= h else 0)


OUT.mkdir(parents=True, exist_ok=True)
log = open(OUT / "nguon_ov.tsv", "a")
for code, qs in QUERIES.items():
    if len(list(OUT.glob(f"{code}*.*"))) >= 2:
        print(f"{code}: đã có", flush=True); continue
    pool, seen = [], set()
    for q in qs:
        for r in search(q):
            if r["id"] in seen or (r.get("width") or 0) < 800:
                continue
            seen.add(r["id"]); pool.append(r)
        if len(pool) >= 6:
            break
    pool.sort(key=score, reverse=True)
    n = 0
    for r in pool:
        if n >= 2:
            break
        data = call(f"{API}{r['id']}/thumb/?full_size=true&compressed=false", raw=True)
        time.sleep(6)
        if not data or len(data) < 20000:
            continue
        suf = "ab"[n]
        (OUT / f"{code}{suf}.jpg").write_bytes(data)
        log.write(f"{code}{suf}\t{r.get('source')}\t{r.get('width')}x{r.get('height')}\t{r.get('title')}\t{r.get('foreign_landing_url')}\n"); log.flush()
        print(f"{code}{suf}: [{r.get('source')}] {r.get('title')[:70]} ({r.get('width')}×{r.get('height')})", flush=True)
        n += 1
    if n == 0:
        print(f"{code}: KHÔNG CÓ", flush=True)
