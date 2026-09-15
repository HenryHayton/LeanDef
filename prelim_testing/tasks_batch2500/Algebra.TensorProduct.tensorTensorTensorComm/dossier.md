## Object

`VTask.tensorTensorTensorComm` is an algebra isomorphism (equivalence of algebras) that rearranges a fourfold tensor product. Specifically, starting from the algebra `(A ⊗[R'] B) ⊗[S] (C ⊗[R] D)`, it produces a canonical isomorphism to `(A ⊗[S] C) ⊗[R'] (B ⊗[R] D)`. In other words, it "interleaves" the four factors: it moves the `B` and `C` factors so that the two algebras sharing the `S`-scalar structure end up together, and the two sharing the `R'`-scalar structure end up together. This is the tensor-product-of-algebras analogue of the ring identity `(ac)(bd) = (ab)(cd)`, i.e., `mul_mul_mul_comm`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.tensorTensorTensorComm : (R : Type uR) -> (R' : Type u_1) -> (S : Type uS) -> (T : Type u_2) -> (A : Type uA) -> (B : Type uB) -> (C : Type uC) -> (D : Type uD) -> [CommSemiring R] -> [CommSemiring S] -> [Algebra R S] -> [Semiring A] -> [Algebra R A] -> [Algebra S A] -> [IsScalarTower R S A] -> [Semiring B] -> [Algebra R B] -> [Semiring C] -> [Algebra R C] -> [Algebra S C] -> [IsScalarTower R S C] -> [Semiring D] -> [Algebra R D] -> [CommSemiring T] -> [Algebra R T] -> [Algebra T A] -> [IsScalarTower R T A] -> [SMulCommClass S T A] -> [Algebra S T] -> [IsScalarTower S T A] -> [CommSemiring R'] -> [Algebra R R'] -> [Algebra R' T] -> [Algebra R' A] -> [Algebra R' B] -> [IsScalarTower R R' A] -> [SMulCommClass S R' A] -> [SMulCommClass R' S A] -> [IsScalarTower R' T A] -> [IsScalarTower R R' B] -> TensorProduct S (TensorProduct R' A B) (TensorProduct R C D) ≃ₐ[T]
    TensorProduct R' (TensorProduct S A C) (TensorProduct R B D)
<!-- PINNED-SIGNATURE:END -->


The first argument `R` is the base commutative semiring sitting at the bottom of the scalar tower. The second argument `R'` is an intermediate commutative semiring extending `R`, serving as the scalar ring for the outer tensor product on one side and an inner tensor on the other. The third argument `S` is another intermediate commutative semiring extending `R`, serving as the outer tensor product scalar on the input and inner on the output for the `A`–`C` pair. The fourth argument `T` is the commutative semiring over which the resulting algebra isomorphism is linear (i.e., `T` is the scalar ring of the `AlgEquiv`). The arguments `A`, `B`, `C`, `D` are the four algebra factors being rearranged: `A` appears in both tensor products over `S` and `R'`; `B` is tensored over `R'` on the left and `R` on the right; `C` is tensored over `R` on the left and `S` on the right; `D` sits inside the `R`-tensor product on both sides. The remaining arguments are the required typeclasses expressing that all scalar towers are compatible, all algebra structures are consistent, and that the various scalar actions commute as needed for the rearrangement to be an algebra map.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a construction of a specific algebra equivalence, total in all its arguments, and the interesting behavior is determined entirely by the typeclass assumptions.

## Worked examples

- Claim: When all four algebras `A`, `B`, `C`, `D` are taken to be the base ring itself (with `R = R' = S = T`), `VTask.tensorTensorTensorComm` gives an algebra isomorphism between two copies of the four-fold tensor product that is naturally the identity on elements of the form `(a ⊗ b) ⊗ (c ⊗ d)`.

- Claim: The underlying linear equivalence of `VTask.tensorTensorTensorComm` agrees with `TensorProduct.AlgebraTensorModule.tensorTensorTensorComm`, meaning on a pure tensor `(a ⊗ b) ⊗ (c ⊗ d)` it sends this to `(a ⊗ c) ⊗ (b ⊗ d)`.

- Claim: `VTask.tensorTensorTensorComm` is an isomorphism, so its inverse composed with itself is the identity `AlgEquiv`.

## Boundaries

- All typeclass arguments must be satisfied simultaneously; if any scalar tower or commutativity condition fails, the definition cannot be applied. There is no meaningful "degenerate" input in the ring-theoretic sense.
- When `R = R' = S = T` and all algebras coincide, the isomorphism still produces a non-trivial rearrangement of tensor factors (it is not definitionally the identity).
- The isomorphism is `T`-linear (it lives in `AlgEquiv T`), not merely `R`-linear; this is a stronger statement that depends on the full typeclass tower.
- The definition is total: no domain restriction is imposed beyond the typeclass constraints.

## Not to be confused with

- `TensorProduct.AlgebraTensorModule.tensorTensorTensorComm`: the underlying *linear* equivalence (not bundled as an algebra map) performing the same rearrangement at the level of modules.
- `TensorProduct.comm`: the simpler flip isomorphism `A ⊗ B ≃ B ⊗ A` for a two-fold tensor product, not a fourfold rearrangement.
- `TensorProduct.assoc`: the associativity isomorphism `(A ⊗ B) ⊗ C ≃ A ⊗ (B ⊗ C)`, which reorganizes parenthesization rather than interleaving four factors.