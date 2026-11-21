"""Gán ảnh chủ kênh gửi (assets/user/1000044xxx.jpg) vào mã khung hình → assets/k/<mã>.jpg"""
import shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC, DST = ROOT / "assets" / "user", ROOT / "assets" / "k"
MAP = {
    "K01a": 4012, "K01b": 4013, "K03": 4014, "K04": 4015,
    "K05a": 4018, "K05b": 4017, "K05c": 4022, "K06": 4021, "K06b": 4020,
    "K09": 4066, "K11a": 4026, "K11b": 4030, "K13": 4028, "K14a": 4025, "K14b": 4067,
    "K16a": 4032, "K16b": 4073, "K18": 4033, "K18b": 4041, "K19": 4034, "K20a": 4035, "K20b": 4036,
    "K22a": 4038, "K23": 4039, "K24": 4040, "K26a": 4043, "K26b": 4042, "K27": 4044,
    "K28b": 4046, "K45c": 4049, "K30a": 4047, "K30b": 4048, "K31": 4050, "K32": 4052,
    "K33": 4053, "K34a": 4062, "K34b": 4054, "K35a": 4055, "K35b": 4056, "K35c": 4057, "K36": 4023,
    "K37": 4059, "K38": 4060, "K39": 4061, "K42a": 4068, "K45a": 4064, "K45b": 4065, "K50": 4058,
    "K52a": 4072, "K52b": 4024, "K52c": 4071, "K54": 4073,
}
DST.mkdir(parents=True, exist_ok=True)
for k, n in MAP.items():
    shutil.copy(SRC / f"100004{n}.jpg", DST / f"{k}.jpg")
from PIL import Image
for k in ("K16a", "K16b", "K54"):          # đầu tượng chụp nằm nghiêng → xoay đứng lại
    im = Image.open(DST / f"{k}.jpg"); im.rotate(-90, expand=True).save(DST / f"{k}.jpg", quality=95)
print(len(MAP), "file")
