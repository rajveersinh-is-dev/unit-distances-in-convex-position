"""Two-circle lens family: random-restart local search.

Parameters: outer radius R, inner radius r, angular steps (hR, hr) of the two arcs,
and the phase offset between the arcs.  The number of points on each arc is chosen to
reach a prescribed total n.  Objective: soft count of unit distances, with a convexity
penalty; only strictly convex results are reported.
"""

from __future__ import annotations

import math
import random

import numpy as np

from src.convex_geometry import degrees, is_strictly_convex_float, unit_pairs_float


def build(R, r, hR, hr, phase, n_out, n_in):
    if not (0.3 < R and 0.3 < r and 0 < hR < math.pi and 0 < hr < math.pi):
        return None
    if 2 * R * math.sin(hR / 2) < 1 - 1e-9 or 2 * r * math.sin(hr / 2) < 1 - 1e-9:
        return None
    pts = [(R * math.cos(j * hR), R * math.sin(j * hR)) for j in range(n_out)]
    pts += [(r * math.cos(phase + k * hr), r * math.sin(phase + k * hr))
            for k in range(n_in)]
    pts.sort(key=lambda p: math.atan2(p[1], p[0]))
    return np.array(pts)


def soft(xy, sigma):
    diff = xy[:, None, :] - xy[None, :, :]
    d = np.sqrt((diff ** 2).sum(-1))
    iu = np.triu_indices(xy.shape[0], 1)
    return float(np.exp(-((d[iu] - 1.0) ** 2) / (2 * sigma ** 2)).sum())


def penalty(xy):
    n = len(xy)
    p = 0.0
    for i in range(n):
        a, b, c = xy[i], xy[(i + 1) % n], xy[(i + 2) % n]
        cr = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if cr <= 0:
            p += -cr + 1e-3
    return p


def search(n, seed, iters=4000):
    rng = random.Random(seed)
    best = (0, None, None)
    for restart in range(60):
        R = rng.uniform(0.7, 3.0)
        r = rng.uniform(0.6, 2.5)
        hR = rng.uniform(0.05, 1.0)
        hr = rng.uniform(0.05, 1.0)
        phase = rng.uniform(math.pi * 0.3, math.pi * 1.7)
        n_out = max(2, n // 2 + rng.randint(0, 2))
        n_in = max(2, n - n_out)
        params = np.array([R, r, hR, hr, phase], dtype=float)
        step = 0.4
        for it in range(iters // 60):
            step = 0.4 * (1 - it / (iters // 60)) + 1e-3
            cand = params + np.array([rng.gauss(0, step) for _ in range(5)])
            xy = build(*cand, n_out, n_in)
            old = build(*params, n_out, n_in)
            if xy is None:
                continue
            f = soft(xy, 0.02) - 300.0 * penalty(xy)
            fo = soft(old, 0.02) - 300.0 * penalty(old) if old is not None else -1e9
            if f > fo:
                params = cand
            u = len(unit_pairs_float(xy, tol=1e-6))
            if u > best[0] and penalty(xy) == 0:
                best = (u, (round(float(R), 4), round(float(r), 4),
                            round(float(hR), 4), round(float(hr), 4),
                            round(float(phase), 4), n_out, n_in), xy)
    return best


if __name__ == "__main__":
    for n in range(8, 17):
        u, params, xy = search(n, seed=0)
        print(f"n={n:>3} best u(P)={u:>3} u/n={u / n:.3f} 2n-7={2 * n - 7:>3} params={params}")
        if xy is not None:
            print("        degrees:", degrees(xy, tol=1e-6),
                  "convex:", is_strictly_convex_float(xy))
