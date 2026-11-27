"""Xuất video Titanic: python3 src/render.py sheet A|… | preview t… | full"""
import math, subprocess, sys
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import shots as S  # noqa
from scenes import skia, W, H, FPS, P, DUR, subtitle  # noqa
from PIL import Image  # noqa

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
SHOTS = S.SHOTS if hasattr(S, "SHOTS") else []
FADE = getattr(S, "FADE", set())


def frame(t, surf=None):
    surf = surf or skia.Surface(W, H)
    c = surf.getCanvas(); c.clear(skia.ColorBLACK)
    for a, b, fn in SHOTS:
        if a <= t < b:
            c.save(); fn(c, t); c.restore()
            for f in FADE:
                if abs(t - f) < 0.3:
                    c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 255 * (1 - abs(t - f) / 0.3)))
            break
    if t < S.NO_SUB_FROM:
        subtitle(c, t)
    if t > DUR - 1.0:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 255 * min(1, (t - (DUR - 1.0)))))
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def chunk(args):
    k, f0, f1 = args
    out = BUILD / f"c_{k:02d}.mp4"
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
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
        sel = [(a, b) for a, b, _ in SHOTS if lo <= a < hi]
        ts = [a + (b - a) * 0.6 for a, b in sel]
        ims = [Image.fromarray(frame(x)[..., :3]).resize((480, 270)) for x in ts]
        sh = Image.new("RGB", (480 * 4, 270 * max(1, math.ceil(len(ims) / 4))))
        for i, im in enumerate(ims):
            sh.paste(im, ((i % 4) * 480, (i // 4) * 270))
        sh.save(BUILD / f"sheet_{int(lo)}.png")
    else:
        nfr = int(DUR * FPS); step = math.ceil(nfr / 24)
        with Pool(4) as pool:
            chs = pool.map(chunk, [(k, f, min(nfr, f + step)) for k, f in enumerate(range(0, nfr, step))])
        (BUILD / "c.txt").write_text("".join(f"file '{x.name}'\n" for x in chs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(BUILD / "c.txt"), "-c", "copy",
                        str(BUILD / "Titanic_nosfx.mp4")], check=True)
        for x in chs:
            x.unlink()
        (BUILD / "c.txt").unlink()
        print("xong")
