"""Tests for numerical search density."""

import random
import numpy as np

from src.search_density import soft_score, convexity_penalty, init_convex, anneal


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
