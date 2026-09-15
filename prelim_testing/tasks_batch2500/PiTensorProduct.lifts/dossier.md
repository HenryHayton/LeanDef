## Object

`VTask.lifts x` is the set of all "pre-images" of an element `x` in the tensor product `⨂[R] i, s i` under the canonical quotient map from the free additive monoid on pairs `(R × Π i, s i)`. Concretely, an element of `FreeAddMonoid (R × Π i, s i)` is a finite list of pairs `(r, v)` where `r : R` is a scalar and `v : Π i, s i` is a tuple of vectors (one per index). Such a list is a "lift" of `x` precisely when, after imposing all the multilinearity and compatibility relations that define the tensor product, it represents `x`. One can think of elements of the lift set as explicit finite formal sums of pure tensors that evaluate to `x` in the tensor product.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lifts : {ι : Type u_1} -> {R : Type u_4} -> [CommSemiring R] -> {s : ι → Type u_7} -> [(i : ι) → AddCommMonoid (s i)] -> [(i : ι) → Module R (s i)] -> (x : PiTensorProduct R fun i => s i) -> Set (FreeAddMonoid (R × ((i : ι) → s i)))
<!-- PINNED-SIGNATURE:END -->


`VTask.lifts : {ι : Type u_1} -> {R : Type u_4} -> [CommSemiring R] -> {s : ι → Type u_7} -> [(i : ι) → AddCommMonoid (s i)] -> [(i : ι) → Module R (s i)] -> (x : PiTensorProduct R fun i => s i) -> Set (FreeAddMonoid (R × ((i : ι) → s i)))`

- `ι` is the index type enumerating the tensor factors.
- `R` is the commutative semiring of scalars, equipped with its `CommSemiring` instance.
- `s` is the family of types, one for each index, forming the tensor factors; each `s i` carries an `AddCommMonoid` and an `R`-module structure.
- `x` is the element of the iterated tensor product `⨂[R] i, s i` whose pre-images are being collected.

The function returns the set of all elements of `FreeAddMonoid (R × Π i, s i)` — i.e., finite lists of scalar-tuple pairs — that map to `x` under the quotient map defining the tensor product.

## Conventions

There are no declared junk-value or boundary conventions for this definition: the function is total and well-defined for every element `x` of the tensor product, and the return type is simply the (possibly empty, but actually always nonempty) fibre of the quotient map over `x`.

## Worked examples

- Claim: For any `x : ⨂[R] i, s i`, the set `VTask.lifts x` is nonempty, because the quotient map from `FreeAddMonoid (R × Π i, s i)` is surjective — every element of the tensor product has at least one lift.

- Claim: If `p` and `q` are both in `VTask.lifts x`, then they represent the same element of the tensor product: they are equal in the quotient, even though they may differ as elements of the free additive monoid.

- Claim: For the zero element `0 : ⨂[R] i, s i`, the empty list `0 : FreeAddMonoid (R × Π i, s i)` (the identity element of the free additive monoid) belongs to `VTask.lifts 0`, since the quotient map sends the empty list to the zero of the tensor product.

- Claim: If `p ∈ VTask.lifts x` and `q ∈ VTask.lifts y`, then `p + q ∈ VTask.lifts (x + y)`, reflecting that the quotient map is a monoid homomorphism.

## Boundaries

- The set `VTask.lifts x` is never empty: since the quotient map `FreeAddMonoid (R × Π i, s i) →+ ⨂[R] i, s i` is surjective by construction, every `x` has at least one preimage.
- When `x = 0`, the empty list (the zero of `FreeAddMonoid`) is always a lift, but it is not the only one — any list that represents the zero tensor also belongs to the set.
- The set `VTask.lifts x` is in general a proper subset (a coset) of the kernel of the quotient map shifted by any fixed lift of `x`; it is not a submonoid unless `x = 0`.
- The definition makes sense even when `ι` is an empty type; in that case the tensor product is `R` itself (by convention) and the lifts are all preimages of a scalar.

## Not to be confused with

- `PiTensorProduct.tprod R s`: the canonical multilinear map sending a family of vectors to their pure tensor — this is a specific element of the tensor product, not a set of lifts.
- The kernel of the quotient map `FreeAddMonoid (R × Π i, s i) →+ ⨂[R] i, s i`: `VTask.lifts 0` equals this kernel, but for nonzero `x` the lifts form a coset rather than a subgroup.
- `FreeAddMonoid (R × Π i, s i)` itself: this is the ambient space from which lifts are drawn, not the set of lifts of a particular element.