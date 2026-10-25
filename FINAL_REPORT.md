# Improvement Report: Exact Strict Convexity Verification

## A. Repository and baseline
- Repository: unit-distances-in-convex-position
- Baseline branch: default
- Scope examined: Mathematical definitions, specifically strict convexity checking.

## B. Improvements implemented
- **Problem discovered:** The `is_strictly_convex` functions (both exact and float variants in `src/convex_geometry.py`) and equivalent inline convexity checks in `src/search_density.py` and `tests/test_claims.py` only checked whether consecutive points make a left turn. This is insufficient to guarantee strict convexity, as a self-intersecting polygon (such as a pentagram with vertices ordered by angle) can have a strictly positive cross product for all adjacent triples, giving a false positive for convexity.
- **Root cause:** The standard test for strict convexity on an ordered set of vertices checks every consecutive triple `(p_i, p_{i+1}, p_{i+2})`. However, this is only equivalent to strict convexity if the polygon is known to be simple (non-self-intersecting). Since points generated in random routines and numeric search weren't guaranteed to form simple polygons without intersection, they might return `True` for some self-intersecting configurations.
- **Solution implemented:** Updated the strict convexity checks to verify that for every edge `(p_i, p_{i+1})`, all remaining vertices `p_{i+j}` lie strictly to the left of the directed line segment.
- **Files or components affected:**
  - `src/convex_geometry.py` (`is_strictly_convex` and `is_strictly_convex_float`)
  - `src/search_density.py` (`convexity_penalty`)
  - `tests/test_claims.py` (inline convexity checks in `random_convex`, `test_theorem5_circles`, and `test_theorem3_crossing`)
- **Expected and demonstrated benefit:** Correctness of mathematical certificates. The codebase now explicitly enforces that the generated point sets form simple strictly convex polygons and not self-intersecting ones.

## C. Verification results
| Check | Outcome | Output/Evidence | Limitation |
|---|---|---|---|
| `pytest tests/` | PASS | `6 passed in 0.04s` | |
| `python -m src.aligned_lens` | PASS | Successfully finds best unit count (9 pts, 7 unit pairs) | |
| `python -m src.constructions` | PASS | Exact rational certificates printed successfully | |
| `python -m src.search_density` | PASS | Numeric search verifies convex sets | |
| Custom Pentagram test | PASS | `is_strictly_convex` now returns `False` for self-intersecting pentagram, where it previously returned `True` | |

## D. Measurable impact
Tests pass completely with the mathematically rigorous convexity checking. `test_claims.py` verifies 100% correctly, avoiding mathematical falsehoods for self-intersecting polygons with winding number > 1.

## E. Remaining risks
- Since the `search_density` numeric solver tests a larger number of configurations, the `O(n^2)` convexity check is slower than the previous `O(n)` check. However, for `n <= 15`, this does not have a measurable impact.

## F. Next-run priorities
1. Replace random numerical searches for bounds with structured constrained optimization to ensure tighter convergence.
2. Expand mathematical unit tests to test cases that previously had false positives (like the pentagram).
3. Investigate if generating point configurations sequentially by adding points bounded by the intersection of half-planes is more efficient than checking full strict convexity after generation.

## G. Overall verdict
VERIFIED IMPROVEMENT

---

# Audit and Improvement Cycle: Strict Convexity Verification

## A. Repository and baseline
- Repository: unit-distances-in-convex-position
- Baseline branch: default
- Scope examined: Mathematical definitions, specifically strict convexity checking.

## B. Improvements implemented
- **Problem discovered:** The `is_strictly_convex` functions (both exact and float variants in `src/convex_geometry.py`) and equivalent inline convexity checks in `src/search_density.py` and `tests/test_claims.py` only checked whether consecutive points make a left turn. This is insufficient to guarantee strict convexity, as a self-intersecting polygon (such as a pentagram with vertices ordered by angle) can have a strictly positive cross product for all adjacent triples, giving a false positive for convexity.
- **Root cause:** The standard test for strict convexity on an ordered set of vertices checks every consecutive triple `(p_i, p_{i+1}, p_{i+2})`. However, this is only equivalent to strict convexity if the polygon is known to be simple (non-self-intersecting). Since points generated in random routines and numeric search weren't guaranteed to form simple polygons without intersection, they might return `True` for some self-intersecting configurations.
- **Solution implemented:** Updated the strict convexity checks to verify that for every edge `(p_i, p_{i+1})`, all remaining vertices `p_{i+j}` lie strictly to the left of the directed line segment.
- **Files or components affected:**
  - `src/convex_geometry.py` (`is_strictly_convex` and `is_strictly_convex_float`)
  - `src/search_density.py` (`convexity_penalty`)
  - `tests/test_claims.py` (inline convexity checks in `random_convex`, `test_theorem5_circles`, and `test_theorem3_crossing`)
- **Expected and demonstrated benefit:** Correctness of mathematical certificates. The codebase now explicitly enforces that the generated point sets form simple strictly convex polygons and not self-intersecting ones.

## C. Verification results
| Check | Outcome | Output/Evidence | Limitation |
|---|---|---|---|
| `pytest tests/` | PASS | `6 passed in 0.04s` | |
| `python -m src.aligned_lens` | PASS | Successfully finds best unit count (9 pts, 7 unit pairs) | |
| `python -m src.constructions` | PASS | Exact rational certificates printed successfully | |
| `python -m src.search_density` | PASS | Numeric search verifies convex sets | |

## D. Measurable impact
Tests pass completely with the mathematically rigorous convexity checking. `test_claims.py` verifies 100% correctly, avoiding mathematical falsehoods for self-intersecting polygons with winding number > 1.

## E. Remaining risks
- Since the `search_density` numeric solver tests a larger number of configurations, the `O(n^2)` convexity check is slower than the previous `O(n)` check. However, for `n <= 15`, this does not have a measurable impact.

## F. Next-run priorities
1. Replace random numerical searches for bounds with structured constrained optimization to ensure tighter convergence.
2. Expand mathematical unit tests to test cases that previously had false positives (like the pentagram).
3. Investigate if generating point configurations sequentially by adding points bounded by the intersection of half-planes is more efficient than checking full strict convexity after generation.

## G. Overall verdict
VERIFIED IMPROVEMENT
