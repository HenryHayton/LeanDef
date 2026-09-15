## Object

Given a commutative semiring `R`, an `R`-module `M`, a type `α`, and a family `S` of `R`-submodules of `M` indexed by `α`, `VTask.submodule S` is the `R`-submodule of the finitely-supported functions `α →₀ M` consisting of all `f : α →₀ M` such that `f i ∈ S i` for every `i : α`. In other words, it is the submodule of finitely-supported functions that respect the given pointwise submodule constraints.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.submodule : {R : Type u_1} -> {M : Type u_2} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> {α : Type u_5} -> (S : α → Submodule R M) -> Submodule R (α →₀ M)
<!-- PINNED-SIGNATURE:END -->


VTask.submodule : {R : Type u_1} -> {M : Type u_2} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> {α : Type u_5} -> (S : α → Submodule R M) -> Submodule R (α →₀ M)

The implicit arguments `R` and `M` are the ring and module respectively; the typeclass arguments supply the semiring structure on `R`, the additive commutative monoid structure on `M`, and the `R`-module structure. The implicit argument `α` is the index type. The explicit argument `S` is the family of submodules, assigning to each index `i : α` an `R`-submodule `S i` of `M`.

## Conventions

There are no declared junk-value or edge conventions for this definition: it is a total construction that is well-defined for every family of submodules over any (possibly empty or infinite) index type, and every element of the resulting submodule type carries the full pointwise membership data.

## Worked examples

- Claim: The zero element of `α →₀ M` always belongs to `VTask.submodule S`, for any family `S`.

- Claim: If `f : α →₀ M` satisfies `f i ∈ S i` for all `i`, and `g : α →₀ M` satisfies `g i ∈ S i` for all `i`, then `f + g ∈ VTask.submodule S`.

- Claim: `VTask.submodule S ≤ VTask.submodule T` whenever `S i ≤ T i` for all `i : α` (monotonicity in the family).

- Claim: For a constant family `S i = N` for all `i`, `VTask.submodule S` is the submodule of all finitely-supported functions whose values all lie in `N`.

## Boundaries

- **Empty index type**: When `α` is the empty type, the only finitely-supported function is the zero function, so `VTask.submodule S` contains only zero regardless of `S`.
- **Empty submodules**: If some `S i` is the zero submodule of `M`, then any member `f` of `VTask.submodule S` must satisfy `f i = 0`. In particular, if every `S i` is zero, `VTask.submodule S` is the zero submodule of `α →₀ M`.
- **Full submodules**: If every `S i` equals `M` as a submodule, then `VTask.submodule S` is the full submodule `⊤` of `α →₀ M`.
- **Finite support compatibility**: Because elements of `α →₀ M` are finitely supported (only finitely many values are nonzero), membership in `VTask.submodule S` still requires `f i ∈ S i` for *all* `i : α`; the finitely-supported condition is inherited from the ambient type, not imposed freshly.

## Not to be confused with

- `Submodule.pi`: The analogous construction for functions in `Π i, M i` (full dependent functions, not finitely supported), where each component type may differ per index.
- `Finsupp.supported`: The submodule of `α →₀ M` of functions whose support is contained in a given set, a different kind of restriction on finitely-supported functions.
- `Submodule.prod`: The product of two submodules over a product index type, which is a special binary case of a similar pointwise construction but lives in a product module, not a finitely-supported function module.