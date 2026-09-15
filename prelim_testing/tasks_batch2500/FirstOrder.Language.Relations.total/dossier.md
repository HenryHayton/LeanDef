## VTask.total

### Object

Given a binary relation symbol `r` in a first-order language `L`, `VTask.total r` is the first-order sentence asserting that `r` is **total** (also called a **linear** or **connex** relation): for every pair of elements `x` and `y`, either `r(x, y)` holds or `r(y, x)` holds (or both). In symbols, the sentence is `∀x ∀y (r(x,y) ∨ r(y,x))`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.total : {L : FirstOrder.Language} -> (r : L.Relations 2) -> L.Sentence
<!-- PINNED-SIGNATURE:END -->


The implicit argument `L` is the ambient first-order language. The explicit argument `r` is a binary relation symbol of `L` — concretely, a term of type `L.Relations 2` — whose totality is being expressed. The result is a closed sentence (no free variables) belonging to `L`.

### Conventions

No special junk-value or edge conventions have been declared for this definition: it is a total function on its inputs, always producing a well-formed sentence, and there are no degenerate boundary cases requiring special treatment.

### Worked examples

- Claim: For any language `L` and binary relation symbol `r : L.Relations 2`, `VTask.total r` is a sentence (has no free variables), i.e., it is an element of `L.Sentence`.

- Claim: In a language `L` with a single binary relation symbol `r`, `VTask.total r` encodes the statement `∀x ∀y (r(x,y) ∨ r(y,x))`, which is satisfied exactly in structures where `r` is a total (connex) relation.

- Claim: If `M` is an `L`-structure and `M ⊨ VTask.total r`, then for every `a b : M`, either `r` holds of `(a, b)` or `r` holds of `(b, a)` in `M`.

### Boundaries

- The definition applies to any binary relation symbol in any first-order language, including the trivial language with no other symbols.
- The sentence produced uses universal quantification over all pairs of elements; in a one-element structure, totality is trivially satisfied because `r(a, a) ∨ r(a, a)` reduces to `r(a,a)`.
- Totality does **not** imply antisymmetry or irreflexivity; the sentence is consistent with `r(x, y)` and `r(y, x)` both holding simultaneously for the same `x` and `y`.
- The definition makes sense and is well-formed even when the underlying structure has an empty domain in the sense of the language, though semantics of empty-domain first-order structures may vary by convention.

### Not to be confused with

- **`FirstOrder.Language.Relations.irreflexive`** (or a similar sentence): that sentence asserts `∀x ¬r(x,x)`, a completely different property.
- **Totality of a function symbol**: `VTask.total` is specifically about *relation* symbols; a total function is a different concept (every input maps to some output).
- **`FirstOrder.Language.Relations.antisymm`**: the sentence `∀x ∀y (r(x,y) ∧ r(y,x) → x = y)`, which together with totality is part of the definition of a linear order but is not the same as totality alone.