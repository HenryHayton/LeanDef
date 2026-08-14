## Object

`VTask.piFinsetUnion` is a canonical equivalence (bijection) between two types of dependent functions:
- On the left: **pairs** consisting of a dependent function on the finite index set `s` and a dependent function on the finite index set `t` (where `s` and `t` are disjoint finsets).
- On the right: a single dependent function on the **union** `s ∪ t`.

Informally, it says that specifying a dependent function on `s ∪ t` is exactly the same data as independently specifying a dependent function on `s` and a dependent function on `t`, provided `s` and `t` are disjoint. It is a finset-indexed analogue of the fact that a function on a disjoint sum of types is the same as a pair of functions on each summand.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piFinsetUnion : {ι : Type u_5} -> [DecidableEq ι] -> (α : ι → Type u_4) -> {s t : Finset ι} -> (h : Disjoint s t) -> ((i : ↥s) → α ↑i) × ((i : ↥t) → α ↑i) ≃ ((i : ↥(s ∪ t)) → α ↑i)
<!-- PINNED-SIGNATURE:END -->


`VTask.piFinsetUnion : {ι : Type u_5} -> [DecidableEq ι] -> (α : ι → Type u_4) -> {s t : Finset ι} -> (h : Disjoint s t) -> ((i : ↥s) → α ↑i) × ((i : ↥t) → α ↑i) ≃ ((i : ↥(s ∪ t)) → α ↑i)`

The index type `ι` is the type whose elements name the "coordinates". `DecidableEq ι` is required for finset membership tests. The argument `α` is the dependent type family: for each index `i : ι`, `α i` is the type of the value at coordinate `i`. The implicit arguments `s` and `t` are the two finite subsets of `ι` being combined. The argument `h` is the proof that `s` and `t` are disjoint (share no elements), which is necessary for the union to decompose cleanly without ambiguity.

## Conventions

No special junk-value or boundary conventions are declared for this equivalence: it is defined precisely when `s` and `t` are disjoint finsets, and the disjointness is required as an explicit hypothesis, so there is no "out-of-domain" input to assign a junk value to.

## Worked examples

- Claim: Applying `VTask.piFinsetUnion α h (f, g)` to an element `⟨i, hi'⟩` where `i ∈ s` returns the value `f ⟨i, hi⟩` (the left component evaluated at `i`).

- Claim: Applying `VTask.piFinsetUnion α h (f, g)` to an element `⟨i, hi'⟩` where `i ∈ t` returns the value `g ⟨i, hi⟩` (the right component evaluated at `i`).

- Claim: When `s = {0}` and `t = {1}` (disjoint singletons in `Fin 3`), the equivalence identifies a pair of single-element functions with a two-element function on `{0, 1}`, and the round-trip through the equivalence and its inverse is the identity.

- Claim: The equivalence `VTask.piFinsetUnion α h` preserves the product measure: the pushforward of `(Measure.pi on s) × (Measure.pi on t)` along the equivalence equals `Measure.pi on s ∪ t`.

## Boundaries

- When `s = ∅` and `t` is arbitrary (with the trivially satisfied disjointness), the left component of the pair is a function on the empty finset, which is a unique element (a unit type). The equivalence then reduces to an isomorphism between functions on `t` alone and functions on `∅ ∪ t = t`, which is essentially the identity.
- When both `s = ∅` and `t = ∅`, the union is empty and both sides are singleton types (there is exactly one function out of the empty set), so the equivalence is between a pair of trivial functions and a single trivial function.
- The hypothesis `h : Disjoint s t` is necessary; the construction is not meaningful (or defined) when `s` and `t` overlap, because an element in both would need to be assigned a value from two potentially different sources.

## Not to be confused with

- `Equiv.sumPiEquivProdPi`: The analogous equivalence for a *type-level* sum `α ⊕ β` rather than a *finset* union `s ∪ t`; `VTask.piFinsetUnion` is built on top of this but works with finsets of indices.
- `Finset.union` (the finset union operation itself): That is merely the set-theoretic union of finsets, not the equivalence on function spaces.
- `MeasurableEquiv.piFinsetUnion`: The measurable-space version of the same equivalence; it carries additional measurability structure but represents the same underlying bijection.