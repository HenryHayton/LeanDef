## Object

`VTask.Ioo a b` is the open interval $(a, b)$: the set of all elements $x$ of the ordered type $\alpha$ satisfying $a < x$ and $x < b$. Both endpoints are excluded.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Ioo : {α : Type u_1} -> [Preorder α] -> (a b : α) -> Set α
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> [Preorder α] -> (a b : α) -> Set α`

The implicit type argument `α` is the carrier type whose elements populate the interval. The instance argument supplies a preorder on `α`, providing the strict-inequality relation needed to define openness at both ends. The first explicit argument `a` is the lower (excluded) bound of the interval; the second explicit argument `b` is the upper (excluded) bound.

## Conventions

When `a ≥ b` in the given preorder, the interval `VTask.Ioo a b` is the empty set, because no element can simultaneously satisfy `a < x` and `x < b` when `b` is not strictly greater than `a`.

## Worked examples

- Claim: The integer `4` belongs to `VTask.Ioo (3 : ℤ) 7`, since `3 < 4` and `4 < 7`.

- Claim: The real number `π` belongs to `VTask.Ioo (3 : ℝ) 4`, since `3 < π < 4`.

- Claim: The element `1` does **not** belong to `VTask.Ioo (1 : ℤ) 5`, because the lower bound is excluded (`1 < 1` is false).

- Claim: `VTask.Ioo (3 : ℤ) 3` is empty, since equal bounds leave no room for a strict inequality on both sides simultaneously.

- Claim: `VTask.Ioo (5 : ℤ) 2` is empty, since the upper bound is less than the lower bound.

## Boundaries

- **Equal bounds** (`a = b`): The interval is empty. No element satisfies both `a < x` and `x < a`.
- **Reversed bounds** (`b < a`): The interval is also empty. The two strict inequalities `a < x` and `x < b` are jointly unsatisfiable.
- **Minimal/maximal elements**: If `α` has a minimum element `⊥`, then `VTask.Ioo ⊥ b` excludes `⊥` itself, containing only elements strictly between `⊥` and `b`.
- **Discrete types** (e.g., `ℤ`, `ℕ`): When `b = a + 1`, the interval is empty because there is no integer strictly between two consecutive integers.
- **Density**: In dense linear orders (e.g., `ℝ` or `ℚ`), `VTask.Ioo a b` is nonempty whenever `a < b`.

## Not to be confused with

- `Set.Icc a b`: the **closed** interval $[a, b]$, which includes both endpoints `a` and `b`.
- `Set.Ico a b`: the **half-open** interval $[a, b)$, which includes `a` but excludes `b`.
- `Set.Ioc a b`: the **half-open** interval $(a, b]$, which excludes `a` but includes `b`.
