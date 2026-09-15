## VTask.equivOfEq

### Object

Given a proof that two intermediate fields `S` and `T` of a field extension `E/F` are equal as intermediate fields, `VTask.equivOfEq` produces a canonical algebra isomorphism (an `F`-algebra equivalence) from `S` to `T`. This is the "transport" or "coercion" map that turns a definitional/propositional equality of subfields into a concrete isomorphism of their underlying types, acting as the identity on the elements shared by the two fields.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.equivOfEq : {F : Type u_4} -> [Field F] -> {E : Type u_5} -> [Field E] -> [Algebra F E] -> {S T : IntermediateField F E} -> (h : S = T) -> ↥S ≃ₐ[F] ↥T
<!-- PINNED-SIGNATURE:END -->


`{F : Type u_4} -> [Field F] -> {E : Type u_5} -> [Field E] -> [Algebra F E] -> {S T : IntermediateField F E} -> (h : S = T) -> ↥S ≃ₐ[F] ↥T`

The implicit type `F` is the base field of the extension. The typeclass `[Field F]` asserts that `F` is a field. The implicit type `E` is the total field of the extension. The typeclass `[Field E]` asserts that `E` is a field. The typeclass `[Algebra F E]` equips `E` with the structure of an `F`-algebra, giving the extension `E/F`. The implicit arguments `S` and `T` are the two intermediate fields (between `F` and `E`) being compared. The explicit argument `h` is the proof that `S` and `T` are equal as intermediate fields. The result is an `F`-algebra isomorphism from the type `↥S` (elements of `S`) to the type `↥T` (elements of `T`).

### Conventions

When `h` is `rfl` (i.e., `S = T` by reflexivity, so `S` and `T` are definitionally the same intermediate field), the resulting isomorphism acts as the identity map on elements.

### Worked examples

- Claim: For any intermediate field `S`, `VTask.equivOfEq (rfl : S = S)` maps every element `x : ↥S` to itself (i.e., the isomorphism is the identity at `rfl`).

- Claim: If `h : S = T` is a proof of equality of two intermediate fields `S` and `T` of `E/F`, then the underlying map of `VTask.equivOfEq h` sends an element `x : ↥S` to the element of `↥T` obtained by transporting `x` along `h`; in particular, the image in `E` of `(VTask.equivOfEq h) x` equals the image in `E` of `x`.

- Claim: The inverse of `VTask.equivOfEq h` is `VTask.equivOfEq h.symm`, meaning composing them yields the identity.

### Boundaries

- The definition is total: it is defined for any proof `h : S = T`, including `rfl`.
- When `h = rfl`, the isomorphism is the identity `AlgEquiv`.
- Since the map is built from an equality, it preserves all algebraic structure: addition, multiplication, the `F`-scalar action, and the embedding into `E`.
- The coercion of any element `(VTask.equivOfEq h x : E)` equals `(x : E)`; the isomorphism does not move elements in the ambient field `E`.

### Not to be confused with

- `AlgEquiv.refl`: the reflexivity algebra isomorphism `S ≃ₐ[F] S`; this is the special case of `VTask.equivOfEq` at `h = rfl`, but `AlgEquiv.refl` is stated directly without going through an equality proof.
- `IntermediateField.lift`: maps that embed one intermediate field into another via inclusion, which do not require an equality and do not produce an isomorphism in general.
- `Subalgebra.equivOfEq`: the analogous construction for subalgebras rather than intermediate fields; `VTask.equivOfEq` is built on top of this but works specifically in the intermediate field setting.
