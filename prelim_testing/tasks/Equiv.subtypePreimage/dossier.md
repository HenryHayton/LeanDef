## Object

`VTask.subtypePreimage` constructs a canonical equivalence (bijection) between two types of functions. Given a predicate `p` on a type `α` and a fixed function `x₀` defined on the subtype of elements satisfying `p`, the equivalence identifies: on one side, all functions `x : α → β` that extend `x₀` (i.e., agree with `x₀` on elements satisfying `p`); on the other side, all functions defined only on elements *not* satisfying `p`. Intuitively, once the behaviour on `{a // p a}` is pinned to `x₀`, the only remaining freedom is what the function does on `{a // ¬p a}`, and this equivalence makes that correspondence precise.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subtypePreimage : {α : Sort u_1} -> {β : Sort u_4} -> (p : α → Prop) -> [DecidablePred p] -> (x₀ : { a // p a } → β) -> { x // x ∘ Subtype.val = x₀ } ≃ ({ a // ¬p a } → β)
<!-- PINNED-SIGNATURE:END -->


`VTask.subtypePreimage : {α : Sort u_1} -> {β : Sort u_4} -> (p : α → Prop) -> [DecidablePred p] -> (x₀ : { a // p a } → β) -> { x // x ∘ Subtype.val = x₀ } ≃ ({ a // ¬p a } → β)`

The type `α` is the domain type over which the predicate is defined. The type `β` is the codomain. The argument `p` is the predicate that splits `α` into two complementary subtypes. The instance `[DecidablePred p]` provides the computational ability to decide membership in `p` for each element. The argument `x₀` is the fixed function on the subtype `{a // p a}` that all functions in the domain of the equivalence must agree with. The result is an equivalence whose left-hand type is the subtype of total functions `α → β` that restrict to `x₀` on `{a // p a}`, and whose right-hand type is the unconstrained function type on `{a // ¬p a}`.

## Conventions

The forward direction of the equivalence sends a constrained function `x : α → β` (satisfying `x ∘ Subtype.val = x₀`) to its restriction to `{a // ¬p a}`. The inverse direction sends a function `y : {a // ¬p a} → β` to the function on all of `α` that uses `x₀` on elements satisfying `p` and uses `y` on elements not satisfying `p`; the proof obligation that this extension agrees with `x₀` on `{a // p a}` is satisfied by construction.

## Worked examples

- Claim: For `α = Bool`, `p = id`, `x₀ = fun _ => 0`, and the function `x : Bool → ℕ` sending `true ↦ 0, false ↦ 7`, the forward map of the equivalence applied to `x` (paired with its agreement proof) evaluates at `⟨false, id⟩` to `7`.

- Claim: The inverse of the equivalence, applied to a function `y : {b : Bool // ¬(b = true)} → ℕ` sending the unique element to `42`, yields a total function `Bool → ℕ` that sends `true` to `x₀ ⟨true, rfl⟩` (the value prescribed by `x₀`) and `false` to `42`.

- Claim: For `p : α → Prop` with `DecidablePred p` and any `x₀`, the equivalence `VTask.subtypePreimage p x₀` is a bijection: its composition with its own inverse is the identity on `{a // ¬p a} → β`.

- Claim: Given `p a = True` for all `a`, the type `{a // ¬p a}` is empty, so `VTask.subtypePreimage p x₀` is an equivalence between a one-element type (there is exactly one extension of `x₀` to all of `α`, namely `x₀` itself composed with the obvious retraction) and the unique function from the empty subtype.

## Boundaries

If `p` is the always-true predicate, then `{a // ¬p a}` is empty, and the right-hand side `{a // ¬p a} → β` is a singleton (there is exactly one function from an empty type). Correspondingly the left-hand side has exactly one element: `x₀` extended trivially. The equivalence correctly identifies the two singletons.

If `p` is the always-false predicate, then `{a // p a}` is empty, so `x₀` is the unique function from the empty subtype, every function `α → β` vacuously satisfies `x ∘ Subtype.val = x₀`, and the equivalence reduces to the identity equivalence between `α → β` and `α → β` (since `{a // ¬p a} = α`).

The equivalence is well-typed for any `Sort`-valued `α` and `β`, not only `Type`-valued ones, as the universe polymorphism in the signature indicates.

## Not to be confused with

- `Equiv.subtypeEquiv`: relates two subtypes of possibly different types via a given equivalence between the ambient types, rather than splitting a function type by a predicate.
- `Equiv.piEquivPiSubtypeProd`: decomposes a product of functions by splitting the domain via a predicate into a product of two function types, without fixing the value on one part.
- `Equiv.subtypeRestrictEquiv` or similar restriction maps: these go from functions on a subtype to functions on a subtype, not from constrained extensions to unrestricted functions on the complement.