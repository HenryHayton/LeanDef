## VTask.Sized

### Object

`VTask.Sized t` is a predicate on an ordered-node tree `t` that asserts every internal node stores the correct cached size: the `size` field of each node equals the total number of nodes in its left subtree plus the total number of nodes in its right subtree plus one (for the node itself). In other words, the tree's stored size annotations are everywhere consistent with the actual shape of the tree. The empty tree (`nil`) trivially satisfies the predicate.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Sized : {α : Type u_1} -> Ordnode α → Prop
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> Ordnode α → Prop`

The implicit type parameter `α` is the type of values stored in the tree's nodes (it does not affect the size-consistency condition). The explicit argument is the ordered-node tree whose size annotations are being checked.

### Conventions

The predicate is trivially true for the empty tree (`nil`): there are no size fields to be wrong.

### Worked examples

- Claim: `VTask.Sized (Ordnode.nil)` holds because the empty tree has no size annotations to be inconsistent.

- Claim: A single-node tree `Ordnode.node 1 Ordnode.nil v Ordnode.nil` satisfies `VTask.Sized`, because `1 = 0 + 0 + 1` and both subtrees (both `nil`) trivially satisfy the predicate.

- Claim: If a node carries a wrong size, e.g., `Ordnode.node 5 Ordnode.nil v Ordnode.nil`, then `VTask.Sized` fails, because `5 ≠ 0 + 0 + 1`.

- Claim: If `VTask.Sized l` and `VTask.Sized r` both hold, then the tree produced by `Ordnode.node' l x r` also satisfies `VTask.Sized`, because `node'` computes the correct size automatically.

- Claim: For any tree `t`, `VTask.Sized t` is preserved under `Ordnode.dual`, i.e., `VTask.Sized t ↔ VTask.Sized (Ordnode.dual t)`, since mirroring a tree does not change its sizes.

### Boundaries

- On `nil`: the predicate holds unconditionally; there are no fields to check.
- On a node whose stored size is zero: the predicate fails (since `size l + size r + 1 ≥ 1 > 0`), which is consistent with the theorem that a `Sized` node always has a positive size field.
- The predicate is defined recursively down to every subtree, so a node at the root can fail even if its own size field is locally correct but a deeply nested node has a wrong annotation.
- `VTask.Sized` says nothing about the relative ordering of keys or the balance factor; it is purely about size-field correctness.

### Not to be confused with

- `Ordnode.Balanced`: a separate invariant asserting that subtree sizes are in the correct weight-balanced ratio; distinct from size-annotation consistency.
- `Ordnode.size`: the function that reads the cached size field from a node, which may or may not equal the actual number of nodes if `Sized` is not assumed.
- `Ordnode.Valid`: a combined validity predicate that bundles `Sized` together with balance and ordering invariants; strictly stronger than `VTask.Sized` alone.