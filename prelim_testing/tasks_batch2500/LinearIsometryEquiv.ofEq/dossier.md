## Object

`VTask.ofEq` constructs a linear isometric equivalence (a bijective linear map that is simultaneously an isometry) between two submodules of a seminormed additive commutative group, given a proof that the two submodules are equal. When two submodules `p` and `q` of a module `E` happen to be literally equal as submodules, this function packages that equality into a canonical isometric isomorphism `p ≃ₗᵢ[R'] q` whose underlying map is just the identity (reinterpreted along the equality proof).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofEq : {E : Type u_5} -> [SeminormedAddCommGroup E] -> {R' : Type u_12} -> [Ring R'] -> [Module R' E] -> (p q : Submodule R' E) -> (hpq : p = q) -> ↥p ≃ₗᵢ[R'] ↥q
<!-- PINNED-SIGNATURE:END -->


`VTask.ofEq : {E : Type u_5} -> [SeminormedAddCommGroup E] -> {R' : Type u_12} -> [Ring R'] -> [Module R' E] -> (p q : Submodule R' E) -> (hpq : p = q) -> ↥p ≃ₗᵢ[R'] ↥q`

`E` is the ambient seminormed additive commutative group serving as the module. `R'` is the scalar ring acting on `E`. `p` and `q` are the two submodules of `E` (with scalar ring `R'`) between which the isometric equivalence is constructed. `hpq` is the proof that `p` and `q` are equal as submodules.

## Conventions

When `p = q` (i.e., the two submodules are definitionally or propositionally equal), the resulting linear isometric equivalence acts as the identity map: elements are sent to their counterpart in the equal submodule without any modification to their value or norm.

## Worked examples

- Claim: For any submodule `p`, `VTask.ofEq p p rfl` is a linear isometric equivalence from `p` to itself, and it maps every element to itself.

- Claim: If `p = q` as submodules of a normed space `E`, then for every `x : ↥p`, the norm of `VTask.ofEq p q hpq x` equals the norm of `x` (the map is an isometry).

- Claim: The linear isometric equivalence `VTask.ofEq p q hpq` has an inverse `VTask.ofEq q p hpq.symm`, and their composition is the identity.

## Boundaries

- The definition requires a proof that `p = q` as submodules; it is not defined for merely isomorphic or isometric submodules.
- When `hpq` is `rfl` (i.e., `p` and `q` are definitionally equal), the resulting equivalence is particularly trivial: the map and its inverse are both the identity on elements.
- Since the ambient space `E` need only be a seminormed group (not necessarily a normed space), the construction works even when the norm is degenerate (i.e., elements can have zero norm without being zero).
- The map is always bijective and linear by construction, with the norm preservation following from the fact that the subtype inclusion preserves norms and the map is the identity on underlying elements.

## Not to be confused with

- `LinearEquiv.ofEq`: The analogous construction that only gives a linear equivalence (not an isometric one), without the norm-preservation guarantee.
- `LinearIsometryEquiv.refl`: The identity isometric equivalence on a single module/submodule, which does not require or use a proof of equality between two distinct submodules.
- `Submodule.equivOfEq` or similar: Other constructions that may produce equivalences between equal submodules but in a different category or without the isometry structure.