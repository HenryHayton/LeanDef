## VTask.D

### Object

`VTask.D f K` is a subset of the domain space `E` constructed via countable intersections and unions of auxiliary "approximation" sets. Its fundamental significance is analytic: when `K` is a complete subset of the space of continuous linear maps from `E` to `F`, the set `VTask.D f K` coincides exactly with the set of points at which `f` is Fréchet differentiable and whose derivative lies in `K`. In other words, it is a Borel-measurable surrogate for the differentiability set of `f` relative to the constraint set `K`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.D : {𝕜 : Type u_1} -> [NontriviallyNormedField 𝕜] -> {E : Type u_2} -> [NormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> {F : Type u_3} -> [NormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> (f : E → F) -> (K : Set (E →L[𝕜] F)) -> Set E
<!-- PINNED-SIGNATURE:END -->


`{𝕜 : Type u_1} -> [NontriviallyNormedField 𝕜] -> {E : Type u_2} -> [NormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> {F : Type u_3} -> [NormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> (f : E → F) -> (K : Set (E →L[𝕜] F)) -> Set E`

The scalar field `𝕜` is a nontrivially normed field (e.g., `ℝ` or `ℂ`). The domain `E` and codomain `F` are normed vector spaces over `𝕜`. The argument `f` is the function whose differentiability is being analyzed. The argument `K` is the target set for the derivative: one asks not only whether `f` is differentiable at a point, but whether the derivative at that point belongs to `K`.

### Conventions

There are no declared junk-value or edge conventions for this definition: `VTask.D f K` is a well-defined set for every function `f` and every set `K` of continuous linear maps, without any preconditions. The completeness assumption on `K` is needed only for the equality `VTask.D f K = { x | DifferentiableAt 𝕜 f x ∧ fderiv 𝕜 f x ∈ K }` to hold; without it, one retains only the inclusion `{ x | DifferentiableAt 𝕜 f x ∧ fderiv 𝕜 f x ∈ K } ⊆ VTask.D f K`.

### Worked examples

- Claim: For any `f : E → F` and `K : Set (E →L[𝕜] F)`, the set of points where `f` is differentiable with derivative in `K` is always a subset of `VTask.D f K`, regardless of whether `K` is complete.

- Claim: When `K` is complete, `VTask.D f K` equals exactly `{ x | DifferentiableAt 𝕜 f x ∧ fderiv 𝕜 f x ∈ K }`, so membership in `VTask.D f K` is equivalent to differentiability of `f` at `x` with `fderiv 𝕜 f x ∈ K`.

- Claim: Taking `K` to be the entire space `Set.univ` of continuous linear maps (which is complete), `VTask.D f Set.univ` equals the set of all points where `f` is Fréchet differentiable.

- Claim: If `f` is nowhere differentiable, then `VTask.D f K` may still be nonempty for a non-complete `K`, since `VTask.D f K` can be larger than the actual differentiability set when `K` is not complete.

### Boundaries

- When `K` is empty, `VTask.D f K` is contained in the empty set of differentiability points with derivative in `K` (which is itself empty), but without completeness of `K` the equality is not guaranteed from the definition alone.
- When `K` is complete, the sets `VTask.D f K` and `{ x | DifferentiableAt 𝕜 f x ∧ fderiv 𝕜 f x ∈ K }` are exactly equal.
- When `K` is not complete, the inclusion `{ x | DifferentiableAt 𝕜 f x ∧ fderiv 𝕜 f x ∈ K } ⊆ VTask.D f K` still holds, but `VTask.D f K` may be strictly larger.
- The set `VTask.D f K` is always a Borel-measurable set (this is the key reason for its construction: to serve as a measurable representative of the differentiability set).

### Not to be confused with

- `FDerivMeasurableAux.A f L r ε`: an auxiliary open approximation set used in the construction of `VTask.D`; it captures points where `f` is well approximated by `L` on a ball of radius `r` with error `ε`, not the full differentiability set.
- `FDerivMeasurableAux.B f K r₁ r₂ ε`: another auxiliary set (an intermediate building block involving intersections over linear maps in `K`) from which `VTask.D f K` is assembled; not the differentiability set itself.
- `{ x | DifferentiableAt 𝕜 f x }`: the plain differentiability set of `f` (with no constraint on the derivative), obtained from `VTask.D f K` by taking `K = Set.univ` and assuming completeness.
