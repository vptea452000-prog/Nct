"""Nhép miệng theo giọng ú ớ: tạo lại đúng đoạn babble (cùng seed, cùng mốc giờ như sfx_events) rồi lấy đường bao âm lượng.

Dùng:  ls = LipSync(T, cache_path)   # T = beats.T
       ls.talk("gam", t)  → 0..1 độ mở miệng tại thời điểm t
Quy ước mốc giờ phải trùng với sfx_events: seed=100+i, bắt đầu a+0.12 (ngoại lệ trong `starts`), kết thúc b-0.45.
"""
import numpy as np
from pathlib import Path
from babble import babble
from sfx_lib import SR

FR = 100  # mẫu đường bao mỗi giây


class LipSync:
    def __init__(self, T, cache, starts=None, lead=0.12, tail=0.45):
        cache = Path(cache)
        starts = starts or {}
        self.clips = []  # (spk, t0, env)
        if cache.exists():
            z = np.load(cache, allow_pickle=True)
            self.clips = list(z["clips"])
            return
        for i, (name, (a, b, row)) in enumerate(T.items()):
            spk, kind, txt, emo = row[3], row[4], row[5], row[6]
            if not (spk and kind != "think" and txt):
                continue
            st = a + starts.get(name, lead)
            d = max(0.35, (b - tail) - st)
            x = babble(spk, d, emo, kind, seed=100 + i)
            hop = SR // FR
            n = len(x) // hop
            env = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1))
            env = env / (np.percentile(env, 95) + 1e-9)
            # làm mượt: miệng mở nhanh, khép chậm hơn chút
            out = np.zeros_like(env); v = 0.0
            for k, e in enumerate(env):
                v = v + (e - v) * (0.6 if e > v else 0.25)
                out[k] = v
            self.clips.append((spk, st, np.clip(out, 0, 1.2)))
        cache.parent.mkdir(parents=True, exist_ok=True)
        np.savez(cache, clips=np.array(self.clips, dtype=object))

    def talk(self, spk, t):
        for s, t0, env in self.clips:
            if s == spk and t0 <= t < t0 + len(env) / FR:
                return float(min(1.0, env[int((t - t0) * FR)]))
        return 0.0
