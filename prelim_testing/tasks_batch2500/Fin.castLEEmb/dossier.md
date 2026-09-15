## Object

`VTask.castLEEmb h` is the canonical injective embedding of `Fin n` into `Fin m`, valid whenever `n ≤ m`. It sends each element `i : Fin n` — a natural number strictly less than `n` — to the element of `Fin m` with the same underlying natural number value. The embedding packages both the underlying function and the proof that it is injective into a single bundled object of type `Fin n ↪ Fin m`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.castLEEmb : {n m : ℕ} -> (h : n ≤ m) -> Fin n ↪ Fin m
<!-- PINNED-SIGNATURE:END -->


`{n m : ℕ} -> (h : n ≤ m) -> Fin n ↪ Fin m`

The implicit arguments `n` and `m` are the source and target sizes; they are inferred from context. The explicit argument `h` is a proof that `n ≤ m`, which is the necessary and sufficient condition for the embedding to exist: every index valid in `Fin n` is automatically valid in `Fin m`. The result is the embedding itself.

## Conventions

There are no junk-value or degenerate-input conventions to declare: the definition is total over all `n`, `m`, and `h` satisfying the type, and the edge case `n = m` (where `h` is a proof of equality cast to `≤`) simply yields the identity embedding.

## Worked examples

- Claim: Applying `VTask.castLEEmb` with `n = 2`, `m = 5`, and `h : 2 ≤ 5` to `⟨1, by omega⟩ : Fin 2` yields `⟨1, by omega⟩ : Fin 5` (the underlying natural number is preserved).

- Claim: The image of the interval `Ico ⟨0, _⟩ ⟨2, _⟩` under `VTask.castLEEmb h` (with `h : 3 ≤ 5`) equals `Ico (castLE h ⟨0, _⟩) (castLE h ⟨2, _⟩)` in `Finset (Fin 5)`, consistent with `map_castLEEmb_Ico`.

- Claim: `VTask.castLEEmb` with `n = m` (equality case) is an embedding whose range is exactly `{i : Fin m | i.val < n}`, which in this case is all of `Fin m`.

- Claim: For any `a b : Fin n` and `h : n ≤ m`, the image `(Icc a b).map (VTask.castLEEmb h)` equals `Icc (castLE h a) (castLE h b)` in `Finset (Fin m)`.

## Boundaries

- **`n = 0`**: There are no elements in `Fin 0`, so the embedding is vacuously defined; its domain is empty and its range is empty.
- **`n = m`**: The proof `h : n ≤ m` degenerates to `n = m`, and the embedding acts as an order-isomorphism (in fact a bijection) from `Fin n` to `Fin m`.
- **`n = 1`**: The domain has exactly one element, `⟨0, _⟩`; the embedding sends it to `⟨0, _⟩ : Fin m`.
- The underlying natural number value is always preserved: for any `i : Fin n`, `(VTask.castLEEmb h i).val = i.val`.
- The embedding is order-preserving: `i ≤ j` in `Fin n` implies `castLEEmb h i ≤ castLEEmb h j` in `Fin m`.

## Not to be confused with

- **`Fin.castIso` / `Fin.castOrderIso`**: These require `n = m` (not merely `n ≤ m`) and produce an equivalence or order-isomorphism, not just an embedding.
- **`Fin.castAdd`**: Embeds `Fin n` into `Fin (n + m)` by the identity on values, but the target size is restricted to the specific form `n + m`.
- **`Fin.natAdd`**: Also embeds into a larger `Fin` type, but shifts values by adding `m`, rather than keeping them the same.
