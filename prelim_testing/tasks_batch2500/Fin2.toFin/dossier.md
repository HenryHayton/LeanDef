## Object

A canonical bijection from the type `Fin2 n` — the inductively defined finite type with `n` elements, whose constructors are `fz` (zero) and `fs` (successor) — to the type `Fin n` — the standard Mathlib finite type of natural numbers less than `n`. It maps the `Fin2` index to the numerically equal element of `Fin n`, preserving the natural ordering.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toFin : {n : ℕ} -> (i : Fin2 n) -> Fin n
<!-- PINNED-SIGNATURE:END -->


`{n : ℕ} -> (i : Fin2 n) -> Fin n`

The implicit argument `n` is the size of the finite type; it is inferred from the input. The explicit argument `i` is the `Fin2 n` element to be converted.

## Conventions

This function is total and well-defined for all `i : Fin2 n` for any `n : ℕ`. There are no junk-value or partiality conventions to declare.

## Worked examples

- Claim: `VTask.toFin fz = (0 : Fin 3)` — the `fz` constructor (zero) maps to the zero element of `Fin n`.
  ```lean
  example : VTask.toFin (@Fin2.fz 2) = (0 : Fin 3) := by decide
  ```

- Claim: `VTask.toFin (fs fz) = (1 : Fin 3)` — one application of `fs` wrapping `fz` maps to the element `1`.
  ```lean
  example : VTask.toFin (Fin2.fs Fin2.fz : Fin2 3) = (1 : Fin 3) := by decide
  ```

- Claim: `VTask.toFin (fs (fs fz)) = (2 : Fin 4)` — two applications of `fs` wrapping `fz` maps to the element `2`.
  ```lean
  example : VTask.toFin (Fin2.fs (Fin2.fs Fin2.fz) : Fin2 4) = (2 : Fin 4) := by decide
  ```

- Claim: The round-trip `Fin2.ofFin (VTask.toFin i) = i` holds for all `i : Fin2 n`, confirming that `VTask.toFin` is injective (in fact, a bijection whose inverse is `ofFin`).

## Boundaries

- When `n = 0`, the type `Fin2 0` is empty, so the function is vacuously well-typed and never actually called.
- At `fz : Fin2 (n+1)`, the result is exactly `0 : Fin (n+1)`.
- At `fs i : Fin2 (n+1)`, the result is the successor (in `Fin`) of `VTask.toFin i`, so the numerical value is preserved by recursion.
- The function is a bijection: `Fin2.ofFin` is its two-sided inverse, satisfying both `ofFin (VTask.toFin i) = i` and `VTask.toFin (ofFin j) = j`.

## Not to be confused with

- `Fin2.ofFin` — the inverse direction, converting a `Fin n` into a `Fin2 n`; `VTask.toFin` and `ofFin` are mutual inverses.
- `Fin.val` — extracts the underlying `ℕ` from a `Fin n`; `VTask.toFin` instead changes the *type* from `Fin2 n` to `Fin n`, not to `ℕ`.
- `Fin2.val` (if it existed) — `Fin2` does not carry a `.val` field in the same way `Fin` does; `VTask.toFin` provides the bridge to reach `Fin`'s `.val`.