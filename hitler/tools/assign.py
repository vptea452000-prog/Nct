"""Gán ảnh người dùng gửi (assets/user/all/10000441xx.jpg) vào mã khung hình -> assets/k/<mã>.jpg"""
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
MAP = {
 "K01": 110, "K02": 111, "K03a": 112, "K03b": 113, "K11": 123, "K04": 115, "K05a": 116, "K05b": 117, "K06": 118, "K07": 119,
 "K08": 120, "K09": 121, "K10": 122, "K12": 124, "K13": 125, "K14": 126, "K14b": 127, "K15a": 128, "K15b": 129, "K16": 130,
 "K17": 131, "K18": 132, "K19": 133, "K20": 134, "K21": 135, "K22a": 138, "K22b": 136, "K22c": 137, "K23": 139, "K24a": 141,
 "K24b": 140, "K25": 142, "K26": 143, "K27": 144, "K29": 145, "K30": 146, "K31a": 147, "K31b": 148, "K32": 149, "K33": 150,
 "K34a": 151, "K34b": 152, "K35": 153, "K36": 154, "K37": 155, "K38": 156, "K39": 157, "K40": 158, "K41a": 159, "K41b": 160,
 "K42": 161, "K43a": 162, "K43b": 163, "K44": 164, "K45": 165, "K46": 166, "K47": 167, "K48": 168, "K49": 169, "K50": 170,
 "K51": 171, "K52a": 172, "K52b": 173, "K53": 174, "K54a": 175, "K54b": 176, "K55": 177, "K56a": 178, "K56b": 179, "K57": 180,
 "K58": 181, "K59": 182, "K59b": 183, "K60": 184, "K61": 185, "K61b": 186, "K_x114": 114,
}
out = ROOT / "assets" / "k"; out.mkdir(parents=True, exist_ok=True)
for code, n in MAP.items():
    Image.open(ROOT / "assets" / "user" / "all" / f"1000044{n}.jpg").convert("RGB").save(out / f"{code}.jpg", quality=95)
print(len(MAP), "ảnh")
