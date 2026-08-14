## VTask.piFinTwoEquiv

### Object

This is a canonical equivalence (bijection with explicit inverse) between the type of dependent functions out of the two-element type `Fin 2` into a family `α` and the binary product `α 0 × α 1`. Concretely, any function `f : (i : Fin 2) → α i` is completely determined by its two values `f 0` and `f 1`, and conversely any pair `(a, b)` with `a : α 0` and `b : α 1` assembles into such a function. The equivalence packages this identification as an `Equiv`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piFinTwoEquiv : (α : Fin 2 → Type u) -> ((i : Fin 2) → α i) ≃ α 0 × α 1
<!-- PINNED-SIGNATURE:END -->


`(α : Fin 2 → Type u) -> ((i : Fin 2) → α i) ≃ α 0 × α 1`

The sole argument `α` is the type family indexed by `Fin 2`; it specifies what type is assigned to each of the two indices `0` and `1`. The resulting `Equiv` witnesses that dependent functions from `Fin 2` into this family are in natural bijection with ordered pairs whose first component lives in `α 0` and second component lives in `α 1`.

### Conventions

No junk-value or out-of-domain conventions apply: the equivalence is total and well-defined for every type family `α : Fin 2 → Type u`, with no edge cases or degenerate inputs.

### Worked examples

- Claim: Applying `VTask.piFinTwoEquiv` (forward direction) to the function `![3, 7] : (i : Fin 2) → (fun _ => ℕ) i` yields the pair `(3, 7)`.
  ```lean
  example : VTask.piFinTwoEquiv (fun _ => ℕ) ![3, 7] = (3, 7) := by decide
  ```

- Claim: The inverse of `VTask.piFinTwoEquiv` applied to the pair `(true, false) : Bool × Bool` reconstructs the function sending `0` to `true` and `1` to `false`.
  ```lean
  example : (VTask.piFinTwoEquiv (fun _ => Bool)).symm (true, false) = ![true, false] := by decide
  ```

- Claim: For the non-dependent case `α := fun _ => ℕ`, the forward map satisfies `(VTask.piFinTwoEquiv (fun _ => ℕ) f).1 = f 0` and `(VTask.piFinTwoEquiv (fun _ => ℕ) f).2 = f 1` for any `f`.

- Claim: `VTask.piFinTwoEquiv` is an `Equiv`, so composing the forward and backward maps yields the identity on pairs: for any `p : α 0 × α 1`, `VTask.piFinTwoEquiv α ((VTask.piFinTwoEquiv α).symm p) = p`.

### Boundaries

- The type family `α` is arbitrary; in particular the two types `α 0` and `α 1` need not be the same, making this genuinely dependent.
- When `α` is the constant family `fun _ => β`, the equivalence specialises to the non-dependent isomorphism `(Fin 2 → β) ≃ β × β`; see `finTwoArrowEquiv` for that specialisation.
- There are no "empty" or "degenerate" edge cases to worry about: `Fin 2` always has exactly two elements, so the equivalence is always an isomorphism of inhabited types (assuming `α 0` and `α 1` are inhabited).
- The `Equiv` structure guarantees both directions are mutually inverse; no partial-function or partiality concerns arise.

### Not to be confused with

- `finTwoArrowEquiv`: the non-dependent version `(Fin 2 → β) ≃ β × β` where both components have the same type.
- `prodEquivPiFinTwo`: a closely related equivalence stated with two explicit type arguments `α β : Type u` rather than a single family `Fin 2 → Type u`.
- `Fin.cons` / `Matrix.cons` (the `![]` matrix notation): these are the building blocks for constructing tuples indexed by `Fin n`, but they are not equivalences themselves.
