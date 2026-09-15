## VTask.IsIntegral

### Object

A ring homomorphism `f : R →+* A` is called **integral** if every element of `A` is integral over `R` with respect to `f`. That is, for every `x : A`, there exists a monic polynomial with coefficients in `R` (transported to `A` via `f`) that `x` satisfies. This is the global, uniform condition making the entire ring `A` an integral extension of `R` via `f`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsIntegral : {R : Type u_1} -> {A : Type u_3} -> [CommRing R] -> [Ring A] -> (f : R →+* A) -> Prop
<!-- PINNED-SIGNATURE:END -->


The sole explicit argument `f` is the ring homomorphism from the commutative ring `R` to the ring `A` whose integrality is being asserted. The type-class arguments supply the ring structures on `R` (required to be commutative) and on `A` (a not-necessarily-commutative ring).

### Conventions

No special junk-value or edge-case conventions have been declared for this predicate; it is a universally quantified `Prop` and is well-defined for any ring homomorphism, including the identity and the zero map.

### Worked examples

- Claim: The identity ring homomorphism `RingHom.id R` satisfies `VTask.IsIntegral (RingHom.id R)`, because every element `x : R` satisfies the monic polynomial `T − x` with coefficients in `R`.

- Claim: If `R` is a field and `A` is an algebraic extension of `R`, then the canonical embedding `f : R →+* A` satisfies `VTask.IsIntegral f`, since every element of `A` is algebraic (hence integral) over `R`.

- Claim: The zero ring homomorphism from `ℤ` to `ℚ` does NOT satisfy `VTask.IsIntegral`, because `VTask.IsIntegral` applied to the zero map would require every rational number to be a root of a monic integer polynomial whose coefficients are all sent to `0` in `ℚ`, which fails for, e.g., `1/2`.

### Boundaries

- When `A = R` and `f` is the identity, the predicate holds: every `x : R` satisfies `T − x`.
- When `A` is the zero ring (trivial ring), the predicate holds vacuously because every element of the zero ring satisfies any polynomial.
- The predicate is stated for `Ring A` (not necessarily commutative), so it applies in non-commutative settings, though integral elements in the non-commutative case must be understood carefully.
- The condition is strictly stronger than asking for a single element to be integral; it must hold for **all** elements of `A` simultaneously.

### Not to be confused with

- `RingHom.IsIntegralElem f x`: the pointwise predicate asserting that a *specific* element `x : A` is integral over `R` via `f`; `VTask.IsIntegral f` is exactly the universally quantified version of this.
- `Algebra.IsIntegral R A`: the algebraic analogue phrased in terms of an `Algebra` instance rather than an explicit ring homomorphism; morally equivalent but syntactically different.
- `RingHom.IsFinite f`: the stronger condition that `A` is finitely generated as an `R`-module via `f`, which implies integrality but is strictly stronger.