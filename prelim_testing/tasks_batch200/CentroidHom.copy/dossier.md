## Object

`VTask.copy` produces a new centroid homomorphism that is definitionally equal to a given one, but whose underlying function is explicitly recorded as a specified function `f'`. The result is a `CentroidHom` whose coercion to a bare function is exactly `f'`, while carrying the same algebraic properties as the original homomorphism `f`. The purpose is purely technical: it allows one to replace the underlying function of a centroid homomorphism with a provably equal one, which can resolve definitional-equality mismatches that arise in formal proofs.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_5} -> [NonUnitalNonAssocSemiring α] -> (f : CentroidHom α) -> (f' : α → α) -> (h : f' = ⇑f) -> CentroidHom α
<!-- PINNED-SIGNATURE:END -->


The first argument `f` is the original centroid homomorphism being copied. The second argument `f'` is the new underlying function that will be recorded as the coercion of the resulting homomorphism. The third argument `h` is a proof that `f'` is pointwise equal (in fact, judgementally equal as functions) to the coercion of `f`; this proof is what guarantees the copy carries valid centroid-homomorphism structure.

## Conventions

There are no junk-value or edge-case conventions declared for this definition: it is a total constructor whose inputs are fully constrained by the proof argument `h`, so no distinguished boundary behaviour needs to be recorded.

## Worked examples

- Claim: For any `CentroidHom α`, the coercion of `VTask.copy f (⇑f) rfl` equals `⇑f`.

- Claim: For any `CentroidHom α`, `VTask.copy f (⇑f) rfl` is equal to `f` as a `CentroidHom α` (i.e., `copy_eq` holds: the copy is the same homomorphism).

- Claim: For a centroid homomorphism `f : CentroidHom ℤ`, taking `f' := (⇑f : ℤ → ℤ)` and `h := rfl`, the coercion of `VTask.copy f f' h` equals `f'`.

## Boundaries

- The proof obligation `h : f' = ⇑f` completely determines the relationship between `f'` and `f`; there is no version of this constructor that accepts an unrelated function.
- When `f' = ⇑f` definitionally (e.g., `h = rfl`), the resulting homomorphism is definitionally equal to `f` in every component, not just propositionally.
- The copy operation is trivially idempotent: copying a copy with the same function again returns a homomorphism propositionally equal to the original.

## Not to be confused with

- `CentroidHom.mk` (or the anonymous constructor `{ ... }`): builds a centroid homomorphism from scratch by supplying all fields, rather than replacing the function of an existing one.
- Function extensionality / `funext`: a proof technique showing two functions are equal, whereas `VTask.copy` is a constructor that embeds such an equality into the homomorphism structure itself.
- `AddMonoidHom.copy`: the analogous operation for additive monoid homomorphisms; `VTask.copy` extends this by additionally preserving the left- and right-multiplication compatibility required of centroid homomorphisms.