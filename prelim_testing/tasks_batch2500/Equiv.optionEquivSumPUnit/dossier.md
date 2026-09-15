## Object

`VTask.optionEquivSumPUnit α` is a canonical type equivalence (a bijection with explicit inverse, witnessing isomorphism of types) between `Option α` and the coproduct `α ⊕ PUnit`. It identifies `some a` with `Sum.inl a` (the "left" injection of a concrete value) and `none` with `Sum.inr PUnit.unit` (the unique element of the "right" unit summand).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.optionEquivSumPUnit : (α : Type w) -> Option α ≃ α ⊕ PUnit.{v + 1}
<!-- PINNED-SIGNATURE:END -->


`VTask.optionEquivSumPUnit : (α : Type w) -> Option α ≃ α ⊕ PUnit.{v + 1}`

The single argument `α` is the type whose optional values are being reclassified. The universe level `w` is the universe of `α`, while `v` is an independent universe level controlling the size of `PUnit`; in the most common use both are the same universe.

## Conventions

No special junk-value or boundary conventions are declared for this definition: the equivalence is total and defined on all elements of both sides, and no exceptional output is needed for any input.

## Worked examples

- Claim: Applying `VTask.optionEquivSumPUnit Nat` to `none` yields `Sum.inr PUnit.unit`.
  ```lean
  example : VTask.optionEquivSumPUnit Nat none = Sum.inr PUnit.unit := by rfl
  ```

- Claim: Applying `VTask.optionEquivSumPUnit Nat` to `some 5` yields `Sum.inl 5`.
  ```lean
  example : VTask.optionEquivSumPUnit Nat (some 5) = Sum.inl 5 := by rfl
  ```

- Claim: The inverse of `VTask.optionEquivSumPUnit Nat` sends `Sum.inl 42` back to `some 42`.
  ```lean
  example : (VTask.optionEquivSumPUnit Nat).symm (Sum.inl 42) = some 42 := by rfl
  ```

- Claim: The inverse of `VTask.optionEquivSumPUnit Nat` sends `Sum.inr PUnit.unit` back to `none`.
  ```lean
  example : (VTask.optionEquivSumPUnit Nat).symm (Sum.inr PUnit.unit) = none := by rfl
  ```

## Boundaries

- The only "missing" value in `Option α` is `none`, and it is mapped to the unique element of the `PUnit` summand; there are no other edge cases.
- Universe polymorphism: `PUnit.{v + 1}` is the `PUnit` in universe `v + 1`. When `α : Type w` and one writes `α ⊕ PUnit`, the universe of `PUnit` must be made explicit if `v ≠ w`; the equivalence is well-formed for any consistent choice.
- The equivalence is fully invertible with no partiality on either side.

## Not to be confused with

- `Option α ≃ α ⊕ Unit`: a superficially identical statement where `Unit` (in `Type 0`) is used instead of the universe-polymorphic `PUnit`; these coincide only when the universe level `v = 0`.
- `Sum.comm`, `Sum.assoc`: equivalences that permute or reassociate sum types without involving `Option` or `PUnit`.
- `Equiv.sumComm`: swaps the two summands, mapping `α ⊕ PUnit` to `PUnit ⊕ α`, which is related but distinct from this equivalence.