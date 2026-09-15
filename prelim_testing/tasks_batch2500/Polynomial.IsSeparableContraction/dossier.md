## Object

`VTask.IsSeparableContraction q f g` is the proposition that `g` is a *separable contraction* of the polynomial `f` relative to the natural number `q`. Concretely, it asserts two things simultaneously: (1) `g` is a separable polynomial (i.e., `g` and its formal derivative are coprime), and (2) there exists a non-negative integer `m` such that substituting `x^(q^m)` for `x` in `g` yields exactly `f`. In other words, `f` is obtained from the separable polynomial `g` by a "Frobenius-style" expansion by a power of `q`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsSeparableContraction : {F : Type u_1} -> [CommSemiring F] -> (q : ℕ) -> (f g : Polynomial F) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsSeparableContraction : {F : Type u_1} -> [CommSemiring F] -> (q : ℕ) -> (f g : Polynomial F) -> Prop`

The implicit type `F` is the coefficient ring, which is required to be a commutative semiring. The natural number `q` is the characteristic exponent (or candidate characteristic exponent) of the ring `F` that governs the expansion — it plays the role of the base whose powers index how far `g` has been contracted from `f`. The polynomial `f` is the polynomial being studied (the one that is supposed to admit a separable contraction), and the polynomial `g` is the proposed separable contraction of `f`.

## Conventions

The parameter `q` is not required to equal the characteristic of `F` by the bare definition; callers may supply any natural number, though the mathematically meaningful case is when `q` is the exponential characteristic of `F`. When `m = 0`, the expansion by `q^0 = 1` is the identity, so any separable polynomial `g` is trivially a separable contraction of itself (with `f = g`). There are no special junk-value conventions for out-of-range inputs because the definition is a `Prop` and is well-formed for all inputs.

## Worked examples

- Claim: Over ℤ with `q = 2`, the polynomial `X` (degree 1, separable over an integral domain) is a separable contraction of `X^2` because expanding `X` by `2^1 = 2` gives `X^2`.

- Claim: Over any commutative semiring `F` with `q = 1`, taking `m = 0` gives `expand F (1^0) g = expand F 1 g = g`, so `g` is a separable contraction of itself whenever `g` is separable; in particular `IsSeparableContraction 1 g g` holds for any separable `g`.

- Claim: If `VTask.IsSeparableContraction q f g` holds, then there exists `m : ℕ` such that `g.natDegree * q ^ m = f.natDegree`.

- Claim: If `F` has exponential characteristic `q` and `VTask.IsSeparableContraction q f g` holds, then `f.natSepDegree = g.natDegree`.

## Boundaries

- When `q = 0`: `q ^ m = 0` for all `m ≥ 1`, and `q ^ 0 = 1`, so the only expansion power that behaves non-trivially is `m = 0`. The proposition can still be satisfied (with `m = 0`), but the structure of possible separable contractions becomes degenerate.
- When `f` is itself separable, it is its own separable contraction with `m = 0` (and `q` arbitrary), so `VTask.IsSeparableContraction q f f` holds whenever `f` is separable.
- The zero polynomial: `expand F (q^m) 0 = 0`, so `VTask.IsSeparableContraction q 0 0` holds if the zero polynomial is deemed separable by the relevant separability predicate (in Mathlib, the zero polynomial is generally not separable, so this would be false).
- The definition places no constraint on `m` beyond existence; the same `f` and `g` might witness the condition for multiple values of `m` if `q = 1`.

## Not to be confused with

- `Polynomial.Separable`: the property that `g` alone is separable (coprime to its derivative), which is only one half of `VTask.IsSeparableContraction`.
- `Polynomial.HasSeparableContraction`: the statement that *some* separable contraction of `f` exists (an existential wrapper around `VTask.IsSeparableContraction`), as opposed to the relation naming a specific witness `g`.
- `Polynomial.expand F n g`: the operation of substituting `x^n` into `g`, which appears inside the definition but is a polynomial-valued map, not a proposition.
