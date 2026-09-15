## Object

`VTask.ofSet s` is the partial bijection on `α` that acts as the identity on the subset `s` and is undefined (returns `none`) on elements outside `s`. More precisely, it is a partial equivalence (`PEquiv`, written `α ≃. α`) whose forward and inverse maps both send an element `a` to `some a` when `a ∈ s`, and to `none` when `a ∉ s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofSet : {α : Type u} -> (s : Set α) -> [DecidablePred fun x => x ∈ s] -> α ≃. α
<!-- PINNED-SIGNATURE:END -->


`VTask.ofSet : {α : Type u} -> (s : Set α) -> [DecidablePred fun x => x ∈ s] -> α ≃. α`

The type parameter `α` is the ambient type on which the partial bijection lives. The argument `s` is the subset of `α` on which the partial bijection is defined to be the identity; elements in `s` are mapped to themselves, and elements outside `s` are mapped to `none` (i.e., are outside the domain and range of the partial bijection). The instance argument `[DecidablePred fun x => x ∈ s]` provides decidability of membership in `s`, which is required to evaluate the forward and inverse maps computationally.

## Conventions

There are no junk-value or boundary conventions to declare: the definition is total as a function from sets (with decidable membership) to partial equivalences, and the behaviour on all inputs is fully determined by whether elements belong to `s` or not.

## Worked examples

- Claim: For the set `s = {1, 2, 3} : Set ℕ`, the forward map of `VTask.ofSet s` sends `2` to `some 2`.
  ```lean
  example : (VTask.ofSet ({1, 2, 3} : Set ℕ)).toFun 2 = some 2 := by decide
  ```

- Claim: For the set `s = {1, 2, 3} : Set ℕ`, the forward map of `VTask.ofSet s` sends `5` to `none`.
  ```lean
  example : (VTask.ofSet ({1, 2, 3} : Set ℕ)).toFun 5 = none := by decide
  ```

- Claim: For the set `s = {1, 2, 3} : Set ℕ`, the inverse map of `VTask.ofSet s` sends `2` to `some 2`.
  ```lean
  example : (VTask.ofSet ({1, 2, 3} : Set ℕ)).invFun 2 = some 2 := by decide
  ```

- Claim: When `s = Set.univ`, the partial equivalence `VTask.ofSet s` behaves like the full identity: every element `a : α` is sent to `some a`.

- Claim: When `s = ∅`, the partial equivalence `VTask.ofSet s` is the everywhere-undefined map: every element is sent to `none`.

## Boundaries

- **Empty set**: When `s = ∅`, both the forward and inverse maps return `none` for every input. The resulting partial bijection has empty domain and range.
- **Universal set**: When `s = Set.univ`, every element is in `s`, so both maps always return `some a`. The result behaves like the total identity bijection (though it lives in `α ≃. α` rather than `α ≃ α`).
- **Singleton set**: `VTask.ofSet {a}` maps `a` to `some a` and everything else to `none`; it is the minimal nontrivial case.
- **Non-membership is symmetric**: The forward and inverse maps are identical functions, reflecting that the partial bijection is self-inverse (it is its own inverse as a `PEquiv`).

## Not to be confused with

- `Equiv.Set.ofEq` / restriction-of-a-bijection-to-a-subset constructions: those produce total bijections between a subset and another set, not a partial bijection on the whole type that is undefined outside the subset.
- `PEquiv.refl`: the everywhere-defined identity partial equivalence on `α`; `VTask.ofSet Set.univ` coincides with it, but `PEquiv.refl` is not parametrized by a subset.
- `Set.indicator`: a function `α → β` that is a given function on `s` and a default value outside; superficially similar but not a partial bijection and lives in a different category of objects.
