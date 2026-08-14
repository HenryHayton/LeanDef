## 1. Object

`VTask.image2 f s t` is the **binary image** of a function `f : α → β → γ` applied to a pair of sets `s ⊆ α` and `t ⊆ β`. It is the set of all values `f a b` where `a` ranges over `s` and `b` ranges over `t`:

$$\{\, f(a,b) \mid a \in s,\; b \in t \,\} \subseteq \gamma.$$

Equivalently, if one uncurries `f` to obtain a single function `f̃ : α × β → γ`, then `VTask.image2 f s t` is exactly the ordinary (unary) image of `f̃` applied to the Cartesian product `s × t`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.image2 : {α : Type u} -> {β : Type v} -> {γ : Type w} -> (f : α → β → γ) -> (s : Set α) -> (t : Set β) -> Set γ
<!-- PINNED-SIGNATURE:END -->


The universe-polymorphic type parameters `α`, `β`, `γ` are the element types of the input and output sets. The argument `f` is the binary function being "lifted" to a set-level operation — it consumes one element of `α` and one element of `β` to produce an element of `γ`. The argument `s` is the first input set, a subset of `α`; the argument `t` is the second input set, a subset of `β`. The result is a subset of `γ`.

## 3. Conventions

When `s` is empty, `VTask.image2 f s t` is the empty set, regardless of `t` and `f`, because no element `a ∈ s` exists to form any pair. Symmetrically, when `t` is empty, the result is again the empty set. These junk-free conventions follow from the existential membership condition: an element of the binary image must witness both a source in `s` and a source in `t`.

## 4. Worked examples

- Claim: `VTask.image2 (· + ·) {1, 2} {10, 20} = {11, 21, 12, 22}` (as sets of natural numbers — every pairwise sum appears).
  ```lean
  example : VTask.image2 (· + ·) ({1, 2} : Set ℕ) {10, 20} = {11, 21, 12, 22} := by
    ext x; simp [VTask.image2]; omega
  ```

- Claim: `VTask.image2 f ∅ t = ∅` for any `f` and `t` — the binary image of the empty set on the left is empty.
  ```lean
  example (f : α → β → γ) (t : Set β) : VTask.image2 f ∅ t = ∅ := by
    ext; simp [VTask.image2]
  ```

- Claim: `VTask.image2 (· * ·) {2} {3, 5} = {6, 10}` (as natural numbers).
  ```lean
  example : VTask.image2 (· * ·) ({2} : Set ℕ) {3, 5} = {6, 10} := by
    ext x; simp [VTask.image2]; omega
  ```

- Claim: If `(VTask.image2 f s t).Nonempty` then `s.Nonempty` — nonemptiness of the binary image implies nonemptiness of both inputs.

## 5. Boundaries

- **Empty first set**: If `s = ∅` then `VTask.image2 f s t = ∅`, since no witness for the first argument can exist.
- **Empty second set**: If `t = ∅` then `VTask.image2 f s t = ∅`, by the same reasoning.
- **Singleton sets**: `VTask.image2 f {a} {b} = {f a b}`, a singleton containing exactly the single value.
- **Non-injective `f`**: Different pairs `(a₁, b₁)` and `(a₂, b₂)` may yield the same value `f a₁ b₁ = f a₂ b₂`; the result is still a set, so the value appears only once.
- **Non-surjective `f`**: Values of `γ` not expressible as `f a b` with `a ∈ s`, `b ∈ t` do not appear in the result.
- **Both sets nonempty**: The result is nonempty if and only if both `s` and `t` are nonempty (given that `f` is total, which it always is here).

## 6. Not to be confused with

- **`Set.image f s`** (unary image): lifts a *single-argument* function over one set; `VTask.image2` is its binary analogue and is not the same as applying `Set.image` twice in sequence.
- **`Set.prod s t`** (Cartesian product): produces pairs `(a, b)` rather than values `f a b`; `VTask.image2 f s t` is the image of `Set.prod s t` under the uncurried `f`, not the product itself.
- **`Set.image (Function.uncurry f) (s ×ˢ t)`**: this is mathematically identical to `VTask.image2 f s t`, but is expressed using the uncurried form and the product set — a common alternative spelling, not a different object.