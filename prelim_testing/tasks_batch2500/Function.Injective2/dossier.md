## Object

`VTask.Injective2 f` is the proposition that the binary function `f : α → β → γ` is **injective when viewed as a function on pairs**: whenever `f` yields the same output on two input pairs, the two input pairs must be equal component-wise. Concretely, `f a₁ b₁ = f a₂ b₂` implies both `a₁ = a₂` and `b₁ = b₂`. This is exactly the classical injectivity of the uncurried map `(a, b) ↦ f a b`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Injective2 : {α : Sort u_1} -> {β : Sort u_2} -> {γ : Sort u_3} -> (f : α → β → γ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Injective2 : {α : Sort u_1} -> {β : Sort u_2} -> {γ : Sort u_3} -> (f : α → β → γ) -> Prop`

The three universe-polymorphic type arguments `α`, `β`, and `γ` are the domain types of the two inputs and the codomain type respectively; they are inferred implicitly. The single explicit argument `f` is the binary function whose injectivity is being asserted.

## Conventions

No junk-value or boundary conventions are declared for this definition: it is a universally-quantified `Prop` that is simply `True` or `False` for every binary function `f`, with no distinguished degenerate inputs that require special treatment.

## Worked examples

- Claim: `VTask.Injective2 (· + · : ℕ → ℕ → ℕ)` is **false** — addition is not injective as a binary function, since e.g. `1 + 2 = 0 + 3` but `1 ≠ 0`.

- Claim: `VTask.Injective2 (Prod.mk : α → β → α × β)` holds for any types `α` and `β`, because `(a₁, b₁) = (a₂, b₂)` immediately gives `a₁ = a₂` and `b₁ = b₂`.

- Claim: If `VTask.Injective2 f` holds and `f a₁ b₁ = f a₂ b₂`, then in particular `a₁ = a₂` (the first components agree).

- Claim: `VTask.Injective2 (fun (a : ℕ) (b : ℕ) => (a, b))` holds, since the pairing map is injective.

## Boundaries

- When `γ` is a subsingleton (all elements are equal), **every** binary function `f : α → β → γ` trivially satisfies the condition vacuously only if `α` and `β` are also subsingletons; otherwise, there exist `a₁ ≠ a₂` with `f a₁ b₁ = f a₂ b₂`, so `VTask.Injective2 f` can fail.
- When `α` or `β` is empty, the universal quantification is vacuously true, so `VTask.Injective2 f` holds for any `f`.
- When `α` and `β` are both singletons, `VTask.Injective2 f` holds trivially for any `f` because there is only one pair of inputs.
- The definition gives a **conjunction** `a₁ = a₂ ∧ b₁ = b₂` as the conclusion; both components of the input pair must simultaneously agree, not just one.

## Not to be confused with

- `Function.Injective f` (unary injectivity): applies to a one-argument function `f : α → β`; `VTask.Injective2` extends this notion to two arguments.
- `Function.Injective (Function.uncurry f)`: the uncurried form of the same property; logically equivalent to `VTask.Injective2 f` but stated differently.
- Separately injective in each argument (fixing the other): a strictly weaker notion where `f a · ` is injective for each fixed `a` and `f · b` is injective for each fixed `b`, which does not imply joint injectivity.
