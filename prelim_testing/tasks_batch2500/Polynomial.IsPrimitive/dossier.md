## VTask.IsPrimitive

### Object

A polynomial `p` over a commutative semiring `R` is **primitive** if every constant polynomial that divides `p` is a unit. Equivalently, no non-unit element of `R`, viewed as a constant polynomial, can factor out of `p`. This is the standard algebraic notion: a polynomial whose coefficients have no common non-unit divisor (in the sense that any common constant divisor must already be invertible in `R`).

> **Note:** This predicate has nothing to do with primitive elements of finite fields or their minimal polynomials.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsPrimitive : {R : Type u_1} -> [CommSemiring R] -> (p : Polynomial R) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsPrimitive : {R : Type u_1} -> [CommSemiring R] -> (p : Polynomial R) -> Prop`

The implicit argument `R` is the coefficient ring, which must be a commutative semiring. The instance argument supplies the commutative semiring structure on `R`. The explicit argument `p` is the polynomial being tested for primitivity.

### Conventions

The zero polynomial is not excluded from the domain by definition; however, in a nontrivial ring the zero polynomial fails to be primitive (every element divides it, so any non-unit element yields a non-unit constant divisor), and this is consistent with the definition returning `False` for `0` in nontrivial rings.

### Worked examples

- Claim: Every monic polynomial is primitive, so `X + 1 : ℤ[X]` is primitive.

- Claim: If `p : ℤ[X]` is primitive then its content equals `1`.

- Claim: If `p` and `q` are both primitive polynomials over a GCD domain `R`, then so is their product `p * q`.

- Claim: The zero polynomial `(0 : ℤ[X])` is NOT primitive, since `2` divides `0` but `2` is not a unit in `ℤ`.

### Boundaries

- **Zero polynomial:** In any nontrivial commutative semiring, the zero polynomial fails to be primitive because every constant (including non-units) divides it.
- **Constant polynomials:** A constant polynomial `C r` is primitive if and only if `r` itself is a unit in `R`, because `C r` divides `C r`, so primitivity forces `r` to be a unit.
- **Unit polynomials:** Any polynomial that is a unit in the polynomial ring is primitive; in particular any nonzero constant that is a unit yields a primitive constant polynomial.
- **Monic polynomials:** Every monic polynomial is primitive, since its leading coefficient is `1`, and the content of a monic polynomial is `1`.
- **Closure under multiplication:** The product of two primitive polynomials is again primitive (this is a form of Gauss's lemma).
- **Trivial ring:** If `R` is the zero ring (trivial ring), every polynomial is primitive vacuously, since every element is a unit.

### Not to be confused with

- **`IsPrimitiveRoot`:** A property of an element of a ring being a primitive root of unity — entirely unrelated to primitivity of polynomials.
- **`Polynomial.primPart`:** The primitive part of a polynomial, which is the result of dividing out the content; a polynomial is primitive iff it equals its own primitive part.
- **`Irreducible` (for polynomials):** A polynomial can be irreducible without being primitive (e.g., `2 * X` over `ℤ` is irreducible in some sense but not primitive), and a primitive polynomial need not be irreducible.