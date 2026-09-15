## 1. Object

Given a finite set `s` of indices and a function `f` that assigns a value in `α` to each index *together with a proof that the index lies in `s`*, `VTask.indicator s f` is the finitely-supported function (finsupp) `ι →₀ α` whose value at `i` is `f i hi` when `i ∈ s` (where `hi : i ∈ s`) and `0` otherwise. Informally, it is the "indicator-weighted" finsupp that is supported within `s` and carries the prescribed values on `s`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.indicator : {ι : Type u_1} -> {α : Type u_2} -> [Zero α] -> (s : Finset ι) -> (f : (i : ι) → i ∈ s → α) -> ι →₀ α
<!-- PINNED-SIGNATURE:END -->


`VTask.indicator : {ι : Type u_1} -> {α : Type u_2} -> [Zero α] -> (s : Finset ι) -> (f : (i : ι) → i ∈ s → α) -> ι →₀ α`

- `ι` is the implicit index type.
- `α` is the implicit value type; it must carry a distinguished zero element (supplied by the `[Zero α]` instance), which serves as the "off-support" default value.
- `s` is the finset of indices on which `f` is defined; the resulting finsupp has support contained in `s`.
- `f` is a dependent function that, for each index `i` and a proof that `i ∈ s`, returns the value to assign at `i`. The proof of membership is threaded through so that the domain of `f` is exactly `s`.

## 3. Conventions

When the index `i` does not belong to `s`, the finsupp evaluates to `0` (the zero of `α`). The support of the result is the subset of `s` where `f` takes nonzero values; indices in `s` where `f` returns `0` are excluded from the support, consistent with the finsupp invariant that the support contains exactly the nonzero entries.

## 4. Worked examples

- Claim: For any index `i` that belongs to `s`, `VTask.indicator s f i = f i hi`.
  (This is the `indicator_of_mem` specialisation: when `i ∈ s`, the result equals the value prescribed by `f`.)

- Claim: For any index `i` that does not belong to `s`, `VTask.indicator s f i = 0`.
  (This is the `indicator_of_notMem` specialisation: outside `s` the result is zero.)

- Claim: The support of `VTask.indicator s f` is a subset of `s`.
  (Formalised as `support_indicator_subset`; indices outside `s` always map to `0` so they cannot appear in the support.)

- Claim: `VTask.indicator {i} (fun _ _ => b) = Finsupp.single i b` for any `b : α`.
  (The singleton-set indicator with constant value `b` coincides with the standard single-point finsupp; this matches `single_eq_indicator`.)

## 5. Boundaries

- **Empty finset**: `VTask.indicator ∅ f` is the zero finsupp; there are no indices in `∅`, so every index maps to `0` and the support is empty.
- **`f` everywhere zero**: If `f i hi = 0` for every `i ∈ s`, then the support is empty and the result is the zero finsupp, even though `s` may be nonempty.
- **`f` injected at a single point**: When `s = {i}`, the result is the finsupp that equals `f i hi` at `i` and `0` everywhere else, i.e., `Finsupp.single i (f i hi)` (modulo the trivial `0` case).
- **Injectivity**: The map `f ↦ VTask.indicator s f` is injective in `f` (holding `s` fixed), so two distinct dependent functions on `s` always produce distinct finsupps.

## 6. Not to be confused with

- `Set.indicator`: The set-theoretic indicator for an arbitrary (possibly infinite) set and an unconstrained function `ι → α`; it returns a plain function, not a finsupp, and does not track a finite support.
- `Finsupp.single`: Creates a finsupp supported at exactly one point; `VTask.indicator` generalises this to an arbitrary finite set.
- `Finsupp.filter`: Restricts an *existing* finsupp to indices satisfying a predicate; `VTask.indicator` *constructs* a new finsupp from scratch given a finset and a dependent function.