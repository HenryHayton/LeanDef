## Object

`VTask.prod f g` is the **Cartesian product of two alternating multilinear maps** with a common domain and index type, assembled into a single alternating multilinear map whose codomain is the product module `N × P`. Concretely, given a tuple `v : ι → M` of vectors from `M`, the combined map sends `v` to the pair `(f v, g v)` in `N × P`. The alternating property (vanishing whenever two inputs coincide) is inherited component-wise from `f` and `g`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {R : Type u_1} -> [Semiring R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> {N : Type u_3} -> [AddCommMonoid N] -> [Module R N] -> {P : Type u_4} -> [AddCommMonoid P] -> [Module R P] -> {ι : Type u_7} -> (f : M [⋀^ι]→ₗ[R] N) -> (g : M [⋀^ι]→ₗ[R] P) -> M [⋀^ι]→ₗ[R] (N × P)
<!-- PINNED-SIGNATURE:END -->


`VTask.prod : {R : Type u_1} -> [Semiring R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> {N : Type u_3} -> [AddCommMonoid N] -> [Module R N] -> {P : Type u_4} -> [AddCommMonoid P] -> [Module R P] -> {ι : Type u_7} -> (f : M [⋀^ι]→ₗ[R] N) -> (g : M [⋀^ι]→ₗ[R] P) -> M [⋀^ι]→ₗ[R] (N × P)`

`R` is the commutative semiring of scalars. `M` is the common source module from which all inputs are drawn. `N` and `P` are the two target modules. `ι` is the index type parametrising the number and arrangement of arguments. `f` is the first alternating multilinear map, landing in `N`. `g` is the second alternating multilinear map, landing in `P`. The result is the alternating multilinear map that evaluates both `f` and `g` on the same tuple of inputs and pairs the results.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total constructor that is well-defined for all valid pairs of alternating maps `f` and `g` sharing the same source module `M`, scalar ring `R`, and index type `ι`.

## Worked examples

- Claim: Applying `VTask.prod f g` to a tuple `v` yields `(f v, g v)` — that is, the first component of the result equals `f` evaluated at `v`, and the second component equals `g` evaluated at `v`.

- Claim: If `f` is the zero alternating map and `g` is an arbitrary alternating map `g`, then `VTask.prod 0 g` applied to any tuple `v` gives `(0, g v)` in `N × P`.

- Claim: If both `f` and `g` are zero alternating maps, then `VTask.prod 0 0` is the zero alternating map into `N × P`, i.e., it evaluates to `(0, 0)` on every input tuple.

- Claim: The underlying multilinear map of `VTask.prod f g` is the product of the underlying multilinear maps of `f` and `g` — applying it to `v` yields `(f.toMultilinearMap v, g.toMultilinearMap v)`.

## Boundaries

- When `ι` is empty (the zero-arity case), both `f` and `g` are constants (elements of `N` and `P` respectively viewed as zero-ary alternating maps), and `VTask.prod f g` is the constant map to the pair of those elements. The alternating condition is vacuously satisfied.
- When `N` or `P` is the zero module `{0}`, the corresponding component of every output is `0`, and the product simply reproduces the other map up to the trivial component.
- The alternating condition is satisfied automatically: if any two inputs `v i` and `v j` (with `i ≠ j`) coincide, then both `f v = 0` and `g v = 0`, so the result is `(0, 0)` in `N × P`.

## Not to be confused with

- **`AlternatingMap.smulRight` / scalar multiplication**: combines a scalar alternating map with an element of a module by forming the tensor, not a Cartesian pair.
- **`AlternatingMap.coprod`**: would combine maps with *different* domain modules (if it existed), as opposed to `VTask.prod` which pairs maps on the *same* domain.
- **`MultilinearMap.prod`**: the analogous construction for multilinear maps that are *not* required to be alternating; `VTask.prod` additionally enforces the alternating property on the result.