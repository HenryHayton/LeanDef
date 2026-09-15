## Object

`VTask.symmetric r` is the first-order sentence (in the language `L`) that expresses the symmetry of the binary relation symbol `r`. Concretely, it is the universal statement: *for all x and y, if r(x, y) holds then r(y, x) holds*. Any `L`-structure satisfies this sentence precisely when the interpretation of `r` is a symmetric relation.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.symmetric : {L : FirstOrder.Language} -> (r : L.Relations 2) -> L.Sentence
<!-- PINNED-SIGNATURE:END -->


The implicit argument `L` is a first-order language (a `FirstOrder.Language`). The explicit argument `r` is a binary relation symbol of that language — that is, an element of `L.Relations 2`, representing one of the basic 2-ary predicates available in `L`.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total function producing a well-formed sentence for every valid choice of language `L` and binary relation symbol `r`, with no degenerate inputs.

## Worked examples

- Claim: For any language `L` and binary relation `r : L.Relations 2`, `VTask.symmetric r` is a sentence (an element of `L.Sentence`, i.e., a closed formula with no free variables).

- Claim: An `L`-structure `M` is a model of `VTask.symmetric r` if and only if the interpretation of `r` in `M` is a symmetric binary relation on the underlying set of `M`.

- Claim: `VTask.symmetric r` is logically distinct from the reflexivity or transitivity sentences for `r`; in particular, a structure can satisfy symmetry without satisfying either of those properties.

## Boundaries

- The definition is total: it is defined for every language `L` and every `r : L.Relations 2`. There are no inputs that cause undefined or degenerate behaviour.
- If `L` has only one binary relation symbol, `VTask.symmetric r` is the unique symmetry sentence for that language.
- The sentence makes no assumption about any other relation symbols in `L`; it refers only to `r`.
- Because the sentence uses universal quantifiers ranging over all elements of the structure, in an empty structure (if one is permitted by the semantics) the sentence holds vacuously.

## Not to be confused with

- The *reflexivity* sentence for `r`: that sentence asserts `∀ x, r(x, x)`, which is a different property and is not implied by symmetry alone.
- The *transitivity* sentence for `r`: that sentence asserts `∀ x y z, r(x,y) ∧ r(y,z) → r(x,z)`, again independent of symmetry.
- `L.Relations 2` itself: this is the *type* of binary relation symbols in `L`, not a sentence; `VTask.symmetric` maps an element of this type to a sentence.