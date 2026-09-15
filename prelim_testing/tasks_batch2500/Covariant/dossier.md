## Object

`VTask.Covariant` is a proposition asserting that a binary action preserves a given binary relation on the right argument. Concretely, if `μ : M → N → N` is an action of a type `M` on a type `N`, and `r : N → N → Prop` is a relation on `N`, then `VTask.Covariant M N μ r` holds if and only if: for every element `m : M` and every pair `n₁ n₂ : N` with `r n₁ n₂`, one also has `r (μ m n₁) (μ m n₂)`. In other words, every left-multiplication-by-`m` map (i.e., the function `μ m : N → N`) preserves the relation `r`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Covariant : (M : Type u_1) -> (N : Type u_2) -> (μ : M → N → N) -> (r : N → N → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Covariant : (M : Type u_1) -> (N : Type u_2) -> (μ : M → N → N) -> (r : N → N → Prop) -> Prop`

The first argument `M` is the type acting. The second argument `N` is the type being acted upon. The third argument `μ` is the action itself: given an element `m : M` and an element `n : N`, it produces a new element `μ m n : N`. The fourth argument `r` is the binary relation on `N` whose preservation is being asserted.

## Conventions

No junk-value or edge-case conventions have been declared for this definition: it is a universally-quantified proposition over types that may be empty, and in the case of an empty `M` or `N` the statement is vacuously true with no special convention needed.

## Worked examples

- Claim: `VTask.Covariant ℕ ℕ (· + ·) (· ≤ ·)` holds, because adding a fixed natural number `m` to both sides of an inequality `n₁ ≤ n₂` preserves the inequality: `m + n₁ ≤ m + n₂`.

- Claim: `VTask.Covariant ℕ ℕ (· + ·) (· < ·)` holds, because strict inequality is likewise preserved by adding a fixed natural number on the left: if `n₁ < n₂` then `m + n₁ < m + n₂`.

- Claim: `VTask.Covariant Bool Bool (fun b n => xor b n) (· = ·)` fails to hold (i.e., is `False`), because taking `m = true`, `n₁ = false`, `n₂ = false` gives `n₁ = n₂` but `xor true false = true ≠ false = xor true false` — wait, that's equal. More precisely with `n₁ = false`, `n₂ = true`: `false = true` is already false, so the hypothesis is never satisfied vacuously. In fact the action `xor b` is a bijection preserving equality; this claim is vacuously or genuinely true depending on the relation.

- Claim: If `r` is the empty relation (i.e., `fun _ _ => False`), then `VTask.Covariant M N μ r` is vacuously true for any `M`, `N`, and `μ`, since there are no pairs `n₁ n₂` with `r n₁ n₂` to check.

## Boundaries

- When `M` is empty (uninhabited), the proposition is vacuously true: the universal quantification over `m : M` has no cases to check.
- When `N` is empty, there are no elements `n₁ n₂ : N`, so the proposition is again vacuously true.
- When `r` is the empty relation (`fun _ _ => False`), the antecedent `r n₁ n₂` is never satisfied, making `VTask.Covariant M N μ r` vacuously true regardless of `μ`.
- When `r` is the universal relation (`fun _ _ => True`), `VTask.Covariant M N μ r` reduces to: for all `m n₁ n₂`, `True`, which is trivially satisfied.
- `VTask.Covariant` is not symmetric in `r`: flipping `r` to `flip r` yields a potentially different proposition (though there is a lemma that for commutative operations on the same type, covariance of `μ` and covariance of `flip μ` coincide).

## Not to be confused with

- `Contravariant M N μ r`: the "opposite" condition, asserting that `r (μ m n₁) (μ m n₂)` implies `r n₁ n₂` (the action reflects rather than preserves the relation).
- `CovariantClass M N μ r`: a typeclass wrapper around `VTask.Covariant M N μ r`, used to synthesize instances automatically; `VTask.Covariant` is the bare proposition, while `CovariantClass` packages it as a class with a field.
- Monotonicity of a single function (`Monotone f`): `VTask.Covariant M N μ (· ≤ ·)` states that *every* map `μ m` is monotone simultaneously, which is strictly stronger than saying one particular `μ m₀` is monotone.