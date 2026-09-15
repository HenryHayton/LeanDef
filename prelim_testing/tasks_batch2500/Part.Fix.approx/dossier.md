## Object

`VTask.approx f` is an infinite stream whose `n`-th term is the `n`-fold iterate of `f` applied to the least element (the totally-undefined partial function) `⊥`. Concretely, the 0-th term is `⊥` (every output undefined), the 1st term is `f ⊥`, the 2nd is `f (f ⊥)`, and so on. These successive approximations form a monotone chain whose least upper bound (limit) is the least fixed point of `f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.approx : {α : Type u_1} -> {β : α → Type u_2} -> (f : ((a : α) → Part (β a)) → (a : α) → Part (β a)) -> Stream' ((a : α) → Part (β a))
<!-- PINNED-SIGNATURE:END -->


`VTask.approx : {α : Type u_1} -> {β : α → Type u_2} -> (f : ((a : α) → Part (β a)) → (a : α) → Part (β a)) -> Stream' ((a : α) → Part (β a))`

The type `α` is the domain of the dependent functions being approximated; `β` assigns to each `a : α` the type of the output at `a`. The argument `f` is the functional whose least fixed point is being computed: it maps a partial dependent function to another partial dependent function, and the approximation sequence is built by iterating `f` starting from `⊥`.

## Conventions

No special junk-value or out-of-domain conventions apply: the stream is defined for every natural-number index, the type is unrestricted, and every position is assigned a well-defined value.

## Worked examples

- Claim: The 0-th approximation `VTask.approx f 0` equals `⊥` (the totally-undefined partial function) for any `f`.

- Claim: The `(n+1)`-th approximation `VTask.approx f (n+1)` equals `f (VTask.approx f n)`, i.e., applying `f` once more to the previous approximation.

- Claim: For any `i`, `VTask.approx f i ≤ VTask.approx f (i+1)` — the chain is monotone (each approximation is pointwise "more defined" than the previous).

- Claim: For any index `i`, `VTask.approx f i ≤ Part.fix f` — every finite approximation is below the fixed point.

- Claim: Conversely, for every input `a` and any element `b` in `Part.fix f a`, there exists some index `i` such that `b ∈ VTask.approx f i a` — the fixed point is exactly the limit of the approximations.

## Boundaries

- At index 0, the result is `⊥`: every output is undefined (no information about the fixed point yet).
- At index 1, the result is `f ⊥`: a single application of `f` to the empty approximation.
- The stream is infinite: it is defined at every non-negative integer index.
- If `f` is Scott-continuous (or at least monotone and respects the chain), the limit of the stream is guaranteed to be the least fixed point of `f`.
- For a constant function `f` that ignores its argument, the stream stabilises immediately at index 1: all terms from index 1 onward are equal.

## Not to be confused with

- `Part.fix f`: the actual least fixed point of `f`, which is the *limit* of `VTask.approx f`, not any individual term of the stream.
- `VTask.approxChain f`: the set (omega-chain) formed by all terms of the approximation sequence, used to phrase Scott-continuity arguments; closely related but a different presentation of the same data.
- `Stream'.iterate`: a general stream of iterates of an endofunction on a plain type, without the partial-function / fixed-point framing.
