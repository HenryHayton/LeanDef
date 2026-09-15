## Object

`VTask.ofBounded` constructs a **bornology** on a type `α` from a specified collection `B` of subsets of `α` that is declared to be the family of *bounded* sets. A bornology is an abstract notion of boundedness: it designates which subsets of `α` count as bounded, subject to the axioms that the empty set is bounded, every subset of a bounded set is bounded, finite unions of bounded sets are bounded, and every singleton is bounded. This constructor lets you build such a structure directly from the collection of bounded sets, provided you supply proofs of all four axioms.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofBounded : {α : Type u_4} -> (B : Set (Set α)) -> (empty_mem : ∅ ∈ B) -> (subset_mem : ∀ s₁ ∈ B, ∀ s₂ ⊆ s₁, s₂ ∈ B) -> (union_mem : ∀ s₁ ∈ B, ∀ s₂ ∈ B, s₁ ∪ s₂ ∈ B) -> (singleton_mem : ∀ (x : α), {x} ∈ B) -> Bornology α
<!-- PINNED-SIGNATURE:END -->


`VTask.ofBounded : {α : Type u_4} -> (B : Set (Set α)) -> (empty_mem : ∅ ∈ B) -> (subset_mem : ∀ s₁ ∈ B, ∀ s₂ ⊆ s₁, s₂ ∈ B) -> (union_mem : ∀ s₁ ∈ B, ∀ s₂ ∈ B, s₁ ∪ s₂ ∈ B) -> (singleton_mem : ∀ (x : α), {x} ∈ B) -> Bornology α`

- `α` is the ambient type on which the bornology is being defined.
- `B` is the proposed family of bounded sets — a collection of subsets of `α` that will become precisely the bounded sets of the resulting bornology.
- `empty_mem` is a proof that the empty set belongs to `B` (the empty set is bounded).
- `subset_mem` is a proof that `B` is downward-closed under inclusion: every subset of a set in `B` also belongs to `B` (subsets of bounded sets are bounded).
- `union_mem` is a proof that `B` is closed under binary unions: if two sets are in `B`, so is their union (finite unions of bounded sets are bounded).
- `singleton_mem` is a proof that every singleton `{x}` belongs to `B` (all points are bounded, ensuring the bornology is compatible with the cofinite filter).

## Conventions

No special junk-value or edge conventions are declared: every argument is a required, mathematically meaningful input, and the constructor is total given those inputs.

## Worked examples

- Claim: For `B` the collection of all finite subsets of `ℕ`, `VTask.ofBounded B ⋯` yields a bornology on `ℕ` whose bounded sets are exactly the finite sets.

- Claim: A set `s : Set α` is bounded in `VTask.ofBounded B empty_mem subset_mem union_mem singleton_mem` if and only if `s ∈ B`.

- Claim: A set `s : Set α` is cobounded in `VTask.ofBounded B empty_mem subset_mem union_mem singleton_mem` if and only if `sᶜ ∈ B`.

- Claim: Under `VTask.ofBounded B empty_mem subset_mem union_mem singleton_mem`, the empty set is always bounded (since `empty_mem : ∅ ∈ B` was required as a hypothesis).

## Boundaries

- The constructor is total: as long as you provide the four proof obligations, the result is a valid `Bornology α`.
- The `singleton_mem` condition is the condition ensuring the bornology is coarser than or equal to the cofinite filter (i.e., every cofinite set is cobounded). Without it, the collection `B` might describe something that fails to be a legitimate bornology.
- The union closure axiom covers only *binary* unions; closure under arbitrary (possibly infinite) unions is not required and does not hold in general.
- If `B` is the discrete collection of all subsets of `α`, the resulting bornology is the discrete bornology where every subset is bounded.
- If `B` contains only the empty set and singletons (and their subsets), the resulting bornology is as coarse as possible while satisfying the axioms.

## Not to be confused with

- `Bornology.ofBounded'` (if it exists): a variant that may axiomatize boundedness differently, e.g., using the union of the whole space rather than singletons.
- `Bornology` (the structure itself): the *type* of bornologies on `α`, whereas `VTask.ofBounded` is a *constructor* producing an element of that type.
- `TopologicalSpace.ofNhds` or similar topology constructors: these build topologies from neighborhood filters, not bornologies from bounded-set families — the pattern is analogous but the objects are different.