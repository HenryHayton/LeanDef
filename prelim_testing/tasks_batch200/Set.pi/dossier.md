## Object

`VTask.pi s t` is the *dependent-function pi set* (or simply the *pi set*) determined by an index set `s` and a family of sets `t`. It consists of all dependent functions `f : ∀ i, α i` such that, for every index `i` that belongs to `s`, the value `f i` lies in `t i`. Indices outside `s` are unconstrained: the function may send them anywhere.

In other words, if one thinks of `t i` as specifying the allowed values at coordinate `i`, then `VTask.pi s t` is the "box" of dependent functions that respect those constraints — but only at coordinates in `s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {ι : Type u_1} -> {α : ι → Type u_2} -> (s : Set ι) -> (t : (i : ι) → Set (α i)) -> Set ((i : ι) → α i)
<!-- PINNED-SIGNATURE:END -->


`VTask.pi : {ι : Type u_1} -> {α : ι → Type u_2} -> (s : Set ι) -> (t : (i : ι) → Set (α i)) -> Set ((i : ι) → α i)`

The implicit argument `ι` is the index type that parameterises the product. The implicit argument `α` is a family of types indexed by `ι`, so `α i` is the type living over the index `i`. The explicit argument `s` is the *active index set*: membership in the pi set is only enforced at indices belonging to `s`. The explicit argument `t` is the family of *slice sets*: `t i` is the permitted subset of `α i` at coordinate `i`.

## Conventions

When `s = Set.univ` (the full index set), every coordinate is constrained and `VTask.pi s t` becomes the standard product of the family `t`. When `s = ∅`, no coordinate is constrained and `VTask.pi s t` is the entire function space `Set.univ` regardless of `t`.

## Worked examples

- Claim: A constant function `fun _ => 3` belongs to `VTask.pi Set.univ (fun _ : Fin 2 => {3})` because it sends every index to 3.

- Claim: The function `fun i : Fin 2 => i.val + 1` belongs to `VTask.pi {0} (fun i => if i = 0 then {1} else Set.univ)` because at the only constrained index 0 the value is 1.

- Claim: `VTask.pi (∅ : Set ℕ) (fun i => (∅ : Set ℕ))` equals `Set.univ`, since no constraint is imposed on any coordinate when the active index set is empty.

- Claim: For any family `t`, the pi set `VTask.pi Set.univ t` is a subset of `VTask.pi s t` whenever `s ⊆ Set.univ`, illustrating monotonicity: fewer active indices means fewer constraints.

## Boundaries

- **Empty active set (`s = ∅`):** Every dependent function satisfies the membership condition vacuously, so `VTask.pi ∅ t = Set.univ` for any `t`.
- **Full active set (`s = Set.univ`):** All coordinates are constrained, giving the classical dependent-function product `∏ i, t i`.
- **Empty slice (`t i = ∅` for some `i ∈ s`):** No function can satisfy `f i ∈ ∅`, so `VTask.pi s t = ∅` as soon as any active index has an empty slice.
- **Universal slices (`t i = Set.univ` for all `i`):** The pi set is again `Set.univ` no matter what `s` is.
- **The index type `ι` is a subsingleton or `Fin 0`:** The function space is a singleton and the pi set is either that singleton or empty depending on whether the unique function (if any) meets the constraints.

## Not to be confused with

- `Set.univ.pi t` — this is `VTask.pi` applied with the full index set; it is the most common special case but does not capture the flexibility of a restricted active set `s`.
- `Set.prod s t` — the binary Cartesian product of two plain sets; `VTask.pi` generalises this to arbitrary (dependent) index families.
- `Set.tprod l t` — the heterogeneous list-indexed product, which uses a `List ι` rather than a `Set ι` to specify active indices.
