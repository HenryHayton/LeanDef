## Object

`VTask.LimZero f` is the proposition that the Cauchy sequence `f` converges to zero. Concretely, it asserts that for every positive tolerance `ε`, there exists an index `i` such that for all later indices `j ≥ i`, the absolute value (as measured by the given absolute-value function `abv`) of the `j`-th term of `f` is strictly less than `ε`. In other words, `f` is a null sequence: its terms eventually become arbitrarily small in absolute value.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.LimZero : {α : Type u_1} -> {β : Type u_2} -> [Field α] -> [LinearOrder α] -> [IsStrictOrderedRing α] -> [Ring β] -> {abv : β → α} -> (f : CauSeq β abv) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.LimZero : {α : Type u_1} -> {β : Type u_2} -> [Field α] -> [LinearOrder α] -> [IsStrictOrderedRing α] -> [Ring β] -> {abv : β → α} -> (f : CauSeq β abv) -> Prop`

The type `α` is the ordered field in which sizes are measured (e.g. `ℚ` or `ℝ`); it must carry a linear order compatible with its ring structure. The type `β` is the ring whose elements form the sequence (e.g. `ℝ`, `ℂ`, or a `p`-adic ring). The function `abv : β → α` is an absolute value (or more generally a norm function satisfying the axioms of an absolute value) used to measure the size of terms of the sequence. The argument `f : CauSeq β abv` is the specific Cauchy sequence being tested for convergence to zero.

## Conventions

There are no junk-value conventions to declare for this definition: `VTask.LimZero` is a logically meaningful proposition for every well-formed `CauSeq β abv`, and its definition is a straightforward universal–existential statement with no special behavior on degenerate or boundary inputs that would require an arbitrary convention.

## Worked examples

- Claim: The constant zero sequence satisfies `VTask.LimZero`, i.e., `VTask.LimZero (CauSeq.const abv 0)` holds.

- Claim: The constant sequence at a nonzero element `x ≠ 0` does NOT satisfy `VTask.LimZero`, i.e., `¬ VTask.LimZero (CauSeq.const abv x)` when `x ≠ 0`.

- Claim: If `f` and `g` both satisfy `VTask.LimZero`, then so does their sum `f + g`, i.e., `VTask.LimZero f → VTask.LimZero g → VTask.LimZero (f + g)`.

- Claim: If `f` satisfies `VTask.LimZero` and `g` is any Cauchy sequence, then `f * g` satisfies `VTask.LimZero`, i.e., `VTask.LimZero f → VTask.LimZero (f * g)`.

## Boundaries

- The zero sequence `0 : CauSeq β abv` always satisfies `VTask.LimZero`, since `abv 0 = 0 < ε` for any `ε > 0`.
- A nonzero constant sequence `CauSeq.const abv x` with `x ≠ 0` does **not** satisfy `VTask.LimZero`, because `abv (f j) = abv x > 0` for all `j`, so taking `ε = abv x / 2` witnesses failure.
- `VTask.LimZero` is preserved under negation: if `f` tends to zero, so does `-f`.
- `VTask.LimZero` is preserved under subtraction: if `f` and `g` both tend to zero, so does `f - g`.
- Two equivalent Cauchy sequences (in the sense of the `≈` relation on `CauSeq`) satisfy `VTask.LimZero` simultaneously: `f ≈ g → (VTask.LimZero f ↔ VTask.LimZero g)`.
- In the ordered-field case (where `β = α` and `abv` is the standard absolute value), exactly one of `Pos f`, `VTask.LimZero f`, or `Pos (-f)` holds (trichotomy).
- A sequence satisfying `VTask.LimZero` cannot simultaneously be `Pos` (bounded away from zero above).
- If `f` does not satisfy `VTask.LimZero`, then there exist `K > 0` and an index `i` such that `abv (f j) ≥ K` for all `j ≥ i`.

## Not to be confused with

- `CauSeq.Pos f`: asserts that `f` is eventually bounded *away from* zero (from above), the opposite extreme from `VTask.LimZero`.
- `f ≈ g` (equivalence of Cauchy sequences): asserts `VTask.LimZero (f - g)`, i.e., `f` and `g` approach each other, not that either approaches zero.
- `lim f = 0` (limit equals zero in the Cauchy completion): logically equivalent to `VTask.LimZero f`, but belongs to the completed field and requires the completion to be constructed.