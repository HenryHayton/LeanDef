## Object

Given a binary relation symbol `r` in a first-order language `L`, `VTask.antisymmetric r` is the first-order sentence expressing that `r` is antisymmetric: for all elements `x` and `y`, if `r(x, y)` and `r(y, x)` both hold, then `x = y`. This is the universal sentence `∀x ∀y (r(x,y) ∧ r(y,x) → x = y)` (written with implications instead of a conjunction, but semantically equivalent).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.antisymmetric : {L : FirstOrder.Language} -> (r : L.Relations 2) -> L.Sentence
<!-- PINNED-SIGNATURE:END -->


VTask.antisymmetric : {L : FirstOrder.Language} -> (r : L.Relations 2) -> L.Sentence

The implicit argument `L` is the first-order language in which the sentence lives. The explicit argument `r` is a binary relation symbol of `L` (a relation symbol of arity 2) whose antisymmetry is to be expressed.

## Conventions

No junk-value or edge-case conventions are declared for this definition: the construction is total and structurally well-defined for any language `L` and any binary relation symbol `r : L.Relations 2`.

## Worked examples

- Claim: For any language `L` and binary relation symbol `r : L.Relations 2`, `VTask.antisymmetric r` is a sentence (a formula with no free variables) in `L`.

- Claim: A structure `M` for `L` satisfies `VTask.antisymmetric r` if and only if the interpretation of `r` in `M` is an antisymmetric relation on the domain of `M`; that is, whenever `(a, b)` and `(b, a)` are both in the interpretation of `r`, then `a = b`.

- Claim: For the language of a single binary relation symbol and the unique relation symbol of arity 2 in that language, `VTask.antisymmetric` produces the standard antisymmetry axiom used in the theory of partial orders.

## Boundaries

- The function is only defined for relation symbols of arity exactly 2 (`L.Relations 2`); there is no version for unary or higher-arity symbols.
- If `L` has no binary relation symbols, then there are simply no inhabitants of `L.Relations 2` to pass, so the function cannot be applied—this is not a special case within the function itself.
- The sentence produced uses universal quantification over two variables and expresses implication (not conjunction), so it correctly handles vacuous cases: if `r` has no pairs `(a, b)` with both `r(a, b)` and `r(b, a)`, the sentence is trivially satisfied.

## Not to be confused with

- `VTask.irreflexive r`: the sentence expressing that `r` is irreflexive (`∀x ¬r(x,x)`), a related but distinct property.
- `VTask.symmetric r`: the sentence expressing symmetry (`∀x ∀y r(x,y) → r(y,x)`), which is almost the opposite of antisymmetry in intent.
- The *semantic* property of a structure being antisymmetric: `VTask.antisymmetric r` is a *syntactic* object (a sentence in the language), not a Prop about a particular model.