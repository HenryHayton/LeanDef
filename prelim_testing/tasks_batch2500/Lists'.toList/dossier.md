## Object

`VTask.toList` converts a ZFA *prelist* (an element of `Lists' α b`, the auxiliary inductive type used to build ZFA set-like lists) into an ordinary Lean `List` whose elements are ZFA lists (`Lists α`). Concretely, an *atom* prelist and the *nil* prelist are both sent to the empty list `[]`; a *cons* prelist built from a head ZFA list `a` and a tail prelist `l` is sent to the ordinary list whose first element is `a` and whose remaining elements are the result of recursively converting `l`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toList : {α : Type u_1} -> {b : Bool} -> Lists' α b → List (Lists α)
<!-- PINNED-SIGNATURE:END -->


VTask.toList : {α : Type u_1} -> {b : Bool} -> Lists' α b → List (Lists α)

The implicit type argument `α` is the type of atoms underlying the ZFA lists. The implicit Boolean `b` is the *kind flag* of `Lists' α b`: when `b = false` the prelist is an atom; when `b = true` it is a list-shaped prelist (either `nil` or a `cons'`). The explicit argument is the prelist to be converted.

## Conventions

Atom prelists are not list-shaped and carry no elements, so they are sent to the empty list `[]` rather than raising an error or being undefined. The `nil` prelist is also sent to `[]`. There is no partial behaviour; the function is defined for every prelist regardless of kind.

## Worked examples

- Claim: `VTask.toList (Lists'.nil : Lists' Nat true) = []`

- Claim: For any atom value `a : Nat`, `VTask.toList (Lists'.atom a) = []`

- Claim: `VTask.toList (Lists'.cons' a Lists'.nil) = [⟨_, a⟩]` — a single-element prelist converts to a singleton ordinary list whose sole entry is the ZFA list wrapping `a`.

- Claim: The round-trip identity holds: for every `l : List (Lists α)`, converting `Lists'.ofList l` back with `VTask.toList` recovers `l` (i.e., `VTask.toList (Lists'.ofList l) = l`).

- Claim: The other direction of the round-trip: for every list-shaped prelist `l : Lists' α true`, `Lists'.ofList (VTask.toList l) = l`.

## Boundaries

- **Atoms (`b = false`):** The function always returns `[]`. An atom carries a single raw value of type `α` but is not a set-like collection, so there are no ZFA-list elements to extract.
- **`nil` (`b = true`, empty):** Returns `[]`, consistent with an empty set/list.
- **`cons'` nodes:** Each recursive step prepends exactly one ZFA list (the head), so the length of the returned ordinary list equals the number of `cons'` constructors in the prelist.
- **Membership characterisation:** An element `a` belongs to a prelist `l` in the ZFA sense if and only if some element of `VTask.toList l` is ZFA-equivalent to `a`.

## Not to be confused with

- `Lists'.ofList` — the inverse operation, converting an ordinary `List (Lists α)` *into* a prelist; `VTask.toList` and `ofList` are mutual inverses on list-shaped prelists.
- `Lists α` — the ZFA list type itself (not a prelist); `VTask.toList` takes a *prelist* `Lists' α b` and produces a `List (Lists α)`, so the source and target types are distinct.
- `List.toList` / coercion lemmas on ordinary lists — unrelated Lean standard-library coercions having nothing to do with ZFA prelists.