## Object

`VTask.Realize` assigns a truth value to a bounded first-order formula relative to a structure. A *bounded formula* over a language `L` with free-variable type `α` and `l` additional bound-variable slots is judged true or false once we supply an interpretation of the free variables (a function `α → M`) and a tuple of `l` elements of the carrier `M` filling the open bound-variable slots. Concretely:

- The absurdity formula is always false.
- An equality atom is true iff the two terms evaluate to the same element of `M`.
- A relation atom is true iff the interpretation of `L`'s relation symbol holds of the evaluated argument tuple.
- An implication is true iff the antecedent being true implies the consequent is true (in the usual logical sense).
- A universally quantified formula (one extra bound-variable slot) is true iff, for every element `x : M`, the body is true when `x` is appended to the bound-variable tuple.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Realize : {L : FirstOrder.Language} -> {M : Type w} -> [L.Structure M] -> {α : Type u'} -> {l : ℕ} -> (_f : L.BoundedFormula α l) -> (_v : α → M) -> (_xs : Fin l → M) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.Realize : {L : FirstOrder.Language} -> {M : Type w} -> [L.Structure M] -> {α : Type u'} -> {l : ℕ} -> (_f : L.BoundedFormula α l) -> (_v : α → M) -> (_xs : Fin l → M) -> Prop
```

`L` is the first-order language (providing function and relation symbols). `M` is the carrier type of the structure being evaluated in. The instance `[L.Structure M]` supplies the interpretations of `L`'s symbols in `M`. `α` is the type indexing the free (unbound) variables of the formula. `l` is the number of open bound-variable slots remaining in the formula (i.e., the formula has `l` variables that have been bound by quantifiers whose scope we are currently inside, awaiting concrete values). `_f` is the bounded formula to be evaluated. `_v` is the *free-variable assignment*: it sends each element of `α` to its value in `M`. `_xs` is the *bound-variable environment*: a tuple of `l` elements of `M` providing the values for the open bound-variable slots.

## Conventions

There are no declared junk-value or default conventions for this definition: it is a structurally recursive function on the constructors of `BoundedFormula`, so every input combination is handled explicitly and no out-of-domain or junk-value behavior applies.

## Worked examples

- Claim: For any structure on `M`, the formula `falsum` with any variable assignment realizes to `False`.

- Claim: For any structure on `M`, `(t₁.bdEqual t₂).Realize v xs` is equivalent to `t₁.realize (Sum.elim v xs) = t₂.realize (Sum.elim v xs)`.

- Claim: The universal formula `(all φ).Realize v xs` is equivalent to `∀ x : M, φ.Realize v (Fin.snoc xs x)`.

- Claim: An implication formula `(φ.imp ψ).Realize v xs` is equivalent to `φ.Realize v xs → ψ.Realize v xs`.

## Boundaries

- When `l = 0`, the bound-variable environment `_xs : Fin 0 → M` is the unique empty tuple; the formula is *closed* with respect to bound variables, so only the free-variable assignment `_v` matters for the evaluation of non-quantified parts.
- When `α` is `Empty` (or `PEmpty`) and `l = 0`, the formula is a *sentence* (no free or open bound variables), and `Realize` reduces to a pure statement about the structure `M`.
- The `all` constructor increases `l` by one; realizing such a formula decreases the open-slot count by requiring a universal choice over `M`, so the recursion always terminates.
- There is no partial application issue: the formula `falsum` always realizes to `False` regardless of the variable assignments; the assignments are ignored.

## Not to be confused with

- `FirstOrder.Language.Formula.Realize`: the specialization of `VTask.Realize` to *closed* bounded formulas (i.e., `BoundedFormula α 0`), which takes only the free-variable assignment `v : α → M` and no bound-variable tuple.
- `FirstOrder.Language.Sentence.Realize`: further specialized to sentences (`BoundedFormula Empty 0`), which takes only the structure; no variable assignment at all.
- `FirstOrder.Language.Term.realize`: evaluates a *term* (not a formula) to an element of `M`; used internally when computing equality and relation atoms, but is not itself a `Prop`.
