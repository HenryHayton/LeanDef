## VTask.supp

### Object

Given a valuation `v : R → Γ₀` from a commutative ring `R` to a linearly ordered commutative monoid with zero `Γ₀`, the **support** of `v` is the set of all elements `x ∈ R` for which `v(x) = 0`, equipped with the structure of an ideal of `R`. Intuitively, the support records precisely those ring elements that the valuation cannot distinguish from zero. For a valuation coming from a prime ideal (e.g., the p-adic valuation), the support is that prime ideal.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.supp : {R : Type u_3} -> {Γ₀ : Type u_4} -> [CommRing R] -> [LinearOrderedCommMonoidWithZero Γ₀] -> (v : Valuation R Γ₀) -> Ideal R
<!-- PINNED-SIGNATURE:END -->


The first implicit argument is the coefficient ring `R`, which must be a commutative ring. The second implicit argument `Γ₀` is the value group (more precisely, a linearly ordered commutative monoid with zero, playing the role of the ordered target of the valuation). The argument `v` is the valuation itself, a map `R → Γ₀` satisfying the standard valuation axioms. The function returns an ideal of `R`.

### Conventions

There are no junk-value conventions for this definition: it is total over all commutative rings and all linearly ordered commutative monoids with zero, and every valuation has a well-defined support ideal (which may be the zero ideal `{0}` if `v` is a faithful/injective-on-units valuation, or may be a nontrivial prime ideal).

### Worked examples

- Claim: An element `x : R` belongs to `VTask.supp v` if and only if `v x = 0`.

- Claim: For the trivial valuation on a field (where every nonzero element maps to 1 and 0 maps to 0), the support is the zero ideal `{0}`.

- Claim: If `s ∈ VTask.supp v` (i.e., `v s = 0`), then for any `a : R`, `v (a + s) = v a`. This follows because adding a support element does not change the valuation.

- Claim: The support of the valuation induced on the quotient `R ⧸ (VTask.supp v)` is the zero ideal of that quotient ring.

### Boundaries

- The zero element of `R` always belongs to `VTask.supp v`, since every valuation satisfies `v 0 = 0`. Thus the support is never empty.
- If `v` is the zero valuation (mapping everything to 0), then `VTask.supp v` is all of `R`, i.e., the unit ideal.
- The support `VTask.supp v` is always a prime ideal of `R`. This follows from the fact that `Γ₀` is an ordered monoid with zero: if `v(xy) = 0` then `v(x) * v(y) = 0`, so by the no-zero-divisors property of ordered monoids, `v(x) = 0` or `v(y) = 0`.
- For a field, the only ideals are `{0}` and the whole field, so the support of any valuation on a field is `{0}` (since the valuation must send units to nonzero values, and every nonzero element of a field is a unit).
- Pulling back a valuation along a ring homomorphism `f : S →+* R` yields a support that is exactly the preimage (comap) of the original support under `f`.

### Not to be confused with

- `Valuation.IsEquiv`: a relation comparing two valuations, not their vanishing sets.
- The kernel of a ring homomorphism `Ideal.ker`: while the support is the set where `v` vanishes, a valuation is not a ring homomorphism in general (it is multiplicative but not additive in the ring sense), so the support is not literally a ring-homomorphism kernel.
- `Valuation.integer`: the subring of elements where `v x ≤ 1`, which is a subring rather than an ideal, and captures "bounded" elements rather than vanishing ones.
