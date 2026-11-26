"""Xuất video Hitler: python3 src/render.py sheet | preview t… | full"""
import math, subprocess, sys
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import shots as S  # noqa
from doc import skia, W, H, FPS, finish, subtitle  # noqa
from PIL import Image  # noqa

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
SUBS = True


def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas(); c.clear(skia.ColorBLACK)
    c.save(); S.draw(c, t); c.restore()
    finish(c, t)
    if SUBS:
        subtitle(c, t, S.ALIGN, S.OFF, 1e9)
    if t > S.DUR - 1.2:
        c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.ColorSetARGB(int(255 * min(1, (t - (S.DUR - 1.2)) / 1.2)), 0, 0, 0)))
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def chunk(args):
    k, f0, f1 = args
    out = BUILD / f"c_{k:02d}.mp4"
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    s = skia.Surface(W, H)
    for i in range(f0, f1):
        pr.stdin.write(frame(i / FPS, s).tobytes())
    pr.stdin.close(); pr.wait()
    return out


if __name__ == "__main__":
    BUILD.mkdir(parents=True, exist_ok=True)
    if sys.argv[1] == "preview":
        for ts in sys.argv[2:]:
            Image.fromarray(frame(float(ts))[..., :3]).save(BUILD / f"pv_{float(ts):06.2f}.png")
    elif sys.argv[1] == "sheet":
        lo, hi = float(sys.argv[2]), float(sys.argv[3])
        ts = [S.OFF + a + (b - a) * 0.55 for a, b, _ in S.S if lo <= a < hi]
        if lo == 0:
            ts = [2.8] + ts
        ims = [Image.fromarray(frame(x)[..., :3]).resize((480, 270)) for x in ts]
        sh = Image.new("RGB", (480 * 4, 270 * max(1, math.ceil(len(ims) / 4))))
        for i, im in enumerate(ims):
            sh.paste(im, ((i % 4) * 480, (i // 4) * 270))
        sh.save(BUILD / f"sheet_{int(lo)}.png")
    else:
        nfr = int(S.DUR * FPS); step = math.ceil(nfr / 24)
        with Pool(4) as pool:
            chs = pool.map(chunk, [(k, f, min(nfr, f + step)) for k, f in enumerate(range(0, nfr, step))])
        (BUILD / "c.txt").write_text("".join(f"file '{x.name}'\n" for x in chs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(BUILD / "c.txt"), "-c", "copy",
                        str(BUILD / "Hitler_nosfx.mp4")], check=True)
        for x in chs:
            x.unlink()
        (BUILD / "c.txt").unlink()
        print("xong")
