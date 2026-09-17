## Object

`VTask.prodMap f g` is the non-unital semiring homomorphism from the product ring `R × S` to the product ring `R' × S'` obtained by applying `f` component-wise to the first coordinate and `g` component-wise to the second coordinate. Concretely, it sends every pair `(r, s)` to `(f r, g s)`. This is the standard "product map" construction lifted to the category of non-unital semirings.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prodMap : {R : Type u_1} -> {R' : Type u_2} -> {S : Type u_3} -> {S' : Type u_4} -> [NonUnitalNonAssocSemiring R] -> [NonUnitalNonAssocSemiring S] -> [NonUnitalNonAssocSemiring R'] -> [NonUnitalNonAssocSemiring S'] -> (f : R →ₙ+* R') -> (g : S →ₙ+* S') -> R × S →ₙ+* R' × S'
<!-- PINNED-SIGNATURE:END -->


`VTask.prodMap : {R : Type u_1} -> {R' : Type u_2} -> {S : Type u_3} -> {S' : Type u_4} -> [NonUnitalNonAssocSemiring R] -> [NonUnitalNonAssocSemiring S] -> [NonUnitalNonAssocSemiring R'] -> [NonUnitalNonAssocSemiring S'] -> (f : R →ₙ+* R') -> (g : S →ₙ+* S') -> R × S →ₙ+* R' × S'`

The implicit type arguments `R`, `R'`, `S`, `S'` are the four non-unital semiring types involved: `R` and `S` are the source types forming the domain product, while `R'` and `S'` are the target types forming the codomain product. The semiring structure instances are provided automatically. The explicit argument `f` is a non-unital semiring homomorphism from `R` to `R'`, governing what happens to the first component. The explicit argument `g` is a non-unital semiring homomorphism from `S` to `S'`, governing what happens to the second component.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total construction, well-defined for any pair of non-unital semiring homomorphisms, with no degenerate inputs requiring special treatment.

## Worked examples

- Claim: For any non-unital semiring homomorphisms `f : R →ₙ+* R'` and `g : S →ₙ+* S'`, and any pair `(r, s) : R × S`, the first component of `VTask.prodMap f g (r, s)` is `f r`.

- Claim: For any non-unital semiring homomorphisms `f : R →ₙ+* R'` and `g : S →ₙ+* S'`, and any pair `(r, s) : R × S`, the second component of `VTask.prodMap f g (r, s)` is `g s`.

- Claim: For any non-unital semiring homomorphism `f : R →ₙ+* R'` and `g : S →ₙ+* S'`, `VTask.prodMap f g` preserves addition: `VTask.prodMap f g (x + y) = VTask.prodMap f g x + VTask.prodMap f g y`.

- Claim: For any non-unital semiring homomorphism `f : R →ₙ+* R'` and `g : S →ₙ+* S'`, `VTask.prodMap f g` preserves multiplication: `VTask.prodMap f g (x * y) = VTask.prodMap f g x * VTask.prodMap f g y`.

## Boundaries

- When both `f` and `g` are identity homomorphisms on their respective types, `VTask.prodMap f g` acts as the identity on the product `R × S`.
- When `f` is the zero homomorphism (mapping everything to `0` in `R'`) and `g` is arbitrary, the first component of every output is `0`.
- The construction is genuinely total: there are no restrictions on `f` or `g` beyond them being valid non-unital semiring homomorphisms.
- The resulting morphism is a `NonUnitalNonAssocSemiring` homomorphism; in particular, it does not require or assert unitality even if the underlying rings happen to be unital.

## Not to be confused with

- `NonUnitalRingHom.prod f g` (which takes two homomorphisms with the *same* domain `R` and pairs their values, rather than acting on a product domain).
- `RingHom.prodMap` (the analogous construction for *unital* ring homomorphisms, which additionally preserves the multiplicative identity).
- `NonUnitalRingHom.fst` / `NonUnitalRingHom.snd` (the projection homomorphisms out of a product, which are the building blocks used internally but go in the opposite direction).