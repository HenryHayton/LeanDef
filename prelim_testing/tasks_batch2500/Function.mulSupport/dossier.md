## Object

`VTask.mulSupport f` is the *multiplicative support* of a function `f : ι → M`. It is the set of all indices `x : ι` for which `f x` is not the identity element `1` of `M`. In other words, it is the set of points at which `f` is "non-trivial" in the multiplicative sense.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mulSupport : {ι : Type u_1} -> {M : Type u_3} -> [One M] -> (f : ι → M) -> Set ι
<!-- PINNED-SIGNATURE:END -->


`VTask.mulSupport : {ι : Type u_1} -> {M : Type u_3} -> [One M] -> (f : ι → M) -> Set ι`

The implicit type argument `ι` is the index type — the domain of the function. The implicit type argument `M` is the codomain, which must carry a distinguished element `1` (supplied by the `[One M]` instance). The explicit argument `f` is the function whose multiplicative support is being computed. The result is a subset of `ι`.

## Conventions

There are no junk-value or boundary conventions specific to this definition: it is a total function and its defining predicate `f x ≠ 1` is well-formed for every element of `ι`, so no special-case junk values arise.

## Worked examples

- Claim: For the constant function `fun _ : Fin 5 => (1 : ℕ)`, every element is excluded from `VTask.mulSupport`, so the support is empty.

- Claim: For `f : Fin 3 → ℤ` defined by `f 0 = 0, f 1 = 1, f 2 = 2`, the element `1` (whose value is the integer `1`) does **not** belong to `VTask.mulSupport f`, but `0` and `2` do.

- Claim: For `f : ℕ → ℕ` defined by `f n = n + 1`, the multiplicative support is all of `ℕ`, since `n + 1 ≠ 1` for all but `n = 0`; specifically `0 ∉ VTask.mulSupport f` because `f 0 = 1`.

- Claim: If `g : ι → M` satisfies `g x = 1` for every `x`, then `VTask.mulSupport g = ∅`.

## Boundaries

- If `f` is the constant function returning `1`, its multiplicative support is the empty set `∅`.
- If `f` never returns `1`, its multiplicative support is all of `ι` (the universal set).
- For a type `M` where `1` is the only element (e.g. `Unit` or a trivial monoid), every function has empty multiplicative support.
- The definition makes sense for any type `M` equipped with `One M`; no further algebraic structure (e.g. multiplication) is required.
- The index type `ι` is unrestricted — it may be finite, infinite, or even empty; in the empty case the support is trivially `∅`.

## Not to be confused with

- **`Function.support`** (additive support): the analogous set `{x | f x ≠ 0}` using the zero element rather than `1`; used for additive structures.
- **`Finsupp.support`**: the *finite* support of a finitely-supported function `ι →₀ M`, which is a `Finset ι` rather than a `Set ι` and carries the additional guarantee of finiteness.
- **`Set.indicator`**: a function constructed from a set that returns `0` outside the set; related in spirit but is a function, not the support set itself.