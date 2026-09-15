## Object

`VTask.restrict` takes a point `w` in the standard simplex over a type `X` with coefficients in a semifield `K`, restricts its weights to a subset `s ⊆ X`, and normalises the result so that the weights again sum to 1. The output is therefore a well-defined point of the standard simplex whose support is contained in `s`. Geometrically, this is the operation of projecting (or "conditioning") a probability-weight vector onto a face of the simplex determined by `s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restrict : {X : Type u_2} -> {K : Type u_8} -> [Semifield K] -> [LinearOrder K] -> [IsStrictOrderedRing K] -> (w : Convexity.StdSimplex K X) -> (s : Set X) -> (hs : ∃ x ∈ s, w.weights x ≠ 0) -> Convexity.StdSimplex K X
<!-- PINNED-SIGNATURE:END -->


`VTask.restrict : {X : Type u_2} -> {K : Type u_8} -> [Semifield K] -> [LinearOrder K] -> [IsStrictOrderedRing K] -> (w : Convexity.StdSimplex K X) -> (s : Set X) -> (hs : ∃ x ∈ s, w.weights x ≠ 0) -> Convexity.StdSimplex K X`

The implicit type `X` is the vertex type of the simplex; `K` is the coefficient field (e.g. `ℝ` or `ℚ`). The typeclass assumptions give `K` the arithmetic structure needed to divide and compare weights. The argument `w` is the simplex point being projected. The argument `s` is the subset of vertices to which the weights are restricted. The proof `hs` certifies that at least one vertex in `s` carries a strictly positive weight in `w`, which is exactly the condition that makes normalisation well-defined (the total restricted weight is non-zero).

## Conventions

Weights of the restricted point at vertices outside `s` are zero: the filter discards them, so they do not appear in the support of the resulting weight function. The normalisation scalar is the reciprocal of the total weight on `s`; if that total were zero the construction would be undefined, which is why `hs` is required. No junk value is assigned for vertices outside the support — the weight function simply evaluates to 0 there by the filter.

## Worked examples

- Claim: For a uniform distribution on three vertices `{0, 1, 2}` each with weight `1/3`, restricting to the subset `{0, 1}` yields the uniform distribution on `{0, 1}`, i.e., each of the two remaining vertices receives weight `1/2`.

- Claim: The support of `(w.restrict s hs).weights` equals the intersection of the support of `w.weights` with `s` (as a `Finset`). Concretely, if `w` assigns positive weight only to vertices `a` and `b`, and `s = {a}`, then `(w.restrict s hs).weights` is the point mass at `a` with weight `1`.

- Claim: The restricted simplex point and the complementarily restricted simplex point together reconstruct `w` as a convex combination: `convexCombPair ... (w.restrict s hs) (w.restrict sᶜ hs') = w`, where the mixing weights are the total weight of `w` on `s` and on `sᶜ` respectively.

## Boundaries

- The hypothesis `hs` is strictly required: if every vertex in `s` had weight 0, the normalisation denominator would be 0 and the construction does not apply. The type signature enforces this by demanding the proof.
- If `s = Set.univ` (all vertices), then the restricted point equals `w` itself, since all weights are retained and their sum is already 1.
- If `s` contains exactly one vertex `x` with `w.weights x ≠ 0`, the result is the point mass at `x`, regardless of how small `w.weights x` was.
- The set `s` need not be finite; only the (finitely supported) part of `w.weights` that lands in `s` is used, so the construction remains well-defined for infinite `X`.

## Not to be confused with

- `Convexity.StdSimplex.convexCombPair`: combines two simplex points into one via a convex interpolation — the *inverse* of the splitting that `restrict` performs together with its complement.
- Restricting a measure to a sub-σ-algebra: that operation changes the measurable structure, not just the support; here only the weight values and their normalisation change.
- The face inclusion map into the standard simplex: a face inclusion *embeds* a lower-dimensional simplex into a higher-dimensional one, whereas `restrict` *projects* from a higher-dimensional simplex down to a lower-dimensional one.