## VTask.num

### Object

`VTask.num q` is the numerator of the nonnegative rational number `q`, expressed as a natural number. Every nonnegative rational has a unique representation as a fraction `p/q` in lowest terms with `p : ℕ` and `q : ℕ` positive and coprime; `VTask.num` returns the `p` in that reduced representation.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.num : (q : ℚ≥0) -> ℕ
<!-- PINNED-SIGNATURE:END -->


```
VTask.num : (q : ℚ≥0) -> ℕ
```

The single argument `q` is the nonnegative rational whose numerator is to be extracted. The result is a natural number (not an integer) because the numerator of a nonnegative rational in lowest terms is always nonnegative.

### Conventions

The numerator is always taken from the fully reduced (lowest-terms) form of the rational number, so `VTask.num (6/4)` equals `3`, not `6`. There are no junk-value conventions because the function is total and always well-defined on `ℚ≥0`.

### Worked examples

- Claim: `VTask.num 0 = 0` (the numerator of zero is zero)

- Claim: `VTask.num 1 = 1` (the numerator of one is one)

- Claim: `VTask.num (3 / 4 : ℚ≥0) = 3` (a fraction already in lowest terms has that numerator)

- Claim: `VTask.num (6 / 4 : ℚ≥0) = 3` (automatic reduction to lowest terms)

- Claim: `(VTask.num q).Coprime q.den` holds for every `q : ℚ≥0` (the numerator and denominator are always coprime)

### Boundaries

- For `q = 0`, the numerator is `0`.
- For any positive integer `n`, the numerator of `(n : ℚ≥0)` is `n` itself (denominator is `1`).
- Fractions that are not in lowest terms are automatically reduced before extracting the numerator, so the result reflects the reduced form.
- The function is total; there are no inputs for which it is undefined.

### Not to be confused with

- `VTask.den` — the denominator of the nonnegative rational, the complementary projection.
- `Rat.num` — the numerator of a (possibly negative) rational `q : ℚ`, which is an `Int` rather than a `Nat`.
- `Int.natAbs` — the absolute value of an integer as a natural number; `VTask.num` uses this internally on the underlying `ℚ` numerator, but is not the same concept.