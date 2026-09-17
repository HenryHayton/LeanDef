## Object

Given two dilations — `f : α →ᵈ β` and `g : β →ᵈ γ` — their composition `VTask.comp g f` is the dilation `α →ᵈ γ` whose underlying map is the ordinary function composition `g ∘ f`. A *dilation* between pseudo-extended-metric spaces is a map that scales every pairwise extended distance by a fixed non-negative constant (its *ratio*); the composition of two such maps is again a dilation, and its ratio is the product of the individual ratios.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> [PseudoEMetricSpace α] -> [PseudoEMetricSpace β] -> [PseudoEMetricSpace γ] -> (g : β →ᵈ γ) -> (f : α →ᵈ β) -> α →ᵈ γ
<!-- PINNED-SIGNATURE:END -->


{α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> [PseudoEMetricSpace α] -> [PseudoEMetricSpace β] -> [PseudoEMetricSpace γ] -> (g : β →ᵈ γ) -> (f : α →ᵈ β) -> α →ᵈ γ

The three type parameters `α`, `β`, `γ` are the source, intermediate, and target pseudo-extended-metric spaces respectively; they are inferred implicitly. The three instance arguments supply the pseudo-extended-metric structure on each space. The argument `g` is the outer dilation (from the intermediate space to the target), and `f` is the inner dilation (from the source to the intermediate space). The result is their composite dilation from `α` to `γ`.

## Conventions

The ratio of the composed dilation equals the product `ratio g * ratio f` of the two individual ratios. Both `ratio g` and `ratio f` are required to be non-zero (an invariant maintained by the `Dilation` type), so the product ratio is also non-zero.

## Worked examples

- Claim: The underlying function of `VTask.comp g f` at any point `x : α` equals `g (f x)`.

- Claim: If `f` is the identity dilation on a pseudo-emetric space `α` (with ratio 1) and `g : α →ᵈ β` has ratio `r`, then `VTask.comp g f` has ratio `r * 1 = r`.

- Claim: For any three dilations `h : γ →ᵈ δ`, `g : β →ᵈ γ`, `f : α →ᵈ β`, the ratio of `VTask.comp (VTask.comp h g) f` equals the ratio of `VTask.comp h (VTask.comp g f)`, since both equal `ratio h * ratio g * ratio f` (multiplication in `ℝ≥0` is associative).

- Claim: For any dilations `g : β →ᵈ γ` and `f : α →ᵈ β` and points `x y : α`, `edist ((VTask.comp g f) x) ((VTask.comp g f) y) = (ratio g * ratio f : ℝ≥0) • edist x y`.

## Boundaries

- The composition is defined for any two composable dilations, with no restriction beyond the type-compatibility of the spaces. There are no edge cases where the operation is undefined.
- When either ratio is 1 (an isometric embedding), the composed ratio remains equal to the other's ratio.
- The `Dilation` type enforces that ratios are non-zero, so the composed ratio `ratio g * ratio f` is automatically non-zero, keeping the result a valid dilation.
- The definition works for general pseudo-extended-metric spaces, including those where distinct points may have zero or infinite distance.

## Not to be confused with

- `Dilation.ratio` — the scalar factor attached to a single dilation, not the operation of combining two dilations.
- `IsometryEquiv.trans` — composition of isometric equivalences; isometries are dilations with ratio 1, so this is a special case of dilation composition but lives in a different type.
- Function.comp applied to the underlying functions — this forgets the dilation structure entirely and produces a bare function, not a bundled dilation with ratio information.