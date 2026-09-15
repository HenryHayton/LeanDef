## Object

`VTask.equivSubtypeMap p q` is the canonical linear equivalence (an invertible `R`-linear map) between a submodule `q` of a submodule `p` and the image of `q` under the inclusion map of `p` into the ambient module `M`. In other words, it witnesses that `q`, viewed as a submodule of the submodule `p`, is linearly isomorphic to the submodule of `M` obtained by pushing `q` forward along the coercion `p ↪ M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.equivSubtypeMap : {R : Type u_1} -> {M : Type u_5} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> (p : Submodule R M) -> (q : Submodule R ↥p) -> ↥q ≃ₗ[R] ↥(Submodule.map p.subtype q)
<!-- PINNED-SIGNATURE:END -->


`VTask.equivSubtypeMap : {R : Type u_1} -> {M : Type u_5} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> (p : Submodule R M) -> (q : Submodule R ↥p) -> ↥q ≃ₗ[R] ↥(Submodule.map p.subtype q)`

The first explicit argument `p` is a submodule of the ambient `R`-module `M`. The second explicit argument `q` is a submodule of `p` itself (i.e., a submodule of the module `↥p`). The result is an `R`-linear equivalence between the type `↥q` (elements of `q` as a subtype of `p`) and the type `↥(Submodule.map p.subtype q)` (elements of the image of `q` in `M` along the inclusion of `p`).

## Conventions

No junk-value or boundary conventions are declared: the definition is a construction over totally unconstrained valid algebraic data (any semiring `R`, any `R`-module `M`, any submodule `p` of `M`, and any submodule `q` of `p`); every input yields a well-defined linear equivalence.

## Worked examples

- Claim: For any element `x : ↥q`, the underlying element of `M` obtained by applying `VTask.equivSubtypeMap p q` to `x` equals the underlying element of `M` of `x` (i.e., the equiv is the identity on underlying elements).

- Claim: The inverse of `VTask.equivSubtypeMap p q` applied to an element `x : ↥(Submodule.map p.subtype q)` yields an element of `↥q` whose image in `M` is exactly the underlying `M`-element of `x`.

- Claim: `VTask.equivSubtypeMap p q` is a bijection from `↥q` to `↥(Submodule.map p.subtype q)`, so in particular the two types are in `R`-linear bijection.

## Boundaries

- When `q` is the zero submodule of `p`, the equivalence maps the trivial module to the trivial submodule `{0}` of `M` sitting inside `p`.
- When `q = p` (regarded as a submodule of itself, i.e., the top submodule of `p`), the image `Submodule.map p.subtype q` equals `p` itself as a submodule of `M`, and the equivalence is the identity on `↥p`.
- When `p = ⊤` (the whole module), elements of `p` are in canonical bijection with elements of `M`, and the equivalence reduces to the natural identification of `q` with its own image under the identity.
- The construction is available for any semiring `R` (not just a ring or field) and any `AddCommMonoid` with a module structure, so it applies in the generality of, e.g., modules over `ℕ`.

## Not to be confused with

- `Submodule.inclusion`: the `R`-linear map (not an equivalence) from a submodule `p` to a larger submodule `q` when `p ≤ q`; this is a monomorphism, not an isomorphism.
- `Submodule.comap_subtype_equiv_of_le`: a related equivalence for sub-submodules that goes in a different direction, comparing comap and submodule lattice operations rather than forward image under the subtype.
- `Submodule.mapSubtype.orderIso`: the order isomorphism between submodules of `p` and submodules of `M` contained in `p`; this is a lattice-level statement, not a linear equivalence between the submodule types themselves.