## VTask.Associated

### Object

Two elements `x` and `y` of a monoid are *associated* if there exists a unit `u` in the monoid such that `x * u = y`. Informally, `x` and `y` are associated when they differ only by a (right) unit factor — they generate the same principal ideal, and in an integral domain or unique factorization domain this is exactly the notion of "same up to units" that lets one identify irreducibles and prime elements without worrying about which associate was chosen.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Associated : {M : Type u_1} -> [Monoid M] -> (x y : M) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Associated : {M : Type u_1} -> [Monoid M] -> (x y : M) -> Prop`

The implicit type argument `M` is the carrier type of the monoid. The instance argument supplies the monoid structure (identity and associative multiplication). The first explicit argument `x` is the "left" element; the second explicit argument `y` is the "right" element — `x` is associated to `y` when `x` multiplied on the right by some unit of the monoid equals `y`.

### Conventions

The relation is not symmetric by definition (the unit multiplies on the right of `x`, not of `y`), yet it turns out to be an equivalence relation on any monoid: it is reflexive (take the identity unit), symmetric, and transitive. No special junk-value or out-of-domain convention is declared for this definition.

### Worked examples

- Claim: In the integers (viewed as a monoid under multiplication), `3` and `-3` are associated, because `-1` is a unit and `3 * (-1) = -3`.

- Claim: In the integers, `2` and `3` are **not** associated, since neither `1` nor `-1` sends `2` to `3`.

- Claim: Every element of a monoid is associated to itself, witnessed by the identity unit `1`.

- Claim: In the monoid of nonzero rationals under multiplication, every two nonzero rationals are associated to each other, because their ratio is itself a unit.

### Boundaries

- **Identity element**: The identity `1` is associated to any unit `u` (take `u` itself as the witness), and any unit is associated to `1`. The identity is *not* associated to a non-unit element, because `1 * v = v` being a non-unit contradicts `v` being in the range of multiplication by a unit from the unit `1`.
- **Units**: Two elements are associated if and only if each divides the other in the divisibility preorder. In particular, all units are mutually associated.
- **Zero in a monoid-with-zero**: Zero is associated only to itself, because `0 * u = 0` for any element `u`, and a unit can never be zero (units are invertible, while `0` is typically not).
- **Non-commutative monoids**: Association is defined via right multiplication by a unit. In a non-commutative setting, `VTask.Associated x y` does not automatically imply `VTask.Associated y x` without additional reasoning, though the relation is still an equivalence when the monoid is commutative or when units are central.

### Not to be confused with

- **`Dvd` (divisibility)**: `x ∣ y` means `∃ k, y = x * k` where `k` need not be a unit; association is the symmetric, unit-only version of divisibility.
- **`IsUnit`**: Asserts that a *single* element is a unit; `VTask.Associated` is a *binary* relation between two elements.
- **Left-associated variant**: One could define association via a left unit (`u * x = y`); this definition uses a right unit, which is the Mathlib convention.