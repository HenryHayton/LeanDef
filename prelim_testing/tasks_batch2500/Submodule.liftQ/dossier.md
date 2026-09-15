## VTask.liftQ

### Object

Given a submodule `p` of a module `M` over a ring `R`, and a semilinear map `f : M →ₛₗ[τ₁₂] M₂` whose kernel contains `p` (i.e., `f` vanishes on every element of `p`), `VTask.liftQ p f h` is the unique semilinear map `M ⧸ p →ₛₗ[τ₁₂] M₂` from the quotient module `M ⧸ p` to `M₂` that makes the obvious triangle commute: composing it with the quotient map `M → M ⧸ p` recovers `f`. This is the universal property of the quotient: a linear map that kills a submodule descends uniquely to the quotient by that submodule.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.liftQ : {R : Type u_1} -> {M : Type u_2} -> [Ring R] -> [AddCommGroup M] -> [Module R M] -> (p : Submodule R M) -> {R₂ : Type u_3} -> {M₂ : Type u_4} -> [Ring R₂] -> [AddCommGroup M₂] -> [Module R₂ M₂] -> {τ₁₂ : R →+* R₂} -> (f : M →ₛₗ[τ₁₂] M₂) -> (h : p ≤ f.ker) -> M ⧸ p →ₛₗ[τ₁₂] M₂
<!-- PINNED-SIGNATURE:END -->


`VTask.liftQ : {R : Type u_1} -> {M : Type u_2} -> [Ring R] -> [AddCommGroup M] -> [Module R M] -> (p : Submodule R M) -> {R₂ : Type u_3} -> {M₂ : Type u_4} -> [Ring R₂] -> [AddCommGroup M₂] -> [Module R₂ M₂] -> {τ₁₂ : R →+* R₂} -> (f : M →ₛₗ[τ₁₂] M₂) -> (h : p ≤ f.ker) -> M ⧸ p →ₛₗ[τ₁₂] M₂`

The argument `p` is the submodule of `M` being quotiented out. The argument `f` is the semilinear map from `M` to `M₂`, twisted by the ring homomorphism `τ₁₂ : R →+* R₂`. The argument `h` is the proof obligation that `p` is contained in the kernel of `f`, guaranteeing that `f` is well-defined on equivalence classes. The ring homomorphism `τ₁₂` relates the scalar action on the source module to that on the target.

### Conventions

There are no special junk-value or out-of-domain conventions for this definition: it is a total construction and every input satisfying the stated types and the inequality `p ≤ f.ker` produces a well-defined semilinear map.

### Worked examples

- Claim: For any semilinear `f : M →ₛₗ[τ₁₂] M₂` with `p ≤ f.ker`, evaluating `VTask.liftQ p f h` at the class of `x : M` gives `f x`.
  (This is the defining pointwise identity: `(p.liftQ f h) (Quotient.mk x) = f x`, confirmed by `Submodule.liftQ_apply`.)

- Claim: Composing `VTask.liftQ p f h` with the quotient map `p.mkQ : M →ₗ[R] M ⧸ p` recovers `f` exactly as a linear map, i.e., `(p.liftQ f h).comp p.mkQ = f`.
  (This is the universal-property triangle identity, confirmed by `Submodule.liftQ_mkQ`.)

- Claim: The kernel of `VTask.liftQ p f h` equals the image of `ker f` under the quotient map `mkQ p`; in particular, if `ker f ≤ p`, then the kernel of the lifted map is trivial.
  (Confirmed by `Submodule.ker_liftQ` and `Submodule.ker_liftQ_eq_bot`.)

- Claim: When `τ₁₂` is surjective as a ring homomorphism, the range of `VTask.liftQ p f h` equals the range of `f`.
  (Confirmed by `Submodule.range_liftQ`.)

### Boundaries

- When `p = ⊥` (the zero submodule), the condition `p ≤ f.ker` is automatically satisfied for any `f`, and the lifted map is essentially isomorphic to `f` itself via the canonical isomorphism `M ⧸ ⊥ ≅ M`.
- When `p = ker f` exactly, the lifted map is injective: its kernel is `⊥` in `M ⧸ p`. This is the statement of `Submodule.ker_liftQ_eq_bot'`.
- When `p` properly contains `ker f` (but the hypothesis `h : p ≤ ker f` forces `p ⊆ ker f`, so this situation does not arise within the type), the map cannot be constructed.
- The hypothesis `h : p ≤ f.ker` is strictly required; without it, cosets would not map to well-defined values.

### Not to be confused with

- `Submodule.mkQ`: the quotient map `M →ₗ[R] M ⧸ p` going in the opposite direction; `liftQ` uses `mkQ` but produces a map *out of* the quotient rather than *into* it.
- `Submodule.liftQL`: the continuous version of the same construction for a continuous linear map `M →SL[σ] M₂`, which additionally carries a topological structure on the lifted map.
- `Submodule.quotientEquiv` / `Submodule.quotientEquivOfIsCompl`: linear *equivalences* (isomorphisms) involving quotients, not merely linear maps from quotients.
