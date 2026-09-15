## Object

This is the canonical continuous linear equivalence between `PiLp p β` — the product of a family of topological modules equipped with the $L^p$ norm structure — and the ordinary dependent-function type `(i : ι) → β i` — the same product with its standard product topology. It witnesses that as topological $\mathbb{k}$-modules these two presentations of the same underlying product are homeomorphically and linearly isomorphic. The underlying linear map is the identity on elements; the equivalence merely changes the topological bookkeeping.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.continuousLinearEquiv : (p : ENNReal) -> (𝕜 : Type u_1) -> {ι : Type u_2} -> (β : ι → Type u_4) -> [Semiring 𝕜] -> [(i : ι) → AddCommGroup (β i)] -> [(i : ι) → Module 𝕜 (β i)] -> [(i : ι) → TopologicalSpace (β i)] -> PiLp p β ≃L[𝕜] (i : ι) → β i
<!-- PINNED-SIGNATURE:END -->


`VTask.continuousLinearEquiv : (p : ENNReal) -> (𝕜 : Type u_1) -> {ι : Type u_2} -> (β : ι → Type u_4) -> [Semiring 𝕜] -> [(i : ι) → AddCommGroup (β i)] -> [(i : ι) → Module 𝕜 (β i)] -> [(i : ι) → TopologicalSpace (β i)] -> PiLp p β ≃L[𝕜] (i : ι) → β i`

The first argument `p` is the extended non-negative real exponent that parametrises the $L^p$-norm weighting on the product; any value in `ENNReal` is accepted. The second argument `𝕜` is the scalar semiring over which all modules in the family are defined. The implicit argument `ι` is the index type of the family. The argument `β` is the family of types, assigning to each index `i : ι` a type `β i`. The instance arguments supply, in order: the semiring structure on `𝕜`; additive abelian group structures on each fibre `β i`; module structures over `𝕜` on each fibre; and a topological space structure on each fibre. Together these instances endow both the source `PiLp p β` and the target `(i : ι) → β i` with the structures needed to speak of continuous linear maps.

## Conventions

No junk-value or edge-case conventions are declared for this definition. Because it is a construction (not a partial function returning a number or element), every combination of inputs that satisfies the typeclass constraints yields a well-formed continuous linear equivalence; there are no degenerate outputs to assign sentinel values to.

## Worked examples

- Claim: For `p = 2`, `𝕜 = ℝ`, and a constant family `β _ = ℝ` over `Fin 3`, the forward direction of `VTask.continuousLinearEquiv 2 ℝ (fun _ : Fin 3 => ℝ)` applied to an element `x : PiLp 2 (fun _ : Fin 3 => ℝ)` equals `WithLp.equiv 2 _ x`.

- Claim: The inverse of `VTask.continuousLinearEquiv p 𝕜 β` is itself a continuous linear map, and composing the forward and inverse maps gives the identity on `(i : ι) → β i`.

- Claim: The underlying `LinearEquiv` of `VTask.continuousLinearEquiv p 𝕜 β` coincides with the canonical linear equivalence `WithLp.linearEquiv p 𝕜 β` between `PiLp p β` and `(i : ι) → β i`.

## Boundaries

- When `ι` is the empty type, the equivalence still holds: both sides are the trivially-pointed one-element type, and the equivalence is the unique map between them.
- When `ι` is a `Fintype` and each `β i` is finite-dimensional, the topology on `PiLp p β` does not depend on `p` (all norms on a finite-dimensional space are equivalent), so `VTask.continuousLinearEquiv` is an equivalence for every `p`.
- The value `p = 0` or `p = ∞` (`⊤`) is admitted; the definition places no restriction on `p` beyond it belonging to `ENNReal`.
- The index type `ι` need not be finite; the equivalence is stated and holds in full generality over arbitrary `ι`.

## Not to be confused with

- `WithLp.linearEquiv`: the purely algebraic linear equivalence between `PiLp p β` and `(i : ι) → β i`, without any topological/continuity data; `VTask.continuousLinearEquiv` extends this with continuity of both directions.
- `PiLp.equiv`: the bare type equivalence (or `Equiv`) between `PiLp p β` and `(i : ι) → β i`, which carries neither algebraic nor topological structure.
- `LinearEquiv.toContinuousLinearEquiv`: a general construction that promotes a `LinearEquiv` to a `ContinuousLinearEquiv` under appropriate hypotheses; `VTask.continuousLinearEquiv` is a specific instance in the `PiLp` setting.