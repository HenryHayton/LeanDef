## Object

`VTask.map f` is the group homomorphism from the group of units of `M` to the group of units of `N` induced by a monoid homomorphism `f : M →* N`. Given a unit `u ∈ Mˣ` (i.e., an invertible element of `M` together with its two-sided inverse), the map sends `u` to the corresponding unit in `Nˣ` whose underlying element is `f(u)` and whose inverse is `f(u⁻¹)`. This is well-defined because `f` preserves multiplication and hence carries invertible elements to invertible elements. The result is itself a monoid (in fact group) homomorphism from `Mˣ` to `Nˣ`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {M : Type u} -> {N : Type v} -> [Monoid M] -> [Monoid N] -> (f : M →* N) -> Mˣ →* Nˣ
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {M : Type u} -> {N : Type v} -> [Monoid M] -> [Monoid N] -> (f : M →* N) -> Mˣ →* Nˣ`

The implicit arguments `M` and `N` are the source and target monoids (supplied by unification). The instance arguments supply the monoid structures on `M` and `N`. The explicit argument `f` is the monoid homomorphism from `M` to `N` that drives the construction; its domain and codomain determine which unit groups appear in the output type.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a total, structure-preserving construction that is well-defined for every monoid homomorphism `f` and every unit of `M`.

## Worked examples

- Claim: Applying `VTask.map` to the identity monoid homomorphism `MonoidHom.id M` yields the identity homomorphism on `Mˣ`.

- Claim: For the unique monoid homomorphism `f : M →* N` into a trivial monoid, `VTask.map f` sends every unit of `M` to the single unit of `Nˣ`, i.e., the map factors through the trivial group.

- Claim: `VTask.map` respects composition: for `f : M →* N` and `g : N →* P`, the homomorphisms `VTask.map (g.comp f)` and `(VTask.map g).comp (VTask.map f)` coincide as maps `Mˣ →* Pˣ`.

- Claim: For `u : Mˣ`, the underlying element of `(VTask.map f) u` in `N` equals `f u.val`.

## Boundaries

- When `f` is the identity monoid homomorphism on `M`, `VTask.map f` is the identity homomorphism on `Mˣ`.
- When `M` or `N` is the trivial (one-element) monoid, the unit group is also trivial, and `VTask.map f` is necessarily the unique homomorphism between trivial groups.
- When `f` is injective, `VTask.map f` is injective on `Mˣ`; when `f` is surjective, `VTask.map f` need not be surjective on `Nˣ` in general (only units in the image of `f` whose preimage is a unit are reached).
- The map correctly tracks two-sided inverses: the inverse of `(VTask.map f) u` inside `Nˣ` is exactly the image under `f` of the inverse of `u` inside `Mˣ`.

## Not to be confused with

- `Units.liftRight` / coercion-based lifts: constructions that try to invert elements of `N` by other means rather than by applying `f` to known inverses in `M`.
- The coercion `Mˣ → M` (or `Units.val`): this is simply the forgetful map embedding units into the monoid, not a homomorphism induced by `f`.
- `MonoidHom.comp`: this composes two existing monoid homomorphisms, whereas `VTask.map` constructs a new homomorphism on unit groups from one on the ambient monoids.