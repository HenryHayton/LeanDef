## VTask.IsPrimitive

### Object

An additive character `ψ : AddChar R R'` (a group homomorphism from the additive group of a commutative ring `R` into the multiplicative monoid `R'`) is called **primitive** when none of its nonzero multiplicative shifts is the trivial (constant-one) character. Concretely, for every nonzero element `a` of `R`, the character `x ↦ ψ(a · x)` is not identically equal to `1`. This condition generalises the classical notion of a primitive Dirichlet character: a character that cannot be induced from a character of a proper quotient.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsPrimitive : {R : Type u} -> [CommRing R] -> {R' : Type v} -> [CommMonoid R'] -> (ψ : AddChar R R') -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsPrimitive : {R : Type u} -> [CommRing R] -> {R' : Type v} -> [CommMonoid R'] -> (ψ : AddChar R R') -> Prop
```

`R` is the source commutative ring, whose additive group the character maps from. `R'` is the target commutative monoid, whose multiplicative structure the character maps into. `ψ` is the additive character being tested for primitivity.

### Conventions

No special junk-value or boundary conventions are declared for this predicate: the quantifier `∀ a ≠ 0` is vacuously true when `R` has no nonzero elements (i.e., `R` is the zero ring), so every character over the zero ring is trivially primitive.

### Worked examples

- Claim: Over a field `F`, any additive character `ψ : AddChar F R'` that is not the trivial character is primitive.

- Claim: For `ψ : AddChar (ZMod n) ℂ` primitive, the character value `ψ a = 1` if and only if `a = 0` in `ZMod n` (for `n ≠ 0`).

- Claim: The `mulShift` function is injective on a primitive character: if `ψ` is primitive then `ψ.mulShift` is injective.

- Claim: For a finite commutative ring `R`, if `r : R` is not a unit, then the multiplicative shift `ψ.mulShift r` of any additive character `ψ` is not primitive.

### Boundaries

- **Zero ring**: If `R` is the zero ring (i.e., `0 = 1` in `R`), there are no nonzero elements, so the universal quantifier is vacuously satisfied and every character is primitive by convention.
- **Trivial character**: The trivial character (mapping everything to `1`) is **not** primitive over any nontrivial ring, since taking any nonzero `a` yields a mulShift that is also identically `1`.
- **Fields**: Over a field, a character is primitive if and only if it is nontrivial, because the multiplicative group acts transitively on nonzero elements and the only subgroup structure is trivial.
- **Finite rings**: If `r` is not a unit in a finite ring, the shift `ψ.mulShift r` can never be primitive, regardless of `ψ`.
- **Preservation**: Primitivity is preserved under post-composition with an injective monoid homomorphism.

### Not to be confused with

- `IsPrimitiveRoot`: A condition on an element of a monoid asserting it is a primitive `n`-th root of unity — a completely different (element-level) notion unrelated to characters.
- `AddChar.IsNontrivial` (or `ψ ≠ 1`): Merely requiring the character itself is not identically `1`; over non-field rings this is strictly weaker than primitivity.
- Primitive polynomials (`Polynomial.IsPrimitive`): A polynomial whose coefficients have gcd 1; shares the name but is an entirely different concept in ring theory.