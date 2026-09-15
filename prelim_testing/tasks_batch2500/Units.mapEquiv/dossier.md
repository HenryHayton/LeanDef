## Object

`VTask.mapEquiv` takes a multiplicative isomorphism between two monoids and produces a multiplicative isomorphism between their respective groups of units. Concretely, if `M` and `N` are monoids that are isomorphic as monoids, then their unit groups `Mˣ` and `Nˣ` are also isomorphic as groups (and as monoids). The isomorphism on units is the one induced in the natural way: a unit in `M` is sent to the corresponding unit in `N` by applying the given isomorphism, and its inverse in `N` is the image of its inverse in `M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapEquiv : {M : Type u_3} -> {N : Type u_4} -> [Monoid M] -> [Monoid N] -> (h : M ≃* N) -> Mˣ ≃* Nˣ
<!-- PINNED-SIGNATURE:END -->


`VTask.mapEquiv : {M : Type u_3} -> {N : Type u_4} -> [Monoid M] -> [Monoid N] -> (h : M ≃* N) -> Mˣ ≃* Nˣ`

The implicit type arguments `M` and `N` are the source and target monoids, inferred from context. The two instance arguments supply the monoid structures on `M` and `N` respectively. The explicit argument `h` is the multiplicative isomorphism (a `MulEquiv`) from `M` to `N` whose existence witnesses that the two monoids are isomorphic; this is the data from which the equivalence on unit groups is constructed.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a total construction on well-typed inputs with no degenerate or boundary cases requiring special treatment.

## Worked examples

- Claim: Applying `VTask.mapEquiv` to the identity isomorphism `MulEquiv.refl M` yields a `MulEquiv` whose underlying forward map sends each unit to itself.

- Claim: For any multiplicative isomorphism `h : M ≃* N`, the composition `VTask.mapEquiv h.symm` composed with `VTask.mapEquiv h` is the identity on `Mˣ`; that is, the construction is coherent with inversion of the base isomorphism.

- Claim: If `h : M ≃* N` and `u : Mˣ`, then `(VTask.mapEquiv h u : N)` equals `h (u : M)` — the coercion to the ambient monoid commutes with the underlying isomorphism.

## Boundaries

- When `h` is the identity isomorphism `MulEquiv.refl M`, the resulting equivalence `VTask.mapEquiv (MulEquiv.refl M)` acts as the identity on `Mˣ`.
- When `M = N` and `h` is an automorphism, the result is an automorphism of `Mˣ`.
- The construction is functorial: applying it to a composite isomorphism `h.trans k` yields the same result as composing the two induced unit-group isomorphisms.
- The inverse of `VTask.mapEquiv h` is `VTask.mapEquiv h.symm`.

## Not to be confused with

- `Units.map` (a plain `MonoidHom` from `Mˣ` to `Nˣ` induced by a monoid homomorphism, not a full isomorphism): `VTask.mapEquiv` requires and produces an equivalence, not merely a homomorphism.
- `MulEquiv.units` or similar constructions that embed or relate unit types in other ways: `VTask.mapEquiv` specifically lifts a monoid isomorphism to an isomorphism of unit groups.
- `Units.equiv` or universe-polymorphic unit-group equivalences arising from type equivalences rather than algebraic isomorphisms.