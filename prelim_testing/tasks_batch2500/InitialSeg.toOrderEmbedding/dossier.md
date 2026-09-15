## Object

Given two partially ordered types and an initial segment embedding between them (a map `f : α ≤i β` that is order-preserving, injective, and whose image is a downward-closed initial segment of `β` with respect to `<`), `VTask.toOrderEmbedding f` produces the underlying order embedding `α ↪o β`. That is, it forgets the initial-segment property and retains only the order-embedding structure: the map is injective and preserves and reflects the order relation `≤`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toOrderEmbedding : {α : Type u_1} -> {β : Type u_2} -> [PartialOrder α] -> [PartialOrder β] -> (f : α ≤i β) -> α ↪o β
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {β : Type u_2} -> [PartialOrder α] -> [PartialOrder β] -> (f : α ≤i β) -> α ↪o β`

The type parameters `α` and `β` are the source and target types, inferred implicitly. The `PartialOrder` instances supply the `≤` relations on `α` and `β`. The explicit argument `f` is the initial segment embedding whose order-embedding is to be extracted.

## Conventions

The resulting order embedding has exactly the same underlying function as `f`: evaluating `VTask.toOrderEmbedding f` at any element `x : α` gives the same value as applying `f` directly to `x`.

## Worked examples

- Claim: For any initial segment embedding `f : α ≤i β` between partial orders, the coercion of `VTask.toOrderEmbedding f` to a function `α → β` equals the coercion of `f` to a function `α → β`.

- Claim: For any initial segment embedding `f : α ≤i β` and element `x : α`, `VTask.toOrderEmbedding f x = f x`.

## Boundaries

- The definition is total: it applies to any initial segment embedding between any two partial orders, with no restrictions.
- When `α = β` and `f` is the identity initial segment, `VTask.toOrderEmbedding f` is the identity order embedding.
- The operation discards the initial-segment (downward-closure) property; the result only guarantees the order-embedding (injectivity plus order-preservation and reflection) properties, not that the image is an initial segment.

## Not to be confused with

- `InitialSeg` (`α ≤i β`) itself: that is the richer structure requiring the image to be an initial segment, whereas the result here is the weaker `OrderEmbedding`.
- `PrincipalSeg.toOrderEmbedding` (`α <i β → α ↪o β`): the analogous forgetful map for *principal* (strict, bounded) initial segment embeddings, not general initial segments.
- `OrderEmbedding.ofMapLEIff` or other order-embedding constructors: those build order embeddings from scratch given a function and a proof, rather than extracting one from an existing initial segment embedding.
