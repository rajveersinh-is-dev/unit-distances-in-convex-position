"""Exact-arithmetic utilities for the study of unit distances in convex position.

All geometry is done with `fractions.Fraction` (exact rational arithmetic), so
convexity tests, distance comparisons and unit-distance tests are exact and
carry no floating-point error.  A configuration is therefore *certified* when
`is_strictly_convex` returns True and `unit_pairs` enumerates exactly the claimed
unit distances: the certificate is reproducible by anyone re-running this module.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from typing import List, Sequence, Tuple


Point = Tuple[F, F]


def sub(p: Point, q: Point) -> Point:
    """Sub.
    
    Args:
        p:
        q:
    
    Returns:
        tuple: Result of type tuple
    
    """
    return (p[0] - q[0], p[1] - q[1])


def cross(o: Point, a: Point, b: Point) -> F:
    """(a - o) x (b - o) -- signed twice the area of triangle o,a,b."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def dist2(p: Point, q: Point) -> F:
    """Dist2.
    
    Args:
        p:
        q:
    
    Returns:
        The computed result
    
    """
    d = sub(p, q)
    return d[0] * d[0] + d[1] * d[1]


def is_strictly_convex(points: Sequence[Point]) -> bool:
    """True iff `points`, listed in order, are the vertices of a strictly convex
    polygon (positive orientation, no three collinear)."""
    n = len(points)
    if n < 3:
        return False
    for i in range(n):
        o = points[i]
        a = points[(i + 1) % n]
        for j in range(2, n):
            b = points[(i + j) % n]
            if cross(o, a, b) <= 0:
                return False
    return True


def unit_pairs(points: Sequence[Point]) -> List[Tuple[int, int]]:
    """All index pairs {i, j} with dist2(points[i], points[j]) == 1 (exactly)."""
    out = []
    for i, j in combinations(range(len(points)), 2):
        if dist2(points[i], points[j]) == 1:
            out.append((i, j))
    return out


def is_strictly_convex_float(points: Sequence[Point], tol: float = 1e-9) -> bool:
    """Floating-point convexity test used only by the numerical search."""
    n = len(points)
    if n < 3:
        return False
    for i in range(n):
        o = points[i]
        a = points[(i + 1) % n]
        for j in range(2, n):
            b = points[(i + j) % n]
            cr = ((a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]))
            if float(cr) <= tol:
                return False
    return True


def unit_pairs_float(points: Sequence[Point], tol: float = 1e-7) -> List[Tuple[int, int]]:
    """Floating-point unit pairs with |d - 1| < tol (numerical search only)."""
    out = []
    for i, j in combinations(range(len(points)), 2):
        if abs(float((points[i][0] - points[j][0]) ** 2)
               + float((points[i][1] - points[j][1]) ** 2) - 1.0) < tol:
            out.append((i, j))
    return out


def degrees(points: Sequence[Point], tol: float = 1e-7) -> List[int]:
    """Unit-distance degree of every vertex."""
    deg = [0] * len(points)
    for i, j in unit_pairs_float(points, tol):
        deg[i] += 1
        deg[j] += 1
    return deg


def segments_cross(p: Point, q: Point, r: Point, s: Point) -> bool:
    """True iff the segments pq and rs properly cross in their interiors."""
    d1 = cross(p, q, r)
    d2 = cross(p, q, s)
    d3 = cross(r, s, p)
    d4 = cross(r, s, q)
    return d1 * d2 < 0 and d3 * d4 < 0


def unit_graph(points: Sequence[Point]):
    """Adjacency lists of the unit-distance graph."""
    n = len(points)
    adj = [set() for _ in range(n)]
    for i, j in unit_pairs(points):
        adj[i].add(j)
        adj[j].add(i)
    return adj


def report(points: Sequence[Point], label: str = "") -> str:
    """Report.
    
    Args:
        points (list):
        label (str):
    
    Returns:
        The computed result
    
    """
    lines = []
    if label:
        lines.append(label)
    lines.append(f"  n = {len(points)}")
    lines.append(f"  strictly convex: {is_strictly_convex(points)}")
    up = unit_pairs(points)
    lines.append(f"  unit distances: {len(up)}")
    lines.append(f"  unit-degree sequence: {degrees(points)}")
    lines.append(f"  unit pairs (index i<j): {up}")
    return "\n".join(lines)
