import sys, os
from PIL import Image, ImageDraw
src, out, names = sys.argv[1], sys.argv[2], sys.argv[3:]
S = Image.new("RGB", (2160, 1230), "white"); d = ImageDraw.Draw(S)
for i, n in enumerate(names):
    im = Image.open(os.path.join(src, n)).convert("RGB").resize((540, 1200))
    S.paste(im, (i * 540, 30)); d.text((i * 540 + 8, 8), n, fill="black")
S.save(out)
