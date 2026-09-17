## Object

`VTask.succ'` computes the successor of a `Num` value and returns it as a `PosNum`. Since the successor of any non-negative binary natural number is always strictly positive, the return type is `PosNum` rather than `Num`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.succ' : Num → PosNum
<!-- PINNED-SIGNATURE:END -->


`VTask.succ' : Num → PosNum`

The single argument is a binary natural number of type `Num` (which can be zero or a positive binary numeral). The function returns the successor — i.e., the value one greater — as a `PosNum`, reflecting that the result is always at least 1.

## Conventions

No special junk-value or edge conventions are declared: the function is total on all `Num` inputs and its return type (`PosNum`) naturally excludes zero, so no sentinel or overflow behavior is needed.

## Worked examples

- Claim: `VTask.succ' 0 = 1`
  ```lean
  example : VTask.succ' 0 = 1 := by decide
  ```

- Claim: `VTask.succ' (Num.pos 1) = PosNum.succ 1`
  ```lean
  example : VTask.succ' (Num.pos 1) = PosNum.succ 1 := by decide
  ```

- Claim: `VTask.succ' 3 = 4`
  ```lean
  example : VTask.succ' 3 = 4 := by decide
  ```

- Claim: The result of `VTask.succ'` always represents a natural number one greater than the input, i.e., `(VTask.succ' n : ℕ) = (n : ℕ) + 1` for all `n : Num`.

## Boundaries

- At `Num.zero` (the value `0`): the function returns `PosNum.one` (`1`), the smallest possible `PosNum`.
- At any `Num.pos p`: the function delegates to the `PosNum` successor function, producing the `PosNum` one step above `p`.
- The return type `PosNum` guarantees the result is never zero, making this a safe way to produce a positive numeral from any `Num`.

## Not to be confused with

- `PosNum.succ`: the successor function on `PosNum` values only; `VTask.succ'` accepts the broader `Num` type (including zero).
- `Num.succ` (if it existed returning `Num`): would return a `Num`, not a `PosNum`, so callers needing a guaranteed-positive result should prefer `VTask.succ'`.
- `Nat.succ`: the successor on natural numbers; `VTask.succ'` operates on the binary numeral types `Num`/`PosNum`, not on `Nat`.