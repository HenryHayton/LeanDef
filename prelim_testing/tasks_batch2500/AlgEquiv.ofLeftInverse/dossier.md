## Object

`VTask.ofLeftInverse` constructs an algebra isomorphism (an invertible, ring- and scalar-compatible map) from an algebra `A` to the image of an algebra homomorphism `f : A →ₐ[R] B`, given explicit evidence that some function `g : B → A` is a left inverse of `f`. Concretely, it packages `f` (restricted to its range) as a two-sided invertible algebra map `A ≃ₐ[R] f.range`, using `g` to supply the inverse direction.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofLeftInverse : {R : Type u} -> {A : Type v} -> {B : Type w} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> {g : B → A} -> {f : A →ₐ[R] B} -> (h : Function.LeftInverse g ⇑f) -> A ≃ₐ[R] ↥f.range
<!-- PINNED-SIGNATURE:END -->


`VTask.ofLeftInverse : {R : Type u} -> {A : Type v} -> {B : Type w} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> {g : B → A} -> {f : A →ₐ[R] B} -> (h : Function.LeftInverse g ⇑f) -> A ≃ₐ[R] ↥f.range`

The commutative semiring `R` is the shared scalar base over which all algebra structures are defined. `A` and `B` are the source and target algebra types respectively, each equipped with their semiring and `R`-algebra structures. The implicit argument `g : B → A` is a bare function serving as the proposed inverse map from `B` back to `A`. The implicit argument `f : A →ₐ[R] B` is the algebra homomorphism whose range will become the codomain of the resulting isomorphism. The explicit argument `h : Function.LeftInverse g ⇑f` is a proof that `g` is a left inverse of `f`, meaning `g (f a) = a` for every `a : A`; this is the essential data that certifies injectivity and enables construction of the isomorphism.

## Conventions

The inverse map on the range subtype is formed by first embedding a range element into `B` via the canonical inclusion and then applying `g`; thus `g` need only be a left inverse of `f` (not a right inverse on all of `B`) for the construction to work correctly on `f.range`.

## Worked examples

- Claim: For `R = ℚ`, `A = ℚ`, `B = ℚ`, `f = AlgHom.id ℚ ℚ`, and `g = id`, `VTask.ofLeftInverse` (with the left-inverse proof for `id`) yields an algebra isomorphism `ℚ ≃ₐ[ℚ] (AlgHom.id ℚ ℚ).range` whose forward map sends each `q : ℚ` to `⟨q, ⋯⟩`.

- Claim: For the inclusion algebra homomorphism `f : ℤ →ₐ[ℤ] ℤ` equal to the identity, with left inverse `g = id`, the resulting isomorphism `VTask.ofLeftInverse h` satisfies `(VTask.ofLeftInverse h).toFun a = ⟨f a, ⋯⟩` for all `a`.

- Claim: If `f : A →ₐ[R] B` has a left inverse `g`, then `(VTask.ofLeftInverse h).symm ⟨f a, _⟩ = a` for every `a : A`, because `g (f a) = a` by hypothesis `h`.

## Boundaries

- `g` is required to be only a left inverse of `f` on all of `A` (i.e., `∀ a, g (f a) = a`); it need not be a right inverse on all of `B`, only on elements of `f.range`.
- On elements of `f.range`, `g` automatically acts as a right inverse: for any `b ∈ f.range`, writing `b = f a` we have `f (g b) = f (g (f a)) = f a = b`, so the right-inverse condition on the range is derived, not assumed.
- The construction is computable (in the sense that it does not use classical choice), making it a decidable alternative to the non-computable injectivity-based isomorphism.
- If `f` is not injective, no left inverse `g` can exist, so the hypothesis `h` is vacuously impossible in that case; the function is thus total over its stated domain.

## Not to be confused with

- `AlgEquiv.ofInjective`: constructs a similar range isomorphism from injectivity alone, but uses classical choice and is not computable.
- `AlgHom.rangeRestrict`: merely restricts the codomain of `f` to `f.range` without providing an inverse, yielding an `AlgHom` rather than an `AlgEquiv`.
- `Function.LeftInverse` vs `Function.RightInverse`: a left inverse `g ∘ f = id` does not in general make `f` a right inverse of `g` on all of `B`, only on `f.range`.