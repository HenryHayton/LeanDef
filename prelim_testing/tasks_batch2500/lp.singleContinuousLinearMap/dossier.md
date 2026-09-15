## Object

`VTask.singleContinuousLinearMap` is the canonical continuous linear embedding of the fibre `E i` into the `lp`-space `lp E p`. Concretely, it sends a vector `x : E i` to the sequence that equals `x` at position `i` and is zero at every other index, and it does so continuously (in fact, isometrically). This is the continuous-linear-map version of the bare linear map `lp.single`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.singleContinuousLinearMap : (𝕜 : Type u_1) -> {α : Type u_3} -> (E : α → Type u_4) -> (p : ENNReal) -> [(i : α) → NormedAddCommGroup (E i)] -> [NormedRing 𝕜] -> [(i : α) → Module 𝕜 (E i)] -> [∀ (i : α), IsBoundedSMul 𝕜 (E i)] -> [DecidableEq α] -> [Fact (1 ≤ p)] -> (i : α) -> E i →L[𝕜] ↥(lp E p)
<!-- PINNED-SIGNATURE:END -->


`VTask.singleContinuousLinearMap : (𝕜 : Type u_1) -> {α : Type u_3} -> (E : α → Type u_4) -> (p : ENNReal) -> [(i : α) → NormedAddCommGroup (E i)] -> [NormedRing 𝕜] -> [(i : α) → Module 𝕜 (E i)] -> [∀ (i : α), IsBoundedSMul 𝕜 (E i)] -> [DecidableEq α] -> [Fact (1 ≤ p)] -> (i : α) -> E i →L[𝕜] ↥(lp E p)`

- `𝕜` is the scalar field (a normed ring) over which all modules are defined.
- `α` is the index type; the fibres of the family are indexed by it.
- `E` is the family of normed modules, one fibre per index in `α`.
- `p` is the integrability exponent (an extended non-negative real), required to satisfy `1 ≤ p`.
- The instance arguments supply normed group structures, module structures, bounded scalar-multiplication conditions, decidable equality on `α`, and the hypothesis `1 ≤ p`.
- `i` is the specific index in `α` whose fibre `E i` is to be embedded: the resulting map sends `E i` into `lp E p` via the single-nonzero-entry injection at position `i`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: the map is total and well-defined for every valid combination of inputs satisfying the stated type-class hypotheses.

## Worked examples

- Claim: Applying `VTask.singleContinuousLinearMap 𝕜 E p i` to a vector `x : E i` returns exactly `lp.single p i x` in `lp E p`.

- Claim: For the standard case `α = Fin 2`, `E = fun _ => ℝ`, `p = 2`, `i = 0`, and `x = 3`, the image under `VTask.singleContinuousLinearMap` is the sequence `(3, 0)` in `lp (fun _ : Fin 2 => ℝ) 2`.

- Claim: Two continuous linear maps `f g : lp E p →L[𝕜] F` (with `p ≠ ⊤`) are equal whenever `f.comp (VTask.singleContinuousLinearMap 𝕜 E p i) = g.comp (VTask.singleContinuousLinearMap 𝕜 E p i)` holds for every `i : α`.

- Claim: `VTask.singleContinuousLinearMap 𝕜 E p i` is an isometric embedding, so the operator norm of the map is at most 1 (in fact exactly 1 when `E i` is non-trivial).

## Boundaries

- The `Fact (1 ≤ p)` hypothesis is essential: the `lp E p` type requires it for the `p`-norm to be a genuine norm. Without this fact, the definition is not available.
- The case `p = ⊤` (the `ℓ∞` case) is included; `singleContinuousLinearMap` works for all `1 ≤ p ≤ ⊤`.
- When `α` is empty, the family has no fibres and no index `i` exists, so the map is vacuously present but never instantiated.
- The map is isometric (distance-preserving), so in particular it is injective and norm-preserving; it never collapses norms.

## Not to be confused with

- `lp.single`: the underlying bare additive/linear map without the continuity bundling; `VTask.singleContinuousLinearMap` wraps this with a proof of continuity.
- `lp.lsingle`: the bundled *linear* map (without the continuity/topological structure) from which `VTask.singleContinuousLinearMap` is constructed.
- The coordinate *projection* `lp E p → E i` (evaluation at `i`), which goes in the opposite direction.