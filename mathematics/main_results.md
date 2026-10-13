# Main results: what is proved here

Every statement below is labelled with its evidence category.  The two problems that
motivated the work (Erdős–Moser 1959, Erdős–Fishburn) are **not** solved by this
project; see §5.

---

## 1. The bridge theorem (PROVED HERE)

**Theorem 1 (bounded degree ⟺ linear bound).** For a finite set `P` of points in
strictly convex position let `G(P)` be its unit-distance graph.  The following are
equivalent:

1. `U_c(n) = O(n)`;
2. there is an absolute constant `c` such that every such `P` has a vertex of
   unit-degree at most `c`;
3. the class `{G(P)}` has bounded degeneracy.

*Proof.* `mathematics/structural_lemmas.md`, Theorem 10. ∎

**Corollary (reformulation).** Erdős–Moser (1959) is equivalent to the statement that
every finite strictly convex point set contains a vertex incident to at most `c` unit
segments for some absolute constant `c`.  The best statement currently available in the
literature is the consequence of Aggarwal's `U_c(n) ≤ n log₂ n + 4n`: some vertex has
degree at most `2 log₂ n + 8`, which still grows.

---

## 2. Neighbourhood structure (PROVED HERE)

**Theorem 2.** For every vertex `v` of `G(P)`:

* (a) `G[N(v)]` is a disjoint union of paths with at most three vertices each;
* (b) an edge of `G[N(v)]` joins two unit-neighbours of `v` that are exactly `π/3`
  apart as seen from `v`;
* (c) `v` lies in at most `2·d(v)/3` unit triangles, so if `u = u(P)` then the number of
  unit triangles of `P` is at most `4u/9`.

*Proof.* `mathematics/structural_lemmas.md`, Lemma 5 (parts (a), (b) and (c)). ∎

---

## 3. Pairwise crossing unit distances, and what they rule out (PROVED HERE)

**Theorem 3.** For every `k ≥ 1` and every `n ≥ 2k` there is a set of `n` points in
strictly convex position whose unit-distance graph contains `k` pairwise crossing edges.

*Proof.* `mathematics/structural_lemmas.md`, Theorem 7: `2k` points on the unit circle at
angles `0, π/(3k), 2π/(3k), …`; the `k` main diagonals have angular separation `π/3` and
hence length `1`.

**Corollary 4 (limitation result).** No theorem of the form

> a topological graph on `n` vertices with no `K + 1` pairwise crossing edges has at most
> `f(n)` edges, where `f(n) = O(n)`,

can prove `U_c(n) = O(n)` for any fixed `K`.  (The kind of bound one would need — `2n − 4`
edges with no three pairwise crossing edges — is contradicted by Theorem 3 as soon as
`k > K`.)

Thus one whole natural family of attacks (bidding on quasi-planarity of
`G(P)`) is **excluded**, independent of the Erdős–Moser conjecture itself.

---

## 4. Classes with bounded density (PROVED HERE)

**Theorem 5.** If the vertices of `P` lie on `k` circles then `u(P) ≤ k n`.
More generally, if they lie on `k` algebraic curves of degree at most `d`, then
`u(P) ≤ k d n`.  In particular:

* vertices on one circle: `u(P) ≤ n`;
* vertices on a parabola or an ellipse: `u(P) ≤ 2n` — the density bound conjectured for
  general convex position by Erdős–Fishburn already holds for these curves.

*Proof.* A unit circle centred at a vertex meets any circle, or any curve of degree `d`,
in at most `2`, resp. `2d`, points, so `d(v) ≤ 2kd` and `u = ½Σd(v) ≤ kdn`.  (The
`k = 1` case and the "two circles meet in ≤ 2 points" input are classical since
Erdős 1946.) ∎

---

## 5. What is **not** proved here (UNRESOLVED)

| Statement | Status |
|---|---|
| Erdős–Moser 1959: `U_c(n) = O(n)` | **open**; best bounds `2n − 7 ≤ U_c(n) ≤ n log₂ n + 4n` |
| Erdős–Fishburn: `u(P) ≤ 2n` | **open**; `2n − 7` is achieved |
| Erdős #97: no convex set has property `E_4` | **open** |
| `δ(G(P)) ≤ 3` for all finite convex `P` (would give `U_c(n) ≤ 3n`) | **UNRESOLVED**; no counterexample found, no proof |
| `δ(G(P)) ≤ 4` for all finite convex `P` | **UNRESOLVED**; equivalent to `u(P) < 2n`, i.e. to Erdős–Fishburn |
| Improving `n log₂ n + 4n` to `o(n log n)` | **UNRESOLVED** here; the known routes (cut matrices / strips) were examined and no improvement found |

**Best densities found computationally** (simulated annealing over convex `n`-gons,
`n = 6…14`, seeded from the known extremal family): `u/n ≈ 0.86` at `n = 14` — far below
the `2 − 7/n` achieved by the published construction.  The search is a negative result:
it did not find any configuration with `u(P) ≥ 2n`, but it also does not reach the known
optimum, so it is **evidence of no value either way** about Erdős–Fishburn.
