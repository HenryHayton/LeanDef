## 1. Object

`VTask.Lex r s x y` is the **lexicographic strict ordering** on the dependent product type `(i : ι) → β i`. It holds when there exists some index `i` such that:
- for every index `j` that precedes `i` in the ordering `r`, the two functions agree (`x j = y j`), and
- at the pivot index `i`, the fiber relation `s` holds between `x i` and `y i`.

Informally: `x` comes before `y` if there is a first (under `r`) position where they differ, and at that position `x` is smaller (under `s`).

## 2. Signature

```
VTask.Lex : {ι : Type u_1} -> {β : ι → Type u_2} -> (r : ι → ι → Prop) -> (s : {i : ι} → β i → β i → Prop) -> (x y : (i : ι) → β i) -> Prop
```

- `ι` — the implicit index type; it carries the "coordinate" ordering.
- `β` — the implicit family of fiber types, one per index.
- `r : ι → ι → Prop` — the strict ordering on the index type used to determine which coordinate is "earlier".
- `s : {i : ι} → β i → β i → Prop` — the strict ordering on each fiber, used to compare the values at the pivot coordinate.
- `x y : (i : ι) → β i` — the two dependent functions being compared.
- Returns a `Prop` that is true exactly when `x` lexicographically precedes `y`.

## 3. Conventions

There are no junk-value or out-of-domain conventions declared for this definition: it is a total predicate over all values of its inputs with no distinguished degenerate inputs requiring special conventions.

## 4. Worked Examples

- Claim: For functions on `Fin 2` with the natural ordering, if `x = ![0, 5]` and `y = ![1, 0]`, then `VTask.Lex (· < ·) (fun {_} => (· < ·)) x y` holds (pivot at index 0, where `0 < 1`).

- Claim: For functions on `Fin 2`, if `x = ![3, 2]` and `y = ![3, 4]`, then `VTask.Lex (· < ·) (fun {_} => (· < ·)) x y` holds (index 0 agrees since `3 = 3`, pivot at index 1 where `2 < 4`).

- Claim: For functions on `Fin 2`, `VTask.Lex (· < ·) (fun {_} => (· < ·)) x x` does not hold for any `x`, because the fiber relation `s` is strict (irreflexive) and thus `s (x i) (x i)` is never satisfied.

- Claim: When `ι` is a type with a well-founded strict total order and each fiber order is well-founded, `VTask.Lex r s` is itself well-founded.

## 5. Boundaries

- **Empty index type**: If `ι` is empty (`IsEmpty ι`), there is no index `i` at which the existential can be witnessed, so `VTask.Lex r s x y` is always false (vacuously, no pivot exists).
- **Singleton index type**: If `ι` has exactly one element (`Unique ι`) and `r` is irreflexive, `VTask.Lex r s x y` reduces to `s (x default) (y default)`; the only candidate pivot is `default`, and the prefix-agreement condition is vacuously satisfied.
- **Reflexivity**: `VTask.Lex r s x x` is always false when `s` is irreflexive, since at any pivot `i` one would need `s (x i) (x i)`.
- **Asymmetry with `r`**: The ordering `r` need not be well-founded or total for the definition to make sense; however, well-foundedness and totality of `r` (together with well-foundedness of each `s i`) are needed to obtain a well-founded `VTask.Lex`.
- **Choice of `r`**: Using `r = (· > ·)` (the reverse ordering) yields the co-lexicographic ordering, which is distinct from the standard lexicographic ordering obtained with `r = (· < ·)`.

## 6. Not to be confused with

- **`Finsupp.Lex r s`**: The lexicographic order on finitely-supported functions; coincides with `VTask.Lex r s` when applied to the coercion of a `Finsupp` to a `Pi` type, but lives on a different type.
- **`DFinsupp.Lex r s`**: The analogous lex order on dependent finitely-supported functions; again coincides with `VTask.Lex` on the underlying `Pi` type but is a separate definition.
- **`List.Lex`**: Lexicographic order on lists, which handles the length mismatch case and operates on a homogeneous sequential structure rather than a dependent product.
