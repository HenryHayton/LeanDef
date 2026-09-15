## Object

`VTask.mk'` constructs a derivation from `R`-algebra `A` into an `A`-module `M` given a linear map and a proof that the linear map satisfies the Leibniz (product) rule. A derivation is an `R`-linear map `D : A → M` satisfying `D(ab) = a · D(b) + b · D(a)` for all `a, b ∈ A`; this constructor packages exactly those two ingredients when `M` is an additive cancellative commutative monoid (which allows the `map_one_eq_zero` condition to be derived automatically from the Leibniz rule rather than supplied by the user).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk' : {R : Type u_1} -> [CommSemiring R] -> {A : Type u_2} -> [CommSemiring A] -> [Algebra R A] -> {M : Type u_3} -> [AddCancelCommMonoid M] -> [Module R M] -> [Module A M] -> (D : A →ₗ[R] M) -> (h : ∀ (a b : A), D (a * b) = a • D b + b • D a) -> Derivation R A M
<!-- PINNED-SIGNATURE:END -->


VTask.mk' : {R : Type u_1} -> [CommSemiring R] -> {A : Type u_2} -> [CommSemiring A] -> [Algebra R A] -> {M : Type u_3} -> [AddCancelCommMonoid M] -> [Module R M] -> [Module A M] -> (D : A →ₗ[R] M) -> (h : ∀ (a b : A), D (a * b) = a • D b + b • D a) -> Derivation R A M

`R` is the base commutative semiring over which everything is linear. `A` is the source commutative semiring (algebra over `R`) whose elements are differentiated. `M` is the target module (simultaneously an `R`-module and an `A`-module) into which the derivation maps; it must additionally be an additive cancellative commutative monoid so that `D(1) = 0` can be deduced automatically. `D` is the underlying `R`-linear map from `A` to `M` that one wishes to promote to a derivation. `h` is the proof that `D` satisfies the Leibniz rule: for every pair of elements `a, b` in `A`, `D(a * b) = a • D(b) + b • D(a)`.

## Conventions

The `map_one_eq_zero` condition (i.e., `D 1 = 0`), which is one of the axioms of a `Derivation`, is not required as an explicit argument; it is automatically deduced from the Leibniz rule `h` together with the cancellative property of `M`. Concretely, specialising `h` at `a = b = 1` and using `1 • x = x` yields `D 1 = D 1 + D 1`, from which cancellation gives `D 1 = 0`.

## Worked examples

- Claim: For any `R`-linear map `D : A →ₗ[R] M` and proof `h` of the Leibniz rule, the coercion of `VTask.mk' D h` back to a function equals `D` as a function (i.e., `⇑(VTask.mk' D h) = ⇑D`).

- Claim: For any `R`-linear map `D : A →ₗ[R] M` and proof `h` of the Leibniz rule, the coercion of `VTask.mk' D h` to an `R`-linear map equals `D` (i.e., `(VTask.mk' D h : A →ₗ[R] M) = D`).

- Claim: The zero linear map `0 : A →ₗ[R] M` satisfies the Leibniz rule (both sides are zero), so `VTask.mk' 0 (fun a b => by simp)` is a well-formed derivation whose underlying function is the zero map.

## Boundaries

- The cancellative hypothesis on `M` (`AddCancelCommMonoid`) is essential for this variant of the constructor: without it one cannot deduce `D 1 = 0` from the Leibniz rule alone, so the standard `Derivation` constructor requires an explicit proof of `D 1 = 0`. When `M` is cancellative, `VTask.mk'` saves the user from supplying that proof.
- When `A` is a semiring (rather than a full ring) the derivation axioms are still well-posed; `VTask.mk'` works in this generality.
- If `D` is the zero linear map, the resulting derivation is the zero derivation regardless of the algebra or module.

## Not to be confused with

- `Derivation.mk` (the standard bundled constructor for `Derivation R A M`): requires an explicit proof that `D 1 = 0`, rather than deriving it from the Leibniz rule via cancellation.
- `LinearMap.mk` / `LinearMap.toFun`: constructs a mere linear map without any Leibniz-rule data; does not produce a derivation.
- `Derivation.toLinearMap`: the projection that extracts the underlying linear map *from* a derivation, which is the inverse direction of `VTask.mk'`.
