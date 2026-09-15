## VTask.nonZeroSMulDivisors

### Object

Given a monoid-with-zero `M₀` acting on a type `M` that has a distinguished zero element, the **non-zero smul-divisors** (also called `M`-regular elements of `M₀`) form the collection of all scalars `r ∈ M₀` such that whenever `r • m = 0` for some `m : M`, we can conclude `m = 0`. In other words, an element is a non-zero smul-divisor precisely when the scalar multiplication map `m ↦ r • m` sends nothing non-zero to zero. This collection is closed under multiplication and contains the identity, so it is naturally a submonoid of `M₀`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nonZeroSMulDivisors : (M₀ : Type u_1) -> [MonoidWithZero M₀] -> (M : Type u_2) -> [Zero M] -> [MulAction M₀ M] -> Submonoid M₀
<!-- PINNED-SIGNATURE:END -->


The first explicit argument `M₀` is the scalar type — a monoid with zero — whose elements are tested for the non-zero smul-divisor property. The second explicit argument `M` is the module/action type, which only needs to carry a zero element and a multiplicative `M₀`-action; it is the type through which the "smul by `r` kills nothing non-zero" condition is stated. The instance arguments supply, respectively, the monoid-with-zero structure on `M₀`, the zero element of `M`, and the `M₀`-action on `M`.

### Conventions

There are no junk-value or boundary conventions to declare: the definition is total (both `M₀` and `M` can be arbitrary, including trivial or degenerate types), and the submonoid is well-defined in every case.

### Worked examples

- Claim: Every element of `VTask.nonZeroSMulDivisors ℤ ℤ` satisfies the property that smulling by it cannot send a nonzero integer to zero — equivalently, the non-zero smul-divisors of `ℤ` acting on itself are exactly the left non-zero-divisors of `ℤ`.

- Claim: The identity element `1 : M₀` always belongs to `VTask.nonZeroSMulDivisors M₀ M`, because `1 • m = m` by the axiom of a monoid action, so `1 • m = 0` implies `m = 0`.

- Claim: If `r₁` and `r₂` both belong to `VTask.nonZeroSMulDivisors M₀ M`, then so does their product `r₁ * r₂`, since the submonoid is closed under multiplication.

- Claim: When `M₀` acts on itself by left multiplication (the `MulAction` from the monoid structure), `VTask.nonZeroSMulDivisors M₀ M₀` coincides with the submonoid of left non-zero-divisors of `M₀`.

### Boundaries

- When `M` is the trivial type (or every element of `M` is `0`), every element of `M₀` vacuously satisfies `∀ m, r • m = 0 → m = 0`, so `VTask.nonZeroSMulDivisors M₀ M` is all of `M₀` (as a submonoid).
- When `M₀` is the zero ring (i.e., `0 = 1`), the unique element `0 = 1` acts as identity, so the submonoid is still nonempty (it contains `1`).
- An element `r` belongs to `VTask.nonZeroSMulDivisors M₀ M` if and only if the scalar multiplication map by `r` is injective on `M` viewed as a type-with-zero (injectivity at zero is automatic; the condition rules out non-zero elements mapping to zero).
- The condition is one-sided: it says `r • m = 0 → m = 0`, not `m • r = 0 → m = 0`, so membership depends on the specific action of `M₀` on `M` and is not symmetric.

### Not to be confused with

- **`nonZeroDivisors M₀`** (written `M₀⁰`): the submonoid of elements `r` such that `r * m = 0 → m = 0` for multiplication in `M₀` itself; this is the special case where `M = M₀` with left-multiplication action, and `VTask.nonZeroSMulDivisors M₀ M₀` equals this.
- **`nonZeroDivisorsLeft M₀`**: the submonoid of left non-zero-divisors of `M₀`; by a lemma in Mathlib, this equals `VTask.nonZeroSMulDivisors M₀ M₀`, but the two definitions present the condition differently.
- **`IsSMulRegular M r`**: a predicate (not a submonoid) asserting that the smul-by-`r` map is injective on all of `M`; membership in `VTask.nonZeroSMulDivisors M₀ M` and `IsSMulRegular M m₀` coincide when `M` is an additive group with a distributive action.
