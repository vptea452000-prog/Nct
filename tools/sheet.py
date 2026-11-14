import sys, glob, os
from PIL import Image, ImageDraw, ImageOps
fs = sorted(glob.glob(os.path.join(sys.argv[1], "*.jpg")))
tw, th = 480, 480
cols = 4
rows = (len(fs) + cols - 1) // cols
S = Image.new("RGB", (cols * tw, rows * (th + 30)), "white")
d = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    im = Image.open(f); sz = im.size; im = ImageOps.exif_transpose(im).convert("RGB")
    im.thumbnail((tw, th))
    x, y = (i % cols) * tw, (i // cols) * (th + 30)
    S.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
    d.text((x + 6, y + th + 6), f"{os.path.basename(f)} {sz[0]}x{sz[1]}", fill="black")
S.save(sys.argv[2])
