## VTask.reduce

### Object

`VTask.reduce` is a retraction from the set of 2×2 integer matrices of fixed determinant `m` to itself that moves any such matrix towards a canonical representative element. Concretely, it applies a finite sequence of elementary transformations (left-multiplications by the modular-group generators `S` and `T`) to the input matrix until the result lands in the distinguished set `reps m` of canonical representatives. The process terminates because each non-final step strictly decreases the absolute value of the lower-left entry of the matrix.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.reduce : {m : ℤ} -> FixedDetMatrix (Fin 2) ℤ m → FixedDetMatrix (Fin 2) ℤ m
<!-- PINNED-SIGNATURE:END -->


```
VTask.reduce : {m : ℤ} -> FixedDetMatrix (Fin 2) ℤ m → FixedDetMatrix (Fin 2) ℤ m
```

The implicit argument `m : ℤ` is the fixed determinant shared by every matrix in the domain and codomain. The explicit argument is a 2×2 integer matrix whose determinant equals `m`, viewed as an element of the subtype `FixedDetMatrix (Fin 2) ℤ m`; it is the matrix to be reduced.

### Conventions

The function is total: it is defined for every integer `m` and every element of `FixedDetMatrix (Fin 2) ℤ m`, including the case `m = 0`. When `m = 0` the image is still a well-typed element of `FixedDetMatrix (Fin 2) ℤ 0`, but the guarantee that the output lies in `reps m` is only stated (and meaningful) for `m ≠ 0`.

Integer division used internally follows Lean/Mathlib's truncated-toward-zero convention for `ℤ`, so the two branches involving `A.1 0 1 / A.1 1 1` and `-A.1 0 1 / -A.1 1 1` are not necessarily equal even when the numerators and denominators are negatives of each other.

### Worked examples

- Claim: For any `A : FixedDetMatrix (Fin 2) ℤ m` with `A.1 1 0 = 0` and `0 < A.1 0 0`, the result `VTask.reduce A` equals `(T ^ (-(A.1 0 1 / A.1 1 1))) • A` (the `reduce_of_pos` branch).

- Claim: For any nonzero `m : ℤ` and any `A : FixedDetMatrix (Fin 2) ℤ m`, the element `VTask.reduce A` belongs to `reps m`.

- Claim: For any `A : FixedDetMatrix (Fin 2) ℤ m` with `A.1 1 0 ≠ 0`, the reduction of `A` equals the reduction of `reduceStep A`, i.e. `VTask.reduce (reduceStep A) = VTask.reduce A`.

- Claim: For any `A : FixedDetMatrix (Fin 2) ℤ m` with `A.1 1 0 = 0` and `¬ 0 < A.1 0 0`, the result `VTask.reduce A` equals `(T ^ (-(-A.1 0 1 / -A.1 1 1))) • (S • (S • A))` (the `reduce_of_not_pos` branch).

### Boundaries

- When the lower-left entry `A.1 1 0` is already zero and the top-left entry `A.1 0 0` is positive, the function returns in one step by applying a power of `T` that adjusts the top-right entry.
- When `A.1 1 0 = 0` but `A.1 0 0 ≤ 0`, the function first applies `S • S` (which effectively negates the matrix up to the fixed-determinant constraint) and then applies a power of `T`; this handles the case where the diagonal is non-positive.
- When `A.1 1 0 ≠ 0`, the function recurses on `reduceStep A`, which strictly decreases `|A.1 1 0|`, guaranteeing termination.
- The guarantee `VTask.reduce A ∈ reps m` requires `m ≠ 0`; for `m = 0` the output is still a well-formed element of the subtype but no canonical-form claim is made.

### Not to be confused with

- `reduceStep`: a single elementary step that decreases `|A.1 1 0|` by one application of the Euclidean algorithm; `VTask.reduce` iterates `reduceStep` until completion.
- `reps m`: the target set of canonical representatives; `VTask.reduce` maps *into* this set but is not the inclusion of `reps m`.
- The `S` and `T` generators of the modular group acting on `FixedDetMatrix`: these are the building blocks used inside `VTask.reduce`, not the reduction map itself.