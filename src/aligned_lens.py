"""Grid-aligned two-circle lens: attempt at an independent reconstruction of the
`2n - 7` construction of Edelsbrunner-Hajnal (1991).

Construction principle.  Two concentric circles of radii `R > r`.  Outer arc: angles
`0, kh, 2kh, ...`; inner arc: angles `alpha + j h, ...`.  The three families of unit
distances are forced by design:

  * consecutive outer points: chord `2 R sin(kh/2) = 1`,
  * consecutive inner points: chord `2 r sin(h/2) = 1`,
  * outer point at angle `theta` with inner points at `theta +/- alpha`, where
    `cos alpha = (R^2 + r^2 - 1)/(2 R r)`.

For all of these to be *simultaneously* on a common angular grid we need
`R = 1/(2 sin(kh/2))`, `r = 1/(2 sin(h/2))` and `alpha = l*h/2` for integers `k, l`;
the last condition becomes the single equation printed below, solved by bisection.
"""

from __future__ import annotations

import math

from src.convex_geometry import degrees, is_strictly_convex_float, unit_pairs_float


def f_of_h(h: float, k: int, l: int) -> float:
    R = 1.0 / (2 * math.sin(k * h / 2))
    r = 1.0 / (2 * math.sin(h / 2))
    c = (R * R + r * r - 1.0) / (2 * R * r)
    c = max(-1.0, min(1.0, c))
    return math.acos(c) - l * h / 2


def solve_h(k: int, l: int):
    """All sign changes of f on (0, 2pi/k) -- i.e. all aligned designs."""
    sols = []
    lo, hi = 1e-4, 1.5
    n = 4000
    prev_x, prev_v = lo, f_of_h(lo, k, l)
    for i in range(1, n + 1):
        x = lo + (hi - lo) * i / n
        v = f_of_h(x, k, l)
        if prev_v * v < 0:
            a, b = prev_x, x
            for _ in range(80):
                m = (a + b) / 2
                if f_of_h(a, k, l) * f_of_h(m, k, l) <= 0:
                    b = m
                else:
                    a = m
            sols.append((a + b) / 2)
        prev_x, prev_v = x, v
    return sols


def build(h: float, k: int, l: int, n_out: int, n_in: int):
    R = 1.0 / (2 * math.sin(k * h / 2))
    r = 1.0 / (2 * math.sin(h / 2))
    alpha = l * h / 2
    pts = [(R * math.cos(j * k * h), R * math.sin(j * k * h)) for j in range(n_out)]
    pts += [(r * math.cos(alpha + i * h), r * math.sin(alpha + i * h))
            for i in range(n_in)]
    pts.sort(key=lambda p: math.atan2(p[1], p[0]))
    return pts


def main():
    best = (0, None)
    for k in range(1, 9):
        for l in range(1, 13):
            for h in solve_h(k, l):
                if not (0.05 < h < 1.2):
                    continue
                for n_out in range(3, 16):
                    for n_in in range(3, 16):
                        pts = build(h, k, l, n_out, n_in)
                        if not is_strictly_convex_float(pts):
                            continue
                        u = len(unit_pairs_float(pts, tol=1e-6))
                        n = len(pts)
                        if u > best[0]:
                            best = (u, (k, l, round(h, 6), n_out, n_in, n))
    print("best unit count found by grid alignment:", best[0],
          "params (k, l, h, n_out, n_in, n):", best[1])
    if best[1]:
        k, l, h, n_out, n_in, n = best[1]
        pts = build(h, k, l, n_out, n_in)
        print("  n =", n, " u =", len(unit_pairs_float(pts, tol=1e-6)),
              " 2n-7 =", 2 * n - 7, " u/n =", len(unit_pairs_float(pts, tol=1e-6)) / n)
        print("  degrees:", degrees(pts, tol=1e-6))


if __name__ == "__main__":
    main()
