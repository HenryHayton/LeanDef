## Object

`VTask.toNonUnitalSubalgebra` converts a submodule of a (non-unital, non-associative) semialgebra into a non-unital subalgebra, provided that the submodule is additionally closed under multiplication. In other words, if `p` is an `R`-submodule of `A` and one can show that `p` is closed under the ring multiplication of `A`, then `p` qualifies as a non-unital `R`-subalgebra of `A`, and this function packages it as such.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toNonUnitalSubalgebra : {R : Type u_1} -> {A : Type u_2} -> [CommSemiring R] -> [NonUnitalNonAssocSemiring A] -> [Module R A] -> (p : Submodule R A) -> (h_mul : ∀ (x y : A), x ∈ p → y ∈ p → x * y ∈ p) -> NonUnitalSubalgebra R A
<!-- PINNED-SIGNATURE:END -->


VTask.toNonUnitalSubalgebra : {R : Type u_1} -> {A : Type u_2} -> [CommSemiring R] -> [NonUnitalNonAssocSemiring A] -> [Module R A] -> (p : Submodule R A) -> (h_mul : ∀ (x y : A), x ∈ p → y ∈ p → x * y ∈ p) -> NonUnitalSubalgebra R A

`R` is the commutative semiring of scalars. `A` is the ambient non-unital, non-associative semiring equipped with an `R`-module structure (making it a semialgebra). `p` is the `R`-submodule of `A` to be promoted. `h_mul` is the proof that `p` is closed under multiplication: for any two elements `x` and `y` of `A`, if both lie in `p`, then their product `x * y` also lies in `p`.

## Conventions

No junk-value or boundary conventions are declared for this definition: it is a total construction on well-typed inputs, and no degenerate input yields a meaningfully distinct output that requires a convention.

## Worked examples

- Claim: For any `R`-submodule `p` of `A` and multiplication-closure proof `h`, an element `a : A` belongs to `VTask.toNonUnitalSubalgebra p h` if and only if it belongs to `p`.

- Claim: If `p ≤ q` as submodules of `A` and both are equipped with multiplication-closure proofs `hp` and `hq`, then `VTask.toNonUnitalSubalgebra p hp ≤ VTask.toNonUnitalSubalgebra q hq` as non-unital subalgebras.

- Claim: The underlying `R`-submodule of `VTask.toNonUnitalSubalgebra p h_mul` (i.e., its carrier viewed as a submodule) equals `p`.

## Boundaries

- The function is total: it requires no hypothesis beyond the types, instances, the submodule, and the multiplication-closure proof. Any valid `Submodule R A` paired with a valid `h_mul` yields a well-formed `NonUnitalSubalgebra R A`.
- The construction does **not** require a multiplicative identity to exist in `p` (or even in `A`); it is precisely designed for the non-unital setting.
- If `A` happens to be unital and `p` contains `1`, the result is still a valid non-unital subalgebra; the unital structure is simply not recorded by this constructor.
- The additive and scalar-multiplication structure of the resulting `NonUnitalSubalgebra R A` is exactly that of `p` as a submodule—no data is altered or lost.

## Not to be confused with

- `Submodule.toSubalgebra` (or analogous): a version that additionally requires membership of the ring unit `1 ∈ p`, yielding a full (unital) subalgebra rather than a non-unital one.
- `NonUnitalSubalgebra.toSubmodule`: the **reverse** direction, which forgets the multiplicative closure and returns the underlying submodule of a non-unital subalgebra.
- `Subalgebra.toSubmodule`: similar forgetful functor but for unital subalgebras; conflating these can obscure whether unitality is present.