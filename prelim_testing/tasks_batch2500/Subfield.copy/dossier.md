## Object

`VTask.copy` produces a new subfield structure whose underlying carrier set is a given set `s`, where `s` is supplied together with a proof that it equals the carrier of an existing subfield `S`. The resulting subfield is mathematically identical to `S` — it has the same elements and the same field operations — but Lean's type theory treats the carrier definitionally as `s` rather than as `↑S`. This is a bookkeeping device: it lets one replace the carrier of a subfield by a definitionally equal set without changing any mathematical content.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {K : Type u} -> [DivisionRing K] -> (S : Subfield K) -> (s : Set K) -> (hs : s = ↑S) -> Subfield K
<!-- PINNED-SIGNATURE:END -->


`{K : Type u} -> [DivisionRing K] -> (S : Subfield K) -> (s : Set K) -> (hs : s = ↑S) -> Subfield K`

`K` is the ambient division ring (the type in which the subfield lives); the instance `[DivisionRing K]` supplies the ring structure on `K`. `S` is the original subfield being copied. `s` is the new carrier set that will appear definitionally in the output. `hs` is the proof that `s` equals the coercion of `S` to a set, ensuring the two carriers are the same set and that all subfield axioms carry over unchanged.

## Conventions

There are no junk-value or out-of-domain conventions to declare: the function is total and every well-typed input produces a meaningful output (a subfield equal to `S` but with carrier `s`).

## Worked examples

- Claim: For any subfield `S` of a division ring `K`, `VTask.copy S ↑S rfl` has the same carrier as `S`.

- Claim: An element `x : K` belongs to `VTask.copy S s hs` if and only if it belongs to `S`; specifically, `x ∈ VTask.copy S s hs ↔ x ∈ S`.

- Claim: `VTask.copy S s hs` equals `S` as a subfield of `K` (the two are definitionally equal as `Subfield K` when `s = ↑S`).

## Boundaries

- The only admissible value of `hs` is a proof that `s = ↑S`; any such proof yields a subfield whose carrier is `s` and whose membership, operations, and closure properties are identical to those of `S`.
- When `s` is taken to be `↑S` itself and `hs` is `rfl`, the copy is transparently the same structure as `S`.
- The function does not create a genuinely new or distinct subfield; the copy and the original have the same elements, the same zero, one, and inverses.
- Because `K` must be a `DivisionRing`, the construction is not available for more general ring types.

## Not to be confused with

- `Subfield.mk` / direct subfield construction: that builds a subfield from scratch by supplying closure data, whereas `VTask.copy` merely re-labels the carrier of an existing subfield.
- `Subfield.map` or `Subfield.comap`: those produce subfields via ring homomorphisms and may genuinely change the mathematical content; `VTask.copy` never changes the elements.
- `Set.image` applied to a subfield's carrier: a pure set operation with no algebraic structure, unlike `VTask.copy` which preserves all subfield axioms.