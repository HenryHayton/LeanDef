## Object

`VTask.copy` constructs a new relation isomorphism (order-isomorphism between two relations) from an existing one, by replacing its forward function and inverse function with definitionally equal alternatives. The resulting isomorphism is propositionally — and in fact definitionally — equal to the original, but carries `f` and `g` as its underlying functions rather than the coercions of `e` and `e.symm`. This is a bookkeeping tool used to improve definitional equality in downstream proofs or constructions.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_1} -> {β : Type u_2} -> {r : α → α → Prop} -> {s : β → β → Prop} -> (e : r ≃r s) -> (f : α → β) -> (g : β → α) -> (hf : f = ⇑e) -> (hg : g = ⇑e.symm) -> r ≃r s
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {α : Type u_1} -> {β : Type u_2} -> {r : α → α → Prop} -> {s : β → β → Prop} -> (e : r ≃r s) -> (f : α → β) -> (g : β → α) -> (hf : f = ⇑e) -> (hg : g = ⇑e.symm) -> r ≃r s`

The implicit type arguments `α` and `β` are the domain and codomain types. The implicit arguments `r` and `s` are the relations on `α` and `β` respectively. The argument `e` is the existing relation isomorphism being copied. The argument `f` is the new forward function, which is required by `hf` to be equal to the coercion of `e`. The argument `g` is the new inverse function, which is required by `hg` to be equal to the coercion of `e.symm`. The proofs `hf` and `hg` witness that `f` and `g` are propositionally equal to the original forward and inverse maps of `e`.

## Conventions

There are no junk-value or edge-case conventions declared for this definition: it is a total construction on bundled structures with no degenerate inputs, and every input is constrained by the hypotheses `hf` and `hg` to be coherent with an existing isomorphism.

## Worked examples

- Claim: For any relation isomorphism `e : r ≃r s`, applying `VTask.copy` with `f = ⇑e` and `g = ⇑e.symm` (using `rfl` proofs) yields an isomorphism whose coercion to a function equals `f` (i.e., `⇑(e.copy f g hf hg) = f`).

- Claim: For any relation isomorphism `e : r ≃r s`, the result of `VTask.copy e f g hf hg` is propositionally equal to `e` itself (i.e., `e.copy f g hf hg = e`).

- Claim: If `e : r ≃r s` is a relation isomorphism and `f : α → β` satisfies `f = ⇑e`, then `⇑(VTask.copy e f (⇑e.symm) hf rfl) = f`.

## Boundaries

- The inputs `f` and `g` must be propositionally equal to `⇑e` and `⇑e.symm` respectively; this is enforced by the proof arguments `hf` and `hg`. If one passes `rfl` for both, the copy is trivially the same as `e` at every type.
- The copy is always propositionally equal to `e` (as stated by `RelIso.copy_eq`), so no information is lost or gained; the sole purpose is to change the definitional representation of the underlying functions.
- There is no failure mode: as long as `hf` and `hg` are valid proofs, the construction always succeeds and always produces a valid relation isomorphism.

## Not to be confused with

- `Equiv.copy` — an analogous copying operation for plain type equivalences (not equipped with any relation-preservation condition); `VTask.copy` specifically preserves and reproves the `map_rel_iff` condition.
- `RelIso.refl` — the identity relation isomorphism on a single relation; unlike `VTask.copy`, it does not take an existing isomorphism as input and is not a bookkeeping tool.
- `RelIso.trans` — composition of two relation isomorphisms, producing a genuinely new isomorphism rather than a definitional copy of an existing one.