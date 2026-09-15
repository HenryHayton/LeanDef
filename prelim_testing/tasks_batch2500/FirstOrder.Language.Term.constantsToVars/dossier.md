## Object

`VTask.constantsToVars` converts a first-order term built over the language `L` *extended with constants drawn from a type `γ`* (written `L[[γ]]`) into an ordinary `L`-term whose variable sort is the disjoint union `γ ⊕ α`. Intuitively, every constant symbol `c : γ` that appears in the input term is replaced by a fresh variable tagged with `Sum.inl c`, while every original variable `a : α` is re-tagged as `Sum.inr a`. The language itself shrinks back to `L`, since the constant symbols have been "demoted" to variables.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.constantsToVars : {L : FirstOrder.Language} -> {α : Type u'} -> {γ : Type u_1} -> (L.withConstants γ).Term α → L.Term (γ ⊕ α)
<!-- PINNED-SIGNATURE:END -->


VTask.constantsToVars : {L : FirstOrder.Language} -> {α : Type u'} -> {γ : Type u_1} -> (L.withConstants γ).Term α → L.Term (γ ⊕ α)

- `L` is the base first-order language (implicit).
- `α` is the type indexing the original free variables of the input term (implicit).
- `γ` is the type of constant symbols that have been adjoined to `L` to form the extended language `L[[γ]]` (implicit).
- The explicit argument is a term of the extended language `L[[γ]]` over variables `α`; it is the term whose constants are to be converted into variables.

## Conventions

There are no junk-value or edge-case conventions to declare for this function: the function is structurally total over all well-formed terms of the extended language, and every case (variables, nullary function symbols, higher-arity function symbols) is handled unambiguously.

## Worked examples

- Claim: Applying `VTask.constantsToVars` to a pure variable `var a` in `L[[γ]]` yields `var (Sum.inr a)` in `L`.

- Claim: A constant symbol `c : γ` appearing as a nullary `L[[γ]]`-function term is mapped to the variable `var (Sum.inl c)` in the output `L`-term.

- Claim: If `t : L[[γ]].Term β` is realized in a structure `M` that is an expansion via `lhomWithConstants L γ`, then `t.constantsToVars.realize (Sum.elim (fun a => L.con a) v) = t.realize v`. (This is the key semantic soundness property: demoting constants to variables and then substituting the original constant interpretations recovers the original realization.)

- Claim: A proper (non-nullary) `L`-function symbol `f` applied to arguments `ts` in `L[[γ]]` is mapped by `VTask.constantsToVars` to the same function symbol `f` applied to the recursively converted arguments.

## Boundaries

- **Pure-variable terms**: A term `var a` contains no constant symbols, so `VTask.constantsToVars` simply re-tags the variable to the right summand: `var (Sum.inr a)`.
- **Constant symbols (nullary extended functions)**: A constant `c : γ` disguised as a zero-arity function in `L[[γ]]` becomes `var (Sum.inl c)` in the output — it is now a variable, not a function application.
- **Ordinary nullary `L`-function symbols**: A genuine nullary symbol of the base language `L` has no arguments to recurse on and is preserved as a zero-arity function application in the output.
- **Higher-arity function symbols**: Any function symbol of arity ≥ 1 must originate from the base language `L` (since `γ` only contributes constants, i.e., arity-0 symbols); the function symbol is kept and each argument is converted recursively. Attempting to have a higher-arity symbol from the constants side is ruled out by an `isEmptyElim`, since no such symbol can exist.
- **Empty `γ`**: If `γ` is an empty type there are no constant symbols to convert, so `VTask.constantsToVars` acts as a simple renaming of variables from `α` to `Empty ⊕ α`.

## Not to be confused with

- `FirstOrder.Language.LHom.onTerm` — the general transport of a term along a language homomorphism; `VTask.constantsToVars` is a specific instance that additionally changes the variable type.
- `FirstOrder.Language.Term.constantsVarsEquivLeft` — a bijective equivalence that further reassociates the variable sort when both ordinary variables and constants-turned-variables are present; it is built on top of `VTask.constantsToVars` via a relabeling.
- `FirstOrder.Language.Term.varsToConstants` — the inverse direction, promoting extra variables of sort `γ ⊕ α` back into constant symbols, yielding a term of `L[[γ]]`.