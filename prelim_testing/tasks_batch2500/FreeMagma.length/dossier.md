## Object

`VTask.length` counts the number of generators (leaves) in an element of the free magma over an alphabet `α`. A free magma is the simplest binary-tree-like algebraic structure: it is either a single generator `of a` (a leaf) or a product `x * y` of two smaller elements (an internal node). The length is exactly the number of leaves in this binary tree, i.e., the total count of generators used, with multiplicity.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.length : {α : Type u} -> FreeMagma α → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.length : {α : Type u} -> FreeMagma α → ℕ`

The implicit type argument `α` is the alphabet (type of generators) over which the free magma is built. The explicit argument is the free magma element whose generator count is to be computed.

## Conventions

There are no junk-value or boundary conventions to declare: the function is total by structural recursion and every case is handled canonically by the definition.

## Worked examples

- Claim: A single generator `FreeMagma.of x` has length 1, for any `x : α`.
  ```lean
  example (α : Type*) (x : α) : VTask.length (FreeMagma.of x) = 1 := by rfl
  ```

- Claim: The product of two elements has length equal to the sum of their lengths, e.g., `(FreeMagma.of a) * (FreeMagma.of b)` has length 2.
  ```lean
  example (α : Type*) (a b : α) : VTask.length (FreeMagma.of a * FreeMagma.of b) = 2 := by rfl
  ```

- Claim: Length is always at least 1 (every free magma element contains at least one generator).

- Claim: For a three-leaf tree `(FreeMagma.of a * FreeMagma.of b) * FreeMagma.of c`, the length is 3.
  ```lean
  example (α : Type*) (a b c : α) : VTask.length ((FreeMagma.of a * FreeMagma.of b) * FreeMagma.of c) = 3 := by rfl
  ```

## Boundaries

- The minimum possible length is 1, achieved by any single generator `FreeMagma.of a`. There is no free magma element of length 0.
- The function is additive over products: `length (x * y) = length x + length y` for all `x y : FreeMagma α`.
- The function does not depend on the specific values of generators, only on the tree structure (the shape of nesting and number of leaves).
- Since `FreeMagma α` is inductively generated, the function is well-defined and total for all elements.

## Not to be confused with

- `List.length`: counts elements in a list, not leaves in a free magma binary tree; unrelated structure.
- `Multiset.card` or `Finset.card`: cardinality of a (multi)set of generators, which would ignore multiplicity or order differently; `VTask.length` counts leaves with multiplicity in tree order.
- Depth or height of the binary tree: those measure the longest path from root to leaf, not the total leaf count.