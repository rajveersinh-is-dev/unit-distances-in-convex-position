"""Tests for grid-aligned two-circle lens constructions."""

import io
import math
import sys
import pytest

from src.aligned_lens import f_of_h, solve_h, build, _evaluate_configuration, _search_best, main


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
        assert angles[i] >= angles[i - 1] - 1e-9


def test_evaluate_configuration():
    """Test _evaluate_configuration."""
    # Evaluate a configuration that we know fails convexity or produces some unit distances
    best_u, _ = _evaluate_configuration(0.698132, 8, 2, 0)
    assert best_u >= 0


def test_search_best():
    """Test that _search_best performs the search and finds a valid best configuration."""
    best_u, best_params = _search_best()
    assert best_u > 0
    assert best_params is not None
    k, l, h, n_out, n_in, n = best_params
    assert k > 0
    assert l > 0
    assert h > 0
    assert n_out >= 3
    assert n_in >= 3
    assert n == n_out + n_in


def test_main():
    """Test the main entry point without mocking to verify real execution."""
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    try:
        main()
        out = new_stdout.getvalue()
    finally:
        sys.stdout = old_stdout

    assert "best unit count" in out
    assert "params (k, l, h, n_out, n_in, n)" in out
    assert "degrees:" in out

def test_solve_h_invalid_interval():
    with pytest.raises(ValueError, match="interval must satisfy 0 < lo < hi"):
        solve_h(8, 2, interval=(1.0, 0.5))

def test_solve_h_invalid_steps():
    with pytest.raises(ValueError, match="steps must be a positive integer"):
        solve_h(8, 2, steps=0)

def test_f_of_h_invalid_k_l():
    with pytest.raises(ValueError, match="k and l must be positive integers"):
        f_of_h(0.1, -1, 2)
    with pytest.raises(ValueError, match="k and l must be positive integers"):
        f_of_h(0.1, 1, -2)

def test_build_invalid_k_l():
    with pytest.raises(ValueError, match="k and l must be positive integers"):
        build(0.1, -1, 2, 3, 3)



def test_build_invalid_h_zero_division(monkeypatch):
    import src.aligned_lens
    class MockMath:
        def __init__(self):
            import math
            self.math = math
        def __getattr__(self, name):
            return getattr(self.math, name)
        def sin(self, x):
            return 0.0

    monkeypatch.setattr(src.aligned_lens, "math", MockMath())
    with pytest.raises(ValueError, match="Invalid h leading to division by zero in radius computation"):
        build(2 * 3.14, 1, 2, 3, 3)

def test_f_of_h_invalid_h_zero_division(monkeypatch):
    import src.aligned_lens
    class MockMath:
        def __init__(self):
            import math
            self.math = math
        def __getattr__(self, name):
            return getattr(self.math, name)
        def sin(self, x):
            return 0.0

    monkeypatch.setattr(src.aligned_lens, "math", MockMath())
    with pytest.raises(ValueError, match=r"sin\(k·h/2\) and sin\(h/2\) must be non‑zero"):
        f_of_h(2 * 3.14, 1, 2)

def test_aligned_lens_main_module():
    import runpy
    import io
    import sys
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    try:
        runpy.run_module("src.aligned_lens", run_name="__main__")
        out = new_stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    assert "best unit count found by grid alignment" in out
