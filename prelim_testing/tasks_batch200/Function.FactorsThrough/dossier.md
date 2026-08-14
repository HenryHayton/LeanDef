## Object

`VTask.FactorsThrough g f` is the proposition that the function `g : α → γ` *factors through* the function `f : α → β`, meaning that `f` separates points at least as finely as `g` does. Concretely, whenever `f` maps two elements `a` and `b` to the same value, `g` must also map them to the same value. Equivalently (when `γ` is nonempty), there exists a function `e : β → γ` such that `g = e ∘ f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.FactorsThrough : {α : Sort u_1} -> {β : Sort u_2} -> {γ : Sort u_3} -> (g : α → γ) -> (f : α → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.FactorsThrough : {α : Sort u_1} -> {β : Sort u_2} -> {γ : Sort u_3} -> (g : α → γ) -> (f : α → β) -> Prop`

The three universe-polymorphic sorts `α`, `β`, `γ` are implicit and inferred. The first explicit argument `g` is the function whose behavior is being constrained — the one that is claimed to factor. The second explicit argument `f` is the function that plays the role of the "quotient map" or "projection": it determines which pairs of inputs must agree under `g`.

## Conventions

There are no junk-value or out-of-domain conventions to declare: `VTask.FactorsThrough` is a universally-quantified proposition over all inputs, and is well-formed and meaningful for any functions `g` and `f` between any types.

## Worked examples

- Claim: If `f : ℕ → Bool` is the parity function `f n = n % 2 == 0` and `g : ℕ → Bool` is the same parity function, then `VTask.FactorsThrough g f` holds because `g = id ∘ f`.

- Claim: The constant function `g a = 0` factors through any function `f`, since `f a = f b` trivially implies `g a = g b = 0`.

- Claim: If `f : α → β` is injective, then every function `g : α → γ` factors through `f`, because `f a = f b` implies `a = b` (by injectivity), which in turn implies `g a = g b`.

- Claim: `VTask.FactorsThrough g f` does *not* hold in general when `g` identifies fewer points than `f`: for instance, if `f` is the constant function and `g` is injective on a type with more than one element, then `f a = f b` for all `a, b` but `g a ≠ g b` for some pair.

## Boundaries

- When `α` is empty, `VTask.FactorsThrough g f` holds vacuously for all `g` and `f`, since there are no elements to check.
- When `f` is injective, `VTask.FactorsThrough g f` holds for every `g`, because injectivity of `f` means `f a = f b → a = b → g a = g b`.
- When `g` is constant (or more generally, when `g` maps all elements to the same value), `VTask.FactorsThrough g f` holds for every `f`.
- The proposition is not symmetric: `VTask.FactorsThrough g f` and `VTask.FactorsThrough f g` have independent truth values in general.
- There is no restriction on the sorts involved; `α`, `β`, `γ` may be propositions (`Prop`), types, or higher sorts.

## Not to be confused with

- `Function.Injective`: states that `f` is injective; a related but distinct concept — injectivity of `f` implies everything factors through `f`, but `VTask.FactorsThrough g f` is a relationship between a specific pair of functions.
- `Function.Surjective`: states that `f` is surjective, which is a dual condition about coverage, not about how another function relates to `f`.
- `Function.LeftInverse` / `Function.RightInverse`: these describe retractions and sections between `f` and some other map, which is a strictly stronger condition than factoring through.
