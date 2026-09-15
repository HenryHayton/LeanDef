## Object

A sesquilinear (or bilinear) map `B : M₁ →ₛₗ[I₁] M₂ →ₛₗ[I₂] M` is called **nondegenerate** if it is simultaneously left-separating and right-separating. Concretely:
- **Left-separating** means: if `B x y = 0` for every `y ∈ M₂`, then `x = 0`.
- **Right-separating** means: if `B x y = 0` for every `x ∈ M₁`, then `y = 0`.

In other words, neither argument of `B` can be "annihilated" by all elements of the other module without itself being zero. This generalises the classical notion of a non-degenerate bilinear form to the semilinear (twisted-scalar) setting over commutative semirings, and to maps landing in a module `M` rather than necessarily in a base ring.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Nondegenerate : {R : Type u_1} -> {R₁ : Type u_2} -> {R₂ : Type u_3} -> {M : Type u_5} -> {M₁ : Type u_6} -> {M₂ : Type u_7} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> [CommSemiring R₁] -> [AddCommMonoid M₁] -> [Module R₁ M₁] -> [CommSemiring R₂] -> [AddCommMonoid M₂] -> [Module R₂ M₂] -> {I₁ : R₁ →+* R} -> {I₂ : R₂ →+* R} -> (B : M₁ →ₛₗ[I₁] M₂ →ₛₗ[I₂] M) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `R`, `R₁`, `R₂` are the scalar commutative semirings involved. `M₁`, `M₂` are the source modules and `M` is the target module, each carrying the appropriate `AddCommMonoid` and `Module` instances. The ring homomorphisms `I₁ : R₁ →+* R` and `I₂ : R₂ →+* R` are the scalar-twist maps making `B` semilinear in each argument. The explicit argument `B` is the semilinear map whose non-degeneracy is being asserted.

## Conventions

No special junk-value or boundary conventions have been declared for this predicate: it is a straightforward logical conjunction of two well-defined separability conditions, and is defined for all inputs in its stated type.

## Worked examples

- Claim: The zero map `B = 0 : M₁ →ₛₗ[I₁] M₂ →ₛₗ[I₂] M` is **not** `VTask.Nondegenerate` whenever `M₁` and `M₂` are nontrivial, because `B x y = 0` for all `y` even when `x ≠ 0`, violating left-separability.

- Claim: For a finite-dimensional real inner product space `V`, the inner product bilinear form `⟪·, ·⟫ : V →ₗ[ℝ] V →ₗ[ℝ] ℝ` satisfies `VTask.Nondegenerate`, since the only vector with zero inner product against every other vector is `0`.

- Claim: Any nondegenerate bilinear map `B` satisfies `VTask.Nondegenerate B` if and only if it is left-separating and right-separating simultaneously.

- Claim: If `VTask.Nondegenerate B` holds, then for any nonzero `x ∈ M₁` there exists some `y ∈ M₂` with `B x y ≠ 0`, and for any nonzero `y ∈ M₂` there exists some `x ∈ M₁` with `B x y ≠ 0`.

## Boundaries

- If the source module `M₁` or `M₂` is the zero module (containing only `0`), the separating conditions become vacuously true, so `VTask.Nondegenerate B` holds for every map `B` from or into a trivial module — consistent with the convention that the only element is `0`.
- The zero map on a nontrivial domain is **never** nondegenerate, since it fails both separating conditions.
- Non-degeneracy is strictly stronger than each separating condition alone: a map can be left-separating but not right-separating, or vice versa, without being nondegenerate.
- The definition applies to semilinear maps with arbitrary twist homomorphisms `I₁`, `I₂`, including the identity (recovering ordinary bilinear maps) and complex conjugation (recovering sesquilinear forms).

## Not to be confused with

- `SeparatingLeft B`: only requires that `B` is left-separating; `VTask.Nondegenerate` additionally requires right-separability.
- `SeparatingRight B`: only requires that `B` is right-separating; `VTask.Nondegenerate` additionally requires left-separability.
- Non-degeneracy of a **quadratic form**: a distinct (though related) condition defined via the associated polar form, not directly a conjunction of two separability conditions on a bilinear map.