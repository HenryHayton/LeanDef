## Object

Given a proof that two natural numbers `i` and `j` are equal, `VTask.cast R M h` is the canonical linear equivalence (linear isomorphism) from the `i`-fold tensor power of the `R`-module `M` to the `j`-fold tensor power of `M`. It is the "trivial" or "transport" isomorphism that identifies these two spaces simply because their indices are definitionally or propositionally equal.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cast : (R : Type u_1) -> (M : Type u_2) -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> {i j : ℕ} -> (h : i = j) -> TensorPower R i M ≃ₗ[R] TensorPower R j M
<!-- PINNED-SIGNATURE:END -->


`VTask.cast : (R : Type u_1) -> (M : Type u_2) -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> {i j : ℕ} -> (h : i = j) -> TensorPower R i M ≃ₗ[R] TensorPower R j M`

The first explicit argument `R` is the commutative semiring of scalars. The second explicit argument `M` is the module over `R` whose tensor powers are being considered. The implicit arguments `i` and `j` are the natural-number exponents (indices) of the two tensor powers. The argument `h` is a proof that `i` equals `j`, which justifies the existence of the isomorphism.

## Conventions

When `h` is the reflexivity proof `rfl` (i.e., `i = i`), `VTask.cast R M rfl` is the identity linear equivalence on `TensorPower R i M`. There are no declared junk-value conventions since the function is total on its domain.

## Worked examples

- Claim: `VTask.cast R M (rfl : 3 = 3)` is a linear equivalence from `TensorPower R 3 M` to `TensorPower R 3 M`, and it acts as the identity on elements.

- Claim: For `h : 1 + 1 = 2`, `VTask.cast R M h` is a linear equivalence from `TensorPower R (1+1) M` to `TensorPower R 2 M` that transports every element without changing its algebraic structure.

- Claim: Composing `VTask.cast R M h` (for `h : i = j`) with `VTask.cast R M h.symm` (for `h.symm : j = i`) yields an equivalence homotopic to the identity on `TensorPower R i M`.

## Boundaries

- When `i = j = 0`, both sides are `TensorPower R 0 M`, which is canonically identified with `R` itself; the cast is still well-defined and is the identity in this case.
- When `i = j` but the proof `h` is not `rfl` (e.g., it is proved via some chain of equalities), the resulting equivalence is still the same as the identity, since propositional equality of natural numbers is proof-irrelevant.
- The map is always an isomorphism — it has a two-sided inverse given by `(VTask.cast R M h).symm`, which equals `VTask.cast R M h.symm`.
- Because `R` must be a `CommSemiring` and `M` an `R`-module, there is no version of this cast for non-module settings.

## Not to be confused with

- `TensorPower.reindex`: a more general reindexing linear equivalence that relabels the index type, of which `VTask.cast` is a special case using `finCongr`.
- `LinearEquiv.refl`: the identity linear equivalence on a fixed module; `VTask.cast` specialises to this only when `h = rfl`.
- `Equiv.cast`: a type-theoretic transport equivalence for types; `VTask.cast` is its linear-algebraic analogue but specifically for tensor powers and preserving the module structure.