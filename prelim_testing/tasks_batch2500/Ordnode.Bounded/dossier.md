## Object

`VTask.Bounded t lo hi` is a predicate asserting that the ordered-node tree `t` is a valid binary search tree (BST) relative to explicit lower and upper bounds. Concretely, it states two things simultaneously:

1. Every element `x` stored in `t` satisfies `lo < x < hi` (strict inequalities, with `lo` living in `WithBot α` so it can be `⊥` = no lower bound, and `hi` living in `WithTop α` so it can be `⊤` = no upper bound).
2. This invariant holds recursively: for every internal node with value `x`, left subtree `l`, and right subtree `r`, we have `Bounded l lo x` and `Bounded r x hi`, which together enforce the full BST ordering throughout the tree.

For the empty tree (`nil`) the predicate reduces to requiring `lo < hi` whenever both bounds are finite (i.e., not `⊥` or `⊤`); if either bound is infinite the empty tree trivially satisfies the predicate.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Bounded : {α : Type u_1} -> [Preorder α] -> Ordnode α → WithBot α → WithTop α → Prop
<!-- PINNED-SIGNATURE:END -->


VTask.Bounded : {α : Type u_1} -> [Preorder α] -> Ordnode α → WithBot α → WithTop α → Prop

The implicit type argument `α` is the type of elements stored in the tree; it carries a `Preorder` instance used for the strict-inequality comparisons. The first explicit argument is the ordered-node tree being checked. The second argument is the lower bound (in `WithBot α`): using `⊥` means there is no lower bound. The third argument is the upper bound (in `WithTop α`): using `⊤` means there is no upper bound.

## Conventions

When the tree is `nil` and both bounds are finite (i.e., `lo = some a` and `hi = some b`), the predicate requires `a < b` — the bounds must themselves be consistent even when there are no elements to check. When the tree is `nil` and at least one bound is infinite (`⊥` or `⊤`), the predicate holds trivially. Setting `lo = ⊥` and `hi = ⊤` expresses pure internal BST order with no external constraint.

## Worked examples

- Claim: `VTask.Bounded Ordnode.nil (⊥ : WithBot ℕ) (⊤ : WithTop ℕ)` holds (empty tree with no bounds).

- Claim: `VTask.Bounded Ordnode.nil (some (3 : ℕ) : WithBot ℕ) (some (5 : ℕ) : WithTop ℕ)` holds because `3 < 5`.

- Claim: `VTask.Bounded Ordnode.nil (some (5 : ℕ) : WithBot ℕ) (some (3 : ℕ) : WithTop ℕ)` does NOT hold because `5 < 3` is false.

- Claim: For the singleton tree `Ordnode.node 1 Ordnode.nil 4 Ordnode.nil`, the predicate `VTask.Bounded (Ordnode.node 1 Ordnode.nil 4 Ordnode.nil) (some (2 : ℕ) : WithBot ℕ) (some (7 : ℕ) : WithTop ℕ)` holds, because the node value `4` satisfies `2 < 4 < 7` and both subtrees are `nil` with consistent inner bounds.

- Claim: If `VTask.Bounded t lo hi` holds, then `VTask.Bounded t ⊥ ⊤` also holds (bounds can always be relaxed to infinite).

## Boundaries

- **Both bounds finite on `nil`**: `VTask.Bounded nil (some a) (some b)` is exactly the proposition `a < b`. If `a ≥ b`, the predicate is `False`.
- **One or both bounds infinite on `nil`**: the predicate is `True` regardless of the other bound.
- **Recursive case**: for a node, the predicate splits into two independent sub-predicates joined by `∧`; both must hold. The node's own value acts as the upper bound for the left subtree and the lower bound for the right subtree, threading the BST invariant through the whole tree.
- **Weakening is always valid**: `VTask.Bounded t lo hi → VTask.Bounded t ⊥ ⊤`. More precisely, any finite bound can be replaced by the corresponding infinite bound and the predicate is preserved.
- **Duality**: `VTask.Bounded t lo hi` on `α` corresponds to `VTask.Bounded (dual t) hi lo` on the order-dual `αᵒᵈ`.
- **Consistency implication**: `VTask.Bounded t (some a) (some b)` (with `t` non-empty or by the nil case) always implies `a < b`.

## Not to be confused with

- `Ordnode.Valid'`: a stronger validity predicate that combines `VTask.Bounded` with size-correctness and balance conditions; `VTask.Bounded` alone says nothing about tree balance or stored sizes.
- `Ordnode.All`: a predicate asserting a pointwise property holds for every element of the tree, without the recursive BST-ordering constraint between subtrees.
- `Ordnode.BST`: a predicate that may assert BST order without tracking explicit external bounds, whereas `VTask.Bounded` always carries explicit lower and upper bounds as arguments.