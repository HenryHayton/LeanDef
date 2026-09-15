## 1. Object

`VTask.IsAlt B` is the proposition that a sesquilinear map `B : M₁ →ₛₗ[I₁] M₁ →ₛₗ[I₂] M` is **alternating**: it asserts that evaluating `B` on any vector twice — that is, `B x x` — yields the zero element of `M`, for every `x` in `M₁`. This is the sesquilinear analogue of the classical notion of an alternating bilinear form.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsAlt : {R : Type u_1} -> {R₁ : Type u_2} -> {M : Type u_5} -> {M₁ : Type u_6} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> [CommSemiring R₁] -> [AddCommMonoid M₁] -> [Module R₁ M₁] -> {I₁ I₂ : R₁ →+* R} -> (B : M₁ →ₛₗ[I₁] M₁ →ₛₗ[I₂] M) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `R`, `R₁`, `M`, `M₁` are the scalar rings and module types involved. The typeclass assumptions supply the necessary commutative semiring structures on `R` and `R₁`, additive commutative monoid structures on `M` and `M₁`, and the corresponding module structures. The ring homomorphisms `I₁ I₂ : R₁ →+* R` are the twisting maps that define the semilinearity of each argument slot. The principal argument `B` is the sesquilinear map being tested: it takes two elements of `M₁` (one in each slot, twisted by `I₁` and `I₂` respectively) and produces an element of `M`.

## 3. Conventions

No junk-value or out-of-domain edge conventions apply: the predicate is a universally quantified proposition over all `x : M₁`, and it is defined for every sesquilinear map without restriction.

## 4. Worked Examples

- Claim: The zero sesquilinear map `(0 : M₁ →ₛₗ[I₁] M₁ →ₛₗ[I₂] M)` satisfies `VTask.IsAlt 0`, since `0 x x = 0` for all `x`.

- Claim: If `B` satisfies `VTask.IsAlt B`, then for every `x : M₁` one has `B x x = 0` (this is exactly `IsAlt.self_eq_zero`).

- Claim: Over a field of characteristic zero with no zero divisors, `VTask.IsAlt B` (for `B : M₁ →ₛₗ[I] M₁ →ₛₗ[I] R`) is equivalent to `B = -B.flip`, i.e., `B` is skew-symmetric.

## 5. Boundaries

- Over a field of characteristic 2, alternating (`B x x = 0`) and skew-symmetric (`B x y + B y x = 0`) are not the same: every skew-symmetric map is symmetric in characteristic 2, but an alternating map still satisfies the diagonal-zero condition.
- The condition `B x x = 0` for all `x` implies `B x y + B y x = 0` for all `x, y` (by expanding `B (x+y) (x+y) = 0`), so alternating implies skew-symmetric in any characteristic.
- When `M` is cancellative (e.g., a module over a ring where addition is cancellable), `VTask.IsAlt B` together with a relation `a + b + c = 0` implies `B a b = B b c` (as in `IsAlt.eq_of_add_add_eq_zero`).
- There is no domain restriction: the predicate is total over all sesquilinear maps `B`.

## 6. Not to be confused with

- **`LinearMap.IsSymm`**: the predicate that `B x y = B y x` for all `x y`; symmetric forms are generally distinct from alternating ones except in characteristic 2.
- **`LinearMap.IsOrtho`**: orthogonality of two specific vectors with respect to `B`, not a global condition on the diagonal.
- **`LinearMap.Antisymm` / skew-symmetry**: the condition `B x y = -B y x`; this is implied by alternating but is strictly weaker in characteristic 2.