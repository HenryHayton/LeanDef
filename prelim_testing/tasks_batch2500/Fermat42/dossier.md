## VTask.Fermat42

### Object

`VTask.Fermat42 a b c` is the proposition that the triple of integers `(a, b, c)` constitutes a *Fermat-42 triple*: a non-trivial solution to the equation `a⁴ + b⁴ = c²` over the integers, where both `a` and `b` are required to be nonzero. (No explicit nonzero condition is imposed on `c`, but it follows automatically from the equation whenever `a` and `b` are nonzero.) The central theorem of the surrounding development is that no such triple exists, from which Fermat's Last Theorem for exponent 4 (i.e., no nonzero integer solution to `x⁴ + y⁴ = z⁴`) follows as an immediate corollary.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Fermat42 : (a b c : ℤ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`(a b c : ℤ) -> Prop`

The first argument `a` and the second argument `b` are the two bases whose fourth powers are summed; both are required to be nonzero. The third argument `c` is the integer whose square equals the sum `a⁴ + b⁴`.

### Conventions

No junk-value or edge conventions are declared for this definition: it is a straightforward conjunction of an explicit nonzero condition on each of `a` and `b` together with the polynomial equation `a⁴ + b⁴ = c²`, and every input is an arbitrary integer with no implicit coercion or default behavior at boundary values.

### Worked examples

- Claim: `VTask.Fermat42 0 1 1` is false (because `a = 0` violates the nonzero condition on `a`).

- Claim: `VTask.Fermat42 1 0 1` is false (because `b = 0` violates the nonzero condition on `b`).

- Claim: If `VTask.Fermat42 a b c` holds then `VTask.Fermat42 b a c` also holds (the roles of `a` and `b` are symmetric).

- Claim: If `VTask.Fermat42 a b c` holds then `c ≠ 0` (nonzeroness of `c` is a consequence, not an assumption).

- Claim: `VTask.Fermat42 a b c` holds for no integers `a`, `b`, `c` whatsoever — the proposition is universally false.

### Boundaries

- When `a = 0` or `b = 0`, the proposition is immediately false regardless of the values of the other arguments, because the definition requires both `a ≠ 0` and `b ≠ 0`.
- The condition on `c` is purely equational: there is no explicit `c ≠ 0` hypothesis, but nonzeroness of `c` follows automatically from the equation and the nonzeroness of `a` (and `b`), so it is a derived fact rather than a boundary case.
- Negative values of `a`, `b`, or `c` are entirely permitted; the equation `a⁴ + b⁴ = c²` treats signs symmetrically in `a` and `b` (since the exponent 4 is even), and flipping the sign of `c` preserves the equation (since `c` appears squared).
- The proposition is universally false: no integer triple satisfies all three conjuncts simultaneously.

### Not to be confused with

- **Fermat's Last Theorem for exponent 4** (`a⁴ + b⁴ = c⁴` has no nonzero integer solution): `VTask.Fermat42` concerns `a⁴ + b⁴ = c²`, which is a strictly stronger statement (it implies FLT-4 by taking `c = z²`), not the equation with a fourth power on the right.
- **The `Minimal` predicate** used in the same development: that predicate adds additional minimality and coprimality conditions on top of being a Fermat-42 triple, and is used as an intermediate device in the proof of non-existence.
- **Pythagorean triples** (`a² + b² = c²`): a superficially similar Diophantine equation but with squares rather than fourth powers on the left, which has infinitely many nonzero integer solutions.