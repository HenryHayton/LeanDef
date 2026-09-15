## Object

`VTask.sofLeftInverse'` constructs a non-unital ring isomorphism (a `NonUnitalRingEquiv`, written `≃+*`) between a non-unital non-associative semiring `R` and the *image* (surjective range, `srange`) of a non-unital ring homomorphism `f : R →+* S`, given evidence that `f` has a left inverse `g : S → R`. Because `f` has a left inverse it is injective, so `R` is in bijection with `f`'s image in `S`; the construction packages that bijection together with the inherited ring structure to produce a genuine ring isomorphism.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sofLeftInverse' : {R : Type u} -> {S : Type v} -> [NonUnitalNonAssocSemiring R] -> [NonUnitalNonAssocSemiring S] -> {F : Type u_1} -> [FunLike F R S] -> [NonUnitalRingHomClass F R S] -> {g : S → R} -> {f : F} -> (h : Function.LeftInverse g ⇑f) -> R ≃+* ↥(NonUnitalRingHom.srange f)
<!-- PINNED-SIGNATURE:END -->


VTask.sofLeftInverse' : {R : Type u} -> {S : Type v} -> [NonUnitalNonAssocSemiring R] -> [NonUnitalNonAssocSemiring S] -> {F : Type u_1} -> [FunLike F R S] -> [NonUnitalRingHomClass F R S] -> {g : S → R} -> {f : F} -> (h : Function.LeftInverse g ⇑f) -> R ≃+* ↥(NonUnitalRingHom.srange f)

`R` is the source non-unital non-associative semiring and `S` is the target. `F` is the type of the homomorphism, which is required to carry both a `FunLike` instance (giving it an underlying function) and a `NonUnitalRingHomClass` instance (ensuring it is a non-unital ring homomorphism). The implicit argument `g : S → R` is the proposed left inverse of `f`. The implicit argument `f : F` is the non-unital ring homomorphism whose image is being identified with `R`. The explicit argument `h` is the proof that `g` is indeed a left inverse of `f`, i.e., `g (f r) = r` for every `r : R`.

## Conventions

No special junk-value or edge-case conventions have been declared for this definition: it is a function from a proof to a structured algebraic object, and the result is well-defined for any valid input.

## Worked examples

- Claim: Applying `VTask.sofLeftInverse'` to the identity map on a non-unital semiring `R` (with itself as left inverse) yields a ring isomorphism from `R` to `srange (NonUnitalRingHom.id R)`.

- Claim: If `f : R →ₙ+* S` is injective and `g` is any left inverse, then `(VTask.sofLeftInverse' h).toFun r` lies in `NonUnitalRingHom.srange f` for every `r : R`.

- Claim: For any `r : R`, applying the forward direction of `VTask.sofLeftInverse' h` and then the inverse direction recovers `r` (i.e., the underlying left inverse condition `h` is exactly the `left_inv` field of the resulting equivalence).

## Boundaries

- The construction requires only a *left* inverse `g` of `f`; `g` need not itself be a ring homomorphism, nor does it need to be a full two-sided inverse globally on `S`. The right-inverse condition is established only on elements of `srange f`.
- If `f` happens to be surjective (so `srange f = S`), the resulting isomorphism is between `R` and all of `S`, but the type of the output still carries the subtype `↥(srange f)` rather than `S` itself.
- The definition is stated in full generality for any `F` with the appropriate typeclasses, so it applies to `NonUnitalRingHom` directly as well as any other type in the non-unital ring hom hierarchy.
- There is no distinctly handled degenerate case for the zero ring or trivial maps; the construction is uniform.

## Not to be confused with

- `NonUnitalRingEquiv.ofLeftInverse` (or its variant without the prime): the version for *unital* ring homomorphisms, which additionally preserves the multiplicative identity.
- `NonUnitalRingHom.srangeRestrict`: the plain ring homomorphism `R →ₙ+* srange f` obtained by restricting the codomain of `f`; `VTask.sofLeftInverse'` upgrades this to a full isomorphism using the left inverse hypothesis.
- `Function.LeftInverse.injective`: a bare injectivity result; `VTask.sofLeftInverse'` is strictly stronger, providing the full ring-isomorphism structure rather than just an injective function.