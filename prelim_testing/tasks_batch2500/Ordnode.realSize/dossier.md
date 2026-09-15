## Object

Given an `Ordnode α` — a weight-balanced binary search tree node that caches its subtree size — `VTask.realSize` computes the **actual** number of elements stored in the tree by traversing every node and counting them one by one, completely ignoring the cached `size` field that each internal node carries. The result is a natural number equal to the true cardinality of the collection represented by the tree.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.realSize : {α : Type u_1} -> Ordnode α → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.realSize : {α : Type u_1} -> Ordnode α → ℕ`

The implicit type argument `α` is the element type stored in the tree. The explicit argument is the `Ordnode α` whose elements are to be counted.

## Conventions

No special junk-value or out-of-domain conventions are declared: the function is total and well-defined on every `Ordnode α`, including trees whose cached `size` field is incorrect or inconsistent.

## Worked examples

- Claim: `VTask.realSize (Ordnode.nil)` equals `0` — the empty tree has no elements.
  ```lean
  example : VTask.realSize (Ordnode.nil (α := Nat)) = 0 := by decide
  ```

- Claim: A single-element tree built as `Ordnode.node 1 Ordnode.nil x Ordnode.nil` has `VTask.realSize` equal to `1`, regardless of the stored size field.
  ```lean
  example : VTask.realSize (Ordnode.node 1 Ordnode.nil (42 : Nat) Ordnode.nil) = 1 := by decide
  ```

- Claim: A tree whose cached `size` field is deliberately wrong (e.g., 99) but which contains exactly 2 nodes still returns `VTask.realSize` equal to `2`.
  ```lean
  example : VTask.realSize
      (Ordnode.node 99
        (Ordnode.node 1 Ordnode.nil (1 : Nat) Ordnode.nil)
        2
        Ordnode.nil) = 2 := by decide
  ```

- Claim: For a well-formed tree with correct cached sizes, `VTask.realSize` agrees with `Ordnode.size`.

## Boundaries

- On `Ordnode.nil`, the result is `0` — the base case of the recursion.
- On `Ordnode.node _ l x r`, the result is `VTask.realSize l + VTask.realSize r + 1`, counting the root and recursing into both subtrees.
- The function is completely insensitive to the cached size value stored in each `node` constructor; it recomputes the count from scratch.
- Because `Ordnode` can in principle hold arbitrarily large trees, there is no upper bound enforced by the function itself; the result grows with the actual number of nodes.

## Not to be confused with

- `Ordnode.size` — returns the *cached* size field from the root node constructor directly, in O(1), and may be incorrect if the tree is malformed.
- `Ordnode.card` / membership-counting functions — count elements satisfying a predicate rather than all elements.
- `Ordnode.Valid` — a proposition asserting that the cached sizes are consistent with the real sizes, i.e., that `size t = VTask.realSize t` holds throughout the tree.