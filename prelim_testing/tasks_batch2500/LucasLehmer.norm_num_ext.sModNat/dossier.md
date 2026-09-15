## Object

`VTask.sModNat q` is a natural-number–valued sequence that computes the Lucas–Lehmer residues modulo `q`, intended for use with Mersenne numbers `q = 2^p − 1`. Concretely, the sequence starts at `4 mod q` and at each successive step squares the current value, adds `q − 2` (which corresponds to subtracting 2 modulo `q`), and reduces modulo `q`. The Lucas–Lehmer primality test for the Mersenne number `2^p − 1` amounts to checking whether `VTask.sModNat (2^p − 1) (p − 2) = 0`. Because it is `ℕ`-valued (rather than `ℤ`-valued), this version is suitable for kernel reduction and certified computation.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sModNat : (q : ℕ) -> ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.sModNat : (q : ℕ) -> ℕ → ℕ`

The first argument `q` is the modulus, which in the Lucas–Lehmer application is taken to be the Mersenne number `2^p − 1` for a prime candidate `p`. The second argument is the index `i` into the sequence: `i = 0` yields the initial value, and `i = k + 1` yields the value obtained by applying one step of the Lucas–Lehmer recurrence to the value at index `k`.

## Conventions

The function is defined for all natural-number inputs and is total; no domain restriction is imposed. When `q = 0` the modular reductions `% 0` follow Lean/Mathlib's convention that `n % 0 = n`, so the sequence grows without bound rather than staying bounded. The intended regime is `q = 2^p − 1` with `p ≥ 2`, in which case `q ≥ 3` and every term lies in `{0, 1, …, q − 1}`.

## Worked examples

- Claim: `VTask.sModNat 7 0 = 4` (initial value 4 mod 7 is 4).
  ```lean
  example : VTask.sModNat 7 0 = 4 := by native_decide
  ```

- Claim: `VTask.sModNat 7 1 = 2` (step 1: 4² + (7−2) = 21, 21 % 7 = 0... wait, 16 + 5 = 21, 21 % 7 = 0; let us redo: actually 4^2 = 16, 16 + 5 = 21, 21 % 7 = 0). Corrected claim: `VTask.sModNat 7 1 = 0`.
  ```lean
  example : VTask.sModNat 7 1 = 0 := by native_decide
  ```

- Claim: For the Mersenne prime `M_3 = 7` the Lucas–Lehmer test index is `p − 2 = 1`, and indeed `VTask.sModNat 7 1 = 0`, confirming 7 is prime.
  ```lean
  example : VTask.sModNat (2^3 - 1) (3 - 2) = 0 := by native_decide
  ```

- Claim: For `q = 2^5 − 1 = 31`, the sequence value at index `3` (= `p − 2 = 5 − 2`) is `0`, corresponding to 31 being prime.
  ```lean
  example : VTask.sModNat (2^5 - 1) (5 - 2) = 0 := by native_decide
  ```

## Boundaries

- **`i = 0` (base case):** The value is `4 % q`. For `q ≥ 5` this is `4`; for `q = 1` it is `0`; for `q = 2` it is `0`; for `q = 3` it is `1`; for `q = 4` it is `0`; for `q = 0` it is `4` (since `4 % 0 = 4` in Lean).
- **`q = 0`:** Modular reduction by `0` is the identity in Lean (`n % 0 = n`), so the sequence is the ordinary integer Lucas–Lehmer sequence without reduction, growing rapidly.
- **`q = 1`:** Every term is `0` because any natural number mod `1` is `0`.
- **`q = 2`:** The initial value is `4 % 2 = 0`, and subsequent steps remain `0`.
- **Large `i` beyond `p − 2`:** The function is still well-defined by its recurrence, but the values beyond the test index have no primality-theoretic significance.

## Not to be confused with

- **`LucasLehmer.sMod`** (`ℤ`-valued version): the signed integer variant of the same sequence; `VTask.sModNat` is its natural-number counterpart, related by casting.
- **`LucasLehmer.norm_num_ext.sModNatTR`**: a tail-recursive implementation of the same mathematical function, equal to `VTask.sModNat` by theorem but more efficient for large computations.
- **`LucasLehmer.LucasLehmerTest`**: the Boolean/Prop predicate that wraps the test `sModNat (2^p − 1) (p − 2) = 0`; `VTask.sModNat` is the underlying numerical sequence, not the test predicate itself.
