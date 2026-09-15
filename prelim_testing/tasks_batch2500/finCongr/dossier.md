## Object

`VTask.finCongr` is the canonical "identity" equivalence (a bijection with explicit inverse) between the finite type `Fin n` and the finite type `Fin m`, valid whenever the natural numbers `n` and `m` are propositionally equal. Concretely, it recasts an element of `Fin n` to an element of `Fin m` by substituting the proof `n = m` into the bound, leaving the underlying natural-number value unchanged in both directions.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finCongr : {n m : ℕ} -> (eq : n = m) -> Fin n ≃ Fin m
<!-- PINNED-SIGNATURE:END -->


`VTask.finCongr : {n m : ℕ} -> (eq : n = m) -> Fin n ≃ Fin m`

The two natural-number arguments `n` and `m` are implicit and inferred from context; they are the sizes of the two finite types being identified. The explicit argument `eq` is a proof that `n` equals `m`, which licenses the identification. The result is a bundled equivalence `Fin n ≃ Fin m`, packaging the forward map, the inverse map, and the proofs that each is a left and right inverse of the other.

## Conventions

There are no junk-value or out-of-domain conventions to declare: the function is total and well-defined for every proof `eq : n = m` over all natural numbers `n` and `m`.

## Worked examples

- Claim: Applying `VTask.finCongr` to the reflexivity proof `rfl : 3 = 3` yields an equivalence whose forward function sends `⟨1, by omega⟩ : Fin 3` to `⟨1, by omega⟩ : Fin 3`, preserving the underlying value.

- Claim: If `h : 2 = 2` then `(VTask.finCongr h).toFun ⟨0, by omega⟩ = ⟨0, by omega⟩`.
  ```lean
  example : (VTask.finCongr (rfl : 2 = 2)).toFun ⟨0, by omega⟩ = ⟨0, by omega⟩ := by decide
  ```

- Claim: The inverse of the forward map is the identity: for any `i : Fin 3`, `(VTask.finCongr rfl).invFun ((VTask.finCongr rfl).toFun i) = i`.
  ```lean
  example (i : Fin 3) : (VTask.finCongr (rfl : 3 = 3)).invFun ((VTask.finCongr rfl).toFun i) = i := by
    simp [VTask.finCongr]
  ```

- Claim: When `h : 4 = 4`, the equivalence `VTask.finCongr h` has `toFun ⟨3, by omega⟩ = ⟨3, by omega⟩`.
  ```lean
  example : (VTask.finCongr (rfl : 4 = 4)).toFun ⟨3, by omega⟩ = ⟨3, by omega⟩ := by decide
  ```

## Boundaries

- When `n = m = 0`, the equivalence is between two empty types (`Fin 0`); it is perfectly well-formed and is vacuously both a left and a right inverse of itself.
- When `eq` is `rfl` (the reflexivity proof), the equivalence is the identity equivalence on `Fin n`.
- The underlying natural-number value of any element is preserved by both the forward and inverse maps; only the type-level bound changes.
- The function accepts any proof `eq : n = m`, not just `rfl`; all such proofs are propositionally equal (by proof irrelevance), so the resulting equivalence is independent of which proof is supplied.

## Not to be confused with

- `Fin.cast`: the bare function `Fin n → Fin m` underlying the forward direction, without the bundled inverse or the proof of bijectivity.
- `Equiv.refl (Fin n)`: the reflexive equivalence on `Fin n` specifically when `n = n`; `VTask.finCongr rfl` reduces to this, but `VTask.finCongr` also covers the heterogeneous case `n = m` for distinct expressions `n` and `m`.
- `finRotate` or other `Fin`-equivalences: those permute elements within a single `Fin n` rather than recasting between two types of equal size.