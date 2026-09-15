## VTask.conjStarAlgAut

### Object

A group homomorphism that assigns to each unitary element `u` of a star-ring `R` the ⋆-algebra automorphism of `R` given by conjugation: `x ↦ u * x * star(u)`. Because `u` is unitary (satisfying `u * star(u) = 1 = star(u) * u`), this map is indeed invertible and preserves the ring, star, and scalar-multiplication structure, making it a genuine ⋆-algebra automorphism. The assignment itself respects multiplication in the unitary group, forming a group homomorphism into the group of ⋆-algebra automorphisms of `R` over the scalar ring `S`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.conjStarAlgAut : (S : Type u_1) -> (R : Type u_2) -> [Semiring R] -> [StarMul R] -> [SMul S R] -> [IsScalarTower S R R] -> [SMulCommClass S R R] -> ↥(unitary R) →* R ≃⋆ₐ[S] R
<!-- PINNED-SIGNATURE:END -->


`VTask.conjStarAlgAut : (S : Type u_1) -> (R : Type u_2) -> [Semiring R] -> [StarMul R] -> [SMul S R] -> [IsScalarTower S R R] -> [SMulCommClass S R R] -> ↥(unitary R) →* R ≃⋆ₐ[S] R`

The first explicit argument `S` is the scalar (coefficient) type over which the ⋆-algebra automorphisms are `S`-linear. The second explicit argument `R` is the star-ring being acted upon. The instance arguments equip `R` with semiring structure, a star operation compatible with multiplication, a scalar action of `S` on `R`, and the compatibility conditions (scalar-tower and scalar-commutativity) needed so that the conjugation map is `S`-linear. The remaining argument (implicit, from the `→*` type) is a unitary element `u : unitary R` whose associated automorphism is `x ↦ u * x * star(u)`.

### Conventions

There are no declared junk-value or edge-case conventions for this definition: the map is a well-defined group homomorphism on all of `unitary R`, and every instance argument is a typeclass whose presence is required by the elaborator, so no inputs fall outside the intended domain.

### Worked examples

- Claim: For the trivial unitary element `1 : unitary R`, `VTask.conjStarAlgAut S R 1` is the identity ⋆-algebra automorphism, since `1 * x * star(1) = x` for all `x`.

- Claim: For unitary elements `u` and `v`, the automorphism assigned to the product `u * v` equals the composition of the automorphisms assigned to `u` and `v` individually, reflecting the group-homomorphism property `map_mul`.

- Claim: The automorphism `VTask.conjStarAlgAut S R u` preserves the star operation, sending `star(x)` to `u * star(x) * star(u) = star(VTask.conjStarAlgAut S R u x)`.

- Claim: The automorphism `VTask.conjStarAlgAut S R u` is `S`-linear: for any scalar `s : S` and element `x : R`, it sends `s • x` to `s • (u * x * star u)`.

### Boundaries

- At `u = 1` (the identity of `unitary R`), the resulting automorphism is the identity map on `R`.
- For central unitary elements `u` (those commuting with every element of `R`), the conjugation automorphism `x ↦ u * x * star(u)` reduces to `x ↦ u * star(u) * x = x`, again yielding the identity automorphism.
- The map always lands inside the group of ⋆-algebra automorphisms (invertible maps preserving ring operations, star, and scalar multiplication); it never produces something that is merely a ring endomorphism or fails to preserve star.
- The kernel consists precisely of those unitary elements that are central in `R` (those commuting with every element), since only then does conjugation act trivially.

### Not to be confused with

- `MulSemiringAction.toAlgAut`: the more general algebra-automorphism version arising from a `MulSemiringAction`; `VTask.conjStarAlgAut` is a star-algebra refinement specialised to conjugation by unitaries.
- `ConjAct.unitsMulDistribMulActionHom`: the multiplicative action of `ConjAct Rˣ` on `R` by conjugation, which does not package the action as a ⋆-algebra automorphism or require a star structure.
- The inner-automorphism group homomorphism for plain rings (no star): that map targets `R ≃+* R` (ring automorphisms), not `R ≃⋆ₐ[S] R` (star-algebra automorphisms), and does not require unitarity in the star sense.