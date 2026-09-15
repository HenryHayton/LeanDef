## Object

Given a binary relation symbol `r` in a first-order language `L`, `VTask.transitive r` is the first-order sentence in `L` asserting that `r` is transitive. In logical notation this is the universal sentence
$$\forall x\, \forall y\, \forall z\,\bigl(r(x,y) \land r(y,z) \to r(x,z)\bigr).$$
A structure `M` for `L` satisfies this sentence if and only if the binary relation on `M` induced by `r` is transitive in the ordinary mathematical sense.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.transitive : {L : FirstOrder.Language} -> (r : L.Relations 2) -> L.Sentence
<!-- PINNED-SIGNATURE:END -->


`VTask.transitive : {L : FirstOrder.Language} -> (r : L.Relations 2) -> L.Sentence`

The implicit argument `L` is the first-order language over which the sentence is built. The explicit argument `r` is a binary (arity-2) relation symbol from that language; it is the relation being asserted to be transitive.

## Conventions

The sentence is defined for every binary relation symbol without restriction; no edge case or junk-value convention is needed because the construction is total on `L.Relations 2`.

## Worked examples

- Claim: For any language `L` and binary relation symbol `r`, `VTask.transitive r` is a universal sentence (i.e., logically equivalent to a universally quantified sentence with no existential quantifiers), as witnessed by `Relations.isUniversal_transitive`.

- Claim: For a structure `M` and binary relation symbol `r`, `M ⊨ VTask.transitive r` if and only if the relation `fun x y => RelMap r ![x, y]` on `M` is an instance of `IsTrans`, i.e., the carrier set of `M` together with the interpretation of `r` forms a transitive relation.

- Claim: In the language of a single binary relation, interpreting it as the usual `≤` on `ℤ`, the resulting structure satisfies `VTask.transitive r` because `≤` on `ℤ` is transitive.

## Boundaries

- The argument `r` must have arity exactly 2 (type `L.Relations 2`); the definition is not applicable to relation symbols of other arities.
- The sentence is a purely universal (∀∀∀) sentence, so it is preserved under taking substructures: any substructure of a transitive structure is also transitive.
- There is no notion of a "trivial" or degenerate case: even for a language with only one model (the empty structure), the sentence is a well-formed `L.Sentence`.

## Not to be confused with

- `VTask.irreflexive` / `VTask.reflexive` — sentences asserting that a binary relation symbol is irreflexive or reflexive, not transitivity.
- `IsTrans` — a Lean typeclass asserting that a given *Lean-level* binary relation on a type is transitive; `VTask.transitive r` is the first-order *sentence* whose models are exactly the structures in which `r` is `IsTrans`.
- `VTask.boundedFormula₂` — the helper that builds an atomic formula from a relation symbol and two bounded variables; `VTask.transitive` uses it internally but is the full transitivity sentence, not a single atomic formula.