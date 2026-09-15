## Object

`VTask.succAbove p i` is the standard order-preserving embedding of `Fin n` into `Fin (n + 1)` that "skips" a chosen target element `p`. Concretely, given a "hole" position `p` in `Fin (n + 1)`, every element `i` of `Fin n` is mapped to the unique element of `Fin (n + 1)` that has the same order as `i` among the elements of `Fin (n + 1)` other than `p`. Elements that would land below `p` are left alone (cast straight up), while elements that would land at or above `p` are shifted up by one to leave `p` empty.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.succAbove : {n : ℕ} -> (p : Fin (n + 1)) -> (i : Fin n) -> Fin (n + 1)
<!-- PINNED-SIGNATURE:END -->


The implicit argument `n` is the size parameter; the finite types involved are `Fin n` and `Fin (n + 1)`. The first explicit argument `p : Fin (n + 1)` is the "hole" — the element of `Fin (n + 1)` that is avoided; no input `i` ever maps to `p`. The second explicit argument `i : Fin n` is the element being embedded.

## Conventions

There are no special junk-value conventions: the function is total on its natural domain, and both arguments are bounded finite types with no out-of-range cases.

## Worked examples

- Claim: `VTask.succAbove (2 : Fin 4) (0 : Fin 3) = 0` — index 0 is strictly below the hole at 2, so it is cast straight up.
  ```lean
  example : VTask.succAbove (2 : Fin 4) (0 : Fin 3) = 0 := by decide
  ```

- Claim: `VTask.succAbove (2 : Fin 4) (2 : Fin 3) = 3` — index 2 (as an element of Fin 3) would land at 2 which is the hole, so it is shifted to 3.
  ```lean
  example : VTask.succAbove (2 : Fin 4) (2 : Fin 3) = 3 := by decide
  ```

- Claim: `VTask.succAbove (0 : Fin 4) (0 : Fin 3) = 1` — with the hole at position 0 every element is shifted up; the least element maps to 1.
  ```lean
  example : VTask.succAbove (0 : Fin 4) (0 : Fin 3) = 1 := by decide
  ```

- Claim: `VTask.succAbove (3 : Fin 4) (2 : Fin 3) = 2` — with the hole at the last position, all elements keep their natural (castSucc) embedding.
  ```lean
  example : VTask.succAbove (3 : Fin 4) (2 : Fin 3) = 2 := by decide
  ```

## Boundaries

- **Hole at `0`**: every element `i : Fin n` is mapped to `i.succ` (i.e., shifted up by one), since no element of `Fin n` satisfies `castSucc i < 0`.
- **Hole at the last element `n`**: every element `i : Fin n` satisfies `castSucc i < n`, so every element is mapped to its `castSucc`, the natural inclusion keeping the value unchanged.
- **`n = 0`**: in this case `Fin 0` is empty, so there are no valid inputs `i` and the function is vacuously defined.
- The image of `VTask.succAbove p` is exactly the complement `{p}ᶜ` in `Fin (n + 1)`; in particular, `p` is never in the image.
- The function is strictly order-preserving and injective for every fixed `p`.

## Not to be confused with

- `Fin.castSucc`: embeds `Fin n` into `Fin (n + 1)` without skipping anything, always mapping `i` to the same numerical value — no hole is introduced.
- `Fin.succ`: shifts every element of `Fin n` up by one, equivalent to `VTask.succAbove 0` but not parameterised by a hole position.
- `Fin.predAbove`: the partial left inverse of `VTask.succAbove`; it maps `Fin (n + 1)` back to `Fin n` by collapsing around a pivot, roughly undoing the hole insertion.