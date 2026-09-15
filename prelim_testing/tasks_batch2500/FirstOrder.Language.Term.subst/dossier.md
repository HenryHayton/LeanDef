## Object

`VTask.subst` performs substitution on a first-order term: given a term `t` built from variables (drawn from type `α`) and function symbols, and a mapping `tf` that sends each variable to a replacement term (over variables of type `β`), `VTask.subst t tf` is the term obtained by simultaneously replacing every variable occurrence `a` in `t` with `tf a`, leaving the function-symbol structure intact.

This is the standard notion of (simultaneous) substitution for first-order terms, which is the fundamental operation underlying instantiation, unification, and the composition of substitutions in formal logic.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subst : {L : FirstOrder.Language} -> {α : Type u'} -> {β : Type v'} -> L.Term α → (α → L.Term β) → L.Term β
<!-- PINNED-SIGNATURE:END -->


VTask.subst : {L : FirstOrder.Language} -> {α : Type u'} -> {β : Type v'} -> L.Term α → (α → L.Term β) → L.Term β

The implicit argument `L` is the first-order language, fixing the available function symbols and their arities. The implicit argument `α` is the type of variables appearing in the input term. The implicit argument `β` is the type of variables that may appear in the output terms. The first explicit argument is the term being substituted into. The second explicit argument is the substitution map: a function assigning to each variable of type `α` a replacement term over `β`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total function defined by structural recursion on the constructors of `L.Term α`, and every input combination yields a well-defined result with no distinguished edge convention needed.

## Worked examples

- Claim: Substituting a term `t` under the identity substitution `var` returns a term with the same variable structure — that is, for any variable `a : α`, `VTask.subst (var a) var = var a`.

- Claim: Applying `VTask.subst` to a `var a` node with substitution `tf` yields exactly `tf a` — the variable is directly replaced by its image under `tf`.

- Claim: Applying `VTask.subst` to a function-application term `func f ts` with substitution `tf` yields `func f (fun i => VTask.subst (ts i) tf)` — the function symbol and arity are preserved, and substitution is pushed into each argument.

- Claim: Composing two substitutions is associative in the sense that `VTask.subst (VTask.subst t tf₁) tf₂ = VTask.subst t (fun a => VTask.subst (tf₁ a) tf₂)` — this is the fundamental monadic/bind law for first-order terms.

## Boundaries

- When the input term is a bare variable `var a`, the result is simply `tf a` — no recursive structure is traversed.
- When the input term is a function application `func f ts` with no arguments (a constant symbol, where the arity is zero), the result is `func f (fun i => ...)` with the empty argument tuple, which is effectively the same constant — constants are unaffected by any substitution.
- The types `α` and `β` are arbitrary and can coincide or differ; when `α = β` and `tf = var`, the substitution acts as the identity.
- There is no restriction requiring `tf` to be injective, surjective, or even to produce distinct terms; it is an arbitrary function.

## Not to be confused with

- `L.Term.realize` (or term evaluation): that operation maps variables to elements of a structure, not to other terms, and returns a domain element rather than a new term.
- Renaming / `L.Term.relabel`: that operation changes the type indexing variables by applying a function on variable names, but does not replace variables with arbitrary terms — it is a special case of `VTask.subst` where `tf = var ∘ f`.
- Substitution of formulas: `VTask.subst` operates on terms only; substituting terms for free variables in a first-order formula is a separate, more involved operation.