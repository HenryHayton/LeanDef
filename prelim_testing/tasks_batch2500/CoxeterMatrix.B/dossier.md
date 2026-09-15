## Object

`VTask.B n` is the Coxeter matrix that encodes the Coxeter group of type Bₙ. It is an `n × n` symmetric matrix (indexed by `Fin n`) whose entries specify the orders of products of pairs of simple reflections in the Bₙ Coxeter group. The associated Coxeter–Dynkin diagram is a straight chain of `n` nodes where all consecutive pairs of nodes are connected by an edge of weight 3 (meaning the two reflections braid to order 3), except for the unique edge between the last two nodes (indices `n−1` and `n−2`), which has weight 4. Diagonal entries are all 1, and non-adjacent pairs of nodes have weight 2 (reflections commute).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.B : (n : ℕ) -> CoxeterMatrix (Fin n)
<!-- PINNED-SIGNATURE:END -->


`VTask.B : (n : ℕ) -> CoxeterMatrix (Fin n)`

The single argument `n` is the rank of the Coxeter system — equivalently, the number of nodes in the Coxeter–Dynkin diagram and the number of simple reflections. The result is a `CoxeterMatrix` whose index type is `Fin n`, i.e., the set `{0, 1, …, n−1}`.

## Conventions

For the degenerate rank `n = 0` the matrix is vacuously defined on the empty index set, yielding an empty Coxeter matrix. For `n = 1` the single off-diagonal pair is absent, so no special edge exists and the matrix is just `[1]`. For `n = 2` the two nodes are both adjacent and would simultaneously qualify as the "last pair", so the sole off-diagonal entry is 4, giving the dihedral group of order 8. The labelling convention places the weight-4 edge at the **high-index** end of the chain (between nodes `n−1` and `n−2`), matching the standard Bourbaki convention for Bₙ.

## Worked examples

- Claim: For n = 4, the entry `(VTask.B 4).M ⟨3, by omega⟩ ⟨2, by omega⟩` equals 4, since nodes 3 and 2 are the last two nodes of the B₄ diagram.
  ```lean
  example : (VTask.B 4).M ⟨3, by omega⟩ ⟨2, by omega⟩ = 4 := by decide
  ```

- Claim: For n = 4, the entry `(VTask.B 4).M ⟨1, by omega⟩ ⟨0, by omega⟩` equals 3, since nodes 1 and 0 are adjacent but not the last pair.
  ```lean
  example : (VTask.B 4).M ⟨1, by omega⟩ ⟨0, by omega⟩ = 3 := by decide
  ```

- Claim: For n = 4, the entry `(VTask.B 4).M ⟨0, by omega⟩ ⟨2, by omega⟩` equals 2, since nodes 0 and 2 are not adjacent.
  ```lean
  example : (VTask.B 4).M ⟨0, by omega⟩ ⟨2, by omega⟩ = 2 := by decide
  ```

- Claim: For n = 4, all diagonal entries equal 1.
  ```lean
  example : (VTask.B 4).M ⟨2, by omega⟩ ⟨2, by omega⟩ = 1 := by decide
  ```

- Claim: The matrix `VTask.B 4` is symmetric, i.e., its (3,2)-entry equals its (2,3)-entry.
  ```lean
  example : (VTask.B 4).M ⟨3, by omega⟩ ⟨2, by omega⟩ = (VTask.B 4).M ⟨2, by omega⟩ ⟨3, by omega⟩ := by decide
  ```

## Boundaries

- **n = 0**: The index type `Fin 0` is empty, so the matrix has no entries. This is a valid, vacuous Coxeter matrix.
- **n = 1**: Only one node; the matrix is the 1×1 matrix `[1]`. The Coxeter group is trivial.
- **n = 2**: There are only two nodes, which are both "adjacent" (consecutive) and also "the last two nodes", so the single off-diagonal entry is 4. The Coxeter group is the dihedral group of order 8, also known as B₂ ≅ C₂.
- **n = 3**: The diagram has a weight-4 edge between nodes 2 and 1, and a weight-3 edge between nodes 1 and 0. This is the standard B₃.
- Off-diagonal entries are always in {2, 3, 4}; they are never 1 (guaranteed by the `off_diagonal` field of `CoxeterMatrix`).

## Not to be confused with

- `CoxeterMatrix.A n`: The Coxeter matrix of type Aₙ, which has all consecutive-edge weights equal to 3 and no weight-4 edge; it is the "uniform chain" diagram without a special end.
- `CoxeterMatrix.D n`: The Coxeter matrix of type Dₙ, which has a branching at one end of the diagram rather than a weight-4 edge.
- The abstract `CoxeterMatrix` structure itself: `VTask.B n` is a specific *instance* of that structure, not the general concept of a Coxeter matrix.