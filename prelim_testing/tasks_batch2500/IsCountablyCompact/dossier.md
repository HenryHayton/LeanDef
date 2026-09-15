## VTask.IsCountablyCompact

### Object

A subset `A` of a topological space is **countably compact** if every non-empty filter on the space that is (i) countably generated and (ii) contained in the principal filter of `A` has at least one cluster point lying inside `A`. Informally, this is the compactness condition weakened so that only countably generated filters—rather than arbitrary ones—need to be tested. Equivalently, one can think of it as saying that every countable open cover of `A` has a finite subcover, though the filter formulation above is the one adopted here.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsCountablyCompact : {E : Type u_2} -> [TopologicalSpace E] -> (A : Set E) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsCountablyCompact : {E : Type u_2} -> [TopologicalSpace E] -> (A : Set E) -> Prop`

The type `E` is the ambient topological space, inferred implicitly. The `TopologicalSpace E` instance, also implicit, supplies the topology on `E`. The explicit argument `A` is the subset of `E` whose countable compactness is being asserted.

### Conventions

No special junk-value or edge-case conventions are declared for this predicate: it is a universally quantified statement over filters, and when the set is empty the quantification over filters with `f ≤ 𝓟 ∅` (i.e., only the trivially empty situation) makes the property vacuously true, which is the natural mathematical convention.

### Worked examples

- Claim: Every compact set is countably compact. If `hA : IsCompact A` then `VTask.IsCountablyCompact A` holds.

- Claim: The union of two countably compact sets is countably compact. If `hA : VTask.IsCountablyCompact A` and `hB : VTask.IsCountablyCompact B`, then `VTask.IsCountablyCompact (A ∪ B)`.

- Claim: A countably compact set that is also Lindelöf is compact. If `hA : VTask.IsCountablyCompact A` and `hl : IsLindelof A`, then `IsCompact A`.

- Claim: In a first-countable topological space, every countably compact set is sequentially compact. If `[FirstCountableTopology E]` and `hA : VTask.IsCountablyCompact A`, then `IsSeqCompact A`.

- Claim: A closed subset of a countably compact space is countably compact. If `[CountablyCompactSpace E]` and `hA : IsClosed A`, then `VTask.IsCountablyCompact A`.

### Boundaries

- The **empty set** satisfies `VTask.IsCountablyCompact ∅` vacuously, because no non-empty filter can be smaller than `𝓟 ∅` (the bottom filter on a non-empty type).
- **Finite sets** are countably compact because they are compact.
- A countably compact set need not be compact in general; the implication reverses only under additional hypotheses such as the space being hereditarily Lindelöf.
- Countably compact is strictly weaker than compact and, in first-countable spaces, equivalent to sequential compactness.
- Continuous images of countably compact sets are countably compact, mirroring the analogous result for compactness.
- A closed subset of a countably compact set is countably compact.

### Not to be confused with

- `IsCompact`: the strictly stronger condition requiring every (not just countably generated) proper filter contained in `𝓟 A` to have a cluster point in `A`; every compact set is countably compact but not vice versa in general.
- `IsSeqCompact`: sequential compactness, defined via sequences rather than filters; equivalent to countable compactness in first-countable spaces but a distinct notion in general.
- `CountablyCompactSpace`: a **typeclass** asserting that the *whole* space `E` is countably compact, rather than a predicate on an individual subset.
