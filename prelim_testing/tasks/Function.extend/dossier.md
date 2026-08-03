## Object

`VTask.extend f g j` is the **extension of `g` along `f`**: it is the function `β → γ` that agrees with `g` on the image of `f` (sending `f a` to `g a` for every `a : α`) and falls back to the auxiliary function `j` on all points of `β` that are not in the range of `f`.

Informally, if you have a function `g : α → γ` and you want to define a function on all of `β` that is consistent with `g` wherever `f` names a preimage, `VTask.extend f g j` does exactly that, using `j` as a fallback (or "junk value") off the image.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.extend : {α : Sort u_1} -> {β : Sort u_2} -> {γ : Sort u_3} -> (f : α → β) -> (g : α → γ) -> (j : β → γ) -> β → γ
<!-- PINNED-SIGNATURE:END -->


`{α : Sort u_1} -> {β : Sort u_2} -> {γ : Sort u_3} -> (f : α → β) -> (g : α → γ) -> (j : β → γ) -> β → γ`

The type variables `α`, `β`, `γ` are the source, intermediate, and target sorts respectively, inferred implicitly. The argument `f` is the function along which the extension is performed — it determines which points of `β` are "named" by elements of `α`. The argument `g` is the function being extended — its values at points named by `f` are preserved. The argument `j` is the fallback (auxiliary) function — it supplies output values for all `b : β` that have no preimage under `f`. The result is the extension, a function from `β` to `γ`.

## Conventions

When a point `b : β` has at least one preimage under `f`, classical choice is used to select *some* preimage `a` with `f a = b`, and the output is `g a`. This is well-defined in the mathematical sense only if `g` is constant on each fiber of `f` (i.e., `f a₁ = f a₂ → g a₁ = g a₂`, spelled `g.FactorsThrough f`); without this condition the output on the image of `f` may depend on the classical choice and should be considered junk as well.

## Worked examples

- Claim: For the inclusion `f : Fin 2 → ℕ` sending `0 ↦ 3, 1 ↦ 7`, the extension `VTask.extend f g j` applied to `3` equals `g 0`, where `g i = i.val + 10` and `j` is the constant `0`.

- Claim: For `f = id : ℕ → ℕ` (which is surjective), `VTask.extend id g j = g` as functions `ℕ → ℕ` for any `g j`, because every point of `ℕ` is in the range of `id`.

- Claim: For an empty source type `α = Empty`, `VTask.extend (Empty.elim) g j = j` for any `g` and `j`, since no point of `β` can be in the range of `f`.

- Claim: For the subtype inclusion `Subtype.val : {n : ℕ // n < 3} → ℕ`, `VTask.extend Subtype.val g j` applied to `5` (which is not less than `3`) equals `j 5`, because `5` has no preimage under `Subtype.val`.

## Boundaries

- **Empty source**: If `α` is an empty type, no point of `β` is in the range of `f`, so the extension equals `j` everywhere.
- **Surjective `f`**: If `f` is surjective, every `b : β` has a preimage, so `j` is never consulted. However, if `g` does not factor through `f`, the classical choice of preimage makes the result non-canonical.
- **`f` not injective and `g` not FactorsThrough**: Points in the image of `f` that have multiple preimages on which `g` disagrees will have their extension value determined by an arbitrary classical choice; mathematically the function is then ill-defined and its values outside this well-behaved regime should be treated as junk.
- **`j` as a zero or arbitrary constant**: A common idiom is to pass `0` (in a type with zero) or `Classical.arbitrary` as `j`, making the definition total but meaningful only on the image of `f`.
- **Injectivity guarantee**: When `f` is injective, there is at most one preimage for each `b`, so the classical choice is forced and `VTask.extend f g j (f a) = g a` holds definitively.

## Not to be confused with

- **`Function.FactorsThrough`**: A predicate asserting that `g` is constant on fibers of `f`; it is a condition *under which* `VTask.extend` behaves well, not the extension itself.
- **`Set.restrict`**: Goes the other direction — restricts a function's domain to a subset rather than extending it to a larger domain.
- **`Function.Surjective.hasRightInverse`/section constructions**: Provide a right inverse to a surjection; related but concern the inverse direction rather than extending a function along a map.