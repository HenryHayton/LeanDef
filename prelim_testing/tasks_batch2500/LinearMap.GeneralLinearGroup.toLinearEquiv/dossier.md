## Object

`VTask.toLinearEquiv` converts an element of the general linear group GL(R, M) — that is, an invertible R-linear endomorphism of M — into an R-linear equivalence (i.e., a linear isomorphism) from M to itself. In classical terms, it forgets that the invertible map lives in a group of units and instead presents it as a two-sided invertible linear map with explicitly named forward and inverse functions.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toLinearEquiv : {R : Type u_1} -> {M : Type u_2} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> (f : LinearMap.GeneralLinearGroup R M) -> M ≃ₗ[R] M
<!-- PINNED-SIGNATURE:END -->


`VTask.toLinearEquiv : {R : Type u_1} -> {M : Type u_2} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> (f : LinearMap.GeneralLinearGroup R M) -> M ≃ₗ[R] M`

The implicit argument `R` is the scalar ring (required to be a semiring) over which everything is linear. The implicit argument `M` is the module being acted upon. The semiring, additive commutative monoid, and module instance arguments supply the algebraic structure on `R` and `M`. The explicit argument `f` is the element of the general linear group: a linear endomorphism of `M` that is known to be invertible (i.e., it is a unit in the monoid of R-linear endomorphisms of M).

## Conventions

No special junk-value or boundary conventions are declared for this definition: the input is always a genuine unit in the endomorphism monoid, so the forward map is always exactly the underlying linear map of `f`, and the inverse function is always the underlying linear map of `f⁻¹`.

## Worked examples

- Claim: For any element `f` of `LinearMap.GeneralLinearGroup R M`, the linear equivalence `VTask.toLinearEquiv f` has its forward function equal to the function underlying `f.val`.

- Claim: For the identity element `1 : LinearMap.GeneralLinearGroup R M`, the linear equivalence `VTask.toLinearEquiv 1` acts as the identity on every `m : M`, i.e., `VTask.toLinearEquiv 1 m = m`.

- Claim: For composable units `f g : LinearMap.GeneralLinearGroup R M`, the linear equivalence `VTask.toLinearEquiv (f * g)` agrees with the composition of `VTask.toLinearEquiv f` and `VTask.toLinearEquiv g`, i.e., for any `m : M`, `VTask.toLinearEquiv (f * g) m = VTask.toLinearEquiv f (VTask.toLinearEquiv g m)`.

## Boundaries

- The definition is total on its stated domain: every element of the general linear group is by definition invertible, so no partial-function edge cases arise.
- The forward direction of the resulting `LinearEquiv` is definitionally equal to the underlying linear map of `f`; no coercion or wrapping changes the function.
- The inverse direction of the resulting `LinearEquiv` is definitionally the underlying linear map of `f⁻¹` (i.e., `f.inv`), the group-theoretic inverse in GL(R, M).
- The left and right inverse laws hold by the unit axioms of the general linear group: `f.inv * f.val = 1` and `f.val * f.inv = 1`.

## Not to be confused with

- `LinearMap.GeneralLinearGroup.toLinearMap` — extracts only the forward linear map from a GL element, without packaging an inverse; the result is a `LinearMap`, not a `LinearEquiv`.
- `LinearEquiv.ofLinear` — constructs a `LinearEquiv` from a pair of linear maps together with explicit proofs of left and right inverse; `VTask.toLinearEquiv` is specifically for GL elements and derives the inverse automatically from the group structure.
- `Module.End.isUnit_iff_bijective` — relates invertibility of a linear endomorphism to bijectivity, but does not itself produce a `LinearEquiv`.
