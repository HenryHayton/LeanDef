## Object

`VTask.comp` is the composition operation for continuous linear maps between topological modules, where both the domain, codomain, and intermediate space are equipped with the **weak operator topology (WOT)** type synonym. Given a continuous σ₂₃-linear map `g : F →SWOT[σ₂₃] G` and a continuous σ₁₂-linear map `f : E →SWOT[σ₁₂] F`, it produces the composite continuous σ₁₃-linear map `g ∘ f : E →SWOT[σ₁₃] G`, viewed through the same WOT type synonym. The scalar-field ring homomorphisms are required to compose compatibly: σ₁₂ followed by σ₂₃ equals σ₁₃.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {𝕜₁ : Type u_5} -> {𝕜₂ : Type u_6} -> {𝕜₃ : Type u_7} -> {E : Type u_9} -> {F : Type u_10} -> {G : Type u_11} -> [NormedField 𝕜₁] -> [NormedField 𝕜₂] -> [NormedField 𝕜₃] -> {σ₁₂ : 𝕜₁ →+* 𝕜₂} -> {σ₁₃ : 𝕜₁ →+* 𝕜₃} -> {σ₂₃ : 𝕜₂ →+* 𝕜₃} -> [RingHomCompTriple σ₁₂ σ₂₃ σ₁₃] -> [AddCommGroup E] -> [TopologicalSpace E] -> [Module 𝕜₁ E] -> [AddCommGroup F] -> [TopologicalSpace F] -> [Module 𝕜₂ F] -> [AddCommGroup G] -> [TopologicalSpace G] -> [Module 𝕜₃ G] -> (g : F →SWOT[σ₂₃] G) -> (f : E →SWOT[σ₁₂] F) -> E →SWOT[σ₁₃] G
<!-- PINNED-SIGNATURE:END -->


`VTask.comp : {𝕜₁ : Type u_5} -> {𝕜₂ : Type u_6} -> {𝕜₃ : Type u_7} -> {E : Type u_9} -> {F : Type u_10} -> {G : Type u_11} -> [NormedField 𝕜₁] -> [NormedField 𝕜₂] -> [NormedField 𝕜₃] -> {σ₁₂ : 𝕜₁ →+* 𝕜₂} -> {σ₁₃ : 𝕜₁ →+* 𝕜₃} -> {σ₂₃ : 𝕜₂ →+* 𝕜₃} -> [RingHomCompTriple σ₁₂ σ₂₃ σ₁₃] -> [AddCommGroup E] -> [TopologicalSpace E] -> [Module 𝕜₁ E] -> [AddCommGroup F] -> [TopologicalSpace F] -> [Module 𝕜₂ F] -> [AddCommGroup G] -> [TopologicalSpace G] -> [Module 𝕜₃ G] -> (g : F →SWOT[σ₂₃] G) -> (f : E →SWOT[σ₁₂] F) -> E →SWOT[σ₁₃] G`

The implicit type arguments `𝕜₁`, `𝕜₂`, `𝕜₃` are the three (normed) scalar fields for the source, intermediate, and target modules. `E`, `F`, `G` are the source, intermediate, and target topological modules, carrying `AddCommGroup`, `TopologicalSpace`, and `Module` structures over their respective fields. The ring homomorphisms `σ₁₂ : 𝕜₁ →+* 𝕜₂`, `σ₂₃ : 𝕜₂ →+* 𝕜₃`, and `σ₁₃ : 𝕜₁ →+* 𝕜₃` are the scalar-field change-of-ring maps for `f`, `g`, and the composite, respectively. The `RingHomCompTriple` instance witnesses that σ₂₃ ∘ σ₁₂ = σ₁₃, ensuring the semilinar composites are coherent. The explicit argument `g` is the outer continuous linear map (from `F` to `G`), and `f` is the inner continuous linear map (from `E` to `F`); composition is applied in the standard mathematical order (right-to-left: `f` first, then `g`).

## Conventions

There are no junk-value or edge-case conventions to declare for this definition: it is a total, structurally well-typed operation whose behaviour is fully determined by the algebraic and topological structure of its inputs with no degenerate or undefined regimes.

## Worked examples

- Claim: For any `g : F →SWOT[σ₂₃] G`, `f : E →SWOT[σ₁₂] F`, and `x : E`, evaluating `VTask.comp g f` at `x` gives the same result as first applying `f` to `x` and then applying `g`.

- Claim: Composition is associative: for composable maps `g₃₄`, `g₂₃`, `g₁₂`, one has `(VTask.comp (VTask.comp g₃₄ g₂₃) g₁₂) = VTask.comp g₃₄ (VTask.comp g₂₃ g₁₂)`.

- Claim: Post-composition with a fixed bounded linear map `g` (when the relevant ring homomorphism is surjective and isometric) gives a continuous map `f ↦ VTask.comp g f` on the WOT space of maps from `E` to `F`.

- Claim: Pre-composition with a fixed bounded linear map `f` (when `G` is a topological additive group with continuous scalar multiplication) gives a continuous map `g ↦ VTask.comp g f` on the WOT space of maps from `F` to `G`.

## Boundaries

- When the three scalar fields coincide (`𝕜₁ = 𝕜₂ = 𝕜₃`) and all ring homomorphisms are the identity, `VTask.comp` specialises to composition of continuous linear maps over a single field, equipped with the WOT.
- In the endomorphism case `E = F = G` with a single field and the identity ring homomorphism, `VTask.comp` coincides with multiplication in the WOT algebra: `f * g = VTask.comp f g`.
- The output lives in the WOT type synonym `E →SWOT[σ₁₃] G`; in particular, the topology on the result is the weak operator topology, not the operator-norm topology, even though the underlying map is continuous and linear.
- There is no restriction on the norms or boundedness beyond what is already encoded in the type `→SWOT[...]`; the definition is total for all valid inputs.

## Not to be confused with

- `ContinuousLinearMap.comp`: composition of continuous linear maps with the operator-norm (strong) topology rather than the weak operator topology — the underlying map is the same, but the ambient topological type is different.
- `LinearMap.comp`: composition of bare (not necessarily continuous) linear maps, which carries neither operator-norm nor weak-operator topology structure.
- `VTask.mul` (multiplication in the WOT endomorphism algebra): coincides with `VTask.comp` for the square/endomorphism case, but is presented as ring multiplication rather than explicit function composition.