## Object

Given a pair of complementary embeddings of complex shapes `c₁` and `c₂` into a common complex shape `c`, and a family of objects `X` indexed over the index type of `c`, `VTask.desc'` assembles a section of `X` over the combined index set `ι₁ ⊕ ι₂` from two partial sections — one over `ι₁` and one over `ι₂` — by routing each index to the appropriate partial section via case analysis. The result at each index `i : ι₁ ⊕ ι₂` lives in `X` evaluated at the image of `i` under the canonical equivalence provided by the complementarity datum.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.desc' : {ι : Type u_1} -> {ι₁ : Type u_2} -> {ι₂ : Type u_3} -> {c : ComplexShape ι} -> {c₁ : ComplexShape ι₁} -> {c₂ : ComplexShape ι₂} -> {e₁ : c₁.Embedding c} -> {e₂ : c₂.Embedding c} -> (ac : e₁.AreComplementary e₂) -> {X : ι → Type u_5} -> (x₁ : (i₁ : ι₁) → X (e₁.f i₁)) -> (x₂ : (i₂ : ι₂) → X (e₂.f i₂)) -> (i : ι₁ ⊕ ι₂) -> X (ac.equiv i)
<!-- PINNED-SIGNATURE:END -->


`{ι : Type u_1} -> {ι₁ : Type u_2} -> {ι₂ : Type u_3} -> {c : ComplexShape ι} -> {c₁ : ComplexShape ι₁} -> {c₂ : ComplexShape ι₂} -> {e₁ : c₁.Embedding c} -> {e₂ : c₂.Embedding c} -> (ac : e₁.AreComplementary e₂) -> {X : ι → Type u_5} -> (x₁ : (i₁ : ι₁) → X (e₁.f i₁)) -> (x₂ : (i₂ : ι₂) → X (e₂.f i₂)) -> (i : ι₁ ⊕ ι₂) -> X (ac.equiv i)`

The implicit arguments `ι`, `ι₁`, `ι₂` are the index types of the three complex shapes involved. The implicit arguments `c`, `c₁`, `c₂` are the complex shapes themselves, with `c` being the ambient shape and `c₁`, `c₂` the two sub-shapes. The implicit arguments `e₁`, `e₂` are embeddings of `c₁` and `c₂` respectively into `c`. The explicit argument `ac` is the proof that these two embeddings are complementary, meaning together they cover all of `c` without overlap; it also carries the canonical equivalence `ac.equiv : ι₁ ⊕ ι₂ ≃ ι` between the disjoint union of sub-indices and the ambient index type. The implicit argument `X` is a type-valued family indexed over `ι`, representing the data type at each position. The argument `x₁` is a section of `X` over the image of `e₁`, i.e., a choice of an element of `X (e₁.f i₁)` for each `i₁ : ι₁`. The argument `x₂` is a section of `X` over the image of `e₂`, i.e., a choice of an element of `X (e₂.f i₂)` for each `i₂ : ι₂`. The argument `i` is the combined index in `ι₁ ⊕ ι₂` at which the assembled section is evaluated.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total function defined by exhaustive pattern matching on the two constructors of the sum type, and every input combination yields a well-typed result.

## Worked examples

- Claim: When `i = Sum.inl i₁`, `VTask.desc' ac x₁ x₂ (Sum.inl i₁)` equals `x₁ i₁` (up to the identification given by `ac.equiv`).

- Claim: When `i = Sum.inr i₂`, `VTask.desc' ac x₁ x₂ (Sum.inr i₂)` equals `x₂ i₂` (up to the identification given by `ac.equiv`).

## Boundaries

- The function is defined for every element of `ι₁ ⊕ ι₂` with no gaps: the two constructors `Sum.inl` and `Sum.inr` are exhaustive, so every index is handled.
- The complementarity condition `ac` ensures that the two embeddings jointly cover all of `c` and are disjoint, making the assembled section globally consistent over `c` (when viewed via `ac.equiv`). Without complementarity the typing of the output — involving `ac.equiv` — would not typecheck.
- The definition makes no assumption about the specific objects in `X`; it works for any type family, including propositions or structures.

## Not to be confused with

- `ComplexShape.Embedding.AreComplementary.desc`: the higher-level version of this construction that operates on cochain complexes (or homological complexes) rather than bare type families; `VTask.desc'` is the auxiliary underlying piece.
- `ComplexShape.Embedding.AreComplementary.equiv`: the equivalence `ι₁ ⊕ ι₂ ≃ ι` itself, which is just an index-level map; `VTask.desc'` uses this equivalence to type its output but additionally selects data from `x₁` or `x₂`.
- `Sum.elim`: the generic eliminator for sum types into a common codomain; `VTask.desc'` is analogous but the codomain type `X (ac.equiv i)` depends on the index, requiring dependent elimination rather than simple `Sum.elim`.