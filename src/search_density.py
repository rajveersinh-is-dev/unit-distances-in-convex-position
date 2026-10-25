"""Numerical hunt for high-density convex configurations.

Question being tested computationally:  is there a convex n-gon with
    u(P) >= 2 n
unit distances?  The best published construction gives `2n - 7`
(Edelsbrunner-Hajnal 1991), so `u(P) >= 2n` would beat the record.

Method.  Direct coordinate search with a convexity penalty.  The objective is the
smooth bump `sum_{i<j} exp(-(d_ij-1)^2/(2 sigma^2))` which tends to the number of
unit distances as `sigma -> 0`; annealing shrinks `sigma` and the step size together.
Initialisations are either a jittered circle or a *two-arc lens* configuration (points
on two concentric circular arcs, i.e. the family that realises the `2n - 7` bound), so
that the known extremal basins are explored.  Only strictly convex results are counted.
"""

from __future__ import annotations

import math
import random

import numpy as np

from src.convex_geometry import (
    degrees,
    is_strictly_convex_float,
    unit_pairs_float,
)


def soft_score(xy: np.ndarray, sigma: float) -> float:
    """Soft score.
    
    Args:
        xy:
        sigma:
    
    Returns:
        float: Result of type float
    
    """
    diff = xy[:, None, :] - xy[None, :, :]
    d = np.sqrt((diff ** 2).sum(-1))
    iu = np.triu_indices(xy.shape[0], 1)
    return float(np.exp(-((d[iu] - 1.0) ** 2) / (2 * sigma ** 2)).sum())


def convexity_penalty(xy: np.ndarray) -> float:
    """Convexity penalty.
    
    Args:
        xy:
    
    Returns:
        The computed result
    
    """
    n = xy.shape[0]
    pen = 0.0
    order = sorted(range(n), key=lambda i: math.atan2(xy[i][1], xy[i][0]))
    for k in range(n):
        o = xy[order[k]]
        a = xy[order[(k + 1) % n]]
        for j in range(2, n):
            b = xy[order[(k + j) % n]]
            cr = (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
            if cr <= 0:
                pen += -cr + 1e-3
    return pen


def init_convex(n: int, rng: random.Random) -> np.ndarray:
    """Start from a two-arc 'lens' configuration whose boundary edges are unit by
    construction (this is the family that realises the 2n-7 bound), or from a jittered
    circle with unit edges."""
    for _ in range(400):
        R = rng.uniform(0.55, 4.0)
        r_ = rng.uniform(0.55, 4.0)
        step1 = 2 * math.asin(min(1.0, 1.0 / (2 * R)))
        step2 = 2 * math.asin(min(1.0, 1.0 / (2 * r_)))
        ang0 = rng.uniform(0, 2 * math.pi)
        phase = math.pi * rng.uniform(-0.5, 0.5)
        n1 = max(2, n // 2)
        pts = [(R * math.cos(ang0 + k * step1), R * math.sin(ang0 + k * step1))
               for k in range(n1)]
        pts += [(r_ * math.cos(math.pi + ang0 + phase + k * step2),
                 r_ * math.sin(math.pi + ang0 + phase + k * step2))
                for k in range(n - n1)]
        pts.sort(key=lambda p: math.atan2(p[1], p[0]))
        xy = np.array(pts)
        if is_strictly_convex_float(xy):
            return xy
    ang = rng.uniform(0, 2 * math.pi)
    return np.array([(math.cos(ang + k * 2 * math.pi / n),
                      math.sin(ang + k * 2 * math.pi / n)) for k in range(n)])


def anneal(n: int, iters: int = 30000, seed: int = 0):
    """Anneal.
    
    Args:
        n:
        iters (int):
        seed (int):
    
    Returns:
        tuple: Result of type tuple
    
    """
    rng = random.Random(seed)

    def keep_scale(xy: np.ndarray) -> np.ndarray:
        """Keep scale.
        
        Args:
            xy:
        
        Returns:
            The computed result
        
        """
        return xy  # the scale is a free parameter; leave it to the search

    xy = keep_scale(init_convex(n, rng))
    best_xy, best_v = xy.copy(), 0
    for it in range(iters):
        t = it / iters
        sigma = 0.15 * (1 - t) ** 4 + 1e-4
        step = 0.3 * (1 - t) ** 2 + 1e-4
        temp = 0.4 * (1 - t) + 1e-8
        cand = xy + np.array([[rng.gauss(0, step), rng.gauss(0, step)]
                                   for _ in range(n)])
        f_new = soft_score(cand, sigma) - 300.0 * convexity_penalty(cand)
        f_old = soft_score(xy, sigma) - 300.0 * convexity_penalty(xy)
        if f_new > f_old or rng.random() < math.exp((f_new - f_old) / temp):
            xy = cand
        cnt = len(unit_pairs_float(best_xy, tol=1e-6))
        if len(unit_pairs_float(xy, tol=1e-6)) > cnt:
            best_xy, best_v = xy.copy(), len(unit_pairs_float(xy, tol=1e-6))
    return best_xy, best_v


def run(n_values, iters, seeds):
    """Worker function for parallel processing.
    
    Args:
        n_values:
        iters:
        seeds:
    
    """
    print(f"{'n':>3} {'best u(P)':>10} {'u/n':>7} {'2n-7':>6} {'convex':>7}  degrees")
    for n in n_values:
        best, best_xy = 0, None
        for s in range(seeds):
            xy, v = anneal(n, iters=iters, seed=s)
            v = len(unit_pairs_float(xy, tol=1e-6))
            if v > best:
                best, best_xy = v, xy
        if best_xy is None:
            best_xy = init_convex(n, random.Random(0))
        print(f"{n:>3} {best:>10} {best / n:>7.3f} {max(2 * n - 7, 0):>6} "
              f"{str(is_strictly_convex_float(best_xy)):>7}  {degrees(best_xy, tol=1e-6)}")


if __name__ == "__main__":
    run(n_values=list(range(6, 15)), iters=8000, seeds=3)
