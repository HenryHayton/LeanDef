## Object

Given a finitely supported function `f : α →₀ M` and a predicate `p : α → Prop`, `VTask.filter p f` is the finitely supported function whose value at each `a : α` is `f a` when `p a` holds and `0` otherwise. In other words, it restricts the "support" of `f` to those indices satisfying `p`, zeroing out all other values.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.filter : {α : Type u_1} -> {M : Type u_5} -> [Zero M] -> (p : α → Prop) -> [DecidablePred p] -> (f : α →₀ M) -> α →₀ M
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the index type; `M` is the value type, which must carry a distinguished zero element (via the `[Zero M]` instance). The argument `p` is the predicate used to select indices: only those `a` for which `p a` is true are kept. The `[DecidablePred p]` instance allows the predicate to be evaluated computationally. The argument `f` is the finitely supported function being filtered.

## Conventions

At any index `a` where `p a` does not hold, the output value is exactly `0` (the zero of `M`), regardless of the original value `f a`. This is the standard junk-value convention for the "masked-out" entries.

## Worked examples

- Claim: Filtering the zero finsupp by any predicate yields the zero finsupp.
  (This follows from `filter_zero`: `(0 : α →₀ M).filter p = 0`.)

- Claim: For `f : α →₀ M` and an index `a` with `p a` true, `(VTask.filter p f) a = f a`.
  (This is the `filter_apply_pos` behaviour: the value is preserved when the predicate holds.)

- Claim: For `f : α →₀ M` and an index `a` with `p a` false, `(VTask.filter p f) a = 0`.
  (This is the `filter_apply_neg` behaviour: the value is zeroed out when the predicate fails.)

- Claim: The support of `VTask.filter p f` equals the set of elements in `f.support` that also satisfy `p`.
  (That is, `(VTask.filter p f).support = {x ∈ f.support | p x}`.)

- Claim: Filtering distributes over addition: `VTask.filter p (v + v') = VTask.filter p v + VTask.filter p v'`.

- Claim: For a single-element finsupp `single a b`, if `p a` holds then `VTask.filter p (single a b) = single a b`; if `p a` fails then `VTask.filter p (single a b) = 0`.

## Boundaries

- **Zero function**: Filtering the zero finsupp always returns the zero finsupp, for any predicate.
- **Predicate always true**: If `p a` holds for every `a`, then `VTask.filter p f = f` (the function is unchanged).
- **Predicate always false**: If `p a` fails for every `a`, then `VTask.filter p f = 0`.
- **Single-point finsupps**: Whether a `single a b` is preserved or zeroed depends entirely on whether `p a` holds.
- **Non-computable predicates**: A `DecidablePred` instance is required; without it, the filter cannot be formed.
- **Zero values in support**: Only elements with nonzero value appear in the support; filtering further restricts to those additionally satisfying `p`.

## Not to be confused with

- `Finsupp.restrict` / `Finsupp.restrictDom`: restricts a finsupp to a *set* (membership predicate) and may carry a submodule/subtype flavour, whereas `VTask.filter` works with an arbitrary `Prop`-valued predicate on indices.
- `Finset.filter`: filters a finite *set* of elements, not a finitely supported *function*; there is no value-zeroing semantics.
- `Finsupp.subtype_domain`: restricts index type to a subtype satisfying a predicate and changes the index type itself, whereas `VTask.filter` keeps the same index type `α`.