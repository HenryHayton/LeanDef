## Object

The **fixing submonoid** of a set `s` (under a monoid action) is the collection of all elements of the monoid `M` that fix every point of `s` under the given action — that is, every `m : M` such that `m • x = x` for all `x ∈ s`. This collection is closed under multiplication and contains the identity, making it a submonoid of `M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.fixingSubmonoid : (M : Type u_1) -> {α : Type u_2} -> [Monoid M] -> [MulAction M α] -> (s : Set α) -> Submonoid M
<!-- PINNED-SIGNATURE:END -->


`VTask.fixingSubmonoid : (M : Type u_1) -> {α : Type u_2} -> [Monoid M] -> [MulAction M α] -> (s : Set α) -> Submonoid M`

The first explicit argument `M` is the monoid whose elements act on the ambient type. The implicit argument `α` is the type being acted upon. The two instance arguments supply the monoid structure on `M` and the action of `M` on `α`. The final explicit argument `s` is the subset of `α` whose pointwise stabiliser is being taken; the result is the submonoid of `M` consisting of exactly those elements that fix every point of `s`.

## Conventions

When `s` is the empty set, every element of `M` vacuously fixes all points of `s`, so the fixing submonoid is the entire monoid `M` (viewed as a submonoid). No junk-value conventions are needed beyond this natural totality: the construction is defined for every set `s`, including the empty set.

## Worked examples

- Claim: For the trivial monoid acting on any type, the fixing submonoid of any set is the whole trivial monoid (the only element fixes everything).

- Claim: For the monoid of functions `ℕ → ℕ` under composition acting on `ℕ` by evaluation, the identity function belongs to `VTask.fixingSubmonoid (M := Function.End ℕ) {0, 1}` because `id • 0 = 0` and `id • 1 = 1`.

- Claim: If `s ⊆ t` then `VTask.fixingSubmonoid M t ≤ VTask.fixingSubmonoid M s` — fixing a larger set is a stronger condition, so the fixing submonoid is smaller (monotone-antitone in `s`).

- Claim: The intersection (as submonoids) of `VTask.fixingSubmonoid M s` and `VTask.fixingSubmonoid M t` equals `VTask.fixingSubmonoid M (s ∪ t)`, because fixing all of `s` and all of `t` is the same as fixing all of `s ∪ t`.

## Boundaries

- **Empty set**: Every element of `M` fixes all points of `∅` vacuously, so `VTask.fixingSubmonoid M ∅ = ⊤` (the whole monoid as a submonoid).
- **Universal set (all of `α`)**: The fixing submonoid of `Set.univ` consists precisely of those elements that act as the identity on every point of `α`; this may be a proper submonoid.
- **Singleton `{x}`**: The fixing submonoid of `{x}` is the stabiliser (as a submonoid) of the single point `x`.
- The construction is always a valid submonoid regardless of the size or structure of `s`.

## Not to be confused with

- **Fixing subgroup** (`fixingSubgroup`): The analogous construction for groups; the fixing submonoid specialises to the fixing subgroup when `M` is a group, but `VTask.fixingSubmonoid` works in the strictly more general monoid setting.
- **Stabiliser of a single point** (`MulAction.stabilizer`): That is the subgroup/submonoid of elements fixing one designated point, whereas `VTask.fixingSubmonoid` simultaneously fixes every point of an entire set `s`.
- **Pointwise stabiliser vs orbit**: The fixing submonoid stabilises `s` pointwise (each point is individually fixed), not merely setwise (the set as a whole mapped to itself).