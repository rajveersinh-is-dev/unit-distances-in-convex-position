"""Convexity tests."""

from fractions import Fraction as F
from src.convex_geometry import is_strictly_convex, is_strictly_convex_float, degrees, report


def test_pentagram_is_not_strictly_convex():
    """A self-intersecting pentagram should not be strictly convex,
    even though adjacent edges make left turns."""
    pts = [
        (F(0), F(10)),
        (F(-10), F(-5)),
        (F(10), F(5)),
        (F(-10), F(5)),
        (F(10), F(-5)),
    ]
    assert not is_strictly_convex(pts)


def test_pentagram_float_is_not_strictly_convex():
    """A self-intersecting pentagram should not be strictly convex (float)."""
    pts = [
        (0.0, 10.0),
        (-10.0, -5.0),
        (10.0, 5.0),
        (-10.0, 5.0),
        (10.0, -5.0),
    ]
    assert not is_strictly_convex_float(pts)


def test_collinear_is_not_strictly_convex():
    """Three collinear points should not be strictly convex."""
    pts = [
        (F(0), F(0)),
        (F(1), F(0)),
        (F(2), F(0)),
        (F(1), F(1)),
    ]
    assert not is_strictly_convex(pts)
    assert not is_strictly_convex_float([(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (1.0, 1.0)])


def test_simple_convex():
    """A simple triangle should be strictly convex."""
    pts = [
        (F(0), F(0)),
        (F(1), F(0)),
        (F(0), F(1)),
    ]
    assert is_strictly_convex(pts)
    assert is_strictly_convex_float([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])


def test_edge_cases_n_less_than_3():
    """Convexity tests for n < 3 should return False."""
    assert not is_strictly_convex([])
    assert not is_strictly_convex([(F(0), F(0))])
    assert not is_strictly_convex([(F(0), F(0)), (F(1), F(0))])

    assert not is_strictly_convex_float([])
    assert not is_strictly_convex_float([(0.0, 0.0)])
    assert not is_strictly_convex_float([(0.0, 0.0), (1.0, 0.0)])


def test_degrees_and_report():
    """Test degrees and report with a simple geometry."""
    pts = [
        (F(0), F(0)),
        (F(1), F(0)),
        (F(0), F(1)),
    ]
    deg = degrees(pts)
    assert deg == [2, 1, 1]  # distance between (1,0) and (0,1) is not 1 (it's 2, so sqrt(2))

    rep = report(pts, "triangle")
    assert "triangle" in rep
    assert "n = 3" in rep
    assert "strictly convex: True" in rep
    assert "unit-degree sequence" in rep


def test_is_strictly_convex_non_convex():
    # Provide a non-convex polygon to trigger False return
    pts = [(0.0, 0.0), (2.0, 0.0), (1.0, 1.0), (1.0, 2.0)]
    from src.convex_geometry import is_strictly_convex
    from fractions import Fraction as F
    fpts = [(F(x), F(y)) for x, y in pts]
    assert not is_strictly_convex(fpts)


def test_segments_cross():
    from src.convex_geometry import segments_cross
    from fractions import Fraction as F

    p = (F(0), F(0))
    q = (F(2), F(2))
    r = (F(0), F(2))
    s = (F(2), F(0))

    assert segments_cross(p, q, r, s)
    assert not segments_cross(p, r, q, s)


def test_unit_graph():
    from src.convex_geometry import unit_graph
    from fractions import Fraction as F
    pts = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1))]
    adj = unit_graph(pts)
    assert len(adj) == 3
    assert 1 in adj[0]
    assert 0 in adj[1]
