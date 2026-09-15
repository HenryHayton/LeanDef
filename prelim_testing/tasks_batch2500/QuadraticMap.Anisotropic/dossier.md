## Object

A quadratic map `Q : M → N` (over a commutative semiring `R`) is called **anisotropic** if the only element of `M` sent to zero by `Q` is the zero vector. In other words, `Q` has no non-trivial isotropic vectors: whenever `Q(x) = 0` it follows that `x = 0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Anisotropic : {R : Type u_3} -> {M : Type u_4} -> {N : Type u_5} -> [CommSemiring R] -> [AddCommMonoid M] -> [AddCommMonoid N] -> [Module R M] -> [Module R N] -> (Q : QuadraticMap R M N) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Anisotropic : {R : Type u_3} -> {M : Type u_4} -> {N : Type u_5} -> [CommSemiring R] -> [AddCommMonoid M] -> [AddCommMonoid N] -> [Module R M] -> [Module R N] -> (Q : QuadraticMap R M N) -> Prop`

The implicit type arguments `R`, `M`, and `N` are the scalar semiring, the domain module, and the codomain additive commutative monoid, respectively. The instance arguments supply the algebraic structure on those types. The explicit argument `Q` is the quadratic map whose anisotropicity is being asserted.

## Conventions

No special junk-value or boundary conventions are declared for this predicate: it is a universally quantified `Prop` and is meaningful for every well-typed quadratic map.

## Worked examples

- Claim: The quadratic map `Q(x) = x²` on `ℝ` (as a map `ℝ → ℝ`) is anisotropic, because `x² = 0` implies `x = 0` in `ℝ`.

- Claim: Any positive-definite quadratic map is anisotropic — `QuadraticMap.PosDef.anisotropic` states that if `Q.PosDef` holds then `Q.Anisotropic` holds.

- Claim: The zero quadratic map on a non-trivial module is **not** anisotropic, since any nonzero vector maps to zero.

- Claim: If `Q₁.prod Q₂` (the product of two quadratic maps) is anisotropic, then both `Q₁` and `Q₂` are individually anisotropic.

## Boundaries

- On the zero module (where `M` has only one element, the zero vector), every quadratic map is trivially anisotropic, since `Q x = 0` forces `x = 0` vacuously.
- The anisotropicity condition is one-sided: it only requires that the kernel of `Q` is trivial; it says nothing about surjectivity or about values on non-zero vectors.
- Anisotropicity does not imply non-degeneracy of the associated bilinear form in general, but over rings where `2` is invertible, an anisotropic quadratic form does yield a left-separating associated bilinear form.
- For a product `Q₁.prod Q₂`, anisotropicity of the product implies anisotropicity of each factor, but the converse need not hold if the codomain addition can cancel contributions.

## Not to be confused with

- **`QuadraticMap.PosDef`**: positive-definiteness is a strictly stronger condition (requires `Q x > 0` for all `x ≠ 0`, not just `Q x ≠ 0`); every positive-definite map is anisotropic, but not conversely.
- **`LinearMap.BilinForm.SeparatingLeft`**: a separating (non-degenerate) bilinear form is a related but distinct notion; anisotropicity of a quadratic form implies left-separation of its associated bilinear form only when `2` is invertible.
- **`QuadraticMap.Nondegenerate`** (if present): non-degeneracy of a quadratic form may refer to its associated bilinear form being non-degenerate, which is a different (and generally stronger or incomparable) condition from anisotropicity of the quadratic map itself.