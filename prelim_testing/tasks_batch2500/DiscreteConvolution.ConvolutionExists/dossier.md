## Object

`VTask.ConvolutionExists L f g` is the proposition asserting that the discrete (additive) convolution of two functions `f : M → E` and `g : M → E'` with respect to a continuous bilinear map `L : E →ₗ[S] E' →ₗ[S] F` is well-defined at **every** point of the monoid `M`. Concretely, it means that for each `x : M`, the infinite sum `∑ y, L (f y) (g (y⁻¹ * x))` (or its additive analogue) converges in `F`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ConvolutionExists : {M : Type u_1} -> {S : Type u_2} -> {E : Type u_3} -> {E' : Type u_4} -> {F : Type u_6} -> [Monoid M] -> [CommSemiring S] -> [AddCommMonoid E] -> [AddCommMonoid E'] -> [AddCommMonoid F] -> [Module S E] -> [Module S E'] -> [Module S F] -> [TopologicalSpace F] -> (L : E →ₗ[S] E' →ₗ[S] F) -> (f : M → E) -> (g : M → E') -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.ConvolutionExists : {M : Type u_1} -> {S : Type u_2} -> {E : Type u_3} -> {E' : Type u_4} -> {F : Type u_6} -> [Monoid M] -> [CommSemiring S] -> [AddCommMonoid E] -> [AddCommMonoid E'] -> [AddCommMonoid F] -> [Module S E] -> [Module S E'] -> [Module S F] -> [TopologicalSpace F] -> (L : E →ₗ[S] E' →ₗ[S] F) -> (f : M → E) -> (g : M → E') -> Prop`

The implicit type arguments fix the monoid `M` over which convolution is performed, the scalar semiring `S`, the domain module `E` in which `f` takes values, the domain module `E'` in which `g` takes values, and the codomain module `F` in which the convolution output lives. The bilinear map `L` specifies how values of `f` and `g` are combined and determines the "multiplication" structure of the convolution. The function `f : M → E` is the first operand (left factor) of the convolution. The function `g : M → E'` is the second operand (right factor).

## Conventions

No junk-value or edge conventions have been declared for this definition: it is a `Prop` that is simply `True` or `False` depending on whether the relevant infinite sums all converge, and there are no designated fallback values to specify.

## Worked examples

- Claim: If `VTask.ConvolutionExists L f g` holds and `VTask.ConvolutionExists L f' g` holds, then `VTask.ConvolutionExists L (f + f') g` also holds (convolution existence is closed under addition of the left factor).

- Claim: If `VTask.ConvolutionExists L f g` holds and `VTask.ConvolutionExists L f g'` holds, then `VTask.ConvolutionExists L f (g + g')` also holds (convolution existence is closed under addition of the right factor).

- Claim: For any scalar `c : S`, if `VTask.ConvolutionExists L f g` holds, then the convolution of `c • f` with `g` at any point `x` equals `c • ((f ⋆[L] g) x)`, reflecting linearity in the left argument.

## Boundaries

- When `M` is a finite monoid, every pair of functions trivially satisfies `VTask.ConvolutionExists L f g` because each sum is finite and hence automatically convergent in any topological module.
- When the topology on `F` is discrete (or trivially convergent), convergence is automatic, so `VTask.ConvolutionExists L f g` holds for all `f`, `g`, and `L`.
- The proposition is over **all** points `x : M`; it is not enough for the sum to converge at a single point or almost everywhere — every point must be covered. The pointwise version `ConvolutionExistsAt` handles the single-point case.
- If `f` or `g` has finite support (is zero outside a finite subset of `M`), then `VTask.ConvolutionExists L f g` holds for any `L` because each individual sum reduces to a finite sum.

## Not to be confused with

- `ConvolutionExistsAt L f g x`: the pointwise version, asserting convergence only at a single point `x`; `VTask.ConvolutionExists` is the universal quantification of this over all `x`.
- The convolution function itself `f ⋆[L] g : M → F`: this is the function whose values are the convolution sums, defined when `ConvolutionExistsAt` holds at each relevant point; `VTask.ConvolutionExists` is the hypothesis guaranteeing that definition is valid everywhere.
- Continuous convolution (as on Lie groups or locally compact groups with a Haar measure): that is a different, measure-theoretic notion; `VTask.ConvolutionExists` concerns discrete summation over a monoid, not integration.