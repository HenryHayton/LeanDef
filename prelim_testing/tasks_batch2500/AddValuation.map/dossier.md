## Object

`VTask.map` transports an additive valuation on a ring `R` valued in an ordered monoid `Γ₀` to one valued in another ordered monoid `Γ'₀`, using a group homomorphism `f : Γ₀ →+ Γ'₀` that preserves both the ordering (monotonicity) and the distinguished top element `⊤`. Concretely, if `v : R → Γ₀` is an additive valuation, the result is the additive valuation `r ↦ f(v(r))`, i.e., the post-composition of `v` by `f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {R : Type u_3} -> {Γ₀ : Type u_4} -> {Γ'₀ : Type u_5} -> [Ring R] -> [LinearOrderedAddCommMonoidWithTop Γ₀] -> [LinearOrderedAddCommMonoidWithTop Γ'₀] -> (f : Γ₀ →+ Γ'₀) -> (ht : f ⊤ = ⊤) -> (hf : Monotone ⇑f) -> (v : AddValuation R Γ₀) -> AddValuation R Γ'₀
<!-- PINNED-SIGNATURE:END -->


The first argument `f` is an additive-group homomorphism from the source value group `Γ₀` to the target value group `Γ'₀`. The second argument `ht` is a proof that `f` sends the top element of `Γ₀` to the top element of `Γ'₀`, which is necessary because an additive valuation must map `0` in the ring to `⊤`. The third argument `hf` is a proof that `f` is monotone (order-preserving), which ensures the ultrametric (non-Archimedean) inequality is preserved. The fourth argument `v` is the additive valuation on `R` valued in `Γ₀` that is being transported.

## Conventions

There are no special junk-value or edge-case conventions for this definition: it is a total construction and every combination of valid inputs yields a well-formed additive valuation.

## Worked examples

- Claim: For the identity additive-group homomorphism `id : Γ₀ →+ Γ₀` (which trivially preserves `⊤` and is monotone), `VTask.map id h_top h_mono v` evaluates on any ring element `r` to the same value as `v r`.

- Claim: If `v` is an additive valuation on `R` with `v 1 = 0`, then `(VTask.map f ht hf v) 1 = f 0 = 0` in `Γ'₀`, because `f` is an additive-group homomorphism and hence `f 0 = 0`.

- Claim: If `v` is an additive valuation on `R` with `v 0 = ⊤`, then `(VTask.map f ht hf v) 0 = f ⊤ = ⊤` in `Γ'₀`, by the hypothesis `ht`.

- Claim: For ring elements `x, y : R`, `(VTask.map f ht hf v) (x * y) = (VTask.map f ht hf v) x + (VTask.map f ht hf v) y`, since both `v` and `f` are additive-group homomorphisms with respect to multiplication/addition.

## Boundaries

- The monotonicity condition `hf` on `f` is strictly required: without it, the ultrametric inequality `v(x + y) ≥ min(v x, v y)` could fail after applying `f`.
- The top-preservation condition `ht : f ⊤ = ⊤` is strictly required: without it, elements that map to `0` in the ring (which must have valuation `⊤`) might fail to have valuation `⊤` under the transported valuation.
- When `f` is the zero homomorphism (mapping everything to `0`), it does NOT satisfy `f ⊤ = ⊤` (since `⊤ ≠ 0` in a `LinearOrderedAddCommMonoidWithTop`), so such an `f` is excluded by the `ht` hypothesis.
- The construction is purely post-compositional: it changes the codomain of the valuation and does not alter the ring `R` or pull back along any ring map.

## Not to be confused with

- `AddValuation.comap`: pulls back an additive valuation along a *ring* homomorphism `S →+* R`, changing the domain ring rather than the value group.
- `AddValuation.onQuot`: restricts an additive valuation to a quotient ring, which also does not change the value group.
- `Valuation.map`: the multiplicative analogue, which transports a (multiplicative) valuation through a monoid homomorphism between multiplicative value groups; `VTask.map` is its additive counterpart.