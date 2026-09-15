## VTask.restrictScalarsCongr

### Object

Given two ring homomorphisms `f, g : R →+* S` that are equal, `VTask.restrictScalarsCongr e` produces a natural isomorphism between the two restriction-of-scalars functors `ModuleCat.restrictScalars f` and `ModuleCat.restrictScalars g`. Here, restriction of scalars along a ring homomorphism `h : R →+* S` is the functor that takes an `S`-module and views it as an `R`-module by pulling back the scalar action through `h`. When `f = g`, these two functors are not merely isomorphic in some abstract sense but are canonically and naturally isomorphic, with the isomorphism given by the identity map on the underlying abelian group of each module.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restrictScalarsCongr : {R : Type u₁} -> {S : Type u₂} -> [Ring R] -> [Ring S] -> {f g : R →+* S} -> (e : f = g) -> ModuleCat.restrictScalars f ≅ ModuleCat.restrictScalars g
<!-- PINNED-SIGNATURE:END -->


`{R : Type u₁} -> {S : Type u₂} -> [Ring R] -> [Ring S] -> {f g : R →+* S} -> (e : f = g) -> ModuleCat.restrictScalars f ≅ ModuleCat.restrictScalars g`

`R` is the source ring and `S` is the target ring; both are implicit. The `Ring` instances for `R` and `S` supply the ring structure needed for the module categories. The ring homomorphisms `f` and `g` from `R` to `S` are the two maps along which scalars are being restricted; they are implicit. The argument `e` is the proof that `f` and `g` are equal as ring homomorphisms, and it is the sole explicit input whose content drives the construction.

### Conventions

When the equality proof `e` is `rfl` (i.e., `f` and `g` are definitionally the same homomorphism), the resulting natural isomorphism is the identity natural isomorphism on `ModuleCat.restrictScalars f`.

### Worked examples

- Claim: For any ring homomorphism `f : R →+* S` and the trivial proof `rfl : f = f`, `VTask.restrictScalarsCongr rfl` is a natural isomorphism from `ModuleCat.restrictScalars f` to itself.

- Claim: The component of `VTask.restrictScalarsCongr e` at any `S`-module `X` is an isomorphism in `ModuleCat R` whose underlying map is the identity on the underlying additive group of `X`.

- Claim: For rings `R` and `S`, homomorphisms `f g : R →+* S`, and a proof `e : f = g`, the natural isomorphism `VTask.restrictScalarsCongr e` composes with `(VTask.restrictScalarsCongr e).symm` to give the identity natural isomorphism.

### Boundaries

- The definition is total: it is defined for any proof `e : f = g`, including `rfl`. There is no restriction on the types `R`, `S`, or the homomorphisms `f`, `g`.
- When `e : f = g` and `e' : g = h`, composing `VTask.restrictScalarsCongr e` and `VTask.restrictScalarsCongr e'` yields a natural isomorphism from `ModuleCat.restrictScalars f` to `ModuleCat.restrictScalars h`, consistent with what `VTask.restrictScalarsCongr (e.trans e')` would produce.
- The result lives in the category of functors from `ModuleCat S` to `ModuleCat R`, so both the objects and the morphisms of that functor category are involved in the naturality statement.
- Since the components are identity maps on underlying abelian groups, the natural isomorphism is particularly simple: it adds no computational content beyond transporting the scalar action.

### Not to be confused with

- `ModuleCat.restrictScalars` itself — that is the functor being compared, not the isomorphism between two instances of it.
- A natural isomorphism arising from a ring isomorphism between `R` and `S` — here both homomorphisms go from the same `R` to the same `S` and the isomorphism is between two copies of the restriction functor for the same target, not between categories of modules over different rings.
- `NatIso.ofComponents` — that is a general tool for building natural isomorphisms component-wise, not specific to restriction of scalars.