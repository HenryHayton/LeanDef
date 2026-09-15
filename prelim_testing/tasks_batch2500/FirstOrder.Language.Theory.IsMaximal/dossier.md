## VTask.IsMaximal

### Object

A first-order theory `T` (over a language `L`) is *maximal* when two conditions both hold: the theory is satisfiable (it has at least one model), and the theory is *complete with respect to individual sentences* in the strongest possible sense — for every sentence `φ` of `L`, either `φ` itself belongs to `T`, or the negation of `φ` belongs to `T`. Intuitively, a maximal theory leaves no sentence undecided: it takes a definite stand (yes or no) on every possible first-order statement expressible in the language. Any maximal theory is in particular complete (it decides the truth value of every sentence in all of its models).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsMaximal : {L : FirstOrder.Language} -> (T : L.Theory) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{L : FirstOrder.Language} -> (T : L.Theory) -> Prop`

The implicit argument `L` is the first-order language over which sentences and theories are formed. The explicit argument `T` is the first-order `L`-theory being tested for maximality — a set of `L`-sentences.

### Conventions

No special junk-value or edge-case conventions are declared for this predicate: it is a straightforward conjunction of two independently meaningful conditions, and there is no distinguished default behavior for degenerate inputs.

### Worked examples

- Claim: If `T` is maximal (i.e., `VTask.IsMaximal T` holds), then for every sentence `φ`, either `φ ∈ T` or `φ.not ∈ T` — this is exactly the second conjunct of the definition.

- Claim: If `T` is maximal, then `T` is complete — meaning every sentence entailed by `T` (in the Boolean semantics) is actually a member of `T`, and `T` has no two models that disagree on any sentence.

- Claim: A consistent but incomplete theory (one that lacks both some sentence `φ` and its negation `φ.not`) does not satisfy `VTask.IsMaximal`, even if it is satisfiable.

- Claim: If `VTask.IsMaximal T` holds and `T ⊨ᵇ φ` for some sentence `φ`, then `φ ∈ T`.

### Boundaries

- The empty theory `∅` is not maximal: although one may argue vacuously about membership, the satisfiability condition requires an actual model, which the empty theory trivially has (in a nonempty language with a nonempty domain), but the membership condition fails for any sentence that is neither a tautology nor a contradiction.
- An unsatisfiable theory (one with no models) cannot be maximal, regardless of how many sentences it contains, because satisfiability is a strict requirement.
- A theory can contain both `φ` and `φ.not` and still formally satisfy the syntactic membership clause, but such a theory is inconsistent and thus not satisfiable, so it would fail the first conjunct and not be maximal.
- Maximality is a global property of the whole theory, not a local or finitary condition; it quantifies universally over all sentences of the language.

### Not to be confused with

- `Theory.IsComplete`: completeness only requires that the theory semantically decides every sentence (all models agree), but does not require the stronger syntactic condition that every sentence or its negation is literally a member of `T`; every maximal theory is complete, but not conversely.
- `Theory.IsSatisfiable`: mere satisfiability is only the first of the two conjuncts in `IsMaximal`; a satisfiable theory need not contain each sentence or its negation.
- A *maximal consistent set* in propositional logic: an analogous but distinct notion in a different (propositional, not first-order) setting; the first-order version here additionally requires satisfiability rather than just consistency.