## Object

`VTask.prod f g` computes the finite product of terms `g i (f i)` as `i` ranges over the **support** of the finitely-supported function `f` — that is, the finite set of indices where `f` takes a nonzero value. The result lives in a commutative monoid `γ`. Because `f` is finitely supported (a `DFinsupp`), this product is always a finite, well-defined element of `γ`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {ι : Type u} -> {γ : Type w} -> {β : ι → Type v} -> [DecidableEq ι] -> [(i : ι) → Zero (β i)] -> [(i : ι) → (x : β i) → Decidable (x ≠ 0)] -> [CommMonoid γ] -> (f : Π₀ (i : ι), β i) -> (g : (i : ι) → β i → γ) -> γ
<!-- PINNED-SIGNATURE:END -->


VTask.prod : {ι : Type u} -> {γ : Type w} -> {β : ι → Type v} -> [DecidableEq ι] -> [(i : ι) → Zero (β i)] -> [(i : ι) → (x : β i) → Decidable (x ≠ 0)] -> [CommMonoid γ] -> (f : Π₀ (i : ι), β i) -> (g : (i : ι) → β i → γ) -> γ

- `ι` is the index type over which `f` is defined.
- `γ` is the commutative monoid in which the product is computed.
- `β` is the family of types giving the value type at each index `i`.
- The `DecidableEq ι` instance is needed to work with finite sets of indices.
- The `Zero (β i)` instances supply the zero element used to identify the support.
- The `Decidable (x ≠ 0)` instances allow constructively deciding which indices lie in the support.
- The `CommMonoid γ` instance provides the multiplication and identity for forming the product.
- `f` is the finitely-supported function whose nonzero-index set (support) determines the range of the product.
- `g` is the function applied at each index: given an index `i` and a value `b : β i`, it produces a factor in `γ`.

## Conventions

Indices outside the support of `f` do not contribute to the product; the product is taken only over `f.support`. When `f` is the zero function (empty support), the product is the identity element `1` of `γ` (empty product convention). If `g i 0 = 1` holds for every `i`, extending the product to any superset of the support gives the same result.

## Worked examples

- Claim: For the zero DFinsupp, `VTask.prod 0 g = 1` for any `g`.

- Claim: For a DFinsupp `f = single i b` supported at a single index `i` with value `b`, and a function `g` satisfying `g i 0 = 1`, `VTask.prod (single i b) g = g i b`.

- Claim: If `h₁` and `h₂` are two functions into a commutative monoid, then `VTask.prod f (fun i b => h₁ i b * h₂ i b) = VTask.prod f h₁ * VTask.prod f h₂`.

- Claim: When `ι` is a `Fintype` and `g i 0 = 1` for every `i`, `VTask.prod f g = ∏ i, g i (f i)` (the product over all indices equals the product over the support).

## Boundaries

- **Zero function**: When `f = 0`, its support is empty, so `VTask.prod f g = 1` regardless of `g`.
- **Single-index support**: When `f = single i b` and `g i 0 = 1`, the product collapses to the single term `g i b`.
- **Negation**: For `f` valued in an `AddGroup`, `VTask.prod (-f) h = VTask.prod f (fun i b => h i (-b))`, provided `h i 0 = 1`.
- **Constant-one kernel**: If `g` maps every `(i, f i)` to `1`, the product is `1`.
- **Support enlargement**: The product can be extended to any finite set containing the support without changing the result, as long as `g i 0 = 1` on the extra indices.

## Not to be confused with

- `DFinsupp.sum`: The additive analogue, summing `g i (f i)` over the support; `VTask.prod` is the multiplicative version.
- `Finsupp.prod`: The same construction for `Finsupp` (finitely-supported functions into a single fixed codomain type with zero), rather than the dependent family setting of `DFinsupp`.
- `∏ i, g i (f i)` (a plain `Finset.prod` over all of `ι`): This agrees with `VTask.prod` only when `ι` is finite and `g i 0 = 1`, not in general.