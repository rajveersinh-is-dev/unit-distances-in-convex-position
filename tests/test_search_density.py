"""Tests for numerical search density."""

import contextlib
import io
import random
import subprocess
import sys
import numpy as np

import src.search_density
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
    new_stdout = io.StringIO()
    with contextlib.redirect_stdout(new_stdout):
        run([6], 1)
    out = new_stdout.getvalue()

    assert "best u(P)" in out
    assert "convex" in out


def test_init_convex_exhausts_loop(monkeypatch):
    """Test init_convex loop exhaustion by forcing is_strictly_convex_float to return False."""
    monkeypatch.setattr(src.search_density, "is_strictly_convex_float", lambda _xy: False)
    rng = random.Random(42)
    xy = init_convex(6, rng)
    assert xy.shape == (6, 2)


def test_run_main_module():
    result = subprocess.run([sys.executable, "-m", "src.search_density"], capture_output=True, text=True, check=True)
    out = result.stdout
    assert "best u(P)" in out


def test_run_best_xy_none(monkeypatch):
    """Test run logic where best_xy is None initially."""
    original_anneal = src.search_density.anneal

    def mock_anneal(n, seed):
        # We need to make sure v <= best (which is 0 initially).
        # We can mock unit_pairs_float to return an empty list so v=0
        return original_anneal(n, seed)[0], 0
    monkeypatch.setattr(src.search_density, "anneal", mock_anneal)
    monkeypatch.setattr(src.search_density, "unit_pairs_float", lambda _xy, tol=1e-6: [])

    new_stdout = io.StringIO()
    with contextlib.redirect_stdout(new_stdout):
        run([6], 1)
    out = new_stdout.getvalue()
    assert "best u(P)" in out
