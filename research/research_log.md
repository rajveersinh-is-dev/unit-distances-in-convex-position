# Research log

A decision-and-discovery record, not a diary.  Dates are all 13 Oct 2026 (single run).

## Selection phase (~60 min)

* Surveyed eight candidate problems across number theory, combinatorics, graph theory,
  geometry and TCS (full table with rejections in `research/problem_selection.md`).
* Confirmed by search that two tempting candidates are already settled: the Erdős
  large-sum-free-subset problem (`S(N) ≥ N/3 + ω(N)`, solved 2025 with
  `S(A) ≥ |A|/3 + c·log log|A|`) and the minimum number of distinct subset sums
  (classical: `C(n+1,2)+1`, current frontier is a stability/inverse theorem).
* Confirmed that the polynomial χ-boundedness of `P5`-free graphs was resolved in
  Dec 2025 and that Seymour's second-neighbourhood conjecture now has 2026 preprints
  treating δ ≤ 7 by CP-SAT: both are moving frontiers where a solo structural attack is
  unlikely to add anything.
* Selected Erdős–Moser (Erdős problem 96) for three reasons: the frontier is a clean
  quantitative gap (`2n−7` vs `n log₂n+4n`); the known machinery is elementary and
  self-contained; and the first hour of direct work produced an original reformulation
  (the bridge theorem) plus several structural lemmas, giving an internal lever.

## Mathematical dead ends (recorded so they are not repeated)

1. **Counting-only degeneration arguments.** `Σ_v C(d_v,2) = Σ_{x≠y}|N(x)∩N(y)| ≤
   2·C(n,2)` is consistent with `δ(G) ≈ 2√n`, so no bounded-degeneracy result can come
   from the common-neighbour lemma alone.  Any constant bound must be geometric.
2. **Quasi-planarity route.** Initially promising: `δ(G) ≤ 3` would give
   `U_c(n) ≤ 3n`.  Looking for a route, I first asked whether the unit-distance graph of
   a convex polygon can contain *many* pairwise crossing edges.  My first attempt was a
   hand-built "two-chain + rotating unit shifts" hexagon/octagon (later verified
   exactly, `src/constructions.py`); while checking it I realised the general case is
   trivial: `2k` equally spaced points on a unit circle have `k` unit main diagonals,
   which pairwise cross.  Hence **no** bounded-order quasi-planarity theorem can apply
   (the limitation corollary).  Route closed — but it became a result.
3. **Cut-matrix strengthening.** The observation that a diagonal split contains no unit
   `K_{2,2}` (no `S₂` submatrix) is *not* new: Aggarwal §1.1 attributes `S₂` to
   Fishburn–Reeds 1992.  It also does not improve Füredi's matrix lemma: in the strip
   argument's regimes the `K_{2,2}`-free (Kővári–Sós–Turán) bound `O(a√b + b)` is
   weaker than Füredi's `a + (a+b)⌊log₂b⌋`.  Withdrawn from the novelty claims.
4. **Concentric-circle alignment.** For two concentric circles each point has at most
   four unit partners, so the density of any two-circle configuration is ≤ 2 with
   endpoint deficits; a three-arc design would need all pairwise angular offsets and
   the same-circle offsets to lie on one common angular grid *and* the three arcs to be
   mutually visible from each other's offset sets.  I could not resolve the resulting
   congruences and abandoned this as a route to density > 2.
5. **Search for `u(P) ≥ 2n`.** Simulated annealing over convex `n`-gons (n = 6…14)
   seeded from both jittered circles and two-arc lenses: best density `u/n ≈ 0.86`.
   The annealer never reaches the published `2n−7`, so the search is not evidence
   either way.  Recorded as inconclusive.

## What remains, precisely

The strongest remaining obstruction is that the bridge theorem reduces Erdős–Moser to
showing `δ(G(P)) ≤ c` for an absolute `c`, and nothing in the local structure (≤ 2
common neighbours, semicircular neighbourhoods, `G[N(v)]` a union of ≤ 3-vertex paths)
currently yields any absolute bound on the minimum degree.
