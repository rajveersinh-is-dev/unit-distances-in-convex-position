# Changelog

All entries describe work that was actually performed.  Commits correspond to the
milestones below.

## [2026-10-13]

### research
- Candidate pool surveyed across eight branches (subset-sum problems, sum-free sets,
  Vizing's conjecture, Seymour's second neighbourhood, χ-boundedness, thrackle,
  Barnette, nowhere-zero flows, Erdős–Moser unit distances) and documented with the
  reason each non-selected candidate was rejected, including the ones that turned out
  to be already solved in 2025.
- Literature for the target problem verified against the live arXiv API and publisher
  pages: Erdős–Moser 1959, Edelsbrunner–Hajnal 1991, Füredi 1990, Brass–Pach 2001,
  Aggarwal 2015 (read in full), Fishburn–Reeds 1992 (located via Aggarwal), Altman
  1963/1972, Morić–Pritchard 2011.
- Novelty classification performed, including the withdrawal of the
  `K_{2,2}`-free-cut lemma (it is `S₂` of Fishburn–Reeds 1992).

### mathematics
- Three local facts proved: common neighbours ≤ 2, half-plane/semicircle +
  angular monotonicity, the 60° lemma.
- **Neighbourhood theorem:** `G[N(v)]` is a disjoint union of paths of at most three
  vertices; consequences for unit triangles (`≤ 4u/9` unit triangles).
- **Bridge theorem:** `U_c(n) = O(n)` ⟺ bounded minimum unit-degree ⟺ bounded
  degeneracy of `{G(P)}`; this reframes Erdős–Moser 1959 as a local question and shows
  that any constant improvement over `2 log₂ n + 8` is genuine progress.
- **Crossing construction:** for every `k`, convex `2k`-gons with `k` pairwise crossing
  unit diagonals, plus the limitation corollary excluding all bounded-order
  quasi-planarity approaches.
- **Round/algebraic sets:** `u(P) ≤ kdn` (so `u ≤ 2n` for points on a parabola or
  ellipse).
- Recorded honestly: the conjecture is not solved, Erdős–Fishburn is not solved,
  `n log₂ n + 4n` was not improved, and `δ(G) ≤ 3` remains unresolved.

### computation
- Exact rational-arithmetic library (`src/convex_geometry.py`) and three exact
  crossing certificates for `k = 2, 3, 4` (`src/constructions.py`).
- Test suite `tests/test_claims.py` covering every theorem instance that admits a
  check; runs clean.
- Two searches for convex density `≥ 2` (annealing over convex `n`-gons; grid-aligned
  two-circle lens).  Both negative; both documented as inconclusive rather than as
  evidence.

### paper
- `paper/main.tex` written and compiled with tectonic (77 KiB PDF).
