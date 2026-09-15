## Object

`VTask.mul` is the ring multiplication map, packaged as a doubly-curried additive monoid homomorphism. Given a (non-unital, non-associative) semiring `R`, it returns an `AddMonoidHom` from `R` to `AddMonoidHom R R`; feeding it an element `a` yields the left-multiplication-by-`a` map, and feeding that the element `b` yields `a * b`. In other words, `VTask.mul` witnesses that the multiplication `(· * ·) : R → R → R` is additive (i.e., an `AddMonoidHom`) in each argument separately.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mul : {R : Type u_1} -> [NonUnitalNonAssocSemiring R] -> R →+ R →+ R
<!-- PINNED-SIGNATURE:END -->


`VTask.mul : {R : Type u_1} -> [NonUnitalNonAssocSemiring R] -> R →+ R →+ R`

The implicit type argument `R` is the carrier of the semiring. The typeclass argument supplies the (non-unital, non-associative) semiring structure, which provides both the additive-monoid structure needed to form `AddMonoidHom` and the multiplication that is being bundled. There are no explicit term arguments: `VTask.mul` is itself a fully-formed `AddMonoidHom` from `R` to `(R →+ R)`, so it is a value, not a function waiting for further data.

## Conventions

There are no junk-value or boundary conventions specific to this definition: it is a total, structure-valued definition whose domain is all of `R`, and every element produces a well-defined additive monoid homomorphism.

## Worked examples

- Claim: For any semiring `R` and elements `x y : R`, applying `VTask.mul` to `x` and then to `y` yields `x * y`.

- Claim: Applying `VTask.mul` to `0 : R` and then to any `y : R` yields `0 * y = 0`, because `VTask.mul` is an `AddMonoidHom` and must send `0` to the zero map.

- Claim: For elements `a b c : R` in a semiring, `VTask.mul (a + b) c = VTask.mul a c + VTask.mul b c`, reflecting that the outer `AddMonoidHom` structure encodes left-distributivity.

- Claim: For elements `a b c : R` in a semiring, `VTask.mul a (b + c) = VTask.mul a b + VTask.mul a c`, reflecting that the inner `AddMonoidHom` structure (for fixed `a`) encodes right-distributivity.

## Boundaries

- When `R` is the zero ring (the trivial one-element semiring), `VTask.mul` maps the unique element to the zero homomorphism, consistent with `0 * 0 = 0`.
- Because the typeclass only requires `NonUnitalNonAssocSemiring`, there is no identity element and no associativity assumed; `VTask.mul` is valid even in those degenerate settings.
- The outer `AddMonoidHom` sends `0 : R` to the zero map `R →+ R` (since `0 * y = 0` for all `y`), and sends `a + b` to the pointwise sum of the maps for `a` and `b` (since `(a + b) * y = a * y + b * y`).
- Applying `VTask.mul a` gives exactly the left-multiplication-by-`a` map (`AddMonoidHom.mulLeft a`).

## Not to be confused with

- `AddMonoidHom.mulLeft a` — this is only the *inner* hom for a fixed `a`; `VTask.mul` additionally packages the dependence on `a` as an outer `AddMonoidHom`.
- `AddMonoidHom.mulRight r` — this bundles right-multiplication by a fixed `r`; `VTask.mul` bundles left-multiplication and is additive in the left argument.
- `LinearMap.mul` / `Algebra.lmul` — these are stronger bundlings (as linear maps over a scalar ring) available when an algebra structure is present; `VTask.mul` requires only the semiring.
