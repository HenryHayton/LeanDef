## VTask.freeVarFinset

### Object

Given a first-order formula with variables drawn from a type `α` and with at most `n` bound (de-Bruijn-indexed) variables, `VTask.freeVarFinset` computes the finite set of *free* variables—those drawn from `α` that appear in the formula and are not captured by any quantifier. The result is a `Finset α`, i.e., a concrete, duplicate-free, enumerable collection of the free variable names actually occurring in the formula.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.freeVarFinset : {L : FirstOrder.Language} -> {α : Type u'} -> [DecidableEq α] -> {n : ℕ} -> L.BoundedFormula α n → Finset α
<!-- PINNED-SIGNATURE:END -->


`{L : FirstOrder.Language}` is the first-order language (signature of function and relation symbols) over which the formula is built. `{α : Type u'}` is the type of free variable names used in the formula. `[DecidableEq α]` is a typeclass argument supplying decidable equality on `α`, required to construct finite sets. `{n : ℕ}` is the number of bound-variable slots available in the formula (its "binding depth"). The final argument is the bounded formula whose free variables are to be collected.

### Conventions

For the constant false formula (`falsum`), the free-variable set is the empty finset, since `falsum` contains no terms and hence no variable occurrences. For an equality atom `t₁ = t₂`, the free variables are the union of the free variables of the two terms. For a relation atom applied to a tuple of terms, the free variables are the union of the free variables of each term in the tuple. For an implication `f₁ → f₂`, the free variables are the union of the free-variable sets of the two subformulas. For a universally quantified formula `∀ x, f`, the free variables are exactly the free variables of the body `f`—the bound variable introduced by the quantifier does not appear in `α` and so does not contribute to the finset.

### Worked examples

- Claim: For the constant false formula `falsum` (of type `L.BoundedFormula α n`), `VTask.freeVarFinset falsum = ∅`.

- Claim: For an implication `f₁.imp f₂`, the free-variable finset is `VTask.freeVarFinset f₁ ∪ VTask.freeVarFinset f₂`.

- Claim: For a universally quantified formula `f.all`, `VTask.freeVarFinset f.all = VTask.freeVarFinset f`, i.e., universal quantification does not add any `α`-typed free variables.

- Claim: If a variable `a : α` does not appear in either subformula of an implication, then `a ∉ VTask.freeVarFinset (f₁.imp f₂)`.

### Boundaries

- **`falsum`**: returns `∅`; there are no terms involved.
- **Atomic equality**: variables come solely from the terms `t₁` and `t₂`; in particular the bound-variable index `n` is irrelevant.
- **Relation atom**: the finset is the union over all argument positions; if the relation has arity 0, the result is `∅`.
- **Universal quantifier**: the newly bound variable slot is a `Fin`-indexed de-Bruijn index, not an `α`-typed name, so it is invisible to `VTask.freeVarFinset`; the result equals the finset of the body.
- **No negation or existential constructor**: these are derived (negation is `imp _ falsum`; existential is `not (all (not _))`), so they are handled by the `imp` and `all` cases recursively.
- The output is always a finite set regardless of how deep or complex the formula is, because every recursive call terminates on a structurally smaller formula.

### Not to be confused with

- `FirstOrder.Language.Term.varFinsetLeft`: collects free variables of a *term*, not a formula; `VTask.freeVarFinset` calls this internally on term subexpressions.
- `FirstOrder.Language.BoundedFormula.restrictFreeVar`: uses the finset produced by `VTask.freeVarFinset` to coerce the free-variable type to a subtype, rather than merely computing which variables are free.
- `FirstOrder.Language.Formula.freeVarFinset` (if it exists as a specialisation): would apply to sentences or unbounded formulas, whereas `VTask.freeVarFinset` operates on the more general `BoundedFormula α n` type parameterised by binding depth `n`.
