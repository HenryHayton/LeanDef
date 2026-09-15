## Object

A *slice* of a holor (a higher-order array/tensor indexed by a list of natural-number dimensions) is the sub-holor obtained by fixing the first index to a particular value `i`. Concretely, if `x` has shape `d :: ds` (so it is a rank-`(1 + |ds|)` tensor whose leading dimension has size `d`), then `VTask.slice x i h` has shape `ds` and its entries are exactly the entries of `x` whose first coordinate equals `i`. In matrix terms, slicing along the first dimension at index `i` is analogous to extracting the `i`-th row.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.slice : {α : Type} -> {d : ℕ} -> {ds : List ℕ} -> (x : Holor α (d :: ds)) -> (i : ℕ) -> (h : i < d) -> Holor α ds
<!-- PINNED-SIGNATURE:END -->


VTask.slice : {α : Type} -> {d : ℕ} -> {ds : List ℕ} -> (x : Holor α (d :: ds)) -> (i : ℕ) -> (h : i < d) -> Holor α ds

- `α` is the element type (the type of values stored in the holor, e.g., `ℝ` or `ℤ`).
- `d` is the size of the leading dimension of `x` (inferred from the holor's shape).
- `ds` is the list of remaining dimensions (the shape of each slice).
- `x` is the holor being sliced; it has shape `d :: ds`.
- `i` is the index along the first dimension at which the slice is taken; it must be a natural number.
- `h` is a proof that `i` is a valid index, i.e., `i < d`, ensuring the slice is in bounds.

The result is a holor of shape `ds` — one fewer dimension than `x`.

## Conventions

No special junk-value or out-of-bounds conventions are declared for this definition: the proof argument `h : i < d` statically enforces that only valid indices are accepted, so there is no out-of-range case to give a junk value to.

## Worked examples

- Claim: For a holor `x : Holor ℕ [2, 3]`, `VTask.slice x 0 (by omega)` has type `Holor ℕ [3]`, i.e., slicing reduces the leading dimension.

- Claim: If `x : Holor ℝ [2]` is defined by `x ⟨[j], _⟩ = if j = 0 then 1.0 else 2.0`, then `VTask.slice x 1 (by omega)` applied to the only valid `HolorIndex []` gives `2.0` — the entry at first index `1`.

- Claim: For a holor `x : Holor α [d]`, every `VTask.slice x i h` is a holor of shape `[]` (a scalar), and evaluating it at the unique `HolorIndex []` gives the same value as `x` evaluated at `⟨[i], …⟩`.

- Claim: Slices partition the entries of `x`: for each multi-index `(i, is)` into `x`, the entry `x[i, is]` equals `(VTask.slice x i h)[is]`.

## Boundaries

- The proof `h : i < d` is required; the function is not defined for `i ≥ d`. There is no fallback or junk value — the type system prevents calling `VTask.slice` with an out-of-range index.
- When `ds = []`, the result is a rank-0 holor (a scalar wrapper), not a bare value of type `α`. This is the base case when slicing down to a single element.
- When `d = 1`, the only valid index is `i = 0` (since `h : 0 < 1`), and the unique slice covers the entire holor content.
- The type `α` is unrestricted — `VTask.slice` works for any element type, whether or not it carries algebraic structure.

## Not to be confused with

- `Holor.unit`: constructs a specific standard-basis holor, not a subholor extracted by fixing an index.
- `List.get` / `Array.get`: retrieves a single scalar element from a sequence by index; `VTask.slice` instead returns a full sub-holor of lower rank, not a single value.
- `Matrix.vecMul` / row extraction on `Matrix`: conceptually similar (fixing a row index), but applies to 2-D matrices with a different type signature; `VTask.slice` generalises this to arbitrary rank.
