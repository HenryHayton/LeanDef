## VTask.FG

### Object

An intermediate field `S` between fields `F` and `E` is called **finitely generated** (over `F`) if there exists a finite set of elements of `E` whose adjunction to `F` recovers `S` exactly. In other words, `S` is finitely generated when it can be written as `F` adjoined with some finite collection of elements `t₁, t₂, …, tₙ ∈ E`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.FG : {F : Type u_1} -> [Field F] -> {E : Type u_2} -> [Field E] -> [Algebra F E] -> (S : IntermediateField F E) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.FG : {F : Type u_1} -> [Field F] -> {E : Type u_2} -> [Field E] -> [Algebra F E] -> (S : IntermediateField F E) -> Prop
```

The implicit type argument `F` is the base field of the extension. The implicit type argument `E` is the ambient (top) field. The `Field` instances give both `F` and `E` their field structure. The `Algebra F E` instance specifies how `F` sits inside `E` and makes `E` an `F`-algebra. The explicit argument `S` is the intermediate field — a subfield of `E` containing (the image of) `F` — whose finite-generatedness over `F` is being asserted.

### Conventions

There are no junk-value or boundary conventions specific to this predicate beyond what the definitions of intermediate fields and adjunction already fix. The notion is genuinely a predicate on intermediate fields with no special treatment of degenerate cases.

### Worked examples

- Claim: The bottom intermediate field `⊥ : IntermediateField F E` (which equals `F` itself embedded in `E`) satisfies `VTask.FG`, since it equals the adjunction of the empty finset.

- Claim: The adjunction of any finite set of elements of `E` over `F` satisfies `VTask.FG`; concretely, for any `t : Finset E`, the intermediate field `IntermediateField.adjoin F ↑t` satisfies `VTask.FG`.

- Claim: If `S` and `T` are both finitely generated intermediate fields over `F`, then their join `S ⊔ T` is also finitely generated.

- Claim: If the extension `E/F` is Noetherian (i.e., `IsNoetherian F E` holds), then every intermediate field `S : IntermediateField F E` satisfies `VTask.FG`.

- Claim: The top intermediate field `⊤ : IntermediateField F E` satisfies `VTask.FG` if and only if `E` is essentially of finite type over `F` (i.e., `Algebra.EssFiniteType F E` holds).

### Boundaries

- The bottom field `⊥` is always finitely generated (witnessed by the empty finset), so the predicate is never vacuously false at the simplest case.
- The top field `⊤` is finitely generated precisely when the whole extension `E/F` is finitely generated; this is the link to `Algebra.EssFiniteType F E`.
- A finite supremum of finitely generated intermediate fields is again finitely generated.
- If the extension is Noetherian, every intermediate field is automatically finitely generated.
- Finite generation is preserved under restriction of scalars in appropriate tower situations.
- The predicate is equivalent to the existence of a *finite set* (not just finset) `t ⊆ E` such that `adjoin F t = S`; the two formulations agree.

### Not to be confused with

- `Algebra.EssFiniteType F E`: this is the preferred way to say the whole extension `E/F` is finitely generated; it coincides with `VTask.FG` on `⊤ : IntermediateField F E` but lives at a different level of abstraction.
- `Subalgebra.FG`: finite generation for subalgebras (over a commutative ring), not for intermediate fields; they are related but not the same predicate.
- `Field.FG`: finite generation of a field as an extension of its prime subfield, a global notion not tied to a specific ambient extension.