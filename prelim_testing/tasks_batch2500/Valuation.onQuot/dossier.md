## VTask.onQuot

### Object

Given a valuation `v : R → Γ₀` on a commutative ring `R` and an ideal `J` contained in the support of `v` (i.e., every element of `J` maps to zero under `v`), `VTask.onQuot` produces a well-defined valuation on the quotient ring `R ⧸ J` that is compatible with `v` via the quotient map `R → R ⧸ J`. Concretely, if `x̄ ∈ R ⧸ J` is the class of `x ∈ R`, the new valuation sends `x̄` to `v(x)`. This is well-defined precisely because elements of `J` lie in the support of `v`, so any two representatives of the same class have the same valuation.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.onQuot : {R : Type u_1} -> {Γ₀ : Type u_2} -> [CommRing R] -> [LinearOrderedCommMonoidWithZero Γ₀] -> (v : Valuation R Γ₀) -> {J : Ideal R} -> (hJ : J ≤ v.supp) -> Valuation (R ⧸ J) Γ₀
<!-- PINNED-SIGNATURE:END -->


The first implicit argument `R` is the commutative ring being valued; the second implicit argument `Γ₀` is the linearly ordered commutative monoid with zero serving as the value group. The `CommRing R` and `LinearOrderedCommMonoidWithZero Γ₀` instances supply the required algebraic structure. The argument `v` is the original valuation on `R` whose values lie in `Γ₀`. The implicit argument `J` is the ideal of `R` being quotiented out; `hJ` is the hypothesis that `J` is contained in the support of `v` (i.e., every element of `J` is sent to zero by `v`). The result is a valuation on the quotient ring `R ⧸ J` taking values in `Γ₀`.

### Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total construction, well-typed for any ideal `J` satisfying the stated containment condition `J ≤ v.supp`, and the output is always a fully valid `Valuation`.

### Worked Examples

- Claim: If `J` is the zero ideal of `R`, then `VTask.onQuot v (le_refl _)` evaluated at the class of `x` equals `v x`, since the zero ideal is always contained in any support and the quotient `R ⧸ (0)` is canonically isomorphic to `R`.

- Claim: If `J = v.supp` (the full support of `v`), then `VTask.onQuot v (le_refl _)` is a valuation on `R ⧸ v.supp` that is everywhere nonzero on nonzero elements — i.e., the quotient valuation descends to an order-embedding on `R ⧸ v.supp`, reflecting the fact that the support is precisely the kernel of the valuation map.

- Claim: For any `x : R` and any ideal `J ≤ v.supp`, applying `VTask.onQuot v hJ` to the image of `x` under the quotient map gives the same value as `v x`.

- Claim: The support of `VTask.onQuot v hJ` (as a valuation on `R ⧸ J`) equals the image of `v.supp` in `R ⧸ J`, i.e., it is the quotient `v.supp ⧸ J`.

### Boundaries

- When `J = v.supp`, the resulting valuation `VTask.onQuot v hJ` has trivial support (the zero ideal of `R ⧸ v.supp`), making the quotient ring a domain with respect to the valuation.
- When `J = 0` (the zero ideal), the hypothesis `hJ : 0 ≤ v.supp` holds automatically (the zero ideal is contained in every ideal), and the quotient valuation is essentially `v` itself transported through the canonical isomorphism.
- The construction requires `J ≤ v.supp` strictly; if `J` contained an element outside the support of `v`, the valuation on the quotient would not be well-defined.
- If `v` is the trivial (zero) valuation (support = all of `R`), then any ideal `J` satisfies `J ≤ v.supp`, and the resulting quotient valuation is again trivial.

### Not to be confused with

- `Valuation.onQuotVal`: The underlying function (not packaged as a `Valuation` structure) that `VTask.onQuot` uses internally; `VTask.onQuot` produces the full `Valuation` bundled with all the required axioms.
- `Ideal.Quotient.lift`: The general ring-homomorphism lifting to a quotient ring, which requires the ideal to be in the kernel of the map; `VTask.onQuot` is the specialization of this idea to valuations with the weaker condition `J ≤ supp v`.
- `Valuation.comap`: The pullback of a valuation along a ring homomorphism, which goes in the opposite direction (pulling back rather than pushing forward to a quotient).