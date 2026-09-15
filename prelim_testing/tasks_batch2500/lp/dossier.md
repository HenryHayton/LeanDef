## VTask.lp

### Object

The **little ℓᵖ space** is the collection of all functions `f : Π i, E i` (indexed over a type `α`, with each fibre `E i` a normed abelian group) whose **p-norm is finite** — i.e., for which the membership condition `Memℓp f p` holds. This collection is presented as an **additive subgroup** of the ambient product type (wrapped in the `PreLp` type synonym), inheriting pointwise addition and negation. For concrete choices of `p` this recovers the classical spaces: `p = 2` gives the Hilbert space of square-summable sequences, `p = 1` the space of absolutely summable sequences, `p = ∞` the space of bounded sequences, and `p = 0` the space of functions with finite (discrete) support.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lp : {α : Type u_3} -> (E : α → Type u_5) -> [(i : α) → NormedAddCommGroup (E i)] -> (p : ENNReal) -> AddSubgroup (PreLp E)
<!-- PINNED-SIGNATURE:END -->


`VTask.lp : {α : Type u_3} -> (E : α → Type u_5) -> [(i : α) → NormedAddCommGroup (E i)] -> (p : ENNReal) -> AddSubgroup (PreLp E)`

The implicit argument `α` is the index type over which the family of spaces is indexed. The argument `E` is the family of normed abelian groups, assigning to each index `i : α` the fibre space `E i`. The typeclass argument equips each fibre `E i` with its normed abelian group structure. The argument `p` is the integrability exponent, a value in the extended non-negative reals `[0, ∞]`, which determines which summability condition is imposed on a function to qualify for membership.

### Conventions

All elements of `VTask.lp E p` are represented as elements of `PreLp E` (the plain product type `Π i, E i` under a type synonym); the subgroup structure on `PreLp E` is inherited pointwise. There are no junk-value conventions needed since the definition is total: every choice of `α`, `E`, and `p` yields a well-defined additive subgroup (possibly containing only the zero function when the condition is very restrictive, but always at least that).

### Worked examples

- Claim: The zero function belongs to `VTask.lp E p` for any family `E` and any exponent `p`, since a function that is zero everywhere has finite p-norm regardless of `p`.

- Claim: For `α = ℕ`, `E i = ℝ` for all `i`, and `p = 2`, the function `f n = 1 / (n + 1 : ℝ)` belongs to `VTask.lp E 2` because the series `Σ 1/(n+1)²` converges.

- Claim: For `α = ℕ`, `E i = ℝ` for all `i`, and `p = 1`, the constant function `f n = 1` does **not** belong to `VTask.lp E 1` because `Σ 1` diverges.

- Claim: If `f` and `g` both belong to `VTask.lp E p`, then so does `f + g`, by the subgroup closure property.

- Claim: For `p = ∞`, a function `f : Π i, E i` belongs to `VTask.lp E ∞` if and only if it is bounded, i.e., `⨆ i, ‖f i‖ < ∞`.

### Boundaries

- **`p = 0`**: Membership requires the function to have **finite support** (only finitely many indices where `f i ≠ 0`). This is a strictly algebraic condition with no norm summability required.
- **`p = ∞`**: Membership requires the function to be **essentially bounded**: the supremum of the norms `‖f i‖` over all `i` must be finite.
- **`p = 1`**: Membership requires absolute summability: `Σ ‖f i‖ < ∞`.
- **`p = 2`**: Membership requires square-summability: `Σ ‖f i‖² < ∞`.
- **Monotonicity in `p`**: If `p ≤ q` and the index type is finite, inclusion may go in either direction depending on context; for infinite index types over ℝ, `ℓᵖ ⊆ ℓ^q` for `p ≤ q`.
- **Finite index type `α`**: When `α` is a `Fintype`, every function `f : Π i, E i` satisfies `Memℓp f p` for all `p`, so `VTask.lp E p` equals the entire `PreLp E` in this case.
- The subgroup always contains at least the zero function, since zero has finite p-norm for every `p`.

### Not to be confused with

- **`MeasureTheory.Lp`**: The Lebesgue `Lᵖ` space of measurable functions on a measure space, defined up to almost-everywhere equality; `VTask.lp` is a purely algebraic/combinatorial construction on indexed families without a measure.
- **`Memℓp`**: The **predicate** asserting that a specific function belongs to the ℓᵖ space; `VTask.lp E p` is the **subgroup** whose carrier is exactly the set of functions satisfying `Memℓp f p`.
- **`PreLp E`**: The bare type synonym for the product `Π i, E i` used as the ambient group; `VTask.lp E p` is a proper **subgroup** of `PreLp E`, not the whole space.
