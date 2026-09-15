## Object

Given a monoid with zero `M₀`, `VTask.nonZeroDivisorsLeft M₀` is the submonoid of `M₀` consisting of all elements that are not left zero divisors — that is, every element `x` such that `x * y = 0` implies `y = 0` for all `y` in `M₀`. In other words, left-multiplication by any member of this submonoid is injective on `M₀` as a function into `M₀`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nonZeroDivisorsLeft : (M₀ : Type u_1) -> [MonoidWithZero M₀] -> Submonoid M₀
<!-- PINNED-SIGNATURE:END -->


`VTask.nonZeroDivisorsLeft : (M₀ : Type u_1) -> [MonoidWithZero M₀] -> Submonoid M₀`

The first argument is the type `M₀`, which must carry the structure of a monoid with zero (supplied by the instance argument). The result is a submonoid of `M₀`.

## Conventions

The element `0` is never a member of this submonoid, because in any nontrivial setting `0 * y = 0` does not force `y = 0`; this is guaranteed unconditionally. There are no junk-value conventions for this definition beyond this structural exclusion of zero.

## Worked examples

- Claim: For a commutative monoid with zero that is also a cancellative commutative monoid with zero (such as `ℤ`), `VTask.nonZeroDivisorsLeft` coincides with the usual two-sided non-zero-divisors submonoid.

- Claim: The integer `2 : ℤ` belongs to `VTask.nonZeroDivisorsLeft ℤ`, since `2 * y = 0` in `ℤ` implies `y = 0`.

- Claim: The element `0 : ℤ` does not belong to `VTask.nonZeroDivisorsLeft ℤ`.

- Claim: In a ring `R` satisfying the left Ore condition with a submonoid `S ≤ VTask.nonZeroDivisorsLeft R`, the numerator map `R → R[S⁻¹]` is injective.

## Boundaries

- The element `0` is always excluded: `0 ∉ VTask.nonZeroDivisorsLeft M₀` holds unconditionally, because taking `y = 1` (or any nonzero element) shows `0 * y = 0` without forcing `y = 0`.
- The element `1` is always a member, as it is in any submonoid containing the monoid identity.
- In a commutative (or more generally, in any monoid with zero where left and right zero divisor notions coincide), this submonoid equals the two-sided non-zero-divisors submonoid.
- In an Artinian ring (viewed through its opposite), this submonoid coincides with the submonoid of units.
- An element belongs to `VTask.nonZeroDivisorsLeft M₀` if and only if it is left-regular (i.e., left-multiplication by it is injective).

## Not to be confused with

- `nonZeroDivisorsRight M₀`: the analogous submonoid of right non-zero-divisors; coincides with `VTask.nonZeroDivisorsLeft M₀` when `M₀` is commutative, but may differ in non-commutative settings.
- `nonZeroDivisors M₀` (written `M₀⁰`): the two-sided non-zero-divisors submonoid, which requires both the left and right cancellation conditions simultaneously; an element belongs to it if and only if it belongs to both `VTask.nonZeroDivisorsLeft M₀` and `nonZeroDivisorsRight M₀`.
- `IsUnit.submonoid M₀`: the submonoid of invertible elements, which is contained in (and in Artinian rings equals) `VTask.nonZeroDivisorsLeft M₀`, but in general is strictly smaller.