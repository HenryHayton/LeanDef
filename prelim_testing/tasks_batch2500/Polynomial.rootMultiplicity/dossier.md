## VTask.rootMultiplicity

### Object

Given a ring element `a` and a polynomial `p` over a ring `R`, `VTask.rootMultiplicity a p` is the largest natural number `n` such that `(X - C a)^n` divides `p`. Equivalently, it is the multiplicity of `a` as a root of `p` — how many times the linear factor `(X − a)` can be extracted from `p`. When `p` is the zero polynomial, the value is defined to be `0` by convention.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.rootMultiplicity : {R : Type u} -> [Ring R] -> (a : R) -> (p : Polynomial R) -> ℕ
<!-- PINNED-SIGNATURE:END -->


`{R : Type u} -> [Ring R] -> (a : R) -> (p : Polynomial R) -> ℕ`

The implicit type argument `R` is the coefficient ring, which must carry a `Ring` instance. The first explicit argument `a` is the ring element being tested as a root — the centre of the linear factor `X − C a`. The second explicit argument `p` is the polynomial whose divisibility by powers of `(X − C a)` is being measured.

### Conventions

When `p` is the zero polynomial, `VTask.rootMultiplicity a 0 = 0` for every `a`; the zero polynomial is not assigned an infinite multiplicity but rather the sentinel value `0`.

### Worked examples

- Claim: For the polynomial `X - C 3` over `ℤ`, the root multiplicity of `3` is `1`.

- Claim: For a nonzero constant polynomial `C r`, the root multiplicity of any element `a` is `0`, since no linear factor divides a nonzero constant.

- Claim: For the zero polynomial, the root multiplicity of any `a` is `0` (by the junk-value convention).

- Claim: If `p = (X - C a)^k * q` where `(X - C a)` does not divide `q`, then `VTask.rootMultiplicity a p = k`.

- Claim: `VTask.rootMultiplicity 0 p` equals the trailing degree of `p` (the largest power of `X` dividing `p`).

### Boundaries

- **Zero polynomial**: `VTask.rootMultiplicity a 0 = 0` for every `a`, even though morally every power of `(X − a)` divides `0`. This is a sentinel convention, not a mathematical limit.
- **Non-root**: If `a` is not a root of `p` (i.e., `p(a) ≠ 0`), then `VTask.rootMultiplicity a p = 0`, since not even `(X − a)^1` divides `p`.
- **Simple root**: If `a` is a simple root of `p`, the multiplicity is exactly `1`.
- **Constant polynomial (nonzero)**: `VTask.rootMultiplicity a (C r) = 0` whenever `C r ≠ 0`.
- **Root of the derivative**: If `a` is a root of multiplicity `n ≥ 1` in `p`, then `a` is a root of multiplicity `n − 1` in the derivative `p'` (under suitable non-zero-divisor conditions on `n` in `R`).
- **Ring requirement**: The definition works over any ring, but divisibility behaviour (and uniqueness of factorisation) depends on additional assumptions such as being an integral domain.

### Not to be confused with

- **`Polynomial.roots`**: A multiset of roots (without multiplicity counted in a naive sense for general rings); `VTask.rootMultiplicity a p` is the count of `a` in this multiset when `R` is an integral domain.
- **`Polynomial.natDegree`**: The degree of a polynomial, which upper-bounds the sum of root multiplicities but is a different invariant entirely.
- **`multiplicity` (the general EMF multiplicity)**: A more general notion of multiplicity for arbitrary elements in a monoid; `VTask.rootMultiplicity` is the specialised, computable version restricted to powers of linear factors `(X − C a)`.