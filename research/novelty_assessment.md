# Novelty assessment (checked against the actual literature)

## Method

The literature was searched with the live arXiv API and with web search on
13 Oct 2026.  Aggarwal's paper (arXiv:1009.2216 / Discrete Math. 338 (2015) 88–92) was
read in full from the ar5iv rendering, including its §1.1 list of forbidden 0-1
matrices and its §2 proofs.

## Claims that are **NOT** ours (corrected after reading Aggarwal §1.1)

* **Lemma 6 (`K_{2,2}` forbidden in a diagonal cut).**  Aggarwal §1.1 attributes the
  forbidden matrix `S₂ = T₂ = [[1,1],[1,1]]` to **P. C. Fishburn and J. A. Reeds,
  "Unit distances between vertices of a convex polygon", Computational Geometry:
  Theory and Applications 2 (1992), 81–91**.  Our Lemma 6 is therefore
  **ESTABLISHED IN PRIOR WORK**; the argument in `structural_lemmas.md` is an
  independent proof of the same statement for diagonal splits, obtained before that
  source was located.  (Note also that Füredi's forbidden pattern
  `(1 1 *; 1 * 1)` does *not* imply `S₂`-freeness, because it needs three columns.)
* **Lemma 9 (points on `k` circles: `u ≤ kn`).**  The essential ingredient — two unit
  circles meet in at most two points — is the observation Erdős made in 1946 and which
  Spencer–Szemerédi–Trotter used for `U(n) = O(n^{4/3})`.  Our lemma is the
  circle-arrangement special case of that classical observation: **elementary corollary
  of ESTABLISHED IN PRIOR WORK**, not a new result.
* **Lemma 4 (unit triangles are equilateral).**  Immediate; the "60°" consequence is
  certainly folklore in this literature.
* The reformulation "proving `U(M_P) = O(n)` for cut matrices would prove
  `U_c(n) = Θ(n)`" appears in Aggarwal §1.1.  Our Theorem 10 is a *different*
  (minimum-degree) reformulation.

## Claims that are **ours but elementary** (potentially new, high confidence of being
new, but simple)

* **Theorem 10 (the bridge).**  `U_c(n) = O(n)` ⟺ some vertex of every convex `n`-gon
  is incident to at most `c` unit segments (absolute `c`) ⟺ the unit-distance graphs of
  convex point sets have bounded degeneracy.  No source locating this equivalence was
  found despite several searches; the proof is three lines.  Classified as
  **PROVED HERE / potentially new (elementary)**.
* **Lemma 5, sharp form.**  `G[N(v)]` is a disjoint union of paths of at most three
  vertices (edges of `G[N(v)]` only between points exactly `π/3` apart on `C(v,1)`).
  The ingredients are classical but the statement was not located.  Classified as
  **PROVED HERE / potentially new (elementary)**.
* **Theorem 7 (`k` pairwise crossing unit distances for every `k`).**  A one-line
  construction on the unit circle; the geometric content (that no bounded-order
  quasi-planarity bound applies) does not appear to be stated anywhere we could find,
  but it is very plausible folklore.  Classified as **PROVED HERE / likely folklore**.

## Claims that are conjectural or unresolved (do not present as results)

* Whether δ(G) ≤ 3 for every finite convex `P` (would give `U_c(n) ≤ 3n`).
* The Erdős–Moser conjecture itself, and the Erdős–Fishburn bound `u(P) ≤ 2n`.
