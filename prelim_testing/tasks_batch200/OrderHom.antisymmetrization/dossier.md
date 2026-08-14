## Object

Given a monotone map (order homomorphism) `f : α →o β` between two preordered types, `VTask.antisymmetrization f` is the induced order homomorphism between the corresponding antisymmetrizations. The antisymmetrization of a preorder is the partial order obtained by identifying elements that are mutually ≤ — it is the quotient by the equivalence relation `x ~ y ↔ x ≤ y ∧ y ≤ x`. Because `f` is monotone, it respects this equivalence relation and therefore descends to a well-defined monotone map on the quotients. This construction witnesses that antisymmetrization is functorial on the category of preorders and monotone maps.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.antisymmetrization : {α : Type u_1} -> {β : Type u_2} -> [Preorder α] -> [Preorder β] -> (f : α →o β) -> (Antisymmetrization α fun x1 x2 => x1 ≤ x2) →o Antisymmetrization β fun x1 x2 => x1 ≤ x2
<!-- PINNED-SIGNATURE:END -->


`VTask.antisymmetrization : {α : Type u_1} -> {β : Type u_2} -> [Preorder α] -> [Preorder β] -> (f : α →o β) -> (Antisymmetrization α fun x1 x2 => x1 ≤ x2) →o Antisymmetrization β fun x1 x2 => x1 ≤ x2`

The implicit type arguments `α` and `β` are the source and target preordered types, respectively. The typeclass arguments supply the preorder structures on each. The explicit argument `f` is the order homomorphism (monotone map) from `α` to `β` whose action is to be lifted to the antisymmetrization quotients.

## Conventions

There are no junk-value or boundary conventions to declare: the function is total and well-typed for any order homomorphism between any two preordered types; no special-case output is assigned to degenerate inputs.

## Worked examples

- Claim: For any order homomorphism `f : α →o β` and any element `a : α`, the image of the equivalence class of `a` under `VTask.antisymmetrization f` is the equivalence class of `f a`. That is, `VTask.antisymmetrization f (toAntisymmetrization _ a) = toAntisymmetrization _ (f a)`.

- Claim: The construction `VTask.antisymmetrization` is compatible with composition: for order homomorphisms `f : α →o β` and `g : β →o γ`, the induced map `VTask.antisymmetrization (g.comp f)` equals `(VTask.antisymmetrization g).comp (VTask.antisymmetrization f)` as order homomorphisms on the antisymmetrization quotients.

- Claim: When `f` is the identity order homomorphism on `α`, `VTask.antisymmetrization f` is the identity order homomorphism on `Antisymmetrization α (· ≤ ·)`.

## Boundaries

- When `α` is already a partial order, the antisymmetrization quotient `Antisymmetrization α (· ≤ ·)` is order-isomorphic to `α` itself (no two distinct elements are identified), and `VTask.antisymmetrization f` behaves essentially the same as `f` under this identification.
- When `α` or `β` has a trivial preorder (all elements mutually ≤), the antisymmetrization quotient collapses to a single element, and `VTask.antisymmetrization f` is correspondingly trivial regardless of what `f` does.
- The map acts on equivalence classes (not on bare elements of `α` or `β`), so its values are always equivalence classes in `Antisymmetrization β (· ≤ ·)`.

## Not to be confused with

- `toAntisymmetrization`: the canonical map sending an element `a : α` to its equivalence class in `Antisymmetrization α (· ≤ ·)`; this is the unit of the functor, not the action on morphisms.
- `Antisymmetrization` (the type): the quotient type itself, whereas `VTask.antisymmetrization` is the functorial action lifting a morphism to that type.
- `OrderIso.antisymmetrization`: a related construction that lifts an order *isomorphism* (rather than just a homomorphism) to an isomorphism of antisymmetrizations.