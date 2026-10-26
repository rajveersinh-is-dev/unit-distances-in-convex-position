import pytest
from fractions import Fraction as F
from src.convex_geometry import is_strictly_convex, is_strictly_convex_float

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
