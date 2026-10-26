"""Exact constructions used in the write-up.

Every construction below returns a list of `Fraction` points together with a
machine-checkable certificate: strict convexity plus the exact unit distances.
Run as a script to print all certificates.
"""

from __future__ import annotations

from fractions import Fraction as F

try:  # allow both `python -m src.constructions` and `python src/constructions.py`
    from src.convex_geometry import (
        Point,
        degrees,
        dist2,
        report,
        segments_cross,
    )
except ImportError:  # pragma: no cover - direct script execution
    from convex_geometry import (
        Point,
        degrees,
        dist2,
        report,
        segments_cross,
    )


def rectangle_two_crossing() -> list[Point]:
    """A 3/5 x 4/5 rectangle: both diagonals have length 1 (rational coordinates).

    The two diagonals are the main diagonals of a convex quadrilateral, so they
    cross in their interiors.
    """
    a, b = F(3, 5), F(4, 5)
    return [
        (F(0), F(0)),
        (a, F(0)),
        (a, b),
        (F(0), b),
    ]


def hexagon_three_crossing() -> list[Point]:
    """Convex hexagon whose three main diagonals all have length 1 (exact).

    The main diagonals of a convex hexagon pairwise cross in their interiors,
    hence the unit-distance graph of a convex point set contains three pairwise
    crossing edges.
    """
    u, v, h = F(3, 5), F(4, 5), F(1, 2)
    p1 = (F(0), F(0))
    p2 = (F(3, 10), -h)
    p3 = (F(7, 10), -h)
    p4 = (F(1), F(0))
    p5 = (p2[0] + u, p2[1] + v)
    p6 = (p3[0] - u, p3[1] + v)
    return [p1, p2, p3, p4, p5, p6]


def octagon_four_crossing() -> list[Point]:
    """Convex octagon whose four main diagonals all have length 1 (exact)."""
    h, H = F(2, 5), F(1, 2)
    u, v = F(3, 5), F(4, 5)
    z1 = (F(0), F(0))
    z2 = (F(3, 10), -h)
    z3 = (F(1, 2), -H)
    z4 = (F(7, 10), -h)
    z5 = (F(1), F(0))
    z6 = (z2[0] + u, z2[1] + v)
    z7 = (z3[0], z3[1] + F(1))
    z8 = (z4[0] - u, z4[1] + v)
    return [z1, z2, z3, z4, z5, z6, z7, z8]


def symmetric_2k_gon(k: int, lower_arc: list[tuple[F, F]], shifts: list[tuple[F, F]]) -> list[Point]:
    """Assemble the symmetric 2k-gon from a lower chain and unit shifts.

    `lower_arc` lists the interior points z_2..z_k of the lower chain (already
    mirror-symmetric, in increasing x order, on or below y = 0), strictly inside
    the strip between z_1 = (0,0) and z_{k+1} = (1,0), so that
    z_1, lower_arc..., z_{k+1} is strictly convex.  `shifts` gives the unit
    vectors v_2..v_k (also mirror symmetric, v_{k+2-i} = (-p_i, q_i)).
    """
    chain = [(F(0), F(0))] + list(lower_arc) + [(F(1), F(0))]
    assert len(chain) == k + 1
    z = list(chain)
    for i in range(2, k + 1):
        p, q = shifts[i - 2]
        z.append((z[i - 1][0] + p, z[i - 1][1] + q))
    return z


def certificate(points: list[Point], name: str) -> None:
    """Certificate.
    
    Args:
        points (list):
        name:
    
    """
    print(report(points, name))
    n = len(points)
    k = n // 2
    diag = [(i, i + k) for i in range(k)]
    print("  main diagonals:", diag)
    print("  all main diagonals unit:", all(dist2(points[i], points[j]) == 1 for i, j in diag))
    crossing = all(
        segments_cross(points[a], points[b], points[c], points[d])
        for (a, b), (c, d) in [(diag[i], diag[j]) for i in range(k) for j in range(i + 1, k)]
    )
    print("  all main diagonals pairwise cross:", crossing)
    print("  degrees:", degrees(points))
    print()


if __name__ == "__main__":
    certificate(rectangle_two_crossing(), "RECTANGLE 3/5 x 4/5  (k = 2)")
    certificate(hexagon_three_crossing(), "HEXAGON  (k = 3)")
    certificate(octagon_four_crossing(), "OCTAGON  (k = 4)")
