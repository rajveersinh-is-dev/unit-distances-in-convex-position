'''aligned_lens.py

Grid‑aligned two‑circle lens construction.

The module reproduces the classic ``2n‑7`` construction of Edelsbrunner‑Hajnal
(1991).  Two concentric circles of radii ``R > r`` are populated with points on
an angular grid.  The radii and the angular offset ``α`` are chosen so that three
families of unit distances are forced by design:

* consecutive outer points – chord length ``1``,
* consecutive inner points – chord length ``1``,
* an outer point at angle ``θ`` is at distance ``1`` from the two inner points at
  angles ``θ ± α``.

The equations can be reduced to a single scalar equation ``f(h) = 0`` where
``h`` is the base angular step.  For given integer parameters ``k`` and ``l`` the
function ``solve_h`` finds all sign changes of ``f`` on the interval ``(0,
2π/k)`` – each sign change corresponds to a viable aligned design.

All public functions are type‑annotated and contain exhaustive docstrings.
The implementation is defensive: invalid arguments raise ``ValueError`` and
edge cases (e.g. division by zero) are handled explicitly.
'''  # noqa: D400

from __future__ import annotations

import math
from typing import List, Tuple

from src.convex_geometry import (
    degrees,
    is_strictly_convex_float,
    unit_pairs_float,
)

__all__: List[str] = [
    "f_of_h",
    "solve_h",
    "build",
    "main",
]

# ---------------------------------------------------------------------------
# Helper constants
# ---------------------------------------------------------------------------
_TOL_BISECT = 1e-12  # tolerance for the bisection termination
_MAX_ITER_BISECT = 80  # safety guard – should be plenty for double precision


def _clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    """Clamp *value* to the interval ``[low, high]``.

    The cosine term in :func:`f_of_h` may drift slightly outside ``[-1, 1]`` due
    to rounding errors; clamping prevents ``math.acos`` from raising a
    ``ValueError``.
    """
    return max(low, min(high, value))


def f_of_h(h: float, k: int, l: int) -> float:
    """Scalar equation whose root yields a valid angular step ``h``.

    Parameters
    ----------
    h:
        Base angular step (radians).  Must be strictly positive.
    k:
        Positive integer determining the outer‑arc step ``k·h``.
    l:
        Positive integer determining the angular offset ``α = l·h/2``.

    Returns
    -------
    float
        The value ``acos(c) - l·h/2`` where ``c`` is the cosine of the required
        offset.  A root of this function corresponds to a configuration where
        the three families of unit distances are simultaneously satisfied.

    Raises
    ------
    ValueError
        If ``h`` is non‑positive or if ``k``/``l`` are not positive integers.
    """
    if h <= 0:
        raise ValueError("h must be positive")
    if k <= 0 or l <= 0:
        raise ValueError("k and l must be positive integers")

    # Radii derived from the unit‑chord condition.
    sin_kh_half = math.sin(k * h / 2)
    sin_h_half = math.sin(h / 2)
    if sin_kh_half == 0 or sin_h_half == 0:
        # This would lead to division by zero – treat as an invalid configuration.
        raise ValueError("sin(k·h/2) and sin(h/2) must be non‑zero")

    R = 1.0 / (2.0 * sin_kh_half)
    r = 1.0 / (2.0 * sin_h_half)
    c = (R * R + r * r - 1.0) / (2.0 * R * r)
    c = _clamp(c)  # protect against tiny numerical overshoots
    return math.acos(c) - (l * h) / 2.0


def solve_h(k: int, l: int, *, interval: Tuple[float, float] | None = None, steps: int = 4000) -> List[float]:
    """Find all roots of :func:`f_of_h` on ``(0, 2π/k)``.

    The algorithm samples the interval uniformly, detects sign changes and
    refines each bracket with a bisection method.

    Parameters
    ----------
    k, l:
        Positive integer parameters of the construction.
    interval:
        Optional custom interval ``(lo, hi)``.  If omitted the default
        ``(1e‑4, 2π/k)`` is used.  ``lo`` must be ``> 0`` and ``hi`` must be ``> lo``.
    steps:
        Number of uniform samples used for the initial sign‑change scan.

    Returns
    -------
    list[float]
        Sorted list of root approximations.
    """
    if k <= 0 or l <= 0:
        raise ValueError("k and l must be positive integers")
    lo_default = 1e-4
    hi_default = 2.0 * math.pi / k
    lo, hi = interval if interval is not None else (lo_default, hi_default)
    if not (0 < lo < hi):
        raise ValueError("interval must satisfy 0 < lo < hi")
    if steps <= 0:
        raise ValueError("steps must be a positive integer")

    roots: List[float] = []
    prev_x = lo
    prev_v = f_of_h(prev_x, k, l)
    for i in range(1, steps + 1):
        x = lo + (hi - lo) * i / steps
        v = f_of_h(x, k, l)
        if prev_v * v < 0:  # sign change detected
            a, b = prev_x, x
            # Bisection refinement
            for _ in range(_MAX_ITER_BISECT):
                m = (a + b) / 2.0
                fm = f_of_h(m, k, l)
                if abs(fm) < _TOL_BISECT:
                    a, b = m, m
                    break
                if f_of_h(a, k, l) * fm <= 0:
                    b = m
                else:
                    a = m
                if b - a < _TOL_BISECT:
                    break
            roots.append((a + b) / 2.0)
        prev_x, prev_v = x, v
    roots.sort()
    return roots


def build(h: float, k: int, l: int, n_out: int, n_in: int) -> List[Tuple[float, float]]:
    """Construct the point set for a given configuration.

    Parameters
    ----------
    h:
        Base angular step (radians).  Must be positive.
    k, l:
        Positive integer parameters as described in :func:`f_of_h`.
    n_out, n_in:
        Number of points on the outer and inner circles respectively.  Both must
        be at least ``3`` to form a polygon.

    Returns
    -------
    list[tuple[float, float]]
        Points ordered by polar angle (counter‑clockwise).
    """
    if h <= 0:
        raise ValueError("h must be positive")
    if k <= 0 or l <= 0:
        raise ValueError("k and l must be positive integers")
    if n_out < 3 or n_in < 3:
        raise ValueError("n_out and n_in must be at least 3")

    sin_kh_half = math.sin(k * h / 2)
    sin_h_half = math.sin(h / 2)
    if sin_kh_half == 0 or sin_h_half == 0:
        raise ValueError("Invalid h leading to division by zero in radius computation")

    R = 1.0 / (2.0 * sin_kh_half)
    r = 1.0 / (2.0 * sin_h_half)
    alpha = l * h / 2.0

    # Outer circle points – spaced by ``k·h``.
    outer = [
        (R * math.cos(j * k * h), R * math.sin(j * k * h))
        for j in range(n_out)
    ]
    # Inner circle points – start at offset ``alpha``.
    inner = [
        (r * math.cos(alpha + i * h), r * math.sin(alpha + i * h))
        for i in range(n_in)
    ]
    pts = outer + inner
    # Sort by polar angle to obtain a proper polygon ordering.
    pts.sort(key=lambda p: math.atan2(p[1], p[0]))
    return pts


def _search_best() -> Tuple[int, Tuple[int, int, float, int, int, int] | None]:
    """Internal helper used by :func:`main` to locate the configuration with the
    maximal number of unit distances.

    Returns
    -------
    tuple[int, tuple|None]
        ``(best_u, best_params)`` where ``best_u`` is the maximal unit‑pair count
        and ``best_params`` is ``(k, l, h, n_out, n_in, n)`` for the corresponding
        configuration, or ``None`` if no configuration satisfies the convexity
        test.
    """
    best_u = 0
    best_params: Tuple[int, int, float, int, int, int] | None = None
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
                        if u > best_u:
                            best_u = u
                            best_params = (k, l, round(h, 6), n_out, n_in, n)
    return best_u, best_params


def main() -> None:
    """Entry point for the command‑line interface.

    The function prints the best configuration discovered by exhaustive search
    over a modest parameter range.  It is deliberately lightweight – heavy
    computation should be performed in a dedicated script or notebook.
    """
    best_u, best_params = _search_best()
    print(
        "best unit count found by grid alignment:",
        best_u,
        "params (k, l, h, n_out, n_in, n):",
        best_params,
    )
    if best_params:
        k, l, h, n_out, n_in, n = best_params
        pts = build(h, k, l, n_out, n_in)
        unit_cnt = len(unit_pairs_float(pts, tol=1e-6))
        print(
            "  n =",
            n,
            " u =",
            unit_cnt,
            " 2n-7 =",
            2 * n - 7,
            " u/n =",
            unit_cnt / n,
        )
        print("  degrees:", degrees(pts, tol=1e-6))


if __name__ == "__main__":
    main()
