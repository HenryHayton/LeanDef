## Object

Given two submonoids `S` and `T` of a monoid `M` with `S ≤ T` (meaning every element of `S` belongs to `T`), `VTask.inclusion h` is the canonical inclusion monoid homomorphism from `S` to `T`. It sends each element of `S` to the same element viewed as an element of `T`. In other words, it is the identity map on underlying elements, packaged as a `MulOneClass`-homomorphism between the two submonoid types.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {M : Type u_1} -> [MulOneClass M] -> {S T : Submonoid M} -> (h : S ≤ T) -> ↥S →* ↥T
<!-- PINNED-SIGNATURE:END -->


`VTask.inclusion : {M : Type u_1} -> [MulOneClass M] -> {S T : Submonoid M} -> (h : S ≤ T) -> ↥S →* ↥T`

`M` is the ambient monoid type. The `MulOneClass` instance provides the multiplicative structure on `M`. `S` and `T` are submonoids of `M`, both inferred implicitly from context. The explicit argument `h` is a proof that `S ≤ T`, i.e., that every element belonging to `S` also belongs to `T`. The result is a monoid homomorphism from the submonoid type `↥S` to the submonoid type `↥T`.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total function whose output is well-defined for all valid inputs, and there are no degenerate input regimes that require a distinguished convention.

## Worked examples

- Claim: For submonoids `S ≤ T` of `ℕ` (under multiplication), `VTask.inclusion h` applied to an element `x : S` returns the element of `T` with the same underlying value as `x`.

- Claim: When `S = T` and `h : S ≤ T` is reflexivity, `VTask.inclusion h` is the identity map on `↥S` (i.e., it sends each element to itself).

- Claim: `VTask.inclusion h` is a monoid homomorphism, so it preserves the identity: `(VTask.inclusion h) 1 = 1`.

- Claim: `VTask.inclusion h` preserves multiplication: for `x y : ↥S`, `(VTask.inclusion h) (x * y) = (VTask.inclusion h) x * (VTask.inclusion h) y`.

## Boundaries

- When `S = T`, `VTask.inclusion h` (with `h` the trivial reflexivity proof) acts as the identity homomorphism on `↥S`. The type signature still gives `↥S →* ↥T`, which coincides with `↥S →* ↥S` up to definitional equality.
- When `S` is the trivial submonoid `{1}` and `T = M` (the whole monoid viewed as a submonoid), `VTask.inclusion h` embeds the one-element submonoid into `M`.
- The function is entirely determined by the underlying set-inclusion `h`; different proofs of the same inequality produce definitionally equal homomorphisms.
- Because the underlying map is literally the identity on elements, `VTask.inclusion h` is always injective.

## Not to be confused with

- `Submonoid.subtype`: the canonical embedding of a single submonoid `S` into the ambient monoid `M` (not into another submonoid `T`).
- `MonoidHom.comp`: the general composition of two monoid homomorphisms; `VTask.inclusion` is a specific instance of inclusion, not a general composition.
- The `AddSubmonoid` version: an analogous construction exists for additive submonoids, but `VTask.inclusion` is for multiplicative `Submonoid`s only.