## Object

`VTask.opEquiv` is a multiplicative isomorphism (a `MulEquiv`) between two groups of units that arise naturally when combining the "opposite monoid" and "units" constructions on a monoid `M`. Specifically, it establishes that the units of the opposite monoid of `M` (written `Mᵐᵒᵖˣ`) are canonically isomorphic, as multiplicative groups, to the opposite of the units of `M` (written `Mˣᵐᵒᵖ`). In other words, it does not matter whether one first forms the opposite monoid and then takes invertible elements, or first takes invertible elements and then passes to the opposite group — the two constructions yield isomorphic objects.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.opEquiv : {M : Type u_2} -> [Monoid M] -> Mᵐᵒᵖˣ ≃* Mˣᵐᵒᵖ
<!-- PINNED-SIGNATURE:END -->


`VTask.opEquiv : {M : Type u_2} -> [Monoid M] -> Mᵐᵒᵖˣ ≃* Mˣᵐᵒᵖ`

The implicit type argument `M` is the underlying monoid whose units and opposite construction are being compared. The instance argument supplies the monoid structure on `M`. The equivalence itself takes no further arguments; it is a single canonical isomorphism between the two unit-opposite composites.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total construction on any monoid, and all its inputs are well-typed structures without exceptional cases.

## Worked examples

- Claim: The underlying element of `VTask.opEquiv u`, unop-ped back to `M`, equals the unop of the coercion of `u` to `Mᵐᵒᵖ`. That is, `((VTask.opEquiv u).unop : M) = unop (u : Mᵐᵒᵖ)` for any `u : Mᵐᵒᵖˣ`.

- Claim: The inverse map `VTask.opEquiv.symm` sends a unit `u : Mˣᵐᵒᵖ` to an element of `Mᵐᵒᵖ` equal to `op (u.unop : M)`. That is, `(VTask.opEquiv.symm u : Mᵐᵒᵖ) = op (u.unop : M)`.

- Claim: `VTask.opEquiv` composed with its own inverse is the identity, i.e., `VTask.opEquiv.symm.trans VTask.opEquiv = MulEquiv.refl _` (global structural property: it is a genuine isomorphism).

- Claim: For `M = ℤ`, a unit `u` in `ℤᵐᵒᵖˣ` is sent by `VTask.opEquiv` to an element of `ℤˣᵐᵒᵖ` whose underlying unit in `ℤˣ` has the same value (under the natural identification of `ℤ` with `ℤᵐᵒᵖ`).

## Boundaries

- The isomorphism is defined for any monoid `M`; in particular it works for commutative monoids, groups, and trivial monoids, though in the commutative case `Mᵐᵒᵖ` is isomorphic to `M` itself and the distinction between the two composites collapses.
- When `M` is the trivial monoid (a single-element type with a trivial multiplication), both sides have exactly one element and the isomorphism is trivially the identity.
- The forward map respects the multiplicative structure: `VTask.opEquiv (u * v) = VTask.opEquiv u * VTask.opEquiv v`.
- The inverse `VTask.opEquiv.symm` is also a `MulEquiv` and provides the reverse direction without any additional hypotheses.

## Not to be confused with

- `MulOpposite.opEquiv` (if it exists): a potential equivalence relating `M` and `Mᵐᵒᵖ` at the monoid level, not at the level of units.
- The coercion map `Mᵐᵒᵖˣ → Mᵐᵒᵖ`: this forgets invertibility and is merely a monoid homomorphism to the underlying type, not an isomorphism between unit groups.
- The additive analogue `AddUnits.opEquiv` for additive monoids: exchanges `+` for `*` throughout but is otherwise the same pattern.
