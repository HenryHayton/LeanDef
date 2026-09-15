## Object

The operator norm of a continuous multilinear map `f : ContinuousMultilinearMap 𝕜 E G` is the smallest non-negative real number `C` such that `‖f m‖ ≤ C * ∏ i, ‖m i‖` holds for every tuple of inputs `m`. Equivalently, it is the infimum of all non-negative "Lipschitz-style" bounds on `f` with respect to the product of individual norms of the input components. It generalises the classical operator norm from linear maps to maps that are multilinear (linear in each argument separately) and automatically assigns the right value that makes `ContinuousMultilinearMap` into a normed space.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.opNorm : {𝕜 : Type u} -> {ι : Type v} -> {E : ι → Type wE} -> {G : Type wG} -> [NontriviallyNormedField 𝕜] -> [(i : ι) → SeminormedAddCommGroup (E i)] -> [(i : ι) → NormedSpace 𝕜 (E i)] -> [SeminormedAddCommGroup G] -> [NormedSpace 𝕜 G] -> [Fintype ι] -> (f : ContinuousMultilinearMap 𝕜 E G) -> ℝ
<!-- PINNED-SIGNATURE:END -->


VTask.opNorm : {𝕜 : Type u} -> {ι : Type v} -> {E : ι → Type wE} -> {G : Type wG} -> [NontriviallyNormedField 𝕜] -> [(i : ι) → SeminormedAddCommGroup (E i)] -> [(i : ι) → NormedSpace 𝕜 (E i)] -> [SeminormedAddCommGroup G] -> [NormedSpace 𝕜 G] -> [Fintype ι] -> (f : ContinuousMultilinearMap 𝕜 E G) -> ℝ

The scalar field `𝕜` must be a nontrivially normed field (e.g. `ℝ` or `ℂ`). The index type `ι` must be finite; it parametrises how many arguments `f` takes. The family `E` assigns a seminormed `𝕜`-module to each index, forming the domain components. `G` is the seminormed `𝕜`-module that is the codomain. The sole explicit argument `f` is the continuous multilinear map whose operator norm is being computed; the result is a real number.

## Conventions

The operator norm is always non-negative: `VTask.opNorm f ≥ 0` for every `f`, even though the infimum is taken over a set that could in principle be empty; continuity of `f` guarantees the set is non-empty and bounded below by 0. The operator norm of the zero map is exactly 0. The operator norm satisfies the norm axioms (nonnegativity, zero-iff condition, triangle inequality, and sub-multiplicativity with scalars), making it the canonical norm on the space of continuous multilinear maps.

## Worked examples

- Claim: For the zero continuous multilinear map, `VTask.opNorm 0 = 0`. This is an instance of `opNorm_zero`: the set of bounds for the zero map contains every non-negative real, and its infimum is 0.

- Claim: For any `f` and any tuple `m`, we have `‖f m‖ ≤ VTask.opNorm f * ∏ i, ‖m i‖`. This is the fundamental bound that the operator norm certifies; it states that `VTask.opNorm f` is indeed a member of the bounding set.

- Claim: `VTask.opNorm f` is the least element of the set `{c : ℝ | 0 ≤ c ∧ ∀ m, ‖f m‖ ≤ c * ∏ i, ‖m i‖}`, i.e., it is not merely a lower bound but actually belongs to this set and is smaller than every other member.

- Claim: For any `f` and `g`, `VTask.opNorm (f + g) ≤ VTask.opNorm f + VTask.opNorm g` (triangle inequality for the operator norm).

## Boundaries

- When `ι` is empty (i.e. `Fintype.card ι = 0`), the product `∏ i, ‖m i‖` equals 1 (empty product), so the bound condition reduces to `‖f m‖ ≤ c` for the unique input `m`. The operator norm then equals `‖f m‖` for that unique `m`.
- When `f = 0`, the operator norm is exactly 0, and the converse also holds: `VTask.opNorm f = 0` if and only if `f = 0`.
- The operator norm is always non-negative regardless of `f`; it is never negative.
- If all component norms `‖m i‖ = 0` for some `i`, the product bound forces `‖f m‖ = 0` automatically without constraining the norm; the operator norm is still well-defined.

## Not to be confused with

- The operator norm of a *linear* map (`NNNorm` / `‖·‖` on `ContinuousLinearMap`): that is a special case with a single argument, whereas this definition handles maps with finitely many arguments simultaneously.
- `ContinuousMultilinearMap.nnnorm`: the non-negative real (`ℝ≥0`) version of the same quantity; it carries the same information but in a different type.
- The sup-norm or pointwise norm on the function itself: the operator norm is not the supremum of `‖f m‖` over the unit ball in any single `E i`, but rather the infimum of constants bounding `‖f m‖` relative to the product of all component norms.