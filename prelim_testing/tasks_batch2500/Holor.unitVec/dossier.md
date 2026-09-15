## Object

`VTask.unitVec` produces the one-dimensional "standard basis" holor (think: a length-`d` array / rank-1 tensor) over a type `α` that carries both a multiplicative and an additive monoid structure. The holor has the multiplicative identity `1` at index position `j` and the additive identity `0` everywhere else. This is the discrete analogue of a standard basis vector in a vector space, expressed in the `Holor` framework.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.unitVec : {α : Type} -> [Monoid α] -> [AddMonoid α] -> (d j : ℕ) -> Holor α [d]
<!-- PINNED-SIGNATURE:END -->


`VTask.unitVec : {α : Type} -> [Monoid α] -> [AddMonoid α] -> (d j : ℕ) -> Holor α [d]`

The implicit type argument `α` is the scalar type of the holor, which must be equipped with both a multiplicative monoid structure (providing `1`) and an additive monoid structure (providing `0`). The first explicit argument `d` is the length (dimension) of the resulting rank-1 holor — it determines how many positions the holor spans. The second explicit argument `j` is the index of the "hot" position where the value is `1`; all other positions hold `0`.

## Conventions

When the "hot" index `j` is out of bounds (i.e., `j ≥ d`), the holor is still well-formed and entirely zero, since no valid index into a length-`d` holor can equal `j`; the definition is total and makes no restriction on `j` relative to `d`.

## Worked examples

- Claim: For `α = ℤ`, `VTask.unitVec 3 1` evaluated at index `[1]` equals `1` and at index `[0]` equals `0`.

- Claim: `VTask.unitVec 4 2` is a length-4 holor over `ℤ` with value `1` at position 2 and `0` at all other positions (0, 1, 3).

- Claim: When `j` equals `d` (out of bounds), `VTask.unitVec 3 3` over `ℤ` is the zero holor of length 3, since no valid index `[i]` with `i < 3` satisfies `i = 3`.

- Claim: For `d = 1` and `j = 0`, `VTask.unitVec 1 0` over `ℕ` is the length-1 holor containing only `1`.

## Boundaries

- **`j` in bounds (`j < d`):** Exactly one position (the `j`-th) holds `1`; all others hold `0`. This is the standard unit-vector behaviour.
- **`j` out of bounds (`j ≥ d`):** The condition `ti.1 = [j]` can never be satisfied by any valid index into a length-`d` holor, so the result is the all-zero holor of length `d`. No error is raised; the definition is total.
- **`d = 0`:** The holor has no valid indices at all, so it is vacuously the empty holor regardless of `j`.
- **`j = 0`, `d = 1`:** The single-entry holor contains exactly `1`.

## Not to be confused with

- `Holor.unit` (if it exists): a potential multiplicative unit or identity element for holor multiplication, not a basis vector.
- A standard `Matrix.stdBasisMatrix` or `LinearMap.stdBasis`: these operate in the `Matrix`/`Finsupp` world and carry different type and index structure from `Holor`.
- `Pi.single`: a function that places a single specified value at one index in a `Pi` type; similar in spirit but lives in a different type family and does not use the `Holor` index-list representation.