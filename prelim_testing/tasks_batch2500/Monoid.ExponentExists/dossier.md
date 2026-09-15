## Object

`VTask.ExponentExists G` is the proposition asserting that the monoid `G` has a *finite exponent*: there exists a positive integer `n` such that the `n`-th power of every element of `G` is the identity. In group-theoretic language, this means the exponent of `G` (the least common multiple of all element orders) is a finite positive integer. Equivalently, every element of `G` has finite order, and there is a single positive integer that simultaneously annihilates all of them.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ExponentExists : (G : Type u) -> [Monoid G] -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.ExponentExists : (G : Type u) -> [Monoid G] -> Prop`

The first argument `G` is the carrier type of the monoid whose finite-exponent property is being asserted. The instance argument supplies the monoid structure on `G` (multiplication and identity).

## Conventions

No junk-value conventions are declared: `VTask.ExponentExists` is a `Prop`-valued predicate with no partial or default output — it simply holds or does not hold for each monoid, and there are no boundary inputs producing canonical sentinel values.

## Worked examples

- Claim: Every finite monoid (in particular, every finite group) satisfies `VTask.ExponentExists`.

- Claim: The trivial (one-element) monoid satisfies `VTask.ExponentExists`, witnessed by `n = 1`, since the only element is the identity and `1 ^ 1 = 1`.

- Claim: If `VTask.ExponentExists G` holds, then every element of `G` has a positive order (i.e., `orderOf g > 0` for all `g : G`).

- Claim: `VTask.ExponentExists G` holds if and only if the monoid exponent `Monoid.exponent G` is a nonzero (equivalently, positive) natural number.

- Claim: The additive group of integers `ℤ` does **not** satisfy `VTask.ExponentExists`, because no single positive integer `n` satisfies `n * g = 0` for all `g : ℤ`.

## Boundaries

- The trivial monoid (a single-element type) satisfies `VTask.ExponentExists`: `n = 1` works trivially.
- Infinite groups with elements of unbounded order, such as `ℤ` or any torsion-free group, do *not* satisfy `VTask.ExponentExists`.
- An infinite group *can* still satisfy `VTask.ExponentExists` if all its elements have finite order bounded by a common positive integer (e.g., `(ℤ/2ℤ)^ω`, the countably infinite direct sum of copies of `ℤ/2ℤ`, satisfies it with `n = 2`).
- The predicate requires the witnessing `n` to be *strictly positive* (`0 < n`), so `n = 0` is never a valid witness.
- If `VTask.ExponentExists G` holds, every individual element has finite order, and the monoid exponent is the least such universal bound.

## Not to be confused with

- `IsOfFinOrder g`: asserts that a single *element* `g` has finite order, which is weaker than `VTask.ExponentExists` (the latter requires all elements to share a common finite bound).
- `Monoid.exponent G`: the *value* of the exponent (a natural number), as opposed to `VTask.ExponentExists G`, which is the *proposition* that this value is positive.
- Finiteness of the group itself (`Finite G`): a monoid can have finite exponent without being finite as a set, and a finite monoid automatically has finite exponent.