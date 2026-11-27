"""Tải bản gốc từ Wikimedia Commons theo danh sách (mã → tên file hoặc từ khóa tìm).
  python3 tools/fetch_commons.py            → assets/src/<mã>.<đuôi> + assets/src/nguon.txt
Mục "?..." = tìm theo từ khóa, lấy kết quả ảnh đầu tiên.
"""
import json, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "src"
UA = {"User-Agent": "NctVideoResearch/1.0 (https://github.com/vptea452000-prog/nct)"}
WIDTH = 3840   # cỡ thu nhỏ chuẩn của Wikimedia (3840 / 1280 / 960…); cỡ khác bị chặn 429
API = "https://commons.wikimedia.org/w/api.php"

C = " by Andre Castaigne (1898-1899).jpg"
ITEMS = {   # mã → danh sách tên file thử lần lượt
    "K01a": ["File:Tigris River in early morning.jpg"],
    "K01b": ["File:Sunset in Baghdad, Iraq.jpg"],
    "K03": ["File:Macedonian phalanx.jpg", "File:Macedonian Phalanx.jpg", "File:Phalanx (Macedonian).jpg"],
    "K04": ["File:Middle East topographic map-blank.svg"],
    "K04b": ["File:Satellite relief map of Middle East.png"],
    "K05a": ["File:Hindu Kush Range.jpg"],
    "K05b": ["File:The army crosses the Gedrosian Desert" + C],
    "K06": ["File:Darius III mosaic.jpg"],
    "K06b": ["File:Alexandermosaic.jpg", "File:Alexander-Mosaic.jpg", "File:BattleofIssus333BC-mosaic.jpg"],
    "K09": ["File:Persepolis The Persian Soldiers.jpg"],
    "K11": ["File:Alexander addresses his officers before the battle of Issus" + C],
    "K13": ["File:Lysimachus coin, Alexander depiction, 297-282 B.C., Thrace.jpg"],
    "K13b": ["File:Alexander coin, British Museum.jpg"],
    "K14": ["File:Alexander quelling the Opis mutiny" + C],
    "K16": ["File:Alexandre Azara - Musée du Louvre AGER Ma 436 ; MR 405 (cropped).jpg"],
    "K16b": ["File:Marble head of Alexander the Great (325-300 BC). Chance find from the area of Giannitsa, Archaeological Museum, Pella (6915004674).jpg"],
    "K18": ["File:Philip II of Macedon Ny Carlsberg Glyptotek IN2263.jpg"],
    "K18b": ["File:Ivory portrait of Philip II.jpg"],
    "K19": ["File:Roman Shepherd's Family with their Flock (SM 555).png"],
    "K20": ["File:Pella Mosaics I – The Lion Hunt (49988918902).jpg"],
    "K29": ["File:Charles Le Brun - Entry of Alexander into Babylon.JPG"],
    "K36": ["File:The marriages of Alexander and his men to the Persian princesses and ladies" + C],
    "K45": ["File:Persépolis, Irán, 2016-09-24, DD 53.jpg"],
    "K52": ["File:The dying Alexander receiving his soldiers" + C],
}


import hashlib


def get(params, tries=6):
    q = API + "?" + urllib.parse.urlencode(dict(params, format="json"))
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=30) as r:
                return json.load(r)
        except Exception as e:
            if "429" in str(e) or "Too many" in str(e):
                time.sleep(20 * (k + 1)); continue
            raise
    raise RuntimeError("API vẫn bị giới hạn")


OPENVERSE = "https://api.openverse.org/v1/images/"


def resolve(entry):
    """Tìm qua Openverse (chỉ mục cả Wikimedia, Flickr, bảo tàng) để tránh giới hạn của API Wikimedia."""
    if not entry.startswith("?"):
        return entry
    q = OPENVERSE + "?" + urllib.parse.urlencode(dict(q=entry[1:], source="wikimedia", page_size=5))
    with urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=30) as r:
        d = json.load(r)
    for res in d.get("results", []):
        land = res.get("foreign_landing_url", "")
        if "commons.wikimedia.org/wiki/File:" in land:
            return "File:" + urllib.parse.unquote(land.split("File:", 1)[1]).replace("_", " ")
    return None


def thumb_url(title, width=WIDTH):
    name = title.split(":", 1)[1].replace(" ", "_")
    h = hashlib.md5(name.encode()).hexdigest()
    q = urllib.parse.quote(name)
    suffix = ".png" if name.lower().endswith((".svg", ".tif", ".tiff")) else ""
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{width}px-{q}{suffix}", suffix or Path(name).suffix.lower()


def download(url, dst, tries=5):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                dst.write_bytes(r.read()); return True
        except Exception as e:
            if "429" in str(e):
                return False      # cỡ này chưa có sẵn trong bộ đệm → thử cỡ khác, không chờ
            if "400" in str(e) or "404" in str(e) or "500" in str(e):
                return False
            raise
    return False


OUT.mkdir(parents=True, exist_ok=True)
log = []
for code, cands in ITEMS.items():
    if list(OUT.glob(f"{code}.*")):
        print(f"{code}: đã có"); continue
    got = None
    for title in cands:
        name = title.split(":", 1)[1].replace(" ", "_"); h = hashlib.md5(name.encode()).hexdigest()
        tries = [thumb_url(title, w) for w in (3840, 1920, 1280, 1024, 960)] + [(f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{urllib.parse.quote(name)}", Path(name).suffix.lower())]
        for url, ext in tries:
            dst = OUT / f"{code}{'.jpg' if ext in ('.jpeg',) else ext}"
            if download(url, dst):
                got = title; break
            time.sleep(4)
        if got:
            break
    print(f"{code}: {got or 'KHÔNG TẢI ĐƯỢC'}", flush=True)
    log.append(f"{code}\t{got or '—'}\t" + (f"https://commons.wikimedia.org/wiki/{urllib.parse.quote((got or '').replace(' ', '_'))}" if got else "không tải được"))
    time.sleep(3)
with open(OUT / "nguon.txt", "a") as f:
    f.write("\n".join(log) + "\n")
