## Object

`VTask.copy` produces a new intermediate field (an intermediate field between `K` and `L`) that is definitionally equal to a given one, but whose underlying carrier set is replaced by a provably equal set. The resulting intermediate field has the same elements, the same field operations, and the same algebraic structure as the original; it exists purely to allow the user to substitute one presentation of the carrier for another in situations where definitional equality matters (e.g., when unifying types in proofs or constructions).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {K : Type u_1} -> {L : Type u_2} -> [Field K] -> [Field L] -> [Algebra K L] -> (S : IntermediateField K L) -> (s : Set L) -> (hs : s = ↑S) -> IntermediateField K L
<!-- PINNED-SIGNATURE:END -->


The type-class arguments `[Field K]`, `[Field L]`, and `[Algebra K L]` supply the ambient algebraic structure: `K` and `L` are fields and `L` is a `K`-algebra, so that intermediate fields between them make sense. The explicit argument `S` is the intermediate field being copied. The argument `s` is a set of elements of `L` that will serve as the carrier of the new intermediate field. The argument `hs` is a proof that `s` equals the underlying carrier set of `S`, guaranteeing the two objects represent the same collection of elements.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total construction defined for any intermediate field `S`, any set `s`, and any proof `hs : s = ↑S`, with no distinguished degenerate inputs.

## Worked examples

- Claim: For any intermediate field `S`, `VTask.copy S ↑S rfl` has the same carrier as `S`, namely `↑S`.

- Claim: For any intermediate field `S` and any proof `hs : s = ↑S`, an element `x : L` belongs to `VTask.copy S s hs` if and only if it belongs to `S`.

- Claim: For any intermediate field `S`, `VTask.copy S ↑S rfl = S` as intermediate fields.

## Boundaries

- The proof `hs` must be of the form `s = ↑S` (set equality with the coercion of `S` to a set). There is no meaningful degenerate case: if `hs` is `rfl` (when `s` is literally `↑S`), the copy is definitionally the same as the original.
- The construction is entirely conservative: it never adds or removes elements. The copy and the original are propositionally equal as intermediate fields.
- Since `hs` is a proof of a proposition (set equality), it does not affect the mathematical content of the result in any way—only its definitional presentation.

## Not to be confused with

- `IntermediateField.map`: moves an intermediate field along a field homomorphism, genuinely changing which elements belong to it.
- `IntermediateField.comap`: pulls back an intermediate field along a homomorphism, again changing the elements rather than merely re-presenting them.
- Subtype coercion / set-valued coercion of an intermediate field: this just produces the underlying set, not a new intermediate field structure.