## VTask.quotEquivOfEqBot

### Object

Given an `R`-module `M` and a submodule `p` of `M` that happens to equal the trivial submodule `⊥`, this is the canonical linear equivalence (an invertible, `R`-linear isomorphism) between the quotient module `M ⧸ p` and `M` itself. Intuitively, quotienting by the zero submodule changes nothing, and this equivalence makes that precise at the level of bundled linear maps.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.quotEquivOfEqBot : {R : Type u_1} -> {M : Type u_2} -> [Ring R] -> [AddCommGroup M] -> [Module R M] -> (p : Submodule R M) -> (hp : p = ⊥) -> (M ⧸ p) ≃ₗ[R] M
<!-- PINNED-SIGNATURE:END -->


`VTask.quotEquivOfEqBot : {R : Type u_1} -> {M : Type u_2} -> [Ring R] -> [AddCommGroup M] -> [Module R M] -> (p : Submodule R M) -> (hp : p = ⊥) -> (M ⧸ p) ≃ₗ[R] M`

The implicit argument `R` is the ring of scalars. The implicit argument `M` is the module being quotiented. The argument `p` is the submodule by which the quotient is formed. The argument `hp` is a proof that `p` equals the bottom (zero) submodule `⊥`; this hypothesis is precisely the condition that makes the quotient canonically isomorphic to the original module.

### Conventions

The forward direction of the equivalence sends the equivalence class of an element `x : M` (i.e., `Quotient.mk x`) to `x` itself. The backward direction (the symm) sends `x : M` to its equivalence class `Quotient.mk x` in `M ⧸ p`. The underlying linear map of the symm coincides with the quotient map `mkQ`.

### Worked examples

- Claim: For `p = ⊥` in a module `M`, applying `VTask.quotEquivOfEqBot` to the class `⟦x⟧` returns `x`.

- Claim: For `p = ⊥` in a module `M`, the symm of `VTask.quotEquivOfEqBot` applied to `x : M` returns the class `⟦x⟧` in `M ⧸ p`.

- Claim: For `p = ⊥` in a module `M`, the coercion of `(VTask.quotEquivOfEqBot hp).symm` to a linear map equals `p.mkQ` (the canonical quotient map).

### Boundaries

The definition requires the hypothesis `hp : p = ⊥` — it is only defined when the submodule is provably the zero submodule. There is no meaningful "junk value" regime: the function is total over its stated domain (submodules that equal `⊥`). The resulting equivalence is definitionally the identity on underlying elements: forward maps `⟦x⟧ ↦ x` and backward maps `x ↦ ⟦x⟧`. No special behavior arises from empty modules or zero scalars beyond what holds for any linear equivalence.

### Not to be confused with

- `Submodule.quotEquivOfEq` — a more general equivalence `M ⧸ p ≃ₗ[R] M ⧸ q` for two equal submodules `p = q`, which does not assume either is `⊥`.
- `Submodule.mkQ` — the canonical *linear map* (not an equivalence) `M →ₗ[R] M ⧸ p`, which is the forward map of the symm here but is not itself an isomorphism.
- `Submodule.quotientBot` — a related statement that `M ⧸ ⊥` is isomorphic to `M`, but expressed via a different route or as a definitional equality rather than a bundled linear equivalence taking an explicit submodule and proof.
