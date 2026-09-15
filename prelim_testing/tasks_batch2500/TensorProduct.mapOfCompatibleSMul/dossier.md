## VTask.mapOfCompatibleSMul

### Object

Given modules M and N that are simultaneously modules over two commutative semirings R and A, with all scalar-multiplication actions mutually commuting in the appropriate sense, and given a compatibility condition that lets the A-action on the tensor product M ⊗[R] N switch between the two tensor factors, there is a canonical ring-change map from the tensor product M ⊗[A] N to the tensor product M ⊗[R] N. This map is, moreover, linear over any third commutative semiring S that also acts on M compatibly with both the A- and R-actions. The map sends a pure tensor m ⊗ n (in M ⊗[A] N) to the corresponding pure tensor m ⊗ n (in M ⊗[R] N), respecting the fact that the A-balanced relation is implied by the R-balanced relation under the compatibility hypothesis.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapOfCompatibleSMul : (R : Type u_1) -> [CommSemiring R] -> (A : Type u_22) -> (S : Type u_23) -> (M : Type u_24) -> (N : Type u_25) -> [AddCommMonoid M] -> [AddCommMonoid N] -> [Module R M] -> [Module R N] -> [CommSemiring A] -> [Module A M] -> [Module A N] -> [SMulCommClass R A M] -> [CommSemiring S] -> [Module S M] -> [SMulCommClass R S M] -> [SMulCommClass A S M] -> [TensorProduct.CompatibleSMul R A M N] -> TensorProduct A M N →ₗ[S] TensorProduct R M N
<!-- PINNED-SIGNATURE:END -->


`VTask.mapOfCompatibleSMul : (R : Type u_1) -> [CommSemiring R] -> (A : Type u_22) -> (S : Type u_23) -> (M : Type u_24) -> (N : Type u_25) -> [AddCommMonoid M] -> [AddCommMonoid N] -> [Module R M] -> [Module R N] -> [CommSemiring A] -> [Module A M] -> [Module A N] -> [SMulCommClass R A M] -> [CommSemiring S] -> [Module S M] -> [SMulCommClass R S M] -> [SMulCommClass A S M] -> [TensorProduct.CompatibleSMul R A M N] -> TensorProduct A M N →ₗ[S] TensorProduct R M N`

- **R** is the "target" commutative semiring: the map lands in the tensor product M ⊗[R] N balanced over R.
- **A** is the "source" commutative semiring: the map starts from the tensor product M ⊗[A] N balanced over A.
- **S** is the "coefficient" commutative semiring over which the resulting linear map is declared to be linear; S acts on M, and its action must commute with both the R- and A-actions.
- **M** and **N** are the two additive commutative monoids serving as the left and right factors of the tensor products; each carries an R-module structure and an A-module structure, and M also carries an S-module structure.
- The `SMulCommClass` instances express that the scalar actions of R on A-scalars (on M), R on S-scalars (on M), and A on S-scalars (on M) all commute with each other.
- The `TensorProduct.CompatibleSMul R A M N` instance is the key hypothesis asserting that the A-scalar action on M ⊗[R] N can be moved across the tensor symbol, i.e., (a • m) ⊗[R] n = m ⊗[R] (a • n) for all a : A, m : M, n : N.

### Conventions

No junk-value or edge conventions are declared for this definition: it constructs a specific linear map from a universally defined tensor product to another, and there are no boundary inputs or degenerate cases for which a special convention is needed beyond the universal properties of tensor products themselves.

### Worked examples

- Claim: For any pure tensor m ⊗ n in M ⊗[A] N, the map `VTask.mapOfCompatibleSMul R A S M N` sends it to the pure tensor m ⊗ n in M ⊗[R] N.

- Claim: The map `VTask.mapOfCompatibleSMul R A S M N` is surjective, meaning every element of M ⊗[R] N is in its image.

- Claim: For any s : S and x : M ⊗[A] N, `VTask.mapOfCompatibleSMul R A S M N (s • x) = s • VTask.mapOfCompatibleSMul R A S M N x`, reflecting S-linearity of the map.

### Boundaries

- When R = A (the two rings coincide), the map is the identity up to canonical isomorphism, since a tensor product balanced over R and one balanced over A are the same object and the compatibility condition is trivially satisfied.
- The map is always well-defined as long as the `CompatibleSMul` hypothesis holds; this hypothesis is the essential content ensuring the A-balanced and R-balanced relations are compatible.
- The map is always **surjective** (this is a theorem in Mathlib). It need not be injective in general.
- When M or N is zero as an abelian group, both tensor products are trivially zero and the map is the zero map.

### Not to be confused with

- `TensorProduct.AlgebraTensorModule.cancelBaseChange`: a related isomorphism in the algebra setting that identifies tensor products over intermediate rings, which is an isomorphism rather than merely a surjection.
- `TensorProduct.lift`: the universal property map used internally to construct this map; it produces a linear map out of a tensor product from a bilinear map, but does not itself change the ring of scalars.
- `TensorProduct.map`: the functoriality map that changes the module maps (the factors M and N) rather than the ring over which the tensor product is taken.