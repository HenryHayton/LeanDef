## Object

`VTask.map` is the *restriction* of a function between ambient types to a function between subtypes. Given a function `f : α → β` and a proof that `f` maps every element satisfying predicate `p` to an element satisfying predicate `q`, it produces the induced function from the subtype `{a : α // p a}` to the subtype `{b : β // q b}`, carrying both the mapped value and the transported membership proof.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {α : Sort u_1} -> {β : Sort u_2} -> {p : α → Prop} -> {q : β → Prop} -> (f : α → β) -> (h : ∀ (a : α), p a → q (f a)) -> Subtype p → Subtype q
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {α : Sort u_1} -> {β : Sort u_2} -> {p : α → Prop} -> {q : β → Prop} -> (f : α → β) -> (h : ∀ (a : α), p a → q (f a)) -> Subtype p → Subtype q`

- `α` and `β` are the ambient sorts from which the subtypes are carved.
- `p` is the predicate defining the domain subtype; elements of `Subtype p` are pairs of a value in `α` and a proof that it satisfies `p`.
- `q` is the predicate defining the codomain subtype; elements of `Subtype q` are pairs of a value in `β` and a proof that it satisfies `q`.
- `f` is the underlying function from `α` to `β` that we wish to restrict.
- `h` is the compatibility proof: for every element `a` of `α`, if `a` satisfies `p` then `f a` satisfies `q`. This is the essential evidence needed to promote `f` to a map between the subtypes.
- The final argument is an element of `Subtype p` (a value in `α` paired with its membership proof), and the result is the corresponding element of `Subtype q`.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total function whose inputs are always fully specified (a function and a compatibility proof), so there are no boundary inputs requiring an arbitrary or conventional choice.

## Worked examples

- Claim: Applying `VTask.map` with the squaring function `f n = n * n` and the compatibility proof that `0 < n → 0 < n * n` sends `⟨3, by norm_num⟩ : {n : ℕ // 0 < n}` to `⟨9, by norm_num⟩ : {n : ℕ // 0 < n}`.

- Claim: When `f = id` and `h` witnesses that `p a → p (id a)`, `VTask.map id h` is the identity function on `Subtype p`, i.e., `VTask.map id h x = x` for all `x`.

- Claim: `VTask.map` is functorial: applying `VTask.map f hfg` after `VTask.map g hgh` equals applying `VTask.map (f ∘ g)` with the composed compatibility proof, i.e., `VTask.map f hfg ∘ VTask.map g hgh = VTask.map (f ∘ g) (fun a ha => hfg _ (hgh a ha))`.

- Claim: If `f : α → β` is injective on all of `α`, then `VTask.map f h` is injective as a function on subtypes.

## Boundaries

- When `p` or `q` is the predicate `fun _ => True`, the corresponding subtype is in bijection with the ambient type itself; `VTask.map f h` in this case behaves like `f` with trivial proof bookkeeping.
- When `p` or `q` is the predicate `fun _ => False`, the domain or codomain subtype is empty; `VTask.map f h` is vacuously well-defined (there are no elements to map or receive).
- The function `h` need not be constructive in any computational sense; it only needs to produce a proof, so `VTask.map` works in full generality for propositions that may not be decidable.
- The sorts `α` and `β` are `Sort u_1` and `Sort u_2`, so `VTask.map` applies uniformly to types and propositions, not just `Type`-valued universes.

## Not to be confused with

- `Subtype.val` (or the coercion `↑`): extracts the underlying value from a subtype element, discarding the proof; it is not a map between subtypes.
- `Set.MapsTo`: a proposition asserting that a function sends a set into another set; related to the hypothesis `h` but not itself a function on subtypes.
- `Set.inclusion`: the canonical map between subtypes induced by a subset relation `s ⊆ t`, which is the special case `VTask.map id h` for the identity function.
