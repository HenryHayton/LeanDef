## Object

`VTask.of` is the canonical monoid homomorphism that embeds one of the factor monoids into their free product (coproduct in the category of monoids). Given a family of monoids indexed by a type `ι`, and a chosen index `i`, it sends each element of `M i` to the corresponding element sitting inside `Monoid.CoprodI M`. This map is the universal inclusion that makes `Monoid.CoprodI M` the coproduct: every element of each summand `M i` is faithfully represented inside the free product, and these inclusions are jointly responsible for generating the whole coproduct.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.of : {ι : Type u_1} -> {M : ι → Type u_2} -> [(i : ι) → Monoid (M i)] -> {i : ι} -> M i →* Monoid.CoprodI M
<!-- PINNED-SIGNATURE:END -->


The index type `ι` and family of types `M : ι → Type` are implicit; the typeclass argument supplies a `Monoid` structure on each `M i`. The chosen index `i : ι` (also implicit) selects which summand is being embedded. The result is a monoid homomorphism `M i →* Monoid.CoprodI M`, i.e., an element of the type of structure-preserving maps from the `i`-th factor monoid to the free product.

## Conventions

There are no declared junk-value or edge conventions for this definition: it is a total construction of a `MonoidHom`, well-defined for every choice of index `i` and every element of `M i`, including the identity element (which is mapped to the identity of the free product by the monoid homomorphism laws).

## Worked examples

- Claim: Applying `VTask.of` to the identity of `M i` yields the identity of `Monoid.CoprodI M` (this follows from `map_one` for any monoid homomorphism).

- Claim: Applying `VTask.of` to a product `x * y` in `M i` equals the product of `VTask.of x` and `VTask.of y` in `Monoid.CoprodI M` (this is `map_mul` for any monoid homomorphism).

- Claim: For a family of groups indexed by `Fin 2`, the image of a non-identity element under `VTask.of` at index `0` is distinct from the image of a non-identity element under `VTask.of` at index `1`, because the free product keeps the generators of different factors apart.

- Claim: The composite of `VTask.of` (at index `i`) followed by the universal map `Monoid.CoprodI.lift` (with component maps `f`) equals `f i`; this is the defining universal property of the coproduct inclusion.

## Boundaries

- When the family has a single summand (i.e., `ι` is a one-element type), `VTask.of` is an isomorphism between `M i` and the free product, which degenerates to `M i` itself.
- When `M i` is the trivial monoid (only the identity), `VTask.of` sends the sole element to the identity of the free product.
- The map is injective for every `i`: distinct elements of `M i` map to distinct elements of the free product. This is a non-trivial fact about the construction of the free product.
- There is no restriction on the index `i` or on which element of `M i` is provided; the map is defined on all inputs.

## Not to be confused with

- `Monoid.CoprodI.lift`: the universal map *out of* the free product induced by a family of homomorphisms from each summand; `VTask.of` is the inclusion *into* the free product, while `lift` goes in the opposite direction.
- `FreeProduct.iof` or direct sum inclusions in additive settings: the free product `CoprodI` is a non-commutative coproduct of monoids, not the direct sum; inclusions into a direct sum commute with each other, while images of `VTask.of` at different indices generate a genuinely non-abelian structure.
- `MonoidHom.id`: the identity homomorphism on a single monoid; `VTask.of` is not the identity but rather an embedding into a strictly larger (or equal) structure.