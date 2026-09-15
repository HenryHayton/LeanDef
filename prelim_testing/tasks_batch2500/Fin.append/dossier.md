## Object

`VTask.append` takes two finite tuples — one of length `m` and one of length `n` — and concatenates them into a single finite tuple of length `m + n`. Indices `0, 1, …, m−1` in the result are served by the first tuple, and indices `m, m+1, …, m+n−1` are served by the second tuple.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.append : {m n : ℕ} -> {α : Sort u_1} -> (a : Fin m → α) -> (b : Fin n → α) -> Fin (m + n) → α
<!-- PINNED-SIGNATURE:END -->


`VTask.append : {m n : ℕ} -> {α : Sort u_1} -> (a : Fin m → α) -> (b : Fin n → α) -> Fin (m + n) → α`

The implicit natural numbers `m` and `n` are the lengths of the two input tuples. The implicit type `α` is the element type, which may be any Sort (including `Prop`). The explicit argument `a` is the left (first) tuple, indexed by `Fin m`. The explicit argument `b` is the right (second) tuple, indexed by `Fin n`. The result is a function from `Fin (m + n)` to `α`.

## Conventions

There are no declared junk-value or edge conventions beyond the natural total behaviour inherited from the Lean/Mathlib function: the definition is genuinely total for all natural numbers `m` and `n`, including zero.

## Worked examples

- Claim: On an index `i : Fin (m + n)` with `i.val < m`, `VTask.append a b i` equals `a ⟨i.val, _⟩` — i.e., the result agrees with the left tuple on the first `m` positions.

- Claim: On an index `i : Fin (m + n)` with `i.val ≥ m`, `VTask.append a b i` equals `b ⟨i.val - m, _⟩` — i.e., the result agrees with the right tuple on the last `n` positions.

- Claim: Converting `VTask.append a b` to a list via `List.ofFn` gives `List.ofFn a ++ List.ofFn b`.

- Claim: Appending any tuple `u : Fin m → α` to the empty tuple `Fin.elim0 : Fin 0 → α` on the right gives back `u` (up to a cast on the index): `VTask.append u Fin.elim0 = u ∘ Fin.cast (Nat.add_zero _)`.

- Claim: `VTask.append` is injective (as a function `Fin (m+n) → α`) if and only if both component tuples are injective and no value appears in both.

## Boundaries

- When `m = 0`: the left tuple is empty (`Fin 0 → α`), and the result is just `b` (up to a `Fin` cast by `Nat.zero_add`). The `Fin.elim0` vacuous left tuple is a concrete special case.
- When `n = 0`: the right tuple is empty, and the result is just `a` (up to a `Fin` cast by `Nat.add_zero`). The `Fin.elim0` vacuous right tuple is a concrete special case.
- When both `m = 0` and `n = 0`: the result is the unique function from `Fin 0` to `α`, also expressible as `Fin.elim0`.
- The type `α` may be any `Sort`, including `Prop`, so this works for tuples of propositions as well as data types.

## Not to be confused with

- `Fin.addCases`: the dependent generalisation of this operation, where the return type may itself depend on the index; `VTask.append` is the non-dependent special case.
- `Fin.cons`: prepends a single element to a tuple of length `n`, producing one of length `n+1`; append concatenates two arbitrary-length tuples.
- `Fin.appendEquiv` / `Fin.appendHomeomorph`: these are (home)omorphism or equivalence structures on the *product* `(Fin m → α) × (Fin n → α)`, not the append function itself.