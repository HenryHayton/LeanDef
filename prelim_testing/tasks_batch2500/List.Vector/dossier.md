## Object

`VTask.Vector α n` is the type of finite lists of elements of type `α` that have exactly `n` elements. It bundles together a list and a proof that the list has the stated length, so every term of this type is simultaneously a list and a certificate of its own length. Mathematically it can be thought of as the set of all sequences of length `n` drawn from `α`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Vector : (α : Type u) -> (n : ℕ) -> Type u
<!-- PINNED-SIGNATURE:END -->


`VTask.Vector : (α : Type u) -> (n : ℕ) -> Type u`

The first argument `α` is the element type — the type from which the entries of the sequence are drawn. The second argument `n` is the required length — the natural number that every term of the resulting type is guaranteed to have as its list-length.

## Conventions

There are no junk-value or edge-case conventions to declare: the definition is a subtype of lists constrained by a propositional equality, so every term is genuinely a list of the exact stated length; there is no out-of-range or undefined behaviour.

## Worked examples

- Claim: The empty list, together with the proof that its length is 0, is a term of `VTask.Vector ℕ 0`.
  ```lean
  example : VTask.Vector ℕ 0 := ⟨[], rfl⟩
  ```

- Claim: The list `[1, 2, 3]`, together with the proof that its length is 3, is a term of `VTask.Vector ℕ 3`.
  ```lean
  example : VTask.Vector ℕ 3 := ⟨[1, 2, 3], rfl⟩
  ```

- Claim: For any type `α`, `VTask.Vector α 0` is inhabited (by the empty-list witness).
  ```lean
  example (α : Type*) : VTask.Vector α 0 := ⟨[], rfl⟩
  ```

- Claim: Two terms of `VTask.Vector ℕ 2` are equal when their underlying lists agree.
  ```lean
  example : (⟨[1, 2], rfl⟩ : VTask.Vector ℕ 2) = ⟨[1, 2], rfl⟩ := rfl
  ```

## Boundaries

- When `n = 0` the only possible underlying list is `[]`, so `VTask.Vector α 0` has exactly one term (up to proof irrelevance).
- When `α` is empty (e.g., `α = Empty`), `VTask.Vector α n` is itself empty for every `n ≥ 1`, and has exactly one term for `n = 0`.
- The length constraint is strict: a list of length `k ≠ n` cannot be a term of `VTask.Vector α n`; the membership proof rules it out at the type level.
- The type is universe-polymorphic: if `α : Type u` then `VTask.Vector α n : Type u`, so no universe bump occurs.

## Not to be confused with

- `Vector α n` (root namespace): an *array*-backed length-indexed type, intended for programming and verification, as opposed to the list-backed mathematical sequence type.
- `Fin n → α`: a function-type encoding of length-`n` sequences, which lacks the list structure and does not directly carry order-of-iteration semantics.
- `List α`: an unrestricted list with no length constraint; it does not track its length in the type.