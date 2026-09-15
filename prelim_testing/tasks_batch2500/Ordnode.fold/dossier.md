## Object

`VTask.fold` folds a binary function with a zero/seed value across every node of an ordered binary tree (`Ordnode α`), combining each node's left subtree result, node value, and right subtree result via the supplied function. It is a structural fold that mirrors the shape of the tree: the base case for an empty tree returns the seed, and each internal node combines the recursive results of its left child, its stored value, and its recursive result of its right child.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.fold : {α : Type u_1} -> {β : Sort u_2} -> (z : β) -> (f : β → α → β → β) -> Ordnode α → β
<!-- PINNED-SIGNATURE:END -->


`VTask.fold : {α : Type u_1} -> {β : Sort u_2} -> (z : β) -> (f : β → α → β → β) -> Ordnode α → β`

The type `α` is the element type stored in the tree nodes; it is inferred implicitly. The type `β` is the result/accumulator type; it too is inferred implicitly. `z` is the seed value returned for an empty tree and used as the accumulator at every leaf boundary. `f` is the combining function: given the folded result of the left subtree, the value at the current node, and the folded result of the right subtree, it produces the result for that node. The final argument is the `Ordnode α` tree to fold over.

## Conventions

The structure of function applications follows the exact shape of the tree, which is implementation-defined (the tree may be rebalanced); consequently the precise nesting of calls to `f` depends on the internal tree structure and is not specified beyond the recursive contract.

## Worked examples

- Claim: `VTask.fold 0 (fun l x r => l + x + r)` on the empty tree `Ordnode.nil` equals `0`.

- Claim: For a single-node tree `Ordnode.node s Ordnode.nil x Ordnode.nil`, `VTask.fold z f (Ordnode.node s Ordnode.nil x Ordnode.nil) = f z x z`.

- Claim: `VTask.fold [] (fun l x r => l ++ [x] ++ r)` traverses the tree in in-order, collecting elements left-to-right, so it agrees with the in-order list of the tree.

- Claim: `VTask.fold 0 (fun l _ r => l + 1 + r)` on any `Ordnode α` counts the total number of nodes.

## Boundaries

- On `Ordnode.nil` (the empty tree), `VTask.fold z f Ordnode.nil = z` regardless of `f`.
- On a single-node tree with empty children, the result is `f z x z` — `f` is called exactly once.
- Because `Ordnode` trees may be rebalanced internally, two trees representing the same ordered set can have different internal shapes; `VTask.fold` with a non-associative or non-commutative `f` may therefore return different values for logically equivalent sets.
- There is no constraint on `α` or `β`; the fold is well-defined for any types, including propositions (`β : Prop`).

## Not to be confused with

- `Ordnode.foldr`: a right fold that applies a binary function `α → β → β` in in-order right-to-left manner, threading a single accumulator; it ignores tree structure duality and does not pass left-subtree results to the combining function.
- `Ordnode.foldl`: a left fold threading a single accumulator in in-order left-to-right order, again without the three-argument combiner.
- `List.foldr` / `List.foldl`: standard list folds; `VTask.fold` is distinct in accepting a *three*-argument combining function that receives both subtree results simultaneously, reflecting the binary tree structure.