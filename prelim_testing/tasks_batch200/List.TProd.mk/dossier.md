## Object

`VTask.mk l f` constructs an element of the iterated (heterogeneous) product type `List.TProd α l` from a dependent function `f` that, for each index `i : ι`, produces a value of type `α i`. Concretely, `List.TProd α l` is the nested binary product type whose factors are `α i` for each `i` appearing (in order) in the list `l`. The constructor packs together all the values `f i` for `i ∈ l`, respecting the order of `l`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk : {ι : Type u} -> {α : ι → Type v} -> (l : List ι) -> (_f : (i : ι) → α i) -> List.TProd α l
<!-- PINNED-SIGNATURE:END -->


The first implicit argument `ι` is the index type whose elements name the factors of the product. The second implicit argument `α` is a type family assigning to each index `i : ι` the type of the corresponding factor. The explicit argument `l` is the list of indices that determines which factors appear (and in what order) in the iterated product. The argument `_f` is the dependent function that supplies a value of type `α i` for every index `i : ι`; it is evaluated at each element of `l` to fill the corresponding factor.

## Conventions

When `l` is the empty list, the resulting `TProd α []` is the unit type `PUnit`, and `VTask.mk [] f` is the unique element `PUnit.unit` regardless of `f`. When `l` is a non-empty list `i :: is`, `VTask.mk (i :: is) f` is the pair whose first component is `f i` and whose second component is `VTask.mk is f`; thus the overall structure is a right-nested tuple.

## Worked Examples

- Claim: For `l = []` and any `f`, `VTask.mk [] f` equals `PUnit.unit`.
  ```lean
  example (f : (i : Fin 3) → Fin i.val.succ) : VTask.mk ([] : List (Fin 3)) f = PUnit.unit := rfl
  ```

- Claim: For `l = [0, 1]` with `α i = Nat` and `f i = i`, `VTask.mk [0, 1] f` has first component `0` and second component a pair with first component `1`.
  ```lean
  example : (VTask.mk [0, 1] (fun i => i) : List.TProd (fun _ => Nat) [0, 1]).1 = 0 := rfl
  ```

- Claim: `(VTask.mk (i :: is) f).1 = f i` (the `fst_mk` theorem).

- Claim: `(VTask.mk (i :: is) f).2 = VTask.mk is f` (the `snd_mk` theorem).

- Claim: If `l` has no duplicates and every `i : ι` belongs to `l`, then `VTask.mk l (v.elim' h) = v` for any element `v : List.TProd α l` (the `mk_elim` round-trip theorem).

## Boundaries

- Empty list: `VTask.mk [] f = PUnit.unit` for every `f`; the function argument has no observable effect.
- Duplicate indices: If `l` contains an index `i` more than once, `VTask.mk l f` will include `f i` in multiple positions (corresponding to each occurrence), because the construction is purely list-driven and does not deduplicate.
- The function `f` is evaluated at every element of `l` in order; if `l` is very long, `f` is queried repeatedly (including repeated queries if indices repeat).
- The `VTask.mk` construction is always total: it is defined for every list and every dependent function with no side conditions.

## Not to be confused with

- `List.TProd.elim`: Extracts the component at a particular membership proof from a `TProd` value; it is the inverse direction to `VTask.mk`.
- `List.TProd.elim'`: Similar to `elim` but requires a proof that the index belongs to the list and that the list has no duplicates; together with `VTask.mk` it forms a round-trip pair.
- `Finset.prod` / `Finset.pi`: Products or pi-types indexed by a `Finset` rather than a `List`, with different universe and definitional behaviour.