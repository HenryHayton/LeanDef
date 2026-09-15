## Object

The *densely ordered sentence* for a first-order ordered language `L` is the closed first-order sentence (i.e., a sentence with no free variables) that expresses density of a strict linear order: for every two elements `x` and `y`, if `x < y` then there exists an element `z` strictly between them, i.e., `x < z` and `z < y`. Formally, this is the universal–existential sentence `∀x, ∀y, x < y → ∃z, x < z ∧ z < y`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.denselyOrderedSentence : (L : FirstOrder.Language) -> [L.IsOrdered] -> L.Sentence
<!-- PINNED-SIGNATURE:END -->


`VTask.denselyOrderedSentence : (L : FirstOrder.Language) -> [L.IsOrdered] -> L.Sentence`

The first argument `L` is the first-order language, which must carry an ordered-language instance (the implicit `[L.IsOrdered]` constraint). This instance supplies the symbol for the strict-less-than relation `<`. The result is a *sentence* of `L` — a first-order formula with no free variables — whose intended meaning is that the ordering is dense.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total function from any ordered language `L` (satisfying `IsOrdered`) to a uniquely determined sentence, with no boundary cases or default-value choices involved.

## Worked examples

- Claim: `VTask.denselyOrderedSentence` for any ordered language `L` is satisfied in a structure `M` if and only if `M` is densely ordered in the mathematical sense (`DenselyOrdered M`).

- Claim: Any structure `M` carrying a `DenselyOrdered` instance satisfies `VTask.denselyOrderedSentence L`, i.e., `M ⊨ L.denselyOrderedSentence` holds whenever `DenselyOrdered M` holds.

- Claim: The sentence `VTask.denselyOrderedSentence L` is a `L.Sentence`, meaning it is a closed formula (a `BoundedFormula L Empty 0`) and in particular has no free variables.

- Claim: The rational numbers `ℚ` with their standard ordering satisfy `VTask.denselyOrderedSentence` for any ordered language `L`, since `ℚ` is a densely ordered set.

## Boundaries

- The definition requires the language `L` to have an `IsOrdered` instance. There is no way to form this sentence for a language not equipped with a notion of strict ordering.
- The sentence is a universal–existential sentence (∀∀∃ prefix), so it is not preserved under substructures in general (existential witnesses need not live in a substructure), but it is preserved downward under elementary substructures.
- Discrete ordered structures (e.g., the integers `ℤ`) do *not* satisfy this sentence, since there is no element strictly between consecutive integers.
- The empty ordered structure trivially satisfies the sentence (the universal hypothesis `x < y` is vacuously false everywhere), so the sentence holds vacuously over the empty domain.

## Not to be confused with

- `FirstOrder.Language.linearOrderSentence` (or similar): a sentence asserting that the order is a *linear* (total) order, which is a different axiom from density.
- `DenselyOrdered` (the Mathlib typeclass): this is a *semantic* Lean typeclass on a type, not a syntactic first-order sentence; the densely ordered sentence is the syntactic counterpart whose satisfaction is equivalent to this typeclass.
- `FirstOrder.Language.denselyOrdered` (if it exists as a theory): a *set* of sentences axiomatising dense linear orders without endpoints, which is a richer theory than just this single density sentence.