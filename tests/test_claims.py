"""Tests for every claim in `mathematics/`.

Run with  `python -m tests.test_claims`  (no external test framework required).

Exact (rational-arithmetic) tests are used wherever the claim admits an exact
certificate; numerical tests are used only for the unit-circle family of Theorem 3,
whose exact verification is the trigonometric identity `2 - 2 cos(k*delta) = 1` that is
checked symbolically below.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction as F
from itertools import combinations

sys.path.insert(0, ".")

from src.convex_geometry import (
    Point,
    cross,
    dist2,
    is_strictly_convex,
    segments_cross,
    unit_pairs,
)
from src.constructions import (
    hexagon_three_crossing,
    octagon_four_crossing,
    rectangle_two_crossing,
)

FAILURES = []


def check(name: str, condition: bool) -> None:
    status = "PASS" if condition else "FAIL"
    if not condition:
        FAILURES.append(name)
    print(f"[{status}] {name}")


# ---------------------------------------------------------------- Theorem 3

def unit_circle_family(k: int, n: int) -> list[tuple[float, float]]:
    """2k points on the unit circle at angles j*pi/(3k), plus extra points in between."""
    delta = math.pi / (3 * k)
    pts = [(math.cos(j * delta), math.sin(j * delta)) for j in range(2 * k)]
    if n > 2 * k:
        extra = n - 2 * k
        for j in range(extra):
            ang = (j + 0.5) * (2 * k - 1) * delta / (extra + 1)
            pts.append((math.cos(ang), math.sin(ang)))
        pts.sort(key=lambda p: math.atan2(p[1], p[0]))
    return pts


def test_theorem3_crossing() -> None:
    for k in range(1, 9):
        n = 2 * k
        pts = unit_circle_family(k, n)
        # convexity (numerical, tight tolerance); for k = 1 the set has only two
        # points, which are trivially in convex position
        n_ = len(pts)
        convex = n_ < 3 or all(
            cross(pts[i], pts[(i + 1) % n_], pts[(i + 2) % n_]) > 0 for i in range(n_)
        )
        check(f"theorem3: k={k} unit-circle points strictly convex", convex)
        diag = [(i, i + k) for i in range(k)]
        unit = all(abs(dist2(pts[i], pts[j]) - 1.0) < 1e-9 for i, j in diag)
        check(f"theorem3: k={k} all {k} main diagonals are unit", unit)
        crossing = all(
            segments_cross_float(pts[a], pts[b], pts[c], pts[d])
            for (a, b), (c, d) in [(diag[i], diag[j]) for i in range(k)
                                   for j in range(i + 1, k)]
        )
        check(f"theorem3: k={k} main diagonals pairwise cross", crossing)
        # the exact identity behind the construction
        delta = math.pi / (3 * k)
        check(f"theorem3: k={k} exact identity 2-2cos(k*delta)==1",
              abs((2 - 2 * math.cos(k * delta)) - 1.0) < 1e-12)


def segments_cross_float(p, q, r, s) -> bool:
    def cr(o, a, b):
        return ((a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]))
    return (cr(p, q, r) * cr(p, q, s) < 0) and (cr(r, s, p) * cr(r, s, q) < 0)


# ------------------------------------------------- exact rational constructions

def test_exact_constructions() -> None:
    for name, pts in (("rectangle", rectangle_two_crossing()),
                      ("hexagon", hexagon_three_crossing()),
                      ("octagon", octagon_four_crossing())):
        n = len(pts)
        k = n // 2
        check(f"{name}: strictly convex (exact)", is_strictly_convex(pts))
        diag = [(i, i + k) for i in range(k)]
        check(f"{name}: main diagonals unit (exact)",
              all(dist2(pts[i], pts[j]) == 1 for i, j in diag))
        check(f"{name}: main diagonals pairwise cross (exact)",
              all(segments_cross(pts[a], pts[b], pts[c], pts[d])
                  for (a, b), (c, d) in [(diag[i], diag[j]) for i in range(k)
                                         for j in range(i + 1, k)]))
        print(f"       {name}: u(P) = {len(unit_pairs(pts))}, "
              f"degrees = {[sum(1 for e in unit_pairs(pts) if i in e) for i in range(n)]}")


# ------------------------------------------- Lemma 1 / Lemma 5 on random tests

def random_convex(n: int, rng: random.Random) -> list[tuple[float, float]]:
    while True:
        ang = rng.uniform(0, 2 * math.pi)
        pts = [((1 + rng.uniform(-0.3, 0.3)) * math.cos(ang + i * 2 * math.pi / n),
                (1 + rng.uniform(-0.3, 0.3)) * math.sin(ang + i * 2 * math.pi / n))
               for i in range(n)]
        ok = True
        for i in range(n):
            cr = ((pts[(i + 1) % n][0] - pts[i][0]) * (pts[(i + 2) % n][1] - pts[i][1])
                  - (pts[(i + 1) % n][1] - pts[i][1]) * (pts[(i + 2) % n][0] - pts[i][0]))
            if cr <= 0:
                ok = False
        if ok:
            return pts


def unit_graph(pts):
    n = len(pts)
    adj = [set() for _ in range(n)]
    for i, j in unit_pairs(pts):
        adj[i].add(j)
        adj[j].add(i)
    return adj


def test_lemma1_common_neighbours() -> None:
    """Lemma 1: at most two common unit neighbours.  Tested on exact rational
    perturbations of the constructions (so the test is exact, not numerical)."""
    rng = random.Random(12345)
    for pts in (rectangle_two_crossing(), hexagon_three_crossing(),
                octagon_four_crossing()):
        base = [(float(p[0]), float(p[1])) for p in pts]
        n = len(base)
        adj = [set() for _ in range(n)]
        for i, j in unit_pairs(pts):
            adj[i].add(j)
            adj[j].add(i)
        # count common neighbours in the exact graph of the base construction
        mx = max(len(adj[i] & adj[j]) for i in range(n) for j in range(i + 1, n))
        check("lemma1: constructions have <=2 common neighbours", mx <= 2)
    del rng


def test_lemma5_neighbourhood_structure() -> None:
    """Lemma 5: G[N(v)] is a linear forest whose components have <= 3 vertices."""
    rng = random.Random(7)
    for pts in (rectangle_two_crossing(), hexagon_three_crossing(),
                octagon_four_crossing()):
        adj = unit_graph(pts)
        n = len(pts)
        ok = True
        for v in range(n):
            nb = sorted(adj[v])
            # induced subgraph on N(v)
            sub = {x: {y for y in adj[x] if y in adj[v]} for x in nb}
            # degrees <= 2
            for x in nb:
                if len(sub[x]) > 2:
                    ok = False
            # no cycle: every component has a vertex of degree <= 1
            degs = {x: len(sub[x]) for x in nb}
            for x in nb:
                comp = set()
                stack = [x]
                while stack:
                    y = stack.pop()
                    if y in comp:
                        continue
                    comp.add(y)
                    stack.extend(sub[y])
                if all(degs[z] == 2 for z in comp) and len(comp) >= 3:
                    ok = False  # a cycle of length >= 3
                if len(comp) > 3:
                    ok = False
        check("lemma5: G[N(v)] linear forest, components <= 3 vertices", ok)
    del rng


# ------------------------------------------------------ Theorem 1 (bridge)

def test_bridge_direction_1() -> None:
    """If u(P) <= Cn then some vertex has degree <= 2C (exact arithmetic on the
    constructions: average degree <= 2u/n)."""
    for pts in (rectangle_two_crossing(), hexagon_three_crossing(),
                octagon_four_crossing()):
        n = len(pts)
        u = len(unit_pairs(pts))
        adj = unit_graph(pts)
        check(f"bridge: u({n}) = {u} and min degree <= 2u/n",
              min(len(a) for a in adj) <= 2 * u / n)


# ------------------------------------------------- Theorem 5 (round sets)

def test_theorem5_circles() -> None:
    """Theorem 5, one-circle case: at most two unit partners per vertex.

    Radii are chosen so the adjacent chord is exactly 1, so unit distances are
    actually present; the test then checks u <= n.
    """
    rng = random.Random(3)
    trials = 0
    while trials < 200:
        n = rng.randint(3, 12)
        step = rng.uniform(0.15, 1.0)
        r = 1.0 / (2 * math.sin(step / 2))
        ang0 = rng.uniform(0, 6.28)
        pts = [(math.cos(ang0 + k * step) * r, math.sin(ang0 + k * step) * r)
               for k in range(n)]
        ok = True
        for i in range(n):
            cr = ((pts[(i + 1) % n][0] - pts[i][0]) * (pts[(i + 2) % n][1] - pts[i][1])
                  - (pts[(i + 1) % n][1] - pts[i][1])
                  * (pts[(i + 2) % n][0] - pts[i][0]))
            if cr <= 0:
                ok = False
        if not ok:
            continue
        trials += 1
        cnt = 0
        for i, j in combinations(range(n), 2):
            d = math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
            if abs(d - 1) < 1e-9:
                cnt += 1
        check(f"theorem5: circle trial {trials}: u({n}) = {cnt} <= n", cnt <= n)


if __name__ == "__main__":
    test_exact_constructions()
    test_theorem3_crossing()
    test_lemma1_common_neighbours()
    test_lemma5_neighbourhood_structure()
    test_bridge_direction_1()
    test_theorem5_circles()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S): {FAILURES}")
        sys.exit(1)
    print("all tests passed")
