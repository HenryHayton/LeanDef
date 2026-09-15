## 1. Object

`VTask.Lex r s x y` is the **lexicographic comparison** of two finitely-supported dependent functions `x` and `y` (elements of `Π₀ i, α i`). It holds precisely when there exists some index `i` such that `x` and `y` agree on every index that `r`-precedes `i`, but at `i` itself the values satisfy `s i (x i) (y i)`. In other words, `x` is strictly less than `y` in the lexicographic order: find the first (with respect to `r`) position where they differ, and there `x` must be smaller (with respect to `s`).

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Lex : {ι : Type u_1} -> {α : ι → Type u_2} -> [(i : ι) → Zero (α i)] -> (r : ι → ι → Prop) -> (s : (i : ι) → α i → α i → Prop) -> (x y : Π₀ (i : ι), α i) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Lex : {ι : Type u_1} -> {α : ι → Type u_2} -> [(i : ι) → Zero (α i)] -> (r : ι → ι → Prop) -> (s : (i : ι) → α i → α i → Prop) -> (x y : Π₀ (i : ι), α i) -> Prop`

The index type `ι` is implicit and ranges over all possible index sets. The family `α` is an implicit dependent type assigning a type to each index. A `Zero` instance for each fiber is required (so that the finitely-supported condition is meaningful — all but finitely many values equal zero). The argument `r` is the ordering relation on the index type `ι`; it determines which index is "earlier" in the lexicographic comparison. The argument `s` is a family of ordering relations, one per index `i`, used to compare fiber values at that index. The arguments `x` and `y` are the two finitely-supported functions being compared.

## 3. Conventions

There are no declared junk-value or edge conventions: the relation is a pure proposition and is defined for all valid inputs without any special treatment of boundary or default values beyond what the mathematical definition dictates.

## 4. Worked examples

- Claim: For finitely-supported functions on `Fin 2` with the natural order on `ℕ`, `VTask.Lex (· < ·) (fun _ => (· < ·)) x y` holds when `x 0 < y 0` and both agree at all smaller indices (vacuously, since `0` is the least).

- Claim: If `x = y` everywhere (i.e., `x = y`), then `VTask.Lex r s x y` is false for any irreflexive `s`, because there is no index `i` at which `s i (x i) (y i)` can hold.

- Claim: When `ι` is a singleton (unique index), `VTask.Lex r (fun _ => (· < ·)) x y` is equivalent to `x default < y default`, as there is only one index to compare and no earlier indices.

- Claim: The standard lexicographic order on `Lex (Π₀ i, α i)` (the type synonym equipped with `<`) is governed by `VTask.Lex (· < ·) (· < ·)`, meaning `a < b` iff there exists `i` with `a j = b j` for all `j < i` and `a i < b i`.

## 5. Boundaries

- **Zero function**: `VTask.Lex r s 0 0` is always false for any irreflexive `s`, since `0 i = 0 i` everywhere, so no witnessing index can exist. More generally, `VTask.Lex r s 0 y` fails whenever `s` does not relate `0` to itself at any index `i` where the two functions first differ — and for well-founded orders where `s i a 0` never holds, the zero function is a `Lex`-minimum.
- **Finite support**: The definition makes sense even though `α i` may be infinite-dimensional; the finitely-supported condition only affects how the functions are stored, not the logical content of the relation.
- **Non-total `r`**: If `r` is not a total or well-founded order on `ι`, the lexicographic comparison may behave in unexpected ways (e.g., not be a strict total order), but the definition is still well-formed.
- **Colex variant**: Using `r = (· > ·)` (the reverse order) with `s = (· < ·)` gives the colexicographic order, in which later indices dominate.

## 6. Not to be confused with

- **`Finsupp.Lex r s`**: The analogous lexicographic relation for finitely-supported functions with a *fixed* codomain type (not dependent), rather than a dependent family; it coincides with `VTask.Lex` via the canonical embedding of `Finsupp` into `DFinsupp`.
- **`Pi.Lex r s x y`**: The lexicographic relation on the full (not finitely-supported) dependent function type `Π i, α i`; `VTask.Lex` is exactly this relation restricted to finitely-supported functions, using their coercion to `Π i, α i`.
- **`Lex (Π₀ i, α i)`**: A *type synonym* wrapping `Π₀ i, α i` and equipping it with an order instance derived from `VTask.Lex (· < ·) (· < ·)`; not the relation itself, but the ordered type it induces.
