## VTask.castNum

### Object
`VTask.castNum` is the canonical embedding of the type `Num` (the type of non-negative binary natural numbers, comprising zero and positive binary numbers) into any type that carries the constants `0` and `1` and the binary operation `+`. It sends the `Num` value representing a non-negative integer *n* to the element of the target type obtained by writing *n* in terms of `0`, `1`, and `+` in the natural way — forming the image of the unique semiring-like map from the non-negative integers into the target.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.castNum : {α : Type u_1} -> [One α] -> [Add α] -> [Zero α] -> Num → α
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the target type into which the cast is performed. The three instance arguments supply the distinguished element `1 : α`, the binary addition operation on `α`, and the distinguished element `0 : α`, respectively. The explicit argument is the `Num` value to be cast.

### Conventions

When the `Num` argument is `0` (the zero element of `Num`), the result is the `Zero` instance's zero element `0 : α`, regardless of the algebraic structure of `α` beyond the presence of `Zero`. When the `Num` argument is a positive binary number `Num.pos p`, the result is determined by recursively casting the underlying `PosNum` using `1` and `+`.

### Worked examples

- Claim: `VTask.castNum 0 = (0 : ℕ)` — casting the `Num` zero into `ℕ` yields `0`.

- Claim: `VTask.castNum (Num.pos 1) = (1 : ℕ)` — casting the smallest positive `Num` into `ℕ` yields `1`.

- Claim: `VTask.castNum (Num.pos (PosNum.bit0 1)) = (2 : ℕ)` — casting the `Num` representing `2` (binary `10`) into `ℕ` yields `2`.

- Claim: `VTask.castNum (Num.pos (PosNum.bit1 1)) = (3 : ℕ)` — casting the `Num` representing `3` (binary `11`) into `ℕ` yields `3`.

### Boundaries

- The zero case is handled directly: `VTask.castNum 0` always returns `0 : α` via the `Zero` instance, with no arithmetic operations involved.
- For `Num.pos p`, the result depends entirely on how `castPosNum` expands `p` using `1`, `bit0` (doubling), and `bit1` (doubling and adding one) in terms of `+` and `1`.
- The function is total: every `Num` value has a well-defined image in any `α` with `Zero`, `One`, and `Add`.
- No ring or semiring axioms are required of `α`; the cast exists even for non-associative or non-commutative structures, though homomorphism properties only hold when appropriate laws are assumed.

### Not to be confused with

- `Nat.cast` / `Int.cast`: the standard coercions from `ℕ` or `ℤ` into a ring or semiring, which require richer typeclass assumptions.
- `PosNum.cast` (or `castPosNum`): the analogous embedding for *positive* binary numbers only; `VTask.castNum` extends it by adding the zero case.
- `Num.toNat`: a conversion from `Num` to `ℕ` specifically, not parameterised over an arbitrary target type.