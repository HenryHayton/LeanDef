## Object

`VTask.ofLinearMap` constructs an algebra homomorphism `A →ₐ[R] B` from a linear map `f : A →ₗ[R] B` together with proofs that `f` preserves the multiplicative unit and multiplication. In other words, if a map between two `R`-algebras is already known to be `R`-linear, one can "upgrade" it to a full algebra map by supplying the two missing multiplicative axioms.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofLinearMap : {R : Type u} -> {A : Type v} -> {B : Type w} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> (f : A →ₗ[R] B) -> (map_one : f 1 = 1) -> (map_mul : ∀ (x y : A), f (x * y) = f x * f y) -> A →ₐ[R] B
<!-- PINNED-SIGNATURE:END -->


`VTask.ofLinearMap : {R : Type u} -> {A : Type v} -> {B : Type w} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> (f : A →ₗ[R] B) -> (map_one : f 1 = 1) -> (map_mul : ∀ (x y : A), f (x * y) = f x * f y) -> A →ₐ[R] B`

The scalar semiring `R` is the common base over which both algebras are defined. `A` and `B` are the source and target `R`-algebras respectively. The argument `f` is the underlying `R`-linear map to be promoted. `map_one` is a proof that `f` sends the multiplicative identity of `A` to the multiplicative identity of `B`. `map_mul` is a proof that `f` distributes over multiplication for all pairs of elements.

## Conventions

The commutativity condition with the algebra structure maps (i.e., that `f (algebraMap R A r) = algebraMap R B r` for all scalars `r`) is derived automatically from `R`-linearity and the preservation of `1`; the caller need not supply this proof separately.

## Worked examples

- Claim: Applying `VTask.ofLinearMap` to `LinearMap.id` with the appropriate trivial proofs yields the identity algebra homomorphism `AlgHom.id R A`.

- Claim: For any algebra homomorphism `φ : A →ₐ[R] B`, applying `VTask.ofLinearMap` to `φ.toLinearMap` (with the proofs that `φ` preserves `1` and `*`) recovers `φ` itself.

- Claim: The underlying linear map of `VTask.ofLinearMap f map_one map_mul` is exactly `f`; that is, converting back via `toLinearMap` is a left inverse to `VTask.ofLinearMap`.

## Boundaries

- The construction is total: as long as the two proofs `map_one` and `map_mul` are supplied, there are no restrictions on `R`, `A`, `B`, or `f`.
- The `commutes` axiom (compatibility with `algebraMap`) is not an independent input; it is always satisfied automatically given linearity and `map_one`, so there is no edge case around it.
- The result is definitionally equal to the original linear map on the underlying function, so any computation that depends only on the function values is unchanged by the promotion.

## Not to be confused with

- `AlgHom.id` — the identity algebra homomorphism constructed directly, not via promotion of a linear map.
- `LinearMap.toAddMonoidHom` — converts a linear map to an additive group homomorphism only, discarding both the scalar and multiplicative structures.
- `RingHom.toAlgHom` — promotes a ring homomorphism (rather than a linear map) to an algebra homomorphism, requiring compatibility with `algebraMap` as an explicit hypothesis rather than deriving it from linearity.