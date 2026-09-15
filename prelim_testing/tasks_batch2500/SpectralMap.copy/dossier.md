## Object

`VTask.copy` produces a `SpectralMap` from `α` to `β` that is mathematically identical to a given spectral map `f`, but whose underlying function is replaced by a (definitionally or propositionally) equal function `f'`. Its purpose is purely bookkeeping: when Lean's definitional equality checker needs the underlying function to be syntactically a particular term, this constructor lets you swap in that term while preserving all the spectral-map structure.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [TopologicalSpace α] -> [TopologicalSpace β] -> (f : SpectralMap α β) -> (f' : α → β) -> (h : f' = ⇑f) -> SpectralMap α β
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [TopologicalSpace α] -> [TopologicalSpace β] -> (f : SpectralMap α β) -> (f' : α → β) -> (h : f' = ⇑f) -> SpectralMap α β`

The implicit type arguments `α` and `β` are the source and target topological spaces; their `TopologicalSpace` instances are inferred automatically. The argument `f` is the original spectral map being copied. The argument `f'` is the new underlying bare function that will be carried by the resulting spectral map. The argument `h` is a proof that `f'` equals the coercion of `f` to a bare function, witnessing that the substitution is legitimate.

## Conventions

There are no junk-value or degenerate-input conventions for this definition: every well-typed input yields a valid `SpectralMap`, and the construction is total over all such inputs.

## Worked examples

- Claim: For any spectral map `f : SpectralMap α β`, calling `VTask.copy f ⇑f rfl` produces a spectral map whose coercion to a bare function is exactly `⇑f`.

- Claim: For any spectral map `f : SpectralMap α β` and any proof `h : f' = ⇑f`, the result `VTask.copy f f' h` is equal (as a `SpectralMap`) to `f` itself — that is, `VTask.copy f f' h = f`.

- Claim: For any spectral map `f : SpectralMap α β` and proof `h : f' = ⇑f`, the coercion of `VTask.copy f f' h` to a bare function is `f'`, not the original coercion of `f`.

## Boundaries

- When `f' = ⇑f` holds by `rfl` (i.e., `f'` is definitionally the coercion of `f`), the copy is indistinguishable from `f` in every respect.
- When `f'` and `⇑f` are propositionally but not definitionally equal, the copy provides a version of `f` whose underlying function is syntactically `f'`, which can resolve unification failures in tactics.
- The resulting spectral map is provably equal to `f` as a `SpectralMap`, regardless of which `h` is supplied (since all proofs of `f' = ⇑f` are interchangeable by proof irrelevance).
- The construction does not create a new mathematical object; it only changes the syntactic presentation of the underlying function.

## Not to be confused with

- `SpectralMap.mk`: the general constructor for spectral maps, which requires the user to supply the continuity and spectral-map properties manually, rather than inheriting them from an existing map.
- Function composition or restriction of a spectral map: those genuinely change the underlying function, whereas `VTask.copy` only renames it to a propositionally equal one.
- The identity spectral map: that is a specific mathematical object, whereas `VTask.copy` is a meta-level tool for fixing definitional equality issues with any spectral map.