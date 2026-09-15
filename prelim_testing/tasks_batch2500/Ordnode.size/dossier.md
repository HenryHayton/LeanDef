## Object

`VTask.size` returns the number of elements stored in an ordered node tree (`Ordnode α`). It is an O(1) operation that reads the cached size tag stored inside each internal node, returning 0 for the empty tree.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.size : {α : Type u_1} -> Ordnode α → ℕ
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> Ordnode α → ℕ`

The implicit type parameter `α` is the type of values stored in the tree. The explicit argument is the ordered node tree whose element count is to be retrieved.

## Conventions

The empty tree (`nil`) has size 0. Internal nodes carry a cached size field that is trusted to accurately reflect the count of all elements in that subtree; `VTask.size` reads this field directly without re-traversing the tree.

## Worked examples

- Claim: `VTask.size (Ordnode.nil)` equals `0`
  ```lean
  example : VTask.size (Ordnode.nil (α := Nat)) = 0 := by decide
  ```

- Claim: A single-node tree containing one element has size 1
  ```lean
  example : VTask.size (Ordnode.node 1 Ordnode.nil 42 Ordnode.nil) = 1 := by decide
  ```

- Claim: The example from the docstring — a tree whose node stores size tag 3 and contains distinct elements analogous to `{2, 1, 4}` — has `VTask.size` equal to 3, reflecting the cached tag, not a re-count.

- Claim: `VTask.size` always returns a natural number (non-negative), so the result is always `≥ 0`.

## Boundaries

- On `Ordnode.nil` the result is exactly `0`.
- On any `Ordnode.node sz _ _ _` the result is exactly `sz`, the cached size tag. If the tree was constructed with an incorrect tag (not through the safe API), `VTask.size` will faithfully return that incorrect tag rather than the true element count.
- There is no upper bound imposed by the function itself; any `ℕ` value stored as the size tag can be returned.

## Not to be confused with

- `Ordnode.card` or similar functions that may traverse the tree to count elements, rather than reading a cached field.
- The `sz` field of an `Ordnode.node` constructor directly — `VTask.size` provides a uniform interface that also handles `nil`, returning 0, whereas pattern-matching on the constructor requires separate handling.
- `Finset.card`, which counts elements of a `Finset` and involves a different data structure entirely.