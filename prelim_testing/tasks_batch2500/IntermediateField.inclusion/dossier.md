## Object

`VTask.inclusion` is the canonical inclusion map from an intermediate field `E` into a larger intermediate field `F`, whenever `E` is contained in `F` (both sitting between a base field `K` and an ambient field `L`). It is a `K`-algebra homomorphism — that is, a ring homomorphism that also respects the `K`-linear structure — and it sends each element of `E` to the "same" element viewed as a member of `F`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {K : Type u_1} -> {L : Type u_2} -> [Field K] -> [Field L] -> [Algebra K L] -> {E F : IntermediateField K L} -> (hEF : E ≤ F) -> ↥E →ₐ[K] ↥F
<!-- PINNED-SIGNATURE:END -->


`VTask.inclusion : {K : Type u_1} -> {L : Type u_2} -> [Field K] -> [Field L] -> [Algebra K L] -> {E F : IntermediateField K L} -> (hEF : E ≤ F) -> ↥E →ₐ[K] ↥F`

`K` is the base field and `L` is the ambient field; both are implicit type arguments with their field structures inferred automatically. The `Algebra K L` instance records how `K` sits inside `L`. `E` and `F` are both intermediate fields between `K` and `L`, also inferred implicitly from context. The sole explicit argument `hEF` is the proof that `E` is a sub-intermediate-field of `F` (i.e., `E ≤ F` as sets of elements of `L`). The output is a `K`-algebra homomorphism from the type of elements of `E` to the type of elements of `F`.

## Conventions

No junk-value or edge conventions are declared: the map is well-defined and meaningful for any proof `hEF : E ≤ F`, including the trivial cases `E = F` (in which case the map is the identity on elements) and `E = ⊥` (in which case the map embeds the base-field copy into `F`).

## Worked examples

- Claim: For any intermediate fields `E ≤ F` over `K` in `L`, the inclusion map sends an element `x : E` to an element of `F` whose coercion to `L` equals the coercion of `x` to `L`.

- Claim: The inclusion map is a `K`-algebra homomorphism, so in particular it satisfies `VTask.inclusion hEF (x + y) = VTask.inclusion hEF x + VTask.inclusion hEF y` for all `x y : E`.

- Claim: When `E = F` (i.e., the proof of `E ≤ F` comes from `le_refl`), the inclusion map acts as the identity on elements: `(VTask.inclusion (le_refl E) x : F) = x` as elements of `F`.

- Claim: The inclusion map is injective, since it is simply a coercion into a larger type and cannot identify distinct elements of `E`.

## Boundaries

- When `E = F` (proved by reflexivity), the map is well-typed and equals the identity `K`-algebra automorphism on `E` (viewing `E = F`).
- When `E = ⊥`, the smallest intermediate field (isomorphic to `K`), the inclusion embeds the base-field copy into an arbitrary `F`; this is consistent with the general definition.
- When `E = F = ⊤` (the full ambient field `L`), the map is again the identity.
- The map is always injective (as a `K`-algebra homomorphism between fields it must be), but it is not necessarily surjective unless `E = F`.
- The proof `hEF` is a data-carrying proposition (it is a `Prop`), so different proofs of the same containment `E ≤ F` give definitionally equal maps.

## Not to be confused with

- `Subalgebra.inclusion`: the analogous inclusion for sub-algebras rather than intermediate fields; `VTask.inclusion` is specifically the intermediate-field version and produces a `K`-algebra map between intermediate-field types.
- The coercion `↑ : E → L`: this sends an element of `E` directly to `L`, skipping the intermediate `F`; `VTask.inclusion` instead targets `F` and is a structured `K`-algebra homomorphism, not merely a set-theoretic embedding.
- `IntermediateField.lift` or restriction maps: those go in the opposite direction (restricting a map from a larger field to a smaller subfield), whereas `VTask.inclusion` always goes from smaller to larger.
