## Object

`VTask.prod f g` computes the product of the values `g a (f a)` as `a` ranges over every element in the (finite) support of `f` — that is, every `a` for which `f a ≠ 0`. Because `f` has finite support by definition, this is a genuine finite product in the commutative monoid `N`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {α : Type u_1} -> {M : Type u_8} -> {N : Type u_10} -> [Zero M] -> [CommMonoid N] -> (f : α →₀ M) -> (g : α → M → N) -> N
<!-- PINNED-SIGNATURE:END -->


The implicit type `α` is the index type; `M` is the coefficient type, which must carry a distinguished zero (so that "support" — the set of indices with non-zero values — is well-defined); `N` is the target commutative monoid in which the product is computed. The argument `f` is the finitely-supported function whose support drives the computation. The argument `g` is a two-argument function that maps each index together with its coefficient to an element of `N`; the product accumulates `g a (f a)` over all indices in the support of `f`.

## Conventions

When the support of `f` is empty (e.g., when `f` is the zero finsupp), the product over an empty index set is the identity element `1` of `N`, by the usual convention for empty products in a monoid.

## Worked examples

- Claim: For the finsupp that maps only `0 : Fin 3` to `2 : ℕ` (and all others to `0`), `VTask.prod f (fun a m => m + 1)` equals `3`.

- Claim: For the zero finsupp `(0 : α →₀ ℕ)`, `VTask.prod 0 g = 1` for any `g`, because the support is empty and the empty product is `1`.

- Claim: For the finsupp `f` that maps `1 : ℕ` to `3` and `2 : ℕ` to `5` (and everything else to `0`), `VTask.prod f (fun a m => m)` equals `15` (the product `3 * 5` in `ℕ`).

## Boundaries

- **Empty support (zero function):** If `f = 0`, the support is empty, and `VTask.prod f g = 1` (the multiplicative identity of `N`), regardless of `g`.
- **Single-element support:** If `f` has support `{a₀}`, then `VTask.prod f g = g a₀ (f a₀)`.
- **`g` ignoring the coefficient:** If `g a m = h a` for some `h : α → N`, the product reduces to a product of `h a` over the support of `f`, independent of the coefficient values.
- **`g` returns `1` for all inputs:** `VTask.prod f (fun _ _ => 1) = 1` for any `f`, since every factor is `1`.
- **Commutativity of `N` is required:** The product is well-defined because `N` is a commutative monoid; the order in which support elements are visited does not matter.

## Not to be confused with

- **`VTask.sum`** (the additive analogue): computes a sum `∑ a ∈ f.support, g a (f a)` in an `AddCommMonoid` rather than a product in a `CommMonoid`.
- **`Finset.prod`**: a product over an explicitly provided `Finset`, whereas `VTask.prod` automatically uses the support of a finsupp and passes both the index and its coefficient to `g`.
- **`Finsupp.mapRange`**: transforms the coefficients of a finsupp pointwise, rather than folding them into a single accumulated value.