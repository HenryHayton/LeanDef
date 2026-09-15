## Object

`VTask.res x n` is the finite list consisting of the first `n` entries of the sequence `x : ℕ → α`, listed in **reverse index order**: the element at index `n-1` appears first, then `n-2`, …, then `x 0` last. Concretely, `res x n = [x(n-1), x(n-2), …, x(1), x(0)]`. It captures exactly the data of `x` on the initial segment `{0, 1, …, n-1}`, and its length equals `n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.res : {α : Type u_2} -> (x : ℕ → α) -> ℕ → List α
<!-- PINNED-SIGNATURE:END -->


`VTask.res : {α : Type u_2} -> (x : ℕ → α) -> ℕ → List α`

The implicit type argument `α` is the common codomain of the sequence. The argument `x` is the sequence being restricted — a function from natural numbers to `α`. The second explicit argument `n` is the length of the restriction, i.e., how many terms of `x` are captured; entries `x 0` through `x (n-1)` appear in the resulting list.

## Conventions

When `n = 0` the result is the empty list `[]`, capturing no entries of `x`.

## Worked examples

- Claim: `VTask.res (fun n => n) 0 = []`
  ```lean
  example : VTask.res (fun n => n) 0 = [] := by decide
  ```

- Claim: `VTask.res (fun n => n) 3 = [2, 1, 0]`
  ```lean
  example : VTask.res (fun n => n) 3 = [2, 1, 0] := by decide
  ```

- Claim: `(VTask.res (fun n => n) 5).length = 5`
  ```lean
  example : (VTask.res (fun n => n) 5).length = 5 := by decide
  ```

- Claim: For any sequence `x : ℕ → α` and `n : ℕ`, `VTask.res x (n + 1) = x n :: VTask.res x n` (the successor step prepends `x n` to the restriction of length `n`).

## Boundaries

- At `n = 0`: the result is always `[]`, regardless of `x`.
- At `n = 1`: the result is the singleton `[x 0]`.
- The function is total for all `n : ℕ`; there is no upper bound on `n`.
- `VTask.res` is injective as a function of `x`: if `res x = res y` (as functions `ℕ → List α`), then `x = y`. Equivalently, `res x n = res y n` if and only if `x` and `y` agree on all indices strictly less than `n`.

## Not to be confused with

- `List.take`: takes the first `n` elements of a *list* (index-ascending order); `VTask.res` operates on a *sequence* and produces entries in descending index order.
- `PiNat.cylinder x n`: the *set* of sequences agreeing with `x` on the first `n` indices; `VTask.res x n` is the *list* encoding that same initial data, and `cylinder x n = { y | res y n = res x n }`.
- `Finset.image` or other truncations of functions: those produce sets or finsets, not ordered lists retaining the index structure.