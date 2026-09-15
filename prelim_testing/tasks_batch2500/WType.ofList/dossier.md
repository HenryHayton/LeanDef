## VTask.ofList

### Object

`VTask.ofList` is one half of a canonical isomorphism between ordinary Lean lists and the W-type encoding of the list data type. It converts any `List γ` into the corresponding element of `WType (WType.Listβ γ)`, the W-type whose shape functor encodes the list signature (a nullary constructor for `nil` and a unary constructor parametrised by the head element for `cons`). The result faithfully encodes the list's structure: an empty list becomes the W-type node labelled `nil` with no children, and a non-empty list becomes the W-type node labelled `cons hd` with a single child subtree obtained by recursively encoding the tail.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofList : (γ : Type u) -> List γ → WType (WType.Listβ γ)
<!-- PINNED-SIGNATURE:END -->


`VTask.ofList : (γ : Type u) -> List γ → WType (WType.Listβ γ)`

The first argument `γ` is the element type — the type of values stored in the list. The second argument is the concrete list to be converted.

### Conventions

There are no special junk-value or out-of-domain conventions for this function: it is a total function defined on all lists of any type, and the mapping is uniquely determined by the recursive structure of the list.

### Worked examples

- Claim: `VTask.ofList Bool []` produces the W-type node corresponding to `Listα.nil` with the empty child function.

- Claim: `VTask.ofList Nat [1, 2, 3]` produces a W-type node labelled `Listα.cons 1` whose single child is the encoding of `[2, 3]`.

- Claim: `VTask.ofList` composed with the inverse `toList` function is the identity on `List γ` (i.e., it is part of a bijection).

- Claim: The image of `VTask.ofList γ []` has constructor label `Listα.nil`.

### Boundaries

- The empty list `[]` maps to the unique W-type leaf node labelled `Listα.nil` — there are no children (the child function is defined on `PEmpty`, hence vacuously).
- A singleton list `[x]` maps to a node labelled `Listα.cons x` with a single child that is the encoding of `[]`.
- The function is defined for all element types `γ`, including `Empty` or `PEmpty`; in those cases only the empty list is constructible, so the only reachable input is `[]`.
- There is no partiality or failure: every finite list of any length is handled.

### Not to be confused with

- `WType.Listβ` itself — that is the *shape functor* (the `β` component of the polynomial functor), not the conversion function.
- The inverse direction `toList : WType (WType.Listβ γ) → List γ` — that goes from W-types back to lists, the opposite of `VTask.ofList`.
- `List.toWType` or similar names that might appear in other formalisations — `VTask.ofList` is the specific Mathlib construction tied to `WType.Listβ`.