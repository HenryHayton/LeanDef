## VTask.findMin'

### Object
`VTask.findMin'` returns the minimum element stored in an ordered binary tree (`Ordnode α`). If the tree is non-empty, it traverses leftward to locate the smallest element according to the tree's ordering. If the tree is empty, it returns a caller-supplied default value.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.findMin' : {α : Type u_1} -> Ordnode α → α → α
<!-- PINNED-SIGNATURE:END -->

`VTask.findMin' : {α : Type u_1} -> Ordnode α → α → α`

The first argument is the ordered binary tree to search. The second argument is a default value of type `α`, returned when the tree is empty.

### Conventions
When the tree is empty (`nil`), the function returns the default value exactly as supplied, rather than raising an error or using any distinguished bottom element.

### Worked examples
- Claim: `VTask.findMin' (Ordnode.node 3 (Ordnode.node 1 Ordnode.nil 1 Ordnode.nil) 2 Ordnode.nil) 99 = 1`
- Claim: On the empty tree, `VTask.findMin' Ordnode.nil 37 = 37`
  ```lean
  example : VTask.findMin' Ordnode.nil 37 = 37 := by decide
  ```
- Claim: For a single-node tree containing value `5`, `VTask.findMin' (Ordnode.node 1 Ordnode.nil 5 Ordnode.nil) 99 = 5`
  ```lean
  example : VTask.findMin' (Ordnode.node 1 Ordnode.nil 5 Ordnode.nil) 99 = 5 := by decide
  ```

### Boundaries
- **Empty tree**: Returns the default value verbatim; the default plays no role when the tree is non-empty.
- **Single-node tree**: The single element is both the minimum and maximum; the default is ignored and that element is returned.
- **Left-skewed tree**: The function correctly descends all the way to the leftmost leaf.
- **Type generality**: Works for any type `α`; no ordering constraint on `α` is required by the function itself — correctness as a minimum-finder relies on the caller maintaining the `Ordnode` invariant.

### Not to be confused with
- `Ordnode.findMin` (if it exists): a version that returns an `Option α` instead of requiring a default, returning `none` on an empty tree.
- `VTask.findMax'`: the symmetric function that traverses rightward to find the maximum element.
- `Ordnode.min`: a field or projection that might store a cached minimum, rather than computing it by traversal.