## VTask.relabel

### Object

Given a first-order language `L` and a function `g : α → β` between two sets of variable labels, `VTask.relabel g` is the operation that substitutes every variable occurrence in an `L`-term over `α` with the corresponding variable label supplied by `g`, leaving the function symbols and the tree structure of the term completely unchanged. It is the canonical covariant action of the category of sets on terms: it transports a term along a renaming of its variable names.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.relabel : {L : FirstOrder.Language} -> {α : Type u'} -> {β : Type v'} -> (g : α → β) -> L.Term α → L.Term β
<!-- PINNED-SIGNATURE:END -->


`VTask.relabel : {L : FirstOrder.Language} -> {α : Type u'} -> {β : Type v'} -> (g : α → β) -> L.Term α → L.Term β`

The implicit argument `L` is the first-order language whose signature (function symbols and arities) is shared by both the input and output term. The implicit type `α` is the type of variable labels used in the source term, and `β` is the type of variable labels used in the resulting term. The explicit argument `g` is the renaming function that maps each source variable label to its target variable label. The final argument is the source term to be relabelled.

### Conventions

The operation is structurally total: every `L.Term α` is accepted with no restrictions on `g`, `α`, or `β`. There are no junk-value conventions to declare because the function has no boundary cases that produce a meaningless default.

### Worked examples

- Claim: Relabelling by the identity function returns the original term unchanged. For any `L`, `α`, and term `t : L.Term α`, `t.relabel id = t`.

- Claim: Relabelling by `g` and then by `h` is the same as relabelling once by `h ∘ g`. For any `f : α → β`, `g : β → γ`, and `t : L.Term α`, `(t.relabel f).relabel g = t.relabel (g ∘ f)`.

- Claim: Evaluating a relabelled term under an environment `v : β → M` gives the same result as evaluating the original term under the pre-composed environment `v ∘ g`. That is, `(t.relabel g).realize v = t.realize (v ∘ g)`.

- Claim: For a constant term (one with no variable leaves), relabelling by any function `g` produces a term equal to relabelling by any other function `h`, since no variable leaves exist to distinguish `g` from `h`.

### Boundaries

- **Identity renaming**: `VTask.relabel id` is definitionally (and provably) equal to the identity function on `L.Term α`.
- **Constant terms**: A term built entirely from function symbols with no `var` leaves is unchanged by any renaming, since `g` is only applied at variable leaves.
- **Non-injective `g`**: If `g` identifies two distinct variable labels, the resulting term may conflate variables that were distinct in the source; the operation does not require `g` to be injective.
- **Non-surjective `g`**: Variable labels in `β` outside the range of `g` simply do not appear in the image term; this is perfectly valid.
- **Composition law**: Sequentially applying `VTask.relabel f` and then `VTask.relabel g` yields the same term as a single application of `VTask.relabel (g ∘ f)`. This makes the family of `VTask.relabel` operations a functor from the category of types-and-functions into the category of term-sets-and-maps.

### Not to be confused with

- **`L.Term.subst` (substitution)**: Substitution replaces each variable with an entire term, not merely a new variable label; `VTask.relabel` is the special case where each variable is replaced by another variable.
- **`L.Formula.relabel`**: The analogous relabelling operation on first-order *formulas* rather than *terms*; formulas additionally carry quantifiers that bind variables, requiring extra care.
- **`L.BoundedFormula.relabel`**: Relabelling on bounded (partially-quantified) formulas, which involves both free and bound variable index management beyond what term relabelling requires.