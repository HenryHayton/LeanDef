## Object

`VTask.ofLeftInverse` constructs a ring isomorphism between a ring `R` and the image (range) of a ring homomorphism `f : R →+* S`, given evidence that `f` admits a left inverse as a bare function. Concretely, if there exists a function `g : S → R` such that `g(f(r)) = r` for every `r : R`, then `f` is injective, and the corestriction of `f` to its image is therefore a bijection — this bijection is packaged as a bundled ring isomorphism `R ≃+* f.range`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofLeftInverse : {R : Type u} -> {S : Type v} -> [NonAssocRing R] -> [NonAssocRing S] -> {g : S → R} -> {f : R →+* S} -> (h : Function.LeftInverse g ⇑f) -> R ≃+* ↥f.range
<!-- PINNED-SIGNATURE:END -->


VTask.ofLeftInverse : {R : Type u} -> {S : Type v} -> [NonAssocRing R] -> [NonAssocRing S] -> {g : S → R} -> {f : R →+* S} -> (h : Function.LeftInverse g ⇑f) -> R ≃+* ↥f.range

- `R` is the source ring (a `NonAssocRing`), inferred from context.
- `S` is the target ring (a `NonAssocRing`), inferred from context.
- The `NonAssocRing` instances for `R` and `S` supply the ring structure used by the isomorphism.
- `g : S → R` is a bare (not necessarily a ring-homomorphism) retraction function, inferred from context; it serves only to witness the existence of a left inverse.
- `f : R →+* S` is the ring homomorphism whose range is the codomain of the resulting isomorphism, inferred from context.
- `h : Function.LeftInverse g ⇑f` is the proof that `g` is a left inverse of `f`, i.e., `∀ r, g (f r) = r`; this is the sole explicit argument and the key hypothesis that makes `f` injective and the construction valid.

## Conventions

There are no junk-value or edge-case conventions to declare: the definition is total over all inputs satisfying the stated types and the left-inverse hypothesis, and every such input yields a well-defined ring isomorphism.

## Worked examples

- Claim: For the identity ring homomorphism `f = RingHom.id R`, the left inverse is `id`, and `VTask.ofLeftInverse` produces an isomorphism `R ≃+* (RingHom.id R).range` whose forward direction sends `r` to `⟨r, ⟨r, rfl⟩⟩`.

- Claim: If `f : R →+* S` is injective with a left inverse `g`, then for any `r : R`, the element `(VTask.ofLeftInverse h) r` belongs to `f.range` and its underlying value in `S` equals `f r`.

- Claim: If `f : ℤ →+* ℤ` is the identity homomorphism and `g = id`, then `VTask.ofLeftInverse (fun x => rfl)` is a ring isomorphism from `ℤ` to `(RingHom.id ℤ).range`.

- Claim: The inverse of `VTask.ofLeftInverse h`, applied to an element `⟨s, hs⟩ ∈ f.range`, equals `g s`.

## Boundaries

- The function `g` need not be a ring homomorphism; it only needs to be a set-theoretic left inverse of `f`.
- The existence of a left inverse implies `f` is injective, so the corestriction to the range is a bijection — but the construction does not require `f` to be surjective onto all of `S`.
- The range `f.range` is a subring of `S`; the isomorphism lands in this subring, not in `S` itself.
- If `f` were not injective, no left inverse could exist, so the hypothesis `h` rules out that degenerate case entirely.
- `NonAssocRing` is used rather than the stronger `Ring` or `CommRing`; the construction works in this generality.

## Not to be confused with

- `RingEquiv.ofBijective`: constructs a ring isomorphism from `R` to `S` (not just to `f.range`) when `f` is both injective and surjective, requiring full bijectivity rather than just a left inverse.
- `RingHom.rangeRestrict`: the ring homomorphism `R →+* f.range` obtained by corestricting `f`, without any inverse — `VTask.ofLeftInverse` upgrades this to an isomorphism using `h`.
- `Function.LeftInverse` vs `Function.RightInverse`: a left inverse `g ∘ f = id` (used here) is not the same as a right inverse `f ∘ g = id`; confusing the two would give the wrong hypothesis.
