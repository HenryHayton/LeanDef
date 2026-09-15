## Object

`VTask.mk0` constructs a unit (an invertible element) in the unit group `G₀ˣ` from a given non-zero element of a `GroupWithZero` `G₀`. Since every non-zero element of a `GroupWithZero` is invertible, this embedding is well-defined: it packages the element together with its multiplicative inverse and the two proofs that they multiply to one in each order.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk0 : {G₀ : Type u_3} -> [GroupWithZero G₀] -> (a : G₀) -> (ha : a ≠ 0) -> G₀ˣ
<!-- PINNED-SIGNATURE:END -->


`{G₀ : Type u_3} -> [GroupWithZero G₀] -> (a : G₀) -> (ha : a ≠ 0) -> G₀ˣ`

The implicit type argument `G₀` is the carrier type of the algebraic structure. The instance argument provides the `GroupWithZero` structure on `G₀`, which supplies multiplication, a zero element, and the fact that every non-zero element is invertible. The explicit argument `a` is the element of `G₀` to be promoted to a unit. The explicit argument `ha` is the proof that `a` is non-zero, which is necessary to guarantee that the multiplicative inverse of `a` exists within `G₀`.

## Conventions

When the non-zero proof `ha` is provided, the underlying value (the "val" coercion) of the resulting unit equals `a` exactly — no normalization or modification of the element is performed. The inverse component of the produced unit is exactly `a⁻¹` as computed in `G₀`.

## Worked examples

- Claim: For `a : G₀` with `ha : a ≠ 0`, coercing `VTask.mk0 a ha` back to `G₀` recovers `a`.

- Claim: In `ℚ`, `VTask.mk0 (3 : ℚ) (by norm_num)` is a unit whose underlying value is `3` and whose inverse is `3⁻¹ = 1/3`.

- Claim: For non-zero `a b : G₀`, the product of units `VTask.mk0 a ha * VTask.mk0 b hb` has underlying value `a * b` in `G₀`, since the coercion `G₀ˣ → G₀` is a monoid homomorphism.

- Claim: For non-zero `a : G₀`, the inverse unit `(VTask.mk0 a ha)⁻¹` has underlying value `a⁻¹` in `G₀`.

## Boundaries

- The element `a` must be non-zero; the argument `ha : a ≠ 0` is required and the function is simply not applicable (not defined) at zero — there is no junk value returned for zero.
- The function is total on its stated domain (non-zero elements of any `GroupWithZero`), so there are no further edge cases once `ha` is supplied.
- In a field (which is a `GroupWithZero`), every non-zero element can be embedded this way, so the image of `VTask.mk0` covers all of `G₀ˣ`.
- The underlying value of the resulting unit is definitionally equal to `a`, so `(VTask.mk0 a ha : G₀) = a` holds by reflexivity.

## Not to be confused with

- `Units.mk` (or `Units.mkOfMulEqOne`): constructs a unit from an element together with an explicitly supplied inverse and proof, without requiring a `GroupWithZero` structure; `VTask.mk0` automatically computes the inverse from the `GroupWithZero` instance.
- The coercion `G₀ˣ → G₀` ("forget the unit structure"): this goes in the opposite direction, extracting the underlying element from an already-known unit.
- `IsUnit.unit`: promotes an element satisfying the `IsUnit` predicate to `G₀ˣ`, but requires an `IsUnit` witness rather than a direct non-zero proof specific to `GroupWithZero`.