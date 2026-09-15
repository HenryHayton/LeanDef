## Object

`VTask.traverse` maps a "monadic" (or applicative) action `f : α → m β` over every node of a binary tree, collecting the results into a single value of type `m (BinaryTree β)`.  The traversal visits the root node first, then the left subtree, then the right subtree (pre-order / node-left-right).  The output tree has the same shape as the input tree, but every stored value has been replaced by the result of applying `f`.  When `m` is the identity applicative, this specialises to plain tree `map`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.traverse : {m : Type u_1 → Type u_2} -> [Applicative m] -> {α : Type u_3} -> {β : Type u_1} -> (f : α → m β) -> BinaryTree α → m (BinaryTree β)
<!-- PINNED-SIGNATURE:END -->


`VTask.traverse : {m : Type u_1 → Type u_2} -> [Applicative m] -> {α : Type u_3} -> {β : Type u_1} -> (f : α → m β) -> BinaryTree α → m (BinaryTree β)`

- `m` is the applicative functor in which effects are collected (e.g. `Option`, `List`, `IO`, `Id`).
- The `Applicative m` instance supplies `pure` and `<*>` for combining results from different nodes.
- `α` is the type of values stored in the input tree.
- `β` is the type of values stored in the output tree.
- `f` is the action applied at each node: given a node value of type `α`, it produces an `m β`.
- The final argument is the `BinaryTree α` to be traversed.

## Conventions

When the input tree is `BinaryTree.nil`, the result is `pure nil`—the empty tree is returned without invoking `f` at all, wrapped in the applicative unit.  Effects from `f` are combined in node → left-subtree → right-subtree order, matching the structural recursion on the tree constructors.

## Worked examples

- Claim: Traversing a `nil` tree with any action returns `pure nil` in every applicative.

- Claim: Traversing a single-node tree `BinaryTree.node 3 .nil .nil` with `f n := some (n + 1)` yields `some (BinaryTree.node 4 .nil .nil)`.
  ```lean
  example : VTask.traverse (fun n => some (n + 1)) (BinaryTree.node 3 .nil .nil) =
      some (BinaryTree.node 4 .nil .nil) := by native_decide
  ```

- Claim: Traversing a two-level tree `BinaryTree.node 1 (BinaryTree.node 2 .nil .nil) .nil` with `f n := [n, n * 10]` produces a list of four trees, reflecting all combinations.

- Claim: Traversing any tree `t` with `pure : α → Id α` returns `pure t` (the tree is unchanged), i.e., `VTask.traverse pure t = pure t` for any lawful applicative.

## Boundaries

- **Empty tree (`BinaryTree.nil`)**: `f` is never called; the result is `pure .nil` regardless of what `f` does, including whether `f` could fail or produce effects.
- **Single-node tree**: `f` is called exactly once; the result is `BinaryTree.node <$> f a <*> pure .nil <*> pure .nil`.
- **Non-terminating or infinite-like structures**: `BinaryTree` in Mathlib is an inductive type and therefore always finite; the recursion always terminates.
- **Failing applicatives** (e.g. `Option`, `Except`): if `f` returns `none` or `err` for any node, the entire traversal short-circuits and the result is `none` / `err`; no partial tree is produced.
- **Order of effects**: the node value is processed before either subtree, and the left subtree before the right; laws such as `comp_traverse` and `naturality` hold when the applicative instances are lawful.

## Not to be confused with

- `BinaryTree.map` — applies a pure function `α → β` to every node without any applicative structure; `VTask.traverse` specialises to `map` when `m = Id`.
- `BinaryTree.foldl` / `BinaryTree.foldr` — these collapse the tree into a single accumulated value rather than producing a new tree of the same shape.
- `List.traverse` — the standard `traverse` for lists; same traversable-functor concept but the shape being preserved is a list, not a binary tree.