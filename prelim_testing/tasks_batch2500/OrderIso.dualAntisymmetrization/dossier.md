## VTask.dualAntisymmetrization

### Object

An order isomorphism witnessing that two constructions on a preordered type commute: taking the antisymmetrization (i.e., quotienting out mutual comparability to obtain a partial order) and then passing to the order dual gives the same partial order as first passing to the order dual and then taking the antisymmetrization. More precisely, it is a canonical order-isomorphism

`(Antisymmetrization α (· ≤ ·))ᵒᵈ ≃o Antisymmetrization αᵒᵈ (· ≤ ·)`

showing that these two operations on preorders commute up to canonical isomorphism.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dualAntisymmetrization : (α : Type u_1) -> [Preorder α] -> (Antisymmetrization α fun x1 x2 => x1 ≤ x2)ᵒᵈ ≃o Antisymmetrization αᵒᵈ fun x1 x2 => x1 ≤ x2
<!-- PINNED-SIGNATURE:END -->


`VTask.dualAntisymmetrization : (α : Type u_1) -> [Preorder α] -> (Antisymmetrization α fun x1 x2 => x1 ≤ x2)ᵒᵈ ≃o Antisymmetrization αᵒᵈ fun x1 x2 => x1 ≤ x2`

The first argument `α` is the carrier type of the preorder whose antisymmetrization and dual are being compared. The instance argument `[Preorder α]` equips `α` with the preorder structure — the `≤` relation — from which both the dual and the antisymmetrization are built.

### Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total construction applicable to any type `α` equipped with any `Preorder` instance, and it produces a well-defined order isomorphism in all cases without any special boundary behaviour.

### Worked examples

- Claim: On the preordered type `ℕ`, the forward map sends the dual of `toAntisymmetrization (· ≤ ·) n` to `toAntisymmetrization (· ≤ ·) (toDual n)` for any `n : ℕ`.

- Claim: On the preordered type `ℕ`, the inverse map sends `toAntisymmetrization (· ≤ ·) (toDual n)` back to `toDual (toAntisymmetrization (· ≤ ·) n)` for any `n : ℕ`, confirming the round-trip.

- Claim: `VTask.dualAntisymmetrization ℕ` is an order isomorphism, i.e., `a ≤ b ↔ VTask.dualAntisymmetrization ℕ a ≤ VTask.dualAntisymmetrization ℕ b` for all `a b : (Antisymmetrization ℕ (· ≤ ·))ᵒᵈ`.

- Claim: The composite of `VTask.dualAntisymmetrization α` with its own inverse is the identity, i.e., `(VTask.dualAntisymmetrization α).symm.trans (VTask.dualAntisymmetrization α) = OrderIso.refl _` (up to definitional equality).

### Boundaries

- When `α` itself is already a partial order (antisymmetric), the antisymmetrization is isomorphic to `α`, but `VTask.dualAntisymmetrization` still applies and produces the canonical isomorphism between the two "dual-of-antisymmetrization" and "antisymmetrization-of-dual" descriptions.
- When `α` has a trivial preorder (all elements are equivalent under mutual comparability), all of `Antisymmetrization α`, `(Antisymmetrization α)ᵒᵈ`, and `Antisymmetrization αᵒᵈ` consist of a single equivalence class, and the isomorphism is trivially the unique map between singletons.
- The isomorphism is natural in `α`: it commutes with preorder-preserving maps in the appropriate categorical sense.

### Not to be confused with

- `Antisymmetrization α (· ≤ ·)`: the underlying quotient type (without the dual), not the isomorphism studied here.
- `OrderIso.dualDual α`: the canonical isomorphism `αᵒᵈᵒᵈ ≃o α` witnessing that taking the dual twice returns the original order; that is a self-inverse on the dual operation alone, not involving antisymmetrization.
- `toDual`/`ofDual`: the equivalence functions that flip the order relation on a fixed type, which are ingredients used inside `VTask.dualAntisymmetrization` but are not themselves isomorphisms between antisymmetrization constructions.