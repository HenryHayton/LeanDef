## Object

Given a ring homomorphism `f : R →+* S`, `VTask.map f` is the induced group homomorphism `GLₙ(R) →* GLₙ(S)` that applies `f` entry-wise to each invertible matrix. Concretely, if `M` is an invertible `n × n` matrix over `R`, then `VTask.map f` sends `M` to the invertible `n × n` matrix over `S` obtained by applying `f` to every entry of `M` (and similarly to its inverse). The resulting function is a group homomorphism: it respects matrix multiplication and sends the identity to the identity.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {n : Type u} -> [DecidableEq n] -> [Fintype n] -> {R : Type v} -> [CommRing R] -> {S : Type u_1} -> [CommRing S] -> (f : R →+* S) -> GL n R →* GL n S
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {n : Type u} -> [DecidableEq n] -> [Fintype n] -> {R : Type v} -> [CommRing R] -> {S : Type u_1} -> [CommRing S] -> (f : R →+* S) -> GL n R →* GL n S`

The index type `n` determines the "size" (shape) of the square matrices; it must be a `Fintype` with decidable equality so that matrix operations are well-defined and computable. `R` and `S` are commutative rings. The argument `f` is a ring homomorphism from `R` to `S`; it is the datum that drives the entry-wise transformation of matrices. The output is a monoid (group) homomorphism from the general linear group over `R` to the general linear group over `S`.

## Conventions

There are no special junk-value or edge-case conventions declared for this definition: it is a total construction that is well-defined for every ring homomorphism `f` and every invertible matrix, including the identity element and trivially small index types.

## Worked examples

- Claim: For the identity ring homomorphism `id : R →+* R`, the induced map `VTask.map (RingHom.id R)` sends every invertible matrix to itself (i.e., it is the identity group homomorphism on `GL n R`).

- Claim: For a ring homomorphism `f : R →+* S` and invertible matrices `M`, `N` in `GL n R`, we have `VTask.map f (M * N) = VTask.map f M * VTask.map f N` (the map is a homomorphism).

- Claim: For the composition of ring homomorphisms `g ∘ f : R →+* T`, the induced map satisfies `VTask.map (g.comp f) = (VTask.map g).comp (VTask.map f)` (functoriality).

- Claim: For the zero-dimensional index type (`n = Fin 0`), `VTask.map f` is a homomorphism between trivial groups, both being isomorphic to the trivial group, so it is necessarily the trivial homomorphism.

## Boundaries

- **Empty index type (`n = Fin 0` or any type with no elements):** The general linear group `GL (Fin 0) R` is a trivial group (there is exactly one `0 × 0` invertible matrix over any ring), and `VTask.map f` is the unique (trivial) homomorphism between two trivial groups. This is well-defined and non-degenerate.
- **`Fin 1` index:** `GL (Fin 1) R` is isomorphic to the group of units `Rˣ`, and `VTask.map f` corresponds to the units map induced by `f`, sending the `1 × 1` matrix `[[u]]` to `[[f u]]`.
- **Non-injective `f`:** If `f` has a nontrivial kernel, then `VTask.map f` need not be injective; matrices that differ only in the kernel of `f` may be identified.
- **Non-surjective `f`:** The image of `VTask.map f` consists precisely of invertible matrices whose entries all lie in the image of `f`.

## Not to be confused with

- `Matrix.map`: Applies a bare function `R → S` entry-wise to a matrix without any invertibility or ring-homomorphism requirements, yielding a plain matrix rather than an element of a general linear group.
- `Units.map`: The general construction sending a monoid homomorphism `M →* N` to a group homomorphism `Mˣ →* Nˣ` on units; `VTask.map` is the specialization of this idea to matrix rings.
- `RingHom.mapMatrix`: The ring homomorphism `Matrix n n R →+* Matrix n n S` induced by `f`; `VTask.map f` is the restriction of this to invertible matrices, with the additional structure of being a group homomorphism between the respective GL groups.