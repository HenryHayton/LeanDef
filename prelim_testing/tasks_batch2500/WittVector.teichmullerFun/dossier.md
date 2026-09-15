## Object

`VTask.teichmullerFun p r` is the **Teichmüller representative** of a ring element `r`, viewed as a Witt vector over the ring `R` at prime `p`. Concretely, it is the Witt vector whose 0-th coefficient is `r` and whose every other coefficient is `0`. It is the underlying sequence-valued function that makes the Teichmüller map into a monoid homomorphism from `R` (as a multiplicative monoid) into the Witt vectors `WittVector p R`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.teichmullerFun : (p : ℕ) -> {R : Type u_1} -> [CommRing R] -> (r : R) -> WittVector p R
<!-- PINNED-SIGNATURE:END -->


`VTask.teichmullerFun : (p : ℕ) -> {R : Type u_1} -> [CommRing R] -> (r : R) -> WittVector p R`

The first argument `p` is the prime (or natural number) parameterising the Witt vector construction; it determines the ring of Witt vectors. The implicit argument `R` is the coefficient ring, which must be a commutative ring. The argument `r` is the ring element being "lifted" to a Witt vector as its Teichmüller representative.

## Conventions

All coefficients at index `n ≠ 0` are defined to be `0` (the zero of `R`), not left undefined or treated as junk values; the function is total and the choice of `0` for non-zeroth positions is a genuine mathematical convention of the Teichmüller map.

## Worked examples

- Claim: The 0-th coefficient of `VTask.teichmullerFun p r` equals `r`.
  (By definition, the 0-th component of the resulting Witt vector is `r`.)

- Claim: For any `n ≠ 0`, the `n`-th coefficient of `VTask.teichmullerFun p r` is `0`.
  (By definition, any component at a nonzero index is `0` in `R`.)

- Claim: `VTask.teichmullerFun p (0 : R)` is the Witt vector all of whose coefficients are `0`, i.e., the zero Witt vector.
  (The 0-th coefficient is `0` and all others are `0`, so every coefficient is `0`.)

- Claim: `VTask.teichmullerFun p (1 : R)` has 0-th coefficient `1` and all others `0`.
  (This is the Teichmüller lift of the multiplicative identity.)

## Boundaries

- When `r = 0`: the resulting Witt vector has all coefficients equal to `0`, making it the zero Witt vector.
- When `r = 1`: all coefficients are `0` except the 0-th which is `1`; this corresponds to the multiplicative identity in the Witt vector ring (whose 0-th ghost component is `1`).
- The argument `p` need not be an actual prime number for this construction to type-check; the function is defined for any `ℕ`, though the deeper algebraic properties of Witt vectors require `p` to be prime.
- There is no restriction on `r`; the function is defined for every element of any commutative ring `R`.

## Not to be confused with

- **`WittVector.teichmuller`**: the packaged monoid homomorphism of which `VTask.teichmullerFun` is merely the underlying bare function; the hom carries additional algebraic structure proofs.
- **The zero Witt vector**: although `VTask.teichmullerFun p 0` coincides with the zero Witt vector, a generic Teichmüller representative is not zero.
- **The unit Witt vector / multiplicative unit**: `VTask.teichmullerFun p 1` is *not* the same object as the additive or multiplicative identity of `WittVector p R` in general; care is needed when comparing ring identities in the Witt vector ring versus simple coefficient-wise descriptions.