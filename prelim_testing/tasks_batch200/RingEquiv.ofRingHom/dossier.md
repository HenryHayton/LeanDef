## Object

`VTask.ofRingHom` constructs a ring isomorphism `R ≃+* S` from a pair of ring homomorphisms that are inverses of each other. Given a ring homomorphism `f : R →+* S` and another ring homomorphism `g : S →+* R` such that `f ∘ g = id_S` and `g ∘ f = id_R`, the result is the bundled two-sided ring isomorphism whose underlying forward map is `f` and whose underlying inverse map is `g`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofRingHom : {R : Type u_4} -> {S : Type u_5} -> [NonAssocSemiring R] -> [NonAssocSemiring S] -> (f : R →+* S) -> (g : S →+* R) -> (h₁ : f.comp g = RingHom.id S) -> (h₂ : g.comp f = RingHom.id R) -> R ≃+* S
<!-- PINNED-SIGNATURE:END -->


VTask.ofRingHom : {R : Type u_4} -> {S : Type u_5} -> [NonAssocSemiring R] -> [NonAssocSemiring S] -> (f : R →+* S) -> (g : S →+* R) -> (h₁ : f.comp g = RingHom.id S) -> (h₂ : g.comp f = RingHom.id R) -> R ≃+* S

The implicit type arguments `R` and `S` are the source and target semirings, inferred from context; their `NonAssocSemiring` instances are also implicit. The argument `f` is the forward ring homomorphism from `R` to `S`. The argument `g` is the proposed inverse ring homomorphism from `S` back to `R`. The proof `h₁` witnesses that composing `f` after `g` yields the identity on `S` (i.e., `g` is a right inverse of `f`). The proof `h₂` witnesses that composing `g` after `f` yields the identity on `R` (i.e., `g` is a left inverse of `f`).

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total constructor that simply packages the given data into a ring isomorphism, and all four arguments are required to be fully specified.

## Worked examples

- Claim: When `f` is a ring homomorphism and `e = VTask.ofRingHom f g h₁ h₂`, the coercion of `e` as a ring homomorphism equals `f`.

- Claim: The symmetry of `VTask.ofRingHom f g h₁ h₂` equals `VTask.ofRingHom g f h₂ h₁`; that is, swapping the roles of `f` and `g` and swapping the two proofs produces the inverse isomorphism.

- Claim: For any ring isomorphism `e : R ≃+* S`, if one takes `f = ↑e` (the coercion to a ring homomorphism), then `VTask.ofRingHom (↑e) g h₁ h₂ = e`, showing that `ofRingHom` recovers `e` when `f` already comes from a ring isomorphism.

## Boundaries

- The definition is total: it places no restrictions on `R` or `S` beyond being `NonAssocSemiring`s, and it requires both inverse proofs to be supplied by the caller.
- If `g` is not truly a two-sided inverse of `f` (i.e., if either `h₁` or `h₂` were somehow false), the construction could not be carried out; soundness is guaranteed by the proof terms.
- The resulting isomorphism's forward function is definitionally equal to `f`, and its inverse function is definitionally equal to `g`.

## Not to be confused with

- `RingEquiv.symm`: takes an already-constructed ring isomorphism and flips it; does not require re-supplying the inverse as a ring homomorphism.
- `RingHom.comp`: merely composes two ring homomorphisms without asserting invertibility or producing an isomorphism.
- `RingEquiv.toRingHom` (coercion `↑e`): goes the other way, extracting a ring homomorphism from a ring isomorphism, rather than building an isomorphism from ring homomorphisms.
