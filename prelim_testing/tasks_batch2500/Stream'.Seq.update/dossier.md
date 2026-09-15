## Object

`VTask.update s n f` produces a new lazy sequence that is identical to `s` in every position except possibly position `n`: if the `n`-th element of `s` exists (i.e., `s.get? n = some a` for some `a`), that element is replaced by `f a`; if position `n` is absent (past the end of a finite sequence), the result is unchanged from `s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.update : {α : Type u} -> (s : Stream'.Seq α) -> (n : ℕ) -> (f : α → α) -> Stream'.Seq α
<!-- PINNED-SIGNATURE:END -->


The first argument `s` is the source sequence to be modified. The second argument `n` is the zero-based index of the element to update. The third argument `f` is the function applied to the element at position `n` when that element is present.

## Conventions

When the index `n` is out of range (i.e., `s.get? n = none`), applying `f` has no effect: `VTask.update s n f = s`. There is no notion of a default or inserted element.

## Worked examples

- Claim: Updating any index of the empty (nil) sequence returns the empty sequence: `VTask.update Stream'.Seq.nil n f = Stream'.Seq.nil`.

- Claim: Updating index 0 of a cons-sequence `cons hd tl` with `f` yields `cons (f hd) tl`, leaving the tail unchanged.

- Claim: Updating index `n+1` of a cons-sequence `cons hd tl` recurses into the tail: `(cons hd tl).update (n+1) f = cons hd (tl.update n f)`.

- Claim: For any sequence `s`, natural numbers `m` and `n`, and function `f`, `(VTask.update s n f).get? m = if m = n then (s.get? m).map f else s.get? m`. In particular, the updated position returns the mapped value, and all other positions are unaffected.

## Boundaries

- **Index out of range (finite sequence):** If `n ≥` the length of a finite sequence so that `s.get? n = none`, then `Option.map f none = none`, so the sequence is returned unchanged.
- **Infinite sequences:** The update touches exactly one position regardless of the length of the sequence.
- **Index zero:** Updating position 0 of a cons-sequence applies `f` directly to the head.
- **Identity function:** Passing `f = id` produces a sequence extensionally equal to `s` at every position, though it may not be definitionally equal.

## Not to be confused with

- `Stream'.Seq.map`: applies a function to *every* element of the sequence, not just one position.
- `Stream'.Seq.cons`: prepends a new element, shifting all indices up, rather than replacing an existing element in place.
- `Function.update`: the underlying pointwise update on functions; `VTask.update` lifts this to the `Seq` abstraction while respecting the sequence invariant.