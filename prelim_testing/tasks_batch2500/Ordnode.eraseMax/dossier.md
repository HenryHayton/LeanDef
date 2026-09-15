## VTask.eraseMax

### Object

`VTask.eraseMax` removes the maximum element from an ordered binary tree (`Ordnode α`). If the tree is empty, it is returned unchanged. Otherwise, the unique largest element (rightmost node in the in-order traversal) is deleted, and the remaining elements are returned in a balanced ordered tree with the same ordering invariants.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.eraseMax : {α : Type u_1} -> Ordnode α → Ordnode α
<!-- PINNED-SIGNATURE:END -->


The single argument is an `Ordnode α` — an ordered binary tree whose nodes carry values of type `α`. No explicit ordering argument is needed because the ordering structure is baked into the `Ordnode` type itself.

### Conventions

When the input tree is empty (`nil`), `VTask.eraseMax` returns `nil` — it does nothing rather than raising an error or returning a default.

### Worked Examples

- Claim: Removing the maximum from the singleton tree `{3}` yields the empty tree.
- Claim: Removing the maximum from `{1, 2, 3}` (a valid ordered tree containing 1, 2, 3) yields a valid ordered tree containing exactly 1 and 2.
- Claim: Applying `VTask.eraseMax` to an empty `Ordnode` returns an empty `Ordnode`.
- Claim: If `t` is a valid `Ordnode` (satisfies `Valid t`), then `VTask.eraseMax t` is also valid (satisfies `Valid (VTask.eraseMax t)`).
- Claim: `VTask.eraseMax` is dual to `eraseMin` in the sense that `dual (VTask.eraseMax t) = eraseMin (dual t)` for every `Ordnode t`.

### Boundaries

- **Empty tree**: `VTask.eraseMax nil = nil`. No error, no partial value — identity on the empty tree.
- **Singleton tree** (a node whose left and right children are both `nil`): the result is `nil`, since the only element is both minimum and maximum.
- **Node with no right child**: when a node has a non-empty left subtree but an empty right child, that node itself is the maximum, so the result is the left subtree directly (no rebalancing step needed).
- **General case**: when the right child is non-empty, the maximum lives somewhere in the right subtree; `VTask.eraseMax` recurses into the right subtree and then rebalances with `balanceL` to restore the size and balance invariants.
- **Validity is preserved**: if the input tree is a valid `Ordnode`, the output is also a valid `Ordnode` (same ordering invariants, correct sizes, balanced).
- **Size**: for a non-empty valid input tree, the output has exactly one fewer element than the input.

### Not to be confused with

- **`eraseMin`**: removes the *minimum* (leftmost) element instead of the maximum; `VTask.eraseMax` and `eraseMin` are duals of each other under the `dual` involution.
- **`findMax'`**: returns the *value* of the maximum element without removing it; `VTask.eraseMax` removes it without returning it.
- **`splitMax'`**: simultaneously returns both the erased tree and the maximum value as a pair; `VTask.eraseMax` discards the maximum value and only returns the pruned tree.
