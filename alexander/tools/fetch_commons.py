"""Tải bản gốc từ Wikimedia Commons theo danh sách (mã → tên file hoặc từ khóa tìm).
  python3 tools/fetch_commons.py            → assets/src/<mã>.<đuôi> + assets/src/nguon.txt
Mục "?..." = tìm theo từ khóa, lấy kết quả ảnh đầu tiên.
"""
import json, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "src"
UA = {"User-Agent": "NctVideoResearch/1.0 (https://github.com/vptea452000-prog/nct)"}
WIDTH = 1920   # cỡ ảnh thu nhỏ chuẩn của Wikimedia (tránh bị giới hạn khi tải bản gốc)
API = "https://commons.wikimedia.org/w/api.php"

ITEMS = {
    "K01a": "File:Tigris River in early morning.jpg",
    "K01b": "File:Sunset in Baghdad, Iraq.jpg",
    "K03": "?Macedonian phalanx Johnny Shumate",
    "K04": "File:Middle East topographic map-blank.svg",
    "K04b": "File:Satellite relief map of Middle East.png",
    "K05a": "File:Hindu Kush Range.jpg",
    "K05b": "?The army crosses the Gedrosian Desert Andre Castaigne",
    "K06": "File:Darius III mosaic.jpg",
    "K06b": "File:Alexandermosaic.jpg",
    "K09": "File:Persepolis The Persian Soldiers.jpg",
    "K11": "?Alexander addresses his officers before the battle of Issus Castaigne",
    "K13": "File:Lysimachus coin, Alexander depiction, 297-282 B.C., Thrace.jpg",
    "K13b": "File:Alexander coin, British Museum.jpg",
    "K14": "?Alexander quelling the Opis mutiny Andre Castaigne",
    "K16": "File:Alexandre Azara - Musée du Louvre AGER Ma 436 ; MR 405 (cropped).jpg",
    "K16b": "?Marble head of Alexander the Great Giannitsa Pella",
    "K18": "File:Philip II of Macedon Ny Carlsberg Glyptotek IN2263.jpg",
    "K18b": "File:Ivory portrait of Philip II.jpg",
    "K19": "?Roman Shepherd's Family with their Flock",
    "K20": "?Pella Mosaics The Lion Hunt",
    # để dành cho phần sau
    "K29": "File:Charles Le Brun - Entry of Alexander into Babylon.JPG",
    "K36": "?The marriages of Alexander and his men to the Persian princesses Castaigne",
    "K45": "?Persépolis, Irán, 2016-09-24, DD 53",
    "K52": "?The dying Alexander receiving his soldiers Castaigne",
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
                time.sleep(15 * (k + 1)); continue
            if "400" in str(e) or "404" in str(e) or "500" in str(e):
                return False
            raise
    return False


OUT.mkdir(parents=True, exist_ok=True)
log = []
for code, entry in ITEMS.items():
    if list(OUT.glob(f"{code}.*")):
        print(f"{code}: đã có"); continue
    try:
        title = resolve(entry)
        if not title:
            print(f"{code}: KHÔNG TÌM THẤY ({entry})"); log.append(f"{code}\t—\tkhông tìm thấy: {entry}"); continue
        ok = False
        for w in (WIDTH, 1280):
            url, ext = thumb_url(title, w)
            dst = OUT / f"{code}{'.jpg' if ext in ('.jpeg',) else ext}"
            if download(url, dst):
                ok = True; break
        if not ok:   # ảnh nhỏ hơn 1920: tải bản gốc
            name = title.split(":", 1)[1].replace(" ", "_"); h = hashlib.md5(name.encode()).hexdigest()
            dst = OUT / f"{code}{Path(name).suffix.lower()}"
            ok = download(f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{urllib.parse.quote(name)}", dst)
        print(f"{code}: {title} → {dst.name if ok else 'LỖI TẢI'}")
        log.append(f"{code}\t{title}\thttps://commons.wikimedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}")
        time.sleep(3)
    except Exception as e:
        print(f"{code}: LỖI {e}"); log.append(f"{code}\tlỗi\t{e}")
with open(OUT / "nguon.txt", "a") as f:
    f.write("\n".join(log) + "\n")
