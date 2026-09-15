## Object

Given two R-algebra homomorphisms φ₁ : B →ₐ[R] C and φ₂ : A →ₐ[R] B (where the codomain of φ₂ equals the domain of φ₁), `VTask.comp φ₁ φ₂` is their composite R-algebra homomorphism A →ₐ[R] C, sending each element x : A to φ₁(φ₂(x)). It is again an R-algebra homomorphism, meaning it is a ring homomorphism that also respects the R-module (scalar) structure.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u} -> {A : Type v} -> {B : Type w} -> {C : Type u₁} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Semiring C] -> [Algebra R A] -> [Algebra R B] -> [Algebra R C] -> (φ₁ : B →ₐ[R] C) -> (φ₂ : A →ₐ[R] B) -> A →ₐ[R] C
<!-- PINNED-SIGNATURE:END -->


The type-universe parameters `u, v, w, u₁` allow the domain and codomain algebras to live in potentially different universes. The base commutative semiring `R` provides the scalar structure shared by all three algebras A, B, C; the `[CommSemiring R]` instance makes this precise. The instances `[Semiring A]`, `[Semiring B]`, `[Semiring C]` equip each algebra with its ring structure, while `[Algebra R A]`, `[Algebra R B]`, `[Algebra R C]` supply the compatible R-scalar action on each. The first explicit argument `φ₁ : B →ₐ[R] C` is the outer homomorphism (applied second); the second explicit argument `φ₂ : A →ₐ[R] B` is the inner homomorphism (applied first).

## Conventions

There are no declared junk-value conventions for this definition: the construction is total and well-defined for any valid pair of composable R-algebra homomorphisms, so no degenerate input regimes requiring special junk-value treatment arise.

## Worked examples

- Claim: For any R-algebra A and the identity map `AlgHom.id R A : A →ₐ[R] A`, composing it with itself yields a map that acts as the identity on elements.

- Claim: For R = ℤ (or any commutative semiring) and a chain of inclusions ι₁ : B →ₐ[R] C, ι₂ : A →ₐ[R] B, the composite `VTask.comp ι₁ ι₂` sends x : A to ι₁(ι₂(x)), preserving both addition and multiplication.

- Claim: Composition is associative: for φ₁ : C →ₐ[R] D, φ₂ : B →ₐ[R] C, φ₃ : A →ₐ[R] B, the composites `VTask.comp (VTask.comp φ₁ φ₂) φ₃` and `VTask.comp φ₁ (VTask.comp φ₂ φ₃)` agree as functions on elements of A.

- Claim: Composing `AlgHom.id R B` on the left with any φ : A →ₐ[R] B gives `VTask.comp (AlgHom.id R B) φ`, which equals φ as a map.

## Boundaries

- When φ₂ is the zero map (if one exists in the category, e.g., mapping everything to 0), the composite `VTask.comp φ₁ φ₂` is the zero map A →ₐ[R] C — composition does not introduce any special behavior here; the result is simply φ₁ applied pointwise to the image of φ₂.
- When A = B = C and φ₁ = φ₂, the composite is the square φ₁ ∘ φ₁, an endomorphism of A.
- When either φ₁ or φ₂ is the identity map, the composite is (extensionally) equal to the other map.
- The definition is stated for semirings and does not require the algebras to be commutative rings; it applies in the generality of `Semiring`.

## Not to be confused with

- `AlgHom.id R A`: the identity R-algebra homomorphism on a single algebra, not a composite of two distinct maps.
- `RingHom.comp`: composition of plain ring homomorphisms, which does not track or preserve the R-algebra (scalar) structure.
- `AlgEquiv.trans`: composition of R-algebra *isomorphisms* (equivalences), which additionally requires both maps to be invertible and produces an `AlgEquiv` rather than an `AlgHom`.