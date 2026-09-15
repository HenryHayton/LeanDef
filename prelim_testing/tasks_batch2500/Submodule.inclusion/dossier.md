## Object

`VTask.inclusion h` is the canonical linear map that embeds a submodule `p` into a larger submodule `p'`, given a proof `h` that `p ≤ p'` (i.e., `p` is contained in `p'`). It sends each element of `p` to the same element, now viewed as an element of `p'`. This is the linear-algebraic counterpart of the set-theoretic inclusion of a subset into a superset.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {R : Type u_1} -> {M : Type u_2} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> {p p' : Submodule R M} -> (h : p ≤ p') -> ↥p →ₗ[R] ↥p'
<!-- PINNED-SIGNATURE:END -->


`VTask.inclusion : {R : Type u_1} -> {M : Type u_2} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> {p p' : Submodule R M} -> (h : p ≤ p') -> ↥p →ₗ[R] ↥p'`

The ambient ring `R` and the ambient module `M` are implicit. The typeclasses require `R` to be a semiring and `M` to be an `R`-module (with the underlying additive commutative monoid structure). The two submodules `p` and `p'` are implicit, inferred from context. The sole explicit argument `h` is the proof that `p ≤ p'`, i.e., that every element of `p` also belongs to `p'`; this proof is what allows the construction of the embedding.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total construction that is well-defined for any proof `h : p ≤ p'`, including the degenerate cases `p = p'` (where it becomes the identity on the subtype) or `p = ⊥` (where it is the unique map from the trivial submodule).

## Worked examples

- Claim: For any element `x : ↥p`, the underlying element of `M` obtained from `VTask.inclusion h x` equals the underlying element of `M` obtained from `x` itself.

- Claim: If `p = p'` and `h : p ≤ p'` is the trivial reflexivity proof, then `VTask.inclusion h` acts as the identity on elements of `↥p` (in the sense that the image element has the same `M`-value as the input).

- Claim: For submodules `p ≤ p' ≤ p''` with proofs `h : p ≤ p'` and `h' : p' ≤ p''`, the composition `VTask.inclusion h' ∘ VTask.inclusion h` sends each `x : ↥p` to the element of `↥p''` with the same underlying `M`-value as `x`.

## Boundaries

- When `p = ⊥` (the zero submodule), `↥p` is a type with a single element (zero), and `VTask.inclusion h` is the unique linear map from this one-element module into `p'`; it sends zero to zero.
- When `p = p'`, the map `VTask.inclusion h` (with `h` the reflexivity proof `le_refl p`) is the identity linear map on `↥p` viewed as a self-map.
- When `p' = ⊤` (the whole module), `VTask.inclusion h` is the map from `↥p` into the full module `↥⊤ ≅ M`, embedding `p` into the entire module; it is always injective.
- The map is always injective, since distinct elements of `p` remain distinct in `p'` (the underlying `M`-values do not change).
- The map is a linear map over `R`, so it respects addition and scalar multiplication in the submodule subtypes.

## Not to be confused with

- `Submodule.subtype p`: The linear map `↥p →ₗ[R] M` that embeds a submodule into the full ambient module `M`, rather than into another submodule `p'`.
- `LinearMap.inclusion` for subsets/subtypes in other contexts: inclusion maps exist for other algebraic structures (e.g., subalgebras, subgroups), but `VTask.inclusion` is specifically for submodules and produces a linear map.
- The coercion `↥p → ↥p'` as plain functions: while the underlying function of `VTask.inclusion h` is just the inclusion of types, `VTask.inclusion h` additionally carries the proof that this map is `R`-linear.