## Object

`VTask.piUnique` is a canonical equivalence (bijection) between the type of dependent functions `(i : α) → β i` and the single fiber `β default`, valid whenever the domain type `α` has a unique element. Since every element of `α` equals `default`, a dependent function on `α` is completely determined by its value at `default`, and this equivalence makes that observation into a precise isomorphism.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piUnique : {α : Sort u} -> [Unique α] -> (β : α → Sort u_1) -> ((i : α) → β i) ≃ β default
<!-- PINNED-SIGNATURE:END -->


`VTask.piUnique : {α : Sort u} -> [Unique α] -> (β : α → Sort u_1) -> ((i : α) → β i) ≃ β default`

The implicit argument `α` is the domain sort, which is required to have a unique element via the `[Unique α]` instance. The explicit argument `β` is the dependent type family indexed by `α`; it assigns to each element of `α` a type in some universe. The result is an `Equiv` (bundled equivalence) between the dependent-function type `∀ i, β i` and the single fiber `β default`, where `default` is the unique element of `α`.

## Conventions

The forward direction of the equivalence evaluates a dependent function at `default`. The inverse direction reconstructs a dependent function from a single value in `β default` by using the fact that every element of `α` equals `default`, extending the value uniformly.

## Worked examples

- Claim: Applying `VTask.piUnique` to the constant family `β := fun _ => ℕ`, the forward map sends the function `fun _ => 42` to `42`.

- Claim: The inverse of `VTask.piUnique (β := fun _ => Bool)` applied to `true` is the constant function sending the unique element to `true`.

- Claim: For any `f : (i : Fin 1) → (fun _ => ℕ) i`, the round-trip `(VTask.piUnique _).symm ((VTask.piUnique _) f)` equals `f`.

- Claim: `(VTask.piUnique (α := Unit) (β := fun _ => ℤ)).toFun (fun _ => -3) = -3`
  ```lean
  example : (VTask.piUnique (α := Unit) (β := fun _ => ℤ)).toFun (fun _ => -3) = -3 := rfl
  ```

- Claim: `(VTask.piUnique (α := Unit) (β := fun _ => ℕ)).invFun 7 = fun _ => 7`
  ```lean
  example : (VTask.piUnique (α := Unit) (β := fun _ => ℕ)).invFun 7 = fun _ => 7 := rfl
  ```

## Boundaries

- When `α` has exactly one element (the only case allowed), the equivalence is an isomorphism between the entire pi-type and a single type; there are no degenerate or empty cases to handle on the domain side.
- When `β` is a constant family `β := fun _ => B`, the equivalence specialises to the classical fact `(α → B) ≃ B` for a one-element domain.
- The equivalence is universe-polymorphic: both `α` and the values `β i` may live in any universe, so the construction applies uniformly to types, propositions, and higher sorts alike.
- Because `Unique` provides both `Inhabited` (a designated element `default`) and the proof that all elements are equal to it, no additional hypotheses are needed beyond the `[Unique α]` instance.

## Not to be confused with

- `Equiv.funUnique`: the non-dependent version, which gives `(α → β) ≃ β` for a unique domain `α`; `VTask.piUnique` handles the fully dependent case.
- `Equiv.piCongrLeft` / `Equiv.piCongrRight`: equivalences that reindex or re-fiber a pi-type, but do not collapse the entire domain to a point.
- `Unique.elim` / `uniqueElim`: the elimination principle for `Unique`, which is the building block for the inverse map inside `VTask.piUnique`, but is not itself an `Equiv`.