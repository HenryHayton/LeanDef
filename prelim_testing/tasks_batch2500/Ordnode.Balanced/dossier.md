## 1. Object

`VTask.Balanced t` is the proposition asserting that an ordered-node binary tree `t` satisfies the **height-balance invariant at every level**. Concretely, at each internal node the sizes of the left and right subtrees must satisfy the `BalancedSz` relation (which encodes the weight-balanced-tree invariant: neither subtree is more than a constant factor `delta` heavier than the other, with a small-tree exception), and this must hold recursively throughout the entire tree.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Balanced : {α : Type u_1} -> Ordnode α → Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Balanced : {α : Type u_1} -> Ordnode α → Prop`

The implicit type parameter `α` is the type of values stored in the tree. The single explicit argument is the `Ordnode α` tree whose global balance is being asserted.

## 3. Conventions

The empty tree (`nil`) is always considered balanced; `VTask.Balanced nil` holds trivially. Balance is a purely structural (size-based) property: it does not depend on the ordering of elements, only on the sizes of subtrees at every node.

## 4. Worked examples

- Claim: The empty `Ordnode` tree is balanced.
- Claim: A single-node tree (a leaf, with `nil` left and right children) is balanced, because `BalancedSz 0 0` holds and both children trivially satisfy the property.
- Claim: If a tree `t` satisfies `VTask.Balanced t`, then its mirror image (obtained by the `dual` operation) also satisfies `VTask.Balanced (dual t)` — formally `Balanced.dual`.
- Claim: A node whose left subtree has size 3 and whose right subtree has size 1 is balanced at that node, because `BalancedSz 3 1` holds (3 ≤ delta * 1 = 3).

## 5. Boundaries

- **Empty tree**: `VTask.Balanced nil` is `True` by definition; no base case can fail.
- **Single internal node with two empty children**: requires `BalancedSz 0 0`, which holds because `0 + 0 ≤ 1`.
- **Heavily skewed trees**: a tree where one subtree is more than `delta` times the size of the other will not satisfy `VTask.Balanced`, even if each individual subtree is itself balanced.
- **Size metadata**: the balance check uses stored size annotations (`size l`, `size r`), so a tree with inconsistent size fields may report unexpected balance behaviour; correct usage assumes the size fields are accurate.

## 6. Not to be confused with

- `BalancedSz l r` — the two-natural-number predicate expressing that sizes `l` and `r` are balanced relative to each other at a single node; `VTask.Balanced` is the recursive lift of this predicate to whole trees.
- `Ordnode.Valid'` — the stronger full validity predicate, which combines balance with correct size annotations and ordering of elements; `VTask.Balanced` alone says nothing about element order or size-field correctness.
- Height-balanced (AVL) trees — `VTask.Balanced` uses a weight/size-based balance criterion (bounded ratio of subtree sizes), not a height-difference criterion.