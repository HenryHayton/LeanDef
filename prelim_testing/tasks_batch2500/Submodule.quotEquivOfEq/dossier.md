## Object

Given two submodules `p` and `p'` of an `R`-module `M` that happen to be equal, `VTask.quotEquivOfEq` produces a canonical linear equivalence (linear isomorphism) between the quotient module `M ⧸ p` and the quotient module `M ⧸ p'`. Intuitively, if two submodules are literally the same object, quotienting by each should yield the same (up to canonical isomorphism) quotient module, and this construction witnesses that fact.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.quotEquivOfEq : {R : Type u_1} -> {M : Type u_2} -> [Ring R] -> [AddCommGroup M] -> [Module R M] -> (p p' : Submodule R M) -> (h : p = p') -> (M ⧸ p) ≃ₗ[R] M ⧸ p'
<!-- PINNED-SIGNATURE:END -->


VTask.quotEquivOfEq : {R : Type u_1} -> {M : Type u_2} -> [Ring R] -> [AddCommGroup M] -> [Module R M] -> (p p' : Submodule R M) -> (h : p = p') -> (M ⧸ p) ≃ₗ[R] M ⧸ p'

`R` is the ring of scalars, given implicitly. `M` is the module over `R`, also implicit. The three instance arguments supply the ring structure on `R`, the abelian group structure on `M`, and the `R`-module structure on `M`. The first explicit argument `p` is the submodule being quotiented in the domain. The second explicit argument `p'` is the submodule being quotiented in the codomain. The argument `h` is the proof that `p` and `p'` are equal as submodules.

## Conventions

No special junk-value or edge-case conventions are declared for this construction: it is defined for any proof of equality of submodules and always produces a well-defined linear equivalence.

## Worked examples

- Claim: When `p = p'` and `h : p = p'` is `rfl`, the equivalence `VTask.quotEquivOfEq p p rfl` sends the coset of any element `m : M` in `M ⧸ p` to the coset of the same element `m` in `M ⧸ p`.

- Claim: For the zero submodule `⊥` of a module `M`, `VTask.quotEquivOfEq ⊥ ⊥ rfl` is a linear equivalence from `M ⧸ ⊥` to `M ⧸ ⊥` that acts as the identity on every coset.

- Claim: If `p q : Submodule R M` and `h : p = q`, then the forward map of `VTask.quotEquivOfEq p q h` followed by the inverse of `VTask.quotEquivOfEq p q h` is the identity on `M ⧸ p`.

## Boundaries

- The only input that varies in a non-trivial way is the proof `h : p = p'`; when `p` and `p'` are definitionally equal, `h = rfl` yields the trivially defined equivalence.
- The equivalence is always an isomorphism (it has a two-sided inverse by design), even though the construction is driven entirely by a propositional equality, not by any structural data beyond `h`.
- When `p = p'`, the underlying function of the equivalence sends the coset `⟦m⟧` in `M ⧸ p` to the coset `⟦m⟧` in `M ⧸ p'`; it is not just abstractly an isomorphism but concretely acts as the "reindexing" identity on representatives.

## Not to be confused with

- `Submodule.Quotient.equiv` — a more general construction giving a linear equivalence between quotients induced by a linear equivalence of the ambient modules (not just an equality of submodules).
- `LinearEquiv.refl R (M ⧸ p)` — the identity linear equivalence on a single fixed quotient module; `VTask.quotEquivOfEq` targets two potentially syntactically distinct quotient types related by an equality of submodules.
- `Submodule.quotientEquivOfEq` (if it existed as a type-level rewrite) — one might confuse this with a coercion or subst at the type level rather than an explicit linear equivalence witnessing the isomorphism.