## Object

`VTask.stream v` is an infinite stream (indexed by natural numbers) of optional integer–fractional-part pairs that encodes the successive steps of the continued-fraction algorithm applied to a value `v` in a linearly-ordered division ring with a floor operation. At index 0 it records the integer part `⌊v⌋` and the fractional part `v − ⌊v⌋`. At each subsequent index it takes the fractional part produced at the previous step, inverts it, and again records the integer and fractional parts of that inverse — unless the fractional part was zero, in which case every subsequent entry is `none`. The resulting sequence of integer parts is precisely the sequence of partial quotients of the continued-fraction expansion of `v`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.stream : {K : Type u_1} -> [DivisionRing K] -> [LinearOrder K] -> [FloorRing K] -> (v : K) -> Stream' (Option (GenContFract.IntFractPair K))
<!-- PINNED-SIGNATURE:END -->


`VTask.stream : {K : Type u_1} -> [DivisionRing K] -> [LinearOrder K] -> [FloorRing K] -> (v : K) -> Stream' (Option (GenContFract.IntFractPair K))`

The type parameter `K` is the ambient linearly-ordered division ring equipped with a floor function (e.g. `ℚ`, `ℝ`, or any `FloorRing`). The three instance arguments supply, respectively, the division-ring structure, the linear order, and the floor operation on `K`. The explicit argument `v` is the value whose continued-fraction decomposition is being computed; all stream indices implicitly quantify over `ℕ`.

## Conventions

The stream is "sequential" in the sense that once an entry is `none`, every subsequent entry is also `none` — i.e. `VTask.stream v` satisfies the `Stream'.IsSeq` predicate. There is no separate junk value for the integer part when the fractional part is zero; instead the entire pair becomes `none` on the very next step. For rational inputs the stream always eventually terminates (reaches `none`); for irrational reals the stream is infinite with no `none` entries.

## Worked examples

- Claim: For `v = (3.4 : ℚ)`, `VTask.stream v 0 = some ⟨3, 2/5⟩` (integer part 3, fractional part 2/5).

- Claim: For `v = (3.4 : ℚ)`, `VTask.stream v 2 = some ⟨2, 0⟩` (integer part 2, fractional part 0).

- Claim: For `v = (3.4 : ℚ)`, `VTask.stream v 3 = none`, because the fractional part at index 2 is 0.

- Claim: For any integer `a : ℤ` embedded in `K`, `VTask.stream (a : K) 1 = none`, because the fractional part of an integer is 0.

## Boundaries

- **At index 0**: Always `some ⟨⌊v⌋, v − ⌊v⌋⟩`; never `none`, regardless of `v`.
- **Fractional part is 0 at index n**: The entry at index `n` is `some ⟨b, 0⟩` for some integer `b`, and every entry at index `n+1` and beyond is `none`.
- **Integer inputs**: For `v` an integer (fractional part = 0), `VTask.stream v 0 = some ⟨v, 0⟩` and `VTask.stream v k = none` for all `k ≥ 1`.
- **Rational inputs**: The stream always eventually becomes `none`; the numerator of the fractional part strictly decreases at each step, so termination is guaranteed in finitely many steps.
- **Irrational inputs** (e.g. over `ℝ`): The stream never reaches `none`; every entry is `some` and fractional parts are always nonzero.
- **Sequential property**: Once `none` appears, it cannot be followed by `some`; `VTask.stream v` is always a `Stream'.IsSeq`.

## Not to be confused with

- `GenContFract.of`: The generalised continued fraction itself, built from this stream's integer parts; `VTask.stream` is the auxiliary computation feeding `GenContFract.of`, not the fraction object.
- `GenContFract.IntFractPair.of`: The single-step pairing `⟨⌊v⌋, v − ⌊v⌋⟩` for one value; `VTask.stream` is the iterated application of this pairing to successive inverses.
- `Int.fract`: The plain fractional-part function `v − ⌊v⌋ : K`; `VTask.stream` wraps this together with the integer part and iterates it, whereas `Int.fract` is just the scalar value at a single step.