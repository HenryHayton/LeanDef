## Object

`VTask.EqOnSource e e'` is the relation asserting that two partial equivalences `e` and `e'` between the same types agree completely on their common source: they share the same source set, and the forward map of `e` coincides with the forward map of `e'` at every point of that source. Two partial equivalences satisfying this relation should be regarded as essentially the same partial bijection, differing only in auxiliary data (such as the stated inverse function) outside the source.

This relation is in fact an equivalence relation on partial equivalences, and is the natural notion of equality-up-to-irrelevant-data in the partial-equivalence setting.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.EqOnSource : {α : Type u_1} -> {β : Type u_2} -> (e e' : PartialEquiv α β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.EqOnSource : {α : Type u_1} -> {β : Type u_2} -> (e e' : PartialEquiv α β) -> Prop`

The two universe-polymorphic type arguments `α` and `β` are inferred automatically and are the domain and codomain types shared by both partial equivalences. The first explicit argument `e` is the left-hand partial equivalence; the second explicit argument `e'` is the right-hand partial equivalence. The proposition holds when `e` and `e'` have the same source set and agree as functions on that source.

## Conventions

This relation is also written using the notation `e ≈ e'` in the Mathlib library, serving as the canonical equivalence relation on `PartialEquiv α β`. There are no junk-value conventions to declare: the relation is a genuine mathematical Prop with no edge-case defaults or sentinel values.

## Worked examples

- Claim: For any partial equivalence `e`, `VTask.EqOnSource e e` holds (reflexivity).

- Claim: If `VTask.EqOnSource e e'`, then `e.source = e'.source` (the source sets are equal).

- Claim: If `VTask.EqOnSource e e'`, then the targets are also equal, i.e., `e.target = e'.target`.

- Claim: If `VTask.EqOnSource e e'`, then the symms also satisfy `VTask.EqOnSource e.symm e'.symm`.

## Boundaries

- If the two partial equivalences have different source sets, `VTask.EqOnSource e e'` is false, even if the forward maps happen to agree on one of the sources.
- If the source sets agree but the forward maps differ at even one point in the source, the relation fails.
- Agreement of the two partial equivalences outside their common source is entirely irrelevant: the relation only checks the forward map on the source.
- The relation does not directly require agreement of the inverse maps; however, since valid partial equivalences have inverses determined by the forward map on the source, the inverse maps automatically agree on the target when `VTask.EqOnSource e e'` holds (as witnessed by `EqOnSource.symm_eqOn`).
- Composition (trans) and restriction (restr) are compatible with the relation: if `e ≈ e'` and `f ≈ f'`, then `e.trans f ≈ e'.trans f'`, and `e.restr s ≈ e'.restr s` for any set `s`.

## Not to be confused with

- `PartialEquiv` equality (`e = e'`): full definitional or propositional equality of the entire structure, which additionally requires the stated inverse maps to be equal; `VTask.EqOnSource` is strictly coarser.
- `Set.EqOn f g s`: pointwise agreement of two functions on a set, which is one half of `VTask.EqOnSource` but does not include the condition that the source sets are equal.
- `PartialHomeomorph.EqOnSource` (for topological partial homeomorphisms): the analogous relation for the topological setting, which reduces to `VTask.EqOnSource` at the level of underlying partial equivalences.