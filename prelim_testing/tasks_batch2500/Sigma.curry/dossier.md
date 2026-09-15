## VTask.curry

### Object

Given a function `f` that takes a single dependent pair (sigma type) `⟨x, y⟩` as input and returns a value in the type `γ x.fst x.snd`, `VTask.curry f` converts `f` into an equivalent two-argument function: first taking an element `x : α`, then a dependent argument `y : β x`, and returning a value in `γ x y`. This is the dependent generalisation of the familiar currying operation from ordinary function theory.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.curry : {α : Type u_1} -> {β : α → Type u_4} -> {γ : (a : α) → β a → Type u_7} -> (f : (x : Sigma β) → γ x.fst x.snd) -> (x : α) -> (y : β x) -> γ x y
<!-- PINNED-SIGNATURE:END -->


```
VTask.curry : {α : Type u_1} -> {β : α → Type u_4} -> {γ : (a : α) → β a → Type u_7} -> (f : (x : Sigma β) → γ x.fst x.snd) -> (x : α) -> (y : β x) -> γ x y
```

- `α` is the base type indexing the sigma type.
- `β` is the dependent type family over `α`, so that the sigma type `Σ x : α, β x` pairs an element of `α` with an element of `β x`.
- `γ` is the dependent return type family, indexed by both an element of `α` and an element of `β` over it.
- `f` is the function to be curried: it takes a dependent pair (sigma value) and returns an element of the appropriate fibre of `γ`.
- `x` is the first argument of the resulting curried function, an element of `α`.
- `y` is the second argument of the resulting curried function, an element of `β x`.

### Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total function on all well-typed inputs, and there are no degenerate inputs requiring special treatment.

### Worked examples

- Claim: For `f : (Σ n : Nat, Fin n) → Nat` defined by `f ⟨n, _⟩ = n`, `VTask.curry f 5 ⟨2, by omega⟩ = 5`.

- Claim: `VTask.curry` and `Sigma.uncurry` are mutual inverses — composing them in either order recovers the original function. Concretely, if `g : ∀ (x : α) (y : β x), γ x y`, then `VTask.curry (Sigma.uncurry g) = g`.

- Claim: For the constant family `γ x y = Nat`, currying preserves multiplication: if `f g : (Σ x : α, β x) → Nat`, then `VTask.curry (fun p => f p * g p) = fun x y => VTask.curry f x y * VTask.curry g x y`.

- Claim: For the non-dependent case where `α = Bool`, `β = fun _ => Bool`, and `γ = fun _ _ => String`, a function `f : (Σ _ : Bool, Bool) → String` curried at `true` and `false` gives `VTask.curry f true false = f ⟨true, false⟩`.

### Boundaries

- When `α` is empty (e.g., `α = Empty`), the curried function is vacuously defined and there are no inhabitants on which to evaluate it.
- When `β x` is empty for some particular `x`, the curried function at that `x` is vacuously defined.
- The operation is fully definitionally transparent: `VTask.curry f x y` reduces definitionally to `f ⟨x, y⟩` with no computation required.
- The operation is a bijection between the two function types; its inverse is `Sigma.uncurry`, and the round-trip identities `VTask.curry (Sigma.uncurry g) = g` and `Sigma.uncurry (VTask.curry f) = f` hold.

### Not to be confused with

- `Sigma.uncurry`: the inverse operation, converting a two-argument dependent function into a function on a sigma type.
- `Equiv.piCurry`: the bundled equivalence version of the same bijection, which also carries proof that the two directions are inverses; `VTask.curry` is just one direction of this equivalence.
- Ordinary (non-dependent) `Function.curry`: curries a function of a product type `α × β → γ` into `α → β → γ`; `VTask.curry` is the strictly more general dependent sigma analogue.