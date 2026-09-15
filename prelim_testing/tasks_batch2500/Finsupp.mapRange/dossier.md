## 1. Object

Given a function `f : M → N` between types carrying zero elements, and a finitely-supported function `g : α →₀ M`, `VTask.mapRange f hf g` is the finitely-supported function `α →₀ N` obtained by composing `f` with `g` pointwise. The result has finite support because `f` maps zero to zero (guaranteed by `hf`), so `f(g(a)) = 0` whenever `g(a) = 0`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapRange : {α : Type u_1} -> {M : Type u_4} -> {N : Type u_5} -> [Zero M] -> [Zero N] -> (f : M → N) -> (hf : f 0 = 0) -> (g : α →₀ M) -> α →₀ N
<!-- PINNED-SIGNATURE:END -->


The first argument `f` is the function to apply to every value in the range of `g`. The second argument `hf` is a proof that `f` sends zero to zero, which ensures the composition remains finitely supported. The third argument `g` is the finitely-supported function whose values are being transformed.

## 3. Conventions

The support of the result is contained in the support of `g`; when `f` is injective, the support of the result equals the support of `g` exactly. When `f` is the identity, `VTask.mapRange f hf g` equals `g` unchanged.

## 4. Worked examples

- Claim: For the zero finitely-supported function on any index type, `VTask.mapRange f hf 0 = 0` for any zero-preserving `f`.

- Claim: If `g : Fin 3 →₀ ℤ` is the finitely-supported function with `g 0 = 2`, `g 1 = -1`, `g 2 = 0`, then `VTask.mapRange (· * 2) (by norm_num) g` is the finitely-supported function with values `4`, `-2`, `0` at indices `0`, `1`, `2` respectively.

- Claim: If `e : M → N` is bijective with `e 0 = 0`, then `VTask.mapRange e he` is injective as a map from `α →₀ M` to `α →₀ N`.

- Claim: Composing two `VTask.mapRange` calls with zero-preserving `f` and `h` in sequence is the same as applying `VTask.mapRange (h ∘ f) _` in one step.

## 5. Boundaries

- When `g` is the zero finitely-supported function (empty support), the result is also the zero finitely-supported function regardless of `f`, since there are no nonzero values to transform.
- The hypothesis `hf : f 0 = 0` is essential; without it, the image of `g` under `f` might assign nonzero values at all of `α`, making finite support impossible to guarantee.
- The support of `VTask.mapRange f hf g` is always a subset of the support of `g`. It equals the support of `g` exactly when `f` is injective (since then `f(g(a)) ≠ 0` iff `g(a) ≠ 0`).
- When `f` is surjective, `VTask.mapRange f hf` is surjective as a map on finitely-supported functions.

## 6. Not to be confused with

- `Finsupp.mapDomain`: transforms the *index type* `α` rather than the *value type* `M`; here we transform values, not indices.
- `Finsupp.comapDomain`: pulls back along a function on the domain `α`, changing which indices are used, not their associated values.
- Pointwise scalar multiplication or addition of finitely-supported functions: those combine two finsupp values, whereas `VTask.mapRange` applies a single unary function to the values of one finsupp.