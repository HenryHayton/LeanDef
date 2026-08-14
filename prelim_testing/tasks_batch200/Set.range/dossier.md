## Object

`VTask.range f` is the **range** (also called the **image**) of the function `f`: the set of all elements of the codomain `α` that are equal to `f y` for at least one element `y` of the domain `ι`. Formally, it is the subset `{x : α | ∃ y : ι, f y = x}`.

A notable feature is that the domain `ι` may be any `Sort` — not just a `Type` — making this construction more general than taking the direct image of the universal set (`f '' Set.univ`), which requires `ι` to live in `Type`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.range : {α : Type u} -> {ι : Sort u_1} -> (f : ι → α) -> Set α
<!-- PINNED-SIGNATURE:END -->


VTask.range : {α : Type u} -> {ι : Sort u_1} -> (f : ι → α) -> Set α

`α` is the codomain type (an ordinary type). `ι` is the domain sort (any `Sort`, including propositions or types). `f` is the function whose range is being computed.

## Conventions

There are no junk-value conventions for this definition: it is a total construction on all functions `f : ι → α` without restriction, and no special output is defined for degenerate inputs.

## Worked examples

- Claim: The element `3` belongs to `VTask.range (fun n : Fin 4 => n.val)` because `f 3 = 3`.

- Claim: The element `5` does not belong to `VTask.range (fun n : Fin 4 => n.val)` because no `n : Fin 4` has value `5`.

- Claim: For a constant function `f : ι → α` sending every element to `c`, `VTask.range f` equals the singleton `{c}` (provided `ι` is nonempty).

- Claim: For the successor function `Nat.succ : ℕ → ℕ`, `0` is not in `VTask.range Nat.succ` while every positive natural number is.

- Claim: For any equivalence `e : α ≃ β`, `VTask.range e.toFun` equals `Set.univ` (the whole of `β`), reflecting surjectivity.

## Boundaries

- If `ι` is an **empty type** (e.g., `Empty` or `False` as a `Prop`), then `VTask.range f` is the empty set, since no witness `y` can exist.
- If `f` is **surjective**, then `VTask.range f = Set.univ`.
- If `ι` is a **`Prop`** (e.g., `True`), `f` is still a valid input and the range is well-defined; this is the extra generality over `f '' Set.univ`.
- The range is invariant under composition with a bijection on the codomain: two functions with the same range are not necessarily equal.

## Not to be confused with

- `f '' s` (set image): the image of a *specific* subset `s ⊆ ι`; `VTask.range f` coincides with `f '' Set.univ` only when `ι : Type`.
- `Set.preimage` (`f ⁻¹' s`): pulls a subset of the codomain back to the domain, going in the opposite direction.
- `Function.Surjective f`: a *proposition* asserting that the range equals the whole codomain, not the range set itself.