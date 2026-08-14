## Object

`VTask.pi` constructs, from a family of partial equivalences indexed by a type `ι`, a single partial equivalence on the corresponding pi (dependent product) types. Concretely, given for each index `i` a partial equivalence `ei i` between `αi i` and `βi i`, the result is a partial equivalence between `(i : ι) → αi i` and `(i : ι) → βi i` that acts pointwise: a dependent function is mapped by applying `ei i` to its `i`-th component for every `i`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {ι : Type u_5} -> {αi : ι → Type u_6} -> {βi : ι → Type u_7} -> (ei : (i : ι) → PartialEquiv (αi i) (βi i)) -> PartialEquiv ((i : ι) → αi i) ((i : ι) → βi i)
<!-- PINNED-SIGNATURE:END -->


`VTask.pi : {ι : Type u_5} -> {αi : ι → Type u_6} -> {βi : ι → Type u_7} -> (ei : (i : ι) → PartialEquiv (αi i) (βi i)) -> PartialEquiv ((i : ι) → αi i) ((i : ι) → βi i)`

The implicit argument `ι` is the index type parametrising the family. The implicit arguments `αi` and `βi` are the domain and codomain type families over `ι`, respectively. The explicit argument `ei` is the family of partial equivalences: for each index `i`, `ei i` is the partial equivalence between `αi i` and `βi i` whose pointwise behaviour determines the constructed product equivalence.

## Conventions

The source of the resulting partial equivalence is the pi-set over all indices: a dependent function belongs to the source precisely when, for every `i`, its `i`-th component belongs to the source of `ei i`. Analogously, the target is the pi-set requiring each component to lie in the target of `ei i`. There are no special junk-value conventions beyond those inherited from the component `PartialEquiv` fields.

## Worked examples

- Claim: The symmetry of `VTask.pi ei` equals the pi of the pointwise symmetries, i.e., `(VTask.pi ei).symm = VTask.pi (fun i => (ei i).symm)`.

- Claim: Composing `VTask.pi ei` with `VTask.pi ei'` (when the types match) yields `VTask.pi (fun i => (ei i).trans (ei' i))`, so composition distributes over the index family.

- Claim: When each `ei i` is the identity partial equivalence `PartialEquiv.refl (αi i)`, the result `VTask.pi (fun i => PartialEquiv.refl (αi i))` equals the identity partial equivalence `PartialEquiv.refl ((i : ι) → αi i)` on the full pi type.

- Claim: For a function `f : (i : ι) → αi i` lying in the source (each `f i` in `(ei i).source`), the forward map sends `f` to the function `fun i => (ei i) (f i)`, and the inverse map sends it back to `f`.

## Boundaries

- If any component `ei i` has an empty source, then the source of `VTask.pi ei` is also empty, since a dependent function must have every component in the corresponding source.
- If `ι` is the empty type, then both the source and target are the single-element pi set (every dependent function over the empty index trivially satisfies the conditions), and the partial equivalence acts as the identity on that singleton.
- The partial equivalence is only guaranteed to be well-behaved (left/right inverse properties) on the declared source and target; behaviour outside these sets is not specified.

## Not to be confused with

- `PartialEquiv.refl`: the identity partial equivalence on a single type, not a product construction over a family.
- `Equiv.piCongrRight`: a total (non-partial) equivalence on pi types built from a family of total equivalences, without any source/target restrictions.
- `PartialEquiv.prod`: the product of exactly two partial equivalences on ordinary product types `α × β`, as opposed to a dependent family of arbitrary arity.