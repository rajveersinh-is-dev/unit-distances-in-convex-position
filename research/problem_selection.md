# Research: unit distances among vertices of a convex polygon (the Erdős–Moser problem)

*Working record. Every claim below is labelled with an evidence category
(PROVED HERE / ESTABLISHED IN PRIOR WORK / COMPUTATIONALLY VERIFIED /
CONJECTURED / etc.). Nothing in this repository is claimed without such a label.*

---

## 1. Candidate pool that was surveyed before selection

| # | Problem | Status found | Why rejected as main target |
|---|---|---|---|
| 1 | Erdős distinct subset-sums conjecture (a_n ≥ c·2^n for dissociated sets) | open (erdosproblems.com/1); frontier: c·2^n/√n, constant √(2/π) (Dubroff–Fox–Xu 2020), finite refinement H_n = Σ binom(j,⌊j/2⌋) (arXiv:2609.27941, Aug 2026) | Extremely active frontier with monthly refinements; the decisive insight (a "variance/near-Gaussian" argument) is already exhausted in the literature |
| 2 | Erdős conjecture on large sum-free subsets (S(N) ≥ N/3 + ω(N)) | **solved in 2025** (L¹-estimate paper, arXiv 2025-02; S(A) ≥ N/3 + c·log log N) | already solved — discarded |
| 3 | Minimum number of distinct subset sums | **classically solved**: every n-set of positive reals has ≥ binom(n+1,2)+1 distinct subset sums, equality iff homogeneous APs; the current frontier is *stability/inverse* versions (arXiv:2605.05498, Carpenter–Defant–Kravitz 2026) | inverse theorem requires deep Freiman-type machinery |
| 4 | Seymour's second neighbourhood conjecture | open, but 2026 preclaims: δ ≤ 7 via CP-SAT (arXiv:2606.30588), dense case n = 2δ+2 (arXiv:2608.11530) | frontier is moving by computer-assisted case analysis, not structural insight |
| 5 | Vizing's conjecture (γ(G□H) ≥ γ(G)γ(H)) | open; best γ(G□H) ≥ ½γ(G)γ(H) + ½max(γ,γ) (Zerbib 2022); known for γ ≤ 3, cycles, chordal, decomposable, Type X | partial results are one-class-at-a-time; no internal lever available |
| 6 | Gyárfás–Sumner / polynomial χ-boundedness | open; **P5 case solved Dec 2025** (Nguyen, arXiv:2512.24907); P_k, k ≥ 6 open | requires absorbing a 40+-page recent framework |
| 7 | Conway's thrackle conjecture, Barnette, Tutte 5-flow, Caccetta–Häggkvist | open | no plausible point of entry within this run |
| 8 | Erdős–Moser: **unit distances among vertices of a convex polygon** | **open** (Erdős problem 96); U_c(n) = O(n)? conjectured; best upper n·log₂ n + 4n (Aggarwal 2015), best lower 2n − 7 (Edelsbrunner–Hajnal 1991) | **SELECTED** — see below |

## 2. Why target 8 was selected

* **Genuinely open since 1959**, precisely stated, with a clean quantitative frontier
  (`2n − 7 ≤ U_c(n) ≤ n log₂ n + 4n`).
* The **decisive work is structural, not computational**: the entire known proof
  apparatus (0-1 cut matrices, strips of width 2, forbidden submatrices) is
  elementary and self-contained; no heavy external theory is needed.
* On first contact I derived several structural facts about the *unit-distance
  graph* of a convex polygon that appear to be absent from the literature
  (see `mathematics/structural_lemmas.md`), and one of them gives an exact
  equivalence between the Erdős–Moser conjecture and a *bounded-minimum-degree*
  statement about these graphs. That gives the run a concrete, testable internal lever.
* Sub-questions (Erdős–Fishburn: is U_c(n) ≤ 2n? Erdős #97 / property E_4) are
  independently interesting and are each tractable by a combination of structural
  argument and small exact-arithmetic computation.

## 3. The exact problem

Let `P` be a finite set of `n` points in **strictly convex position** in ℝ² (the
vertex set of a strictly convex n-gon). Write

    u(P) = #{ {x,y} ⊆ P : x ≠ y, |x − y| = 1 },     U_c(n) = max{ u(P) : |P| = n, P convex }.

* **Erdős–Moser (1959):** is `U_c(n) = O(n)`? (Erdős offered $500 / repeatedly
  asked for a linear bound.)
* **Erdős–Moser 1959 (original guess):** `U_c(n) < Cn` — refuted by Edelsbrunner–Hajnal (1991)
  with a construction achieving `2n − 7`.
* **Erdős–Fishburn:** `u(P) ≤ 2n` for every convex n-set P.
* **Erdős (#97 / property E_4):** no finite convex point set P has the property that
  *every* p ∈ P has at least 4 other points of P at a common distance from p.

Strongest known results:

| Bound | Source | Category |
|---|---|---|
| `U_c(n) ≤ O(n log n)` | Füredi 1990 (JCTA 55, 316–320): 12n log₂ n − 6n | ESTABLISHED IN PRIOR WORK |
| `U_c(n) ≤ n log₂ n + O(n)` | Brass–Pach (2001) short proof; **`n log₂ n + 4n`** Aggarwal 2015 (Discrete Math. 338, 88–92) | ESTABLISHED IN PRIOR WORK |
| `U_c(n) ≥ 2n − 7` | Edelsbrunner–Hajnal 1991 (JCTA 56, 312–316) | ESTABLISHED IN PRIOR WORK |
| `m_k ≤ 2kn`, and `m_k ≤ kn` for convex position; top-k sum ≤ (2k−1)n | Altman 1963/1972; Morić–Pritchard 2011 (arXiv:1103.0412) | ESTABLISHED IN PRIOR WORK |

(Here `m_k` is the multiplicity of the k-th largest distance; Morić–Pritchard also
prove the Erdős–Lovász–Vesztergombi conjecture `m_1+…+m_k ≤ kn` for k ≤ 4 by
computation.)

## 4. Research map (targets A–E)

* **Target A (full result).** Prove `U_c(n) = O(n)`.
* **Target B (intermediate, and the main one pursued here).** Prove that the
  **minimum unit-degree** of the unit-distance graph of a convex n-gon is bounded by
  an absolute constant; ideally ≤ 3. By the bridge lemma
  (`mathematics/main_results.md`, Theorem 2) this is *equivalent* to Target A.
* **Target C (weaker, very concrete).** Decide whether some convex n-gon has
  minimum unit-degree ≥ 4 (equivalently `u(P) ≥ 2n`), which would refute the
  Erdős–Fishburn bound `u(P) ≤ 2n` and beat the `2n − 7` record.
* **Target D (obstruction).** Show that a *natural* approach is limited: exhibit,
  for every k, a convex polygon with k pairwise crossing unit chords
  (`mathematics/structural_lemmas.md`, Theorem 3). This rules out obtaining O(n) from
  any quasi-planarity bound of bounded order.
* **Target E (independent structural question).** Erdős #97: no convex set has
  property E_4.
