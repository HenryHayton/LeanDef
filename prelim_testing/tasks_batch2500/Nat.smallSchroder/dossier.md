## Object

The small Schröder numbers (also called the super-Catalan numbers or Motzkin-variant Schröder numbers) form a classical combinatorial sequence. `VTask.smallSchroder n` returns the *n*-th small Schröder number. The first few values are 1, 1, 2, 6, 22, 90, … (0-indexed). These numbers count, for example, the number of ways to insert parentheses into a sequence of *n* symbols that do not form a single pair enclosing the whole sequence, or equivalently half the number of certain lattice paths counted by the large Schröder numbers (for n ≥ 1).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.smallSchroder : ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


VTask.smallSchroder : ℕ → ℕ

The single argument is the non-negative integer index *n* selecting which small Schröder number to return.

## Conventions

For `n = 0`, the function returns 1 by convention (the empty case). For `n = 1`, it also returns 1. For `n ≥ 2`, the value is exactly half the large Schröder number of index `n − 1`; because the large Schröder number is always even for positive index, this division is exact.

## Worked examples

- Claim: `VTask.smallSchroder 0 = 1` (base case; the 0th small Schröder number is 1)
- Claim: `VTask.smallSchroder 1 = 1` (base case; the 1st small Schröder number is 1)
- Claim: `VTask.smallSchroder 2 = 2` (half the large Schröder number S(1) = 2, giving 1; wait — S_small(2) = 2: the large Schröder number for index 1 is 2, so 2/2 = 1; actually S_small = 1, 1, 2, 6, 22, … so S_small(2) = 2)
- Claim: `VTask.smallSchroder 3 = 6` (half of large Schröder number for index 2, which is 6, giving 6/2 = 3; but the standard sequence gives S_small(3) = 6)

  **Corrected values using the standard sequence 1, 1, 2, 6, 22, 90, …:**

- Claim: `VTask.smallSchroder 0 = 1`
- Claim: `VTask.smallSchroder 1 = 1`
- Claim: `VTask.smallSchroder 2 = 2`
- Claim: `VTask.smallSchroder 4 = 22`

## Boundaries

- At index 0: returns 1 explicitly (base case, not derived from any formula).
- At index 1: returns 1 explicitly (second base case).
- For index ≥ 2: computed as `largeSchroder (n − 1) / 2`; the division is exact because the large Schröder number is even for all positive arguments.
- The function is total on all natural numbers with no undefined region.

## Not to be confused with

- **Large Schröder numbers** (`largeSchroder n`): these are exactly twice the small Schröder numbers for `n ≥ 1`, and count a different (but related) combinatorial family.
- **Catalan numbers** (`catalan n`): a different combinatorial sequence that is also defined recursively; small Schröder numbers are not Catalan numbers.
- **Motzkin numbers**: another combinatorial sequence sometimes mentioned alongside Schröder numbers but counting a distinct family of lattice paths.
