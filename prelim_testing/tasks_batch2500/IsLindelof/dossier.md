## Object

A subset `s` of a topological space is **Lindelöf** if it has the following covering property: every open cover of `s` admits a countable subcover. Equivalently (and this is the definition adopted here), every nontrivial filter on the space that has the countable intersection property and whose sets all contain `s` must have a cluster point lying inside `s`. This is the natural countable analogue of compactness: where compactness demands finite subcovers, the Lindelöf property demands only countable ones.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsLindelof : {X : Type u} -> [TopologicalSpace X] -> (s : Set X) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsLindelof : {X : Type u} -> [TopologicalSpace X] -> (s : Set X) -> Prop`

The ambient type `X` is inferred; its topological structure is supplied by the typeclass instance. The explicit argument `s` is the subset of `X` whose Lindelöf property is being asserted.

## Conventions

There are no junk-value or out-of-domain conventions to declare: `VTask.IsLindelof` is a totally-defined predicate on all subsets of any topological space, including the empty set and the whole space, with no implicit restrictions.

## Worked examples

- Claim: Every finite subset of a topological space satisfies `VTask.IsLindelof`.

- Claim: Every countable subset of a topological space satisfies `VTask.IsLindelof`.

- Claim: Every compact set satisfies `VTask.IsLindelof`, since any finite subcover is in particular a countable one.

- Claim: The countable union of Lindelöf sets is again Lindelöf; in particular, a countable union of compact sets (each being Lindelöf) is Lindelöf.

- Claim: If `X` is a Lindelöf space, then every closed subset of `X` satisfies `VTask.IsLindelof`.

## Boundaries

- The empty set satisfies `VTask.IsLindelof` (it is finite, hence Lindelöf).
- Any singleton or subsingleton set satisfies `VTask.IsLindelof`.
- The whole space `Set.univ` satisfies `VTask.IsLindelof` if and only if the ambient space is a Lindelöf space (`LindelofSpace X`).
- In a `NonLindelofSpace`, no Lindelöf set can equal the whole universe.
- Removing an open set from a Lindelöf set preserves the Lindelöf property: if `s` is Lindelöf and `t` is open, then `s \ t` is Lindelöf.
- The union of two Lindelöf sets is Lindelöf; more generally, any countable union of Lindelöf sets is Lindelöf.

## Not to be confused with

- `IsCompact`: the analogous property requiring *finite* subcovers; every compact set is Lindelöf, but not vice versa.
- `LindelofSpace X`: the global typeclass asserting that the whole space `Set.univ` is Lindelöf, as opposed to the set-level predicate `VTask.IsLindelof s` for an individual subset.
- `IsSigmaCompact`: a set that is a countable union of compact sets; every σ-compact set is Lindelöf, but Lindelöf sets need not be σ-compact in general.