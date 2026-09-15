## VTask.ofSubalgebras

### Object

Given a Lie algebra isomorphism `e : L₁ ≃ₗ⁅R⁆ L₂` between two Lie algebras over a commutative ring `R`, and a Lie subalgebra `L₁'` of `L₁` whose image under `e` equals a prescribed Lie subalgebra `L₂'` of `L₂`, this construction produces a Lie algebra isomorphism `L₁' ≃ₗ⁅R⁆ L₂'` between the two subalgebras themselves — i.e., it restricts the ambient isomorphism to an isomorphism of the subalgebras.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofSubalgebras : {R : Type u} -> {L₁ : Type v} -> {L₂ : Type w} -> [CommRing R] -> [LieRing L₁] -> [LieRing L₂] -> [LieAlgebra R L₁] -> [LieAlgebra R L₂] -> (L₁' : LieSubalgebra R L₁) -> (L₂' : LieSubalgebra R L₂) -> (e : L₁ ≃ₗ⁅R⁆ L₂) -> (h : LieSubalgebra.map e.toLieHom L₁' = L₂') -> ↥L₁' ≃ₗ⁅R⁆ ↥L₂'
<!-- PINNED-SIGNATURE:END -->


VTask.ofSubalgebras : {R : Type u} -> {L₁ : Type v} -> {L₂ : Type w} -> [CommRing R] -> [LieRing L₁] -> [LieRing L₂] -> [LieAlgebra R L₁] -> [LieAlgebra R L₂] -> (L₁' : LieSubalgebra R L₁) -> (L₂' : LieSubalgebra R L₂) -> (e : L₁ ≃ₗ⁅R⁆ L₂) -> (h : LieSubalgebra.map e.toLieHom L₁' = L₂') -> ↥L₁' ≃ₗ⁅R⁆ ↥L₂'

`R` is the commutative ring of scalars over which the Lie algebras are defined. `L₁` and `L₂` are the ambient Lie algebras. The instance arguments supply the commutative ring structure on `R` and the Lie algebra structures on `L₁` and `L₂`. The explicit argument `L₁'` is a Lie subalgebra of `L₁` — the domain subalgebra to be restricted to. The explicit argument `L₂'` is a Lie subalgebra of `L₂` — the target subalgebra into which the restriction must map. The argument `e` is the ambient Lie algebra isomorphism from `L₁` to `L₂` whose restriction is sought. The argument `h` is a proof that the image of `L₁'` under the Lie homomorphism underlying `e` is exactly `L₂'`, which is the compatibility condition that makes the restriction well-defined as a map onto `L₂'`.

### Conventions

There are no junk-value or out-of-domain conventions to declare: the definition is well-typed whenever the hypothesis `h` is supplied, and `h` itself encodes the only non-trivial precondition (equality of the image with `L₂'`). Every input satisfying the type signature produces a valid Lie algebra isomorphism.

### Worked examples

- Claim: If `e` is the identity isomorphism on a Lie algebra `L` and `L'` is any Lie subalgebra, then `VTask.ofSubalgebras L' L' (LieEquiv.refl R L) (by simp)` is an isomorphism from `L'` to itself.

- Claim: For any Lie algebra isomorphism `e : L₁ ≃ₗ⁅R⁆ L₂`, the underlying function of `VTask.ofSubalgebras L₁' L₂' e h` sends an element `x : ↥L₁'` to the element `e x` viewed in `↥L₂'`.

- Claim: The inverse of `VTask.ofSubalgebras L₁' L₂' e h` equals `VTask.ofSubalgebras L₂' L₁' e.symm (by rw [← h]; simp [LieSubalgebra.map_comp])` — that is, the restriction of the inverse isomorphism is the inverse of the restriction.

### Boundaries

- The hypothesis `h` must hold definitionally or propositionally; the definition does not attempt to choose a canonical target subalgebra automatically — `L₂'` must be specified and shown equal to the image.
- If `L₁'` is the top subalgebra (the whole of `L₁`) and `L₂'` is the top subalgebra (the whole of `L₂`), the restriction recovers an isomorphism equivalent to `e` itself (up to the canonical identifications of the tops with the ambient algebras).
- If `L₁'` is the trivial (zero) subalgebra, then `L₂'` must also be the trivial subalgebra, and the result is the unique isomorphism between two zero Lie algebras.
- The equality condition `h` is an equality of subalgebras (as sets-with-structure), not merely containment, so the result is genuinely an isomorphism `L₁' ≃ₗ⁅R⁆ L₂'`, not just an injective morphism.

### Not to be confused with

- `LieEquiv.lieSubalgebraEquivOfEq`: a variant that produces an equivalence between two subalgebras of the *same* ambient Lie algebra that happen to be propositionally equal, rather than relating subalgebras of two different Lie algebras via an ambient isomorphism.
- `LieHom.restrict` or similar: a plain Lie *homomorphism* obtained by restricting a homomorphism (not necessarily invertible) to a subalgebra; `VTask.ofSubalgebras` specifically yields an *isomorphism*.
- `LinearEquiv.ofSubmodules`: the purely linear (module) version of the same construction, which does not preserve or reference the Lie bracket.