# Literature review and verification of sources

All entries below were checked against the live arXiv API / publisher pages on
13 Oct 2026 (day of this run). Bibliographic details are copied from the records
that were actually fetched; nothing here is reconstructed from memory.

## Primary sources for the target problem

1. **P. Erdős and L. Moser (1959)**, problem on the maximum number of unit distances
   among the vertices of a convex n-gon. Appears in: P. Erdős, "On some problems of
   elementary and combinatorial geometry", *Ann. Mat. Pura Appl.* (1975) and in
   *Paul Erdős: The Art of Counting* (ed. J. Spencer, MIT Press, 1973); also as
   [Va99, 4.68] in Z. Füredi's list and as **Erdős problem 96 on
   erdosproblems.com**. Original guess `U_c(n) ~ 5n/3 + O(1)` was refuted
   (see [EdHa91]).

2. **H. Edelsbrunner, P. Hajnal, "A lower bound on the number of unit distances
   between the vertices of a convex polygon", J. Combin. Theory Ser. A **56** (1991),
   312–316.** Establishes `U_c(n) ≥ 2n − 7`. [ESTABLISHED IN PRIOR WORK]

3. **Z. Füredi, "The maximum number of unit distances in a convex n-gon",
   J. Combin. Theory Ser. A **55** (1990), 316–320.** Proves
   `f(n) ≤ 12 n log₂ n − 6n`. Proof: strip decomposition (strips of width 2 around
   lines 3y = 2k and 3x = 2k) + a 0-1 matrix lemma: an a×b 0-1 matrix with no
   submatrix of the shape
   ```
       1 1 *
       1 * 1
   ```
   has at most `a + (a+b)⌊log₂ b⌋` ones; plus Corollary 2.3 for unit pairs across a
   line. Records Klaus Danzer's construction of arbitrarily large finite convex sets
   with "property E_3" and Erdős's conjecture that no finite convex set has
   property E_4 (Erdős #97). [ESTABLISHED IN PRIOR WORK]

4. **P. Brass and J. Pach (2001)**, short proof of the O(n log n) bound
   (referenced by Aggarwal as giving the same order with a simpler argument).

5. **A. Aggarwal, "On Unit Distances in a Convex Polygon", arXiv:1009.2216 (2010);
   Discrete Mathematics 338 (2015), 88–92.** Improves Füredi to `U_c(n) ≤ n log₂ n + 4n`.
   Introduces cut matrices (0-1 matrices of unit pairs across a diagonal), shows they
   are "distance-like" matrices, and uses two properties of convex polygons ("diagonal
   property" and "obtuse angle property") to forbid additional patterns, including a
   class of cycles; answers a question of Fishburn and Reeds in the negative.
   [ESTABLISHED IN PRIOR WORK]

6. **F. Morić and D. Pritchard, "Counting large distances in convex polygons",
   arXiv:1103.0412 (2011); short version at EuroComb 2011; Comput. Geom. Theory Appl.**
   Prove `m_1+…+m_k ≤ (2k−1)n` in general, and the Erdős–Lovász–Vesztergombi
   conjecture `m_1+…+m_k ≤ kn` for `k ≤ 4` (for large n) by exhaustive computer
   search over distance configurations of two disjoint convex-hull intervals;
   also `m_3 ≤ 3n/2` for large n. Conjecture 1.1 in that paper is the
   Erdős–Fishburn statement `u(P) ≤ 2n`. [ESTABLISHED IN PRIOR WORK]

7. **E. Altman, "On a problem of P. Erdős", Amer. Math. Monthly 70 (1963), 148–157;
   "Some theorems on convex polygons", Canad. Math. Bull. 15 (1972), 329–340.**
   Source of the "diagonal property" and the bounds `m_k ≤ 2kn`, `m_k ≤ kn` in
   convex position. [ESTABLISHED IN PRIOR WORK]

8. **Z. Füredi, "The maximum number of unit distances in a convex n-gon"** also
   records Erdős's conjecture that no finite convex set has property E_4
   (Erdős problem 97 on erdosproblems.com).

9. **erdosproblems.com/96 and /97** (maintained by Thomas Bloom), status "open" as of
   the page edit of 23 Jan 2026 (fetched 13 Oct 2026). [ESTABLISHED IN PRIOR WORK]

## Searches performed, and what they did *not* find

* arXiv full-text/API queries on: "unit distances" + "convex"; "convex polygon" +
  "unit distances"; "unit distances in convex position". The only recent hits are
  Aggarwal 2010/2015 and Morić–Pritchard 2011 — i.e. the problem was **not** solved by
  anyone between 2015 and 2026. So "Recently solved" is ruled out for the main
  problem: classification = **Confirmed open**.
* Searched for a "minimum-degree reformulation" of the Erdős–Moser conjecture.
  **No source found** stating that `U_c(n) = O(n)` is equivalent to a bounded
  minimum unit-degree. This is claimed here as a new (but elementary) bridge lemma;
  see the novelty assessment.
* Searched arXiv for "superlinearly many unit distances in convex position"
  (a 2026 preprint posted on an external bounty venue, claiming a Lean-verified
  disproof of Erdős 96): **the paper is not on arXiv** and could not be retrieved;
  it is *not* cited as a source in this project and its claim is not relied upon.
  Our own structural results below are independent of it.
* Searched erdosproblems.com and general web for "distinct subset sums" minimum
  count, Seymour's second neighbourhood, Vizing's conjecture, χ-boundedness,
  sum-free subsets — used for the candidate table only.

## Verdict on status

**Confirmed open.** The precise statement `U_c(n) = O(n)?` is listed as open by a
specialist-maintained database (erdosproblems.com/96), the strongest published upper
bound dates from 2015, and no arXiv submission between 2011 and 2026 addresses it.
