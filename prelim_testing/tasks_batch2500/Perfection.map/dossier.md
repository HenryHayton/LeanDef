## Object

Given a prime `p`, two commutative semirings `R` and `S` both of characteristic `p`, and a ring homomorphism `φ : R →+* S`, `VTask.map p φ` is the induced ring homomorphism between their respective *perfections* — the inverse-limit rings `Perfection R p` and `Perfection S p`. Concretely, the perfection of a ring `R` of characteristic `p` is the inverse system `... → R → R → R` under the Frobenius endomorphism `x ↦ xᵖ`; elements are compatible sequences `(r₀, r₁, r₂, …)` with `rₙ₊₁ᵖ = rₙ`. The induced map applies `φ` componentwise to such sequences, and this is compatible with the Frobenius transition maps because `φ` is a ring homomorphism in characteristic `p`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {R : Type u_1} -> [CommSemiring R] -> (p : ℕ) -> [hp : Fact (Nat.Prime p)] -> [CharP R p] -> {S : Type u₂} -> [CommSemiring S] -> [CharP S p] -> (φ : R →+* S) -> Perfection R p →+* Perfection S p
<!-- PINNED-SIGNATURE:END -->


The first argument `p : ℕ` is the prime characteristic shared by both rings. The instance `hp : Fact (Nat.Prime p)` asserts that `p` is indeed prime. The instances `[CommSemiring R]`, `[CharP R p]`, `[CommSemiring S]`, and `[CharP S p]` equip the two types with their ring structure and the characteristic-`p` constraint. The argument `φ : R →+* S` is the underlying ring homomorphism that is to be lifted to the perfection. The output is a ring homomorphism `Perfection R p →+* Perfection S p`.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is total on all valid inputs satisfying the type-class constraints, and the output is always a well-defined ring homomorphism.

## Worked examples

- Claim: For the identity ring homomorphism `id : R →+* R`, the map `VTask.map p (RingHom.id R)` acts as the identity on `Perfection R p` — namely, for any element `f : Perfection R p` and index `n : ℕ`, the `n`-th coefficient of `VTask.map p (RingHom.id R) f` equals the `n`-th coefficient of `f`.

- Claim: For ring homomorphisms `φ : R →+* S` and `ψ : S →+* T` (all of characteristic `p`), the composite `(VTask.map p ψ).comp (VTask.map p φ)` equals `VTask.map p (ψ.comp φ)` as ring homomorphisms `Perfection R p →+* Perfection T p` — reflecting that the construction is functorial.

- Claim: For any `φ : R →+* S` and any `f : Perfection R p` and `n : ℕ`, the `n`-th coefficient of `VTask.map p φ f` in `S` equals `φ` applied to the `n`-th coefficient of `f` in `R` (compatibility with the coefficient projections).

## Boundaries

- When `φ` is the zero ring homomorphism (if applicable in the semiring setting), `VTask.map p φ` sends every element of `Perfection R p` to the zero element of `Perfection S p`, since zero is applied componentwise.
- The construction is defined for commutative *semirings*, not just rings; no invertibility of `p` or of elements is required.
- If `φ` is an isomorphism, `VTask.map p φ` is also an isomorphism (with inverse `VTask.map p φ.symm`), but `VTask.map` itself only guarantees a ring homomorphism.
- The prime-ness of `p` (enforced by `Fact (Nat.Prime p)`) is essential for the perfection construction to be well-defined; the definition is not meaningful for composite `p`.

## Not to be confused with

- `Perfection.coeff n` — the projection ring homomorphism extracting the `n`-th component from an element of `Perfection R p`, rather than mapping between perfections.
- `PerfectionMap.map` — a more general version that works with arbitrary perfection maps (not necessarily the canonical one), of which `VTask.map` is the special case corresponding to the canonical perfections `of p R` and `of p S`.
- `mapMonoidHom p φ` — the underlying monoid-homomorphism-level construction that `VTask.map` extends to a full ring homomorphism by additionally verifying compatibility with addition and zero.