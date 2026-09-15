## 1. Object

Two indices `i` and `j` in a root pairing are **orthogonal** when each root is a fixed point of the other's reflection. Concretely, this means the Cartan-like pairing of `i` against `j` is zero **and** the pairing of `j` against `i` is also zero. (In a root pairing the pairing is generally not symmetric, so both directions must vanish independently.) Geometrically, being orthogonal means the hyperplane reflection defined by root `i` fixes root `j`, and vice versa.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsOrthogonal : {ι : Type u_1} -> {R : Type u_2} -> {M : Type u_3} -> {N : Type u_4} -> [CommRing R] -> [AddCommGroup M] -> [Module R M] -> [AddCommGroup N] -> [Module R N] -> (P : RootPairing ι R M N) -> (i j : ι) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsOrthogonal : {ι : Type u_1} -> {R : Type u_2} -> {M : Type u_3} -> {N : Type u_4} -> [CommRing R] -> [AddCommGroup M] -> [Module R M] -> [AddCommGroup N] -> [Module R N] -> (P : RootPairing ι R M N) -> (i j : ι) -> Prop`

The implicit type arguments `ι`, `R`, `M`, `N` are respectively the index type, the coefficient ring, the ambient module in which roots live, and the ambient module in which coroots live; the typeclass arguments equip these with their algebraic structures. The explicit argument `P` is the root pairing whose pairing maps and reflections are used. The arguments `i` and `j` are the indices of the two roots being tested for orthogonality.

## 3. Conventions

Orthogonality requires **both** pairings to vanish: `pairing P i j = 0` and `pairing P j i = 0`. Under mild torsion-freeness and domain hypotheses the two conditions become equivalent to each other (so a single pairing vanishing suffices), but in general the definition is a conjunction and both halves are independent.

## 4. Worked examples

- Claim: `VTask.IsOrthogonal P i j` is equivalent to `VTask.IsOrthogonal P j i` for any root pairing `P` and any indices `i`, `j`.

- Claim: If `VTask.IsOrthogonal P i j` holds, then the reflection of root `i` by root `j` equals root `i` (i.e., `P.reflection j (P.root i) = P.root i`).

- Claim: If `VTask.IsOrthogonal P i j` holds, then the reflections `P.reflection i` and `P.reflection j` commute as linear maps.

- Claim: Under the hypotheses `[NeZero (2 : R)]`, `[IsDomain R]`, and `[Module.IsTorsionFree R M]`, `VTask.IsOrthogonal P i j` is equivalent to the single condition `P.pairing i j = 0`.

## 5. Boundaries

- The relation is **symmetric**: `VTask.IsOrthogonal P i j ↔ VTask.IsOrthogonal P j i`, so the order of `i` and `j` does not matter.
- When `i = j`, orthogonality of a root with itself would require `pairing P i i = 0`; in a non-degenerate root system this fails (the pairing of a root with itself equals 2 in classical normalizations), so a root is generally **not** orthogonal to itself.
- Under weak additional hypotheses (the ring is an integral domain, 2 is invertible, and the module is torsion-free), the two conditions `pairing P i j = 0` and `pairing P j i = 0` become logically equivalent, and one suffices to conclude orthogonality.
- The Coxeter weight `P.coxeterWeight i j` equals zero if and only if `VTask.IsOrthogonal P i j` (under `[NeZero (2 : R)]` and `[IsDomain R]`).

## 6. Not to be confused with

- **`RootPairing.pairing P i j = 0`** (one half of orthogonality): vanishing of a single pairing value does not in general imply the reverse pairing also vanishes, so it is strictly weaker than `VTask.IsOrthogonal`.
- **Orthogonality of vectors in an inner-product space**: the geometric notion that two vectors have zero inner product. For root systems over ℝ this coincides with `VTask.IsOrthogonal`, but the Mathlib definition is stated purely in terms of the abstract pairing maps, without reference to any inner product.
- **`RootPairing.coxeterWeight`**: the product `pairing P i j * pairing P j i`; it equals zero precisely when the pair is orthogonal, but it can also be zero if one factor vanishes without the other, making it a coarser invariant.