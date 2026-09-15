## VTask.Represents

### Object

Given a finite index type `ι`, an `R`-module `M`, and a family of elements `b : ι → M` (thought of as a spanning set of `M`), `VTask.Represents b A f` is the proposition that the square matrix `A` (indexed by `ι`) **represents** the `R`-linear endomorphism `f : M → M` with respect to the spanning family `b`. Concretely, this means that for every vector `x : ι → R`, taking the linear combination of the columns of `A` weighted by `x` via `b` yields the same element of `M` as first forming the linear combination of `b` weighted by `x` and then applying `f`. Equivalently, the map `(ι → R) → M` induced by `A` through `b` coincides with the map `(ι → R) → M` induced by `f` through `b`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Represents : {ι : Type u_1} -> [Fintype ι] -> {M : Type u_2} -> [AddCommGroup M] -> {R : Type u_3} -> [CommRing R] -> [Module R M] -> (b : ι → M) -> [DecidableEq ι] -> (A : Matrix ι ι R) -> (f : Module.End R M) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Represents : {ι : Type u_1} -> [Fintype ι] -> {M : Type u_2} -> [AddCommGroup M] -> {R : Type u_3} -> [CommRing R] -> [Module R M] -> (b : ι → M) -> [DecidableEq ι] -> (A : Matrix ι ι R) -> (f : Module.End R M) -> Prop`

- `ι` is the finite index type that simultaneously indexes the rows and columns of the matrix and the elements of the spanning family.
- The `Fintype ι` instance makes the index set finite, so finite linear combinations are well-defined.
- `M` is the `R`-module in which the endomorphism lives.
- `AddCommGroup M` and `CommRing R` provide the algebraic structure needed for a module.
- `Module R M` specifies the `R`-module structure on `M`.
- `b : ι → M` is the spanning family (a function sending each index to an element of `M`); it plays the role of the basis or spanning set through which the matrix is interpreted.
- `DecidableEq ι` is a technical instance needed for matrix and linear-combination computations over `ι`.
- `A : Matrix ι ι R` is the square matrix whose representational role is being asserted.
- `f : Module.End R M` is the `R`-linear endomorphism of `M` that `A` is claimed to represent.

### Conventions

No junk-value or edge-case output conventions are declared for this definition: it is a `Prop`-valued relation, so it either holds or does not, and there are no default fallback values to specify.

### Worked examples

- Claim: The zero matrix represents the zero endomorphism with respect to any spanning family `b`.

- Claim: The identity matrix `(1 : Matrix ι ι R)` represents the identity endomorphism `(1 : Module.End R M)` with respect to any spanning family `b`.

- Claim: If `A` represents `f` and `A'` represents `f'` (both with respect to `b`), then `A + A'` represents `f + f'`.

- Claim: If `A` represents `f` and `A'` represents `f'` (both with respect to `b`), then `A * A'` represents `f * f'` (composition of endomorphisms).

- Claim: The scalar matrix `algebraMap R (Matrix ι ι R) r` represents `algebraMap R (Module.End R M) r` (scalar multiplication by `r`) for any `r : R`.

### Boundaries

- When the span of the family `b` is not all of `M` (i.e., `b` is not spanning), a given matrix `A` may represent two distinct endomorphisms simultaneously; uniqueness of the represented endomorphism requires the spanning condition `Submodule.span R (Set.range b) = ⊤`.
- When `ι` is empty (no indices), the only matrix is the empty matrix and the only endomorphism representable is the zero map; the relation still makes sense and the zero matrix represents the zero endomorphism.
- The relation is not required to be an equivalence relation on matrices; a single matrix can represent at most one endomorphism when `b` is spanning, but may represent none if no `R`-linear endomorphism is consistent with the matrix action through `b`.
- Scalar multiples, sums, and products of representing pairs again represent the corresponding scalar multiple, sum, and product, so the representing relation is compatible with the ring and module structure on both sides.

### Not to be confused with

- **The matrix of a linear map in a basis** (e.g., `LinearMap.toMatrix`): that construction requires `b` to be an actual basis (linearly independent and spanning), whereas `VTask.Represents` only requires a spanning family and is a relation rather than a function.
- **`Matrix.toLin`**: this converts a matrix to a linear map on `ι → R`, not to an endomorphism of an arbitrary module `M` via a spanning family.
- **`Module.Basis.repr`**: the coordinate representation of an element in a basis, a different direction of the correspondence (element → coordinates rather than matrix ↔ endomorphism).