## VTask.numLeaves

### Object
The number of leaves of a binary tree. A binary tree is either empty (a single leaf, `nil`) or an internal node with a value and two subtrees (`node`). The leaf count of a tree is the total number of `nil` nodes it contains — equivalently, the number of positions where a new node could be inserted. Every `nil` contributes exactly one leaf, and every internal node contributes no leaves directly but combines the leaf counts of its two subtrees.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.numLeaves : {α : Type u} -> BinaryTree α → ℕ
<!-- PINNED-SIGNATURE:END -->

`VTask.numLeaves : {α : Type u} -> BinaryTree α → ℕ`

The implicit type argument `α` is the type of values stored at internal nodes (leaves carry no data). The explicit argument is the binary tree whose leaves are to be counted.

### Conventions
The empty tree (`nil`) is treated as a single leaf and contributes 1 to the count. This is the standard convention for leaf-counting in full binary trees, where every tree (including the trivially empty one) has at least one leaf.

### Worked examples
- Claim: The nil tree has exactly 1 leaf.
  ```lean
  example : VTask.numLeaves (BinaryTree.nil (α := ℕ)) = 1 := by decide
  ```
- Claim: A single-node tree `node v nil nil` has exactly 2 leaves.
  ```lean
  example : VTask.numLeaves (BinaryTree.node 0 .nil .nil) = 2 := by decide
  ```
- Claim: A tree `node v nil (node w nil nil)` has 3 leaves.
  ```lean
  example : VTask.numLeaves (BinaryTree.node 0 .nil (.node 1 .nil .nil)) = 3 := by decide
  ```
- Claim: For any binary tree `t`, `VTask.numLeaves t ≥ 1`.

### Boundaries
- **Empty tree (`nil`):** Returns 1, not 0. The empty tree is itself a leaf.
- **Single internal node (`node v nil nil`):** Returns 2, since there are two `nil` children.
- **General tree with `n` internal nodes:** A full binary tree with `n` internal nodes has exactly `n + 1` leaves, which is consistent with this definition.
- The result is always a positive natural number (at least 1) for any well-formed `BinaryTree`.

### Not to be confused with
- **`BinaryTree.numNodes` (or similar):** Counts internal nodes only, not leaves; for a tree with `n` internal nodes the leaf count is `n + 1` and the node count is `n`.
- **Depth or height of a binary tree:** Measures the longest root-to-leaf path, not the total number of leaves.
- **A leaf-count that returns 0 for `nil`:** Some formulations treat `nil` as non-existent rather than as a leaf; this definition explicitly counts `nil` as one leaf.