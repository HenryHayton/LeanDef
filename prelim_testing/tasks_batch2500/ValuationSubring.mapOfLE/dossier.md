## VTask.mapOfLE

### Object

Given a field `K` and two valuation subrings `R ≤ S` of `K` (so `R` is a *coarsening* of `S`, meaning `S` sits inside `R` as a valuation ring, or equivalently `R` refines the valuation of `S`), this is the canonical monoid-with-zero homomorphism from the value group of `R` to the value group of `S` induced by the inclusion. Concretely, every element of the value group of `R` is an equivalence class of units of `K` modulo the unit group of `R`; the map sends such a class to the corresponding class in the value group of `S`, which is well-defined because the unit group of `R` maps into the unit group of `S` under the ring inclusion.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapOfLE : {K : Type u} -> [Field K] -> (R S : ValuationSubring K) -> (h : R ≤ S) -> R.ValueGroup →*₀ S.ValueGroup
<!-- PINNED-SIGNATURE:END -->


`VTask.mapOfLE : {K : Type u} -> [Field K] -> (R S : ValuationSubring K) -> (h : R ≤ S) -> R.ValueGroup →*₀ S.ValueGroup`

The implicit type `K` is the ambient field. The `Field K` instance supplies the field structure. `R` and `S` are valuation subrings of `K`. The argument `h` is a proof that `R ≤ S` (as subrings, i.e., `R` is contained in `S`), which is the coarsening hypothesis that makes the map well-defined. The result is a monoid-with-zero homomorphism from the value group of `R` to the value group of `S`.

### Conventions

No special junk-value or out-of-domain conventions are declared: the map is defined for all valuation subrings `R ≤ S` of any field `K`, and the monoid-with-zero structure (sending zero/one to zero/one and respecting multiplication) is baked into the return type.

### Worked examples

- Claim: When `R = S`, the map `VTask.mapOfLE R S (le_refl R)` sends a value-group element of `R` to the "same" element viewed in `S.ValueGroup`.

- Claim: The map `VTask.mapOfLE R S h` preserves the multiplicative identity: it sends `1 : R.ValueGroup` to `1 : S.ValueGroup`.

- Claim: For any `x y : R.ValueGroup`, `VTask.mapOfLE R S h (x * y) = VTask.mapOfLE R S h x * VTask.mapOfLE R S h y`.

- Claim: The map `VTask.mapOfLE R S h` sends `0 : R.ValueGroup` to `0 : S.ValueGroup`.

### Boundaries

- When `R = S`, the map is the identity on value groups (up to definitional equality on quotient types).
- The map is well-defined on equivalence classes: two units of `K` that are equivalent modulo the unit group of `R` map to equivalent elements modulo the unit group of `S`, because the unit group of `R` injects into that of `S` via `h`.
- The zero element of the value group (representing the zero of `K`) is preserved.
- This map is not in general an isomorphism: when `R` is strictly contained in `S` (i.e., `R < S`), the value group of `S` is a proper quotient of the value group of `R`, and the map has a nontrivial kernel.

### Not to be confused with

- `ValuationSubring.inclusion`: the ring homomorphism `R →+* S` between the subrings themselves, not the induced map on value groups.
- The map going in the opposite direction (from `S.ValueGroup` to `R.ValueGroup`): because `S.ValueGroup` is a quotient of `R.ValueGroup` when `R ≤ S`, a map in the reverse direction would be an embedding, not a quotient map.
- `ValuationSubring.ValueGroup`: the value group object itself (the quotient of the nonzero elements of `K` by the unit group of the valuation subring), which is the *domain* and *codomain* of the present map rather than the map itself.
