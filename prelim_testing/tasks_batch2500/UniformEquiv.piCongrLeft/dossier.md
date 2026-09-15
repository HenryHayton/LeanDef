## VTask.piCongrLeft

### Object

Given a bijection `e : ι ≃ ι'` between two index types and a family of uniform spaces `β` indexed by `ι'`, `VTask.piCongrLeft e` is the **uniform isomorphism** (a bijection that is uniformly continuous in both directions) between the reindexed product `(i : ι) → β (e i)` and the original product `(j : ι') → β j`. Concretely, it simply reindexes a dependent function through `e`: a function `f` defined on `ι` (with values `f i : β (e i)`) is sent to the function on `ι'` whose value at `j` is `f (e⁻¹ j)`. This is the uniform-space analogue of the purely set-theoretic reindexing isomorphism for pi types.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piCongrLeft : {ι : Type u_4} -> {ι' : Type u_5} -> {β : ι' → Type u_6} -> [(j : ι') → UniformSpace (β j)] -> (e : ι ≃ ι') -> ((i : ι) → β (e i)) ≃ᵤ ((j : ι') → β j)
<!-- PINNED-SIGNATURE:END -->


`VTask.piCongrLeft : {ι : Type u_4} -> {ι' : Type u_5} -> {β : ι' → Type u_6} -> [(j : ι') → UniformSpace (β j)] -> (e : ι ≃ ι') -> ((i : ι) → β (e i)) ≃ᵤ ((j : ι') → β j)`

- `ι` is the source index type (implicit).
- `ι'` is the target index type (implicit).
- `β` is the family of types indexed by `ι'`, each equipped with a uniform space structure (provided by the instance argument `[(j : ι') → UniformSpace (β j)]`).
- `e` is the explicit bijection `ι ≃ ι'` used to reindex the product; it is the essential datum that determines the isomorphism.

The result is a uniform isomorphism `≃ᵤ` between the reindexed pi type `(i : ι) → β (e i)` and the original pi type `(j : ι') → β j`.

### Conventions

No junk-value conventions are declared: the definition is total and well-defined for every equivalence `e` and every uniformly-spaced family `β`; there are no edge inputs that require a conventional junk output.

### Worked examples

- Claim: When `e` is the identity equivalence `Equiv.refl ι`, `VTask.piCongrLeft (Equiv.refl ι)` equals the identity uniform isomorphism on `(i : ι) → β i`.

- Claim: The forward map of `VTask.piCongrLeft e` satisfies `(VTask.piCongrLeft e x) (e i) = x i` for every `x : (i : ι) → β (e i)` and every `i : ι`. (This follows directly from how reindexing works: applying the reindexed function at `e i` recovers the original value at `i`.)

- Claim: The inverse map of `VTask.piCongrLeft e` acts by precomposition with `e`: `(VTask.piCongrLeft e).symm g = fun i => g (e i)` for `g : (j : ι') → β j`.

- Claim: For any two composable equivalences `e₁ : ι ≃ ι'` and `e₂ : ι' ≃ ι''`, the isomorphism `VTask.piCongrLeft (e₁.trans e₂)` is the composition of `VTask.piCongrLeft e₁` followed by `VTask.piCongrLeft e₂` (transitivity/functoriality of the construction).

### Boundaries

- **Identity equivalence**: When `e = Equiv.refl ι`, the isomorphism reduces to the identity uniform equivalence on `(i : ι) → β i`.
- **Inverse**: The inverse uniform isomorphism `(VTask.piCongrLeft e).symm` is `VTask.piCongrLeft e⁻¹` (up to definitional equality), and its underlying function is simply precomposition with `e`.
- **Single-element index**: When `ι` and `ι'` are both singletons, `VTask.piCongrLeft e` is the unique uniform isomorphism between two isomorphic one-element products.
- **Empty index**: When `ι` and `ι'` are both empty, both sides are the trivial (one-element) uniform space, and the isomorphism is the unique such map.
- The definition places no restriction on the cardinality of `ι` or `ι'`, nor on the specific uniform structures on the fibres.

### Not to be confused with

- `Equiv.piCongrLeft`: the purely set-theoretic (non-uniform) reindexing equivalence between pi types; `VTask.piCongrLeft` upgrades this to a uniform isomorphism.
- `UniformEquiv.piCongrRight`: the uniform isomorphism that replaces the fibre uniform spaces pointwise (fibre-wise isomorphism), rather than reindexing the domain.
- `ContinuousLinearEquiv` or `HomeomorphismOfEquiv` analogues: topological or linear versions of reindexing; `VTask.piCongrLeft` specifically tracks uniform continuity, not just continuity or linearity.