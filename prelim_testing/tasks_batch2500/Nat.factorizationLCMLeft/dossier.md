## Object

`VTask.factorizationLCMLeft a b` is the natural number obtained by collecting, from the prime factorization of `lcm a b`, exactly those prime-power factors that "come from `a`": for each prime `p` dividing `lcm a b`, the prime `p` contributes its full power `p^(v_p(a))` when `v_p(a) ≥ v_p(b)`, and contributes nothing (i.e., `p^0 = 1`) otherwise.  The result is a divisor of `a` that is coprime to `VTask.factorizationLCMRight a b`, and together the two factors multiply to `lcm a b` (when both inputs are nonzero).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.factorizationLCMLeft : (a b : ℕ) -> ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.factorizationLCMLeft : (a b : ℕ) -> ℕ`

The first argument `a` is the "left" natural number whose prime-power contributions (at primes where it dominates) make up the result. The second argument `b` is the "right" natural number used as a reference: a prime's contribution is included only when its exponent in `a` is at least as large as its exponent in `b`.

## Conventions

When either `a` or `b` is `0`, the `lcm` is `0` and the factorization product is empty, so `VTask.factorizationLCMLeft a b = 1` in that case.

## Worked examples

- Claim: `VTask.factorizationLCMLeft 12 18 = 4`. Here `12 = 2^2 · 3` and `18 = 2 · 3^2`; `lcm = 36 = 2^2 · 3^2`. At prime 2: `v_2(12)=2 ≥ v_2(18)=1`, so include `2^2 = 4`. At prime 3: `v_3(12)=1 < v_3(18)=2`, so include `3^0 = 1`. Product = 4.
  ```lean
  example : VTask.factorizationLCMLeft 12 18 = 4 := by native_decide
  ```

- Claim: `VTask.factorizationLCMLeft 18 12 = 9`. Here the roles are swapped; at prime 2: `v_2(18)=1 < v_2(12)=2`, contribute 1; at prime 3: `v_3(18)=2 ≥ v_3(12)=1`, contribute `3^2 = 9`. Product = 9.
  ```lean
  example : VTask.factorizationLCMLeft 18 12 = 9 := by native_decide
  ```

- Claim: `VTask.factorizationLCMLeft 4 9 = 4`. Since `gcd(4,9)=1`, every prime of the `lcm` belongs exclusively to one side; `4=2^2` contributes `2^2=4`, and `9=3^2` contributes nothing (its exponent in `a=4` is 0 < 2).
  ```lean
  example : VTask.factorizationLCMLeft 4 9 = 4 := by native_decide
  ```

- Claim: `VTask.factorizationLCMLeft 0 5 = 1`. Since `a = 0`, the lcm is 0 and the product over primes of `lcm 0 5` is empty, giving 1.
  ```lean
  example : VTask.factorizationLCMLeft 0 5 = 1 := by native_decide
  ```

## Boundaries

- **Either argument is 0**: `lcm a 0 = lcm 0 b = 0`, and the factorization of `0` has an empty support in Mathlib's convention, so the product is 1.
- **`a = b`**: Every prime satisfies `v_p(a) = v_p(b)`, so the condition `v_p(b) ≤ v_p(a)` holds everywhere, and `VTask.factorizationLCMLeft a a = a`.
- **`a = 1`**: All prime exponents of `a` are 0; since `v_p(b) ≤ 0` only when `b` is not divisible by `p`, the result is 1 whenever `b > 1`. If `b = 1` as well, the result is also 1.
- **Coprime inputs**: When `gcd(a,b)=1` and both are positive, the two factorization halves are disjoint and `VTask.factorizationLCMLeft a b` equals the product of the prime powers of `a` whose prime appears in `a` but not `b` — which is exactly `a` itself.
- The result is always a **positive** natural number (≥ 1), even in degenerate cases.

## Not to be confused with

- `Nat.factorizationLCMRight a b`: the complementary factor collecting the primes where `b` dominates (i.e., `v_p(b) > v_p(a)`); together the two multiply to `lcm a b`.
- `Nat.gcd a b`: the greatest common divisor, which uses `min` of exponents rather than a conditional max-side selection.
- `Nat.lcm a b` itself: the full least common multiple, of which `VTask.factorizationLCMLeft` is only one (coprime) factor.
