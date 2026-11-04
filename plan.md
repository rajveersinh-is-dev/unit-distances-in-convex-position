1. **Fix Pylint warnings in test files**: Move imports to the top level, add missing docstrings, and remove unused variables/reimports in `test_aligned_lens.py`, `test_claims.py`, and `test_search_density.py`.
2. **Increase coverage in `src/aligned_lens.py`**: Add tests for the `ValueError` exception paths in `f_of_h`, `solve_h`, and `build` (e.g., `sin(h/2) == 0`, `k <= 0`, `interval` checks).
3. **Increase coverage in `src/search_density.py`**: Add tests to cover lines for the fallback generation loop (by mocking `is_strictly_convex_float`) and the `best_xy is None` logic in `run`.
4. **Improve coverage in `tests/test_claims.py`**:
   - Add a test for `random_convex` to ensure it generates valid strictly convex polygons.
   - Test `unit_circle_family` with `n > 2 * k` to cover the extra points logic.
   - Refactor the verification part of `test_lemma5_neighbourhood_structure` into a helper function so that invalid graphs can be tested, achieving branch coverage for the falsification logic.
   - Ensure the `check` function is tested by intentionally triggering and catching a failure.
5. **Complete pre commit steps**: Ensure proper testing, verification, review, and reflection are done by running all checks (`pytest`, `flake8`, `pylint`, and `coverage`).
6. **Submit**: Once all tests pass and coverage reaches ~100%, submit the final code and update the baseline report.
