## VTask.domCongrAlg

### Object

Given a multiplicative isomorphism `e : G ≃* H` between two monoids, together with a proof that the action of every element `a : G` on any element `x : A` coincides with the action of its image `e a : H` on `x`, `VTask.domCongrAlg` produces an **algebra isomorphism** (an `AlgEquiv` over a commutative semiring `k`) between the skew monoid algebra `SkewMonoidAlgebra A G` and the skew monoid algebra `SkewMonoidAlgebra A H`. In other words, it transports the entire algebra structure across the re-labelling of the monoid of "exponents" induced by `e`, as long as the two actions on the coefficient ring `A` are compatible through `e`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.domCongrAlg : (k : Type u_1) -> {G : Type u_2} -> {H : Type u_3} -> (A : Type u_4) -> [Monoid G] -> [Monoid H] -> [Semiring A] -> [CommSemiring k] -> [Algebra k A] -> [MulSemiringAction G A] -> [MulSemiringAction H A] -> [SMulCommClass G k A] -> [SMulCommClass H k A] -> {e : G ≃* H} -> (he : ∀ (a : G) (x : A), a • x = e a • x) -> SkewMonoidAlgebra A G ≃ₐ[k] SkewMonoidAlgebra A H
<!-- PINNED-SIGNATURE:END -->


The first explicit argument `k` is the commutative semiring over which both skew monoid algebras are `k`-algebras, and over which the resulting equivalence is `k`-linear. The implicit argument `G` is the source monoid (the domain of `e`). The implicit argument `H` is the target monoid (the codomain of `e`). The explicit argument `A` is the coefficient semiring on which both `G` and `H` act by `MulSemiringAction`s. The remaining bracketed arguments supply the required typeclass instances: monoid structures on `G` and `H`, a semiring structure on `A`, commutativity of `k`, the `k`-algebra structure on `A`, the two `MulSemiringAction` instances for `G` and `H` on `A`, and the two `SMulCommClass` instances asserting that the respective monoid actions commute with the `k`-scalar action on `A`. The implicit argument `e : G ≃* H` is the multiplicative equivalence used to relabel the group elements. The explicit argument `he` is the proof that for all `a : G` and all `x : A`, the action of `a` on `x` equals the action of `e a` on `x`; this compatibility condition ensures the algebra multiplication is preserved, not merely the linear structure.

### Conventions

When `e` is the identity multiplicative equivalence `MulEquiv.refl G` and `he` is the trivial proof `(fun _ _ ↦ rfl)`, `VTask.domCongrAlg` reduces to `AlgEquiv.refl`, the identity algebra equivalence on `SkewMonoidAlgebra A G`.

### Worked examples

- Claim: For the identity multiplicative equivalence on a monoid `G`, `VTask.domCongrAlg k A (fun _ _ ↦ rfl)` (with `e = MulEquiv.refl G`) equals `AlgEquiv.refl`.

- Claim: The underlying algebra homomorphism of `VTask.domCongrAlg k A he` equals `SkewMonoidAlgebra.mapDomainAlgHom k A he`; that is, the algebra equivalence's forward map coincides with the canonical algebra map induced by re-labelling domain elements via `e`.

### Boundaries

- The compatibility hypothesis `he : ∀ (a : G) (x : A), a • x = e a • x` is essential: without it the underlying linear isomorphism of supports does not respect multiplication in the skew monoid algebra. The definition is only well-formed when this condition holds.
- When both `G` and `H` are the trivial one-element monoid and `A` is any `k`-algebra, both skew monoid algebras are isomorphic to `A` itself, and the resulting equivalence is the identity on `A`.
- The construction is covariant in `e`: applying it to the inverse equivalence `e.symm` together with the induced compatibility yields an equivalence in the opposite direction, which is the inverse of the original equivalence.
- The definition is total: no additional restriction on `k`, `G`, `H`, or `A` is imposed beyond the stated typeclass hypotheses.

### Not to be confused with

- `SkewMonoidAlgebra.domCongr` (without the `Alg` suffix): this is the underlying multiplicative or linear equivalence between skew monoid algebras, lacking the full algebra-equivalence (`AlgEquiv`) structure that `VTask.domCongrAlg` provides.
- `SkewMonoidAlgebra.mapDomainAlgHom`: this is merely an algebra *homomorphism* (not necessarily invertible) induced by a compatible map between index monoids; `VTask.domCongrAlg` upgrades this to an invertible algebra *equivalence* when the map is a multiplicative isomorphism.
- `MonoidAlgebra.domCongr`: the analogous construction for ordinary (non-skew) monoid algebras, where the action of the monoid on `A` is trivial and no compatibility condition between the two actions is needed.