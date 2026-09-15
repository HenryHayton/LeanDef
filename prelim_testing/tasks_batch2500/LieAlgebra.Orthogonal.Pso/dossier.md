## VTask.Pso

### Object

Given a commutative ring `R` and an element `i` of `R`, `VTask.Pso p q R i` is the diagonal matrix indexed by the disjoint union type `p ⊕ q`, whose diagonal entries are `1` at every index coming from the left summand `p` and `i` at every index coming from the right summand `q`. Its intended use is as a change-of-basis matrix that, when `i` is a square root of −1 (i.e. `i² = −1`), converts the indefinite diagonal bilinear form (with signature `(p, q)`) into the positive-definite one.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Pso : (p : Type u_2) -> (q : Type u_3) -> (R : Type u₂) -> [DecidableEq p] -> [DecidableEq q] -> [CommRing R] -> (i : R) -> Matrix (p ⊕ q) (p ⊕ q) R
<!-- PINNED-SIGNATURE:END -->


`p` and `q` are the index types that together form the row and column index set `p ⊕ q` of the square matrix; they require decidable equality so that the diagonal construction is well-defined. `R` is the coefficient commutative ring. `i` is the ring element placed on the diagonal at every index belonging to the right summand `q`; it is intended to be a square root of −1, though no algebraic constraint on `i` is imposed by the definition itself.

### Conventions

No junk-value or edge conventions are declared for this definition: the matrix is well-defined for any element `i` in any commutative ring `R`, and the index types `p` and `q` may be any types with decidable equality, including empty types (in which case the corresponding block of the diagonal simply vanishes).

### Worked examples

- Claim: For the `(Fin 2) ⊕ (Fin 1)` case over the integers with `i = 0`, the matrix `VTask.Pso (Fin 2) (Fin 1) ℤ 0` has a `1` at position `(Sum.inl 0, Sum.inl 0)` and a `0` at position `(Sum.inr 0, Sum.inr 0)`.
  ```lean
  example : VTask.Pso (Fin 2) (Fin 1) ℤ 0 (Sum.inl 0) (Sum.inl 0) = 1 ∧
            VTask.Pso (Fin 2) (Fin 1) ℤ 0 (Sum.inr 0) (Sum.inr 0) = 0 := by
    constructor <;> decide
  ```

- Claim: For the `(Fin 1) ⊕ (Fin 1)` case over ℤ with `i = -1`, the `(Sum.inr 0, Sum.inr 0)` entry is `−1` and the `(Sum.inl 0, Sum.inl 0)` entry is `1`.
  ```lean
  example : VTask.Pso (Fin 1) (Fin 1) ℤ (-1) (Sum.inl 0) (Sum.inl 0) = 1 ∧
            VTask.Pso (Fin 1) (Fin 1) ℤ (-1) (Sum.inr 0) (Sum.inr 0) = -1 := by
    constructor <;> decide
  ```

- Claim: For any index `j` in the left summand `p`, the `(Sum.inl j, Sum.inl j)` diagonal entry of `VTask.Pso p q R i` equals `1`.

- Claim: For any index `k` in the right summand `q`, the `(Sum.inr k, Sum.inr k)` diagonal entry of `VTask.Pso p q R i` equals `i`.

- Claim: All off-diagonal entries of `VTask.Pso p q R i` are `0`.

### Boundaries

- When `p` is the empty type, the entire matrix is indexed only over the right summand `q`, and every diagonal entry equals `i`; the transformation acts as scalar multiplication by `i`.
- When `q` is the empty type, the entire matrix is indexed only over `p`, and every diagonal entry equals `1`; the matrix is the identity.
- When both `p` and `q` are empty, the matrix is the unique `0×0` empty matrix.
- When `i = 1`, the matrix is the identity matrix regardless of the sizes of `p` and `q`.
- When `i = 0`, the right-summand block of the diagonal is zero, making the matrix singular.
- The definition does not enforce `i² = −1`; users wishing to invoke the transformation property between indefinite and definite forms must supply that hypothesis separately.

### Not to be confused with

- The identity matrix `Matrix.one` over `p ⊕ q`: that sets all diagonal entries to `1`, whereas `VTask.Pso` sets the right-block entries to `i`.
- A block-diagonal matrix with two separate matrix blocks: `VTask.Pso` is a single diagonal matrix, not a `Matrix.fromBlocks` construction.
- The indefinite bilinear form matrix itself (with `1`s and `−1`s on the diagonal): `VTask.Pso` is the *change-of-basis* tool, not the form matrix.
