## 1. Object

`VTask.Map r f g` is the *pushforward* of a heterogeneous binary relation `r : α → β → Prop` along a pair of functions `f : α → γ` and `g : β → δ`. The resulting relation on the codomains holds between two elements `c : γ` and `d : δ` precisely when there exist preimages `a : α` and `b : β` with `r a b`, `f a = c`, and `g b = d`. Intuitively, two output elements are related if the relation witnesses them through some related pair of inputs.

## 2. Signature

```
VTask.Map : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> {δ : Type u_4} -> (r : α → β → Prop) -> (f : α → γ) -> (g : β → δ) -> γ → δ → Prop
```

- `α`, `β`, `γ`, `δ` — implicit universe-polymorphic types; `α` and `β` are the source types of `r`, while `γ` and `δ` are the target types after mapping.
- `r : α → β → Prop` — the base relation being transported.
- `f : α → γ` — the function applied to the left-hand side of `r`.
- `g : β → δ` — the function applied to the right-hand side of `r`.
- Result `γ → δ → Prop` — the pushed-forward relation on the codomains.

## 3. Conventions

There are no junk-value or edge-case conventions declared for this definition: `VTask.Map` is a total, universally-defined construction — it accepts any relation and any pair of functions without restriction, and the existential body always yields a well-formed `Prop`.

## 4. Worked Examples

- Claim: For `r := (· < · : ℕ → ℕ → Prop)`, `f := (· + 1)`, `g := (· + 1)`, we have `VTask.Map r f g 3 5` holds, since `2 < 4`, `2 + 1 = 3`, `4 + 1 = 5`.

- Claim: `VTask.Map (· = · : ℕ → ℕ → Prop) id id` is the equality relation on `ℕ` — two natural numbers are related by the pushforward of equality through identity functions if and only if they are equal.

- Claim: If `r : α → β → Prop` and `f : α → γ`, `g : β → δ` are both injective, then `VTask.Map r f g (f a) (g b) ↔ r a b` for all `a : α`, `b : β`.

- Claim: `VTask.Map` is monotone in its relation argument: if `r ≤ s` (pointwise), then `VTask.Map r f g ≤ VTask.Map s f g` for any functions `f` and `g`.

## 5. Boundaries

- **Empty relation**: If `r` is the empty relation (always `False`), then `VTask.Map r f g` is also the empty relation, since no witness `a`, `b` with `r a b` can exist.
- **Full relation**: If `r` is the full relation (always `True`) and `f`, `g` are surjective, then `VTask.Map r f g` is the full relation on the codomains.
- **Non-surjective functions**: If `f` is not surjective, there exist elements `c : γ` outside the image of `f` such that `VTask.Map r f g c d` is `False` for every `d`, regardless of `r`.
- **Non-injective functions**: If `f` is not injective, the pushed-forward relation can merge distinct source elements: `VTask.Map r f g c d` can be witnessed by multiple distinct pairs `(a, b)`.
- **Composition**: Mapping a relation through composed functions `(h ∘ f)` and `(k ∘ g)` equals first mapping through `f`, `g` and then mapping through `h`, `k` — the construction is compatible with function composition.

## 6. Not to Be Confused With

- `Relation.map` (a different naming or namespace variant in some contexts) — refers to the same mathematical idea but may appear under a different namespace or with slightly different universe assumptions.
- `Function.onFun r f` (also written `r on f`) — this *pulls back* a relation along a single function to the domain, rather than pushing it forward to the codomain; `VTask.Map (r on f) f f` and `r on f` are related but distinct.
- `Setoid.map` — a construction that maps a setoid (reflexive, symmetric, transitive relation) along a function at the level of setoids, producing a setoid on the codomain; it is related but carries additional algebraic structure and is defined only for endorelations.