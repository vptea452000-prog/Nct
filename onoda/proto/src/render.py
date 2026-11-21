"""Xuất bản thử phong cách hoạt hình.
  python3 src/render.py preview 1.0 5.0 ...  → build/preview_<t>.png
  python3 src/render.py full                 → build/Onoda_style_test_nosfx.mp4
"""
import math, subprocess, sys
from multiprocessing import Pool
from pathlib import Path

import skia
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ROOT, W, H, FPS, draw_grain  # noqa
import subs, scenes  # noqa

DUR = scenes.DUR
NFR = int(math.ceil(DUR * FPS))
BUILD = ROOT / "build"

# phụ đề theo lời kịch bản, mốc ước lượng (chưa có MP3)
CUES = [
    (0.2, 3.5, ["Năm 1974, trong rừng núi của", "một hòn đảo Philippines,"]),
    (3.6, 6.5, ["vẫn còn một sĩ quan Nhật mặc", "quân phục, mang súng"]),
    (6.6, 9.3, ["và tin rằng Thế chiến thứ hai", "chưa kết thúc."]),
    (9.4, 11.9, ["Ông chỉ chịu buông súng khi chỉ huy", "cũ, lúc ấy đã thành người bán sách,"]),
    (12.0, 14.3, ["bay sang đọc lệnh cho ông nghe."]),
    (14.4, 17.3, ["Người lính ấy là", "thiếu úy Hiroo Onoda."]),
]
CUES = [{"start": a, "end": b, "lines": l} for a, b, l in CUES]


def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas()
    c.clear(skia.ColorBLACK)
    c.save()
    scenes.draw_frame(c, t)
    c.restore()
    draw_grain(c, 22)
    subs.draw_sub(c, CUES, t)
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def chunk(args):
    k, f0, f1 = args
    out = BUILD / f"chunk_{k:02d}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    s = skia.Surface(W, H)
    for i in range(f0, f1):
        p.stdin.write(frame(i / FPS, s).tobytes())
    p.stdin.close(); p.wait()
    return out


if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for ts in sys.argv[2:]:
            Image.fromarray(frame(float(ts))[..., :3]).save(BUILD / f"preview_{float(ts):05.2f}.png")
    else:
        step = math.ceil(NFR / 8)
        with Pool(4) as pool:
            chunks = pool.map(chunk, [(k, f, min(NFR, f + step)) for k, f in enumerate(range(0, NFR, step))])
        (BUILD / "chunks.txt").write_text("".join(f"file '{c.name}'\n" for c in chunks))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(BUILD / "chunks.txt"), "-c", "copy",
                        str(BUILD / "Onoda_style_test_nosfx.mp4")], check=True)
        for c in chunks:
            c.unlink()
        (BUILD / "chunks.txt").unlink()
        print("xong")
