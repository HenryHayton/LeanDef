## Object

Given a continuous `R`-algebra homomorphism `f : A →A[R] B` and a bare function `f' : A → B` that is definitionally (or provably) equal to the underlying function of `f`, `VTask.copy` produces a new continuous `R`-algebra homomorphism whose underlying function is literally `f'` rather than `⇑f`. The resulting morphism is equal to `f` as a continuous algebra homomorphism, but its coercion to a bare function is `f'`, not `⇑f`. This is a bookkeeping tool used to repair or establish definitional equalities in proofs and constructions.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type u_1} -> [CommSemiring R] -> {A : Type u_2} -> [Semiring A] -> [TopologicalSpace A] -> {B : Type u_3} -> [Semiring B] -> [TopologicalSpace B] -> [Algebra R A] -> [Algebra R B] -> (f : A →A[R] B) -> (f' : A → B) -> (h : f' = ⇑f) -> A →A[R] B
<!-- PINNED-SIGNATURE:END -->


The type-class arguments supply the ambient algebraic and topological structure: a commutative semiring `R` serving as the scalar ring, semirings `A` and `B` equipped with topologies, and `R`-algebra structures on both `A` and `B`. The explicit arguments are:
- `f` — the original continuous `R`-algebra homomorphism being copied.
- `f'` — the replacement bare function `A → B` that will become the new underlying function.
- `h` — a proof that `f'` equals the coercion `⇑f` of the original map, certifying that the two functions agree.

## Conventions

There are no junk-value or out-of-domain conventions declared for this definition: it is a total construction and every input satisfying the stated type and proof obligations produces a well-formed result.

## Worked examples

- Claim: For any `f : A →A[R] B`, `f'`, and `h : f' = ⇑f`, the coercion of `VTask.copy f f' h` equals `f'`.
  (This is the content of `coe_copy`: `⇑(VTask.copy f f' h) = f'`.)

- Claim: For any `f : A →A[R] B`, `f'`, and `h : f' = ⇑f`, the result `VTask.copy f f' h` is equal to `f` as a continuous algebra homomorphism.
  (This is the content of `copy_eq`: `VTask.copy f f' h = f`.)

- Claim: Applying `VTask.copy` with `f' = ⇑f` and `h = rfl` yields a morphism whose coercion is `⇑f` itself, i.e., `⇑(VTask.copy f (⇑f) rfl) = ⇑f`.

## Boundaries

- The only requirement on `f'` is the proof `h : f' = ⇑f`; in particular `f'` need not be defined by the same explicit formula as `f` — it merely needs to be provably (not necessarily definitionally) equal to `⇑f`.
- The result is always definitionally equal to `f` at the level of the morphism type, as witnessed by `copy_eq`.
- No restrictions on `R`, `A`, or `B` beyond the stated type-class assumptions are imposed; the definition is total.

## Not to be confused with

- The identity morphism `ContinuousAlgHom.id R A` — that is a specific canonical element, not a copying device for bookkeeping.
- `AlgHom.copy` (or `RingHom.copy`) — analogous copying constructors for purely algebraic (non-topological) algebra homomorphisms or ring homomorphisms, which do not carry continuity data.
- `ContinuousAlgHom.comp` — composition of two continuous algebra homomorphisms, which changes the domain or codomain rather than replacing the underlying function by a definitionally friendlier one.