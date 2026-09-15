## Object

`VTask.cycleG` is a state-transition function used to drive the cyclic streaming of a list. Its state encodes both the "current position" in a list being traversed and a saved copy of the original list to restart from. One call advances the state by one element: it consumes the head of the working list, yielding that head as the next output value, and when the working list is exhausted it resets to the saved original list, effectively looping back to the beginning.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cycleG : {α : Type u} -> α × List α × α × List α → α × List α × α × List α
<!-- PINNED-SIGNATURE:END -->


`VTask.cycleG : {α : Type u} -> α × List α × α × List α → α × List α × α × List α`

The single argument is a 4-tuple `(v, l, v₀, l₀)` representing the full cycle state:
- `v` is the current "head" value (the element that was just produced, or a placeholder when resetting).
- `l` is the remaining tail of the list still to be emitted before the next reset.
- `v₀` is the first element of the original list (the value to restart at after the working list is exhausted).
- `l₀` is the tail of the original list (the list to restart from after exhaustion).

The return value is a new 4-tuple of the same shape, representing the next state.

## Conventions

The `v` component of the input tuple is not used in the output when `l` is non-empty, because the next state's head is taken from `l` instead; the old `v` is effectively discarded. When `l` is empty, the state resets entirely to `(v₀, l₀, v₀, l₀)`, re-exposing the original starting element and list.

## Worked examples

- Claim: When the working list is empty, `VTask.cycleG (x, [], a, [b, c])` resets to `(a, [b, c], a, [b, c])`.

- Claim: When the working list is non-empty, `VTask.cycleG (x, [1, 2, 3], 0, [1, 2, 3])` advances to `(1, [2, 3], 0, [1, 2, 3])`.

- Claim: `VTask.cycleG (99, [42], 0, [42])` yields `(42, [], 0, [42])`, and a subsequent call on the result yields `(0, [42], 0, [42])`, restarting the cycle.

## Boundaries

- When the working list `l` is `[]`, the function ignores both `v` and `l` entirely and produces `(v₀, l₀, v₀, l₀)`. The reset is complete: the next state is identical to the state at the very start of the cycle.
- When `l` has at least one element `v₂ :: l₂`, the current value `v` is dropped, `v₂` becomes the new head, and `l₂` the new remaining list; the saved original `(v₀, l₀)` is passed through unchanged.
- The saved pair `(v₀, l₀)` is never modified by `VTask.cycleG`; it acts as a permanent anchor.
- If `l₀ = []` and `l = []`, the function returns `(v₀, [], v₀, [])` and every subsequent call on that state will do the same, emitting `v₀` forever — a cycle of length 1.

## Not to be confused with

- `Stream'.cycle` — the corecursive stream definition that *uses* `VTask.cycleG` as its generator; `VTask.cycleG` is only the single-step state transformer, not the full infinite stream.
- A simple list rotation function — `VTask.cycleG` does not rotate a list in place; it advances a streaming cursor with an embedded reset mechanism.
- `List.cycle` (if it existed) — `VTask.cycleG` operates on an explicit 4-tuple state, not directly on a list value.
