## Object

`VTask.traverse` is the traversal operation for the free magma functor. Given a `FreeMagma α` — a binary tree whose leaves carry values of type `α` — and an effectful function `F : α → m β` valued in an applicative functor `m`, it lifts `F` through the entire tree structure, applying `F` to every leaf and reassembling the tree under the applicative effects, yielding an `m (FreeMagma β)`. In other words, it is the canonical way to "map with effects" over every element of a free magma, preserving the tree's multiplication structure.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.traverse : {m : Type u → Type u} -> [Applicative m] -> {α β : Type u} -> (F : α → m β) -> FreeMagma α → m (FreeMagma β)
<!-- PINNED-SIGNATURE:END -->


`VTask.traverse : {m : Type u → Type u} -> [Applicative m] -> {α β : Type u} -> (F : α → m β) -> FreeMagma α → m (FreeMagma β)`

The universe-polymorphic applicative functor `m` provides the computational context (e.g. `Option`, `List`, `IO`). The `Applicative m` instance supplies the `pure` and `<*>` combinators needed to reassemble the tree. The types `α` and `β` are the leaf-element types before and after the traversal. The function `F` is the effectful transformation applied to each leaf. The final argument is the free magma (binary tree) being traversed.

## Conventions

There are no junk-value conventions for this definition: the function is total and structurally recursive on well-formed `FreeMagma` values, with no edge cases that produce arbitrary or undefined outputs.

## Worked examples

- Claim: Traversing a single-leaf free magma `FreeMagma.of x` with `F` gives `FreeMagma.of <$> F x`.

- Claim: `VTask.traverse some (FreeMagma.of 3) = some (FreeMagma.of 3)` (using `F = some` and `m = Option`).

- Claim: For `x y : FreeMagma α`, traversing the product `x * y` distributes as `(· * ·) <$> VTask.traverse F x <*> VTask.traverse F y`; this is exactly `traverse_mul`.

- Claim: `VTask.traverse (fun n => [n, n+1]) (FreeMagma.of 0 * FreeMagma.of 10)` (with `m = List`) yields a list of four free magmas corresponding to the two independent binary choices at each leaf.

## Boundaries

- **Single leaf (`FreeMagma.of x`)**: The traversal applies `F` to the single value and wraps the result in `FreeMagma.of` via `fmap`, giving `FreeMagma.of <$> F x`. No multiplication is involved.
- **Product node (`x * y`)**: The traversal recurses into both subtrees independently and recombines them with the magma multiplication lifted into the applicative functor via `<$>` and `<*>`. This respects the left-to-right ordering imposed by `Applicative`.
- **Deeply nested trees**: Structural recursion guarantees termination for any finite `FreeMagma`; no bound on depth is required.
- **Identity applicative**: With the identity applicative, `VTask.traverse pure` acts as `fmap pure`, and the traversal reduces to `pure <$> id` on each leaf, which (by traversal laws) is equivalent to wrapping the whole tree in `pure`.

## Not to be confused with

- `FreeMagma.map` / `fmap`: The plain functor map applies a pure function `α → β` to each leaf, with no applicative effects; `VTask.traverse` generalises this to effectful `α → m β`.
- `Traversable.traverse` (the typeclass method): `VTask.traverse` is the underlying implementation that witnesses the `Traversable FreeMagma` instance; the typeclass method and this function agree on all inputs (`traverse_eq`), but they are nominally distinct.
- Traversal on `FreeMonoid` or `FreeAddMagma`: Those structures carry a different algebraic shape (lists / additive binary trees) and have their own traverse instances that should not be conflated with the multiplicative free magma version here.