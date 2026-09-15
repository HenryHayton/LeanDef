## Object

`VTask.toArithmeticFunction f` is the arithmetic function (in the sense of a function `ℕ → R` that is required to vanish at `0`) obtained from an arbitrary function `f : ℕ → R` by forcing its value at `0` to be the zero element of `R`, while retaining `f`'s values at every positive natural number.

In other words, it is the canonical way to "sanitize" any function on the natural numbers into a proper arithmetic function, patching only the value at `0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toArithmeticFunction : {R : Type u_1} -> [Zero R] -> (f : ℕ → R) -> ArithmeticFunction R
<!-- PINNED-SIGNATURE:END -->


`VTask.toArithmeticFunction : {R : Type u_1} -> [Zero R] -> (f : ℕ → R) -> ArithmeticFunction R`

The type parameter `R` is the codomain, which must carry a distinguished zero element (supplied by the `Zero R` instance). The argument `f` is the raw function `ℕ → R` to be promoted; its value at every positive natural number is preserved unchanged in the result.

## Conventions

The value at `0` is always `0` (the zero of `R`), regardless of what `f 0` happens to be; `f 0` is silently discarded. For every `n ≠ 0`, the result agrees with `f n` exactly.

## Worked examples

- Claim: `VTask.toArithmeticFunction (fun n => n) 0 = 0` — the value at zero is forced to `0` even though the underlying function would give `0` here anyway.
  ```lean
  example : VTask.toArithmeticFunction (fun n => n) 0 = 0 := by decide
  ```

- Claim: `VTask.toArithmeticFunction (fun n => n * n) 5 = 25` — at a positive input the result equals the original function value.
  ```lean
  example : VTask.toArithmeticFunction (fun n => n * n) 5 = 25 := by decide
  ```

- Claim: `VTask.toArithmeticFunction (fun _ => 7) 0 = 0` — even a constant function `fun _ => 7` has its value at `0` overridden to `0`.
  ```lean
  example : VTask.toArithmeticFunction (fun _ => 7) 0 = 0 := by decide
  ```

- Claim: `VTask.toArithmeticFunction (fun _ => 7) 3 = 7` — at any positive input the constant value is preserved.
  ```lean
  example : VTask.toArithmeticFunction (fun _ => 7) 3 = 7 := by decide
  ```

- Claim: If `f` is already an `ArithmeticFunction R` (which already satisfies `f 0 = 0`), then `VTask.toArithmeticFunction f = f` — the operation is idempotent on genuine arithmetic functions.

## Boundaries

- At `n = 0`: the output is always `0 : R`, completely ignoring `f 0`. This is the only point where `f`'s actual values are discarded.
- At every `n ≠ 0`: the output equals `f n` exactly; no transformation is applied.
- Two functions `f` and `f'` that agree on all positive naturals (but possibly differ at `0`) produce identical `ArithmeticFunction` values under this construction.
- The construction is total: it is defined for every `R` with a `Zero` instance and every function `f : ℕ → R`, with no further restrictions.

## Not to be confused with

- `ArithmeticFunction` itself — that is the *type* of functions `ℕ → R` vanishing at `0`; `VTask.toArithmeticFunction` is the *constructor* that produces such a value from an arbitrary function.
- The coercion `ArithmeticFunction R → (ℕ → R)` — this goes in the *opposite* direction, extracting the underlying plain function from an arithmetic function.
- Restriction or truncation maps — those typically change the domain; this construction keeps all inputs but only patches the single value at `0`.