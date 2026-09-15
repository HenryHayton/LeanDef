## Object

`VTask.apply 𝕜 E F m` is the **evaluation-at-a-point** map for continuous multilinear maps: it takes a fixed tuple of vectors `m = (m i)_{i ∈ ι}` (one vector from each factor space `E i`) and packages the operation "evaluate this continuous multilinear map at `m`" as a continuous linear map from `ContinuousMultilinearMap 𝕜 E F` to `F`. In other words, it is the canonical linear functional that sends a continuous multilinear map `c` to the value `c m`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.apply : (𝕜 : Type u_1) -> {ι : Type u_2} -> (E : ι → Type u_3) -> (F : Type u_4) -> [NormedField 𝕜] -> [(i : ι) → TopologicalSpace (E i)] -> [(i : ι) → AddCommGroup (E i)] -> [(i : ι) → Module 𝕜 (E i)] -> [AddCommGroup F] -> [Module 𝕜 F] -> [TopologicalSpace F] -> [IsTopologicalAddGroup F] -> [∀ (i : ι), ContinuousSMul 𝕜 (E i)] -> [ContinuousConstSMul 𝕜 F] -> (m : (i : ι) → E i) -> ContinuousMultilinearMap 𝕜 E F →L[𝕜] F
<!-- PINNED-SIGNATURE:END -->


`VTask.apply (𝕜 : Type u_1) {ι : Type u_2} (E : ι → Type u_3) (F : Type u_4) ...`

The first explicit argument `𝕜` is the scalar field, which must be a normed field. The implicit argument `ι` is the index type parametrising the family of domain spaces. The argument `E` is the family of topological vector spaces over `𝕜` indexed by `ι`, each carrying its own topology, additive group structure, and `𝕜`-module structure (with the scalar multiplication being continuous). The argument `F` is the codomain topological vector space over `𝕜`, which must be a topological additive group and admit continuous constant scalar multiplication by `𝕜`. The final explicit argument `m` is the evaluation point: a dependent tuple selecting one element `m i` from each `E i`. The result is a continuous linear map from `ContinuousMultilinearMap 𝕜 E F` to `F`.

## Conventions

There are no declared junk-value or edge-case conventions for this definition: its inputs are always meaningful (even for empty index types or trivial spaces), and the continuous linear map returned is well-defined in all cases without any special sentinel behaviour.

## Worked examples

- Claim: For the real numbers with `ι = Fin 1`, `E = fun _ => ℝ`, `F = ℝ`, and `m = fun _ => 3`, the application map sends any continuous multilinear map `c` to `c (fun _ => 3)`.

- Claim: If `c` is the continuous multilinear map that multiplies all components together (e.g., over `Fin 2` with `E = fun _ => ℝ` and `F = ℝ`), then `VTask.apply ℝ (fun _ => ℝ) ℝ (fun _ => 2) c = c (fun _ => 2)`, i.e., the image of `c` under the evaluation map is `4`.

- Claim: `VTask.apply 𝕜 E F m` is linear in the continuous multilinear map argument: for any two continuous multilinear maps `c₁` and `c₂` and scalar `r`, `VTask.apply 𝕜 E F m (r • c₁ + c₂) = r • (c₁ m) + c₂ m`.

## Boundaries

- **Empty index type (`ι` empty):** When `ι` is empty, every family `E` is vacuous, and the unique evaluation point `m` is the empty tuple. The resulting continuous linear map is still well-defined, sending each continuous multilinear map to its value at the unique empty-tuple point.
- **Singleton index type:** For `ι = Fin 1`, the "multilinear" map reduces to a linear map, and `VTask.apply` is simply evaluation at the single vector `m ⟨0, _⟩`.
- **Trivial spaces:** If every `E i` or `F` is the zero module, the map is the zero continuous linear map, which is legitimate.
- **Continuity:** The continuous linear map is always continuous (by construction), regardless of the specific topology chosen, as long as the required typeclass hypotheses are satisfied.

## Not to be confused with

- `ContinuousMultilinearMap.toFun` or bare evaluation `c m`: those directly produce the value `c m ∈ F`, whereas `VTask.apply 𝕜 E F m` encapsulates evaluation as a *continuous linear map* in the `c` variable.
- `ContinuousLinearMap.apply` (or its multilinear analogue for a fixed map varying over points): that fixes the *map* and varies the *input point*, the opposite role from here where the *point* is fixed and the *map* varies.
- `MultilinearMap.toLinearMap` or related "currying" constructions: those change the multilinear structure by fixing some arguments, rather than constructing a linear functional on the space of all such maps.
