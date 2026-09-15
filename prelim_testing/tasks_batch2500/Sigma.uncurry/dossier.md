## Object

`VTask.uncurry` converts a dependently-typed two-argument function into a one-argument function whose input is a dependent pair (sigma type). Concretely, given a function `f` that takes a base value `x : α` and a fibre value `y : β x` and returns an element of the type `γ x y`, `VTask.uncurry f` accepts a single sigma-pair `⟨x, y⟩ : Σ x : α, β x` and returns `f x.fst x.snd : γ x.fst x.snd`. It is the right-to-left direction of the canonical currying bijection for dependent functions over sigma types.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.uncurry : {α : Type u_1} -> {β : α → Type u_4} -> {γ : (a : α) → β a → Type u_7} -> (f : (x : α) → (y : β x) → γ x y) -> (x : Sigma β) -> γ x.fst x.snd
<!-- PINNED-SIGNATURE:END -->


`VTask.uncurry : {α : Type u_1} -> {β : α → Type u_4} -> {γ : (a : α) → β a → Type u_7} -> (f : (x : α) → (y : β x) → γ x y) -> (x : Sigma β) -> γ x.fst x.snd`

- `α` is the base type indexing the sigma type; it is inferred.
- `β` is the type family over `α` forming the fibres of the sigma type; it is inferred.
- `γ` is the dependent return-type family: for each base element and each fibre element it specifies the type of the result; it is inferred.
- `f` is the curried dependent function to be uncurried: it takes the base element and fibre element as separate arguments.
- `x` is the dependent pair on which the uncurried function is evaluated.

## Conventions

There are no junk-value or edge-case conventions declared for this definition: the function is total over all inputs (every sigma pair has a well-defined first and second projection), and no special output is assigned to any degenerate input.

## Worked examples

- Claim: Evaluating `VTask.uncurry` on the sigma pair `⟨0, true⟩` where `f n b = b` recovers `f 0 true = true`.
  ```lean
  example : VTask.uncurry (fun (n : Nat) (b : Bool) => b) ⟨0, true⟩ = true := rfl
  ```

- Claim: Evaluating `VTask.uncurry` on `⟨"hello", 3⟩` where `f s n = n + 1` gives `4`.
  ```lean
  example : VTask.uncurry (fun (_ : String) (n : Nat) => n + 1) ⟨"hello", 3⟩ = 4 := rfl
  ```

- Claim: `VTask.uncurry` and `Sigma.curry` are mutual inverses: `Sigma.curry (VTask.uncurry f) = f` for any compatible `f`.

- Claim: `VTask.uncurry (Sigma.curry g) = g` for any compatible `g : (Σ x, β x) → γ x.fst x.snd`.

## Boundaries

- When the sigma type is empty (i.e., `α` is uninhabited or all fibres `β a` are empty), the resulting function has an empty domain and is trivially well-defined but can never be applied.
- When `α` has a single element and each fibre is a singleton, `VTask.uncurry f` is a function on a one-element type and simply returns `f` applied to the unique pair.
- The function is total: it is defined for every dependent pair in `Σ x : α, β x` without restriction.
- The result type `γ x.fst x.snd` may itself be a `Prop`, a `Type`, or any universe level, so `VTask.uncurry` works uniformly across universe levels.

## Not to be confused with

- `Function.uncurry`: the non-dependent uncurrying for ordinary product types `α × β → γ`, which does not handle fibre-dependent return types.
- `Sigma.curry`: the inverse operation that takes a function on `Σ x, β x` and splits it into a two-argument curried function.
- `(Equiv.piCurry γ).symm`: the same mathematical bijection packaged as an equivalence, which provides additional structure (inverses, bijectivity proofs) but agrees with `VTask.uncurry` at the function level.
