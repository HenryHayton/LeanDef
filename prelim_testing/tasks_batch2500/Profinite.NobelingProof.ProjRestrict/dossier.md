## VTask.ProjRestrict

### Object

Given a set `C` of Boolean-valued functions on an index type `I`, and a predicate `J` on `I`, the **projection** map `π C J` is the image of `C` under the coordinate-restriction map that sends each function `f : I → Bool` to its restriction `f|_J`, i.e., to the function `I → Bool` that agrees with `f` on indices satisfying `J` (and is determined by `J`). `VTask.ProjRestrict` is the canonical map that takes an element of `C` and returns the corresponding element of `π C J`, viewed as a member of the subtype `↑(π C J)`. In other words, it is the corestriction of the coordinate-projection to its image: the same underlying function as the projection, but packaged with the proof that its output lands in `π C J`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ProjRestrict : {I : Type u} -> (C : Set (I → Bool)) -> (J : I → Prop) -> [(i : I) → Decidable (J i)] -> ↑C → ↑(Profinite.NobelingProof.π C J)
<!-- PINNED-SIGNATURE:END -->


`VTask.ProjRestrict : {I : Type u} -> (C : Set (I → Bool)) -> (J : I → Prop) -> [(i : I) → Decidable (J i)] -> ↑C → ↑(Profinite.NobelingProof.π C J)`

- `I` is the index type whose elements label the Boolean coordinates.
- `C` is the ambient subset of `I → Bool` whose elements are the functions being projected.
- `J` is the predicate on `I` that specifies which coordinates are retained by the projection.
- The instance argument `[(i : I) → Decidable (J i)]` provides decidability of the predicate `J`, needed to compute the restricted coordinates effectively.
- The final argument is an element of `C` (a function `I → Bool` together with its membership proof), and the result is its image under the coordinate projection, packaged as an element of `↑(π C J)`.

### Conventions

There are no junk-value or edge-case conventions to declare: the map is total on its stated domain `↑C` and every input produces a well-typed output in `↑(π C J)` by construction.

### Worked examples

- Claim: For any element `x : ↑C`, the underlying value of `VTask.ProjRestrict C J x` equals `Profinite.NobelingProof.Proj J x.val`, i.e., the image of `x` under the coordinate projection.

- Claim: `VTask.ProjRestrict C J` is surjective: every element of `↑(π C J)` is in the image of this map, since `π C J` is by definition the image of `C` under `Proj J`.

- Claim: If `C` contains a single function `f : I → Bool` and `J` is the always-true predicate, then `VTask.ProjRestrict C J ⟨f, hf⟩` is the element of `↑(π C J)` corresponding to `f` itself.

- Claim: If `J` is the always-false predicate (no coordinates retained), then every element of `C` maps to the same element of `π C J` under `VTask.ProjRestrict C J`, namely the unique constant function in the image.

### Boundaries

- When `C` is empty, `VTask.ProjRestrict C J` is vacuously defined (it is a function on an empty type) and no outputs are produced.
- When `J` holds for all `i : I`, the projection retains all coordinates, so `VTask.ProjRestrict C J` acts as an inclusion (the image `π C J` is isomorphic to `C` itself).
- When `J` holds for no `i : I`, all elements of `C` collapse to the same output; if `C` is nonempty, `π C J` is a singleton.
- The decidability instance is required for the map to be computable; without it the map can still be stated but cannot be reduced.

### Not to be confused with

- `Profinite.NobelingProof.Proj J` — the underlying projection map `(I → Bool) → (I → Bool)` defined on all of `I → Bool`, not restricted to `C` or corestricted to the image.
- `Set.MapsTo.restrict` — the general Mathlib combinator that corestricts a map with a `MapsTo` proof; `VTask.ProjRestrict` is a specific instance of this applied to the Nobeling projection setting.
- `Profinite.NobelingProof.π C J` — the **set** (the image of `C` under `Proj J`), as opposed to the **map** `VTask.ProjRestrict C J` that goes into it.
