# Definitions

Throughout, `P = {p_1, …, p_n} ⊂ ℝ²` is a finite set of points in **strictly convex
position**: the points are the vertices of a strictly convex `n`-gon — equivalently,
every point is an extreme point of `conv(P)` and no three points are collinear.  We
always list `P` in counter-clockwise boundary order.

* `|p − q|` — Euclidean distance.
* **Unit-distance graph** `G = G(P)`: the graph on vertex set `P` with

      xy ∈ E(G)   ⟺   |x − y| = 1.

  `G` is simple and unweighted; `u(P) := |E(G)|` is the number of unit distances of `P`.
* `U_c(n) := max{ u(P) : |P| = n, P in strictly convex position }` — the extremal
  function of the Erdős–Moser problem.
* `d(v) := deg_G(v)` — the **unit-degree** of `v`; `δ(G)` the minimum degree.
* **Degeneracy:** a graph is `c`-degenerate if every subgraph has a vertex of degree
  at most `c`.
* **Main diagonals of a convex `2k`-gon** `z_1, …, z_{2k}`: the `k` chords
  `(z_i, z_{i+k})`, `i = 1, …, k`.
* A **crossing pair** of edges: two edges of `G` (drawn as straight segments between
  the points) that cross in their interiors.
* **`k`-crossing:** a set of `k` pairwise crossing edges.

## The problem

* **Erdős–Moser (1959).** Is `U_c(n) = O(n)`?
* **Erdős–Moser (1959, first guess).** `U_c(n) ~ 5n/3 + O(1)` — *false*
  (Edelsbrunner–Hajnal 1991: `U_c(n) ≥ 2n − 7`).
* **Erdős–Fishburn.** `u(P) ≤ 2n` for every convex `n`-set `P`.
* **Erdős (#97 / property `E_4`).** Is there a finite convex point set in which every
  point has at least 4 other points at a common distance from it?  (Danzer constructed
  arbitrarily large finite convex sets with property `E_3`.)

## The three facts about a single vertex that drive everything

For `v ∈ P`, write `N(v)` for the unit-neighbours of `v` and use the cyclic order of
`P`. The arc `C(v,1)` is the unit circle centred at `v`.

1. **Common neighbours.** If `x ≠ y` then `|N(x) ∩ N(y)| ≤ 2`
   (two distinct unit circles meet in at most two points).
2. **Half-plane (semicircle).** A strictly convex set has a unique supporting line at
   `v`; every other point of `P` lies in the open half-plane it bounds.  Hence the
   directions from `v` to the other points span an angle **< π**, and `N(v)` lies on an
   arc of `C(v,1)` of angular length < π.
3. **Angular monotonicity.** From `v`, the directions to the other vertices appear in
   the same cyclic order as the vertices (the fan `v, w_1, …, w_{n-1}` is a
   triangulation of the polygon).  Combined with 2: the unit-neighbours of `v` appear
   in cyclic order along an arc of `C(v,1)` of angular length < π.
