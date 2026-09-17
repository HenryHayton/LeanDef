## Object

`VTask.IsImage e s t` is the proposition that the set `t ⊆ β` is an **image set** of `s ⊆ α` under the partial equivalence `e : PartialEquiv α β`. Concretely, this means that for every point `x` in the domain (source) of `e`, the forward image `e x` lands in `t` if and only if `x` itself belongs to `s`. Equivalently, the forward map sends `source ∩ s` exactly onto `target ∩ t`, and the preimage of `t` under `e` (intersected with the source) equals `source ∩ s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsImage : {α : Type u_1} -> {β : Type u_2} -> (e : PartialEquiv α β) -> (s : Set α) -> (t : Set β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsImage : {α : Type u_1} -> {β : Type u_2} -> (e : PartialEquiv α β) -> (s : Set α) -> (t : Set β) -> Prop`

The implicit type arguments `α` and `β` are the domain and codomain types. The explicit argument `e` is the partial equivalence whose forward map is used to relate the two sets. The argument `s` is the subset of the domain `α` being considered. The argument `t` is the candidate image subset of `β` that is asserted to correspond to `s` under `e`.

## Conventions

The predicate only imposes a condition on points that lie in `e.source`; behaviour of `e` outside its source is irrelevant to whether `VTask.IsImage e s t` holds, so there is no junk-value convention to declare for points outside the source.

## Worked examples

- Claim: For any partial equivalence `e`, the source `e.source` and target `e.target` satisfy `VTask.IsImage e e.source e.target`.

- Claim: If `e` and `e'` are partial equivalences with disjoint sources and disjoint targets, then `VTask.IsImage e e'.source e'.target` holds, because no point of `e.source` maps to `e'.target` (the two targets are disjoint) and no point of `e.source` lies in `e'.source` (the two sources are disjoint).

- Claim: If `VTask.IsImage e s t` holds, then `VTask.IsImage e.symm t s` also holds — the image relationship is symmetric with respect to swapping the partial equivalence with its inverse and interchanging the two sets.

## Boundaries

- If `e.source` is empty, `VTask.IsImage e s t` holds vacuously for **any** `s` and `t`, because the universal quantifier over `e.source` is over an empty set.
- The sets `s` and `t` need not be subsets of `e.source` and `e.target` respectively; the predicate only constrains behaviour on the overlap with the source.
- Even if `s` is disjoint from `e.source`, the predicate can still hold: every `x ∈ e.source` fails `x ∈ s`, and correspondingly `e x ∉ t` for all such `x` (assuming `t` is also disjoint from `e.target` in a compatible way).

## Not to be confused with

- `Set.image`: the plain set-theoretic forward image `e '' s`; `VTask.IsImage e s t` is a two-sided membership condition, not just the image set itself.
- `PartialEquiv.source` / `PartialEquiv.target`: these are the built-in domain and codomain sets of the partial equivalence, whereas `s` and `t` in `VTask.IsImage` are arbitrary subsets that may differ from the source and target.
- A homeomorphism or full equivalence image theorem: `VTask.IsImage` is specific to **partial** equivalences and only quantifies over the source of `e`, making it weaker than a global image statement.