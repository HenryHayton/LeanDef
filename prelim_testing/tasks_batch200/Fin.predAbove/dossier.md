## VTask.predAbove

### Object

`VTask.predAbove p i` is a surjection from `Fin (n+1)` to `Fin n` that "collapses" the extra element by treating `p : Fin n` as a dividing point. Concretely, it sends `i : Fin (n+1)` to `i - 1` when `i` is strictly above `p` (embedded in `Fin (n+1)` via its canonical inclusion), and sends `i` to itself (viewed in `Fin n`) when `i` is at or below that embedding. Geometrically, this is the coface/degeneracy map of the simplicial category: it surjects the `(n+1)`-element chain onto the `n`-element chain by merging the slot above `p` with `p` itself.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.predAbove : {n : ℕ} -> (p : Fin n) -> (i : Fin (n + 1)) -> Fin n
<!-- PINNED-SIGNATURE:END -->


`VTask.predAbove : {n : ℕ} -> (p : Fin n) -> (i : Fin (n + 1)) -> Fin n`

The implicit argument `n` is the natural number determining the sizes of both finite types involved. The first explicit argument `p` is the pivot element in `Fin n`; it determines where the collapse occurs. The second explicit argument `i` is the element of `Fin (n+1)` being mapped down to `Fin n`.

### Conventions

The function is total and defined for all `p : Fin n` and `i : Fin (n+1)` with no junk values; every input pair yields a well-typed element of `Fin n`.

### Worked examples

- Claim: When `p = 1` and `i = 3` in `Fin 4` (so `n = 3`), we have `castSucc p = ⟨1, _⟩ < i = ⟨3, _⟩`, so the result is `pred i = ⟨2, _⟩`, i.e., `VTask.predAbove (⟨1, by omega⟩ : Fin 3) (⟨3, by omega⟩ : Fin 4) = ⟨2, by omega⟩`.
  ```lean
  example : VTask.predAbove (⟨1, by omega⟩ : Fin 3) (⟨3, by omega⟩ : Fin 4) = ⟨2, by omega⟩ := by
    native_decide
  ```

- Claim: When `p = 2` and `i = 1` in `Fin 4` (so `n = 3`), we have `castSucc p = ⟨2, _⟩ ≥ i = ⟨1, _⟩`, so the result is `castPred i = ⟨1, _⟩`, i.e., `VTask.predAbove (⟨2, by omega⟩ : Fin 3) (⟨1, by omega⟩ : Fin 4) = ⟨1, by omega⟩`.
  ```lean
  example : VTask.predAbove (⟨2, by omega⟩ : Fin 3) (⟨1, by omega⟩ : Fin 4) = ⟨1, by omega⟩ := by
    native_decide
  ```

- Claim: `VTask.predAbove` is surjective for every pivot `p : Fin n`; for any `j : Fin n` there exists `i : Fin (n+1)` with `VTask.predAbove p i = j`.

- Claim: `VTask.predAbove` is monotone in `i` for every fixed `p`; if `i ≤ i'` in `Fin (n+1)` then `VTask.predAbove p i ≤ VTask.predAbove p i'` in `Fin n`.

### Boundaries

- When `i = 0`: `castSucc p` is never strictly less than `0`, so the result is `castPred 0 = 0` in `Fin n`.
- When `i = last (n)` (the top element of `Fin (n+1)`): `castSucc p < last n` always holds (since `castSucc p ≤ last (n-1) < last n`), so the result is `pred (last n) = last (n-1)`, the top element of `Fin n`.
- When `p = 0` (the smallest pivot): any `i ≥ 1` satisfies `castSucc 0 = 0 < i`, so only `i = 0` maps to `castPred 0 = 0`; all other inputs are decremented.
- When `p = last (n-1)` (the largest valid pivot in `Fin n`): `castSucc p = last n - 1`, so only `i = last n` (i.e., `i = n`) satisfies `castSucc p < i`; all other inputs are sent via `castPred`.
- The two "images" of different preimages can coincide: specifically, both `p` (viewed in `Fin (n+1)` via `castSucc`) and `succ p` map to `p` (viewed in `Fin n`), which is the merging that makes this a surjection (not injection).

### Not to be confused with

- `Fin.succAbove`: the *injection* `Fin n → Fin (n+1)` that skips a specified element; it is a left inverse family to `predAbove` (they are adjoint degeneracy/coface maps).
- `Fin.pred`: unconditionally subtracts one from a `Fin (n+1)` to get a `Fin n`, requiring a proof the input is nonzero; `predAbove` is the version that handles zero inputs gracefully by leaving them unchanged.
- `Fin.castPred`: casts a `Fin (n+1)` element known to be strictly less than `n` into `Fin n` without changing its value; this is what `predAbove` uses in the "not above" branch, but `predAbove` works unconditionally without such a hypothesis.
