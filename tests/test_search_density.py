"""Tests for numerical search density."""

import io
import random
import sys
import numpy as np

from src.search_density import soft_score, convexity_penalty, init_convex, anneal, run


def test_soft_score():
    """Test soft score function for valid point configurations."""
    xy = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0]])
    score = soft_score(xy, sigma=0.1)
    assert isinstance(score, float)
    assert score > 0


def test_convexity_penalty_convex():
    """Test convexity penalty is zero for convex shapes."""
    xy = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0]])
    pen = convexity_penalty(xy)
    assert pen == 0.0


def test_convexity_penalty_non_convex():
    """Test convexity penalty is non-zero for non-convex shapes."""
    # A self-intersecting polygon
    xy = np.array([[1.0, 0.0], [0.0, 0.1], [0.1, 0.0], [-1.0, 0.0], [0.0, -1.0]])
    pen = convexity_penalty(xy)
    assert pen > 0.0


def test_init_convex():
    """Test the initialization logic creates convex shapes."""
    rng = random.Random(42)
    xy = init_convex(6, rng)
    assert xy.shape == (6, 2)
    assert convexity_penalty(xy) == 0.0


def test_anneal():
    """Test the anneal optimization loop."""
    xy, v = anneal(6, seed=42)
    assert xy.shape == (6, 2)
    assert convexity_penalty(xy) == 0.0
    assert v > 0


def test_init_convex_fallback():
    """Test init_convex successfully returns an array.
    Using a specific seed to hit the fallback circle generation."""
    # Seed chosen so that it falls back to the jittered circle logic
    # if it doesn't immediately find a lens configuration.
    rng = random.Random(999)
    xy = init_convex(6, rng)
    assert xy.shape == (6, 2)


def test_run():
    """Test run executes with minimal params."""
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    try:
        run([6], 1)
        out = new_stdout.getvalue()
    finally:
        sys.stdout = old_stdout

    assert "best u(P)" in out
    assert "convex" in out

def test_init_convex_exhausts_loop(monkeypatch):
    """Test init_convex loop exhaustion by forcing is_strictly_convex_float to return False."""
    from src import search_density
    monkeypatch.setattr(search_density, "is_strictly_convex_float", lambda xy: False)
    rng = random.Random(42)
    xy = init_convex(6, rng)
    assert xy.shape == (6, 2)

def test_run_main_module():
    import runpy
    import io
    import sys
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    try:
        runpy.run_module("src.search_density", run_name="__main__")
        out = new_stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    assert "best u(P)" in out


def test_run_best_xy_none(monkeypatch):
    """Test run logic where best_xy is None initially."""
    from src import search_density
    original_anneal = search_density.anneal
    def mock_anneal(n, seed):
        # We need to make sure v <= best (which is 0 initially).
        # We can mock unit_pairs_float to return an empty list so v=0
        return original_anneal(n, seed)[0], 0
    monkeypatch.setattr(search_density, "anneal", mock_anneal)
    monkeypatch.setattr(search_density, "unit_pairs_float", lambda xy, tol=1e-6: [])

    import io
    import sys
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    try:
        run([6], 1)
        out = new_stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    assert "best u(P)" in out
