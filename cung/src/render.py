"""Xuất Tập 5: Cung tên (không lời, bóng thoại).
  python3 src/render.py preview 1.0 5.0 ...  → build/preview_<t>.png
  python3 src/render.py full                 → build/Cung_v1_nosfx.mp4
"""
import math, subprocess, sys
from multiprocessing import Pool
from pathlib import Path

import skia
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ROOT, W, H, FPS, draw_grain  # noqa
import scenes  # noqa

DUR = scenes.DUR
NFR = int(math.ceil(DUR * FPS))
BUILD = ROOT / "build"

def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas()
    c.clear(skia.ColorBLACK)
    c.save()
    scenes.draw_frame(c, t)
    c.restore()
    draw_grain(c, 22)
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
            Image.fromarray(frame(float(ts))[..., :3]).save(BUILD / f"preview_{float(ts):06.2f}.png")
    elif sys.argv[1] == "sheet":
        from PIL import ImageDraw
        times = [i * 1.4 + 0.7 for i in range(int(DUR / 1.4))]
        cols, tw_, th_ = 8, 216, 384
        rows = math.ceil(len(times) / cols)
        sheet = Image.new("RGB", (cols * tw_, rows * (th_ + 24)), "white"); d = ImageDraw.Draw(sheet)
        for i, ts in enumerate(times):
            im = Image.fromarray(frame(ts)[..., :3]).resize((tw_, th_), Image.BILINEAR)
            x, y = (i % cols) * tw_, (i // cols) * (th_ + 24)
            sheet.paste(im, (x, y)); d.text((x + 4, y + th_ + 4), f"{ts:.2f}s", fill="black")
        sheet.save(BUILD / "contact_sheet.png")
    else:
        step = math.ceil(NFR / 8)
        with Pool(4) as pool:
            chunks = pool.map(chunk, [(k, f, min(NFR, f + step)) for k, f in enumerate(range(0, NFR, step))])
        (BUILD / "chunks.txt").write_text("".join(f"file '{c.name}'\n" for c in chunks))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(BUILD / "chunks.txt"), "-c", "copy",
                        str(BUILD / "Cung_v1_nosfx.mp4")], check=True)
        for c in chunks:
            c.unlink()
        (BUILD / "chunks.txt").unlink()
        print("xong")
