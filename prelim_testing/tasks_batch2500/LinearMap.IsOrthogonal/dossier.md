## Object

A linear map `f : M → M` is **orthogonal** with respect to a bilinear form `B` on a module `M` over a commutative ring `R` if the form is *bi-invariant* under `f`: applying `f` to both arguments of `B` leaves the value unchanged. In other words, `f` preserves the "inner product" (or pairing) defined by `B` for every pair of vectors.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsOrthogonal : {R : Type u_20} -> {M : Type u_21} -> [CommRing R] -> [AddCommGroup M] -> [Module R M] -> (B : LinearMap.BilinForm R M) -> (f : M → M) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsOrthogonal : {R : Type u_20} -> {M : Type u_21} -> [CommRing R] -> [AddCommGroup M] -> [Module R M] -> (B : LinearMap.BilinForm R M) -> (f : M → M) -> Prop`

The type `R` is the commutative ring of scalars. The type `M` is the module on which everything lives. The instance arguments supply the commutative-ring structure on `R`, the abelian-group structure on `M`, and the `R`-module structure on `M`. The argument `B` is the bilinear form with respect to which orthogonality is measured; it is a bilinear map `M × M → R`. The argument `f` is the (set-theoretic) endomorphism of `M` being tested for orthogonality.

## Conventions

No special junk-value or boundary conventions are declared for this definition: the predicate is a universally quantified `Prop` that is well-formed for any `B` and any `f : M → M`, including non-linear maps; the statement is simply `False`-or-`True` depending on whether the equation holds for all pairs of vectors.

## Worked examples

- Claim: The identity map is orthogonal with respect to any bilinear form `B`, because `B (id x) (id y) = B x y` for all `x y`.

- Claim: If `f` satisfies `VTask.IsOrthogonal B f` and `g` also satisfies `VTask.IsOrthogonal B g`, then the composition `f ∘ g` satisfies `VTask.IsOrthogonal B (f ∘ g)`, since `B (f (g x)) (f (g y)) = B (g x) (g y) = B x y`.

- Claim: The zero map on a module over a ring where `0 ≠ 1` is generally *not* orthogonal with respect to a non-degenerate bilinear form, because `B 0 0 = 0` but `B x y` need not be zero for all `x y`.

- Claim: For a symmetric bilinear form `B` over a ring where `2` is left-regular, if `f` satisfies `B (f x) (f x) = B x x` for all `x`, then `VTask.IsOrthogonal B f` holds.

## Boundaries

- When `M` is the zero module the predicate holds vacuously for any `f` and any `B`, since there are no non-trivial pairs `(x, y)`.
- When `B` is the zero bilinear form, every map `f` is orthogonal, because both sides of the equation are `0`.
- The definition requires no linearity assumption on `f`; it is stated for any function `f : M → M`. Linearity must be checked separately if needed.
- The predicate is symmetric in its two quantified variables in the sense that `B (f x) (f y) = B x y` must hold for *all* ordered pairs `(x, y)`, not just unordered ones.

## Not to be confused with

- `LinearMap.IsAdjointPair B B f g`: asserts `B (f x) y = B x (g y)` for all `x y`, which coincides with `VTask.IsOrthogonal B f` only when `g` is the inverse of `f` (and in that special case is equivalent, as shown by `LinearEquiv.isAdjointPair_symm_iff`).
- Orthogonality of *vectors* or *subspaces* with respect to `B` (i.e., `B x y = 0`), which is a different use of the word "orthogonal" in the same bilinear-form context.
- `LinearMap.BilinForm.IsSymm`: the symmetry property of the form itself (`B x y = B y x`), not a property of a map acting on the form.