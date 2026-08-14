## 1. Object

`VTask.WCovBy a b` is the **weak cover** relation on a preorder: it holds when `a` is either equal to `b` or is *covered* by `b`, meaning `a ≤ b` and no element lies strictly between `a` and `b`. Equivalently, it is the reflexive closure of the (strict) cover relation. The notation used in Mathlib is `a ⩿ b`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.WCovBy : {α : Type u_1} -> [Preorder α] -> (a b : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.WCovBy : {α : Type u_1} -> [Preorder α] -> (a b : α) -> Prop`

The type `α` is an implicit type parameter; it must carry a preorder instance (also implicit). The explicit arguments `a` and `b` are the two elements of `α` being compared: the relation asserts that `a` is weakly covered by `b`, i.e., `a` is below `b` with nothing strictly in between.

## 3. Conventions

The relation is reflexive: every element weakly covers itself, so `VTask.WCovBy a a` holds for any `a`. When `a ≠ b` (or equivalently when `a < b`), `VTask.WCovBy a b` is the same as the strict cover relation.

## 4. Worked examples

- Claim: In ℕ with the usual order, `VTask.WCovBy 3 3` holds (reflexivity).

- Claim: In ℕ with the usual order, `VTask.WCovBy 3 4` holds, since 3 ≤ 4 and there is no natural number strictly between 3 and 4.

- Claim: In ℕ with the usual order, `VTask.WCovBy 3 5` does not hold, because 4 lies strictly between 3 and 5.

- Claim: For any preorder, if `VTask.WCovBy a b` holds then `a ≤ b`.

## 5. Boundaries

- **Reflexivity:** `VTask.WCovBy a a` always holds for any element `a`, because `a ≤ a` and the vacuously-true no-betweenness condition is satisfied (nothing can satisfy `a < c < a`).
- **Antisymmetric case:** If both `VTask.WCovBy a b` and `VTask.WCovBy b a` hold, then `a` and `b` are equivalent under the preorder (i.e., `a ≤ b` and `b ≤ a`), and the two weak covers are compatible.
- **Non-transitivity:** `VTask.WCovBy` is generally not transitive; if `a ⩿ b` and `b ⩿ c` with `a < b < c`, then transitivity would require no element between `a` and `c`, which may fail.
- **Interval characterisation:** `VTask.WCovBy a b` holds if and only if the open interval `(a, b)` is empty (combined with `a ≤ b`).
- **Relation to strict cover:** When `a ≠ b`, `VTask.WCovBy a b` is equivalent to the strict cover `a ⋖ b`.

## 6. Not to be confused with

- **`CovBy a b` (strict cover, `a ⋖ b`):** Requires `a < b` (strictly), so it does not include the reflexive case `a = b`. `VTask.WCovBy` is the reflexive closure of `CovBy`.
- **`a ≤ b` (ordinary `LE`):** The `≤` relation allows elements strictly between `a` and `b`; `VTask.WCovBy` additionally forbids any such intermediate element.
- **`a < b` (strict order):** The strict order merely requires `a ≤ b` and `a ≠ b`, with no constraint on intermediate elements.
