## VTask.map

### Object

`VTask.map f` is the order isomorphism between the poset of upper sets of `α` and the poset of upper sets of `β` that is canonically induced by an order isomorphism `f : α ≃o β`. Concretely, an upper set `s ⊆ α` is sent to its direct image `f(s) ⊆ β`, which is again an upper set because `f` preserves and reflects the order; the inverse sends `t ⊆ β` to its preimage `f⁻¹(t) ⊆ α`. The construction is entirely functorial: it respects composition, identities, and inversion of order isomorphisms, and it is itself an order isomorphism with respect to the inclusion ordering on upper sets.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {α : Type u_1} -> {β : Type u_2} -> [Preorder α] -> [Preorder β] -> (f : α ≃o β) -> UpperSet α ≃o UpperSet β
<!-- PINNED-SIGNATURE:END -->


VTask.map : {α : Type u_1} -> {β : Type u_2} -> [Preorder α] -> [Preorder β] -> (f : α ≃o β) -> UpperSet α ≃o UpperSet β

`α` and `β` are the source and target types, each equipped with a preorder. The explicit argument `f` is the order isomorphism between `α` and `β` whose action on elements is lifted pointwise to an order isomorphism on upper sets.

### Conventions

No junk-value conventions are declared for this definition: it is a total function on a fully constrained input (an order isomorphism), and every output is a genuine, well-formed order isomorphism of upper sets with no edge-case degeneracy.

### Worked examples

- Claim: For any order isomorphism `f : α ≃o β` and any upper set `s : UpperSet α`, an element `b : β` belongs to `VTask.map f s` if and only if `f.symm b` belongs to `s`.

- Claim: `VTask.map (OrderIso.refl α)` is the identity order isomorphism on `UpperSet α`; i.e., `VTask.map (OrderIso.refl α) = OrderIso.refl _`.

- Claim: Mapping is functorial under composition: for order isomorphisms `f : α ≃o β` and `g : β ≃o γ`, and an upper set `s : UpperSet α`, we have `VTask.map g (VTask.map f s) = VTask.map (f.trans g) s`.

- Claim: The inverse of `VTask.map f` is `VTask.map f.symm`; i.e., `(VTask.map f).symm = VTask.map f.symm`.

- Claim: For `f : α ≃o β` and `a : α`, the principal upper set `Ici a` in `α` maps to `Ici (f a)` in `β`: `VTask.map f (Ici a) = Ici (f a)`.

- Claim: For `f : α ≃o β` and `a : α`, the strict principal upper set `Ioi a` maps to `Ioi (f a)`: `VTask.map f (Ioi a) = Ioi (f a)`.

### Boundaries

- When `f` is the identity isomorphism `OrderIso.refl α`, `VTask.map f` is the identity isomorphism on `UpperSet α`.
- When `f` is the composition `f.trans g`, the map satisfies `VTask.map (f.trans g) = (VTask.map g) ∘ (VTask.map f)` as order isomorphisms (functoriality).
- The complement interaction: the complement of the image of an upper set `s` as a lower set equals `LowerSet.map f (s.compl)`, linking the upper-set and lower-set map constructions.
- Since `f` is an order isomorphism (in particular a bijection), the direct-image and preimage operations are exact inverses of each other on the set level, so no information is lost or gained.
- The underlying set of `VTask.map f s` is exactly the direct image `f '' s` (not merely some upper closure thereof); this is possible because `f` is an order isomorphism.

### Not to be confused with

- `LowerSet.map f`: the analogous construction for **lower** sets induced by `f`; note the docstring for `VTask.map` mistakenly says "lower sets" but the object is about upper sets.
- `upperClosure (f '' s)`: the upper closure of the image of an arbitrary set `s`; this coincides with `VTask.map f (upperClosure s)` but is a different starting point (arbitrary set, not an upper set).
- `OrderIso.setCongr` or set-level image maps: `VTask.map f` is order-isomorphism-valued and lives in the world of upper sets as a lattice, not merely a set-level image map.