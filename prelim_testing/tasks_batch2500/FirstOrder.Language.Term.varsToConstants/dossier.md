## Object

`VTask.varsToConstants` converts a first-order term whose variable type is a disjoint sum `γ ⊕ α` into a term over the language `L` extended by constants of type `γ`, where the `α`-tagged variables remain as genuine variables and the `γ`-tagged variables are promoted to (new) constant symbols. In other words, it reinterprets one summand of a sum-typed variable set as a set of constants, leaving the other summand as the variable set of the output term.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.varsToConstants : {L : FirstOrder.Language} -> {α : Type u'} -> {γ : Type u_1} -> L.Term (γ ⊕ α) → (L.withConstants γ).Term α
<!-- PINNED-SIGNATURE:END -->


`VTask.varsToConstants : {L : FirstOrder.Language} -> {α : Type u'} -> {γ : Type u_1} -> L.Term (γ ⊕ α) → (L.withConstants γ).Term α`

- `L` is the base first-order language whose function symbols appear in the input term.
- `α` is the type indexing the "true" variables that remain as variables in the output term.
- `γ` is the type indexing the extra variables in the input that are to be treated as constants in the output; the output language is `L` augmented with a constant symbol for each element of `γ`.
- The single explicit argument is the input term, whose variable set is the disjoint sum `γ ⊕ α`.

## Conventions

The function is total with no junk-value conventions; every syntactic form of the input term is handled and produces a well-formed output term.

## Worked examples

- Claim: A variable tagged with `Sum.inr a` (a genuine variable) is sent to the variable `a` in the output term, i.e., `VTask.varsToConstants (var (Sum.inr a)) = var a`.

- Claim: A variable tagged with `Sum.inl c` (a "constant slot") is sent to the term consisting of the constant symbol corresponding to `c` in the expanded language, i.e., `VTask.varsToConstants (var (Sum.inl c)) = Constants.term (Sum.inr c)`.

- Claim: Under a suitable structure and expansion, `(VTask.varsToConstants t).realize v = t.realize (Sum.elim (fun a => L.con a) v)` — that is, evaluating the converted term under an assignment `v : α → M` gives the same result as evaluating the original term under the assignment that maps each `Sum.inl c` to the interpretation of constant `c` and each `Sum.inr a` to `v a`.

- Claim: For a function symbol application `func f ts`, `VTask.varsToConstants (func f ts)` is the term `func (Sum.inl f) (fun i => VTask.varsToConstants (ts i))`, reflecting that function nodes are rebuilt with the language injection and each subterm is recursively converted.

## Boundaries

- When `γ` is an empty type, no variables are promoted to constants; the output term lives over `L.withConstants (∅)` which is canonically isomorphic to `L` itself, and the original variables (all tagged `Sum.inr`) are preserved verbatim.
- When `α` is an empty type, the input term has no genuine variables; every leaf is either a function application or a `Sum.inl`-tagged constant slot. The output term is a closed term (no free variables) over the constant-extended language.
- The function operates purely syntactically: no model, interpretation, or semantic structure is required for the conversion.
- Composition with `constantsVarsEquivLeft.symm` relates `VTask.varsToConstants` to the inverse direction `constantsVarsEquivLeft`, providing a round-trip characterisation.

## Not to be confused with

- `FirstOrder.Language.Term.constantsVarsEquivLeft`: a bijective equivalence between terms with constants and terms with sum-variable types, of which `VTask.varsToConstants` is essentially one direction.
- `FirstOrder.Language.LHom.onTerm`: transports a term along a language homomorphism, which changes function symbols but does not promote variables to constants.
- `FirstOrder.Language.Term.relabel`: renames (relabels) the variable type of a term via a function, without introducing any new constant symbols.