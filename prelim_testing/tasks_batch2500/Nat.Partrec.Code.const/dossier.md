## Object

`VTask.const n` produces a `Nat.Partrec.Code` — a concrete program in the language of partial recursive functions — that, when evaluated on any input, halts and returns the natural number `n`. In other words, it encodes the constant function `λ _ => n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.const : ℕ → Nat.Partrec.Code
<!-- PINNED-SIGNATURE:END -->


The sole argument is the natural number `n` that the resulting code should output unconditionally, regardless of any input it is later applied to.

## Conventions

No junk-value or boundary conventions are declared: the function is total and well-defined on every natural number with no degenerate output regime.

## Worked examples

- Claim: `VTask.const 0` is the zero code (the base case produces the primitive `zero` code directly).

- Claim: `VTask.const 1` is a composition of `succ` with `VTask.const 0`, encoding the function that first computes 0 and then applies the successor, yielding 1.

- Claim: `VTask.const 3` is built by three nested compositions of `succ` over `VTask.const 0`, ultimately encoding the constant function returning 3.

- Claim: For every `n : ℕ`, the code `VTask.const n` encodes a total function whose output on any input is `n`.

## Boundaries

- At `n = 0`: the result is exactly the primitive `zero` code, with no composition layer wrapping it.
- At `n = 1`: the result wraps `VTask.const 0` inside a single `comp succ` layer.
- For large `n`: the code has depth proportional to `n`, forming a linear chain of `succ` compositions; there is no size bound, but the construction is always finite and terminates.

## Not to be confused with

- `Nat.Partrec.Code.zero`: the primitive zero *code* that always returns 0; `VTask.const 0` reduces to this, but `VTask.const n` for `n ≥ 1` is a strictly compound code.
- `Nat.Partrec.Code.id` (or analogous identity code): encodes the identity function, not a constant — it returns its *input*, whereas `VTask.const n` ignores its input entirely.
- A Lean constant literal or `Function.const`: a meta-level notion of a constant value or function in the host language, not an object-level partial-recursive code with an explicit syntactic structure.