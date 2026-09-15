## Object

`VTask.ofArchimedean f` is the ordered ring homomorphism (an order-preserving ring map) from an Archimedean ordered commutative ring `R` into `ArchimedeanClass.FiniteResidueField K`, constructed from a given ordered ring embedding `f : R →+*o K`. Conceptually, every element of the Archimedean ring `R` maps to a finite (non-infinitely-large) element of `K`, and `FiniteResidueField K` is the subquotient of `K` consisting of those finite elements modulo the infinitesimals; the Archimedean property of `R` guarantees that `f` always lands in the finite part, so the composite into the residue field is well-defined.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofArchimedean : {K : Type u_1} -> [LinearOrder K] -> [Field K] -> [IsOrderedRing K] -> {R : Type u_2} -> [LinearOrder R] -> [CommRing R] -> [IsStrictOrderedRing R] -> [Archimedean R] -> (f : R →+*o K) -> R →+*o ArchimedeanClass.FiniteResidueField K
<!-- PINNED-SIGNATURE:END -->


`VTask.ofArchimedean : {K : Type u_1} -> [LinearOrder K] -> [Field K] -> [IsOrderedRing K] -> {R : Type u_2} -> [LinearOrder R] -> [CommRing R] -> [IsStrictOrderedRing R] -> [Archimedean R] -> (f : R →+*o K) -> R →+*o ArchimedeanClass.FiniteResidueField K`

`K` is the target ordered field (supplied implicitly); `R` is the source Archimedean strictly-ordered commutative ring (supplied implicitly). The single explicit argument `f` is the ordered ring homomorphism from `R` into `K` that is to be lifted to the finite-residue-field level. The output is an ordered ring homomorphism from `R` into `ArchimedeanClass.FiniteResidueField K`.

## Conventions

No junk-value or boundary conventions are declared for this construction: it is a total, well-typed function on its domain with no degenerate inputs.

## Worked examples

- Claim: `VTask.ofArchimedean f` is injective for any ordered ring embedding `f : R →+*o K`.

- Claim: For any `r : R`, the value `VTask.ofArchimedean f r` equals `mk (.mk _ (mk_map_nonneg_of_archimedean f r))` — i.e., it is the class of `f r` viewed as a finite element.

- Claim: `VTask.ofArchimedean f` preserves zero: its value at `0 : R` equals `0` in `ArchimedeanClass.FiniteResidueField K`.

- Claim: `VTask.ofArchimedean f` preserves order: if `x ≤ y` in `R`, then `VTask.ofArchimedean f x ≤ VTask.ofArchimedean f y` in `ArchimedeanClass.FiniteResidueField K`.

## Boundaries

- Because `R` is required to be Archimedean, every element of `R` is "finite" relative to `K`, so the map is always defined with no truncation or clamping. If `R` were non-Archimedean this construction would not type-check.
- The map is always injective (as `ofArchimedean_injective` records), so distinct elements of `R` always give distinct elements of the finite residue field.
- When `R` itself is a field and the map `f` is an ordered field embedding, the resulting map into `ArchimedeanClass.FiniteResidueField K` is still only a ring homomorphism (the target is a ring, not necessarily a field).

## Not to be confused with

- `ArchimedeanClass.FiniteResidueField` itself — that is the type (the quotient ring of finite elements by infinitesimals), not the map into it.
- The standard-part map on `K` — that goes from finite elements of `K` to the residue field, whereas `VTask.ofArchimedean` starts from an external Archimedean ring `R` with a given embedding.
- A plain ring homomorphism `R →+* ArchimedeanClass.FiniteResidueField K` — `VTask.ofArchimedean` additionally carries the order-preserving datum, making it an ordered ring map `R →+*o …`.