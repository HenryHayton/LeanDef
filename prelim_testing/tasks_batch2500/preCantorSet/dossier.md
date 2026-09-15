## Object

The *order-n pre-Cantor set* is the subset of the real line obtained by starting with the closed unit interval $[0,1]$ and, at each successive stage, replacing every closed interval present with the two closed sub-intervals that remain after its open middle third is deleted.  After $n$ such stages one obtains a finite union of $2^n$ closed intervals, each of length $3^{-n}$.  The classical Cantor (middle-thirds) set is the intersection of all these stages.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.preCantorSet : ℕ → Set ℝ
<!-- PINNED-SIGNATURE:END -->


The single argument is the stage number $n \geq 0$: a natural number that counts how many rounds of middle-third removal have been performed.  Stage $0$ yields the full unit interval; stage $n+1$ is obtained from stage $n$ by scaling the whole set by $1/3$ (left copy) and by the affine map $x \mapsto (2+x)/3$ (right copy).

## Conventions

The definition is total on all natural numbers; no junk values arise because every stage is a well-defined, non-empty compact subset of $\mathbb{R}$.

## Worked examples

- Claim: `VTask.preCantorSet 0 = Set.Icc 0 1` (stage 0 is exactly the unit interval $[0,1]$).

- Claim: The real number $1/3$ belongs to `VTask.preCantorSet 1` (it is the right endpoint of the left sub-interval $[0,1/3]$ kept after the first deletion).

- Claim: The real number $1/2$ does **not** belong to `VTask.preCantorSet 1` (it lies in the open middle third $(1/3, 2/3)$ removed at stage 1).

- Claim: `VTask.preCantorSet 1` equals `Set.Icc 0 (1/3) ∪ Set.Icc (2/3) 1` (after one step the two surviving closed thirds).

- Claim: `VTask.preCantorSet (n+1) ⊆ VTask.preCantorSet n` for every $n$ (the stages form a decreasing chain of compact sets).

- Claim: For every $n$, `VTask.preCantorSet n` is a union of exactly $2^n$ closed intervals each of length $3^{-n}$.

## Boundaries

- At stage $0$ the set is the entire closed unit interval; no removal has yet taken place.
- At every finite stage the set is compact, non-empty, and has measure $(2/3)^n$; it never becomes empty at any finite stage.
- The sets are strictly decreasing: each stage is a proper subset of all earlier stages.
- The self-similar structure is exact: `VTask.preCantorSet (n+1)` is the union of two scaled copies of `VTask.preCantorSet n` under the contractions $x/3$ and $(2+x)/3$.
- All endpoints of the surviving intervals at every stage are members of the set at all subsequent stages (they are never removed).

## Not to be confused with

- **The Cantor set itself**: that is the *intersection* over all $n$ of `VTask.preCantorSet n`, not any single finite-stage set.
- **A general Cantor-like set**: other constructions remove intervals of different proportions; this definition is specifically the middle-*thirds* construction.
- **The Cantor function (devil's staircase)**: a monotone function whose derivative is zero almost everywhere, defined in terms of the Cantor set but not itself a subset of $\mathbb{R}$.