## VTask.castOrderIso

### Object

`VTask.castOrderIso eq` is the canonical order isomorphism between `Fin n` and `Fin m` that is induced by the equality proof `eq : n = m`. It transports every element `i : Fin n` to the element of `Fin m` with the same underlying natural-number value, and it does so in a way that strictly preserves and reflects the natural ordering (`≤`) on both types. Because it merely reinterprets the index bound rather than permuting entries, it is the unique monotone bijection that acts as the identity on underlying natural numbers.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.castOrderIso : {m n : ℕ} -> (eq : n = m) -> Fin n ≃o Fin m
<!-- PINNED-SIGNATURE:END -->


`{m n : ℕ} -> (eq : n = m) -> Fin n ≃o Fin m`

The implicit arguments `m` and `n` are the two natural-number bounds being identified. The explicit argument `eq` is the proof that `n` equals `m`; it is the sole datum that justifies the construction and determines the direction of the isomorphism.

### Conventions

No special junk-value or boundary conventions are declared: the definition is total and well-behaved for every equality proof `eq`; the only case is `n = m`.

### Worked examples

- Claim: Applying `VTask.castOrderIso rfl` to `(2 : Fin 5)` yields `(2 : Fin 5)`, because the equality is reflexive and the underlying value is unchanged.
  ```lean
  example : (VTask.castOrderIso rfl : Fin 5 ≃o Fin 5) ⟨2, by norm_num⟩ = ⟨2, by norm_num⟩ := by
    simp [VTask.castOrderIso]
  ```

- Claim: When `eq : 3 = 3`, `VTask.castOrderIso eq` equals the identity order isomorphism `OrderIso.refl (Fin 3)`, since there is only one such isomorphism acting trivially on the underlying values.

- Claim: The symmetry of `VTask.castOrderIso eq` (where `eq : n = m`) equals `VTask.castOrderIso eq.symm`, meaning reversing the iso corresponds to using the reversed equality proof.

- Claim: For `eq : 4 = 4 := rfl`, the element `(0 : Fin 4)` maps to `(0 : Fin 4)` and the order relation `(0 : Fin 4) ≤ (3 : Fin 4)` is preserved, i.e., the image of `0` is still `≤` the image of `3`.

### Boundaries

- When `eq` is `rfl` (i.e., `n = n`), the isomorphism is definitionally equal to the identity on `Fin n` as an order isomorphism.
- Because both `n` and `m` must be equal, the only edge case is the reflexive one; there is no non-trivial degenerate input.
- The isomorphism preserves and reflects `≤` exactly: `i ≤ j` in `Fin n` if and only if the images are `≤` in `Fin m`.
- For `n = 0`, both `Fin 0` and `Fin m` (with `m = 0`) are empty, and the isomorphism is the unique empty order isomorphism.

### Not to be confused with

- `Fin.castEmb` / `Fin.castLE`: These produce order embeddings (or mere functions) when one bound is ≤ the other, not requiring equality and not yielding an isomorphism.
- `Equiv.cast`: This is a plain type-theoretic equivalence derived from `n = m` acting on `Fin`; it does not carry the order-isomorphism structure.
- `OrderIso.refl`: This is the identity order isomorphism on a fixed type; `VTask.castOrderIso rfl` reduces to it, but the general form takes a proof of equality as data.
