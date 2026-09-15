## Object

`VTask.split'` computes the Euclidean-style decomposition of an ordinal notation `o` with respect to `ω` (the first infinite ordinal). It returns a pair `(a, n)` where `a` is an `ONote` and `n` is a natural number, satisfying `o = ω * a + n`. In other words, `a` is the "quotient" when dividing `o` by `ω`, and `n` is the "remainder" (a finite natural number).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.split' : ONote → ONote × ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.split' : ONote → ONote × ℕ`

The single argument is an ordinal notation (`ONote`) representing the ordinal to be decomposed. The output is a pair: its first component is the quotient `ONote` (the part of `o` at or above `ω`), and its second component is the natural-number remainder (the part of `o` strictly below `ω`).

## Conventions

The zero ordinal `0 : ONote` maps to `(0, 0)`, reflecting that `0 = ω * 0 + 0`. There is no junk-value issue here: the function is total and the decomposition `o = ω * a + n` is always valid.

## Worked examples

- Claim: `VTask.split' 0 = (0, 0)` — the zero ordinal has quotient 0 and remainder 0.
  ```lean
  example : VTask.split' 0 = (0, 0) := by decide
  ```

- Claim: For the `ONote` term `oadd 0 1 0` (representing the finite ordinal 1), `VTask.split'` returns `(0, 1)` — a purely finite ordinal has quotient 0 and remainder equal to its finite value.
  ```lean
  example : VTask.split' (ONote.oadd 0 1 0) = (0, 1) := by decide
  ```

- Claim: For the `ONote` term `oadd 1 1 0` (representing `ω`), `VTask.split'` returns `(oadd 0 1 0, 0)` — `ω = ω * 1 + 0`, so quotient is 1 (as a finite `ONote`) and remainder is 0.
  ```lean
  example : VTask.split' (ONote.oadd 1 1 0) = (ONote.oadd 0 1 0, 0) := by decide
  ```

- Claim: For the `ONote` term `oadd 1 2 (oadd 0 3 0)` (representing `ω * 2 + 3`), `VTask.split'` returns `(oadd 0 2 0, 3)` — quotient is 2 and remainder is 3.
  ```lean
  example : VTask.split' (ONote.oadd 1 2 (ONote.oadd 0 3 0)) = (ONote.oadd 0 2 0, 3) := by decide
  ```

## Boundaries

- At `0`, both components are `0`.
- For a term `oadd 0 n a` (where the leading exponent is zero, i.e., the ordinal is a finite natural number `n`), the result is `(0, n)` regardless of `a`; note that in a well-formed (`NF`) term with leading exponent 0, the tail `a` must itself be 0.
- For a term `oadd e n a` with `e ≠ 0`, the remainder is inherited recursively from the tail `a`, and the quotient is built by decrementing the exponent `e` by 1.
- When `o` is well-formed (`NF o`) and `split' o = (a, n)`, then `a` is also well-formed and the ordinal equation `repr o = ω * repr a + n` holds exactly (this is the content of `nf_repr_split'`).

## Not to be confused with

- `ONote.split`: a related function that returns `(scale 1 o', m)` instead of `(o', m)`; it scales the quotient component by `ω` so that the result satisfies `o = a + n` rather than `o = ω * a + n`.
- `ONote.repr`: the function interpreting an `ONote` as an actual `Ordinal`; `split'` operates on notation, not directly on ordinal values.
- Natural-number `Nat.div`/`Nat.mod`: ordinary integer division; `split'` performs division by the transfinite ordinal `ω`, not by a natural number.