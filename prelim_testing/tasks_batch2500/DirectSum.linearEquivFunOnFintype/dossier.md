## Object

`VTask.linearEquivFunOnFintype` is the canonical *R*-linear isomorphism between the direct sum ⊕ᵢ Mᵢ (as a `DirectSum`) and the direct product ∏ᵢ Mᵢ (as a dependent function type `∀ i, M i`), valid whenever the index type ι is finite. Because ι is finite, every element of the product has only finitely many nonzero components, so the two constructions coincide and carry the same *R*-module structure; this equivalence makes that coincidence explicit and invertible in a way that respects scalar multiplication and addition.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.linearEquivFunOnFintype : (R : Type u) -> [Semiring R] -> (ι : Type v) -> (M : ι → Type w) -> [(i : ι) → AddCommMonoid (M i)] -> [(i : ι) → Module R (M i)] -> [Fintype ι] -> (DirectSum ι fun i => M i) ≃ₗ[R] (i : ι) → M i
<!-- PINNED-SIGNATURE:END -->


`VTask.linearEquivFunOnFintype : (R : Type u) -> [Semiring R] -> (ι : Type v) -> (M : ι → Type w) -> [(i : ι) → AddCommMonoid (M i)] -> [(i : ι) → Module R (M i)] -> [Fintype ι] -> (DirectSum ι fun i => M i) ≃ₗ[R] (i : ι) → M i`

- `R` is the semiring of scalars over which the module structure is defined.
- The `[Semiring R]` instance supplies the ring/semiring axioms for `R`.
- `ι` is the (finite) index type that parameterises the family of modules.
- `M` is the family of *R*-modules, one for each index in `ι`.
- The `[(i : ι) → AddCommMonoid (M i)]` instance equips each `M i` with its additive commutative monoid structure.
- The `[(i : ι) → Module R (M i)]` instance equips each `M i` with scalar multiplication by `R`.
- The `[Fintype ι]` instance asserts that `ι` has only finitely many elements, which is the essential hypothesis enabling the equivalence.

The result is an `R`-linear equivalence (`≃ₗ[R]`) whose forward direction sends an element of the direct sum to the corresponding dependent function, and whose inverse assembles a dependent function into a finitely-supported direct sum element.

## Conventions

No junk-value or edge conventions are declared: the equivalence is defined for every valid combination of inputs satisfying the stated type-class constraints, and its behaviour is fully determined by those constraints with no special case handling required.

## Worked examples

- Claim: For `R = ℤ`, `ι = Fin 2`, and `M = fun _ => ℤ`, the forward map of `VTask.linearEquivFunOnFintype` sends the direct sum element with value `3` at index `0` and `5` at index `1` to the function `![3, 5]`.

- Claim: `VTask.linearEquivFunOnFintype` is an `R`-linear map in the forward direction, meaning it preserves addition and scalar multiplication.

- Claim: For `R = ℝ`, `ι = Fin 0` (the empty index type), `VTask.linearEquivFunOnFintype` witnesses that the zero direct sum `⨁ i : Fin 0, M i` is linearly equivalent to the trivially-indexed product, both of which are the zero module.

- Claim: For `R = ℚ`, `ι = Unit`, `M = fun _ => ℚ`, the forward map of `VTask.linearEquivFunOnFintype` sends any element `x : ⨁ _ : Unit, ℚ` to the constant function whose single value equals the unique component of `x`.

## Boundaries

- When `ι` is empty (`Fintype ι` with `Fintype.card ι = 0`), both sides reduce to the zero module and the equivalence is the unique linear isomorphism between them.
- When `ι` has exactly one element, the equivalence degenerates to the identity-like isomorphism between `M (default : ι)` viewed as a direct sum and `M (default : ι)` viewed as a function.
- The finiteness hypothesis on `ι` is essential: without it, an element of `∀ i, M i` need not be finitely supported, so no such equivalence can exist in general.
- The equivalence works for any semiring `R`, not just rings or fields, as long as each `M i` is an `R`-module.

## Not to be confused with

- `DirectSum.toAddMonoidHom` / the coercion to `AddMonoidHom`: a mere additive group homomorphism, not the full linear equivalence.
- `DFinsupp.equivFunOnFintype`: the analogous equivalence for `DFinsupp` (finitely-supported dependent functions) rather than for `DirectSum`; `VTask.linearEquivFunOnFintype` is built on top of this but lives in the `DirectSum` world.
- The infinite-index analogue one might imagine: no such *linear equivalence* between `⨁ i, M i` and `∀ i, M i` exists when `ι` is infinite, because elements of the product need not be finitely supported.