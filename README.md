# Unit distances among vertices of a convex polygon — the Erdős–Moser problem

An autonomous, proof-first investigation of the problem posed by Erdős and Moser in
1959 (**Erdős problem 96**):

> For a finite set `P` of `n` points in **strictly convex position** in `ℝ²`, let `u(P)`
> be the number of pairs at distance exactly `1`, and let
> `U_c(n) = max u(P)`.  Is `U_c(n) = O(n)`?

**Status of the problem: OPEN.** The literature stands at

```
   2n − 7  ≤  U_c(n)  ≤  n·log₂ n + 4n
Edelsbrunner–Hajnal 1991      Aggarwal 2015 (Discrete Math. 338, 88–92)
```

and the related conjecture `u(P) ≤ 2n` (Erdős–Fishburn) is also open.

---

## What was actually proved in this repository

| # | Result | Category |
|---|---|---|
| 1 | **Bridge theorem.** `U_c(n) = O(n)` ⟺ some absolute constant `c` bounds the minimum unit-degree of every convex `n`-gon ⟺ the unit-distance graphs of convex point sets have bounded degeneracy. | **PROVED HERE** (elementary, no located prior statement) |
| 2 | **Neighbourhood theorem.** For every vertex `v`, `G[N(v)]` is a disjoint union of paths of at most **three** vertices; its edges join unit-neighbours of `v` exactly `π/3` apart as seen from `v`. Consequently `v` lies in at most `2·d(v)/3` unit triangles. | **PROVED HERE** (elementary, no located prior statement) |
| 3 | **Crossing construction.** For every `k ≥ 1` and every `n ≥ 2k` there is a convex `n`-gon whose unit-distance graph has `k` **pairwise crossing** edges. | **PROVED HERE** (one-line construction; probably folklore) |
| 4 | **Limitation corollary.** No theorem of the form "a topological graph with no `K+1` pairwise crossing edges has `O(n)` edges" can prove `U_c(n) = O(n)` — that whole family of attacks is excluded. | **PROVED HERE** |
| 5 | **Round/algebraic sets.** Points on `k` circles give `u(P) ≤ kn`; points on `k` curves of degree `≤ d` give `u(P) ≤ kdn`. Hence `u ≤ n` for points on a circle and `u ≤ 2n` (Erdős–Fishburn's density) for points on a parabola or ellipse. | PROVED HERE from a classical ingredient (Erdős 1946) |
| 6 | Whether the minimum unit-degree of a convex `n`-gon is bounded by `3` (or even by any absolute constant) — the question Theorem 1 reduces Erdős–Moser to. | **UNRESOLVED** here |

Everything else in this repository (including the computational search) is reported as
what it is: no new lower bound, no counterexample, no improvement of `n log₂ n + 4n`.

### The main theorem (Theorem 1, the bridge)

> Let `G(P)` be the unit-distance graph of a convex point set `P`.  Then `U_c(n) = O(n)`
> if and only if there is an absolute constant `c` such that **every** finite convex
> point set has a vertex incident to at most `c` unit segments.

*Proof.* One direction is induction on `n` after deleting a low-degree vertex (deleting
a vertex preserves convexity); the other is averaging (`avg degree = 2u/n ≤ 2C`).
Full proof: [`mathematics/structural_lemmas.md`, Theorem 10](mathematics/structural_lemmas.md).

**Why it matters:** the 1959 conjecture becomes a *local* statement — "some vertex has
few unit neighbours" — and any improvement over the currently known `2 log₂ n + 8`
(averaging version of Aggarwal's bound) is genuine progress, whether or not the
constant is small.  Concretely: `δ(G) ≤ 4` already gives `U_c(n) ≤ 4n` (settling
Erdős–Moser), Erdős–Fishburn's `u(P) ≤ 2n` would imply `δ(G) ≤ 4`, and `δ(G) ≤ 3` would
give `U_c(n) ≤ 3n`.

### Proof strategy in one paragraph

Three elementary geometric facts carry the paper: (i) two unit circles meet in at most
two points, so any two vertices have at most two common unit neighbours; (ii) a
supporting line at a convex vertex puts all its unit neighbours on an arc of angle
`< π`; (iii) three pairwise-unit points form an equilateral triangle, so any two
*adjacent* unit neighbours of `v` are exactly `π/3` apart as seen from `v`.  Combining
(ii) and (iii) forces `G[N(v)]` to be a union of short paths (Theorem 2), and the
bridge theorem follows by a two-line induction/averaging argument.  The crossing
construction is `2k` equally spaced points on a unit-diameter circle: the `k` main
diagonals are all unit and pairwise cross.

## Repository map

```
mathematics/
  definitions.md          the set-up and the three local facts
  structural_lemmas.md    all lemmas/theorems with complete proofs (Theorems 1–11)
  main_results.md         what is proved, what is not (evidence labels)
research/
  problem_selection.md    the candidate pool, why this problem was chosen, targets A–E
  literature_review.md    every source checked, and the searches that found nothing
  novelty_assessment.md   honest classification, including the claims we withdrew
paper/
  main.tex, main.pdf      the write-up (compiles with tectonic)
src/
  convex_geometry.py      exact rational arithmetic: convexity, unit pairs, crossings
  constructions.py        exact certificates for k = 2, 3, 4 crossing configurations
  search_density.py       annealing search for convex density > 2 (inconclusive)
  aligned_lens.py         grid-aligned two-circle lens search (inconclusive)
tests/
  test_claims.py          tests every theorem that admits a checkable instance
```

## Dependencies and reproduction

Python 3.14 (any 3.9+ should do), `numpy` (only for the numerical search); exact
arithmetic uses the standard library `fractions`.

```bash
# 1. exact certificates for all constructions and every checkable theorem instance
python -m tests.test_claims            # → "all tests passed"

# 2. print the exact certificates (convexity, unit distances, crossings)
python -m src.constructions

# 3. the annealing search for u(P) >= 2n (negative, ~2 minutes)
python -m src.search_density

# 4. the grid-aligned lens search (negative)
python -m src.aligned_lens

# 5. rebuild the paper (tectonic)
tectonic -X compile paper/main.tex --outdir paper
```

Versions used for the reported runs: Python 3.14.6, numpy 2.4.6, tectonic 0.15,
PowerShell/Windows; results obtained 13 Oct 2026.  Randomised searches use fixed
`random.Random(seed)` seeds and are therefore deterministic.

## Honest limitations

* The Erdős–Moser conjecture is **not** solved; neither is Erdős–Fishburn's `u(P) ≤ 2n`.
* Theorem 3 (crossing) is almost certainly folklore among specialists, though we could
  not locate a statement of it.
* The numerical search did not beat `2n−7` and did not even reach the known optimum, so
  it is evidence of **no** value either way; it is included as a reproducible record of
  an attempt, not as a result.
* The forbidden `2×2` cut-matrix pattern that a diagonal split cannot contain is the
  pattern `S₂` of Fishburn–Reeds (1992); our proof of it was obtained independently but
  the result is not new, and the novelty file says so.

## Remaining open questions (see `paper/main.tex` §9)

1. `U_c(n) = O(n)` (equivalently: bounded minimum unit-degree).
2. `u(P) ≤ 2n` (equivalently: minimum unit-degree `≤ 4`).
3. Erdős #97: no convex set has property `E_4`.
4. Is the minimum unit-degree of every convex `n`-gon at most `3`?  (Would give
   `U_c(n) ≤ 3n`.)
5. Improve `n log₂ n + 4n` to `o(n log n)`.

## Citations

* P. Erdős and L. Moser, Problem 11, *Canadian Math. Bulletin* 2 (1959), 43.
* H. Edelsbrunner and P. Hajnal, *J. Combin. Theory Ser. A* 56 (1991), 312–316.
* Z. Füredi, *J. Combin. Theory Ser. A* 55 (1990), 316–320.
* P. Brass and J. Pach, *J. Combin. Theory Ser. A* 94 (2001), 178–179.
* A. Aggarwal, *Discrete Math.* 338 (2015), 88–92 (arXiv:1009.2216).
* P. C. Fishburn and J. A. Reeds, *Comput. Geom. Theory Appl.* 2 (1992), 81–91.
* E. Altman, *Amer. Math. Monthly* 70 (1963), 148–157; *Canad. Math. Bull.* 15 (1972), 329–340.
* F. Morić and D. Pritchard, arXiv:1103.0412 (2011).

## License

MIT — see [`LICENSE`](LICENSE).  The mathematical content is offered as a research
record; correctness claims are limited to those labelled **PROVED HERE** in
`mathematics/main_results.md`.
