## VTask.restrictVar

### Object

Given a first-order term `t` whose free variables come from some type `α`, and a function `_f` defined on exactly the finite set of variables that actually appear in `t`, `VTask.restrictVar t _f` produces a new term of the same logical shape (same function symbols, same tree structure) but whose variables now live in the target type `β`. Every variable occurrence `a` in `t` is replaced by `_f(a)` (where `a` is viewed as an element of the variable-finset of `t`). The result is a term over `β` whose semantic value under any valuation `v : β → M` agrees with the original term's value under the valuation `a ↦ v(_f(a))`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restrictVar : {L : FirstOrder.Language} -> {α : Type u'} -> {β : Type v'} -> [DecidableEq α] -> (t : L.Term α) -> (_f : ↥t.varFinset → β) -> L.Term β
<!-- PINNED-SIGNATURE:END -->


`VTask.restrictVar : {L : FirstOrder.Language} -> {α : Type u'} -> {β : Type v'} -> [DecidableEq α] -> (t : L.Term α) -> (_f : ↥t.varFinset → β) -> L.Term β`

The implicit argument `L` is the first-order language (specifying function symbols and their arities). The implicit arguments `α` and `β` are the source and target variable types, respectively. The `DecidableEq α` instance is needed to compute the finite set of variables appearing in `t`. The explicit argument `t` is the term being transformed. The argument `_f` is a function whose domain is the subtype consisting exactly of the variables that occur in `t` (i.e., the elements of `t.varFinset`), and whose codomain is `β`; it specifies where each occurring variable should be sent.

### Conventions

The function `_f` is only required to be defined on variables that actually appear in `t` (the membership of `t.varFinset`), not on all of `α`. This is the key design choice: no junk value is needed for variables outside the finset, so there are no junk-value conventions to declare.

### Worked examples

- Claim: For a variable term `var a`, `VTask.restrictVar (var a) f = var (f ⟨a, _⟩)`, i.e., the result is again a variable term, with the variable relabelled by `f`.

- Claim: For a function-application term `func F ts`, `VTask.restrictVar (func F ts) f` equals `func F` applied pointwise to the restricted sub-terms, where each `ts i` is restricted via the restriction of `f` to the variables of `ts i` (a sub-finset of the whole finset). This means the function symbol and arity are preserved exactly.

- Claim: The semantic value of `VTask.restrictVar t f` under a valuation `v : β → M` equals the semantic value of `t` under the valuation `a ↦ v (f ⟨a, ha⟩)` for any valuation agreeing with `f` in this way. Formally: if `∀ a, v (f a) = v' a` then `(VTask.restrictVar t f).realize v = t.realize v'`.

- Claim: If `s` is a set containing all variables of `t` and `h : ↑t.varFinset ⊆ s`, then using the inclusion `Set.inclusion h` as the function `f` yields a term that realizes to the same value as the original under any valuation restricted to `s`.

### Boundaries

- If `t` is a variable term `var a`, then `t.varFinset` is the singleton `{a}`, so `_f` must only be defined at the single element `⟨a, mem_singleton_self a⟩`. The output is `var (f ⟨a, _⟩)`, a variable term in the target language.
- If `t` is a constant (a 0-ary function symbol applied to an empty tuple), then `t.varFinset` is empty, `_f` is the unique function from the empty type, and `VTask.restrictVar t _f = t` (modulo the trivial re-labelling).
- The function `_f` does not need to be injective or surjective; variables in `β` may coincide or be left unused.
- The language `L`, function symbols, and the tree structure of `t` are preserved exactly; only variable leaves change.

### Not to be confused with

- `L.Term.relabel` (or similar renamings): A full relabelling takes a function `α → β` defined on *all* of `α`, not just on the variables appearing in `t`; `VTask.restrictVar` is the more economical version requiring only the variables that occur.
- `VTask.restrictVarLeft`: A sibling operation for terms over a sum type `α ⊕ γ` that restricts only the left ("bound") variables, leaving the right component untouched.
- `Finset.restrict` or set-theoretic restriction: A restriction of a *function* to a smaller domain, unrelated to first-order terms.
