"""Dựng lại một vài khoảng thời gian rồi ghép vào bản không tiếng (không phải xuất lại cả video).
  python3 src/patch.py 275.59 284.28 315.85 337.2
"""
import subprocess, sys
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import render as R  # noqa
from scenes import FPS, DUR  # noqa

B = R.BUILD
rng = [(float(sys.argv[i]), float(sys.argv[i + 1])) for i in range(1, len(sys.argv), 2)]
jobs = []
for k, (a, b) in enumerate(rng):
    f0, f1 = round(a * FPS), round(b * FPS)
    step = max(1, (f1 - f0 + 3) // 4)
    for j, s in enumerate(range(f0, f1, step)):
        jobs.append((100 + k * 10 + j, s, min(f1, s + step)))
with Pool(4) as pool:
    outs = pool.map(R.chunk, jobs)
src = B / "Titanic_nosfx.mp4"
pieces, t = [], 0.0
cuts = []
for k, (a, b) in enumerate(rng):
    cuts.append(("old", t, a)); cuts.append(("new", k, None)); t = b
cuts.append(("old", t, DUR))
lst = []
for i, (kind, x, y) in enumerate(cuts):
    out = B / f"seg_{i:02d}.mp4"
    if kind == "old":
        f0, f1 = round(x * FPS), round(y * FPS)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", f"trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS",
                        "-an", "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p", str(out)], check=True)
    else:
        mine = [o for (n, _, _), o in zip(jobs, outs) if 100 + x * 10 <= n < 110 + x * 10]
        (B / "p.txt").write_text("".join(f"file '{m.name}'\n" for m in mine))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(B / "p.txt"), "-c", "copy", str(out)], check=True)
    lst.append(out)
(B / "p.txt").write_text("".join(f"file '{m.name}'\n" for m in lst))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(B / "p.txt"), "-c", "copy", str(B / "Titanic_nosfx_new.mp4")], check=True)
for o in outs + lst:
    o.unlink()
(B / "p.txt").unlink()
(B / "Titanic_nosfx_new.mp4").replace(src)
print("xong")
