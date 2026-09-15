## Object

A `VTask.DMatrix m n α` is the type of *dependently typed matrices*: a collection of entries indexed by a row index `i : m` and a column index `j : n`, where the type of each entry `(i, j)` is allowed to depend on both `i` and `j` via the family `α`. Concretely, an element of this type is a function that, given any row index and any column index, produces a value of the appropriate type for that cell. When `α` is a constant family — i.e., `α i j = β` for some fixed type `β` — this specialises to an ordinary matrix over `β` with rows indexed by `m` and columns indexed by `n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.DMatrix : (m : Type u) -> (n : Type u') -> (α : m → n → Type v) -> Type (max u u' v)
<!-- PINNED-SIGNATURE:END -->


VTask.DMatrix : (m : Type u) -> (n : Type u') -> (α : m → n → Type v) -> Type (max u u' v)

The first argument `m` is the type used to index rows. The second argument `n` is the type used to index columns. The third argument `α` is the *entry-type family*: a function assigning to each pair `(i, j)` the type that the `(i, j)`-entry of any such matrix must inhabit. The resulting type is the universe `Type (max u u' v)` combining the universe levels of all three ingredients.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total type former with no partial cases or distinguished degenerate inputs that require a special-case convention.

## Worked examples

- Claim: The constant-family case recovers plain matrices: any `f : VTask.DMatrix Bool Bool (fun _ _ => ℕ)` is simply a function `Bool → Bool → ℕ`, so `(fun _ _ => 0) : VTask.DMatrix Bool Bool (fun _ _ => ℕ)` is the all-zeros 2×2 matrix of natural numbers.

- Claim: Two elements of `VTask.DMatrix Bool Bool (fun _ _ => ℕ)` that agree on every entry are equal, illustrating function extensionality for these matrices: if `M N : VTask.DMatrix Bool Bool (fun _ _ => ℕ)` satisfy `∀ i j, M i j = N i j`, then `M = N`.

- Claim: A `VTask.DMatrix` can have genuinely heterogeneous entry types. With `m = n = Bool` and `α i _ = if i then ℕ else Bool`, the matrix whose first row (index `true`) contains natural numbers and whose second row (index `false`) contains booleans is a valid element of `VTask.DMatrix Bool Bool (fun i _ => if i then ℕ else Bool)`. For example, `(fun i j => if h : i then (0 : ℕ) else (false : Bool)) : VTask.DMatrix Bool Bool (fun i _ => if i then ℕ else Bool)` is such a matrix (modulo the dependent typing).

## Boundaries

- **Empty index types.** When `m` or `n` is an empty type (e.g., `Empty` or `Fin 0`), `VTask.DMatrix m n α` is still a perfectly well-formed type; it is inhabited by exactly one element — the vacuous function — since there is no valid index at which to produce a value.
- **Unit index types.** When both `m` and `n` are `Unit`, `VTask.DMatrix Unit Unit α` is equivalent to the single-entry type `α () ()`.
- **Constant family.** When `α i j = β` for all `i, j`, `VTask.DMatrix m n (fun _ _ => β)` is definitionally equal to `m → n → β`, the type of ordinary matrices (functions) with entries in `β`.

## Not to be confused with

- **`Matrix m n α`** (non-dependent matrices): the special case where the entry type `α` is constant across all positions; `VTask.DMatrix` strictly generalises this.
- **`∀ i : m, n → α i`** (partially dependent functions): similar in spirit but only allows the entry type to depend on the row index, not also on the column index.
- **`Σ i j, α i j`** (dependent pairs / sigma types): a sigma type bundles a *single* index pair with *one* value, whereas `VTask.DMatrix m n α` packages a value for *every* index pair simultaneously.