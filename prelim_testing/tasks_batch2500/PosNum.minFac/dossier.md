## Object

`VTask.minFac` computes the smallest prime factor of a positive binary numeral `n`. When `n = 1` (which has no prime factors by convention), it returns `1`. For all other values of `n`, it returns the least prime that divides `n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.minFac : PosNum → PosNum
<!-- PINNED-SIGNATURE:END -->


`VTask.minFac : PosNum → PosNum`

The sole argument is a positive binary numeral whose smallest prime factor is sought.

## Conventions

The value `1` is treated specially: since `1` has no prime factorization, the function returns `1` at this input, a sentinel that is not itself prime. This is the only junk-value convention; for all `n ≥ 2` the result is genuinely the smallest prime divisor of `n`.

## Worked examples

- Claim: `VTask.minFac 1 = 1` (sentinel value for the unit)

- Claim: `VTask.minFac 2 = 2` (2 is prime, its smallest factor is itself)

- Claim: `VTask.minFac 4 = 2` (4 = 2², smallest prime factor is 2)

- Claim: `VTask.minFac 9 = 3` (9 = 3², smallest prime factor is 3)

- Claim: `VTask.minFac 15 = 3` (15 = 3 × 5, smallest prime factor is 3)

- Claim: `VTask.minFac 13 = 13` (13 is prime, smallest factor is itself)

## Boundaries

- At `n = 1`: returns `1`, not a prime. This is the only input where the output is not prime.
- For any even `n ≥ 2` (i.e., `n` of the form `bit0 _`): returns `2` immediately, without further computation.
- For odd `n ≥ 3` (i.e., `n` of the form `bit1 _`): an iterative search is performed starting from the candidate divisor `3`, and the smallest prime divisor is returned.
- For a prime `p`: returns `p` itself.
- The function is total on all `PosNum` inputs; there are no undefined cases.

## Not to be confused with

- `Nat.minFac`: the analogous function on `ℕ`. `VTask.minFac` agrees with it (modulo the `PosNum`↔`ℕ` coercion), but operates directly on binary numerals.
- `Num.minFac`: the version lifted to `Num` (which includes zero); `VTask.minFac` only handles strictly positive numerals.
- A primality test: `VTask.minFac n = n` characterises primes (for `n ≠ 1`), but the function itself returns a factor, not a boolean.