## VTask.stirlingFirst

### Object

The unsigned Stirling number of the first kind, written $c(n,k)$ or $\left[{n \atop k}\right]$. It counts the number of permutations of an $n$-element set whose cycle decomposition consists of exactly $k$ disjoint cycles. Because it counts combinatorial objects, the value is always a non-negative integer. The word "unsigned" distinguishes it from the signed variant $s(n,k)=(-1)^{n-k}c(n,k)$ that arises in the theory of falling factorials.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.stirlingFirst : ℕ → ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.stirlingFirst : ℕ → ℕ → ℕ`

The first argument is the number of elements being permuted. The second argument is the prescribed number of disjoint cycles that the permutation must have.

### Conventions

By convention, the number of permutations of the empty set (0 elements) having exactly 0 cycles is taken to be 1 (the empty permutation counts as having zero cycles). For any positive number of cycles $k \geq 1$, the empty set contributes 0 permutations, so `VTask.stirlingFirst 0 (k+1) = 0`. Symmetrically, a non-empty set of $n+1$ elements cannot be permuted into 0 cycles, so `VTask.stirlingFirst (n+1) 0 = 0`. When $k > n$, one cannot form $k$ cycles from only $n$ elements, so the value is 0.

### Worked examples

- Claim: `VTask.stirlingFirst 0 0 = 1` (the unique empty permutation has zero cycles)
  ```lean
  example : VTask.stirlingFirst 0 0 = 1 := by decide
  ```

- Claim: `VTask.stirlingFirst 4 2 = 11` (there are 11 permutations of {1,2,3,4} with exactly 2 cycles)
  ```lean
  example : VTask.stirlingFirst 4 2 = 11 := by decide
  ```

- Claim: `VTask.stirlingFirst 4 4 = 1` (the only way to have 4 cycles on 4 elements is the identity, with four fixed points)
  ```lean
  example : VTask.stirlingFirst 4 4 = 1 := by decide
  ```

- Claim: `VTask.stirlingFirst 5 1 = 24` (permutations of 5 elements forming a single cycle; equals 4!)
  ```lean
  example : VTask.stirlingFirst 5 1 = 24 := by decide
  ```

- Claim: For any $n$, `VTask.stirlingFirst (n+1) n = (n+1).choose 2`, i.e., the second-from-diagonal entry equals the binomial coefficient $\binom{n+1}{2}$.

- Claim: For any $n$, `VTask.stirlingFirst (n+1) 1 = n.factorial`, i.e., the number of permutations of $n+1$ elements forming exactly one cycle is $n!$.

### Boundaries

- `VTask.stirlingFirst 0 0 = 1`: the empty permutation is counted once.
- `VTask.stirlingFirst 0 k = 0` for all `k ≥ 1`: no non-trivial cycle structure exists on an empty set.
- `VTask.stirlingFirst n 0 = 0` for all `n ≥ 1`: a non-empty set always has at least one cycle.
- `VTask.stirlingFirst n k = 0` whenever `k > n`: you cannot have more cycles than elements.
- `VTask.stirlingFirst n n = 1` for all `n`: the only permutation with $n$ cycles on $n$ elements is the identity (every element a fixed point, i.e., a 1-cycle).
- The recurrence `VTask.stirlingFirst (n+1) (k+1) = n * VTask.stirlingFirst n (k+1) + VTask.stirlingFirst n k` reflects inserting the new element either into one of the $n$ positions within existing cycles (first term) or forming a new singleton cycle (second term).

### Not to be confused with

- **Stirling numbers of the second kind** (`Nat.stirlingSecond`): those count partitions of an $n$-set into exactly $k$ non-empty subsets, not permutation cycle structures.
- **Signed Stirling numbers of the first kind**: the signed variant $s(n,k) = (-1)^{n-k} c(n,k)$ arises in expanding falling factorials as polynomials; `VTask.stirlingFirst` is always non-negative.
- **Binomial coefficients** (`Nat.choose`): although `VTask.stirlingFirst (n+1) n = Nat.choose (n+1) 2`, the two functions differ for other arguments and have different combinatorial meanings.