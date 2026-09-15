## Object

`VTask.copy` produces a new continuous map from `X` to `Y` whose underlying function is definitionally equal to a given bare function `f'`, while the continuity certificate is transferred from an existing continuous map `f`. It is purely a bookkeeping device: the resulting continuous map is propositionally (and in fact definitionally) equal to `f`, but its `toFun` field is the explicitly supplied `f'` rather than `⇑f`. This is useful when Lean's definitional equality checker needs the underlying function to be syntactically a particular term.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : C(X, Y)) -> (f' : X → Y) -> (h : f' = ⇑f) -> C(X, Y)
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : C(X, Y)) -> (f' : X → Y) -> (h : f' = ⇑f) -> C(X, Y)`

The first two implicit arguments are the domain and codomain types. The two instance arguments supply the topological structure on each. The argument `f` is the existing continuous map from which continuity is borrowed. The argument `f'` is the bare function that will serve as the `toFun` field of the result. The proof `h` witnesses that `f'` is equal to the coercion of `f`, justifying the transfer of the continuity certificate.

## Conventions

There are no junk-value or out-of-domain conventions for this definition: it is total and the hypothesis `h` fully determines the relationship between `f` and `f'`.

## Worked examples

- Claim: For any continuous map `f : C(X, Y)`, the coercion of `f.copy f' h` as a function equals `f'`.
  (By `VTask.coe_copy`, `⇑(f.copy f' h) = f'`.)

- Claim: For any continuous map `f : C(X, Y)`, `f.copy (⇑f) rfl` equals `f` as a continuous map.
  (By `VTask.copy_eq`, the copied map is propositionally equal to the original.)

- Claim: Given `f : C(ℝ, ℝ)` and `f' := fun x => f x` with proof `h : f' = ⇑f`, the result `f.copy f' h` is continuous from `ℝ` to `ℝ`.

## Boundaries

- The proof `h` must go in the direction `f' = ⇑f`; if one has `⇑f = f'` instead, one must supply `h.symm`.
- When `f'` is definitionally equal to `⇑f` but not syntactically so, `h` may still be supplied as `rfl` if Lean can close the goal by reduction; otherwise an explicit proof is required.
- The resulting continuous map is always propositionally equal to `f` (by `copy_eq`), so `copy` never changes the mathematical content, only the syntactic presentation of `toFun`.
- There is no restriction on the topological spaces `X` and `Y`; the construction works for any topological spaces.

## Not to be confused with

- `ContinuousMap.mk`: the raw constructor for a continuous map, which requires the user to supply a continuity proof directly rather than inheriting it from an existing continuous map.
- Function composition or restriction: `copy` does not alter the values of the map, whereas composition or restriction can change which function is computed.
- `Set.codRestrict` / `ContinuousMap.restrict`: these change the codomain or domain of a map; `copy` leaves both unchanged and only renames the underlying function term.