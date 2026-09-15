## Object

`VTask.isRepresentation R b` is the subalgebra of the full matrix algebra `Matrix ι ι R` consisting precisely of those square matrices that actually represent some `R`-linear endomorphism of `M` with respect to the indexed family of vectors `b : ι → M`. In other words, a matrix `A` belongs to this subalgebra if and only if there exists an `R`-module endomorphism `f : M →ₗ[R] M` such that `A` is the matrix of `f` in the basis (or generating family) `b`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.isRepresentation : {ι : Type u_1} -> [Fintype ι] -> {M : Type u_2} -> [AddCommGroup M] -> (R : Type u_3) -> [CommRing R] -> [Module R M] -> (b : ι → M) -> [DecidableEq ι] -> Subalgebra R (Matrix ι ι R)
<!-- PINNED-SIGNATURE:END -->


`VTask.isRepresentation : {ι : Type u_1} -> [Fintype ι] -> {M : Type u_2} -> [AddCommGroup M] -> (R : Type u_3) -> [CommRing R] -> [Module R M] -> (b : ι → M) -> [DecidableEq ι] -> Subalgebra R (Matrix ι ι R)`

The index type `ι` is the finite type that parameterises rows and columns; the `Fintype ι` instance ensures the index set is finite. `M` is the underlying `R`-module and carries an `AddCommGroup` and `Module R M` instance. `R` is the commutative ring of scalars. The explicit argument `b : ι → M` is the ordered family of vectors of `M` that plays the role of the basis (or more generally a generating/representing family) with respect to which endomorphisms are expressed as matrices. The `DecidableEq ι` instance is needed for matrix-level computations.

## Conventions

No junk-value or out-of-domain conventions apply: the definition is total over all inputs satisfying the stated type-class assumptions, and its carrier is defined by an existential condition that is perfectly meaningful for any such inputs.

## Worked examples

- Claim: The identity matrix belongs to `VTask.isRepresentation R b` for any valid `b`, because the identity endomorphism is represented by the identity matrix.

- Claim: The zero matrix belongs to `VTask.isRepresentation R b` because the zero endomorphism is represented by the zero matrix.

- Claim: If `A₁` and `A₂` both belong to `VTask.isRepresentation R b`, then so does `A₁ + A₂`, since the sum of the representing endomorphisms represents the sum matrix. (This is guaranteed by the subalgebra structure.)

- Claim: If `A₁` and `A₂` both belong to `VTask.isRepresentation R b`, then so does `A₁ * A₂`, since composition of endomorphisms corresponds to matrix multiplication. (Again guaranteed by the subalgebra structure.)

## Boundaries

- When `ι` is empty (the trivial case), every `0 × 0` matrix trivially represents the unique endomorphism of `M` at that index type, so the subalgebra is all of `Matrix ι ι R`.
- When `b` is a basis of `M`, every matrix `A` over `R` represents exactly one endomorphism, so `VTask.isRepresentation R b` equals the full matrix algebra `Matrix ι ι R`.
- When `b` does not span `M`, the subalgebra may be a proper subalgebra: not every matrix corresponds to a well-defined endomorphism.
- The scalar matrices (images of the algebra map from `R`) always belong to the subalgebra, since scalar multiplications are representable.

## Not to be confused with

- `Matrix.Represents b f` — this is the *predicate* asserting that a specific matrix represents a specific endomorphism `f`; `VTask.isRepresentation` collects all matrices satisfying this predicate for *some* `f`.
- `LinearMap.toMatrix` / `Matrix.toLin` — these are the bijections converting between endomorphisms and matrices when `b` is a basis; `VTask.isRepresentation` is a subalgebra, not a linear map or equivalence.
- `Module.End R M` itself — this is the algebra of endomorphisms of `M`; `VTask.isRepresentation R b` is its image inside the matrix algebra, which may not be all matrices.