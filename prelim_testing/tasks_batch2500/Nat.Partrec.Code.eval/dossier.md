## Object

`VTask.eval` assigns to each `Nat.Partrec.Code` (a syntactic description of a partial recursive function) the partial function `ℕ →. ℕ` that it denotes under the standard Kleene-style interpretation. It is the *semantic valuation map* for Gödel-style codes of partial recursive functions: applying `VTask.eval c` to a natural number `n` runs the program encoded by `c` on input `n`, returning its output if the computation terminates, and diverging otherwise.

The eight constructors of `Nat.Partrec.Code` cover the standard building blocks of partial recursive functions:
- `zero` — the constant-zero function;
- `succ` — the successor function;
- `left`/`right` — the projections of Cantor's pairing decoding;
- `pair` — pointwise pairing of two programs;
- `comp` — sequential composition;
- `prec` — primitive recursion;
- `rfind'` — unbounded minimization (μ-operator) starting from a given offset.

The fundamental theorem (`exists_code`) states that a partial function `f : ℕ →. ℕ` is partial recursive if and only if there exists a code `c` such that `VTask.eval c = f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.eval : Nat.Partrec.Code → ℕ →. ℕ
<!-- PINNED-SIGNATURE:END -->


VTask.eval : Nat.Partrec.Code → ℕ →. ℕ

The first argument is a code — a finite syntactic term of type `Nat.Partrec.Code` that describes which partial recursive function is being defined. The second argument is the natural-number input to that function (passed in curried form, so `VTask.eval c` is the partial function itself, and `VTask.eval c n` is its value at `n`). Because pairing is used to encode multiple arguments, inputs to multi-argument sub-computations are presented as Cantor-pair–encoded natural numbers.

## Conventions

There are no special junk-value conventions: the function is total in both arguments in the sense that `VTask.eval c n` is always a well-defined element of `Part ℕ` (possibly `Part.none` if the computation diverges). Divergence is represented by `Part.none`; convergence to value `v` is represented by `Part.some v`. There is no undefined behaviour on any constructor or any natural-number input.

## Worked examples

- Claim: `VTask.eval Nat.Partrec.Code.zero 42 = Part.some 0` — the `zero` code ignores its input and always returns 0.

- Claim: `VTask.eval Nat.Partrec.Code.succ 7 = Part.some 8` — the `succ` code applies the successor function.

- Claim: `VTask.eval (Nat.Partrec.Code.prec Nat.Partrec.Code.zero Nat.Partrec.Code.succ) (Nat.pair 0 0) = Part.some 0` — primitive recursion with base case `zero` at `n = 0` returns `eval zero 0 = 0`.

- Claim: For any code `c` and natural numbers `a`, `k`, `eval (Nat.Partrec.Code.prec cf cg) (Nat.pair a (k + 1))` equals the monadic bind of `eval (Nat.Partrec.Code.prec cf cg) (Nat.pair a k)` into `eval cg ∘ Nat.pair a ∘ Nat.pair k` — this is `eval_prec_succ`.

- Claim: `VTask.eval (Nat.Partrec.Code.comp Nat.Partrec.Code.succ Nat.Partrec.Code.zero) 99 = Part.some 1` — composing `succ` after `zero` gives the constant-1 function.

- Claim: A partial function `f : ℕ →. ℕ` is `Nat.Partrec f` if and only if there exists a code `c` with `VTask.eval c = f`.

## Boundaries

- **Divergence**: `rfind'` and `prec` can both produce `Part.none` (diverge) for inputs where the minimization search finds no witness or where a recursive sub-call diverges. All other constructors (`zero`, `succ`, `left`, `right`) always converge.
- **Input 0 to `left`/`right`**: `Nat.unpair 0 = (0, 0)`, so `VTask.eval Nat.Partrec.Code.left 0 = Part.some 0` and similarly for `right`.
- **`prec` at `n = 0`**: `VTask.eval (Nat.Partrec.Code.prec cf cg) (Nat.pair a 0) = VTask.eval cf a`.
- **`rfind'` at offset `m`**: When the argument is `Nat.pair a m`, the search starts at `n = m` (not at 0), and the returned value is the absolute index `n ≥ m`, not the offset from `m`.
- **`pair` constructor**: If either sub-code diverges on the input, the whole `pair` computation diverges; convergence requires both halves to converge.
- **`comp` constructor**: `comp cf cg` first runs `cg` on the input; if that diverges the whole computation diverges; if it converges to `v`, then `cf` is run on `v`.

## Not to be confused with

- `Nat.Partrec.Code.evaln` — a step-indexed (bounded) approximation to `VTask.eval` that runs for at most `k` steps and returns an `Option ℕ`; it under-approximates `VTask.eval` but is computable in a stronger sense.
- `Nat.Partrec` (the predicate on functions) — this asserts that a given partial function `ℕ →. ℕ` is partial recursive, without providing a concrete code; `VTask.eval` provides the *witness* direction.
- `Nat.Partrec.Code.curry` — a code combinator that partially applies one argument of a code, distinct from `VTask.eval` itself.