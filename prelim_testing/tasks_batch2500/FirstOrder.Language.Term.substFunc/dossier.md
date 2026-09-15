## Object

`VTask.substFunc` takes a term in a first-order language `L` over a variable type `α` and a "function substitution" — a mapping that sends each `n`-ary function symbol of `L` to an `L'`-term whose free variables are drawn from `Fin n` — and produces the corresponding term in `L'` over the same variable type `α`. Intuitively, it replaces every function symbol occurrence in the original term with the expression prescribed by the substitution, threading the original subterms through by substituting the formal arguments `0, 1, …, n-1` with the recursively transformed subterms.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.substFunc : {L : FirstOrder.Language} -> {L' : FirstOrder.Language} -> {α : Type u'} -> L.Term α → ({n : ℕ} → L.Functions n → L'.Term (Fin n)) → L'.Term α
<!-- PINNED-SIGNATURE:END -->


VTask.substFunc : {L : FirstOrder.Language} -> {L' : FirstOrder.Language} -> {α : Type u'} -> L.Term α → ({n : ℕ} → L.Functions n → L'.Term (Fin n)) → L'.Term α

- `L` is the source first-order language whose function symbols appear in the input term.
- `L'` is the target first-order language into which functions are translated.
- `α` is the type of free variables appearing in the term; the same variable type is inherited by the output term.
- The first explicit argument is the `L`-term to be transformed.
- The second explicit argument is the function substitution: for every arity `n` and every `n`-ary function symbol of `L`, it provides an `L'`-term whose free variables live in `Fin n` (representing the `n` argument positions).

## Conventions

The function substitution argument is never consulted for variable nodes, so it may be arbitrary on any portion of its domain not actually used by the input term. There are no junk-value conventions declared beyond this structural non-dependency.

## Worked examples

- Claim: For a term that is a plain variable `a`, `VTask.substFunc (var a) tf = var a` for any function substitution `tf`. The variable case passes through unchanged, independent of the substitution.

- Claim: Applying `VTask.substFunc` with the identity substitution `Functions.term` (which sends every function symbol `f` to its canonical term representation) is the identity on terms: for every `t : L.Term α`, `t.substFunc Functions.term = t`. This is the content of `substFunc_term`.

- Claim: Semantic correctness — when each element `c g` of the function substitution agrees in realisation with the original function `g` (i.e., the realisation of `c g` applied to the realised subterms equals the realisation of `g`), then the realisation of the substituted term under any variable valuation equals the realisation of the original term. This is the content of `realize_substFunc`.

## Boundaries

- When the input is a variable node `var a`, the output is exactly `var a`; the function substitution has no effect.
- When the input is a function application `func f ts`, the substitution for `f` is retrieved, and then the formal arguments `0, 1, …, n-1` in that replacement term are each substituted by the recursively transformed corresponding subterms `ts i`.
- The target language `L'` may differ arbitrarily from the source language `L`; the construction is fully heterogeneous.
- If the input term contains no function symbols (i.e., is a pure variable term), the output is the same term reinterpreted as an `L'`-term, irrespective of the function substitution provided.

## Not to be confused with

- `FirstOrder.Language.Term.subst`: substitutes free *variables* of a term with other terms, rather than substituting *function symbols* with terms.
- `FirstOrder.Language.LHom.onTerm`: applies a language homomorphism to a term, translating both function symbols and relation symbols uniformly, rather than allowing a per-symbol expression-level replacement.
- `FirstOrder.Language.Term.realize`: evaluates a term in a structure under a variable assignment; it produces a semantic value rather than a new syntactic term.