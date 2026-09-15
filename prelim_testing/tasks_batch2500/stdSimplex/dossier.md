## Object

The standard simplex (over an index type `ι` and a coefficient semiring `𝕜` with a compatible partial order) is the subset of the function space `ι → 𝕜` consisting of all functions whose values are everywhere non-negative and sum (over the finite index set `ι`) to exactly `1`. Geometrically, when `𝕜 = ℝ` and `ι = Fin (n+1)`, this is the usual convex hull of the standard basis vectors in `ℝ^{n+1}`, i.e., the classical `n`-dimensional simplex embedded in `(n+1)`-dimensional space. It is the free object in the category of convex spaces.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.stdSimplex : (𝕜 : Type u_2) -> (ι : Type u_1) -> [Semiring 𝕜] -> [PartialOrder 𝕜] -> [Fintype ι] -> Set (ι → 𝕜)
<!-- PINNED-SIGNATURE:END -->


VTask.stdSimplex : (𝕜 : Type u_2) -> (ι : Type u_1) -> [Semiring 𝕜] -> [PartialOrder 𝕜] -> [Fintype ι] -> Set (ι → 𝕜)

The first explicit argument `𝕜` is the type of coefficients, which must carry a semiring structure and a compatible partial order (so that non-negativity `0 ≤ f x` is meaningful and sums can be formed). The second explicit argument `ι` is the index type (the "vertices" of the simplex), which must be finite so that the sum `∑ x, f x` is well-defined. The instance arguments supply the semiring, partial-order, and finiteness structures needed to state the two defining conditions.

## Conventions

There are no declared junk-value or edge-case conventions specific to this definition; the set is well-defined for every valid combination of `𝕜` and `ι` satisfying the type-class constraints, including degenerate cases such as a one-element index type.

## Worked examples

- Claim: For `ι = Fin 1` (a one-element index type) and `𝕜 = ℝ`, the unique element is the constant function sending `0` to `1`.

- Claim: The function `Pi.single i 1 : ι → ℝ` (which is `1` at index `i` and `0` elsewhere) belongs to `VTask.stdSimplex ℝ ι` for any `i : ι`.

- Claim: For `𝕜 = ℝ` and `ι = Fin 2`, the midpoint function `fun _ => (1/2 : ℝ)` belongs to `VTask.stdSimplex ℝ (Fin 2)`, since both coordinates are non-negative and their sum is `1`.

- Claim: For `𝕜 = ℝ` and `ι = Fin 2`, the segment connecting `Pi.single 0 1` and `Pi.single 1 1` is contained in `VTask.stdSimplex ℝ (Fin 2)`, reflecting that the simplex is convex.

## Boundaries

- When `ι` is a one-element type (e.g., `Fin 1`), the simplex is a single point: the unique function with value `1` at the sole index. The simplex is zero-dimensional.
- When `ι` is empty (a `Fintype` with zero elements), the sum `∑ x, f x` is the empty sum, which equals `0` in any `AddCommMonoid`. Since `0 ≠ 1` in a nontrivial semiring, the simplex is empty; in a trivial semiring where `0 = 1`, every function satisfies both conditions.
- The definition requires only a `Semiring` and `PartialOrder`; no `LinearOrder`, `Field`, or `TopologicalSpace` is assumed at definition time, making the set meaningful in purely algebraic settings.
- Convexity and compactness of the set require additional structure (an `OrderedSemiring` or a topological space) and are stated as separate lemmas rather than being built into the definition.

## Not to be confused with

- The *simplicial* standard simplex `Δ[n]` (a simplicial set / presheaf on `SimplexCategory`): that is a combinatorial/categorical object, not a subset of a function space with real-valued coordinates.
- The *convex hull* of the standard basis vectors, which is a description of the same set over `ℝ` but is expressed differently in Mathlib and may carry additional convex-set structure.
- A *probability simplex*: informally the same, but in Mathlib that informal name refers to this same object restricted to `𝕜 = ℝ≥0` or `𝕜 = ℝ`; the definition here is more general and works over any ordered semiring.