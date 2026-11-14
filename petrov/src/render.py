"""Xuất tập Petrov.

  python3 src/render.py preview 3.0 29.5 ...   → build/preview_<t>.png (xem thử khung hình)
  python3 src/render.py sheet                  → build/contact_sheet.png (dải khung hình toàn tập, 1 khung/1,5 s)
  python3 src/render.py full                   → build/Petrov_v1.mp4 + build/Petrov_v1.srt
"""
import json, math, subprocess, sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import skia
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ROOT, W, H, FPS, draw_grain  # noqa
import subs, scenes  # noqa

DUR = 104.088
NFR = int(math.ceil(DUR * FPS))
BUILD = ROOT / "build"
_cues = None


def cues():
    global _cues
    if _cues is None:
        words = json.loads((BUILD / "words.json").read_text(encoding="utf-8"))
        _cues = subs.build_cues(words)
    return _cues


def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas()
    c.clear(skia.ColorBLACK)
    scenes.draw_frame(c, t)
    draw_grain(c, 34)
    subs.draw_sub(c, cues(), t)
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def render_chunk(args):
    k, f0, f1 = args
    out = BUILD / f"chunk_{k:02d}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-g", "60", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surf = skia.Surface(W, H)
    for i in range(f0, f1):
        p.stdin.write(frame(i / FPS, surf).tobytes())
    p.stdin.close()
    p.wait()
    return out


def full(workers=4):
    subs.write_srt(cues(), BUILD / "Petrov_v1.srt")
    step = math.ceil(NFR / (workers * 3))
    jobs = [(k, f0, min(NFR, f0 + step)) for k, f0 in enumerate(range(0, NFR, step))]
    with Pool(workers) as pool:
        chunks = pool.map(render_chunk, jobs)
    lst = BUILD / "chunks.txt"
    lst.write_text("".join(f"file '{c.name}'\n" for c in chunks))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(BUILD / "video_only.mp4")], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(BUILD / "video_only.mp4"), "-i", str(ROOT / "audio/voice.mp3"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-t", f"{DUR:.3f}", "-movflags", "+faststart", str(BUILD / "Petrov_v1.mp4")], check=True)
    for c in chunks:
        c.unlink()
    print("xong:", BUILD / "Petrov_v1.mp4")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "preview":
        for ts in sys.argv[2:]:
            arr = frame(float(ts))
            Image.fromarray(arr[..., :3]).save(BUILD / f"preview_{float(ts):06.2f}.png")
    elif mode == "sheet":
        times = [float(x) for x in sys.argv[2:]] or [i * 1.5 + 0.7 for i in range(int(DUR / 1.5))]
        cols = 8
        tw_, th_ = 216, 384
        rows = math.ceil(len(times) / cols)
        sheet = Image.new("RGB", (cols * tw_, rows * (th_ + 24)), "white")
        from PIL import ImageDraw
        d = ImageDraw.Draw(sheet)
        for i, ts in enumerate(times):
            im = Image.fromarray(frame(ts)[..., :3]).resize((tw_, th_), Image.BILINEAR)
            x, y = (i % cols) * tw_, (i // cols) * (th_ + 24)
            sheet.paste(im, (x, y))
            d.text((x + 4, y + th_ + 4), f"{ts:.2f}s", fill="black")
        sheet.save(BUILD / "contact_sheet.png")
    elif mode == "full":
        full()
