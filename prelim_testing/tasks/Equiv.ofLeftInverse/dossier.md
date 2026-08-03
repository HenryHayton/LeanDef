## Object

`VTask.ofLeftInverse` constructs a canonical equivalence (bijection) between a type `α` and the image of a function `f : α → β` in `β`, given that `f` admits a left inverse (a retraction) whenever `α` is nonempty. Because `f` has a left inverse on a nonempty `α`, it must be injective, so `α` bijects with its range.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofLeftInverse : {α : Sort u_3} -> {β : Type u_4} -> (f : α → β) -> (f_inv : Nonempty α → β → α) -> (hf : ∀ (h : Nonempty α), Function.LeftInverse (f_inv h) f) -> α ≃ ↑(Set.range f)
<!-- PINNED-SIGNATURE:END -->


`VTask.ofLeftInverse : {α : Sort u_3} -> {β : Type u_4} -> (f : α → β) -> (f_inv : Nonempty α → β → α) -> (hf : ∀ (h : Nonempty α), Function.LeftInverse (f_inv h) f) -> α ≃ ↑(Set.range f)`

The implicit argument `α` is the source sort; `β` is the target type. The argument `f` is the function whose range is to be shown equivalent to `α`. The argument `f_inv` is a candidate left inverse of `f`, but it is only required to be supplied when `α` is known to be nonempty (the `Nonempty α` guard allows the construction to remain well-typed when `α` is empty, since there is then no obligation to produce a meaningful inverse). The argument `hf` is the proof that, for every witness of nonemptiness, `f_inv h` is indeed a left inverse of `f`, i.e., `f_inv h (f a) = a` for all `a : α`.

## Conventions

When `α` is empty the equivalence is still well-defined: both sides are empty and the construction degenerates gracefully, even though `f_inv` and `hf` are never actually called. The gating of `f_inv` and `hf` on `Nonempty α` is deliberately more cautious than analogous constructions in stronger algebraic settings (e.g., linear or ring equivalences), where typeclass assumptions already rule out emptiness.

## Worked examples

- Claim: For `f : Fin 3 → ℕ` defined by `f i = i.val`, the forward direction of `VTask.ofLeftInverse f _ _` sends each `i : Fin 3` to the subtype element `⟨i.val, i, rfl⟩` in `Set.range f`.

- Claim: If `α` is a nonempty type and `f : α → β` has a left inverse `g`, then the forward map of `VTask.ofLeftInverse f (fun _ => g) (fun _ => hg)` applied to any `a : α` produces the element `⟨f a, ⟨a, rfl⟩⟩ : Set.range f`.

- Claim: When `α` is the empty type `Empty`, `VTask.ofLeftInverse f f_inv hf` is an equivalence between `Empty` and `Set.range f`, and the range is also empty regardless of the choice of `f_inv`.

- Claim: `VTask.ofLeftInverse f f_inv hf` equals `VTask.ofLeftInverse` applied with any other `f_inv'` and `hf'` satisfying the same left-inverse condition, because both are equal to the canonical `ofInjective f` equivalence (up to definitional equality of the underlying maps).

## Boundaries

- When `α` is empty (`IsEmpty α`): the equivalence still type-checks and is valid. The range of `f` is empty, so both sides are empty types. The `f_inv` and `hf` arguments are never evaluated.
- When `α` is nonempty: the left-inverse condition forces `f` to be injective, so the range has exactly as many elements as `α`, and the equivalence is a genuine bijection.
- The construction requires `β : Type` (not merely `Sort`) because `Set.range f` lives in `Set β`, which requires `β` to be a type. The source `α` may be any `Sort`.
- The result is a *computable* equivalence: both the forward and inverse maps are definitionally given and do not rely on classical choice.

## Not to be confused with

- `VTask.ofLeftInverse'` (a related construction where `f_inv` is an unconditional function `β → α` without the `Nonempty α` guard, suitable when emptiness is not a concern).
- `Equiv.ofInjective`: constructs the same range equivalence directly from an injectivity proof rather than an explicit left inverse; `VTask.ofLeftInverse` is provably equal to this when both apply.
- `Function.LeftInverse`: the bare proposition that `g ∘ f = id`; `VTask.ofLeftInverse` *uses* this property to build a bundled `Equiv`, not merely to state it.