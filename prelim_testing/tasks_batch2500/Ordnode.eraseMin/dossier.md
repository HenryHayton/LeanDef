## VTask.eraseMin

### Object

`VTask.eraseMin` removes the minimum (leftmost) element from an ordered binary tree (`Ordnode α`). If the tree is empty, the operation leaves it unchanged. The resulting tree contains all elements of the original except its smallest one, and remains a valid ordered tree of the same type.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.eraseMin : {α : Type u_1} -> Ordnode α → Ordnode α
<!-- PINNED-SIGNATURE:END -->


The sole argument is the ordered binary tree from which the minimum element is to be removed. The element type `α` is inferred implicitly.

### Conventions

The function is total: when applied to the empty tree (`nil`), it simply returns the empty tree unchanged — no error, no partiality. There is no junk value to speak of; the empty-tree case is a genuine, well-defined base case of the operation.

### Worked examples

- Claim: Applying `VTask.eraseMin` to the empty tree returns the empty tree.
  (By definition, `VTask.eraseMin nil = nil`.)

- Claim: Applying `VTask.eraseMin` to a singleton tree `{x}` returns the empty tree.
  (A singleton is `node 1 nil x nil`; the left child is `nil`, so the result is the right subtree `nil`.)

- Claim: Applying `VTask.eraseMin` to a two-node tree `{1, 2}` (represented as `node 2 (node 1 nil 1 nil) 2 nil`) returns the singleton `{2}`.
  (The left child is non-nil, so the function recurses leftward, eventually removing the node carrying `1`, and rebalances to yield a tree containing only `2`.)

- Claim: If `t` is a valid `Ordnode α`, then `VTask.eraseMin t` is also valid.
  (Validity is preserved: the BST and balance invariants are maintained by the operation.)

- Claim: For any non-empty valid `Ordnode α` of size `n`, the size of `VTask.eraseMin t` equals `n - 1`.
  (Exactly one element, the minimum, is removed.)

- Claim: `VTask.eraseMin` is dual to `eraseMax` under the `dual` involution: `dual (VTask.eraseMin t) = eraseMax (dual t)` for all `t`.

### Boundaries

- **Empty tree**: `VTask.eraseMin nil = nil`. The operation is a no-op on the empty tree.
- **Singleton tree** `node 1 nil x nil`: the left child is `nil`, so the result is the right subtree `nil`, i.e., an empty tree.
- **Tree with only a right subtree** (left child is `nil`): the result is simply the right subtree, with no rebalancing needed.
- **General case**: when the left subtree is non-empty, the minimum lies deeper to the left; the function recurses and then rebalances using a right-biased balance (`balanceR`) because the left side has shrunk by one.

### Not to be confused with

- `eraseMax`: removes the *maximum* (rightmost) element rather than the minimum; it is the mirror-image operation under `dual`.
- `findMin` / `findMin'`: *reads* the minimum element without modifying the tree, whereas `VTask.eraseMin` *removes* it.
- `erase`: removes an *arbitrary specified* element by value, not necessarily the minimum.
