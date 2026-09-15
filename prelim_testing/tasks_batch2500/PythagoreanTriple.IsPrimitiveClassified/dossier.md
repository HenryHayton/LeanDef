## Object

A Pythagorean triple `(x, y, z)` — that is, a triple of integers satisfying `x² + y² = z²` — is called **primitively classified** if its two legs `x` and `y` can be expressed using the classical parametric formula: there exist coprime integers `m` and `n`, one even and one odd, such that one leg equals `m² − n²` and the other equals `2mn`. This is the standard number-theoretic parametrisation that generates all primitive Pythagorean triples (up to the labelling of which leg is "odd" and which is "even").

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsPrimitiveClassified : {x y z : ℤ} -> PythagoreanTriple x y z → Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsPrimitiveClassified : {x y z : ℤ} -> PythagoreanTriple x y z → Prop`

The implicit arguments `x`, `y`, `z` are the three integers forming the Pythagorean triple. The explicit argument is the proof (or witness) that `x² + y² = z²`, i.e. the membership certificate in the type `PythagoreanTriple x y z`. The predicate is a property of that certified triple.

## Conventions

The parametrising integers `m` and `n` are required to be coprime (integer gcd equal to 1) **and** of opposite parity (one even, one odd). This mixed-parity condition is part of the definition of primitively classified, not merely a consequence derived from coprimality alone. The predicate is symmetric between the two labelling choices (which leg is `m² − n²` and which is `2mn`): both orderings are admitted by an explicit disjunction, so the definition is invariant under swapping `x` and `y`.

## Worked Examples

- Claim: The classic triple `(3, 4, 5)` is primitively classified: take `m = 2, n = 1`; then `m² − n² = 3`, `2mn = 4`, `gcd(2,1) = 1`, and `2` is even while `1` is odd.

- Claim: The triple `(4, 3, 5)` is also primitively classified (same witnesses with roles of legs swapped): take `m = 2, n = 1`; then `2mn = 4` and `m² − n² = 3`.

- Claim: The triple `(5, 12, 13)` is primitively classified: take `m = 3, n = 2`; then `m² − n² = 5`, `2mn = 12`, `gcd(3,2) = 1`, and `3` is odd while `2` is even.

- Claim: Any primitive Pythagorean triple (one with `gcd(x, y) = 1`) is primitively classified — this is the content of `isPrimitiveClassified_of_coprime`.

## Boundaries

- The predicate can in principle be stated for any `PythagoreanTriple x y z`, even non-primitive ones (where `gcd(x, y) > 1`), but the interesting content and the associated theorems concern the primitive case.
- The degenerate triple `(0, 0, 0)` satisfies `PythagoreanTriple 0 0 0`; for it, taking `m = n = 0` would give the expressions but `gcd(0, 0) = 0 ≠ 1`, so those witnesses do not certify primitive classification. Other witnesses (e.g. `m = 1, n = 0`) satisfy the parity and gcd conditions but give `x = 1 ≠ 0`; hence this triple is not primitively classified.
- A non-primitive triple such as `(6, 8, 10)` (a scalar multiple of `(3, 4, 5)`) is generally not primitively classified since the required parametric witnesses would violate the coprimality or parity conditions.
- The mixed-parity requirement on `m` and `n` (one even, one odd) excludes the case where both are odd or both are even, which would force `2mn` to be divisible by 4 or `m² − n²` to be even — inconsistent with primitivity.

## Not to be confused with

- `PythagoreanTriple.IsClassified`: a weaker predicate that allows arbitrary integer scaling of the parametric form (i.e. `x = k(m²−n²)`, `y = 2kmn` for some integer `k`), covering all Pythagorean triples, not just primitive ones.
- `PythagoreanTriple`: the underlying type/predicate asserting `x² + y² = z²` with no coprimality or parametric structure imposed.
- A "primitive" Pythagorean triple in the informal sense (coprime legs) — being primitive is a *necessary* condition for primitive classification, but `IsPrimitiveClassified` additionally requires the explicit parametric witnesses with the coprimality and parity constraints on `m` and `n`.