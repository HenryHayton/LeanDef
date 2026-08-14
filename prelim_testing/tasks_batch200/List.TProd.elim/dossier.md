## Object

`VTask.elim` is the projection function for a typed heterogeneous product indexed by a list. Given a list `l` of indices, a value of type `List.TProd α l` (an iterated product whose `i`-th factor is `α i`), and a proof that some index `i` belongs to `l`, it returns the component of the product at index `i`. When `i` appears more than once in `l`, the first occurrence is chosen.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.elim : {ι : Type u} -> {α : ι → Type v} -> [DecidableEq ι] -> {l : List ι} -> List.TProd α l → {i : ι} → i ∈ l → α i
<!-- PINNED-SIGNATURE:END -->


`VTask.elim : {ι : Type u} -> {α : ι → Type v} -> [DecidableEq ι] -> {l : List ι} -> List.TProd α l → {i : ι} → i ∈ l → α i`

The type `ι` is the index type; `α` is the family of types, one per index. The `DecidableEq ι` instance is needed to decide whether two indices are equal. The implicit argument `l` is the ordered list of indices forming the product. The first explicit argument is the element of the iterated product `List.TProd α l`. The implicit argument `i` is the index being projected. The final explicit argument is a membership proof witnessing that `i` lies in `l`.

## Conventions

When `i` appears more than once in the list `l`, `VTask.elim` returns the component corresponding to the **first** occurrence of `i` in `l`; later duplicates are ignored.

## Worked examples

- Claim: For `v : List.TProd α (i :: l)`, projecting at `i` via `VTask.elim v (List.mem_cons_self i l)` returns the first component `v.1`.

- Claim: For `v : List.TProd α (i :: l)` and a proof `hj : j ∈ l` with `j ≠ i`, projecting at `j` via `VTask.elim v (List.mem_cons_of_mem i hj)` equals projecting the tail `v.2` at `j`.

- Claim: If `f : ∀ i, α i` and `hi : i ∈ l`, then `VTask.elim (List.TProd.mk l f) hi = f i`; that is, projecting the canonical element built from `f` recovers `f` pointwise.

- Claim: If `l` has no duplicates and two elements `v w : List.TProd α l` agree on all projections, then `v = w`.

## Boundaries

- The membership proof argument is essential: there is no version that takes an index without evidence that it belongs to `l`. An index not in `l` simply cannot be supplied.
- When `l` is empty, the type `List.TProd α []` is `PUnit` and no membership proof `i ∈ []` exists, so `VTask.elim` is vacuously inapplicable on the empty list.
- Duplicate indices are handled by selecting the leftmost occurrence; the function is well-defined regardless of duplicates, but the `ext` (injectivity) theorem requires `l.Nodup` to ensure distinct projections determine the element uniquely.
- The function is total on its stated domain: any `i ∈ l` and any element of `List.TProd α l` are accepted.

## Not to be confused with

- `List.TProd.elim'`: a variant that projects using a proof that every index of type `ι` belongs to `l`, rather than a specific membership proof for a given `i`.
- `List.TProd.mk`: the constructor that builds a `List.TProd α l` from a dependent function `∀ i, α i`; this is the left inverse of `VTask.elim` (up to nodup conditions).
- `Fin.cons` / `Fin`-indexed products: a different family of heterogeneous products indexed by natural numbers rather than an arbitrary list of indices.