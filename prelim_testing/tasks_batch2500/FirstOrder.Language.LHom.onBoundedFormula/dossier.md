## VTask.onBoundedFormula

### Object

Given a language map (a homomorphism of first-order languages) `g : L →ᴸ L'`, `VTask.onBoundedFormula g` is the induced map that translates any bounded formula of `L` with `k` free de Bruijn-style bound variables and free variables drawn from a set `α` into a corresponding bounded formula of `L'` with the same structure. Every logical connective and quantifier is preserved exactly; only the function symbols, relation symbols, and constant symbols appearing in terms and atomic formulas are relabelled via `g`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.onBoundedFormula : {L : FirstOrder.Language} -> {L' : FirstOrder.Language} -> {α : Type u'} -> (g : L →ᴸ L') -> {k : ℕ} -> L.BoundedFormula α k → L'.BoundedFormula α k
<!-- PINNED-SIGNATURE:END -->


`{L : FirstOrder.Language} -> {L' : FirstOrder.Language} -> {α : Type u'} -> (g : L →ᴸ L') -> {k : ℕ} -> L.BoundedFormula α k → L'.BoundedFormula α k`

The implicit argument `L` is the source first-order language; `L'` is the target first-order language. The implicit type `α` is the sort of free variables appearing in the formula. The explicit argument `g` is the language homomorphism used to translate all symbols. The implicit natural number `k` tracks the number of bound variables, ensuring the result lives in the same "bounded arity" as the input. The final explicit argument is the bounded formula of `L` to be translated.

### Conventions

The map is defined by structural recursion on the five constructors of `BoundedFormula`: falsum, equality, relation application, implication, and universal quantification. There are no junk values or partiality conventions because every well-formed bounded formula maps to a well-formed bounded formula of the same shape.

### Worked examples

- Claim: Applying `VTask.onBoundedFormula` to `falsum` (the ⊥ formula) always returns `falsum` in the target language, regardless of the language map.

- Claim: Applying the identity language map `LHom.id L` via `VTask.onBoundedFormula` to any bounded formula `ψ` returns exactly `ψ` unchanged; i.e., `(LHom.id L).onBoundedFormula ∘ id = id` on `L.BoundedFormula α n`.

- Claim: For composable language maps `ψ : L →ᴸ L'` and `φ : L' →ᴸ L''`, applying the composite map `(φ.comp ψ).onBoundedFormula` agrees with first applying `ψ.onBoundedFormula` and then `φ.onBoundedFormula`; that is, `(φ.comp ψ).onBoundedFormula = φ.onBoundedFormula ∘ ψ.onBoundedFormula`.

- Claim: If `M` carries an `L'`-structure and `φ : L →ᴸ L'` is an expansion on `M`, then a bounded formula `ψ` of `L` and its translate `VTask.onBoundedFormula φ ψ` are realized by the same variable assignments in `M`.

### Boundaries

- **falsum**: The absurdity constant `⊥` has no symbols to translate; it maps to `falsum` in `L'`.
- **Equality atoms**: Both terms in an equality are translated via the companion term-translation function induced by `g`; the equality connective itself is preserved.
- **Relation atoms**: The relation symbol is relabelled by `g`, and each argument term is translated; the arity is preserved by the language-homomorphism contract.
- **Implication**: Both sub-formulas are translated recursively; the logical structure is unchanged.
- **Universal quantification**: The body is translated recursively; the bound-variable count `k` increments as expected inside the `all` constructor, and the result has the same `k` as the input at the outer level.
- The type index `k` is invariant: a formula of arity `k` always maps to a formula of arity `k`, so no coercion or re-indexing occurs.

### Not to be confused with

- **`LHom.onTerm`**: Translates individual terms (not full formulas) along a language map; `VTask.onBoundedFormula` calls this as a subroutine on term subexpressions.
- **`LHom.onFormula`**: The special case of `VTask.onBoundedFormula` for *sentences* (formulas with no free variables, `α = Empty` and `k = 0`); `VTask.onBoundedFormula` is the general bounded version.
- **`BoundedFormula.mapTermRel`**: A lower-level combinator that replaces terms and relation symbols by arbitrary functions, not necessarily induced by a language homomorphism; `VTask.onBoundedFormula` is a special structured case of that operation.