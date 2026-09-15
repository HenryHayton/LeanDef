## Object

`VTask.prod f g` is the linear map from a module `M` to the product module `M₂ × M₃` that sends every element `x : M` to the pair `(f x, g x)`. It packages two linear maps sharing the same domain into a single linear map whose codomain is the direct product of their respective codomains.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {R : Type u} -> {M : Type v} -> {M₂ : Type w} -> {M₃ : Type y} -> [Semiring R] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> [Module R M] -> [Module R M₂] -> [Module R M₃] -> (f : M →ₗ[R] M₂) -> (g : M →ₗ[R] M₃) -> M →ₗ[R] M₂ × M₃
<!-- PINNED-SIGNATURE:END -->


`VTask.prod : {R : Type u} -> {M : Type v} -> {M₂ : Type w} -> {M₃ : Type y} -> [Semiring R] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> [Module R M] -> [Module R M₂] -> [Module R M₃] -> (f : M →ₗ[R] M₂) -> (g : M →ₗ[R] M₃) -> M →ₗ[R] M₂ × M₃`

The scalar ring `R` and the three module types `M`, `M₂`, `M₃` are implicit, inferred from the two explicit arguments. The first explicit argument `f` is a linear map from `M` to `M₂`; its values become the first component of the output pair. The second explicit argument `g` is a linear map from `M` to `M₃`; its values become the second component of the output pair.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total construction that is well-defined for any two linear maps on the same domain, including zero maps, identity maps, and maps between trivial modules.

## Worked examples

- Claim: Applying `VTask.prod f g` to an element `x` yields `(f x, g x)` — i.e., the first projection recovers `f` and the second recovers `g`.

- Claim: When `R = ℤ`, `M = M₂ = M₃ = ℤ`, `f = LinearMap.id`, and `g` is multiplication by `2`, then `VTask.prod f g` sends `3` to `(3, 6)`.

- Claim: `VTask.prod 0 0` is the zero linear map into `M₂ × M₃`, sending every element to `(0, 0)`.

- Claim: The composition of `VTask.prod f g` with the canonical projection `LinearMap.fst R M₂ M₃` equals `f` (and similarly with `LinearMap.snd` and `g`).

## Boundaries

- If both `f` and `g` are zero maps, `VTask.prod f g` is the zero map into the product, mapping every element to the zero pair `(0, 0)`.
- If `M` is the zero module (trivially), `VTask.prod f g` is the unique linear map from the zero module to `M₂ × M₃`.
- Linearity is preserved over the full domain: the result correctly satisfies `map_add` and `map_smul` with no restrictions on the ring or modules.
- The construction works for any semiring `R` (not just rings or fields), so it applies in the setting of `ℕ`-modules as well.

## Not to be confused with

- `LinearMap.coprod`: takes two linear maps with *different* domains and a *shared* codomain, producing a map out of a direct sum — the dual construction.
- `LinearMap.fst` / `LinearMap.snd`: the projection maps *out* of a product module, which are the canonical left and right inverses of `VTask.prod f g` up to composition.
- `Prod.map` on functions: the function-level pairing that maps `(x, y)` to `(f x, g y)`, which has a *product* domain rather than a shared domain.