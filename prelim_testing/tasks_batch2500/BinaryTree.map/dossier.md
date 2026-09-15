## VTask.map

### Object
`VTask.map f t` applies the function `f` to every value stored at the nodes of the binary tree `t`, producing a new binary tree of the same shape whose node values are the images under `f`. The empty tree maps to the empty tree; a node with value `a`, left subtree `l`, and right subtree `r` maps to a node with value `f a`, left subtree `map f l`, and right subtree `map f r`. This is the standard functorial `map` for binary trees.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {α : Type u} -> {β : Type u_1} -> (f : α → β) -> BinaryTree α → BinaryTree β
<!-- PINNED-SIGNATURE:END -->


The first argument `f` is the function to apply element-wise to each node value, mapping values of type `α` to values of type `β`. The second argument is the binary tree whose values are to be transformed; it is consumed structurally, and its shape (branching structure) is preserved exactly in the output.

### Conventions

This definition is total: it is defined for every function `f` and every binary tree, including the empty tree `nil`. There are no junk-value conventions to declare.

### Worked examples

- Claim: Mapping any function over the empty tree (`nil`) yields the empty tree (`nil`).
  ```lean
  example : VTask.map (fun n : Nat => n + 1) BinaryTree.nil = BinaryTree.nil := by decide
  ```

- Claim: Mapping `(· + 1)` over a single-node tree containing `3` yields a single-node tree containing `4`.
  ```lean
  example : VTask.map (· + 1) (BinaryTree.node 3 .nil .nil) = BinaryTree.node 4 .nil .nil := by decide
  ```

- Claim: `VTask.map id t = t` for any binary tree `t` (the identity functor law).

- Claim: `VTask.map (g ∘ f) t = VTask.map g (VTask.map f t)` for any composable `f`, `g` and tree `t` (the composition functor law).

- Claim: Mapping `toString` over `BinaryTree.node 1 (BinaryTree.node 2 .nil .nil) .nil` produces `BinaryTree.node "1" (BinaryTree.node "2" .nil .nil) .nil`.

### Boundaries

- Applied to `nil`, the result is always `nil` regardless of `f`; in particular the output type changes from `BinaryTree α` to `BinaryTree β` even for the empty case.
- The shape of the tree is preserved exactly: the number of nodes, the depth of every node, and the left/right branching structure are all invariant under `map`.
- `map id` is the identity on trees (definitionally equal after reduction), satisfying one of the standard functor laws.
- Composition of two maps can always be fused into a single map: `map (g ∘ f) = map g ∘ map f`.

### Not to be confused with

- `BinaryTree.traverse`: a more general traversal that threads an applicative effect through the tree, of which `map` is a special (effect-free) case.
- `List.map` or `Functor.map` applied to a list representation of tree values: those discard tree shape, while `VTask.map` preserves it.
- A tree fold/reduction (`BinaryTree.foldr` or similar): those collapse the tree into a single value, whereas `VTask.map` always returns a tree of the same shape.