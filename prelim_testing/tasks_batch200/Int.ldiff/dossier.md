## 1. Object

`VTask.ldiff a b` computes the bitwise set-difference of two integers `a` and `b`. Treating each integer as a (two's-complement) infinite sequence of bits, the `k`-th bit of the result is `1` exactly when the `k`-th bit of `a` is `1` **and** the `k`-th bit of `b` is `0`; otherwise it is `0`. Equivalently, the result bit is the Boolean value `aₖ ∧ ¬bₖ`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ldiff : ℤ → ℤ → ℤ
<!-- PINNED-SIGNATURE:END -->


`VTask.ldiff : ℤ → ℤ → ℤ`

The first argument `a` is the integer whose bits form the "base" set — only bits that are set in `a` can appear in the result. The second argument `b` is the integer whose bits are "subtracted" (masked away) — any bit position that is `1` in `b` is forced to `0` in the result.

## 3. Conventions

The operation is defined on all pairs of integers without restriction; it is a total function on `ℤ`. Negative integers are treated via their standard two's-complement (infinite-precision) representation, so every negative integer has an infinite run of leading `1`-bits. No special junk values or out-of-domain conventions are declared for this function.

## 4. Worked examples

- Claim: `VTask.ldiff 12 10 = 4`  
  In binary, `12 = ...01100` and `10 = ...01010`; applying `aₖ ∧ ¬bₖ` bit-by-bit gives `...00100 = 4`.

- Claim: `VTask.ldiff 15 6 = 9`  
  `15 = ...01111`, `6 = ...00110`; result is `...01001 = 9` (bits 1 and 2, which are set in `6`, are cleared).

- Claim: For any integer `a`, `VTask.ldiff a a = 0` because every bit position satisfies `aₖ ∧ ¬aₖ = false`.

- Claim: For any integer `a`, `VTask.ldiff a 0 = a` because `¬0 = ...11111...` (all ones in two's-complement), so no bits of `a` are cleared.

- Claim: `VTask.ldiff (-3) 5 = -8`  
  In two's-complement, `-3 = ...111101` and `5 = ...000101`; applying `aₖ ∧ ¬bₖ` clears bits 0 and 2, leaving `...111000 = -8`.

## 5. Boundaries

- **Both arguments zero**: `VTask.ldiff 0 0 = 0`; the empty set minus the empty set is empty.
- **First argument zero**: `VTask.ldiff 0 b = 0` for any `b`, since there are no `1`-bits in `0` that could survive the mask.
- **Second argument zero**: `VTask.ldiff a 0 = a` for any `a`, since no bits of `a` are masked away.
- **Both arguments `-1`**: `-1` has all bits set in two's-complement; `VTask.ldiff (-1) (-1) = 0`.
- **Second argument `-1`**: `-1` has all bits set, so it masks away every bit of the first argument; `VTask.ldiff a (-1) = 0` for any `a`.
- **First argument `-1`**: `VTask.ldiff (-1) b` clears exactly the `1`-bits of `b`; this equals `~~~b` (bitwise NOT of `b`).
- The operation is **not commutative** in general: `VTask.ldiff a b ≠ VTask.ldiff b a` unless `a = b` or both are zero.

## 6. Not to be confused with

- **`Int.land` (bitwise AND)**: computes `aₖ ∧ bₖ`, keeping bits that are `1` in *both* operands, rather than only in `a` and not `b`.
- **`Int.lor` (bitwise OR)**: computes `aₖ ∨ bₖ`, the union of both bit-sets, not their difference.
- **`Int.lxor` (bitwise XOR)**: computes `aₖ ⊕ bₖ`, the symmetric difference; differs from `ldiff` because it also keeps bits that are `1` in `b` but not in `a`.
