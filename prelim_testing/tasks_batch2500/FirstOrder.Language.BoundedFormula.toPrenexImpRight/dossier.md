## Object

Given a bounded first-order formula `φ` and a bounded formula `ψ`, `VTask.toPrenexImpRight φ ψ` produces a formula in prenex normal form (all quantifiers pulled to the front) that is semantically equivalent to the implication `φ → ψ`. The procedure works by hoisting any leading universal or existential quantifiers from `ψ` outward, adjusting `φ` by lifting its bound variables appropriately at each step so that scoping remains correct. When `ψ` has no leading quantifier, the result is simply the literal implication `φ → ψ`. This function is an auxiliary helper for the general algorithm that converts any bounded formula into prenex normal form.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toPrenexImpRight : {L : FirstOrder.Language} -> {α : Type u'} -> {n : ℕ} -> L.BoundedFormula α n → L.BoundedFormula α n → L.BoundedFormula α n
<!-- PINNED-SIGNATURE:END -->


`VTask.toPrenexImpRight : {L : FirstOrder.Language} -> {α : Type u'} -> {n : ℕ} -> L.BoundedFormula α n → L.BoundedFormula α n → L.BoundedFormula α n`

The language parameter `L` is the first-order language over which formulas are built. The type `α` is the type of free variables that may appear in formulas. The natural number `n` is the number of bound variable slots available, i.e., both input formulas and the output formula are `n`-bounded. The first `BoundedFormula` argument (`φ`) is intended to be quantifier-free and plays the role of the antecedent. The second `BoundedFormula` argument (`ψ`) is intended to already be in prenex normal form and plays the role of the consequent; quantifiers are pulled from this argument to the outside of the resulting implication.

## Conventions

The function is designed to be meaningful (in the sense of prenex-normality and semantic equivalence) only when `φ` is quantifier-free and `ψ` is in prenex normal form. When these preconditions hold, the output is guaranteed to be in prenex normal form and logically equivalent to `φ → ψ`. Outside these preconditions, the function still produces a well-typed formula, but no guarantee of prenex normality or semantic equivalence with `φ → ψ` is given.

## Worked examples

- Claim: When `ψ` is quantifier-free (e.g., `ψ = φ.imp φ` for a quantifier-free `φ`), `VTask.toPrenexImpRight φ ψ` equals `φ.imp ψ` — the result is just the plain implication with no quantifier prefix.

- Claim: When `ψ = BoundedFormula.ex θ` (an existential), pulling the quantifier outward gives `(φ.liftAt 1 n).toPrenexImpRight θ` wrapped in an existential — the bound variable count in `φ` is extended by one to match the body's depth before recursing.

- Claim: When `ψ = BoundedFormula.all θ` (a universal), the result is `((φ.liftAt 1 n).toPrenexImpRight θ).all` — a universal quantifier is prepended to the recursively-constructed inner implication.

- Claim: `isPrenex_toPrenexImpRight` — if `φ` is quantifier-free and `ψ` is in prenex normal form, then `VTask.toPrenexImpRight φ ψ` is in prenex normal form.

- Claim: `realize_toPrenexImpRight` — if `φ` is quantifier-free and `ψ` is in prenex normal form, then `VTask.toPrenexImpRight φ ψ` and `φ.imp ψ` have the same realization under any variable assignment.

## Boundaries

- If `ψ` is quantifier-free, the result is definitionally equal to `φ.imp ψ` with no quantifier prefix, regardless of the structure of `φ`.
- If `ψ` begins with an existential quantifier `∃`, the existential is hoisted outward and the recursion continues on the body of `ψ`, with `φ` lifted to accommodate the extra bound variable.
- If `ψ` begins with a universal quantifier `∀`, similarly the universal is hoisted and the recursion continues.
- The function terminates because it recurses on the structure (depth of quantifier prefix) of `ψ`.
- If `φ` is not quantifier-free, the output may not be in prenex normal form even if `ψ` is; the prenex-normality guarantee requires `φ` to be quantifier-free.

## Not to be confused with

- `BoundedFormula.toPrenexImp`: the sibling operation that handles the case where the antecedent `φ` may itself carry quantifiers; `toPrenexImpRight` only peels quantifiers from the consequent.
- `BoundedFormula.toPrenex`: the top-level algorithm that converts any bounded formula to prenex normal form, which calls `toPrenexImpRight` as an auxiliary.
- `BoundedFormula.imp`: the raw implication constructor, which simply forms `φ → ψ` without any prenex-normalization.
