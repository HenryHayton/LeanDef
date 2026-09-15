## VTask.map

### Object

Given a ring homomorphism `f : R →+* S`, `VTask.map f` is the induced group homomorphism from the special linear group `SL(n, R)` to the special linear group `SL(n, S)`. It acts by applying `f` entry-wise to the matrix representative of each element. The determinant condition (equal to 1) is preserved because ring homomorphisms commute with determinants, so the result is again a matrix of determinant 1 over `S`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {n : Type u} -> [DecidableEq n] -> [Fintype n] -> {R : Type v} -> [CommRing R] -> {S : Type u_1} -> [CommRing S] -> (f : R →+* S) -> Matrix.SpecialLinearGroup n R →* Matrix.SpecialLinearGroup n S
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {n : Type u} -> [DecidableEq n] -> [Fintype n] -> {R : Type v} -> [CommRing R] -> {S : Type u_1} -> [CommRing S] -> (f : R →+* S) -> Matrix.SpecialLinearGroup n R →* Matrix.SpecialLinearGroup n S`

- `n` is the index type parametrising the matrix size; it must be a finite type with decidable equality (so that determinants are computable).
- `R` is the source commutative ring; `S` is the target commutative ring.
- `f` is the ring homomorphism from `R` to `S` whose entry-wise action on matrices induces the group homomorphism.
- The result is a group homomorphism (a `MonoidHom`) from `SpecialLinearGroup n R` to `SpecialLinearGroup n S`.

### Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total construction on algebraic structures with no degenerate inputs.

### Worked examples

- Claim: For any `g : SpecialLinearGroup n R` and ring homomorphism `f : R →+* S`, the underlying matrix of `VTask.map f g` is obtained by applying `f` to each entry of the underlying matrix of `g`.

- Claim: The identity element of `SpecialLinearGroup n R` maps to the identity element of `SpecialLinearGroup n S` under `VTask.map f`, for any ring homomorphism `f`.

- Claim: For ring homomorphisms `f : R →+* S` and `g : S →+* T`, the composite group homomorphism `VTask.map (g.comp f)` equals the composition `(VTask.map g).comp (VTask.map f)` as group homomorphisms `SpecialLinearGroup n R →* SpecialLinearGroup n T`.

- Claim: When `f : R →+* S` is injective (e.g. an integral domain embedding), `VTask.map f` is an injective group homomorphism.

### Boundaries

- When `f` is the identity ring homomorphism `RingHom.id R`, `VTask.map f` is the identity group homomorphism on `SpecialLinearGroup n R`.
- When `n` has exactly one element, every special linear group is trivial (the single 1×1 matrix with entry 1), so `VTask.map f` is the unique trivial group homomorphism regardless of `f`.
- The construction is functorial: applying `VTask.map` to a composition of ring homomorphisms yields the composition of the induced group homomorphisms.
- If `f` is a ring isomorphism, `VTask.map f` is a group isomorphism.
- The determinant of every element in the image is 1 by construction, regardless of how degenerate `f` might be (e.g. the zero ring homomorphism to a trivial ring).

### Not to be confused with

- `Matrix.SpecialLinearGroup.mapGL`: the related map to the *general* linear group `GL n S`, which does not require the determinant-1 condition to be preserved a priori but satisfies it as a lemma.
- `Matrix.GeneralLinearGroup.map`: the analogous construction for general linear groups, which does not impose the determinant-1 constraint.
- `Matrix.map`: the bare entry-wise application of a function to a matrix, which is not a group homomorphism and does not enforce any determinant condition.