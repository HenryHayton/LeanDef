## Object

Given a natural number `n` and a chosen index `i : Fin (n + 1)`, `VTask.finSuccEquiv'` is the canonical bijection between `Fin (n + 1)` and `Option (Fin n)` that sends the distinguished element `i` to `none`, and every other element `j` (reached via `Fin.succAbove i`) to `some k` for the unique `k : Fin n` such that `i.succAbove k = j`. Informally: it is a "puncture at `i`" equivalence — remove the point `i` from `{0, …, n}` and rename the remaining `n` points as `{0, …, n-1}`, packaging this as an `Equiv`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finSuccEquiv' : {n : ℕ} -> (i : Fin (n + 1)) -> Fin (n + 1) ≃ Option (Fin n)
<!-- PINNED-SIGNATURE:END -->


VTask.finSuccEquiv' : {n : ℕ} -> (i : Fin (n + 1)) -> Fin (n + 1) ≃ Option (Fin n)

The implicit argument `n` is the natural number one less than the cardinality of the domain/codomain finite type. The explicit argument `i` is the special element of `Fin (n + 1)` that is designated as the "hole" — it is the unique element mapped to `none` under the forward direction of the equivalence.

## Conventions

There are no junk-value conventions to declare: the equivalence is a total bijection defined on all of `Fin (n + 1)`, and `i` ranges freely over that entire type.

## Worked examples

- Claim: For `i = 1 : Fin 3`, applying `VTask.finSuccEquiv'` to `i` itself yields `none`.

- Claim: For `i = 1 : Fin 3` and `j = 0 : Fin 2` (which satisfies `castSucc 0 < 1`), applying `VTask.finSuccEquiv'` to `castSucc 0 = 0` yields `some 0`.

- Claim: For `i = 0 : Fin (n+1)`, the equivalence `VTask.finSuccEquiv' 0` agrees with the standard `Fin.equivOptionFin` (a.k.a. `finSuccEquiv n`), sending `0` to `none` and `k.succ` to `some k`.

- Claim: The inverse of `VTask.finSuccEquiv' i` sends `none` back to `i`.

## Boundaries

- **At `i` itself**: `(VTask.finSuccEquiv' i) i = none` always, regardless of the value of `i`.
- **When `i = Fin.last n`**: The equivalence maps every `j ≠ Fin.last n` to `some (j.castLT ...)`, i.e., it is essentially the identity on the lower `n` elements viewed as `Option (Fin n)`.
- **When `i = 0`**: The equivalence coincides with the standard `finSuccEquiv n` (the equivalence `Fin (n+1) ≃ Option (Fin n)` that sends `0 ↦ none` and `k+1 ↦ some k`).
- **Elements below `i` (i.e., `castSucc m < i`)**: Mapped to `some m` via `castSucc` (the lower elements are not shifted).
- **Elements above `i` (i.e., `i ≤ castSucc m`)**: The element `m.succ` is mapped to `some m` (elements above the hole are shifted down by one).
- **Inverse direction**: `(VTask.finSuccEquiv' i).symm none = i`, `(VTask.finSuccEquiv' i).symm (some m) = Fin.castSucc m` if `castSucc m < i`, and `= m.succ` if `i ≤ castSucc m`.

## Not to be confused with

- `Fin.predAbove i`: A function `Fin (n+1) → Fin n` (not an equivalence) that maps both `i.castSucc` and `i.succ` to `i`, so it is not injective and cannot be an equivalence; `VTask.finSuccEquiv'` avoids this collapse by using `Option`.
- `finSuccEquiv n` (the zero-puncture variant): This is the special case of `VTask.finSuccEquiv'` with `i = 0`; it sends `0 ↦ none` and does not allow choosing an arbitrary puncture point.
- `Fin.succAbove i`: A function `Fin n → Fin (n+1)` that embeds `Fin n` into `Fin (n+1)` by skipping `i`; it is the inverse of the `some`-branch of `VTask.finSuccEquiv' i`, not the full equivalence.