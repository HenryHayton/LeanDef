## Object

`VTask.ofLeftInverse'` constructs a ring isomorphism (a `RingEquiv`) from a non-unital ring `R` to the image (range) of a non-unital ring homomorphism `f : R →ₙ+* S`, given evidence that `f` has a left inverse. Because `f` has a left inverse it is injective, so the co-restricted map `R → f.range` is bijective and thus an isomorphism.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofLeftInverse' : {R : Type u} -> {S : Type v} -> [NonUnitalRing R] -> [NonUnitalRing S] -> {g : S → R} -> {f : R →ₙ+* S} -> (h : Function.LeftInverse g ⇑f) -> R ≃+* ↥f.range
<!-- PINNED-SIGNATURE:END -->


VTask.ofLeftInverse' : {R : Type u} -> {S : Type v} -> [NonUnitalRing R] -> [NonUnitalRing S] -> {g : S → R} -> {f : R →ₙ+* S} -> (h : Function.LeftInverse g ⇑f) -> R ≃+* ↥f.range

`R` and `S` are the source and target non-unital rings, respectively. The instance arguments supply each type's non-unital ring structure. The implicit argument `f` is the non-unital ring homomorphism being restricted; `g` is the bare set-function acting as a left inverse to `f`. The explicit argument `h` is the proof that `g` is indeed a left inverse of `f`, i.e., `g (f x) = x` for every `x : R`. The result is a ring isomorphism from `R` to the subring `f.range` inside `S`.

## Conventions

No junk-value or out-of-domain conventions are declared: every input satisfying the stated types is valid, and the function is total on its domain.

## Worked examples

- Claim: When `f` is the identity non-unital ring homomorphism on a non-unital ring `R` (with `g = id` as left inverse), `VTask.ofLeftInverse'` produces an isomorphism from `R` to `(NonUnitalRingHom.id R).range`, which equals `R` itself.

- Claim: If `f : R →ₙ+* S` is injective and `g` is any left inverse, then the forward component of the isomorphism `VTask.ofLeftInverse' h` applied to `x : R` lands in `f.range`, specifically at the element `⟨f x, ⟨x, rfl⟩⟩`.

- Claim: The isomorphism `VTask.ofLeftInverse' h` is surjective onto `f.range`; every element `⟨s, hs⟩ : ↥f.range` is hit by some `x : R`.

- Claim: For any `x : R`, applying the inverse of `VTask.ofLeftInverse' h` to the image `⟨f x, ⟨x, rfl⟩⟩` returns `x`.

## Boundaries

- The construction requires only that `g` is a left inverse on the underlying function level; `g` need not be a ring homomorphism itself.
- Because a left inverse implies injectivity, `f` is automatically injective whenever `VTask.ofLeftInverse'` applies, so the co-restriction to `f.range` is indeed bijective.
- The range `f.range` is a non-unital subring of `S`; the isomorphism targets this subring as a type in its own right (`↥f.range`), not all of `S`.
- If `f` were not injective no left inverse could exist, so that degenerate case is excluded by the hypothesis `h`.

## Not to be confused with

- `NonUnitalRingHom.rangeRestrict`: the plain co-restriction of `f` to its range as a ring homomorphism, without an inverse or isomorphism structure.
- A `RingEquiv` built from a surjective homomorphism: `VTask.ofLeftInverse'` works from a left-inverse hypothesis (injectivity side), not a surjectivity/quotient argument.
- The unital analogue for `RingHom` (i.e., ring homomorphisms between unital rings): `VTask.ofLeftInverse'` specifically handles `NonUnitalRingHom` and `NonUnitalRing`.