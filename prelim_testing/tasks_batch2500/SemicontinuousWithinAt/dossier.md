## Object

`VTask.SemicontinuousWithinAt r s x` is the proposition that the relation `r : α → β → Prop` is *semicontinuous within `s` at `x`*: for every `y` such that `r x y` holds, the property `r x' y` holds for all points `x'` in the set `s` that are sufficiently close to `x`. In other words, any "witness" `y` that is related to `x` via `r` remains related to every nearby point of `s`. This is a localised, relational generalisation of lower semicontinuity (where `r x y` encodes `y < f x`), upper semicontinuity (where `r x y` encodes `f x < y`), and the lower/upper hemicontinuity of set-valued maps.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SemicontinuousWithinAt : {α : Type u_1} -> {β : Type u_2} -> [TopologicalSpace α] -> (r : α → β → Prop) -> (s : Set α) -> (x : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.SemicontinuousWithinAt : {α : Type u_1} -> {β : Type u_2} -> [TopologicalSpace α] -> (r : α → β → Prop) -> (s : Set α) -> (x : α) -> Prop`

The implicit type `α` is the domain of points (equipped with a topology via the instance argument); `β` is an arbitrary type of "witnesses" carrying no topology of its own. The argument `r` is the binary relation being tested for semicontinuity. The argument `s` is the subset of `α` within which nearby points are sought (the neighbourhood filter is restricted to `s`). The argument `x` is the base point in `α` at which semicontinuity is evaluated.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a universally quantified proposition and is vacuously true whenever `r x y` is false for every `y`, or when `s` is chosen so that `x` is not a limit point of `s` (in which case the restricted neighbourhood filter has no nearby points to check).

## Worked examples

- Claim: A constant relation (one that does not depend on the point `x'`) is always semicontinuous within any set at any point, because the truth value of `r x' y` is independent of `x'`.

- Claim: If `r` is semicontinuous within `s` at `x`, and `t ⊆ s`, then `r` is also semicontinuous within `t` at `x`, since the neighbourhood filter within `t` is coarser than within `s`.

- Claim: If `r` is semicontinuous at `x` (without any restriction), then it is semicontinuous within any set `s` at `x`, because the unrestricted neighbourhood filter is finer than any restricted one.

- Claim: If `g : α → α` is continuous within `s` at `x`, mapping `s` into `t`, and `r` is semicontinuous within `t` at `g x`, then the composed relation `r ∘ g` is semicontinuous within `s` at `x`.

## Boundaries

- When `s = ∅`, the neighbourhood filter `𝓝[∅] x` is the trivial filter (all sets are eventually true), so `VTask.SemicontinuousWithinAt r ∅ x` holds for every `r` and every `x`.
- When `r x y` is false for every `y`, the universal quantifier over `y` is vacuously satisfied, so `VTask.SemicontinuousWithinAt r s x` holds regardless of the topology, the set `s`, or the structure of `r` near `x`.
- The definition places no topological requirement on `β`; the witnesses `y` are tested one at a time, with no notion of convergence in `β`.
- Semicontinuity within `s` at a point `x` that is isolated in `s` is automatic, because the relative neighbourhood filter at an isolated point contains a set whose only element of `s` is `x` itself.
- The condition is strictly weaker than global semicontinuity (`Semicontinuous r`) and than pointwise semicontinuity at `x` without restriction (`SemicontinuousAt r x`), both of which imply it.

## Not to be confused with

- `SemicontinuousAt r x`: semicontinuity at `x` using the unrestricted neighbourhood filter, with no subset restriction — strictly stronger than `VTask.SemicontinuousWithinAt r s x` for every `s`.
- `SemicontinuousOn r s`: semicontinuity within `s` at *every* point of `s` simultaneously, rather than at a single specified point `x`.
- `LowerSemicontinuousWithinAt f s x`: the classical lower semicontinuity of a function `f : α → γ` (where `γ` is an ordered type) within `s` at `x`, which is a special case of `VTask.SemicontinuousWithinAt` obtained by taking `r x y ↔ y < f x`.