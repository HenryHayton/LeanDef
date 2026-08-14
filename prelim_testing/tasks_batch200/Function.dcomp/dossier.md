## Object

`VTask.dcomp` is the **dependent function composition** operator. Given a dependent function `f` whose output type may depend on both its explicit argument and an implicit index, and a function `g` that for each index produces a value in a type family, `VTask.dcomp f g` is the function that applies `g` first and then feeds the result to `f`. In symbols, `(VTask.dcomp f g) x = f (g x)`, where the type of `g x` depends on `x`, and the type of `f (g x)` depends on both `x` and `g x`. It is the analogue of ordinary function composition `(∘)` lifted to the setting where intermediate and output types vary fibre-wise.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dcomp : {α : Sort u₁} -> {β : α → Sort u₂} -> {φ : {x : α} → β x → Sort u₃} -> (f : {x : α} → (y : β x) → φ y) -> (g : (x : α) → β x) -> (x : α) -> φ (g x)
<!-- PINNED-SIGNATURE:END -->


`VTask.dcomp : {α : Sort u₁} -> {β : α → Sort u₂} -> {φ : {x : α} → β x → Sort u₃} -> (f : {x : α} → (y : β x) → φ y) -> (g : (x : α) → β x) -> (x : α) -> φ (g x)`

The implicit universe-polymorphic sorts `α`, `β`, and `φ` set up the dependent type structure. Specifically:
- `α` is the index type; `x : α` is the shared index that coordinates everything.
- `β` is a type family over `α`; each `β x` is the type in which `g` lands at index `x`.
- `φ` is a type family over the total space of `β`; each `φ y` (for `y : β x`) is the output type of `f` at that fibre element.
- `f` is the **outer function**: given an index `x` (implicit) and an element `y : β x`, it produces a value of type `φ y`.
- `g` is the **inner function**: given an index `x`, it produces an element of `β x`.
- `x` is the **point** at which the composed function is evaluated.
The result has type `φ (g x)`, reflecting that the return type depends on both the index and the output of `g`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total, universe-polymorphic function with a direct pointwise computation rule and imposes no restrictions on its inputs.

## Worked examples

- Claim: When `g : ℕ → Fin 3` is the constant function returning `⟨0, by decide⟩` and `f : Fin 3 → Bool` is `Fin.val · == 0`, then `VTask.dcomp f g 7 = true`.
  ```lean
  example : VTask.dcomp (fun (y : Fin 3) => decide (y.val = 0)) (fun (_ : Nat) => (⟨0, by decide⟩ : Fin 3)) 7 = true := by decide
  ```

- Claim: `VTask.dcomp f g` applied at `x` always equals `f (g x)` (the defining unfolding). In particular for `f := List.length` and `g := fun n : ℕ => List.replicate n ()`, `VTask.dcomp List.length (fun n => List.replicate n ()) 4 = 4`.
  ```lean
  example : VTask.dcomp List.length (fun n => List.replicate n ()) 4 = 4 := by decide
  ```

- Claim: When `α = Unit`, `β = fun _ => ℕ`, and `φ = fun n => Fin (n + 1)`, `VTask.dcomp (fun n => (⟨0, Nat.zero_lt_succ n⟩ : Fin (n + 1))) (fun _ => 3) ()` has type `Fin 4`.

## Boundaries

- The definition is **total**: it is defined for all universe levels and all input types, including propositional sorts (`Prop`).
- When `β` is a constant family (i.e., `β _ = B` for some fixed type `B`) and `φ` is also constant, `VTask.dcomp` reduces to ordinary function composition `(∘)`.
- Applying `VTask.dcomp f g` at any `x` reduces definitionally to `f (g x)` by the computation rule `dcomp_apply`.
- There are no restrictions on whether `α`, `β`, or `φ` are types or propositions; the construction works uniformly across all `Sort` universes.

## Not to be confused with

- **`Function.comp` (`∘`)**: ordinary (non-dependent) function composition where all types are fixed, not varying with the index.
- **`Function.comp₂` or `bicompl`**: composition of binary or multi-argument non-dependent functions; different arity.
- **`Function.dite` / dependent `if-then-else`**: another form of dependent combination of functions, but conditioned on a decidable proposition rather than by sequential application.