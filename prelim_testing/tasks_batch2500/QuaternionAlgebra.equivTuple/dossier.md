## VTask.equivTuple

### Object

A canonical equivalence (bijection) between the quaternion algebra `ℍ[R, c₁, c₂, c₃]` over a type `R` with structural constants `c₁`, `c₂`, `c₃` and the type of functions from `{0, 1, 2, 3}` (i.e., `Fin 4 → R`) into `R`. The forward direction extracts the four components of a quaternion into a 4-tuple, and the backward direction assembles a 4-tuple into a quaternion.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.equivTuple : {R : Type u_1} -> (c₁ c₂ c₃ : R) -> QuaternionAlgebra R c₁ c₂ c₃ ≃ (Fin 4 → R)
<!-- PINNED-SIGNATURE:END -->


The implicit argument `R` is the coefficient type (typically a ring or field). The three explicit arguments `c₁`, `c₂`, `c₃` are the structural constants that parameterise the quaternion algebra — they govern the multiplication rules among the basis elements `i`, `j`, `k` in `ℍ[R, c₁, c₂, c₃]`.

### Conventions

The forward map sends a quaternion with real part `a.1` and imaginary components `a.2`, `a.3`, `a.4` to the function assigning index `0 ↦ a.1`, `1 ↦ a.2`, `2 ↦ a.3`, `3 ↦ a.4`; the inverse map reconstructs the quaternion from the four values at indices `0`, `1`, `2`, `3` in that fixed order.

### Worked examples

- Claim: Applying `VTask.equivTuple` to the quaternion `⟨1, 2, 3, 4⟩` in `ℍ[ℝ, c₁, c₂, c₃]` yields the function `![1, 2, 3, 4] : Fin 4 → ℝ`.

- Claim: The composition of the inverse of `VTask.equivTuple c₁ c₂ c₃` followed by `VTask.equivTuple c₁ c₂ c₃` is the identity on `Fin 4 → R`.

- Claim: For the standard Hamilton quaternions `ℍ[ℝ, -1, -1, -1]`, applying `VTask.equivTuple (-1) (-1) (-1)` to the zero quaternion yields the zero function `fun _ => 0`.

- Claim: For any quaternion `q : ℍ[R, c₁, c₂, c₃]`, `(VTask.equivTuple c₁ c₂ c₃ q) 0 = q.re`.

### Boundaries

- The equivalence is defined for any type `R`; no ring or field structure on `R` is required. It is a pure set-theoretic equivalence (a bijection of types), not a ring or module isomorphism, so no algebraic structure is assumed.
- The four-component indexing is zero-based and in fixed order: component `0` is the real (scalar) part, components `1`, `2`, `3` are the three imaginary parts.
- When `R` has only one element (a subsingleton), the equivalence still holds and both sides are singletons.

### Not to be confused with

- `QuaternionAlgebra.linearEquivTuple` — a version of this equivalence that also respects linear (module) structure over `R`, carrying more algebraic coherence data.
- `Quaternion.equivTuple` — the specialisation to the standard Hamilton quaternions `ℍ[R, -1, -1]`, which may carry additional algebraic structure assumptions.
- `Fin 4 → R` vs `R × R × R × R` — the codomain is functions from `Fin 4`, not a nested product type; do not confuse the two representations of 4-tuples.