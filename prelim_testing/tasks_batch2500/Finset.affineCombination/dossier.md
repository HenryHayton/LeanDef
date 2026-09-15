## Object

Given a finite index set `ι`, a collection of points `p : ι → P` in an affine space `P` (over a ring `k` with translation vector space `V`), and a finite set `s : Finset ι`, `VTask.affineCombination s p` is the **affine map** from weight functions `ι → k` to points of `P` that sends a weight function `w` to the affine (barycentric) combination
$$\sum_{i \in s} w(i) \cdot p(i)$$
interpreted in the affine-space sense. When the weights sum to 1, this is precisely the affine combination (barycenter) of the points `p(i)` with those weights. The result is packaged as a `k`-affine map `(ι → k) →ᵃ[k] P`, whose underlying linear part is the weighted vector subtraction `weightedVSub s p`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.affineCombination : (k : Type u_1) -> {V : Type u_2} -> {P : Type u_3} -> [Ring k] -> [AddCommGroup V] -> [Module k V] -> [S : AddTorsor V P] -> {ι : Type u_4} -> (s : Finset ι) -> (p : ι → P) -> (ι → k) →ᵃ[k] P
<!-- PINNED-SIGNATURE:END -->


`VTask.affineCombination : (k : Type u_1) -> {V : Type u_2} -> {P : Type u_3} -> [Ring k] -> [AddCommGroup V] -> [Module k V] -> [S : AddTorsor V P] -> {ι : Type u_4} -> (s : Finset ι) -> (p : ι → P) -> (ι → k) →ᵃ[k] P`

- `k` is the scalar ring over which the affine space and the weights live.
- `V` is the translation vector space of the affine space.
- `P` is the affine space (a torsor over `V`).
- The typeclass arguments supply the ring structure on `k`, the abelian group structure on `V`, the `k`-module structure on `V`, and the torsor structure making `P` an affine space.
- `ι` is the index type enumerating the points.
- `s` is the finite set of indices that are summed over; only points indexed by elements of `s` contribute to the combination.
- `p` is the family of points in `P` indexed by `ι`.
- The return value is the affine map `(ι → k) →ᵃ[k] P` sending each weight function to the corresponding weighted combination of the points.

## Conventions

The affine combination is defined for all weight functions, not merely those whose weights sum to 1; lemmas that require the barycenter interpretation carry an explicit hypothesis that the weights sum to 1. The specific base point used internally to reduce the affine combination to a vector computation is chosen from the torsor by a classical choice and does not affect the value of the map (any two choices give the same result for weight sums equal to 1).

## Worked examples

- Claim: For any single-point family `p : Fin 1 → P` and the weight function constantly equal to `1`, applying `VTask.affineCombination {0} p` to that weight function returns `p 0`.

- Claim: The underlying linear map of `VTask.affineCombination s p` (i.e., its `.linear` component) equals `Finset.weightedVSub s p`.

- Claim: When all weights are zero, `VTask.affineCombination s p` applied to the zero weight function returns the canonical base point of the torsor (the internally chosen default point), reflecting the empty-sum convention.

- Claim: For two points `p 0` and `p 1` in a real affine space and the weight function `w 0 = 1/2, w 1 = 1/2`, the value of `VTask.affineCombination {0,1} p w` is the midpoint of `p 0` and `p 1`.

## Boundaries

- **Empty index set (`s = ∅`)**: The sum is empty, and the map returns the internally chosen base point regardless of the weight function. This base point is a classical choice from the (necessarily nonempty) torsor, but the result is still a well-defined affine map.
- **Singleton (`|s| = 1`)**: For `s = {i}`, the combination reduces to `w(i) • (p(i) -ᵥ base) +ᵥ base`; when `w(i) = 1` this equals `p(i)` as expected.
- **Weights not summing to 1**: The map is defined and well-typed for any weights, but geometrically the output may not lie in the affine hull of the points in any meaningful barycentric sense; lemmas about barycentric properties require the sum-to-1 hypothesis explicitly.
- **Repetitions in the index family**: The same geometric point may appear multiple times (via different indices in `ι`); the combination counts each such index separately according to `s`.

## Not to be confused with

- `Finset.weightedVSub`: The *linear* (vector-valued) map that computes a weighted alternating sum of differences of points; it is the linear part of `VTask.affineCombination`, not the affine map itself.
- `Finset.weightedVSubOfPoint`: A helper that subtracts a *specific* base point from each `p(i)` before weighting; `VTask.affineCombination` wraps this into a base-point-independent affine map.
- `Finset.centroid`: The special case where all weights equal `1 / |s|`; it is a particular evaluation of `VTask.affineCombination`, not the general weighted version.