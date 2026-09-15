## Object

`VTask.sumArrowHomeomorphProdArrow` is the canonical homeomorphism between the function space `(ι ⊕ ι' → X)` — continuous (in the product/pointwise topology) functions out of a disjoint-sum type — and the product `(ι → X) × (ι' → X)` of two separate function spaces. Concretely, a function `f : ι ⊕ ι' → X` corresponds to the pair `(f ∘ Sum.inl, f ∘ Sum.inr)`, and this correspondence is a homeomorphism: both the map and its inverse are continuous.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumArrowHomeomorphProdArrow : {X : Type u_1} -> [TopologicalSpace X] -> {ι : Type u_7} -> {ι' : Type u_8} -> (ι ⊕ ι' → X) ≃ₜ (ι → X) × (ι' → X)
<!-- PINNED-SIGNATURE:END -->


`{X : Type u_1} -> [TopologicalSpace X] -> {ι : Type u_7} -> {ι' : Type u_8} -> (ι ⊕ ι' → X) ≃ₜ (ι → X) × (ι' → X)`

`X` is the common codomain, equipped with a topology via the instance argument. `ι` is the left index type and `ι'` is the right index type forming the coproduct `ι ⊕ ι'`. All three type arguments are implicit and inferred from context. The homeomorphism itself takes no explicit term-level arguments; it is a proof-carrying structure.

## Conventions

All type arguments (`X`, `ι`, `ι'`) are implicit and inferred from context; no junk-value convention applies since the definition is fully parametric and total.

## Worked examples

- Claim: The underlying equivalence of `VTask.sumArrowHomeomorphProdArrow` agrees with `Equiv.sumArrowEquivProdArrow`: for `f : Bool ⊕ Unit → ℝ`, applying the homeomorphism gives the pair `(f ∘ Sum.inl, f ∘ Sum.inr)`.

- Claim: `VTask.sumArrowHomeomorphProdArrow` is a homeomorphism (i.e., it is continuous and its inverse is continuous), so composing it with its inverse yields the identity on `(ι ⊕ ι' → X)`.

- Claim: For the special case `ι = Fin 2`, `ι' = Fin 3`, `X = ℝ`, the homeomorphism maps a function `f : Fin 2 ⊕ Fin 3 → ℝ` to the pair `(fun i => f (Sum.inl i), fun j => f (Sum.inr j))`.

- Claim: The inverse of `VTask.sumArrowHomeomorphProdArrow` maps a pair `(g, h)` with `g : ι → X` and `h : ι' → X` to the function `Sum.elim g h : ι ⊕ ι' → X`.

## Boundaries

- When `ι` or `ι'` is empty (`Empty` or `PEmpty`), the homeomorphism still applies: the corresponding factor in the product becomes a one-point space (there is exactly one function from an empty type), and the homeomorphism reduces correctly to projecting onto the non-empty factor.
- When both `ι` and `ι'` are empty, both factors are singletons and the homeomorphism is a homeomorphism between two one-point spaces.
- When `X` is given the discrete or indiscrete topology, continuity is trivially satisfied, but the homeomorphism still holds in all cases.
- The function spaces carry the product (pointwise) topology, as is standard for `ι → X` in Mathlib when `ι` is a type with no additional structure.

## Not to be confused with

- `Equiv.sumArrowEquivProdArrow`: the underlying set-theoretic equivalence without any topology or continuity data; `VTask.sumArrowHomeomorphProdArrow` strictly extends it.
- `Homeomorph.prodArrowHomeomorphArrowProd`: a homeomorphism involving products of arrow types in a different arrangement (currying/uncurrying over a product domain rather than a sum domain).
- `ContinuousMap.sumArrow`: a related construction for `ContinuousMap` (bundled continuous maps) rather than bare function types with the pointwise topology.