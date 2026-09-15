## Object

`VTask.lid` is the canonical linear equivalence that witnesses the left unit law for the tensor product of modules over a commutative semiring: it identifies the tensor product `R ⊗[R] M` with `M` itself by sending a simple tensor `r ⊗ m` to the scalar multiple `r • m`. This isomorphism expresses the fact that tensoring an `R`-module `M` on the left with the base ring `R` (viewed as an `R`-module over itself) recovers `M` up to canonical isomorphism.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lid : (R : Type u_1) -> [CommSemiring R] -> (M : Type u_5) -> [AddCommMonoid M] -> [Module R M] -> TensorProduct R R M ≃ₗ[R] M
<!-- PINNED-SIGNATURE:END -->


`VTask.lid : (R : Type u_1) -> [CommSemiring R] -> (M : Type u_5) -> [AddCommMonoid M] -> [Module R M] -> TensorProduct R R M ≃ₗ[R] M`

The first explicit argument `R` is the commutative semiring acting as the base ring (and as the left factor in the tensor product). The second explicit argument `M` is the `R`-module forming the right factor. The instance arguments supply the algebraic structures: a `CommSemiring` structure on `R`, an `AddCommMonoid` structure on `M`, and an `R`-module structure on `M`.

## Conventions

No junk-value conventions apply: both `R` and `M` are constrained to carry their required algebraic structures via typeclass instances, so the equivalence is well-defined for every valid pair of inputs. There are no edge cases involving degenerate or trivial inputs that produce conventionally assigned outputs.

## Worked examples

- Claim: The forward map of `VTask.lid R M` sends a simple tensor `r ⊗ m` to `r • m`; in particular, for `R = ℤ` and `M = ℤ`, the element `3 ⊗ₜ 5` maps to `15`.

- Claim: The inverse map of `VTask.lid R M` sends any `m : M` back to `1 ⊗ₜ m` in `R ⊗[R] M`.

- Claim: Composing the forward direction of `VTask.lid R M` with its inverse is the identity on `R ⊗[R] M`, i.e., `(VTask.lid R M).symm` followed by `VTask.lid R M` is the identity linear map.

- Claim: The forward map is `R`-linear: for any `s : R` and `x : R ⊗[R] M`, `(VTask.lid R M) (s • x) = s • (VTask.lid R M) x`.

## Boundaries

- When `M = R` (the base ring viewed as a module over itself), the equivalence `VTask.lid R R` is a ring-module isomorphism between `R ⊗[R] R` and `R`, mapping `r ⊗ s` to `r * s`.
- When `M = 0` (the zero module), the equivalence degenerates to the unique isomorphism between `R ⊗[R] 0 ≅ 0` and `0`, which is always valid.
- The equivalence is natural in `M`: a linear map `f : M →ₗ[R] N` intertwines the two left-unit equivalences, i.e., `VTask.lid R N ∘ (id_R ⊗ f) = f ∘ VTask.lid R M`.

## Not to be confused with

- `TensorProduct.rid`: the analogous right unit equivalence `M ⊗[R] R ≃ₗ[R] M`, which acts by `m ⊗ r ↦ r • m` from the right factor.
- `TensorProduct.comm`: the commutativity equivalence `M ⊗[R] N ≃ₗ[R] N ⊗[R] M`, which swaps the two factors rather than collapsing one of them into scalar multiplication.
- `TensorProduct.assoc`: the associativity equivalence `(M ⊗[R] N) ⊗[R] P ≃ₗ[R] M ⊗[R] (N ⊗[R] P)`, a rebracketing rather than a unit law.