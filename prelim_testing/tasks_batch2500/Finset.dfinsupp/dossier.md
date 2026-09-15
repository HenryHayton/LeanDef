## Object

`VTask.dfinsupp s t` is the finite set of all finitely-supported functions (dependent finitely-supported functions, i.e. elements of `Π₀ i, α i`) whose support is contained in `s` and whose value at each index `i ∈ s` lies in the finite set `t i`. Concretely, it is the collection of all `Dfinsupp` maps `f` such that `f i = 0` for every `i ∉ s` and `f i ∈ t i` for every `i ∈ s`. In other words, it enumerates exactly those finitely-supported tuples whose non-zero entries are drawn from the prescribed finite menus `t i` at each allowed index `i ∈ s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dfinsupp : {ι : Type u_1} -> {α : ι → Type u_2} -> [DecidableEq ι] -> [(i : ι) → Zero (α i)] -> (s : Finset ι) -> (t : (i : ι) → Finset (α i)) -> Finset (Π₀ (i : ι), α i)
<!-- PINNED-SIGNATURE:END -->


`{ι : Type u_1} -> {α : ι → Type u_2} -> [DecidableEq ι] -> [(i : ι) → Zero (α i)] -> (s : Finset ι) -> (t : (i : ι) → Finset (α i)) -> Finset (Π₀ (i : ι), α i)`

The implicit type `ι` is the index type. The type family `α` assigns a coefficient type to each index. The `DecidableEq ι` instance is needed to work with finite supports. The family of `Zero` instances marks the distinguished zero element in each `α i`. The argument `s` is the finite set of indices that are allowed to be non-zero (the candidate support). The argument `t` is a family of finite sets, one per index `i ∈ ι`, specifying which values from `α i` are permitted at index `i`.

## Conventions

For any index `i` that lies outside `s`, the resulting finitely-supported functions are forced to take the value `0` at `i`, regardless of whether `0 ∈ t i`; the sets `t i` for `i ∉ s` are not consulted.

## Worked examples

- Claim: When `s = ∅` and `t` is any family of finsets, `VTask.dfinsupp ∅ t` is a singleton containing only the zero function.

- Claim: When `s = {i₀}` (a singleton) and `t i₀ = {a, b}` (a two-element finset), `VTask.dfinsupp {i₀} t` has exactly 2 elements, one sending `i₀` to `a` (zero elsewhere) and one sending `i₀` to `b` (zero elsewhere).

- Claim: The cardinality of `VTask.dfinsupp s t` equals the product over `i ∈ s` of `(t i).card`, mirroring the cardinality of the Cartesian product `s.pi t`.

- Claim: A `DFinsupp` element `f` belongs to `VTask.dfinsupp s t` if and only if for all `i ∈ s`, `f i ∈ t i`, and for all `i ∉ s`, `f i = 0`.

## Boundaries

- When `s = ∅`, the only finitely-supported function with empty support is the zero function, so the result is `{0}` regardless of `t`.
- When some `t i` is empty for `i ∈ s`, there is no valid assignment for index `i`, so the whole finset is empty.
- Values of `t i` for indices `i` outside `s` are completely ignored; even if `t i = ∅` for `i ∉ s`, it has no effect on the result.
- The zero element of each `α i` does not need to belong to `t i` for `i ∈ s`; the finset is determined purely by membership in `t`.

## Not to be confused with

- `Finset.pi s t`: the Cartesian product finset of non-dependent or dependent functions on `s`; `VTask.dfinsupp` wraps this into the `DFinsupp` world by forcing values to be zero outside `s`.
- `Finsupp.finset` (or analogous constructions for `Finsupp`): the non-dependent analogue that builds finsets of functions `ι →₀ α` rather than dependently-typed `Π₀ i, α i`.
- `DFinsupp.support`: the support of a single `DFinsupp` element; distinct from the index set `s` used to construct the whole finset `VTask.dfinsupp s t`.