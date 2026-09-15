## Object

Given a type `M` equipped with a non-associative semiring structure, and two ring congruence relations `c` and `d` on `M` with `c ≤ d` (meaning every pair related by `c` is also related by `d`), `VTask.map` produces the canonical ring homomorphism from the quotient ring `M/c` to the quotient ring `M/d`. Concretely, it sends the `c`-equivalence class of any element `x` to the `d`-equivalence class of `x`. This is well-defined precisely because `c ≤ d`: if two elements are `c`-equivalent, they are certainly `d`-equivalent, so the class of `x` in `M/c` maps unambiguously to the class of `x` in `M/d`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {M : Type u_1} -> [NonAssocSemiring M] -> (c d : RingCon M) -> (h : c ≤ d) -> c.Quotient →+* d.Quotient
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {M : Type u_1} -> [NonAssocSemiring M] -> (c d : RingCon M) -> (h : c ≤ d) -> c.Quotient →+* d.Quotient`

The implicit type argument `M` is the underlying carrier type. The instance argument provides the non-associative semiring structure on `M`. The argument `c` is the finer (smaller) ring congruence — the one we quotient by to obtain the domain. The argument `d` is the coarser (larger) ring congruence — the one we quotient by to obtain the codomain. The argument `h` is the proof that `c` is contained in `d`, i.e., whenever `c` relates two elements so does `d`; this is exactly the condition needed for the map to be well-defined.

## Conventions

No junk-value or out-of-domain conventions are declared for this definition: the map is defined for all pairs of ring congruences with a containment proof, and the output is always a valid ring homomorphism.

## Worked examples

- Claim: For any ring congruence `c` on a semiring `M`, applying `VTask.map c c (le_refl c)` to any element `[x]_c` yields `[x]_c` — that is, the map induced when `c = d` acts as the identity on every element of `c.Quotient`.

- Claim: If `c ≤ d ≤ e` are ring congruences on a semiring `M`, then `VTask.map c e (le_trans h₁ h₂)` equals the composition of `VTask.map c d h₁` followed by `VTask.map d e h₂` as ring homomorphisms — composing the two canonical maps gives the same result as the single canonical map for the outer pair.

- Claim: The kernel of `VTask.map c d h` consists of exactly those `c`-equivalence classes `[x]_c` such that `x` is `d`-equivalent to `0`, i.e., `d.Rel x 0`.

## Boundaries

- When `c = d` and `h` is `le_refl c`, the resulting homomorphism is the identity on `c.Quotient` (not syntactically equal, but equal as a ring homomorphism).
- When `c` is the trivial congruence (equality) and `d` is any congruence, the homomorphism is the quotient map from `M` itself (up to the identification `M ≅ M/equality`) to `M/d`.
- When `d` is the total congruence (every pair related), the codomain `d.Quotient` is the zero ring, and `VTask.map c d h` is the unique ring homomorphism to the zero ring.
- The map is always surjective whenever `d`'s quotient map is surjective, which it always is; hence `VTask.map c d h` is always a surjective ring homomorphism.
- The containment `h : c ≤ d` is essential: without it the assignment `[x]_c ↦ [x]_d` would not be well-defined, so there is no version of this construction that works without the ordering hypothesis.

## Not to be confused with

- `RingCon.mk'` (for a single congruence `c`): this is the quotient map `M →+* M/c` itself, not a map between two quotients.
- `RingHom.liftOfRightInverse` or `RingCon.lift`: these produce homomorphisms out of a quotient ring given an arbitrary compatible homomorphism, rather than the canonical comparison map between two quotient rings of the same base.
- The analogous construction for `Con` (congruences on monoids/groups without ring structure): that version lacks the ring homomorphism structure and operates in a different category.