## Object

Given a non-unital star algebra homomorphism `f : A →⋆ₙₐ[R] B`, `VTask.copy` produces a new non-unital star algebra homomorphism whose underlying function is a prescribed function `f'`, subject to the proof that `f'` equals the coercion of `f` to a bare function. The result is extensionally identical to `f` but carries `f'` as its definitional underlying function. This is a utility constructor whose sole purpose is to replace the underlying function with a definitionally equal one, which can resolve definitional equality issues in proofs.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> [Monoid R] -> [NonUnitalNonAssocSemiring A] -> [DistribMulAction R A] -> [Star A] -> [NonUnitalNonAssocSemiring B] -> [DistribMulAction R B] -> [Star B] -> (f : A →⋆ₙₐ[R] B) -> (f' : A → B) -> (h : f' = ⇑f) -> A →⋆ₙₐ[R] B
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {R : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> [Monoid R] -> [NonUnitalNonAssocSemiring A] -> [DistribMulAction R A] -> [Star A] -> [NonUnitalNonAssocSemiring B] -> [DistribMulAction R B] -> [Star B] -> (f : A →⋆ₙₐ[R] B) -> (f' : A → B) -> (h : f' = ⇑f) -> A →⋆ₙₐ[R] B`

The implicit type arguments `R`, `A`, and `B` are the scalar type and the source and target algebras, respectively. The typeclass arguments supply the algebraic structure: `R` is a monoid acting on both `A` and `B` via `DistribMulAction`, while `A` and `B` are non-unital non-associative semirings each equipped with a star involution. The argument `f` is the original non-unital star algebra homomorphism being copied. The argument `f'` is the new underlying bare function that will be installed. The argument `h` is a proof that `f'` equals the coercion of `f` to a function, ensuring the two are equal as functions.

## Conventions

There are no junk-value or edge-case conventions for this definition: it is a total constructor over all well-typed inputs satisfying the equality constraint `h`, and no special behaviour is assigned to any degenerate configuration.

## Worked examples

- Claim: The coercion of `VTask.copy f f' h` to a bare function equals `f'` (i.e., `⇑(f.copy f' h) = f'`).

- Claim: The result of `VTask.copy f f' h` is propositionally equal to `f` as a non-unital star algebra homomorphism (i.e., `f.copy f' h = f`).

- Claim: For any element `a : A`, evaluating `(f.copy f' h) a` gives the same value as `f' a`, because the underlying function of the copy is definitionally `f'`.

- Claim: `VTask.copy f (⇑f) rfl` produces a morphism equal to `f`, since supplying `f'` as the coercion of `f` itself and `rfl` as the proof is always valid.

## Boundaries

- The only admissible inputs are those where `h : f' = ⇑f`; in particular `f'` must be propositionally (not merely pointwise) equal to the coercion of `f`. Pointwise equality alone is insufficient.
- The most degenerate valid call is `f.copy (⇑f) rfl`, which yields a copy whose underlying function is unchanged at every level; the result is propositionally equal to `f`.
- When `f'` is syntactically identical to `⇑f`, the copy differs from `f` only in how the underlying function field is recorded, not in any observable mathematical behaviour.
- All structural properties of the homomorphism — preservation of addition, multiplication, scalar multiplication, zero, and the star involution — are inherited from `f` via the equality `h`.

## Not to be confused with

- `NonUnitalAlgHom.copy`: the analogous copy constructor for non-unital algebra homomorphisms *without* a star structure; it does not track or preserve the star involution.
- `StarAlgHom.copy`: the copy constructor for *unital* star algebra homomorphisms, which additionally requires the morphism to preserve the multiplicative identity.
- The identity morphism on `A`: that is a specific non-unital star algebra homomorphism from `A` to itself, not a general mechanism for replacing the underlying function of an arbitrary morphism.