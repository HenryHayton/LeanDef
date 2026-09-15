## Object

Given a tower of fields `K ⊆ F ⊆ E ⊆ L`, where `F` and `E` are both intermediate fields of the extension `L / K` and `F ≤ E`, `VTask.extendScalars h` produces `E` viewed as an intermediate field of `L / F` — that is, it re-interprets the same subfield `E` but now regards `F` (rather than `K`) as the base field. Concretely, the underlying subset of `L` is unchanged; only the scalar field is "extended" from `K` to `F`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.extendScalars : {K : Type u_1} -> {L : Type u_2} -> [Field K] -> [Field L] -> [Algebra K L] -> {F E : IntermediateField K L} -> (h : F ≤ E) -> IntermediateField (↥F) L
<!-- PINNED-SIGNATURE:END -->


`{K : Type u_1} -> {L : Type u_2} -> [Field K] -> [Field L] -> [Algebra K L] -> {F E : IntermediateField K L} -> (h : F ≤ E) -> IntermediateField (↥F) L`

The implicit type arguments `K` and `L` are the small (base) and large (ambient) fields of the original extension. The type-class arguments supply the field structures on `K` and `L` together with the `K`-algebra structure on `L`. The implicit arguments `F` and `E` are two intermediate fields of `L / K`. The explicit argument `h` is a proof that `F` is contained in `E` (as intermediate fields, i.e., as subsets of `L`). The result is an intermediate field of `L` over `F` (the subtype `↥F`) whose underlying subfield of `L` is exactly `E`.

## Conventions

No special junk-value or out-of-range conventions are declared for this definition: the construction is total and well-defined whenever `F ≤ E` holds, which is exactly what the proof argument `h` guarantees.

## Worked examples

- Claim: If `F = E` (every field is ≤ itself), then `VTask.extendScalars (le_refl F)` is `F` viewed as an intermediate field of `L / F`, i.e., it corresponds to the top element `⊤` of `IntermediateField (↥F) L`.

- Claim: If `K ⊆ F ⊆ E ⊆ L` is a proper tower, then `VTask.extendScalars h` has the same underlying carrier set in `L` as `E` itself; in particular, an element `x : L` belongs to `VTask.extendScalars h` if and only if `x ∈ E`.

- Claim: `VTask.extendScalars h` is inverse to `IntermediateField.restrictScalars F` in the sense that restricting the scalars of `VTask.extendScalars h` back to `K` recovers `E` as an intermediate field of `L / K`.

## Boundaries

- The definition requires a proof `h : F ≤ E`; if `F = E` the result is an intermediate field of `L / F` that, as a subfield, equals `F` itself (the "trivial" extension).
- If `E = ⊤` (all of `L`), then `VTask.extendScalars h` is the top intermediate field of `L / F`, namely `L` itself viewed as a trivial extension.
- The underlying set of `VTask.extendScalars h` in `L` is the same as the underlying set of `E`; only the base field bookkeeping changes.
- The algebra instance on `↥F` that is required to form `IntermediateField (↥F) L` is provided automatically by the `Algebra K L` instance together with the fact that `↥F` is a subfield of `L`.

## Not to be confused with

- `IntermediateField.restrictScalars`: goes in the opposite direction — given an intermediate field of `L / F` it produces one of `L / K`, so it is the inverse operation to `VTask.extendScalars`.
- `Algebra.extendScalars` / scalar extension of modules: that construction tensors a module over a new ring, producing a genuinely different object, whereas `VTask.extendScalars` keeps the same underlying subfield of `L` and only changes the recorded base field.
- `IntermediateField.lift`: lifts an intermediate field along a morphism of base fields, a different (non-identity-on-underlying-set) operation.