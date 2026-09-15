## Object

`VTask.Compares o a b` is a proposition that expresses the ordering relationship between two elements `a` and `b` of a type equipped with a less-than relation, according to the tag `o` drawn from the three-valued type `Ordering`. Concretely:
- when `o = lt`, it asserts `a < b`;
- when `o = eq`, it asserts `a = b`;
- when `o = gt`, it asserts `a > b` (i.e., `b < a`).

It provides a uniform, case-dispatching way to talk about all three possible strict-ordering outcomes between two elements.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Compares : {α : Type u_1} -> [LT α] -> Ordering → α → α → Prop
<!-- PINNED-SIGNATURE:END -->


VTask.Compares : {α : Type u_1} -> [LT α] -> Ordering → α → α → Prop

The implicit type argument `α` is the carrier type on which comparison is performed. The instance argument supplies the less-than relation `<` on `α`. The first explicit argument `o : Ordering` is the ordering tag (`lt`, `eq`, or `gt`) whose meaning is being asserted. The second explicit argument `a : α` is the left-hand element being compared. The third explicit argument `b : α` is the right-hand element being compared.

## Conventions

There are no junk-value conventions to declare: the definition is total over all three constructors of `Ordering` and all elements of any type with a `LT` instance, so every combination of inputs yields a well-formed proposition.

## Worked examples

- Claim: For natural numbers, `VTask.Compares Ordering.lt 2 5` is exactly the proposition `2 < 5`.

- Claim: For natural numbers, `VTask.Compares Ordering.eq 3 3` is exactly the proposition `3 = 3`.

- Claim: For natural numbers, `VTask.Compares Ordering.gt 7 4` is exactly the proposition `4 < 7` (i.e., `7 > 4`).

- Claim: If `h : VTask.Compares Ordering.lt a b` holds in a preorder, then `a ≤ b` follows from `le_of_lt h`.

## Boundaries

- At `o = lt`: the proposition is `a < b`, which may be `False` for equal or reversed elements.
- At `o = eq`: the proposition is `a = b` (propositional equality), independent of any order structure beyond `LT`.
- At `o = gt`: the proposition is `b < a`, using the same underlying `<` as the `lt` case but with arguments swapped.
- The type `α` need only carry a `LT` instance; no `Preorder` or `LinearOrder` axioms (such as transitivity or totality) are required for `VTask.Compares` itself to be stated, though many consequences about it require stronger hypotheses.
- When `a = b` in a type where `<` is irreflexive, `VTask.Compares Ordering.lt a a` and `VTask.Compares Ordering.gt a a` are both `False`, while `VTask.Compares Ordering.eq a a` is `True`.
- If `VTask.Compares o a b` and `VTask.Compares o' a b` both hold in a preorder, then `o = o'` (injectivity), so at most one ordering tag can be witnessed for a given pair.

## Not to be confused with

- `cmp : α → α → Ordering` (for `LinearOrder α`): a computable function that *returns* an `Ordering` value, rather than a proposition asserting a relationship; `VTask.Compares` is the bridge between `cmp`'s output and the underlying order relations.
- `Ordering.swap`: swaps `lt` and `gt` tags; `VTask.Compares o.swap a b` is equivalent to `VTask.Compares o b a`, not the same as `VTask.Compares o a b`.
- `LE` / `le`: the non-strict ≤ relation, which conflates the `lt` and `eq` cases that `VTask.Compares` distinguishes separately.
