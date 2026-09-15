## VTask.findMax'

### Object
`VTask.findMax'` returns the maximum element stored in an ordered binary tree (`Ordnode α`). If the tree is empty, it returns a caller-supplied default value instead. When the tree is non-empty and the elements are stored in sorted order (as the `Ordnode` invariant requires), the result is the largest element in the tree.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.findMax' : {α : Type u_1} -> α → Ordnode α → α
<!-- PINNED-SIGNATURE:END -->

`VTask.findMax' : {α : Type u_1} -> α → Ordnode α → α`

The first (explicit) argument is the default value to return when the tree is empty; it acts as a fallback and its type determines the element type `α`. The second argument is the ordered binary tree being queried.

### Conventions
When the tree is empty (`nil`), the function returns the supplied default value unchanged — there is no notion of failure or `Option`; the default is the junk/fallback value for the empty case.

### Worked examples
- Claim: `VTask.findMax' 37 (Ordnode.nil) = 37`
  ```lean
  example : VTask.findMax' 37 (Ordnode.nil) = 37 := by decide
  ```
- Claim: `VTask.findMax' 37 {1, 2, 3} = 3` (where `{1,2,3}` denotes the `Ordnode` containing 1, 2, and 3)
  ```lean
  example : VTask.findMax' 37
    (Ordnode.node 3
      (Ordnode.node 1 Ordnode.nil 1 Ordnode.nil)
      2
      (Ordnode.node 1 Ordnode.nil 3 Ordnode.nil)) = 3 := by decide
  ```
- Claim: For a singleton tree containing only `5`, `VTask.findMax' 0 (singleton 5) = 5`.

### Boundaries
- **Empty tree**: `VTask.findMax' d Ordnode.nil = d` for any default `d`. The default value is returned as-is.
- **Singleton tree**: `VTask.findMax' d (singleton x) = x`; the default is ignored because the tree is non-empty.
- **The default value is completely ignored** whenever the tree contains at least one element; its value is irrelevant in that case.
- The function assumes the `Ordnode` invariant (elements in sorted order) in order for the returned value to be the true maximum; if the tree violates the invariant the result is merely the rightmost spine's root, not necessarily the largest element.

### Not to be confused with
- `Ordnode.findMax` (the `Option`-returning variant): returns `none` on an empty tree instead of a default value.
- `Ordnode.findMin'`: the symmetric function that returns the *minimum* element (walking the left spine instead of the right).
- `Ordnode.max` or `max` on ordered types: a pairwise comparison, not a tree traversal.