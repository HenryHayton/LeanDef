## Object

`VTask.onFinset s f hf` constructs a finitely-supported function (a `Finsupp`) from an ordinary function `f : α → M` together with a finite set `s : Finset α` that witnesses the finiteness of `f`'s support. The result agrees with `f` at every point of `α`, but the finitely-supported function packaging records that `f` is zero outside `s`, making it a legitimate member of `α →₀ M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.onFinset : {α : Type u_1} -> {M : Type u_4} -> [Zero M] -> (s : Finset α) -> (f : α → M) -> (hf : ∀ (a : α), f a ≠ 0 → a ∈ s) -> α →₀ M
<!-- PINNED-SIGNATURE:END -->


`VTask.onFinset : {α : Type u_1} -> {M : Type u_4} -> [Zero M] -> (s : Finset α) -> (f : α → M) -> (hf : ∀ (a : α), f a ≠ 0 → a ∈ s) -> α →₀ M`

The implicit type `α` is the index type; `M` is the value type, which must carry a distinguished zero element (given by the `Zero M` instance). The argument `s` is the finset that bounds the support of `f`: every index where `f` may be nonzero must lie inside `s`. The argument `f` is the underlying function to be wrapped. The argument `hf` is the proof obligation that `f` is indeed zero outside `s`, expressed as: for every `a`, if `f a ≠ 0` then `a ∈ s`.

## Conventions

There are no junk-value or boundary conventions declared for this definition; the construction is valid for any `s`, `f`, and proof `hf` satisfying the stated type, and evaluation always returns exactly `f a` at every point `a`.

## Worked examples

- Claim: Evaluating `VTask.onFinset {0, 1} (fun n : Fin 3 => if n = 1 then 5 else 0) hf` at index `1` gives `5`.
  (By `onFinset_apply`, every evaluation reduces to `f a`, so the result at `1` is `if 1 = 1 then 5 else 0 = 5`.)

- Claim: The support of `VTask.onFinset s f hf` is a subset of `s`.
  (This follows immediately from `support_onFinset_subset`: the constructed `Finsupp`'s support is contained in the bounding finset `s`.)

- Claim: An index `a` belongs to the support of `VTask.onFinset s f hf` if and only if `f a ≠ 0`.
  (This is the content of `mem_support_onFinset`: support membership is equivalent to nonzero value, regardless of how large `s` is.)

- Claim: If `g : α → M → N` satisfies `g i 0 = 1` for all `i ∈ s`, then the product of `VTask.onFinset s f hf` with `g` equals `∏ a ∈ s, g a (f a)`.
  (By `prod_onFinset`, because the support is contained in `s` and `g` kills zero-valued terms, the product collapses to a finite product over `s`.)

## Boundaries

- If `s` is the empty finset and `f` is the zero function, then `hf` is trivially satisfied and the result is the zero `Finsupp` (empty support).
- If `s` contains extra elements where `f` is zero, those elements are **not** in the support of the resulting `Finsupp`; the support is precisely `{a ∈ s | f a ≠ 0}`, which may be strictly smaller than `s`.
- There is no requirement that `f` is nonzero anywhere; the construction works even when `f` is identically zero.
- The condition `hf` is a proof, not a filter: it is the caller's responsibility to supply it; the resulting `Finsupp` does not recheck it.

## Not to be confused with

- `Finsupp.indicator`: builds a `Finsupp` from a finset and a value function, but is specifically tailored to indicator-style usage and does not require a pre-supplied proof that the function vanishes outside the set.
- `Finsupp.restrict`: restricts the support of an already-existing `Finsupp` to a subset, rather than wrapping a bare function.
- `Finsupp.single`: produces a `Finsupp` supported on a single point, a much simpler special case.
