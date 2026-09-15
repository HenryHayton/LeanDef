## VTask.restrict

### Object

`VTask.restrict p f` is the restriction of a (possibly dependent) function `f : (x : α) → β x` to the subtype `{x : α // p x}`. Given a predicate `p` on `α` and a function `f` defined on all of `α`, it produces a new function whose domain is only those elements of `α` satisfying `p`, yielding the same values as `f` on those elements.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restrict : {α : Sort u_5} -> {β : α → Type u_4} -> (p : α → Prop) -> (f : (x : α) → β x) -> (x : Subtype p) -> β ↑x
<!-- PINNED-SIGNATURE:END -->


`VTask.restrict : {α : Sort u_5} -> {β : α → Type u_4} -> (p : α → Prop) -> (f : (x : α) → β x) -> (x : Subtype p) -> β ↑x`

The implicit argument `α` is the ambient type. The implicit argument `β` is a type family over `α` giving the codomain of each fibre, allowing the function to be dependent. The argument `p` is the predicate defining which elements of `α` are in the subdomain; the restricted function is only defined on elements satisfying `p`. The argument `f` is the original dependent function defined on all of `α`. The argument `x` is an element of the subtype, i.e., a pair of an element of `α` together with a proof that it satisfies `p`; the result is the value of `f` at the underlying element `x.1`.

### Conventions

There are no junk-value or edge conventions declared: the function is total and well-defined for every choice of `p`, `f`, and `x`; no special junk values arise.

### Worked examples

- Claim: Restricting the squaring function on `ℕ` to the subtype of even naturals at the element `⟨4, h⟩` gives `16`.

- Claim: `VTask.restrict (fun n : ℕ => n % 2 = 0) (fun n => n * n) ⟨4, by decide⟩ = 16`
  ```lean
  example : VTask.restrict (fun n : ℕ => n % 2 = 0) (fun n => n * n) ⟨4, by decide⟩ = 16 := by decide
  ```

- Claim: Restricting the identity function on `ℕ` to `{n // n < 5}` at `⟨3, h⟩` returns `3`.
  ```lean
  example : VTask.restrict (fun n : ℕ => n < 5) id ⟨3, by decide⟩ = 3 := by decide
  ```

- Claim: For any `f : (x : α) → β x`, any predicate `p`, and any `x : Subtype p`, `VTask.restrict p f x = f x.1`.

### Boundaries

- When `p` is the always-true predicate (`fun _ => True`), the subtype is essentially all of `α`, and the restriction coincides with `f` itself on every element.
- When `p` is the always-false predicate (`fun _ => False`), the subtype is empty (`IsEmpty`), so the restricted function has an empty domain; it is vacuously defined and can never be applied.
- The restriction operator `fun f => VTask.restrict p f` is surjective (when each fibre `β a` is nonempty) and inherits injectivity from `f`: if `f` is injective on `α`, then `VTask.restrict p f` is injective on the subtype.
- For a non-dependent function `f : α → β`, the restriction equals the composition of `f` with the subtype inclusion `Subtype.val`.

### Not to be confused with

- `Set.restrict`: the version where the domain restriction is described by a `Set` rather than a `Subtype` predicate; morally the same concept but with a different syntactic packaging.
- `Function.comp`: plain composition of functions, which does not carry a proof of predicate membership in the input type.
- `Subtype.val` (the coercion `↑x`): this merely extracts the underlying element from a subtype value; it does not apply a function to it.