## Object

`VTask.find` selects a canonical element from a nonempty chain of partial refinements, with the guarantee that if the index `i` already appears in the carrier of some member of the chain, the selected element is one that covers `i`.

A *partial refinement* in the context of the Shrinking Lemma is a partial assignment of open sets refining a given open cover, defined on some finite subset of the index type (the *carrier*). A *chain* is a totally-ordered collection under the natural refinement ordering. `VTask.find` acts as a choice function that is "aware" of whether index `i` is already handled by some member of the chain.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.find : {ι : Type u_1} -> {X : Type u_2} -> [TopologicalSpace X] -> {u : ι → Set X} -> {s : Set X} -> {p : Set X → Prop} -> (c : Set (ShrinkingLemma.PartialRefinement u s p)) -> (ne : c.Nonempty) -> (i : ι) -> ShrinkingLemma.PartialRefinement u s p
<!-- PINNED-SIGNATURE:END -->


VTask.find : {ι : Type u_1} -> {X : Type u_2} -> [TopologicalSpace X] -> {u : ι → Set X} -> {s : Set X} -> {p : Set X → Prop} -> (c : Set (ShrinkingLemma.PartialRefinement u s p)) -> (ne : c.Nonempty) -> (i : ι) -> ShrinkingLemma.PartialRefinement u s p

- `ι` is the index type used to label the open sets of the cover.
- `X` is the topological space being covered.
- The `TopologicalSpace X` instance supplies the topology on `X`.
- `u` is the original open cover: a function assigning to each index an open set of `X`.
- `s` is the set being covered (the domain of the refinement problem).
- `p` is a property that each refined open set must satisfy.
- `c` is the chain of partial refinements from which the selection is made.
- `ne` is a proof that `c` is nonempty, ensuring a selection is always possible.
- `i` is the index that guides which element of the chain is selected: if some member of `c` has `i` in its carrier, the result is such a member; otherwise an arbitrary member is returned.

## Conventions

When no member of the chain `c` has `i` in its carrier, `VTask.find c ne i` returns an arbitrary (but fixed) element of `c` — specifically the element witnessed by `ne`. There is no meaningful junk value in the strict sense, since the result is always a valid member of `c`; the "fallback" case is simply the nonempty witness rather than a distinguished default outside the intended domain.

## Worked examples

- Claim: For any nonempty chain `c` and any index `i`, the result `VTask.find c ne i` is itself a member of `c`.

- Claim: If `v ∈ c` and `i ∈ carrier v`, and `c` is a chain under the refinement order, then `(VTask.find c ne i) i = v i` — that is, the selected partial refinement agrees with `v` at index `i`.

- Claim: `i ∈ (VTask.find c ne i).carrier` if and only if `i` belongs to the union of carriers of all elements of `c` (i.e., `i ∈ chainSupCarrier c`).

- Claim: Even in the fallback case (no member of `c` has `i` in its carrier), `VTask.find c ne i` is a legitimate partial refinement satisfying all the structural requirements of `PartialRefinement u s p`.

## Boundaries

- **`i` not in any carrier**: When no `v ∈ c` has `i ∈ carrier v`, the function returns `ne.some`, the nonempty witness of `c`. The result is still a valid partial refinement; `i` will simply not be in its carrier.
- **`i` in exactly one carrier**: The unique such `v` is returned (up to the choice made by the existential).
- **`i` in multiple carriers**: Since `c` is assumed to be a chain, any two partial refinements in `c` that both have `i` in their carriers must be ordered, so they agree on `i`. The element chosen by `VTask.find` is one of these, and all give the same value at `i`.
- **Singleton chain**: When `c = {v}`, `VTask.find c ne i` always returns `v` regardless of whether `i ∈ carrier v`.
- **The index type `ι` is empty**: If `ι` is empty, no `i` can be provided, so `VTask.find` cannot be applied; this is not a boundary case in practice.

## Not to be confused with

- `ShrinkingLemma.PartialRefinement.chainSup`: The supremum of the whole chain, which assembles all carriers into one partial refinement, rather than selecting a single existing member.
- `Set.Nonempty.some`: A bare choice of an element from a nonempty set, with no awareness of the index `i` or its membership in any carrier.
- `ShrinkingLemma.PartialRefinement.carrier`: The finite set of indices already handled by a single partial refinement, not the selection function across a chain.