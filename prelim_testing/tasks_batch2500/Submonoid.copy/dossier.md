## Object

`VTask.copy` produces a new submonoid of `M` that is definitionally equal (as a submonoid) to a given submonoid `S`, but whose underlying carrier set is replaced by a (propositionally) equal set `s`. The resulting submonoid has the same one-membership and multiplication-closure properties as `S`, just packaged under the new carrier.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {M : Type u_1} -> [MulOneClass M] -> (S : Submonoid M) -> (s : Set M) -> (hs : s = ↑S) -> Submonoid M
<!-- PINNED-SIGNATURE:END -->


`{M : Type u_1} -> [MulOneClass M] -> (S : Submonoid M) -> (s : Set M) -> (hs : s = ↑S) -> Submonoid M`

The ambient type `M` is a type equipped with a multiplicative monoid structure (one and multiplication). `S` is the original submonoid being copied. `s` is the replacement carrier set. `hs` is a proof that `s` equals the coercion of `S` to a plain set, guaranteeing the replacement is valid.

## Conventions

There are no junk-value or edge-case conventions to declare: the function is total and the proof `hs` fully constrains the input, so no degenerate inputs arise.

## Worked examples

- Claim: For any submonoid `S` of a monoid `M`, `VTask.copy S ↑S rfl` has the same carrier as `S`.

- Claim: An element `m : M` belongs to `VTask.copy S s hs` if and only if it belongs to `S`.

- Claim: `VTask.copy S ↑S rfl` equals `S` as a submonoid.

## Boundaries

- The proof argument `hs` must be a proof that `s = ↑S` (coercion of the submonoid to a set). No other set is accepted by the type signature.
- When `s` is literally `↑S` and `hs` is `rfl`, the copy is definitionally the same submonoid.
- The function is total: it is defined for every monoid `M`, every submonoid `S`, every set `s` equal to the carrier of `S`, and every proof of that equality.
- Membership in the copy is equivalent to membership in `S` for every element of `M`.

## Not to be confused with

- `Submonoid.mk`: constructs a submonoid from scratch by providing a carrier and proofs directly, without referencing an existing submonoid.
- Submonoid coercion `↑S : Set M`: the plain set underlying a submonoid, not itself a submonoid.
- Submonoid.map: transports a submonoid along a monoid homomorphism, changing the ambient monoid rather than just renaming the carrier.