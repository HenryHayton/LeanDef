## Object

`VTask.verschiebungFun x` produces a new Witt vector over the commutative ring `R` (for prime `p`) by shifting all coefficients of `x` up by one index and inserting `0` at position `0`. Concretely, if `x` has coefficients `(a₀, a₁, a₂, …)`, the result has coefficients `(0, a₀, a₁, a₂, …)`. This is the set-theoretic (function-level) version of the classical Verschiebung ('shift') map on Witt vectors.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.verschiebungFun : {p : ℕ} -> {R : Type u_1} -> [CommRing R] -> (x : WittVector p R) -> WittVector p R
<!-- PINNED-SIGNATURE:END -->


The implicit argument `p` is the prime (or natural number) governing the Witt vector construction; `R` is the coefficient ring, which must be a commutative ring. The explicit argument `x` is the Witt vector whose coefficients are to be shifted.

## Conventions

The 0th coefficient of the result is always `0`, regardless of the input. There are no junk values in the usual sense, since Witt vectors are defined for all natural-number indices; the definition is total.

## Worked examples

- Claim: The 0th coefficient of `VTask.verschiebungFun x` is `0` for any Witt vector `x`.

- Claim: For any Witt vector `x` and any `i : ℕ`, the `(i + 1)`th coefficient of `VTask.verschiebungFun x` equals the `i`th coefficient of `x`.

- Claim: Applying `VTask.verschiebungFun` to the zero Witt vector yields the zero Witt vector (every coefficient is `0`, and shifting only `0`s gives `0`s).

- Claim: If `x` has `x.coeff 0 = 5` and `x.coeff 1 = 3` (over a suitable ring), then `(VTask.verschiebungFun x).coeff 1 = 5` and `(VTask.verschiebungFun x).coeff 2 = 3`.

## Boundaries

- At index `0`: the result always has coefficient `0`, regardless of the input `x`. No information from `x` appears at position `0`.
- At any positive index `n = i + 1`: the result's coefficient is exactly `x.coeff i`, so no coefficients of `x` are lost; they merely shift one step upward.
- The map is injective: two Witt vectors with different coefficient sequences will have different shifted sequences, since the shift only adds a leading `0`.
- The map is not surjective: any Witt vector whose `0`th coefficient is nonzero is not in the image of `VTask.verschiebungFun`.

## Not to be confused with

- `WittVector.verschiebung`: the additive monoid homomorphism whose underlying function is `VTask.verschiebungFun`; `VTask.verschiebungFun` is the bare function, lacking the bundled homomorphism structure.
- `WittVector.frobeniusFun`: a different fundamental operation on Witt vectors that raises coefficients via the Frobenius endomorphism rather than shifting them.
- Truncated Witt vector shifts: in some treatments a 'shift' modifies a finite-length Witt vector; `VTask.verschiebungFun` operates on infinite Witt vectors indexed by all of `ℕ`.