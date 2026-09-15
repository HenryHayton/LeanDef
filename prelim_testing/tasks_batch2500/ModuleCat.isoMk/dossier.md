## VTask.isoMk

### Object

`VTask.isoMk` constructs an isomorphism between two objects `M` and `N` in the category of `R`-modules (`ModuleCat R`) from two pieces of data: an isomorphism between their underlying abelian groups (an isomorphism in the category `Ab` of abelian groups), together with a proof that this isomorphism is compatible with the scalar multiplication actions of `R` on both modules. In other words, it packages an additive group isomorphism that also respects the `R`-module structure into a full-fledged isomorphism of `R`-modules.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.isoMk : {R : Type u} -> [Ring R] -> {M N : ModuleCat R} -> (φ : (CategoryTheory.forget₂ (ModuleCat R) Ab).obj M ≅ (CategoryTheory.forget₂ (ModuleCat R) Ab).obj N) -> (hφ :
    ∀ (r : R),
      CategoryTheory.CategoryStruct.comp φ.hom (N.smul r) = CategoryTheory.CategoryStruct.comp (M.smul r) φ.hom) -> M ≅ N
<!-- PINNED-SIGNATURE:END -->


`(φ : (CategoryTheory.forget₂ (ModuleCat R) Ab).obj M ≅ (CategoryTheory.forget₂ (ModuleCat R) Ab).obj N) -> (hφ : ∀ (r : R), CategoryTheory.CategoryStruct.comp φ.hom (N.smul r) = CategoryTheory.CategoryStruct.comp (M.smul r) φ.hom) -> M ≅ N`

The implicit argument `R` is a ring, and `M`, `N` are objects of the category `ModuleCat R` (i.e., `R`-modules). The first explicit argument `φ` is an isomorphism in the category `Ab` between the abelian groups underlying `M` and `N`; concretely, `φ.hom` is an additive group isomorphism from the underlying group of `M` to that of `N`. The second explicit argument `hφ` is a compatibility condition asserting that for every ring element `r : R`, the forward map `φ.hom` intertwines the scalar-multiplication-by-`r` endomorphisms of `M` and `N`: first applying scalar multiplication by `r` on `M` and then `φ.hom` gives the same result as first applying `φ.hom` and then scalar multiplication by `r` on `N`.

### Conventions

No junk-value or edge-case conventions are declared for this constructor: it is a total function on well-formed inputs, and the output isomorphism is fully determined by the supplied abelian-group isomorphism and compatibility proof.

### Worked examples

- Claim: For any `R`-module `M`, applying `VTask.isoMk` to the identity isomorphism on the underlying abelian group (with the trivial compatibility condition) yields an isomorphism whose forward map `hom` coincides with the identity morphism on `M`.

- Claim: The forward morphism `(VTask.isoMk φ hφ).hom` in `ModuleCat R` is equal to `homMk φ.hom hφ`, i.e., it is precisely the `R`-linear map whose underlying additive group map is `φ.hom`.

- Claim: The inverse morphism `(VTask.isoMk φ hφ).inv` in `ModuleCat R` is the `R`-linear map built from the inverse `φ.inv` of the underlying abelian-group isomorphism, equipped with the naturality condition inherited from the full module isomorphism.

- Claim: The symmetric isomorphism `(VTask.isoMk φ hφ).symm` equals `VTask.isoMk φ.symm` (applied with the appropriate compatibility proof), so taking the symmetric isomorphism corresponds to taking the symmetric isomorphism at the level of abelian groups.

### Boundaries

- When `M` and `N` are equal as objects of `ModuleCat R`, one may supply the identity isomorphism on the underlying abelian group; the compatibility condition is then trivially satisfied, and the result is the identity isomorphism on `M`.
- The compatibility condition `hφ` is genuinely required: without it, an arbitrary abelian group isomorphism need not respect scalar multiplication, and the output would not be a valid morphism in `ModuleCat R`.
- The construction is symmetric: the inverse of the resulting module isomorphism is determined entirely by the inverse `φ.inv` of the abelian-group isomorphism, with its own automatically derivable compatibility.
- There is no restriction on the ring `R` beyond it being a ring; in particular `R` need not be commutative.

### Not to be confused with

- `ModuleCat.homMk`: constructs a *morphism* (not an isomorphism) in `ModuleCat R` from an underlying abelian-group morphism; `VTask.isoMk` requires and produces the stronger notion of isomorphism.
- `LinearEquiv.toModuleIso`: converts a `LinearEquiv` (an explicit `R`-linear bijection in the algebraic sense) directly to an isomorphism in `ModuleCat R`; `VTask.isoMk` instead works at the categorical level, starting from an isomorphism in `Ab`.
- `CategoryTheory.Iso.mk`: the generic category-theoretic isomorphism constructor, which requires specifying forward and backward morphisms already in `ModuleCat R` along with the two composition identities, rather than lifting from `Ab`.
