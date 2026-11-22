import cv2, numpy as np
im = cv2.imread("assets/k/K16b.jpg"); h, w = im.shape[:2]
s = 1000 / h; sm = cv2.resize(im, (int(w*s), 1000))
mask = np.zeros(sm.shape[:2], np.uint8)
rect = (int(sm.shape[1]*0.06), 10, int(sm.shape[1]*0.88), 975)
bg = np.zeros((1,65), np.float64); fg = np.zeros((1,65), np.float64)
cv2.grabCut(sm, mask, rect, bg, fg, 8, cv2.GC_INIT_WITH_RECT)
m = np.where((mask==1)|(mask==3), 255, 0).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(m)
big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); m = np.where(lab==big, 255, 0).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9,9),np.uint8))
m = cv2.resize(m, (w, h), interpolation=cv2.INTER_LINEAR); m = cv2.GaussianBlur(m, (7,7), 0)
out = np.dstack([im, m]); cv2.imwrite("thumb/head_cut.png", out)
prev = im.copy(); prev[m<128] = (40,200,40); cv2.imwrite("thumb/_cut_prev.jpg", cv2.resize(prev,(int(w*s*0.6),600)))
