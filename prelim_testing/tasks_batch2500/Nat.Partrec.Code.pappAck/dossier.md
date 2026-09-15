## Object

For each natural number `n`, `VTask.pappAck n` is a `Nat.Partrec.Code` — a first-class code (program description) in Mathlib's partial-recursive-function framework — that computes the one-argument function `m ↦ ack n m`, i.e., the Ackermann function with its first argument fixed to `n`. The family `VTask.pappAck` is thus the "partial application" of the two-argument Ackermann function to its first argument, expressed entirely within the universe of partial-recursive codes.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pappAck : ℕ → Nat.Partrec.Code
<!-- PINNED-SIGNATURE:END -->


`VTask.pappAck : ℕ → Nat.Partrec.Code`

The single argument is the fixed first argument `n` of the Ackermann function — the "level" or "row" of the Ackermann table whose associated code is being returned.

## Conventions

No special junk-value or edge conventions are declared beyond the recursive definition itself: the base case `n = 0` returns a distinguished code (the successor code), and every positive `n + 1` builds the code for level `n + 1` from the code for level `n` by a wrapping step. The function is total on all natural numbers with no undefined or fallback outputs.

## Worked examples

- Claim: `VTask.pappAck 0` equals `Nat.Partrec.Code.succ`, the code for the successor function, because `ack 0 m = m + 1`.

- Claim: `VTask.pappAck 1` is the result of applying the `step` combinator to `Nat.Partrec.Code.succ`, encoding the function `m ↦ ack 1 m = m + 2` (iterated successor).

- Claim: `VTask.pappAck 2` is obtained by applying `step` twice (to the code for level 0), encoding `m ↦ ack 2 m = 2m + 3`.

- Claim: For every `n : ℕ`, the code `VTask.pappAck n` evaluates (under the standard denotation of `Nat.Partrec.Code`) to the total function `m ↦ ack n m`.

## Boundaries

- At `n = 0` the output is exactly the code for the successor function; no wrapping via `step` occurs.
- At `n = 1` exactly one application of `step` has been made.
- The function is defined for all `n : ℕ`; there is no maximum input and no case that falls through to an error or default value.
- For large `n` the returned code grows (in structural depth) linearly with `n`, even though the function it represents has an astronomically fast-growing runtime.

## Not to be confused with

- `Nat.Partrec.Code.eval` — the denotation map that *runs* a code on an input; `VTask.pappAck` only *constructs* a code, it does not evaluate it.
- The two-argument Ackermann function itself (`Nat.ack`) — `VTask.pappAck n` is a code object representing the one-argument slice at level `n`, not the numeric value of the Ackermann function.
- `step` (the combinator used internally) — `step c` is the code-level operation that lifts a code for level `n` to one for level `n+1`; it is a building block of `VTask.pappAck`, not the family itself.