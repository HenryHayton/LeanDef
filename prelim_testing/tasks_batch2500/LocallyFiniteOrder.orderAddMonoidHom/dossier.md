## Object

`VTask.orderAddMonoidHom` is the canonical embedding of a linearly ordered, locally finite, cancellative additive commutative group `G` into the integers `ℤ`, packaged as an *ordered additive monoid homomorphism* (`G →+o ℤ`). It is the unique (up to sign) order-and-monoid-compatible map from such a group to `ℤ`; the theorem says that this map is either surjective (when `G` is non-trivial) or identically zero (when `G` is trivial).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.orderAddMonoidHom : (G : Type u_2) -> [AddCommGroup G] -> [LinearOrder G] -> [IsOrderedAddMonoid G] -> [LocallyFiniteOrder G] -> G →+o ℤ
<!-- PINNED-SIGNATURE:END -->


`VTask.orderAddMonoidHom : (G : Type u_2) -> [AddCommGroup G] -> [LinearOrder G] -> [IsOrderedAddMonoid G] -> [LocallyFiniteOrder G] -> G →+o ℤ`

The explicit argument `G` is the source group — a type that is simultaneously an abelian additive group, a linear order compatible with addition (`IsOrderedAddMonoid`), and locally finite (every bounded interval contains finitely many elements). The remaining arguments are instance arguments supplying the required algebraic and order structure on `G`. The result is an ordered additive monoid homomorphism from `G` to `ℤ`.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a structure-valued map defined on any type satisfying the stated typeclasses, and the result is always a well-formed ordered additive monoid homomorphism (possibly the zero map when `G` is trivial).

## Worked examples

- Claim: Applying `VTask.orderAddMonoidHom ℤ` to an integer `n : ℤ` returns `n` itself, i.e., the map is the identity on `ℤ`.

- Claim: For `G = ℤ`, `VTask.orderAddMonoidHom ℤ` maps `0` to `0` (homomorphism property at the identity).

- Claim: For `G = ℤ`, `VTask.orderAddMonoidHom ℤ` is monotone: if `a ≤ b` in `ℤ` then the image of `a` is `≤` the image of `b` in `ℤ`.

- Claim: The map `VTask.orderAddMonoidHom ℤ` sends `a + b` to `(VTask.orderAddMonoidHom ℤ) a + (VTask.orderAddMonoidHom ℤ) b` for all `a b : ℤ`.

## Boundaries

- When `G` is the trivial group `{0}`, the only additive monoid homomorphism to `ℤ` is the zero map, so `VTask.orderAddMonoidHom` returns the zero map in this case.
- When `G` is non-trivial (contains a positive element), the map is surjective onto `ℤ` (or at least onto a non-zero subgroup, which must be all of `ℤ` since every non-trivial subgroup of `ℤ` is infinite cyclic and hence isomorphic to `ℤ`).
- The locally finite order condition is essential: it ensures that intervals are finite, allowing a well-defined counting argument that produces the integer value.
- The map is always a homomorphism and always monotone regardless of whether `G` is trivial; the surjectivity-or-zero dichotomy is an additional structural fact.

## Not to be confused with

- `AddMonoidHom` from `G` to `ℤ`: the plain additive monoid homomorphism without the monotonicity/order constraint bundled in.
- `OrderIso` from `G` to `ℤ`: an order isomorphism, which would additionally require the map to be bijective and have a monotone inverse; `VTask.orderAddMonoidHom` need not be an isomorphism.
- The canonical map from `G` to its *Grothendieck group* or *completion*: that construction applies to monoids and yields a group, whereas here `G` is already a group and the target `ℤ` is fixed.