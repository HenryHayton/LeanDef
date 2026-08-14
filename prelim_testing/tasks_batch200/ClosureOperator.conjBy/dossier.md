## VTask.conjBy

### Object

Given a closure operator `c` on a preordered set `α` and an order-isomorphism `e : α ≃o β`, `VTask.conjBy c e` is the closure operator on `β` defined by conjugating `c` by `e`: it sends each element `b : β` to `e(c(e⁻¹(b)))`. In other words, it is the composite `e ∘ c ∘ e⁻¹`, which is the canonical way to "transport" a closure operator along an order-isomorphism.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.conjBy : {α : Type u_4} -> {β : Type u_5} -> [Preorder α] -> [Preorder β] -> (c : ClosureOperator α) -> (e : α ≃o β) -> ClosureOperator β
<!-- PINNED-SIGNATURE:END -->


The first argument `c` is the closure operator on the source preorder `α` being transported. The second argument `e` is the order-isomorphism from `α` to the target preorder `β`; it determines how elements of `β` are pulled back to `α` for the closure computation and then pushed forward again.

### Conventions

No junk-value or edge conventions are declared: the operation is total and well-defined for any closure operator and any order-isomorphism between preorders.

### Worked examples

- Claim: Conjugating a closure operator by the identity isomorphism returns the original closure operator (`conjBy_refl`): for any `c : ClosureOperator α`, `VTask.conjBy c (OrderIso.refl α) = c`.

- Claim: Conjugation is functorial with respect to composition of order-isomorphisms (`conjBy_trans`): for isomorphisms `e₁ : α ≃o β` and `e₂ : β ≃o γ` and closure operator `c` on `α`, `VTask.conjBy c (e₁.trans e₂) = VTask.conjBy (VTask.conjBy c e₁) e₂`.

- Claim: If `b : β` is closed under `c` (i.e., `c(e⁻¹ b) = e⁻¹ b`), then `b` is closed under `VTask.conjBy c e` (i.e., the transported closure operator maps `b` to itself).

- Claim: For any `b : β`, the transported closure operator satisfies the inflation property: `b ≤ (VTask.conjBy c e) b`, mirroring the inflation axiom `x ≤ c(x)` of `c`.

### Boundaries

- When `e` is the identity isomorphism `OrderIso.refl α`, the result equals the original closure operator `c` exactly.
- When `e₁` and `e₂` are two isomorphisms that can be composed, conjugating first by `e₁` then by `e₂` gives the same result as conjugating once by `e₁.trans e₂`; this captures the functoriality of the conjugation construction.
- The construction is defined for arbitrary preorders; no lattice or complete-lattice structure is needed.
- If `c` is the identity closure operator (the one satisfying `c x = x` for all `x`), then `VTask.conjBy c e` is also the identity closure operator on `β`.

### Not to be confused with

- `ClosureOperator.closure`: the underlying function of a closure operator, which just applies the closure map without any transport along an isomorphism.
- `OrderIso.conj`: the raw function-level conjugation `e ∘ f ∘ e⁻¹` for a function `f`, without packaging the result as a `ClosureOperator`.
- `GaloisConnection.conjugate` / transfer of Galois connections: a related but distinct notion of transporting adjoint pairs along isomorphisms, not the same as transporting a single closure operator.
