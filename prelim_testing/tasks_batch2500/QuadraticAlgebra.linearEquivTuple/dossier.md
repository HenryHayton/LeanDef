## Object

`VTask.linearEquivTuple` is the canonical linear isomorphism (a `LinearEquiv` over the semiring `R`) between the quadratic algebra `QuadraticAlgebra R a b` and the type of 2-tuples `Fin 2 → R`. Concretely, it sends an element of the quadratic algebra — which has a "real" part `re` and an "imaginary" part `im` — to the function `![re, im]` (i.e., the 2-tuple whose 0-th entry is `re` and whose 1st entry is `im`). The isomorphism respects the `R`-module structure: addition and scalar multiplication are computed component-wise.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.linearEquivTuple : {R : Type u_1} -> (a b : R) -> [Semiring R] -> QuadraticAlgebra R a b ≃ₗ[R] Fin 2 → R
<!-- PINNED-SIGNATURE:END -->


`VTask.linearEquivTuple : {R : Type u_1} -> (a b : R) -> [Semiring R] -> QuadraticAlgebra R a b ≃ₗ[R] Fin 2 → R`

The implicit type argument `R` is the coefficient semiring. The explicit arguments `a` and `b` are the two parameters that define the quadratic algebra `QuadraticAlgebra R a b` — they appear in the relation satisfied by the algebra's distinguished generator. The typeclass argument `[Semiring R]` provides the semiring structure on `R` needed to form the linear equivalence.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total construction defined for any semiring `R` and any pair of elements `a b : R`, and the linearity axioms hold definitionally without any side conditions.

## Worked examples

- Claim: Applying `VTask.linearEquivTuple a b` to an element `z : QuadraticAlgebra R a b` yields the 2-tuple `![z.re, z.im]`.

- Claim: For the pair `(3 : ℤ)` and `(5 : ℤ)`, applying the forward map to `⟨2, 7⟩ : QuadraticAlgebra ℤ 3 5` gives the function that evaluates to `2` at `0` and `7` at `1`.

- Claim: The inverse map `(VTask.linearEquivTuple a b).symm` applied to the 2-tuple `x : Fin 2 → R` returns `⟨x 0, x 1⟩ : QuadraticAlgebra R a b`.

- Claim: The composite `(VTask.linearEquivTuple a b).symm ∘ (VTask.linearEquivTuple a b)` is the identity on `QuadraticAlgebra R a b`.

## Boundaries

- When `a = 0` and `b = 0`, the quadratic algebra degenerates but the linear equivalence with `Fin 2 → R` still holds; no special behaviour is introduced.
- The isomorphism exists for any semiring `R`, including non-commutative semirings; no commutativity is required.
- Because this is a `LinearEquiv`, both the forward and backward maps are `R`-linear; neither map is merely set-theoretic.
- The type `Fin 2 → R` is identified with 2-tuples indexed by `{0, 1}`; index `0` corresponds to `re` and index `1` corresponds to `im`.

## Not to be confused with

- `QuadraticAlgebra.equivProd`: a bare `Equiv` (bijection of types) to `R × R`, without any linearity structure.
- `QuadraticAlgebra.equivTuple`: the underlying `Equiv` (or `RingEquiv`-level) version mapping to `Fin 2 → R`, without the `LinearEquiv` wrapper.
- `Matrix.linearEquivFin`: a linear equivalence involving finite-index functions but for matrix rows/columns, unrelated to quadratic algebras.