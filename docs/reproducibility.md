# Reproducibility

Everything in this repository was produced in a single autonomous run on 13 Oct 2026.

## Environment actually used

| Component | Version / detail |
|---|---|
| OS | Windows 11, PowerShell 7 |
| Python | 3.14.6 (`C:\Python314`) |
| numpy | 2.4.6 |
| LaTeX | tectonic 0.15 (`tectonic -X compile`) |
| Git | 2.53.0.windows.1 |
| GitHub CLI | authenticated account `daveaddams91-dev` (scopes `gist, read:org, repo, user, workflow`) |

Exact arithmetic: Python `fractions.Fraction` throughout (`src/convex_geometry.py`).
Floating point is used *only* by the two numerical searches, and their output is never
used as evidence for a mathematical claim.

## Commands and what they produce

```bash
python -m tests.test_claims
```
Verifies, in exact rational arithmetic where possible:
* the three exact crossing configurations (`k = 2, 3, 4`) are strictly convex, their
  main diagonals all have squared length `1`, and the main diagonals pairwise cross;
* Theorem 3's unit-circle family for `k = 1..8` (numerical convexity/crossing with the
  exact trigonometric identity `2 − 2cos(kδ) = 1` checked separately);
* Lemma 1 (`≤ 2` common unit neighbours) and Lemma 5 (`G[N(v)]` is a union of paths of
  at most three vertices) on all constructions;
* the bridge theorem's averaging direction, and Theorem 5's one-circle bound
  `u(P) ≤ n` over 200 random circle configurations.

Expected output: many `[PASS]` lines ending in `all tests passed`.

```bash
python -m src.constructions
```
Prints the full certificates of the three exact constructions (n, strict convexity,
unit pairs, degree sequences).

```bash
python -m src.search_density       # ~2 minutes
python -m src.aligned_lens         # ~3 minutes
```
The two searches for a convex configuration with `u(P) ≥ 2n`.  Both are negative; both
are deterministic (fixed seeds).  Their output is reported verbatim in
`paper/main.tex` §8 and is **not** used as evidence for any mathematical claim.

```bash
tectonic -X compile paper/main.tex --outdir paper
```
Builds `paper/main.pdf` (verified: builds cleanly, one cosmetic overfull-hbox warning).

## What is *not* reproducible here

* The literature review: it was performed against live arXiv API queries and web
  searches on 13 Oct 2026.  Sources and the negative results of the searches are
  recorded in `research/literature_review.md`; a future reader with the same access can
  repeat them, but no snapshot of the web is included.
* No proof assistant (Lean/Coq/Isabelle) was available in this environment, so nothing
  in the repository is labelled *formally verified*.  The strongest evidence category
  used is *computed exactly by rational arithmetic* for the finite constructions.
