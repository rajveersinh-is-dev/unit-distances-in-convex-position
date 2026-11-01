import pytest
import math

from src.aligned_lens import f_of_h, solve_h, build

def test_f_of_h():
    """Test f_of_h raises ValueError on invalid inputs and returns correct values for valid."""
    with pytest.raises(ValueError):
        f_of_h(-1.0, 1, 1)
    with pytest.raises(ValueError):
        f_of_h(0.1, -1, 1)
    with pytest.raises(ValueError):
        f_of_h(0.1, 1, -1)

    # Check that a specific configuration gives expected float result
    # We know that for h near 0.698132, k=8, l=2, f_of_h evaluates to near 0.
    val = f_of_h(0.698132, 8, 2)
    assert abs(val) < 1e-3

def test_solve_h():
    """Test solve_h returns valid roots."""
    roots = solve_h(8, 2)
    assert len(roots) > 0
    # The root ~0.698132 should be among them
    assert any(abs(r - 0.698132) < 1e-4 for r in roots)

    with pytest.raises(ValueError):
        solve_h(-1, 2)

    with pytest.raises(ValueError):
        solve_h(8, 2, interval=(1.0, 0.5))

def test_build():
    """Test build creates correctly sized lists of points."""
    with pytest.raises(ValueError):
        build(-0.1, 8, 2, 3, 6)
    with pytest.raises(ValueError):
        build(0.1, 8, 2, 2, 6)
    with pytest.raises(ValueError):
        build(0.1, 8, 2, 3, 2)

    pts = build(0.698132, 8, 2, 3, 6)
    assert len(pts) == 9

    # Points should be ordered counter-clockwise by polar angle
    angles = [math.atan2(p[1], p[0]) for p in pts]
    for i in range(1, len(angles)):
        assert angles[i] >= angles[i-1] - 1e-9
