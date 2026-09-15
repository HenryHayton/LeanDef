## Object

`VTask.prod f g` is the **pairing** of two equivariant maps with a common source and a common scalar-action twist. Given equivariant maps `f : α →ₑ[σ] γ` and `g : α →ₑ[σ] δ`, it produces the equivariant map `α →ₑ[σ] γ × δ` that sends every element `x : α` to the pair `(f x, g x)`. The resulting map is again equivariant with respect to the same monoid homomorphism `σ`, using the product `SMul` on `γ × δ` (acting componentwise from `N`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {M : Type u_1} -> {N : Type u_2} -> {α : Type u_3} -> {γ : Type u_5} -> {δ : Type u_6} -> [SMul M α] -> [SMul N γ] -> [SMul N δ] -> {σ : M → N} -> (f : α →ₑ[σ] γ) -> (g : α →ₑ[σ] δ) -> α →ₑ[σ] γ × δ
<!-- PINNED-SIGNATURE:END -->


VTask.prod : {M : Type u_1} -> {N : Type u_2} -> {α : Type u_3} -> {γ : Type u_5} -> {δ : Type u_6} -> [SMul M α] -> [SMul N γ] -> [SMul N δ] -> {σ : M → N} -> (f : α →ₑ[σ] γ) -> (g : α →ₑ[σ] δ) -> α →ₑ[σ] γ × δ

`M` is the monoid acting on the source type `α`; `N` is the monoid acting on the two target types `γ` and `δ`. The scalar-action instances `SMul M α`, `SMul N γ`, and `SMul N δ` equip these types with the relevant actions. The monoid homomorphism `σ : M → N` is the twist relating the source and target actions, shared by both input maps. The first argument `f` is the equivariant map into the first component `γ`, and the second argument `g` is the equivariant map into the second component `δ`.

## Conventions

No special junk-value or boundary conventions are declared: the definition is total and well-behaved for all inputs satisfying the stated type-class constraints.

## Worked examples

- Claim: For equivariant maps `f g : α →ₑ[σ] γ`, the underlying function of `VTask.prod f g` evaluated at `x` is `(f x, g x)`.

- Claim: If `f : α →ₑ[σ] γ` and `g : α →ₑ[σ] δ`, then for any `m : M` and `x : α`, `(VTask.prod f g) (m • x) = m • ((VTask.prod f g) x)` in `γ × δ` (where the product is acted on componentwise via `σ m`).

- Claim: Composing `VTask.prod f g` with the first projection (as a function) recovers `f`; composing with the second projection recovers `g`.

## Boundaries

- When `γ = δ` and `f = g`, the result is the diagonal map `x ↦ (f x, f x)`; this is a valid special case with no degenerate behaviour.
- The construction requires that `N` acts on **both** `γ` and `δ`, since the product `SMul` on `γ × δ` acts componentwise; if the actions were incompatible there would be no valid instance, but the type-class system enforces compatibility automatically.
- The definition is total: it places no restrictions on `σ`, on the types, or on the maps beyond those already expressed in the types of `f` and `g`.

## Not to be confused with

- `MulEquiv.prodComm` or `Equiv.prodComm` — those are about swapping the two components of an already-existing product, not about pairing two maps into a product.
- The cartesian product of two equivariant maps `α →ₑ[σ] γ` and `β →ₑ[σ'] δ` with **different** source types — `VTask.prod` requires a **shared** source `α` and a **shared** twist `σ`.
- `LinearMap.prod` in linear algebra — the analogous construction for linear maps; `VTask.prod` is its equivariant-map analogue, but requires only `SMul` structure, not a full module structure.