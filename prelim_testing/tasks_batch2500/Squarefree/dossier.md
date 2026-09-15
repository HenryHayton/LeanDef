## VTask.Squarefree

### Object

An element `r` of a monoid is *squarefree* if no non-unit element of the monoid has its square dividing `r`. Equivalently, whenever `x² ∣ r` holds for some element `x`, the element `x` must already be a unit (invertible). This generalises the classical notion from the integers—a positive integer is squarefree when it is not divisible by the square of any integer greater than 1—to arbitrary monoids.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Squarefree : {R : Type u_1} -> [Monoid R] -> (r : R) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{R : Type u_1} -> [Monoid R] -> (r : R) -> Prop`

The type parameter `R` is the ambient monoid (inferred implicitly). The typeclass argument supplies the monoid structure on `R`, providing the multiplication and unit needed to speak about divisibility and invertibility. The explicit argument `r` is the particular element of `R` whose squarefreeness is being asserted.

### Conventions

The predicate is vacuously true if the only elements whose squares divide `r` are units; in particular, units themselves are always squarefree (since any `x` with `x² ∣ u` for a unit `u` must itself be a unit in a monoid where units are closed under divisibility conditions). The zero element of a ring, if present, is *not* squarefree in general, because any element's square divides zero, so `x` would need to be a unit for all `x`, which typically fails.

### Worked examples

- Claim: The integer `6` is squarefree — every integer `x` with `x * x ∣ 6` must satisfy `IsUnit x` in `ℤ`.

- Claim: The integer `12` is *not* squarefree — `2 * 2 = 4` divides `12` but `2` is not a unit in `ℤ`.

- Claim: Every unit `u` in a monoid satisfies `VTask.Squarefree u`, because if `x * x ∣ u` then `x` must be a unit (a square dividing a unit forces the factor to be a unit).

- Claim: In `ℤ`, the element `0` is not squarefree, since `2 * 2 ∣ 0` but `2` is not a unit.

### Boundaries

- **Units**: Every unit of a monoid is squarefree. The square of any element dividing a unit already forces that element to be a unit in typical algebraic settings.
- **Zero**: In a ring viewed as a monoid under multiplication, `0` is generally *not* squarefree because every element's square divides `0`, and not every element is a unit.
- **Irreducibles**: In a unique factorisation domain, squarefree elements coincide with products of distinct irreducibles (up to units), matching the classical integer definition.
- **The element `1`**: The multiplicative identity is squarefree in any monoid because any `x` with `x * x ∣ 1` must be a unit.
- **Products**: The product of two coprime squarefree elements is squarefree; multiplying a squarefree element by itself yields a non-squarefree element (when it is not a unit).

### Not to be confused with

- **`Irreducible`**: An irreducible element cannot be written as a product of two non-units, a stronger and different condition from having no squared non-unit factor.
- **`IsUnit`**: Being a unit is a special case of being squarefree; `IsUnit x → VTask.Squarefree x`, but squarefree elements need not be units.
- **`UniqueFactorizationMonoid.squarefree_iff_nodup_factors`**: A theorem characterising squarefreeness via factor lists; not the definition itself.
