## VTask.IsQuasiregular

### Object

In a non-unital semiring `R`, an element `x : R` is called **quasiregular** if it is invertible with respect to the binary operation `(x, y) ↦ y + x + x * y`, sometimes called the **circle operation** or **quasi-multiplication**. Concretely, `x` is quasiregular if there exists an element `y` (its **quasi-inverse**) such that both

  y + x + x * y = 0   and   x + y + y * x = 0.

This is the non-unital analogue of the notion that `1 + x` is a unit: whenever a unit `1` exists, `x` is quasiregular precisely when `1 + x` is invertible.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsQuasiregular : {R : Type u_1} -> [NonUnitalSemiring R] -> (x : R) -> Prop
<!-- PINNED-SIGNATURE:END -->


VTask.IsQuasiregular : {R : Type u_1} -> [NonUnitalSemiring R] -> (x : R) -> Prop

The implicit argument `R` is the ambient non-unital semiring. The instance argument supplies the semiring structure on `R`. The explicit argument `x` is the element of `R` being tested for quasiregularity.

### Conventions

There are no junk-value conventions to declare: `VTask.IsQuasiregular` is a predicate that is either true or false for each element; it carries no default value for out-of-domain inputs, and the domain is all elements of any non-unital semiring.

### Worked examples

- Claim: In any non-unital semiring, `0` is quasiregular (with quasi-inverse `0`).

- Claim: In a unital ring `R`, an element `x : R` is quasiregular if and only if `1 + x` is a unit in `R`.

- Claim: If `f : R →ₙ+* S` is a non-unital ring homomorphism and `x : R` is quasiregular, then `f x` is quasiregular in `S`.

- Claim: In a product `A × B` of non-unital semirings, a pair `(a, b)` is quasiregular if and only if both `a` and `b` are separately quasiregular.

- Claim: In a dependent product (pi type) `∀ i, κ i`, a tuple `x` is quasiregular if and only if every component `x i` is quasiregular.

### Boundaries

- The zero element is always quasiregular in any non-unital semiring; `y = 0` serves as its own quasi-inverse since `0 + 0 + 0 * 0 = 0`.
- The predicate makes sense even when `R` has no multiplicative identity. When a unit `1` is present, quasiregularity of `x` is equivalent to `1 + x` being a unit.
- The element `x = -1` (in a ring where it exists) is **not** quasiregular, since `1 + (-1) = 0` is not a unit.
- The predicate is preserved under non-unital semiring homomorphisms: the image of a quasiregular element is quasiregular.
- The notion is well-behaved under unitisation: an element embedded into the unitisation `Unitization R A` via the canonical map is quasiregular there if and only if it is quasiregular in `A`.

### Not to be confused with

- `IsUnit x`: asserts that `x` is invertible under ordinary multiplication; quasiregularity instead asks for invertibility under the circle operation and applies in non-unital settings.
- `quasispectrum R a`: the set of scalars `r` for which `-(r⁻¹ • a)` is **not** quasiregular; quasiregularity governs membership in the complement of this spectrum.
- Classical *regularity* in semigroup/ring theory (von Neumann regularity): an element `x` is von Neumann regular if `x = x * y * x` for some `y`, a different condition that also generalises invertibility but in a different direction.