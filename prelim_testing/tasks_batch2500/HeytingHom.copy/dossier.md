## Object

A constructor that produces a new Heyting algebra homomorphism from an existing one by substituting a (definitionally) equal underlying function. The resulting homomorphism carries the new function as its `toFun` field while inheriting all the algebraic properties (preservation of `⊔`, `⊓`, `⊥`, and Heyting implication `⇨`) from the original. Its main purpose is to allow users to present a `HeytingHom` whose underlying function has a preferred definitional form, without having to re-prove any of the homomorphism axioms.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [HeytingAlgebra α] -> [HeytingAlgebra β] -> (f : HeytingHom α β) -> (f' : α → β) -> (h : f' = ⇑f) -> HeytingHom α β
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [HeytingAlgebra α] -> [HeytingAlgebra β] -> (f : HeytingHom α β) -> (f' : α → β) -> (h : f' = ⇑f) -> HeytingHom α β`

The implicit type arguments `α` and `β` are the source and target Heyting algebras, respectively. The instance arguments supply the Heyting algebra structures on each. `f` is the original Heyting algebra homomorphism being copied. `f'` is the new underlying function that the caller wishes to use. `h` is the proof that `f'` is equal (as a function) to the coercion of `f`, ensuring no mathematical content is changed.

## Conventions

There are no junk-value or edge conventions for this definition: it is a total constructor whose inputs are fully constrained by the equality hypothesis `h`, so there are no degenerate or boundary inputs that require special casing.

## Worked examples

- Claim: For any `HeytingHom f`, copying it with the identity substitution yields a homomorphism whose coercion equals the original underlying function.

- Claim: `VTask.copy f (⇑f) rfl` equals `f` as a `HeytingHom`.

- Claim: The coercion of `VTask.copy f f' h` equals `f'` (not just propositionally, but by the `coe_copy` theorem).

- Claim: `VTask.copy f f' h` satisfies `map_sup`, `map_inf`, `map_bot`, and `map_himp` because `f'` equals `⇑f`, so all preservation properties transfer.

## Boundaries

- The hypothesis `h : f' = ⇑f` must be a proof of propositional (not merely definitional) equality of functions; it is given explicitly by the caller.
- If `f' = ⇑f` holds definitionally but not syntactically, the caller must supply an explicit proof term (e.g., `rfl` when the equality is reflexive, or a custom proof otherwise).
- The copy is equal to the original as a `HeytingHom` (`VTask.copy f f' h = f`), so no mathematical information is lost or altered.
- There is no restriction on `α` or `β` beyond carrying a `HeytingAlgebra` instance.

## Not to be confused with

- `HeytingHom.mk` — the raw structure constructor, which requires the caller to provide all field proofs from scratch rather than inheriting them from an existing homomorphism.
- A composition or restriction of `f` — `VTask.copy` does not change the mathematical function, only its syntactic/definitional presentation.
- Lattice homomorphism copy constructors (e.g., for `LatticeHom` or `BoundedLatticeHom`) — those copy analogous structures for weaker algebraic settings, without the Heyting implication field.