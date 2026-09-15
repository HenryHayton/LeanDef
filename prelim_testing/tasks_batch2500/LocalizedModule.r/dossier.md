## Object

`VTask.r` is the binary relation on pairs `(m, s) ∈ M × S` (where `S` is a submonoid of a commutative semiring `R` and `M` is an `R`-module) defined by: `(m₁, s₁) ~ (m₂, s₂)` if and only if there exists an element `u ∈ S` such that `u • (s₂ • m₁) = u • (s₁ • m₂)` inside `M`. Informally, two pairs are related when the would-be difference `s₂ • m₁ - s₁ • m₂` is annihilated by some element of `S`. This is the standard equivalence relation used to construct the localisation of a module `M` at a submonoid `S`, directly analogous to the construction of a localisation of a ring.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.r : {R : Type u} -> [CommSemiring R] -> (S : Submonoid R) -> (M : Type v) -> [AddCommMonoid M] -> [Module R M] -> (a b : M × ↥S) -> Prop
<!-- PINNED-SIGNATURE:END -->


The type string is inserted automatically above.

- `R` is the ambient commutative semiring over which everything is defined.
- The `CommSemiring R` instance supplies the ring structure on `R`.
- `S` is the submonoid of `R` whose elements serve as the denominators (the multiplicative set being inverted).
- `M` is the `R`-module whose elements serve as the numerators.
- The `AddCommMonoid M` and `Module R M` instances give `M` its additive and scalar-multiplication structure.
- `a` and `b` are the two pairs in `M × ↥S` being compared; each consists of a numerator element of `M` and a denominator element of `S`.

## Conventions

No junk-value conventions are declared: the relation is a genuine mathematical predicate on all pairs in `M × S`, and the statement of the existential is uniform with no distinguished degenerate inputs.

## Worked examples

- Claim: For any `(m, s) ∈ M × S`, `VTask.r S M (m, s) (m, s)` holds (reflexivity), witnessed by taking `u = 1 ∈ S`.

- Claim: In the `ℤ`-module `ℤ` localised at the submonoid `S = {1}`, the pairs `(2, 1)` and `(4, 2)` do NOT satisfy `VTask.r S ℤ (2, 1) (4, 2)` when `S` only contains the unit, because `2 • 1 = 2` and `1 • 4 = 4` and any `u ∈ S` is `1`, giving `1 • 1 • 2 = 2 ≠ 4 = 1 • 1 • 4`.

- Claim: In `ℤ` viewed as a `ℤ`-module, with `S` the positive integers as a submonoid, `VTask.r S ℤ (2, 1) (4, 2)` holds, witnessed by `u = 1 ∈ S`, since `1 • 2 • 2 = 4 = 1 • 1 • 4`.

- Claim: If `(m₁, s₁) ~ (m₂, s₂)` then `(m₂, s₂) ~ (m₁, s₁)` (symmetry), because the witnessing `u` for the first direction is also a witness for the second after swapping sides of the equation.

## Boundaries

- When `S = {1}` (the trivial submonoid), the relation reduces to `s₂ • m₁ = s₁ • m₂` (i.e., no extra cancellation is available), which may fail to be an equivalence relation on general semirings unless the module is torsion-free.
- When the module `M` is the zero module, every pair is related to every other pair, since the scalar equation holds trivially.
- The existential quantifier over `u` is essential: in a module with torsion, or a semiring with zero-divisors, two pairs may be equivalent even if `s₂ • m₁ ≠ s₁ • m₂`, provided some `u ∈ S` kills the difference.
- Because `R` is only required to be a `CommSemiring` (not a ring), the condition is stated multiplicatively (`u • (s₂ • m₁) = u • (s₁ • m₂)`) rather than via subtraction, so this definition is valid in the semiring setting.

## Not to be confused with

- The ring-localisation equivalence relation on `R × S`: that is the special case where the module `M` is `R` itself acting on itself by multiplication.
- `Setoid.r` or arbitrary setoid relations: `VTask.r` is a specific, mathematically motivated relation tied to the module-localisation construction, not a generic setoid.
- Module hom kernels or submodule membership predicates: `VTask.r` is a relation on `M × S`, not a predicate on `M` alone.