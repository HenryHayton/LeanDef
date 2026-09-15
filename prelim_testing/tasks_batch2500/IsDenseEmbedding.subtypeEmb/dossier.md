## Object

`VTask.subtypeEmb` constructs, from a predicate `p` on a type `α`, a function `e : α → β`, and a term `x` of the subtype `{x // p(x)}`, a new term of the subtype consisting of points in `β` that lie in the closure of the image `e({x | p x})`. Concretely, it sends `x` to `e x`, promoted to the closure-subtype by the observation that `e x` itself already belongs to the image `e({x | p x})` and hence to its closure. In other words, it embeds the subtype `{x // p x}` (via `e`) into the closure of its image.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subtypeEmb : {β : Type u_2} -> [TopologicalSpace β] -> {α : Type u_5} -> (p : α → Prop) -> (e : α → β) -> (x : { x // p x }) -> { x // x ∈ closure (e '' {x | p x}) }
<!-- PINNED-SIGNATURE:END -->


`VTask.subtypeEmb p e x`

The topology on `β` is provided as a typeclass instance and determines what "closure" means. The predicate `p : α → Prop` carves out the subtype of `α` whose image under `e` is being closed up. The map `e : α → β` is the ambient embedding whose restriction to the subtype is being studied. The element `x : {x // p x}` is the specific subtype member being mapped.

## Conventions

There are no junk-value or edge conventions needed: the function is total and well-defined for every choice of `p`, `e`, and `x`; the only subtlety is that the output type tracks membership in the closure of the image, which is always satisfied by the construction.

## Worked examples

- Claim: For `e = id : ℝ → ℝ` and `p x = (0 < x)`, applying `VTask.subtypeEmb p e` to a positive real `x` yields a term whose underlying value equals `x` and which lies in `closure (id '' {x | 0 < x})`.

- Claim: For any `β` with a topological space, any `e : α → β`, and any `x : {x // p x}`, the underlying `β`-value of `VTask.subtypeEmb p e x` equals `e x.val`.

## Boundaries

- If the image `e '' {x | p x}` is already closed (e.g., when `e` is a closed embedding or when `{x | p x}` is compact and `β` is Hausdorff), then the closure coincides with the image itself, and the output subtype is just `e '' {x | p x}`.
- If `p` is the constant false predicate, then `{x // p x}` is empty, and `VTask.subtypeEmb p e` is vacuously defined (its domain is empty), but the type is still well-formed.
- The function is compatible with uniform structure: when `e` is a uniform embedding and a dense embedding, `VTask.subtypeEmb p e` is itself a uniform embedding (see the neighborhood theorems).
- When `e` is a dense embedding, `VTask.subtypeEmb p e` is again a dense embedding into the closure subtype.

## Not to be confused with

- `IsDenseEmbedding.subtype`: a theorem asserting that `VTask.subtypeEmb p e` is a dense embedding when `e` is, not the map itself.
- The plain subtype inclusion `Subtype.val` (or coercion): that maps `{x // p x}` into `α`, whereas `VTask.subtypeEmb p e` maps into a closure-subtype of `β`.
- `Set.inclusion` for subset inclusions: that handles inclusions between subtypes of the same ambient type, not the image-and-closure construction here.