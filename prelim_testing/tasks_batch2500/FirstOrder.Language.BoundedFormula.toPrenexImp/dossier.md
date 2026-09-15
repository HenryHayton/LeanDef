## VTask.toPrenexImp

### Object
`VTask.toPrenexImp φ ψ` is a prenex normal form of the implication `φ → ψ`, constructed under the assumption that both `φ` and `ψ` are already in prenex normal form. The operation works by pulling quantifiers from the antecedent `φ` outward (with appropriate variable-index adjustments), flipping existential quantifiers to universal and vice versa as they cross the implication, and recursing until the antecedent is quantifier-free, at which point the remaining quantifier-shuffling is handled by the auxiliary `toPrenexImpRight`. The result is logically equivalent to `φ.imp ψ` (the raw implication) and is again in prenex normal form.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toPrenexImp : {L : FirstOrder.Language} -> {α : Type u'} -> {n : ℕ} -> L.BoundedFormula α n → L.BoundedFormula α n → L.BoundedFormula α n
<!-- PINNED-SIGNATURE:END -->


The implicit argument `L` is the first-order language whose syntax is used. The implicit argument `α` is the type of free variables that may appear in the formula. The implicit natural number `n` bounds the number of "bound" (de Bruijn-indexed) free variable slots. The first explicit argument `φ` is the antecedent formula, assumed to be in prenex normal form. The second explicit argument `ψ` is the consequent formula, also assumed to be in prenex normal form.

### Conventions

This operation is only guaranteed to produce a prenex normal form when both input formulas are already in prenex normal form; feeding non-prenex inputs may still produce a result, but its prenex status is not assured. When `φ` is quantifier-free, `VTask.toPrenexImp φ ψ` coincides with the auxiliary `toPrenexImpRight φ ψ`, which handles the consequent side.

### Worked examples

- Claim: If `φ` is quantifier-free and `ψ` is in prenex normal form, then `VTask.toPrenexImp φ ψ` equals `VTask.toPrenexImpRight φ ψ`.

- Claim: If `φ = ∃x, φ'` and both `φ` and `ψ` are prenex, then `VTask.toPrenexImp φ ψ` is a prenex normal form for `(∃x, φ') → ψ`, which is logically equivalent to `∀x, φ' → ψ[x↦x]` (with `ψ` having its bound variables lifted); the result carries a leading universal quantifier.

- Claim: If `φ = ∀x, φ'` and both `φ` and `ψ` are prenex, then `VTask.toPrenexImp φ ψ` carries a leading existential quantifier, reflecting that `(∀x, φ') → ψ` is equivalent to `∃x, φ' → ψ` (with variable lifting).

- Claim: For any prenex `φ` and prenex `ψ`, the formula `VTask.toPrenexImp φ ψ` is itself in prenex normal form.

- Claim: For any prenex `φ` and prenex `ψ`, the realization of `VTask.toPrenexImp φ ψ` in any structure under any variable assignment coincides with the realization of the plain implication `φ.imp ψ`.

### Boundaries

- When both `φ` and `ψ` are quantifier-free (in particular, atomic or quantifier-free combinations), the operation reduces directly to `toPrenexImpRight`, which in that case simply returns the plain implication `φ.imp ψ`.
- The operation is defined for all `BoundedFormula α n` inputs, regardless of prenex status, but semantic equivalence to `φ.imp ψ` and the prenex-output guarantee only hold under the hypothesis that both inputs are prenex.
- Variable indices in `ψ` are lifted by 1 at depth `n` whenever a quantifier is pulled out of `φ`, to maintain correct de Bruijn indexing.

### Not to be confused with

- `VTask.toPrenexImpRight`: the companion operation that prenexifies an implication by pulling quantifiers from the *consequent* `ψ`, used as a subroutine once `φ` is quantifier-free.
- `FirstOrder.Language.BoundedFormula.toPrenex`: the top-level function that converts an arbitrary formula to prenex normal form, of which `toPrenexImp` is an auxiliary.
- `FirstOrder.Language.BoundedFormula.imp`: the raw (non-prenex) implication constructor, which simply forms `φ → ψ` without any quantifier manipulation.