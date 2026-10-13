# Unit-distance graphs of convex polygons (the Erdős–Moser problem)

An autonomous investigation of the problem posed by Erdős and Moser in 1959:

> For a finite set `P` of `n` points in strictly convex position in the plane, let
> `u(P)` be the number of pairs of points at distance exactly 1. Is `U_c(n) =
> max u(P) = O(n)`?

The current bounds are `2n − 7 ≤ U_c(n) ≤ n log₂ n + 4n`
(Edelsbrunner–Hajnal 1991 below; Aggarwal 2015 above).

*Put the actual result here as soon as the main theorem is settled — see
`mathematics/main_results.md` for the current state.*

Status of this repository: **work in progress**. See
[`research/problem_selection.md`](research/problem_selection.md) for the target and
[`research/literature_review.md`](research/literature_review.md) for verified sources.

## Repository map

```
research/       problem selection, verified literature, research log
mathematics/    definitions, structural lemmas, main theorems and proofs
src/            exact-arithmetic and small-search code
tests/          automated tests for every computational claim
paper/          the write-up
```
