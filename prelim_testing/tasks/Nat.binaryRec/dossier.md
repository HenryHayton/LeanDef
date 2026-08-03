## Object

`VTask.binaryRec` is a recursion/induction principle for natural numbers structured around their binary digit representations. Every natural number can be viewed as either zero or as the result of prepending a bit (true or false) to a shorter natural number. This recursor exploits that decomposition: given a value for zero and a way to extend any result from `n` to `Nat.bit b n` (the number formed by prepending bit `b` to the binary representation of `n`), it produces a value for every natural number.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.binaryRec : {motive : ℕ → Sort u} -> (zero : motive 0) -> (bit : (b : Bool) → (n : ℕ) → motive n → motive (Nat.bit b n)) -> (n : ℕ) -> motive n
<!-- PINNED-SIGNATURE:END -->


`{motive : ℕ → Sort u} -> (zero : motive 0) -> (bit : (b : Bool) → (n : ℕ) → motive n → motive (Nat.bit b n)) -> (n : ℕ) -> motive n`

The implicit argument `motive` is the type family (predicate or data family) over natural numbers whose instances are being constructed. The argument `zero` supplies the value at `0`. The argument `bit` is a step function: given a boolean `b`, a natural number `n`, and a previously computed value at `n`, it produces a value at `Nat.bit b n` (the number whose binary representation is `b` prepended to that of `n`). The final argument `n` is the natural number at which the result is computed.

## Conventions

When `n = 0`, the recursor returns the `zero` value directly: `VTask.binaryRec zero bit 0 = zero`. When `n = 1`, the recursor returns `bit true 0 zero`, since `1 = Nat.bit true 0`. The `bit` step function is called with the least-significant bit of `n` and the right-shift of `n` by one; the recursion on the shifted value terminates because right-shifting a nonzero natural number strictly decreases it.

## Worked examples

- Claim: For the constant-unit motive, `VTask.binaryRec () (fun _ _ _ => ()) 0 = ()`

- Claim: For the identity function built by this recursor at `n = 1`, the result equals `Nat.bit true 0`; concretely, `VTask.binaryRec 0 (fun b n _ => Nat.bit b n) 1 = 1`

- Claim: The recursor applied to a motive counting binary digits returns `0` at `0` and `1 + VTask.binaryRec 0 (fun _ n acc => 1 + acc) (1 >>> 1)` at `1`.

- Claim: At `n = 2`, the step `bit` is invoked with `b = false` and `n = 1` (since `2 = Nat.bit false 1`), producing `bit false 1 (bit true 0 zero)` from the two-level unfolding.

## Boundaries

- At `n = 0`, the base case fires and `zero` is returned regardless of the `bit` function.
- At `n = 1 = Nat.bit true 0`, the step fires once with `b = true`, `n = 0`, and the accumulated value `zero`.
- The unfolding equation `VTask.binaryRec zero bit (Nat.bit b n) = bit b n (VTask.binaryRec zero bit n)` holds unconditionally when either `n ≠ 0` or `b = true`; when `n = 0` and `b = false`, `Nat.bit false 0 = 0`, so the call reduces to the base case and the equation holds only if `bit false 0 zero = zero`.
- The recursion is well-founded: at each recursive step the argument is the right-shift of the current input, which is strictly smaller than any nonzero natural number.

## Not to be confused with

- `VTask.binaryRec'`: a variant that additionally requires the leading bit to be `true` when `n = 0`, avoiding the leading-zero ambiguity.
- `VTask.binaryRecFromOne`: a variant that treats `0` and `1` as separate base cases, skipping the `Nat.bit b 0` with `b = false` degenerate case entirely.
- `Nat.rec` (the standard recursor): recurses by peeling off one successor at a time in unary, rather than processing one binary digit at a time.