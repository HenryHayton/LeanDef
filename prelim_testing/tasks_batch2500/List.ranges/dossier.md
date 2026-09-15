## Object

`VTask.ranges` takes a list of natural numbers and produces a list of lists of natural numbers that partitions the consecutive range `[0, 1, …, sum − 1]` into contiguous blocks whose sizes match the original list entries.

More precisely, if the input is `[a₀, a₁, …, aₙ₋₁]`, the output is a list of `n` sublists where the `i`-th sublist is a consecutive block of `aᵢ` integers, the blocks are pairwise disjoint, every block is duplicate-free, and together they cover exactly `List.range (a₀ + a₁ + … + aₙ₋₁)`.

Example: `[1, 2, 3].ranges = [[0], [1, 2], [3, 4, 5]]`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ranges : List ℕ → List (List ℕ)
<!-- PINNED-SIGNATURE:END -->


`VTask.ranges : List ℕ → List (List ℕ)`

The single argument is the list of block sizes. Each entry specifies how many consecutive natural numbers should appear in the corresponding output sublist.

## Conventions

The input list is unrestricted: the empty list `[]` maps to `[]`, and any entry equal to `0` produces an empty sublist `[]` in the corresponding position.

## Worked examples

- Claim: `VTask.ranges [] = []`
  ```lean
  example : VTask.ranges [] = [] := by decide
  ```

- Claim: `VTask.ranges [1, 2, 3] = [[0], [1, 2], [3, 4, 5]]`
  ```lean
  example : VTask.ranges [1, 2, 3] = [[0], [1, 2], [3, 4, 5]] := by decide
  ```

- Claim: `VTask.ranges [0, 3] = [[], [0, 1, 2]]`
  ```lean
  example : VTask.ranges [0, 3] = [[], [0, 1, 2]] := by decide
  ```

- Claim: `(VTask.ranges [1, 2, 3]).map List.length = [1, 2, 3]`
  ```lean
  example : (VTask.ranges [1, 2, 3]).map List.length = [1, 2, 3] := by decide
  ```

- Claim: `(VTask.ranges [2, 3]).flatten = List.range 5`
  ```lean
  example : (VTask.ranges [2, 3]).flatten = List.range 5 := by decide
  ```

## Boundaries

- **Empty input**: `VTask.ranges [] = []`, the empty list of blocks.
- **Zero-sized block**: A `0` entry in the input produces an empty sublist `[]` at that position; the length map still reflects the `0`, and the join is unaffected.
- **Single entry**: `VTask.ranges [n] = [List.range n]`, a single block covering `0` through `n − 1`.
- **All zeros**: `VTask.ranges [0, 0, …, 0]` is a list of empty lists, and the join is `[]`.

## Not to be confused with

- `List.range n`: produces a single flat list `[0, 1, …, n − 1]`; `VTask.ranges` partitions such a range into multiple sublists.
- `List.splitAt` / `List.splitAtOn`: splits a list at a specific index or element rather than partitioning a range by prescribed block sizes.
- `List.groupBy`: groups elements by a predicate on adjacent pairs, not by prescribed integer lengths.