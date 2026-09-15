## Object

`VTask.ofFn n v` constructs the polynomial whose coefficient at degree `i` is `v i` for `0 ≤ i < n`, and whose coefficient at degree `i ≥ n` is zero. More precisely, it packages a function `v : Fin n → R` — thought of as a length-`n` coefficient vector — into a polynomial of degree less than `n` over a semiring `R`. The construction is linear in `v`, making `VTask.ofFn n` a linear map from the space of such coefficient vectors to the polynomial ring.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofFn : {R : Type u_1} -> [Semiring R] -> [DecidableEq R] -> (n : ℕ) -> (Fin n → R) →ₗ[R] Polynomial R
<!-- PINNED-SIGNATURE:END -->


`VTask.ofFn : {R : Type u_1} -> [Semiring R] -> [DecidableEq R] -> (n : ℕ) -> (Fin n → R) →ₗ[R] Polynomial R`

The implicit type argument `R` is the coefficient ring. The `Semiring R` instance equips `R` with the ring structure needed to form polynomials. The `DecidableEq R` instance allows equality comparisons on coefficients, as needed to form the underlying finitely-supported function. The natural number `n` fixes the length of the coefficient vector, i.e., the number of coefficients (corresponding to degrees `0` through `n − 1`). The linear map takes as its single explicit argument a function `v : Fin n → R` assigning a ring element to each index in `{0, 1, …, n − 1}`, and returns the polynomial with those coefficients.

## Conventions

For any index `i` with `i < n`, the coefficient of `VTask.ofFn n v` at degree `i` equals `v ⟨i, _⟩`. For any index `i` with `i ≥ n`, the coefficient of `VTask.ofFn n v` at degree `i` is zero — no junk value is introduced; out-of-range coefficients are simply zero, consistent with polynomial semantics.

## Worked examples

- Claim: `VTask.ofFn 3 ![1, 2, 3]` is the polynomial `1 + 2·X + 3·X²` over `ℤ`, meaning its coefficient at degree `0` is `1`, at degree `1` is `2`, and at degree `2` is `3`.

- Claim: `VTask.ofFn 0 ![]` is the zero polynomial over any semiring `R`, since there are no nonzero coefficients.

- Claim: For `n = 1` and `v : Fin 1 → R` the constant function with value `r`, `VTask.ofFn 1 v` is the constant polynomial `r`, with coefficient `r` at degree `0` and `0` at all higher degrees.

- Claim: `VTask.ofFn n` is an injective linear map whenever `R` is a nontrivial semiring, since two distinct coefficient vectors yield polynomials that differ at some degree `< n`.

## Boundaries

- When `n = 0`, the domain is `Fin 0 → R`, which has exactly one element (the empty function), and the map sends it to the zero polynomial.
- When `v` is the zero function (all coefficients zero), the result is the zero polynomial regardless of `n`.
- The polynomial produced always has degree strictly less than `n` (or is the zero polynomial); coefficients at degree `≥ n` are exactly zero.
- The map is `R`-linear, so scalar multiples and sums of coefficient vectors correspond to scalar multiples and sums of the resulting polynomials.

## Not to be confused with

- `Polynomial.C` — embeds a single ring element as a constant polynomial (degree 0), not a vector of coefficients.
- `Polynomial.ofFinsupp` — constructs a polynomial from an arbitrary finitely-supported function on `ℕ`, not restricted to a finite initial segment `Fin n`.
- `MvPolynomial.ofFinsupp` — a similar construction but for multivariate polynomials over a multi-index type, unrelated to the single-variable finite-vector setting here.