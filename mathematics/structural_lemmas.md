# Structural lemmas (all proved here)

Notation as in `definitions.md`.  `C(v, 1)` is the unit circle centred at `v`.

---

### Lemma 1 (common neighbours). *If `x ≠ y` then `|N(x) ∩ N(y)| ≤ 2`.*

**Proof.** `N(x) ⊂ C(x,1)` and `N(y) ⊂ C(y,1)`, so
`N(x) ∩ N(y) ⊆ C(x,1) ∩ C(y,1)`.  Two distinct circles meet in at most two points,
and `C(x,1) ≠ C(y,1)` because `x ≠ y`. ∎

---

### Lemma 2 (half-plane corollary / semicircle). *For `v ∈ P` all other points of `P`
lie in the open half-plane bounded by a supporting line at `v`.  Consequently
`N(v)` is contained in an arc of `C(v,1)` of angular length `< π`.*

**Proof.** A strictly convex set has a supporting line at each of its vertices, touching
`P` only at `v`; strict convexity puts every other point of `P` strictly on the interior
side.  Directions from `v` to the other points therefore lie in an open interval of
length `π`, and every `w ∈ N(v)` has direction from `v` lying in that interval. ∎

---

### Lemma 3 (angular monotonicity). *Let `P = {w_1, …, w_{n-1}} ∪ {v}` with
`w_1, …, w_{n-1}` in cyclic order.  Then the directions from `v` to
`w_1, w_2, …, w_{n-1}` are strictly increasing (modulo the choice of origin angle).*

**Proof.** The diagonals `v w_i` (`i = 2, …, n-2`) lie inside the polygon and triangulate
it: the triangles `△(v w_i w_{i+1})`, `i = 1, …, n-2`, are pairwise interior-disjoint and
cover `P`'s convex hull (the standard fan triangulation from a vertex, valid because the
polygon is convex).  If two of the directions `v → w_i`, `v → w_j` (`i < j`) were not in
cyclic order, the corresponding triangles `△(v w_i w_{i+1})` and `△(v w_j w_{j+1})` would
overlap in the interior, contradicting interior-disjointness. ∎

**Consequence (the local model of a vertex).** Listing `N(v) = {u_1, …, u_d}` in the
order given by Lemma 3, the angles `θ_1 < θ_2 < ⋯ < θ_d < π` of the directions
`v → u_i` satisfy `θ_d − θ_1 < π`, and the map `i ↦ θ_i` is the cyclic order of `P`.

---

### Lemma 4 (the 60° lemma). *If `x, y, z ∈ P` with `xy, yz, zx ∈ E(G)` — a unit
triangle — then `∠yxz = ∠xyz = ∠yzx = π/3`.  In particular `G` contains no `K_4`.*

**Proof.** A triangle with all three sides equal to `1` is equilateral.  Four points of
`ℝ²` cannot be pairwise at distance `1`, so no `K_4` can appear in `G`. ∎

---

### Lemma 5 (neighbourhoods). *For every `v`, `G[N(v)]` is a disjoint union of paths
whose components have at most three vertices.  Hence `v` lies in at most
`2·d(v)/3` unit triangles, and `G[N(v)]` is triangle-free.*

**Proof.** By Lemma 2, the points of `N(v)` lie on an arc of `C(v,1)` of angular length
`< π`; by Lemma 4, whenever `y, z ∈ N(v)` are adjacent in `G` the angle `∠yvz` equals
exactly `π/3`.  So every edge of `G[N(v)]` joins two points of `N(v)` whose angular
parameters differ by exactly `π/3`.  Hence every vertex of `G[N(v)]` has degree at most
`2` (partners at `+π/3` and `−π/3`, each existing at most once, because two points at the
same angle and radius on `C(v,1)` coincide).  A component of maximum degree `≤ 2` is a
path or a cycle; but a component contains a vertex of minimum angular parameter, which
has degree `≤ 1`, so no component is a cycle: all components are paths.  A path with `ℓ`
vertices has `ℓ − 1` edges, each spanning exactly `π/3` in angle; since the whole arc has
length `< π = 3·(π/3)`, the angles of a path take at most three distinct values, so
`ℓ ≤ 3`.  Finally `G[N(v)]` is triangle-free, since a triangle inside `N(v)` together
with `v` would be a `K_4` in `G`, excluded by Lemma 4. ∎

---

### Lemma 6 (no unit `K_{2,2}` across a diagonal). *Let `ab` be a diagonal of the
polygon `P` and let `A, B` be the two non-empty open chains of vertices into which it
splits `P`.  Then there are no `x, x′ ∈ A` and `y, y′ ∈ B` with all four distances
`|xy|, |xy′|, |x′y|, |x′y′|` equal to `1`.*

**Proof.** Suppose `x, x′, y, y′` exist.  Because `P` is strictly convex, the four points
are in convex position, and their cyclic order is either *alternating*
(`x, y, x′, y′`) or *grouped* (`x, x′, y, y′`) up to relabelling.

*Step 1 — the hypothesis forces the alternating order.*  `y` is at distance `1` from both
`x` and `x′`, so `y ∈ C(x,1) ∩ C(x′,1)`; likewise `y′`.  Since `y ≠ y′` and two distinct
unit circles meet in at most two points (Lemma 1), `{y, y′} = C(x,1) ∩ C(x′,1)`, which
requires `|xx′| < 2`; the two points of that intersection lie on opposite sides of the
line `xx′`.  Symmetrically, `{x, x′} = C(y,1) ∩ C(y′,1)` and `x, x′` lie on opposite
sides of the line `yy′`.

Now assume the cyclic order is grouped, i.e. (after relabelling) the four points occur as
`x, x′, y, y′`.  Then `x` and `x′` are adjacent vertices of the quadrilateral they span
and `y, y′` are adjacent.  Applying the argument of Step 1 inside this quadrilateral:
`y, y′ ∈ C(x,1) ∩ C(x′,1)` forces `y, y′` to lie on opposite sides of the line `xx′`; but
two adjacent vertices of a convex quadrilateral lie on the same side of the line through
the other two vertices — hmm, this needs care, so proceed by coordinates instead:
put `x = (0,0)`, `x′ = (t,0)` with `0 < t < 2`.  The two points at distance `1` from both
are `(t/2, ±h)` with `h = √(1 − t²/4) > 0`, one above and one below the `x`-axis.  In a
grouped order the two points on the same side of the line `xx′` would be adjacent, but
the quadrilateral `(0,0), (t,0), (t/2,h), (t/2,−h)` has its cyclic order
`(0,0), (t/2,h), (t,0), (t/2,−h)` — alternating, never grouped.  Hence the cyclic order
of the four points is alternating, and the quadrilateral is a rhombus with side `1`
(its diagonals are `xx′` and `yy′`).

*Step 2 — a diagonal split forbids the alternating order.*  The cyclic order of the
polygon is `a`, (vertices of `A`), `b`, (vertices of `B`), back to `a`; the two open
chains are contiguous arcs of the cyclic order.  Since `x, x′ ∈ A` and `y, y′ ∈ B`, the
restriction of the cyclic order to `{x, x′, y, y′}` is grouped (two consecutive from
`A`, two consecutive from `B`), contradicting Step 1. ∎

**Remark (sharpness).** The obstruction in Step 1 is real: the four points
`(±3/5, 0), (0, ±4/5)` form a rhombus of side `1` and hence contain a unit `K_{2,2}`.
What Lemma 6 rules out is only the appearance of such a `K_{2,2}` *inside a single
diagonal-split*, i.e. of the pattern

```
1 1
1 1
```

as a submatrix of a cut matrix.  This is a different (and, as far as we could tell, not
previously recorded) forbidden configuration for the 0-1 cut matrices of Füredi and
Aggarwal; see `research/novelty_assessment.md`.

---

### Theorem 7 (arbitrarily many pairwise crossing unit distances). *For every `k ≥ 1`
and every `n ≥ 2k` there is a set `P` of `n` points in strictly convex position whose
unit-distance graph contains `k` pairwise crossing edges.*

**Proof.** Let `δ = π/(3k)` and place `2k` points on the unit circle at angles
`0, δ, 2δ, …, (2k−1)δ`.  They lie on a circular arc of total length `2kδ = 2π/3 < π`,
hence they are in strictly convex position.  The `k` chords `(z_i, z_{i+k})`,
`i = 1, …, k`, are the main diagonals of this convex `2k`-gon: for `i < j ≤ k` their
endpoints occur in the cyclic order `z_i, z_j, z_{i+k}, z_{j+k}`, so the two chords
cross in their interiors.  Moreover

```
|z_{i+k} − z_i| = 2·sin(kδ/2) = 2·sin(π/6) = 1 ,
```

so every main diagonal is a unit edge.  For `n > 2k`, insert `n − 2k` additional points
on the same circular arc at angles strictly between the existing ones; this keeps the set
strictly convex (still an arc of length `< π`) and destroys none of the unit distances
already present. ∎

**Corollary 8 (a limitation on a whole family of approaches).** For no integer `K` is
`U_c(n)` bounded by any theorem of the form "a topological graph on `n` vertices with no
`K + 1` pairwise crossing edges has at most `f(n)` edges" with `f(n) = O(n)`: the
unit-distance graph of a convex `2k`-gon contains `k` pairwise crossing edges, so taking
`k > K` violates the hypothesis of any such theorem.

*(For reference: the known bounds of this type are `2n − 4` edges when no three edges are
pairwise crossing (Capoyleas–Pach), and `O(n log^{2K−4} n)` in general; all of them are
vacuous for the unit-distance graphs of Theorem 7.)*

---

### Lemma 9 (round sets). *If the vertices of `P` lie on `k` circles, then `d(v) ≤ 2k`
for every `v`, and `u(P) ≤ k·n`.*

**Proof.** Fix `v`.  For each of the `k` circles `Γ`, the intersection
`C(v,1) ∩ Γ` consists of at most two points, so `v` has at most `2k` unit-neighbours in
`P`.  Hence `Σ_v d(v) ≤ 2kn` and `u(P) = ½Σ_v d(v) ≤ kn`. ∎

**Corollary.** Points on one circle: `u ≤ n`.  Points on a parabola or an ellipse (each
meeting a unit circle in at most `4` points by Bézout): `u ≤ 2n`.

---

### Theorem 10 (the bridge: bounded minimum degree ⟺ `U_c(n) = O(n)`). *The following
are equivalent:*

1. *`U_c(n) = O(n)`;*
2. *there is a constant `c` such that every convex `n`-gon has a vertex of unit-degree
   at most `c`;*
3. *the class `{G(P) : P finite, strictly convex}` has bounded degeneracy.*

**Proof.** (2) ⟹ (1): induct on `n`.  If `n` is small the claim is vacuous.  For `n`
large, take a vertex `v` of degree `≤ c`, remove it — the remaining `n − 1` points are
still strictly convex — and apply the induction hypothesis:
`u(P) ≤ c + c(n − 1) = cn`.

(1) ⟹ (2): if `u(P) ≤ Cn` for all convex `n`-sets then the average unit-degree is
`2u(P)/n ≤ 2C`, so some vertex has degree `≤ 2C`; take `c = 2C`.

(2) ⟺ (3): every induced subgraph of `G(P)` is the unit-distance graph of a subset of
`P`, which is again strictly convex; hence a degree bound for all convex point sets is
exactly a degeneracy bound for the class. ∎

**Corollary 11 (reformulation of Erdős–Moser).** *The Erdős–Moser conjecture is
equivalent to:*

> there is an absolute constant `c` such that every finite set of points in strictly
> convex position has a vertex incident to at most `c` unit segments.

In particular, proving that *some* vertex of every convex `n`-gon has at most `c` unit
neighbours — for **any** absolute constant `c` — settles the 1959 conjecture.  The best
currently available statement follows from Aggarwal's `U_c(n) ≤ n log₂ n + 4n` and gives
`c ≤ 2 log₂ n + 8`, which still grows with `n`.

---

## What these lemmas do *not* give (recorded honestly)

* Lemmas 1 and 5 bound the number of *unit triangles* through a vertex by `2d(v)/3`, but
  Lemma 1 alone permits minimum degree up to `≈ 2√n`: `Σ_v C(d_v,2) = Σ_{x≠y} |N(x)∩N(y)|
  ≤ 2·C(n,2)` is consistent with `d(v) ≈ 2√n` for all `v`.  A constant degeneracy bound
  therefore needs the geometry, not just the counting.
* Lemma 6 forbids `K_{2,2}` in every diagonal-split, which is a *different* forbidden
  pattern from Füredi's `(1 1 *; 1 * 1)`; combining the two does not by itself improve
  the strip argument of Füredi–Brass–Pach–Aggarwal, because the strip bound
  `(a+b)(2log₂(a+b)−1)` for an `a × b` cut matrix is stronger than the
  `K_{2,2}`-free (Kővári–Sós–Turán) bound `O(a√b + b)` in the regimes the strip argument
  uses.  Improving `n log n` to `o(n log n)` is **UNRESOLVED** in this project.
* Whether δ(G) ≤ 3 for every finite convex `P` (which would give `U_c(n) ≤ 3n`) is
  **UNRESOLVED** here; see `mathematics/main_results.md` §4 for the computational
  evidence collected.
