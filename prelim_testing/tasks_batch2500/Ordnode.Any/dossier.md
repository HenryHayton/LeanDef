## Object

`VTask.Any P t` is a proposition asserting that at least one element of the ordered-node tree `t` satisfies the predicate `P`. It is the existential counterpart to `All`, which requires every element to satisfy `P`. On the empty tree it is vacuously false; on a non-empty tree it holds as soon as *any* element—whether in the left subtree, the root, or the right subtree—satisfies `P`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Any : {α : Type u_1} -> (P : α → Prop) -> Ordnode α → Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.Any : {α : Type u_1} -> (P : α → Prop) -> Ordnode α → Prop
```

The implicit type argument `α` is the type of values stored in the tree. `P` is the predicate being tested: a function from elements of `α` to `Prop`. The second explicit argument is the `Ordnode α` tree whose elements are being searched.

## Conventions

There are no junk-value or boundary conventions to declare for this definition: the predicate is structurally total over all `Ordnode α` trees, returns `False` on the empty tree (`nil`) as the natural identity for disjunction, and uses straightforward left-subtree / root / right-subtree disjunction on nodes. No sentinel or junk values arise.

## Worked examples

- Claim: `VTask.Any (fun x => x < 2) (Ordnode.singleton 1)` is equivalent to `True`, i.e., it holds because `1 < 2`.

- Claim: `VTask.Any (fun x => x < 2) (Ordnode.nil)` is `False`, since the empty tree contains no elements.

- Claim: `VTask.Any (fun x => x = 3) (Ordnode.singleton 3) ↔ True` follows from `Ordnode.any_singleton`, since `3 = 3`.

- Claim: For any tree `t` and predicate `P`, `VTask.Any P t ↔ ∃ x, Ordnode.Emem x t ∧ P x` (this is `any_iff_exists`).

- Claim: If `P` implies `Q` pointwise, then `VTask.Any P t` implies `VTask.Any Q t` (this is `Any.imp`).

## Boundaries

- **Empty tree (`nil`)**: `VTask.Any P nil` is always `False`, regardless of `P`. There are no elements to witness the existential.
- **Singleton tree**: `VTask.Any P (singleton x)` is logically equivalent to `P x` alone.
- **Non-constructive predicates**: Because `VTask.Any P t` is a `Prop`, it may not be computationally decidable unless `P` itself is decidable. No `Decidable` instance is provided in general.
- **Tree structure vs. content**: The `Ordnode` carries a size annotation in each node, but `VTask.Any` is insensitive to it; only the stored values and tree shape matter.

## Not to be confused with

- `Ordnode.All P t`: the universal counterpart, requiring *every* element to satisfy `P`; `VTask.Any` is its existential dual.
- `Ordnode.Emem x t`: membership of a *specific* element `x` in `t`; `VTask.Any` quantifies over *all* elements with an arbitrary predicate rather than checking a fixed value.
- `Ordnode.find` or `Ordnode.any` (boolean): a computable Boolean function returning `true` if some element satisfies a decidable predicate; `VTask.Any` is a proposition, not a boolean computation.