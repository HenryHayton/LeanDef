## VTask.restrictVarLeft

### Object

Given a first-order term whose variable type is a disjoint sum `α ⊕ γ`, `VTask.restrictVarLeft` produces a new term of type `β ⊕ γ` by renaming only the "left" variables (those of type `α`) according to a supplied function, while leaving all "right" variables (those of type `γ`) unchanged. The function is not required to be defined on all of `α`, only on the finite set of left-variables that actually appear in the term (`varFinsetLeft`), making this a restriction in the precise sense: the domain of the renaming map is restricted to exactly the variables that are needed.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restrictVarLeft : {L : FirstOrder.Language} -> {α : Type u'} -> {β : Type v'} -> [DecidableEq α] -> {γ : Type u_2} -> (t : L.Term (α ⊕ γ)) -> (_f : ↥t.varFinsetLeft → β) -> L.Term (β ⊕ γ)
<!-- PINNED-SIGNATURE:END -->


`VTask.restrictVarLeft : {L : FirstOrder.Language} -> {α : Type u'} -> {β : Type v'} -> [DecidableEq α] -> {γ : Type u_2} -> (t : L.Term (α ⊕ γ)) -> (_f : ↥t.varFinsetLeft → β) -> L.Term (β ⊕ γ)`

- `L` is the first-order language (its function and relation symbols) to which the term belongs.
- `α` is the type indexing the "left" variables that may appear in `t`.
- `β` is the target type for left variables after renaming.
- The `DecidableEq α` instance is required to build and manipulate the finite set of left-variables.
- `γ` is the type indexing the "right" variables, which pass through unchanged.
- `t` is the term to be operated on; its variables live in `α ⊕ γ`.
- `_f` is the renaming function, whose domain is exactly the finite set of left-variables actually occurring in `t` (the subtype `↥t.varFinsetLeft`); it assigns each such variable a value in `β`.

### Conventions

There are no junk-value conventions to declare: the function is total on every well-typed input (each `t` and compatible `f`) and the construction is deterministic with no distinguished "default" behaviour at any boundary.

### Worked examples

- Claim: For a term consisting solely of a right variable `Sum.inr c`, applying `restrictVarLeft` with any (vacuous) `f` returns `var (Sum.inr c)` unchanged, since no left variables appear.

- Claim: For a term `var (Sum.inl a)` whose `varFinsetLeft` is the singleton `{a}`, applying `restrictVarLeft f` where `f` maps the unique element to some `b : β` yields `var (Sum.inl b)`.

- Claim: Semantics are preserved by `restrictVarLeft`: if `xs : β ⊕ γ → M` is an assignment and `xs' : α → M` satisfies `xs (Sum.inl (f a)) = xs' a` for every `a` in `t.varFinsetLeft`, then `(t.restrictVarLeft f).realize xs = t.realize (Sum.elim xs' (xs ∘ Sum.inr))`.

- Claim: When the renaming `f` is the restriction of an inclusion `Set.inclusion h` for some superset `s ⊇ t.varFinsetLeft`, the realization of the restricted term under a suitably composed assignment equals the realization of the original term.

### Boundaries

- When `t` contains no left variables at all (`varFinsetLeft t = ∅`), the function `_f` has empty domain and is vacuously supplied; the result is the same term with left-variable type changed to `β` but no actual left variables present.
- When `t = var (Sum.inr c)` for any `c : γ`, the result is exactly `var (Sum.inr c)` regardless of `f`.
- When `t = var (Sum.inl a)`, the result is `var (Sum.inl (f ⟨a, _⟩))` using the unique membership proof that `a ∈ varFinsetLeft t`.
- For compound terms built by function application, the renaming is propagated recursively to each subterm, with `f` restricted appropriately to the left-variables of each subterm.

### Not to be confused with

- `FirstOrder.Language.Term.relabel`: renames *all* variables (both left and right) via a function on the entire variable type `α ⊕ γ`, rather than only the left component.
- `FirstOrder.Language.Term.varFinsetLeft`: the finite set of left-variables actually occurring in a term — this is the domain type of `_f` in `VTask.restrictVarLeft`, not the operation itself.
- `FirstOrder.Language.Term.substitute` / `realize`: substitution and semantic evaluation replace variables with *terms* or *values*, whereas `VTask.restrictVarLeft` only renames the left variable indices.