## Object

`VTask.finSumNatEquiv n` is a canonical bijection between the disjoint-union type `Fin n ⊕ ℕ` and the natural numbers `ℕ`. It works by placing the finite block `{0, 1, …, n−1}` at the bottom, laid out in order via the `inl` summand, and then shifting the infinite `ℕ`-block (the `inr` summand) upward by `n`.

Forward direction:
- `inl a` (where `a : Fin n`) maps to the natural number `a` (the underlying value of the fin).
- `inr a` (where `a : ℕ`) maps to `n + a`.

Inverse direction:
- A natural number `i < n` maps back to `inl ⟨i, _⟩`.
- A natural number `i ≥ n` maps back to `inr (i − n)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finSumNatEquiv : (n : ℕ) -> Fin n ⊕ ℕ ≃ ℕ
<!-- PINNED-SIGNATURE:END -->


The single argument `n : ℕ` is the size of the finite block that occupies the initial segment `{0, …, n−1}` of `ℕ` in the equivalence.

## Conventions

No special junk-value or boundary conventions are declared for this definition: the equivalence is total and well-behaved at every natural number `n`, including `n = 0`, where the `Fin 0` summand is empty and the equivalence reduces to the identity on the `inr ℕ` summand.

## Worked examples

- Claim: With `n = 3`, the left summand element `inl ⟨2, _⟩` maps to `2`.
- Claim: With `n = 3`, the right summand element `inr 0` maps to `3 + 0 = 3`.
- Claim: With `n = 3`, the right summand element `inr 5` maps to `3 + 5 = 8`.
- Claim: With `n = 0`, the right summand element `inr 7` maps to `0 + 7 = 7`, so `VTask.finSumNatEquiv 0` sends `inr 7` to `7`.
- Claim: `(VTask.finSumNatEquiv 3).symm 1 = Sum.inl ⟨1, by omega⟩` — the inverse sends a number below `n` back to the `inl` branch.
- Claim: `(VTask.finSumNatEquiv 3).symm 5 = Sum.inr 2` — the inverse sends `5` (which is `≥ 3`) to `inr (5 − 3) = inr 2`.

## Boundaries

- When `n = 0`, the `Fin 0` part is the empty type, contributing no elements. The `inr` summand spans all of `ℕ`, and the equivalence is the identity on those elements: `inr a ↦ 0 + a = a`.
- When `i = n` exactly, `i` is the first element **not** in the finite block; the inverse sends it to `inr 0`.
- The forward map is injective by construction: the two branches cover disjoint ranges (`{0,…,n−1}` and `{n, n+1,…}`), so there are no collisions.

## Not to be confused with

- `Fin.equivSubtype` — an equivalence between `Fin n` and the subtype `{i : ℕ // i < n}`; works only within the finite range, not involving an extra `ℕ` summand.
- `Equiv.sumComm` — swaps the two summands of a coproduct `A ⊕ B ≃ B ⊕ A`; does not collapse to a single `ℕ`.
- `finProdNatEquiv` (or similar) — a bijection between `Fin n × ℕ` and `ℕ` using a product rather than a coproduct/sum type.