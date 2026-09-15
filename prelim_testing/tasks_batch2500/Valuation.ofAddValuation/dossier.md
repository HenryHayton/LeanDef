## VTask.ofAddValuation

### Object

A canonical, order-and-ring-compatible bijection (an equivalence of types) between additive valuations on a ring `R` taking values in `(Additive Γ₀)ᵒᵈ` and multiplicative valuations on `R` taking values in `Γ₀`. Concretely, an additive valuation measures the "size" of ring elements using an additively-written ordered monoid, whereas a multiplicative valuation uses a multiplicatively-written one; this equivalence converts between the two presentations by unwinding the `Additive`, `OrderDual` (applied twice), and `toMul`/`ofMul` wrappers so that both valuations encode exactly the same mathematical data.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofAddValuation : {R : Type u_3} -> {Γ₀ : Type u_5} -> [Ring R] -> [LinearOrderedCommMonoidWithZero Γ₀] -> AddValuation R (Additive Γ₀)ᵒᵈ ≃ Valuation R Γ₀
<!-- PINNED-SIGNATURE:END -->


`{R : Type u_3} -> {Γ₀ : Type u_5} -> [Ring R] -> [LinearOrderedCommMonoidWithZero Γ₀] -> AddValuation R (Additive Γ₀)ᵒᵈ ≃ Valuation R Γ₀`

The implicit type `R` is the ring being valued. The implicit type `Γ₀` is the target ordered monoid for the multiplicative side; the additive side correspondingly uses `(Additive Γ₀)ᵒᵈ`, i.e., the additive notation for `Γ₀` with the order dualized twice (so the order is the same as on `Γ₀`). The `Ring R` instance gives `R` its ring structure. The `LinearOrderedCommMonoidWithZero Γ₀` instance supplies the ordering and multiplicative monoidal structure on the value group.

### Conventions

No special junk-value or boundary conventions are declared: the equivalence is a total bijection defined on all additive valuations of the specified type, and every element of the domain maps to a well-defined multiplicative valuation with no degenerate cases.

### Worked examples

- Claim: Applying `VTask.ofAddValuation` to a round-tripped valuation recovers the original multiplicative valuation. That is, for any `v : Valuation R Γ₀`, `VTask.ofAddValuation (VTask.toAddValuation v) = v`.

- Claim: The inverse of `VTask.ofAddValuation` is exactly `VTask.toAddValuation`. That is, `VTask.ofAddValuation.symm = VTask.toAddValuation` (as an equivalence).

- Claim: For any `v : AddValuation R (Additive Γ₀)ᵒᵈ` and any `r : R`, evaluating `VTask.ofAddValuation v` at `r` yields `Additive.toMul (OrderDual.ofDual (v r))`.

### Boundaries

- The domain is the entire type `AddValuation R (Additive Γ₀)ᵒᵈ`; there are no excluded inputs.
- The equivalence is an `≃` (a definitional bijection with explicit inverse), not merely a function, so both `VTask.ofAddValuation` and its inverse `VTask.ofAddValuation.symm` are available and satisfy the round-trip identities by construction.
- The double `OrderDual` wrapping on the additive side means the order on `(Additive Γ₀)ᵒᵈ` is canonically identified with the order on `Γ₀`, so no order-reversal occurs across the equivalence.
- The zero element of `Γ₀` (playing the role of the value at zero in a valuation) is preserved correctly by the translation between additive and multiplicative notation.

### Not to be confused with

- `VTask.toAddValuation`: the inverse direction of the same equivalence, converting a multiplicative `Valuation R Γ₀` into an `AddValuation R (Additive Γ₀)ᵒᵈ`.
- `AddValuation.toValuation`: an earlier, lower-level conversion step that may not handle all the `Additive`/`OrderDual` bookkeeping that `VTask.ofAddValuation` resolves.
- `Valuation` itself: the target type of the equivalence, not the equivalence map; do not confuse the type with the conversion function.