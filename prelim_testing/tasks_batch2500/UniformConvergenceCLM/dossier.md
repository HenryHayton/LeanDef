## Object

`VTask.UniformConvergenceCLM σ F 𝔖` is a type synonym for the space of continuous `σ`-semilinear maps from a topological vector space `E` to a topological vector space `F`, but equipped with the *topology of uniform convergence on the members of `𝔖`* rather than the default (operator-norm or pointwise) topology. Here `𝔖` is a prescribed family of subsets of `E`; convergence of a net of continuous linear maps in this topology means uniform convergence on each set belonging to `𝔖`. When every continuous linear image of a set in `𝔖` is bounded in `F`, this topology makes the synonym itself a topological vector space.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.UniformConvergenceCLM : {𝕜₁ : Type u_1} -> {𝕜₂ : Type u_2} -> [NormedField 𝕜₁] -> [NormedField 𝕜₂] -> (σ : 𝕜₁ →+* 𝕜₂) -> {E : Type u_3} -> (F : Type u_4) -> [AddCommGroup E] -> [Module 𝕜₁ E] -> [TopologicalSpace E] -> [AddCommGroup F] -> [Module 𝕜₂ F] -> [TopologicalSpace F] -> Set (Set E) → Type (max u_3 u_4)
<!-- PINNED-SIGNATURE:END -->


`VTask.UniformConvergenceCLM : {𝕜₁ : Type u_1} -> {𝕜₂ : Type u_2} -> [NormedField 𝕜₁] -> [NormedField 𝕜₂] -> (σ : 𝕜₁ →+* 𝕜₂) -> {E : Type u_3} -> (F : Type u_4) -> [AddCommGroup E] -> [Module 𝕜₁ E] -> [TopologicalSpace E] -> [AddCommGroup F] -> [Module 𝕜₂ F] -> [TopologicalSpace F] -> Set (Set E) → Type (max u_3 u_4)`

- `σ` is the ring homomorphism from the scalar field `𝕜₁` of `E` to the scalar field `𝕜₂` of `F`; it specifies the *semilinearity* of the maps being collected.
- `F` is the codomain topological vector space (over `𝕜₂`).
- The implicit argument `E` (inferred from context) is the domain topological vector space (over `𝕜₁`).
- The `NormedField` instances on `𝕜₁` and `𝕜₂`, the `AddCommGroup`/`Module`/`TopologicalSpace` instances on `E` and `F` supply the algebraic and topological structure needed to define continuous semilinear maps and the uniform-convergence topology.
- The final explicit argument `𝔖 : Set (Set E)` is the *family of subsets* of `E` on which uniform convergence is demanded; changing `𝔖` changes the topology placed on the synonym.

## Conventions

As a type synonym, `VTask.UniformConvergenceCLM σ F 𝔖` is definitionally equal to the type of continuous `σ`-semilinear maps `E →SL[σ] F`; every element is literally a continuous linear map, and the two types share the same underlying set. The topology is, however, distinct from any topology already registered on `E →SL[σ] F`: it is specifically the topology of uniform convergence on sets in `𝔖`, installed through the type-synonym mechanism so that the two topologies can coexist without conflict.

## Worked examples

- Claim: When `𝔖` is the family of all singletons `{{x} | x : E}`, the topology of `VTask.UniformConvergenceCLM σ F 𝔖` is the topology of pointwise (simple) convergence on `F`-valued continuous linear maps.

- Claim: When `𝔖` is the family of all bounded subsets of `E` (in an appropriate sense) and `𝕜₁ = 𝕜₂` with `σ = id`, the topology of `VTask.UniformConvergenceCLM σ F 𝔖` coincides with the topology of uniform convergence on bounded sets, which is the standard topology used on the space of continuous linear maps between Banach spaces.

- Claim: An element of `VTask.UniformConvergenceCLM σ F 𝔖` is exactly a continuous `σ`-semilinear map from `E` to `F`; the type synonym introduces no new algebraic constraints beyond those already present in `E →SL[σ] F`.

## Boundaries

- If `𝔖` is empty, the topology of uniform convergence on no sets is the indiscrete topology (every net converges to every point); the type synonym is still well-formed.
- If `𝔖` contains unbounded sets and the continuous linear images of those sets are themselves unbounded in `F`, the type synonym is still defined, but the resulting topology may fail to make it a topological vector space (the boundedness hypothesis on images is genuinely needed for that conclusion).
- The definition is total: it is well-formed for any choice of `σ`, `F`, and `𝔖`, regardless of whether the resulting topology is Hausdorff, metrizable, or locally convex.

## Not to be confused with

- `E →SL[σ] F` (continuous semilinear maps with the default topology): same underlying elements, but a potentially different topology; `VTask.UniformConvergenceCLM σ F 𝔖` is the type synonym that carries the `𝔖`-uniform topology.
- `E →L[𝕜] F` (continuous linear maps when `𝕜₁ = 𝕜₂` and `σ = id`): a special case of continuous semilinear maps; `VTask.UniformConvergenceCLM` applies to the more general semilinear setting.
- The uniform convergence topology on function spaces `E → F` (not restricted to linear maps): `VTask.UniformConvergenceCLM` specifically tracks *continuous linear* maps, not arbitrary functions.