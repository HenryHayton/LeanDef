## Object

`VTask.evenOddRec` is a recursion principle for natural numbers structured around the binary representation of a natural number. It provides a way to define (or prove) a property or function `P : ℕ → Sort*` for every natural number by supplying: a base case at zero, and two step cases — one that extends any value `P n` to `P (2 * n)` (the even doubling step) and one that extends any value `P n` to `P (2 * n + 1)` (the odd doubling step). Every natural number can be reached from 0 by a finite sequence of such doublings and odd-doublings, mirroring the binary expansion of the number, so these three cases are sufficient to cover all of ℕ.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.evenOddRec : {P : ℕ → Sort u_1} -> (h0 : P 0) -> (h_even : (n : ℕ) → P n → P (2 * n)) -> (h_odd : (n : ℕ) → P n → P (2 * n + 1)) -> (n : ℕ) -> P n
<!-- PINNED-SIGNATURE:END -->


`{P : ℕ → Sort u_1}` is the motive: the type family indexed by natural numbers that we are recursing into. `h0 : P 0` is the base case, supplying an element of `P` at zero. `h_even : (n : ℕ) → P n → P (2 * n)` is the even step: given any natural number `n` and a value of type `P n`, it produces a value of type `P (2 * n)`. `h_odd : (n : ℕ) → P n → P (2 * n + 1)` is the odd step: given any natural number `n` and a value of type `P n`, it produces a value of type `P (2 * n + 1)`. The final argument `n : ℕ` is the natural number at which we want to evaluate the result, yielding a term of type `P n`.

## Conventions

The even step `h_even` is applied at `n = 0` as part of the binary recursion machinery when reaching 0 by even steps; however, the reduction lemma for even inputs requires a coherence condition `h_even 0 h0 = h0` to ensure the result at 0 agrees with `h0`. No junk values arise since the function is total over all natural numbers.

## Worked examples

- Claim: `VTask.evenOddRec 0 (fun n acc => 2 * acc) (fun n acc => 2 * acc + 1) 0 = 0`
  (Applying `evenOddRec` at `n = 0` returns the base case `h0`, here 0.)

- Claim: `VTask.evenOddRec 0 (fun n acc => 2 * acc) (fun n acc => 2 * acc + 1) 1 = 1`
  (Here `1 = 2 * 0 + 1`, so the odd step is applied to the base: `h_odd 0 0 = 2 * 0 + 1 = 1`.)

- Claim: `VTask.evenOddRec 0 (fun n acc => 2 * acc) (fun n acc => 2 * acc + 1) 6 = 6`
  (Here `6 = 2 * 3`, and `3 = 2 * 1 + 1`, and `1 = 2 * 0 + 1`; the recursion faithfully reconstructs the number by re-assembling its binary digits from the base case.)

- Claim: The reduction `VTask.evenOddRec h0 h_even h_odd 0 = h0` holds definitionally, expressing that evaluation at 0 returns the base case.

- Claim: For any `n`, `VTask.evenOddRec h0 h_even h_odd (2 * n + 1) = h_odd n (VTask.evenOddRec h0 h_even h_odd n)` (given the coherence condition `h_even 0 h0 = h0`), expressing that evaluation at an odd number unfolds via the odd step.

## Boundaries

- At `n = 0`: the recursion immediately returns `h0`; no step cases are invoked.
- The even step `h_even` is applied with `n = 0` during the binary recursion machinery when traversing the zero path; to obtain the clean reduction `(2 * n).evenOddRec ... = h_even n (...)`, the coherence side condition `h_even 0 h0 = h0` must hold.
- The odd step `h_odd` at `n = 0` gives `P 1`, consistent with `1 = 2 * 0 + 1`.
- There are no inputs for which the function is undefined; it is total over all natural numbers and all sort levels.

## Not to be confused with

- `Nat.rec` / `Nat.recOn`: the standard successor-based recursor on ℕ, which steps by 1 rather than by doubling.
- `Nat.binaryRec`: the underlying binary recursor that this definition wraps; it operates using boolean bit values (`bit0`/`bit1`) rather than the arithmetic expressions `2 * n` and `2 * n + 1`.
- `Nat.strongRecOn` / `Nat.strong_induction_on`: strong induction on ℕ, which gives access to all smaller values rather than just one predecessor in a binary tree.
