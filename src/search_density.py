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
import scipy.optimize
import scipy.spatial.distance

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
    d = scipy.spatial.distance.pdist(xy)
    return float(np.sum(np.exp(-((d - 1.0) ** 2) / (2 * sigma ** 2))))


def convexity_penalty(xy: np.ndarray) -> float:
    """Convexity penalty.

    Args:
        xy:

    Returns:
        The computed result

    """
    n = xy.shape[0]
    cx = np.mean(xy[:, 0])
    cy = np.mean(xy[:, 1])
    angles = np.arctan2(xy[:, 1] - cy, xy[:, 0] - cx)
    order = np.argsort(angles)
    xy_sorted = xy[order]

    o = xy_sorted
    a = np.roll(xy_sorted, -1, axis=0)

    edge = a - o
    b_to_o = xy_sorted[np.newaxis, :, :] - o[:, np.newaxis, :]

    cr = edge[:, 0:1] * b_to_o[:, :, 1] - edge[:, 1:2] * b_to_o[:, :, 0]

    mask = np.ones((n, n), dtype=bool)
    np.fill_diagonal(mask, False)
    mask[np.arange(n), (np.arange(n) + 1) % n] = False

    pen = np.sum(np.where(cr[mask] <= 1e-3, (-cr[mask] + 1e-3)**2, 0.0))
    return float(pen)


def init_convex(n: int, rng: random.Random) -> np.ndarray:
    """Start from a two-arc 'lens' configuration whose boundary edges are unit by
    construction (this is the family that realises the 2n-7 bound), or from a jittered
    circle with unit edges."""
    for _ in range(400):
        r_out = rng.uniform(0.55, 4.0)
        r_ = rng.uniform(0.55, 4.0)
        step1 = 2 * math.asin(min(1.0, 1.0 / (2 * r_out)))
        step2 = 2 * math.asin(min(1.0, 1.0 / (2 * r_)))
        ang0 = rng.uniform(0, 2 * math.pi)
        phase = math.pi * rng.uniform(-0.5, 0.5)
        n1 = max(2, n // 2)
        pts = [(r_out * math.cos(ang0 + k * step1), r_out * math.sin(ang0 + k * step1))
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


def anneal(n: int, seed: int = 0):
    """Optimize using structured constrained optimization (L-BFGS-B).

    Args:
        n: number of points
        seed (int): random seed for initialization

    Returns:
        tuple: (best_xy, best_v)
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
    x_flat = xy.flatten()

    def objective(x_flat_arr, sigma):
        xy_arr = x_flat_arr.reshape((n, 2))
        score = soft_score(xy_arr, sigma)
        pen = convexity_penalty(xy_arr)
        return -(score - 300.0 * pen)

    sigmas = [0.15, 0.05, 0.01, 0.005, 0.001]

    best_xy = xy.copy()
    best_v = len(unit_pairs_float(best_xy, tol=1e-6))

    for sigma in sigmas:
        res = scipy.optimize.minimize(objective, x_flat, args=(sigma,), method='L-BFGS-B')
        x_flat = res.x
        xy_cand = x_flat.reshape((n, 2))
        cand_v = len(unit_pairs_float(xy_cand, tol=1e-6))
        if cand_v > best_v and is_strictly_convex_float(xy_cand):
            best_v = cand_v
            best_xy = xy_cand.copy()

    return best_xy, best_v


def run(n_values, seeds):
    """Worker function for parallel processing.

    Args:
        n_values:
        seeds:

    """
    print(f"{'n':>3} {'best u(P)':>10} {'u/n':>7} {'2n-7':>6} {'convex':>7}  degrees")
    for n in n_values:
        best, best_xy = 0, None
        for s in range(seeds):
            xy, v = anneal(n, seed=s)
            v = len(unit_pairs_float(xy, tol=1e-6))
            if v > best:
                best, best_xy = v, xy
        if best_xy is None:
            best_xy = init_convex(n, random.Random(0))
        print(f"{n:>3} {best:>10} {best / n:>7.3f} {max(2 * n - 7, 0):>6} "
              f"{str(is_strictly_convex_float(best_xy)):>7}  {degrees(best_xy, tol=1e-6)}")


if __name__ == "__main__":
    run(n_values=list(range(6, 15)), seeds=3)
