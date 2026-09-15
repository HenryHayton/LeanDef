## Object

`VTask.sMod p` is the integer-valued sequence defined by the Lucas–Lehmer recurrence modulo `2^p − 1`. Concretely, starting from the seed value `4 mod (2^p − 1)`, each successive term is obtained by squaring the previous term, subtracting 2, and reducing modulo `2^p − 1`. The result at each step is an integer in the range `[0, 2^p − 2)` (for `p ≠ 0`). This sequence is the integer shadow of the standard Lucas–Lehmer test sequence: the Mersenne prime `M_p = 2^p − 1` is prime if and only if the `(p−2)`-th term of this sequence is zero.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sMod : (p : ℕ) -> ℕ → ℤ
<!-- PINNED-SIGNATURE:END -->


VTask.sMod : (p : ℕ) -> ℕ → ℤ

The first argument `p` is the exponent determining the Mersenne modulus `2^p − 1` against which all reductions are performed; it also governs the starting value. The second argument is the index `i` in the recurrence, indicating how many steps of the squaring-minus-two iteration have been applied.

## Conventions

When `p = 0` the modulus `2^0 − 1 = 0`, so all reductions are modulo 0; in Lean/Mathlib, integer modulo 0 is defined to return 0, making every term of the sequence equal to 0 in this degenerate case. The nonnegativity and strict upper-bound theorems both require `p ≠ 0`, reflecting that the interesting bounded regime only holds when the modulus is positive.

## Worked examples

- Claim: `VTask.sMod 5 0 = 4` (since `4 % (2^5 − 1) = 4 % 31 = 4`).

- Claim: `VTask.sMod 5 1 = 14` (since `(4^2 − 2) % 31 = 14 % 31 = 14`).

- Claim: `VTask.sMod 5 2 = 194 % 31 = 8` (since `14^2 − 2 = 194` and `194 % 31 = 8`).

- Claim: `VTask.sMod 5 3 = 0` (since `8^2 − 2 = 62` and `62 % 31 = 0`); this is consistent with `p = 5` yielding the Mersenne prime 31, and `p − 2 = 3` being the index checked by the Lucas–Lehmer criterion.

- Claim: For any `p` and `i`, `VTask.sMod p i % (2^p − 1) = VTask.sMod p i` (the sequence values are already fully reduced).

- Claim: For `p ≠ 0` and any `i`, `0 ≤ VTask.sMod p i` and `VTask.sMod p i < 2^p − 1`.

## Boundaries

- **`p = 0`**: The modulus `2^0 − 1 = 0`. Integer remainder modulo 0 in Lean is 0, so `VTask.sMod 0 i = 0` for all `i`. The nonnegativity and strict upper-bound theorems do not apply here.
- **`p = 1`**: The modulus `2^1 − 1 = 1`. Every integer reduced modulo 1 is 0, so `VTask.sMod 1 i = 0` for all `i`.
- **`i = 0`**: The sequence is initialized to `4 % (2^p − 1)`. For `p ≥ 3` this equals 4; for `p = 1` it equals 0; for `p = 2` it equals `4 % 3 = 1`.
- **General `p ≠ 0`**: Each term satisfies `0 ≤ VTask.sMod p i < 2^p − 1`, so the output is always a non-negative integer strictly below the Mersenne number.

## Not to be confused with

- **`LucasLehmer.sZMod p i`**: The same recurrence viewed in `ZMod (2^p − 1)` rather than `ℤ`; related by `sZMod p i = (sMod p i : ZMod (2^p − 1))`.
- **`LucasLehmer.lucasLehmerResidue p`**: The single residue value `sMod p (p − 2)` cast into `ZMod (2^p − 1)`, used directly in the primality statement; it is zero iff `sMod p (p − 2) = 0`.
- **The unmodulated Lucas sequence `s`**: The version of the recurrence without reduction modulo `2^p − 1`, whose terms grow doubly exponentially and are used in theoretical arguments but not for computation.