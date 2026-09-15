## VTask.kernImage

### Object

Given a function `f : α → β` and a set `s ⊆ α`, the **kernel image** `kernImage f s` is the set of all elements `y : β` with the property that every preimage of `y` under `f` already lies in `s`. Equivalently, it is the largest set `t ⊆ β` whose preimage under `f` is contained in `s`: a point `y` belongs to `kernImage f s` precisely when `f ⁻¹' {y} ⊆ s`.

This construction is the right adjoint to the preimage operation `f ⁻¹'` in the sense that `f ⁻¹' t ⊆ s ↔ t ⊆ kernImage f s`, making the pair `(f ⁻¹', kernImage f)` a Galois connection between the power sets of `β` and `α`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.kernImage : {α : Type u} -> {β : Type v} -> (f : α → β) -> (s : Set α) -> Set β
<!-- PINNED-SIGNATURE:END -->


`VTask.kernImage : {α : Type u} -> {β : Type v} -> (f : α → β) -> (s : Set α) -> Set β`

The first (implicit) argument is the domain type; the second (implicit) argument is the codomain type. The argument `f` is the function through which the kernel image is taken. The argument `s` is the subset of the domain that acts as the "target" for preimages.

### Conventions

The definition is total: no junk-value conventions are needed. Every input `(f, s)` yields a well-defined subset of `β`.

### Worked examples

- Claim: For the function `f : Fin 3 → Bool` defined by `f 0 = false`, `f 1 = true`, `f 2 = true`, and `s = {1, 2}` (all of `Fin 3`), every `y : Bool` satisfies `f ⁻¹' {y} ⊆ s`, so `kernImage f s = Set.univ`.

- Claim: For any `f : α → β`, `kernImage f ∅ = (Set.range f)ᶜ`. That is, the kernel image of the empty set consists exactly of those `y : β` that are not in the range of `f` — for such `y` there is no `x` with `f x = y`, so the condition `f ⁻¹' {y} ⊆ ∅` is vacuously true.

- Claim: For any `f : α → β` and `s : Set α`, `kernImage f (sᶜ) = (f '' s)ᶜ`. That is, the kernel image of the complement of `s` is the complement of the direct image of `s`.

- Claim: For any `f : α → β` and `t : Set β`, `kernImage f (f ⁻¹' t) = t` if and only if the complement of the range of `f` is contained in `t`.

### Boundaries

- **Empty source set:** `kernImage f ∅ = (range f)ᶜ`. A point `y` satisfies the vacuous condition `f ⁻¹' {y} ⊆ ∅` if and only if `y` has no preimage, i.e., `y ∉ range f`.
- **Full source set:** `kernImage f Set.univ = Set.univ`, since for any `y` all preimages trivially lie in `Set.univ`.
- **Points outside the range:** For any `s`, every `y ∉ range f` belongs to `kernImage f s` (the condition is vacuous). Hence `(range f)ᶜ ⊆ kernImage f s` always holds.
- **Complement interaction:** `kernImage f (sᶜ) = (f '' s)ᶜ`, so the kernel image of a complement is the complement of the ordinary image.
- **Monotonicity:** `kernImage f` is monotone: if `s ⊆ t` then `kernImage f s ⊆ kernImage f t`.

### Not to be confused with

- **`Set.image f s` (direct image):** This is the set of values `f x` for `x ∈ s`; membership requires *existence* of a preimage in `s`, whereas `kernImage f s` requires *all* preimages to lie in `s`.
- **`Set.preimage f t` (preimage / pullback):** This maps subsets of `β` back to `α`; `kernImage` maps subsets of `α` forward to `β` and is the right adjoint of the preimage, not the preimage itself.
- **`Set.range f`:** This is the image of the entire domain `Set.univ` under `f`; it differs from `kernImage f s` for proper subsets `s`, and appears in the boundary behaviour of `kernImage f ∅`.
