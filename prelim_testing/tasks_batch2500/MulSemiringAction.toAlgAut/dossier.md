## Object

`VTask.toAlgAut G R A` is the group homomorphism that sends each element `g` of a group `G` to the algebra automorphism of `A` over `R` given by the action of `g`. In other words, it packages the multiplicative action of `G` on the `R`-algebra `A` into a single monoid homomorphism `G →* (A ≃ₐ[R] A)`, landing in the group of `R`-algebra automorphisms of `A`. This captures, in one bundled map, both the ring-automorphism and the `R`-linearity of every group element's action.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toAlgAut : (G : Type u_2) -> (R : Type u_3) -> (A : Type u_4) -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Group G] -> [MulSemiringAction G A] -> [SMulCommClass G R A] -> G →* A ≃ₐ[R] A
<!-- PINNED-SIGNATURE:END -->


`VTask.toAlgAut : (G : Type u_2) -> (R : Type u_3) -> (A : Type u_4) -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Group G] -> [MulSemiringAction G A] -> [SMulCommClass G R A] -> G →* A ≃ₐ[R] A`

`G` is the group acting on the algebra; `R` is the commutative semiring of scalars; `A` is the `R`-algebra being acted upon. The instance arguments supply the algebraic structures: `R` must be a commutative semiring, `A` a semiring with an `R`-algebra structure, `G` a group, the action of `G` on `A` must be a multiplicative semiring action, and the action must commute with the scalar action of `R` on `A` (the `SMulCommClass` condition).

## Conventions

No junk-value or edge-case conventions are relevant here: the definition is a total construction and every input satisfying the stated type-class constraints yields a well-defined group homomorphism with no special boundary behaviour.

## Worked examples

- Claim: For any group `G` with a `MulSemiringAction` on an `R`-algebra `A` satisfying `SMulCommClass G R A`, the map `VTask.toAlgAut G R A` sends the identity element `1 : G` to the identity algebra automorphism `AlgEquiv.refl R A`.

- Claim: For any group `G` with the above structure and elements `g h : G`, one has `VTask.toAlgAut G R A (g * h) = VTask.toAlgAut G R A g * VTask.toAlgAut G R A h`, expressing that `VTask.toAlgAut G R A` is a group homomorphism.

- Claim: For each `g : G`, the underlying function of the algebra equivalence `VTask.toAlgAut G R A g` is the scalar-multiplication map `(g • · : A → A)`.

## Boundaries

- When `G` is the trivial group, `VTask.toAlgAut G R A` is the unique homomorphism from the trivial group into `A ≃ₐ[R] A`, sending the single element to `AlgEquiv.refl R A`.
- The result is always a genuine group homomorphism (not merely a monoid homomorphism to a monoid of endomorphisms): the image of every group element is an invertible algebra automorphism, with inverse given by the action of `g⁻¹`.
- The `SMulCommClass G R A` hypothesis is essential: without it, the action of each `g` would not be `R`-linear and hence could not land in `A ≃ₐ[R] A`.

## Not to be confused with

- `MulSemiringAction.toRingAut`: a weaker variant producing a homomorphism `G →* A ≃+* A` into ring automorphisms, without the `R`-algebra structure.
- `DistribMulAction.toModuleEnd`: produces a homomorphism into the monoid of `R`-linear endomorphisms `A →ₗ[R] A`, not into invertible automorphisms.
- `AlgEquiv.refl R A`: the single identity element of `A ≃ₐ[R] A`, which is the value of `VTask.toAlgAut G R A` only at `1 : G`.