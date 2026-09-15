## Object

`VTask.realize v t` is the element of the model `M` obtained by evaluating the first-order term `t` under the variable assignment `v`. Concretely, every occurrence of a variable `k` in `t` is replaced by the element `v k`, and every application of an `n`-ary function symbol `f` to sub-terms is replaced by the interpretation of `f` in `M` applied to the already-evaluated sub-terms. The result is a single element of the carrier set `M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.realize : {L : FirstOrder.Language} -> {M : Type w} -> [L.Structure M] -> {α : Type u'} -> (v : α → M) -> (_t : L.Term α) -> M
<!-- PINNED-SIGNATURE:END -->


`VTask.realize : {L : FirstOrder.Language} -> {M : Type w} -> [L.Structure M] -> {α : Type u'} -> (v : α → M) -> (_t : L.Term α) -> M`

The implicit argument `L` is the first-order language (its function symbols and arities). The implicit argument `M` is the carrier type of the model. The instance argument supplies the interpretation of `L`'s function symbols and relation symbols in `M`. The implicit argument `α` is the type indexing the free variables of the term. The explicit argument `v` is the variable assignment: a function sending each variable index to a concrete element of `M`. The explicit argument `_t` is the first-order term being evaluated.

## Conventions

The function is total: every term and every variable assignment yields exactly one element of `M`, with no junk values or default conventions required.

## Worked examples

- Claim: For a variable term `var k`, `VTask.realize v (var k) = v k` — the value is simply the assignment applied to the index.

- Claim: For a term built from a nullary function symbol (a constant) `c`, `VTask.realize v c.term = c` — the realization of a constant term is the element that the structure assigns to that constant, regardless of the variable assignment.

- Claim: For a term `t.subst tf` obtained by substituting terms `tf a` for each variable `a`, evaluating under `v` equals evaluating `t` under the assignment that first evaluates each `tf a` under `v`: `VTask.realize v (t.subst tf) = VTask.realize (fun a => VTask.realize v (tf a)) t`.

- Claim: For a unary function symbol `f` applied to a term `t`, `VTask.realize v (f.apply₁ t) = funMap f ![VTask.realize v t]`.

## Boundaries

- When `α` is the empty type (no variables), the variable assignment `v` is vacuously supplied (it is a function from the empty type) and every term is a closed term; `VTask.realize v t` still produces a well-defined element for any such `v`.
- The function handles the base case (variable terms) and the recursive case (function applications) uniformly; there are no partiality issues since terms are finitely constructed.
- Nested function applications are handled recursively: each sub-term is fully evaluated before the outer function symbol is interpreted.
- Lifting and substitution operations on terms commute with `VTask.realize` in the expected compositional way (see `realize_liftAt`, `realize_subst`).

## Not to be confused with

- `FirstOrder.Language.Formula.Realize` / formula realization: evaluates a formula to a truth value (`Prop`), not an element of `M`; it uses term realization internally but is a distinct, higher-level notion.
- `FirstOrder.Language.BoundedFormula.realize`: realization of bounded formulas (with both free and bound variables), which combines a variable assignment with a tuple for bound variables and returns a `Prop`.
- `FirstOrder.Language.Term.subst`: purely syntactic substitution of terms for variables, producing another term rather than evaluating to an element of a model.