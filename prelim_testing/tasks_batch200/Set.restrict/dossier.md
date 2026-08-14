## Object

`VTask.restrict s f` is the restriction of a dependent function `f : (a : α) → π a` to a subset `s` of its domain. The result is a new dependent function that accepts only elements of `s` (represented as subtypes) and returns the same values as `f` on those elements.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restrict : {α : Type u_1} -> {π : α → Type u_6} -> (s : Set α) -> (f : (a : α) → π a) -> (a : ↑s) -> π ↑a
<!-- PINNED-SIGNATURE:END -->


`VTask.restrict : {α : Type u_1} -> {π : α → Type u_6} -> (s : Set α) -> (f : (a : α) → π a) -> (a : ↑s) -> π ↑a`

The implicit argument `α` is the ambient type on which `f` is defined. The implicit argument `π` is the dependent type family giving the codomain fiber over each element of `α`. The argument `s` is the subset of `α` to which the domain is restricted. The argument `f` is the dependent function being restricted. The final argument `a` is a term of the subtype `↥s`, i.e., an element of `α` together with a proof that it belongs to `s`.

## Conventions

No special junk-value or edge conventions are declared: the function is total and its behavior is uniform across all inputs — it simply evaluates `f` at the underlying element of `α`.

## Worked examples

- Claim: Restricting the squaring function `fun n : ℕ => n * n` to the set `{1, 2, 3}` at the subtype element `⟨2, by decide⟩` yields `4`.
  ```lean
  example : VTask.restrict {1, 2, 3} (fun n : ℕ => n * n) ⟨2, by decide⟩ = 4 := by rfl
  ```

- Claim: Restricting the identity function on `ℕ` to `Set.univ` at the subtype element `⟨5, Set.mem_univ 5⟩` returns `5`.
  ```lean
  example : VTask.restrict Set.univ (fun n : ℕ => n) ⟨5, Set.mem_univ 5⟩ = 5 := by rfl
  ```

- Claim: Restricting a constant function `fun _ : ℕ => 42` to any set `s` at any element `a : ↥s` returns `42`.
  ```lean
  example (s : Set ℕ) (a : ↥s) : VTask.restrict s (fun _ : ℕ => 42) a = 42 := by rfl
  ```

## Boundaries

- When `s = Set.univ`, every element of `α` is in `s`, and the restricted function behaves identically to the original `f` (up to the subtype wrapper).
- When `s = ∅`, the restricted function has an empty domain (the subtype `↥∅` is uninhabited), so it is vacuously defined and imposes no constraints.
- The function handles the non-dependent case (where `π` is a constant type family) as a special instance, reducing to ordinary function restriction.
- The range of the restricted function equals the image of `s` under `f`.

## Not to be confused with

- `Subtype.restrict`: the same operation but with argument order/style that takes the subtype membership proof packaged differently; `VTask.restrict` takes `↥s` directly.
- `Set.MapsTo.restrict`: restricts a function `f : α → β` to a map between subtypes `↥s → ↥t`, requiring a proof that `f` maps `s` into `t`.
- `Set.restrictPreimage`: restricts a function `f : α → β` to the preimage of a set in the codomain, rather than a set in the domain.
