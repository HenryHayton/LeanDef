## VTask.IsExtensionPair

### Object

Given a first-order language `L` and two `L`-structures `M` and `N`, the predicate `IsExtensionPair L M N` asserts that `(M, N)` forms an *extension pair*: for every finitely-generated partial isomorphism from `M` into `N` (a partial bijection whose domain and codomain are finitely-generated substructures), and for every element `m` of `M`, there exists a larger finitely-generated partial isomorphism that still maps `M` to `N` but whose domain now contains `m`. Informally, no element of `M` can ever be left out permanently — the partial map can always be grown to cover any prescribed element of `M`.

This is the key hypothesis in back-and-forth arguments: when both `(M, N)` and `(N, M)` are extension pairs, one can interleave extensions to build a full isomorphism between `M` and `N`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsExtensionPair : (L : FirstOrder.Language) -> (M : Type w) -> (N : Type w') -> [L.Structure M] -> [L.Structure N] -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsExtensionPair : (L : FirstOrder.Language) -> (M : Type w) -> (N : Type w') -> [L.Structure M] -> [L.Structure N] -> Prop`

`L` is the first-order language that both structures interpret. `M` is the *source* structure — the one whose elements must always be absorbable into the domain of any partial map. `N` is the *target* structure — the one into which the partial isomorphisms map. The two bracketed arguments are the `L`-structure instances on `M` and `N` respectively, carrying the interpretations of the language symbols; they are inferred automatically by Lean's typeclass system.

### Conventions

The ordering of the pair is asymmetric: `IsExtensionPair L M N` only guarantees that domains (in `M`) can be extended, not codomains (in `N`). To also extend codomains one needs the separate statement `IsExtensionPair L N M`. There is an equivalent reformulation in terms of codomains (`isExtensionPair_iff_cod`), but the *definition* is stated domain-first. No junk-value conventions apply because the predicate is a `Prop` and is genuinely meaningful for all inputs.

### Worked examples

- Claim: If `M` is any linear order satisfying the linear-order theory and `N` is a dense linear order without endpoints (DLO) that is nonempty, then `VTask.IsExtensionPair Language.order M N`.

- Claim: For a countably-generated ultrahomogeneous `L`-structure `M`, `VTask.IsExtensionPair L M M` holds — every finitely-generated partial automorphism of `M` can be extended to cover any prescribed element.

- Claim: If `M` is a countably-generated `L`-structure and both `VTask.IsExtensionPair L M N` and `VTask.IsExtensionPair L N M` hold, then for any finitely-generated partial isomorphism `g : L.FGEquiv M N` there exists a full `L`-isomorphism `f : M ≃[L] N` extending `g`.

### Boundaries

- When `M` is empty (no elements), the universal quantification over `m : M` is vacuously true, so `IsExtensionPair L M N` holds for any non-empty `N` and any empty `M`.
- When `N` is a single-element structure, extension may be impossible unless `M` is also a single-element structure; the predicate can fail.
- The predicate does not require `M` or `N` to be countable or countably-generated; however, the main consequence theorems (constructing global isomorphisms or embeddings) typically add a countable-generation hypothesis on top.
- The predicate is not symmetric: `IsExtensionPair L M N` and `IsExtensionPair L N M` are independent conditions, and both are needed for the back-and-forth isomorphism theorem.

### Not to be confused with

- `L.IsUltrahomogeneous M`: the self-referential case `IsExtensionPair L M M`; ultrahomogeneity is equivalent to the extension pair condition with both arguments equal (for countably-generated `M`).
- `L.FGEquiv M N`: the *type* of individual finitely-generated partial isomorphisms from `M` to `N`; `IsExtensionPair` is a *property of the pair of structures* about all such maps simultaneously.
- Saturation or universality of a model: those are different (and generally stronger) extension properties involving realizing types rather than extending specific finite partial maps.
