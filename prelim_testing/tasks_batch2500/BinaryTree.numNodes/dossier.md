## VTask.numNodes

### Object

The function counts the number of **internal nodes** in a binary tree — that is, the nodes that carry a value and have two subtrees. Leaves (the empty tree, `nil`) are not counted. For a fully explicit finite tree, `numNodes` returns the total count of branching points in the tree's structure.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.numNodes : {α : Type u} -> BinaryTree α → ℕ
<!-- PINNED-SIGNATURE:END -->


The implicit argument `α` is the type of values stored at each internal node. The single explicit argument is the binary tree whose internal nodes are to be counted.

### Conventions

The empty tree (`nil`) has zero internal nodes; this is the base case and the unique tree with `numNodes` equal to zero.

### Worked Examples

- Claim: `VTask.numNodes (BinaryTree.nil)` equals `0` — the empty tree has no internal nodes.
  ```lean
  example : VTask.numNodes (BinaryTree.nil (α := ℕ)) = 0 := by decide
  ```

- Claim: A single-node tree `node 42 nil nil` has exactly 1 internal node.
  ```lean
  example : VTask.numNodes (BinaryTree.node 42 BinaryTree.nil BinaryTree.nil) = 1 := by decide
  ```

- Claim: For a tree `node 1 (node 2 nil nil) (node 3 nil nil)`, `numNodes` returns 3 (the root plus its two children).
  ```lean
  example : VTask.numNodes
      (BinaryTree.node 1
        (BinaryTree.node 2 BinaryTree.nil BinaryTree.nil)
        (BinaryTree.node 3 BinaryTree.nil BinaryTree.nil)) = 3 := by decide
  ```

- Claim: For a right-spine tree of depth 3, `numNodes` returns 3.
  ```lean
  example : VTask.numNodes
      (BinaryTree.node 1 BinaryTree.nil
        (BinaryTree.node 2 BinaryTree.nil
          (BinaryTree.node 3 BinaryTree.nil BinaryTree.nil))) = 3 := by decide
  ```

### Boundaries

- **Empty tree (`nil`)**: `numNodes nil = 0`. This is the only tree with zero internal nodes.
- **Single node**: A tree consisting of one node with two `nil` children returns `1`.
- **Leaves are not counted**: `nil` subtrees contribute nothing to the count; only `node` constructors are counted.
- **Additivity**: The count for a `node` tree is exactly the sum of the counts of its left and right subtrees, plus one for the node itself.

### Not to be confused with

- **`BinaryTree.numLeaves`** (if present): counts `nil` leaves rather than internal `node` constructors; for a tree with `n` internal nodes, the number of leaves is `n + 1`.
- **`BinaryTree.height` / `depth`**: measures the length of the longest root-to-leaf path, not the total count of nodes.
- **Size functions that count all constructors**: some tree-size functions count both leaves and nodes; `numNodes` counts only the internal `node` constructors.