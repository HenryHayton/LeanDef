## 1. Object

`VTask.findGreatest P n` computes the largest natural number `i` with `i ≤ n` for which the predicate `P i` holds. If no such positive `i` exists (i.e., `P` fails at every positive integer up to `n`), the function returns `0`. In other words, it is the argmax-style search for the greatest witness to `P` within the initial segment `{0, 1, …, n}`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.findGreatest : (P : ℕ → Prop) -> [DecidablePred P] -> ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.findGreatest : (P : ℕ → Prop) -> [DecidablePred P] -> ℕ → ℕ`

The first argument `P` is the decidable predicate being tested: a property of natural numbers whose truth or falsity can be determined algorithmically at each point. The instance argument `[DecidablePred P]` supplies the decision procedure for `P`, enabling the function to branch on whether `P` holds at each candidate. The final argument `n` is the upper bound of the search; only indices in `{0, 1, …, n}` are considered.

## 3. Conventions

When no positive index `i` with `1 ≤ i ≤ n` satisfies `P i`, the function returns `0` regardless of whether `P 0` holds. In particular, `0` is the universal default/junk value when no witness is found in the positive part of the range, even if `P 0` is true.

## 4. Worked examples

- Claim: `VTask.findGreatest (fun _ => False) 10 = 0` — searching with an always-false predicate over any bound returns 0.
  ```lean
  example : VTask.findGreatest (fun _ => False) 10 = 0 := by decide
  ```

- Claim: `VTask.findGreatest (fun i => i % 2 = 0) 7 = 6` — the largest even number ≤ 7 is 6.
  ```lean
  example : VTask.findGreatest (fun i => i % 2 = 0) 7 = 6 := by decide
  ```

- Claim: `VTask.findGreatest (fun i => i = 3) 5 = 3` — the only witness is 3, which is within the bound 5.
  ```lean
  example : VTask.findGreatest (fun i => i = 3) 5 = 3 := by decide
  ```

- Claim: `VTask.findGreatest (fun _ => True) 0 = 0` — with upper bound 0, the only candidate is 0; the result is 0 (the default).
  ```lean
  example : VTask.findGreatest (fun _ => True) 0 = 0 := by decide
  ```

## 5. Boundaries

- **Bound is 0**: `VTask.findGreatest P 0 = 0` always, since the only candidate is index 0 and the function returns 0 unconditionally at this base case.
- **No positive witness exists**: If `P i` is false for every `1 ≤ i ≤ n`, the result is 0, even when `P 0` might be true.
- **Result satisfies P (when nonzero)**: If the output `m` is nonzero, then `P m` holds. The result 0 does not guarantee `P 0`.
- **Result is bounded by `n`**: `VTask.findGreatest P n ≤ n` always holds.
- **Maximality**: For any `k` with `VTask.findGreatest P n < k ≤ n`, `P k` is false; the result is genuinely the largest witness.
- **Monotone in the bound**: Increasing the upper bound `n` can only increase or maintain the result.

## 6. Not to be confused with

- `Nat.find`: finds the *smallest* natural number satisfying a predicate (requires the predicate to hold somewhere), whereas `VTask.findGreatest` finds the *largest* within a bounded range and returns 0 by default.
- `Finset.sup`: computes the supremum of a function over a finite set, a more general algebraic notion rather than a bounded linear search.
- A bounded minimizer: `VTask.findGreatest` searches for a maximum, not a minimum; the two are not interchangeable even when a unique witness exists.