## Object

`VTask.glue` concatenates two ordered node trees into a single balanced ordered tree. It is a low-level internal operation that assumes its two inputs are already mutually consistent — that every element in the left tree is less than every element in the right tree, and that their sizes are within the required balance ratio of each other. Given those preconditions, it produces a single `Ordnode` containing exactly all elements from both inputs, maintaining order and balance.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.glue : {α : Type u_1} -> Ordnode α → Ordnode α → Ordnode α
<!-- PINNED-SIGNATURE:END -->


```
VTask.glue : {α : Type u_1} -> Ordnode α → Ordnode α → Ordnode α
```

The implicit type parameter `α` is the type of elements stored in the trees. The first explicit argument is the left subtree; the second is the right subtree. Both must be valid, balanced, ordered trees, and together they must satisfy the mutual balancing precondition (their sizes must not differ by more than the allowed factor `delta`).

## Conventions

When the left tree is `nil`, the function returns the right tree unchanged. When the right tree is `nil` (and the left is non-empty), it returns the left tree unchanged. These are sensible identity-like behaviours at the boundary.

## Worked Examples

- Claim: `VTask.glue Ordnode.nil Ordnode.nil = Ordnode.nil` — gluing two empty trees yields the empty tree.

- Claim: For any `Ordnode α` `t`, `VTask.glue Ordnode.nil t = t` — the empty left tree is an identity on the right.

- Claim: For any `Ordnode α` `t` of the form `node s l x r`, `VTask.glue (Ordnode.node s l x r) Ordnode.nil = Ordnode.node s l x r` — gluing a non-empty tree with the empty right tree returns the left tree unchanged.

- Claim: When both inputs are non-empty and balanced with respect to each other, the size of `VTask.glue l r` equals `size l + size r` — no elements are lost or duplicated.

## Boundaries

- If either argument is `nil`, the result is simply the other argument; no rebalancing is attempted.
- When both arguments are non-empty, the function extracts the maximum element from the left subtree (if the left is larger) or the minimum element from the right subtree (if the right is larger or equal), then calls a single rotation/balance step. This keeps the result balanced without a full rebuild.
- The function is **not** a general-purpose merge for arbitrarily-sized trees; correctness (both the ordering invariant and the balance invariant of the result) depends on the caller ensuring the two inputs are mutually ordered and their sizes are within the `delta`-ratio bound. Violating this precondition produces undefined behaviour from the perspective of the formal invariants.
- On equal-size inputs the right tree's minimum is extracted, i.e., the tie-breaking condition favors pulling from the right.

## Not to be confused with

- `Ordnode.merge`: A more general (and more expensive) merge that does **not** require the two trees to be size-balanced with respect to each other; it handles arbitrarily disparate sizes by recursively descending into both trees.
- `Ordnode.append` / `Ordnode.join`: Union-style operations that may also handle duplicate keys or unordered inputs, rather than assuming strict mutual ordering.
- `Ordnode.balanceL` / `Ordnode.balanceR`: Single-sided rebalancing primitives that correct a small imbalance on one side; `glue` uses these internally but operates on a fundamentally different problem (concatenation rather than one-sided repair).