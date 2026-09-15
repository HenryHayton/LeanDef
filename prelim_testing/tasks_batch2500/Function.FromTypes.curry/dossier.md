## Object

`VTask.curry` converts a function that takes a *single* dependent-tuple argument `(i : Fin n) → p i` into an equivalent *iterated* (curried) function whose arguments are supplied one type at a time. The result type `Function.FromTypes p τ` is the nested function type `p 0 → p 1 → … → p (n-1) → τ` built from the family `p`. In other words, `VTask.curry` is the canonical currying isomorphism for heterogeneous finite-arity functions.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.curry : {n : ℕ} -> {p : Fin n → Type u} -> {τ : Type u} -> (((i : Fin n) → p i) → τ) → Function.FromTypes p τ
<!-- PINNED-SIGNATURE:END -->


`VTask.curry : {n : ℕ} -> {p : Fin n → Type u} -> {τ : Type u} -> (((i : Fin n) → p i) → τ) → Function.FromTypes p τ`

- `n` is the (implicit) arity — the number of arguments the resulting curried function will accept.
- `p` is the (implicit) type family, assigning to each position `i : Fin n` the type of the argument at that position.
- `τ` is the (implicit) return type of the whole function.
- The explicit argument is the function to be curried: it takes a full dependent tuple `(i : Fin n) → p i` and produces a value of type `τ`.

The output is the curried form `Function.FromTypes p τ`, i.e. `p 0 → p 1 → … → p (n-1) → τ`.

## Conventions

When `n = 0` the only element of `(i : Fin 0) → p i` is the empty tuple (there are no arguments), so `VTask.curry f` evaluates `f` at that unique empty tuple and returns a plain value of type `τ` — no function arrows remain.

## Worked examples

- Claim: For `n = 0`, `VTask.curry` applied to a 0-ary function `f : (i : Fin 0 → p i) → ℕ` that returns `42` is just the value `42 : Function.FromTypes (fun _ => ℕ) ℕ`, which is `42 : ℕ`.

- Claim: For `n = 2` with `p = ![ℕ, Bool]`, `VTask.curry (fun t => if t 1 then t 0 + 1 else t 0)` has type `ℕ → Bool → ℕ`, and applying it to `3` then `true` gives `4`.

- Claim: `VTask.curry` and `Function.FromTypes.uncurry` form an inverse pair: for any `f : ((i : Fin n) → p i) → τ`, applying `uncurry` to `VTask.curry f` recovers `f` (stated as `Function.FromTypes.uncurry_curry`).

- Claim: Applying `VTask.curry f` to a first argument `a : p 0` yields `VTask.curry (f ∘ Fin.cons a)`, reducing the arity by one (stated as `Function.FromTypes.curry_apply_succ`).

## Boundaries

- **Arity 0 (`n = 0`):** The result type `Function.FromTypes p τ` reduces to `τ` itself (no arrows). `VTask.curry f` is not a function but a value; it is obtained by applying `f` to the unique empty dependent tuple.
- **Arity 1 (`n = 1`):** The result is a simple (non-dependent) function `p 0 → τ`.
- **General arity:** The recursion peels off one argument at a time, so the result is a fully iterated nested function.
- The function is total on all inputs; there are no domain restrictions.

## Not to be confused with

- `Function.FromTypes.uncurry`: the inverse operation — takes a `Function.FromTypes p τ` and produces a function from a dependent tuple to `τ`.
- `Function.curry`: the standard (non-dependent, binary) currying `(α × β → γ) → α → β → γ`; `VTask.curry` generalises this to any finite heterogeneous arity.
- `Fin.cons` / `Fin.tail`: tuple constructors/destructors used internally when reasoning about how curried arguments are assembled, not the currying operation itself.