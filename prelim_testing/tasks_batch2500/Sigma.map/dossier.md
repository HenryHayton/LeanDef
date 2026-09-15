## Object

`VTask.map` transforms a dependent pair (sigma type) by simultaneously applying a function to its first component (the index) and a compatible function to its second component (the fiber value), yielding a new dependent pair in a possibly different sigma type.

More precisely, given a pair `⟨a, b⟩` where `a : α₁` and `b : β₁ a`, applying `VTask.map f₁ f₂` produces the pair `⟨f₁ a, f₂ a b⟩`, where the new index is `f₁ a` and the new fiber value is `f₂ a b : β₂ (f₁ a)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {α₁ : Type u_2} -> {α₂ : Type u_3} -> {β₁ : α₁ → Type u_5} -> {β₂ : α₂ → Type u_6} -> (f₁ : α₁ → α₂) -> (f₂ : (a : α₁) → β₁ a → β₂ (f₁ a)) -> (x : Sigma β₁) -> Sigma β₂
<!-- PINNED-SIGNATURE:END -->


VTask.map : {α₁ : Type u_2} -> {α₂ : Type u_3} -> {β₁ : α₁ → Type u_5} -> {β₂ : α₂ → Type u_6} -> (f₁ : α₁ → α₂) -> (f₂ : (a : α₁) → β₁ a → β₂ (f₁ a)) -> (x : Sigma β₁) -> Sigma β₂

The implicit arguments `α₁` and `α₂` are the source and target index types. The implicit arguments `β₁` and `β₂` are the source and target fiber families, indexed by `α₁` and `α₂` respectively. The explicit argument `f₁` is the function that transforms the index component. The explicit argument `f₂` is a family of functions, one for each source index `a`, that transforms the fiber value while respecting the index map: `f₂ a` carries a value in `β₁ a` to a value in `β₂ (f₁ a)`. The explicit argument `x` is the input dependent pair whose two components are to be mapped.

## Conventions

There are no junk-value or edge-case conventions for this definition: it is a total function on all sigma types, all index-transforming functions, and all fiber-transforming families, with no special behavior at boundary inputs.

## Worked examples

- Claim: `VTask.map` with `f₁ = Nat.succ` and `f₂ = fun _ (s : String) => s ++ "!"` sends `⟨(2 : Nat), ("hello" : String)⟩` viewed as a sigma over the constant `String` family to a pair with first component `3` and second component `"hello!"`.
  ```lean
  example : VTask.map (β₁ := fun _ : Nat => String) (β₂ := fun _ : Nat => String)
      Nat.succ (fun _ s => s ++ "!") ⟨2, "hello"⟩ = ⟨3, "hello!"⟩ := by
    rfl
  ```

- Claim: `VTask.map` with `f₁ = id` and `f₂ = fun _ n => n * 2` sends `⟨(true : Bool), (5 : Nat)⟩` in the constant-`Nat` sigma to `⟨true, 10⟩`.
  ```lean
  example : VTask.map (β₁ := fun _ : Bool => Nat) (β₂ := fun _ : Bool => Nat)
      id (fun _ n => n * 2) ⟨true, 5⟩ = ⟨true, 10⟩ := by
    rfl
  ```

- Claim: Mapping with identity functions on both components returns the original dependent pair unchanged.
  ```lean
  example (α : Type) (β : α → Type) (x : Sigma β) :
      VTask.map (f₁ := id) (f₂ := fun _ b => b) x = x := by
    cases x; rfl
  ```

- Claim: Composing two applications of `VTask.map` is the same as applying `VTask.map` once with composed functions: `VTask.map g₁ g₂ (VTask.map f₁ f₂ x) = VTask.map (g₁ ∘ f₁) (fun a b => g₂ (f₁ a) (f₂ a b)) x`.

## Boundaries

- When both `f₁` and `f₂` are identity-like (i.e., `f₁ = id` and `f₂ a = id`), the output equals the input unchanged.
- When `f₁` is not injective, distinct indices may be collapsed together in the output, but the function is still well-defined and total.
- When `f₂ a` is not injective for some `a`, distinct fiber values at that index may be collapsed; again, the function remains total and well-defined.
- There is no restriction on the types involved: the source and target fiber families may be entirely unrelated, as long as `f₂` provides the bridge.

## Not to be confused with

- `Sigma.mk`: constructs a single dependent pair from an index and a fiber value; does not transform an existing pair.
- `Prod.map`: maps both components of a plain (non-dependent) product; the fiber type does not depend on the first component.
- `PSigma.map`: the analogous operation for `PSigma` (where types may live in `Sort` rather than `Type`); structurally identical but for a different universe-polymorphic variant.