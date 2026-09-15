## Object

`VTask.optionCongr` constructs, from a bijection `e : α ≃ β` between two types, a corresponding bijection `Option α ≃ Option β`. The bijection acts pointwise: `none` maps to `none`, and `some a` maps to `some (e a)`. The result is a genuine equivalence (with explicit inverse and proofs of left- and right-inverse), not merely a function.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.optionCongr : {α : Type u_1} -> {β : Type u_2} -> (e : α ≃ β) -> Option α ≃ Option β
<!-- PINNED-SIGNATURE:END -->


`VTask.optionCongr : {α : Type u_1} -> {β : Type u_2} -> (e : α ≃ β) -> Option α ≃ Option β`

The type arguments `α` and `β` are implicit and inferred from context. The single explicit argument `e` is the input equivalence between the underlying types whose elements are being wrapped; the result is the lifted equivalence between the `Option`-wrapped types.

## Conventions

The `none` element of `Option α` is treated as a fixed point: both the forward and backward directions of the resulting equivalence send `none` to `none`. There is no junk value regime since the construction is total and well-defined for every equivalence `e`.

## Worked examples

- Claim: For the identity equivalence on a type `α`, `VTask.optionCongr (Equiv.refl α)` equals `Equiv.refl (Option α)` (the construction respects identity).

- Claim: For any equivalence `e : α ≃ β`, the forward map of `VTask.optionCongr e` sends `none` to `none`.

- Claim: For any equivalence `e : α ≃ β` and any `a : α`, the forward map of `VTask.optionCongr e` sends `some a` to `some (e a)`.

- Claim: For any equivalence `e : α ≃ β`, the symmetry of `VTask.optionCongr e` equals `VTask.optionCongr e.symm` (the construction commutes with taking inverses).

- Claim: For equivalences `e₁ : α ≃ β` and `e₂ : β ≃ γ`, `VTask.optionCongr (e₁.trans e₂)` equals `(VTask.optionCongr e₁).trans (VTask.optionCongr e₂)` (the construction is functorial under composition).

- Claim: The map `e ↦ VTask.optionCongr e` is injective: distinct equivalences yield distinct lifted equivalences.

## Boundaries

- When `α = β` and `e` is a permutation (i.e., `e : Perm α`), `VTask.optionCongr e` is a permutation of `Option α`. In this setting, the sign of the lifted permutation equals the sign of the original permutation.
- When `e` is a transposition swapping two elements `x` and `y` of `α`, `VTask.optionCongr e` is the transposition that swaps `some x` and `some y` in `Option α`, leaving `none` fixed.
- The construction is defined for any types `α` and `β` in any universes; there is no restriction to finite or decidable types.

## Not to be confused with

- `EquivFunctor.mapEquiv Option e` — this is universe-monomorphic (requires `α` and `β` to be in the same universe); `VTask.optionCongr` is the universe-polymorphic generalisation and they coincide when universes match.
- `Option.map` — this is the underlying function from `Option α → Option β`, not a bundled equivalence; `VTask.optionCongr` packages both directions and their proofs together.
- `Equiv.removeNone` — the inverse operation, which strips the `Option` wrapper from an equivalence `Option α ≃ Option β` (that necessarily fixes `none`) to recover an equivalence `α ≃ β`.