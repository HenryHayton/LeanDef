## Object

`VTask.copy` constructs a new Esakia homomorphism from an existing one by replacing its underlying function with a provably equal alternative. The resulting morphism is definitionally equal to the original at the level of functions, while the new carrier function is used as the observable coercion. This is a standard "copy with new definitional identity" device used to repair or adjust definitional equalities in a proof assistant context.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [TopologicalSpace α] -> [Preorder α] -> [TopologicalSpace β] -> [Preorder β] -> (f : EsakiaHom α β) -> (f' : α → β) -> (h : f' = ⇑f) -> EsakiaHom α β
<!-- PINNED-SIGNATURE:END -->


The first two type-level arguments fix the source type `α` and target type `β`, each equipped with a topology (the `TopologicalSpace` instances) and a partial order (the `Preorder` instances) — these are the structures required to speak about Esakia homomorphisms between them. The argument `f` is the original Esakia homomorphism being copied. The argument `f'` is the new underlying function that will serve as the coercion of the result. The argument `h` is the proof that `f'` is pointwise equal to the coercion of `f`, ensuring that no mathematical content is changed.

## Conventions

The operation is total and imposes no junk-value or edge-case conventions; it is defined for every valid combination of inputs satisfying the equality proof `h`.

## Worked examples

- Claim: For any Esakia homomorphism `f`, calling `VTask.copy f (⇑f) rfl` yields a morphism whose coercion equals `⇑f`.

- Claim: For any Esakia homomorphism `f`, `VTask.copy f (⇑f) rfl` is equal to `f` as an Esakia homomorphism (i.e., `copy_eq` holds: the copy and the original are the same morphism).

- Claim: The coercion of `VTask.copy f f' h` equals `f'` (i.e., `coe_copy` holds: the supplied function is exactly what gets coerced).

## Boundaries

- The only admissible value of `h` is a proof that `f' = ⇑f`; the definition is total over all such triples `(f, f', h)`.
- When `f' = ⇑f` by `rfl`, the copy is trivially the same morphism as `f` with the same coercion, making the operation idempotent in the strongest sense.
- The operation does not change any of the topological or order-theoretic content of `f`; it purely adjusts the syntactic identity of the underlying function.

## Not to be confused with

- `ContinuousOrderHom.copy`: the analogous copy operation for continuous order homomorphisms (not Esakia homomorphisms); `VTask.copy` additionally preserves the Esakia open-map condition.
- Constructing an entirely new `EsakiaHom` via its constructor: that requires re-verifying all axioms, whereas `VTask.copy` inherits them from the original `f`.
- Function extensionality (`funext`): that proves two functions are equal given pointwise equality, while `VTask.copy` packages a pointwise-equal function into a new morphism record without any propositional rewriting.