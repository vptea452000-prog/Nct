import sys, numpy as np
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
box = tuple(int(v) for v in sys.argv[3].split(",")) if len(sys.argv) > 3 else (0, 330, 1080, 2150)
im = Image.open(src).convert("RGB").crop(box)
a = np.asarray(im).astype(int)
bg = a[5, 5]
m = (np.abs(a - bg).sum(2) > 40)
rows, cols = np.where(m.any(1))[0], np.where(m.any(0))[0]
y0, y1, x0, x1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
out = im.crop((x0 + 2, y0 + 2, x1 - 2, y1 - 2))
out.save(dst, quality=95)
print(dst, out.size)
