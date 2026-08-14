## Object

`VTask.swapCore a b r` is the elementary transposition function on a type with decidable equality. It maps the element `r` to `b` if `r` equals `a`, to `a` if `r` equals `b`, and leaves `r` unchanged otherwise. Informally, it is the action of the transposition (a b) on a single element `r`: it swaps `a` and `b` and fixes everything else.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.swapCore : {α : Sort u_1} -> [DecidableEq α] -> (a b r : α) -> α
<!-- PINNED-SIGNATURE:END -->


`VTask.swapCore : {α : Sort u_1} -> [DecidableEq α] -> (a b r : α) -> α`

The implicit type argument `α` is the ambient type on which the transposition acts; it must be a `Sort`, so the construction works for both types and propositions. The `DecidableEq α` instance is required so that equality checks on elements of `α` can be computed. The explicit argument `a` is the first element of the pair being swapped; `b` is the second element of the pair; `r` is the element being mapped — the "input" on which the transposition acts.

## Conventions

When `a = b`, the function acts as the identity on every element: swapping an element with itself does nothing, so `VTask.swapCore a a r = r` for all `r`. There are no junk values; the function is total over all choices of `a`, `b`, and `r`.

## Worked examples

- Claim: `VTask.swapCore 1 2 1 = 2` — mapping the first swap target gives the second.
  ```lean
  example : VTask.swapCore 1 2 1 = 2 := by decide
  ```

- Claim: `VTask.swapCore 1 2 2 = 1` — mapping the second swap target gives the first.
  ```lean
  example : VTask.swapCore 1 2 2 = 1 := by decide
  ```

- Claim: `VTask.swapCore 1 2 3 = 3` — an element outside the swapped pair is fixed.
  ```lean
  example : VTask.swapCore 1 2 3 = 3 := by decide
  ```

- Claim: `VTask.swapCore 5 5 3 = 3` — swapping an element with itself is the identity.
  ```lean
  example : VTask.swapCore 5 5 3 = 3 := by decide
  ```

- Claim: `VTask.swapCore a b (VTask.swapCore a b r) = r` for all `a b r : α` — the transposition is an involution.

- Claim: `VTask.swapCore a b r = VTask.swapCore b a r` for all `a b r : α` — the swap is symmetric in its two targets.

## Boundaries

- When `r = a` and `r = b` simultaneously (i.e., `a = b = r`), the first branch fires and returns `b = a = r`, which is correct: the identity case.
- When `a = b` but `r ≠ a`, neither swap branch fires, and `r` is returned unchanged — the whole function is the identity.
- The function is defined for all elements of any `Sort` with decidable equality; there are no excluded inputs.
- The function is its own inverse: applying it twice always recovers the original element.

## Not to be confused with

- `Equiv.swap a b` — the full `Equiv` (permutation) built from this helper, which packages both the forward map and its inverse (which coincide here) with proofs; `VTask.swapCore` is merely the underlying map.
- A general transposition in a permutation group — `VTask.swapCore` operates on a single element, not on an entire permutation or list.
- `Function.swap` — which swaps the first two *arguments* of a two-argument function, unrelated to element transposition.