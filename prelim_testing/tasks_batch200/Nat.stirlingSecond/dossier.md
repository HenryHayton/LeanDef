## Object

The Stirling number of the second kind, commonly written S(n, k) or {n \brack k} in combinatorics, counts the number of ways to partition a set of n labelled elements into exactly k non-empty, unordered subsets. It is a fundamental quantity in enumerative combinatorics, appearing in the study of set partitions, the connection coefficients between the standard and falling-factorial polynomial bases, and the analysis of hash functions and occupancy problems.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.stirlingSecond : ℕ → ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.stirlingSecond : ℕ → ℕ → ℕ`

The first argument n is the size of the set being partitioned; the second argument k is the prescribed number of non-empty blocks in the partition.

## Conventions

The empty partition (zero elements into zero blocks) is counted as exactly one partition, so S(0, 0) = 1 by convention. Attempting to partition zero elements into one or more non-empty blocks is impossible, giving S(0, k) = 0 for k ≥ 1. Attempting to partition a non-empty set into zero blocks is equally impossible, giving S(n, 0) = 0 for n ≥ 1. When k > n, no surjective assignment exists, so S(n, k) = 0 for k > n.

## Worked examples

- Claim: VTask.stirlingSecond 0 0 = 1 (the unique empty partition)
  ```lean
  example : VTask.stirlingSecond 0 0 = 1 := by decide
  ```

- Claim: VTask.stirlingSecond 3 2 = 3 (the three partitions of {1,2,3} into 2 non-empty blocks are {1,2}|{3}, {1,3}|{2}, {2,3}|{1})
  ```lean
  example : VTask.stirlingSecond 3 2 = 3 := by decide
  ```

- Claim: VTask.stirlingSecond 4 2 = 7
  ```lean
  example : VTask.stirlingSecond 4 2 = 7 := by decide
  ```

- Claim: VTask.stirlingSecond 5 3 = 25
  ```lean
  example : VTask.stirlingSecond 5 3 = 25 := by decide
  ```

- Claim: VTask.stirlingSecond 4 5 = 0 (cannot partition 4 elements into 5 non-empty blocks)
  ```lean
  example : VTask.stirlingSecond 4 5 = 0 := by decide
  ```

- Claim: VTask.stirlingSecond n n = 1 for all n (each element must be its own block)

- Claim: VTask.stirlingSecond (n+1) 1 = 1 for all n (only one way: put everything in one block)

- Claim: VTask.stirlingSecond (n+1) n = C(n+1, 2) for all n (exactly one pair must share a block)

## Boundaries

- S(0, 0) = 1: the empty set has exactly one partition into zero blocks (the empty partition).
- S(0, k) = 0 for k ≥ 1: there is no way to produce a non-empty block from an empty set.
- S(n, 0) = 0 for n ≥ 1: a non-empty set cannot be partitioned into zero blocks.
- S(n, k) = 0 whenever k > n: pigeonhole prevents surjection of n elements onto k non-empty blocks.
- S(n, n) = 1 for all n: the only partition into n non-empty blocks of an n-element set is the discrete partition into singletons.
- S(n+1, 1) = 1 for all n: the entire set forms the unique single block.
- The recurrence S(n+1, k+1) = (k+1)·S(n, k+1) + S(n, k) has a clean combinatorial interpretation: either the (n+1)-th element forms a singleton block (S(n, k) choices for the remaining n elements into k blocks), or it joins one of the existing k+1 blocks ((k+1)·S(n, k+1) ways).

## Not to be confused with

- **Stirling numbers of the first kind**: those count permutations of n elements with exactly k disjoint cycles, not set partitions into blocks.
- **Bell numbers**: the Bell number B(n) = Σ_k S(n, k) sums over all k, counting total set partitions without fixing the block count.
- **Binomial coefficients C(n, k)**: those count k-element subsets of an n-element set, not surjective partitions into k labelled or unlabelled blocks.