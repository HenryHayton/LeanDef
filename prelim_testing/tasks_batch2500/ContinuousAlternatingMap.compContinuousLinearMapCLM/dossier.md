## Object

Given a continuous linear map `f : E →L[𝕜] E'` between topological vector spaces over a normed field `𝕜`, `VTask.compContinuousLinearMapCLM f` is the operation of **pre-composing** a continuous alternating multilinear map `g : E' [⋀^ι]→L[𝕜] F` with `f` in each argument slot, yielding a new continuous alternating map `g ∘ (f, …, f) : E [⋀^ι]→L[𝕜] F`. This assignment `g ↦ g ∘ (f, …, f)` is itself continuous and linear in `g`, so the whole construction is packaged as a **bundled continuous linear map** from the space of continuous alternating maps on `E'` to the space of continuous alternating maps on `E`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compContinuousLinearMapCLM : {𝕜 : Type u_1} -> {E : Type u_2} -> {F : Type u_3} -> {ι : Type u_4} -> [NormedField 𝕜] -> [AddCommGroup E] -> [Module 𝕜 E] -> [TopologicalSpace E] -> [AddCommGroup F] -> [Module 𝕜 F] -> [TopologicalSpace F] -> [IsTopologicalAddGroup F] -> [ContinuousConstSMul 𝕜 F] -> {E' : Type u_6} -> [AddCommGroup E'] -> [Module 𝕜 E'] -> [TopologicalSpace E'] -> (f : E →L[𝕜] E') -> E' [⋀^ι]→L[𝕜] F →L[𝕜] E [⋀^ι]→L[𝕜] F
<!-- PINNED-SIGNATURE:END -->


The scalar field over which all spaces are modules and continuity is measured. The domain space whose elements will be fed into the resulting alternating maps. The codomain space into which the given continuous linear map `f` maps, and from which the original alternating maps take their inputs. The index type parametrising the arity of the alternating maps. The target space into which all alternating maps take values. All type-class arguments supply the relevant normed-field, module, topological-space, topological-group, and scalar-continuity structures on these types.

The sole explicit argument, `f`, is the continuous linear map `E →L[𝕜] E'` used for pre-composition: each input alternating map `g : E' [⋀^ι]→L[𝕜] F` is mapped to the alternating map that first applies `f` to each of its `ι`-many arguments and then applies `g`. The output is a continuous linear map from `E' [⋀^ι]→L[𝕜] F` to `E [⋀^ι]→L[𝕜] F`.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a totally defined construction on well-typed inputs with no degenerate special cases requiring a sentinel value.

## Worked examples

- Claim: When `f` is the identity continuous linear map `id : E →L[𝕜] E`, `VTask.compContinuousLinearMapCLM (ContinuousLinearMap.id 𝕜 E)` acts as the identity on `E [⋀^ι]→L[𝕜] F`, sending each `g` to itself.

- Claim: For two continuous linear maps `f₁ : E →L[𝕜] E'` and `f₂ : E₀ →L[𝕜] E`, `VTask.compContinuousLinearMapCLM (f₁.comp f₂)` equals the composition of `VTask.compContinuousLinearMapCLM f₂` after `VTask.compContinuousLinearMapCLM f₁` as continuous linear maps on alternating maps (i.e., pre-composition is contravariantly functorial).

- Claim: For any scalar `c : 𝕜` and continuous alternating map `g : E' [⋀^ι]→L[𝕜] F`, `VTask.compContinuousLinearMapCLM f (c • g)` equals `c • VTask.compContinuousLinearMapCLM f g`, reflecting the linearity of `VTask.compContinuousLinearMapCLM f` in its argument.

## Boundaries

- When `ι` is the empty type, the alternating maps degenerate to constant maps (elements of `F`), and pre-composition with `f` leaves them unchanged; `VTask.compContinuousLinearMapCLM f` is the identity in this degenerate arity.
- When `f` is the zero map, every alternating map in the image of `VTask.compContinuousLinearMapCLM f` is identically zero, because all arguments are sent to zero before being fed into the original map.
- The docstring notes that, for **general** topological vector spaces, `VTask.compContinuousLinearMapCLM` is not required to be continuous as a function of `f` itself; continuity is only guaranteed in the argument `g`.
- The construction is well-defined regardless of the cardinality of `ι`; for finite `ι` of size `n` this gives the familiar alternating `n`-linear case, but `ι` can be any type.

## Not to be confused with

- `ContinuousAlternatingMap.compContinuousLinearMap` (the unbundled version): this sends `(g, f)` to the pre-composed alternating map but does **not** package the assignment as a continuous linear map in `g`.
- `ContinuousMultilinearMap.compContinuousLinearMapL`: the analogous construction for **multilinear** (not necessarily alternating) maps; alternating maps are a special case but the two spaces differ.
- `ContinuousLinearMap.comp`: composition of two continuous linear maps between normed spaces, which has the opposite variance and operates in the category of linear maps rather than alternating maps.