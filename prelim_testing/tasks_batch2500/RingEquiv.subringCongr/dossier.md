## Object

`VTask.subringCongr` constructs the canonical ring isomorphism (identity map) between two subrings of a ring that are known to be equal as subrings. Given a proof that two subrings `s` and `t` of a ring `R` are identical, it packages the identity correspondence between their underlying types into a bundled ring isomorphism `s ≃+* t`, preserving both addition and multiplication.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subringCongr : {R : Type u} -> [NonAssocRing R] -> {s t : Subring R} -> (h : s = t) -> ↥s ≃+* ↥t
<!-- PINNED-SIGNATURE:END -->


`VTask.subringCongr : {R : Type u} -> [NonAssocRing R] -> {s t : Subring R} -> (h : s = t) -> ↥s ≃+* ↥t`

The ambient type `R` is the ring in which both subrings live. The instance supplies the non-associative ring structure on `R`. The implicit arguments `s` and `t` are the two subrings being identified. The explicit argument `h` is the proof of equality `s = t`, which is the sole data driving the construction.

## Conventions

There are no junk-value or default conventions declared for this definition: it is a total function on a fully constrained domain (a proof of equality between subrings), leaving no room for undefined or conventionally-chosen behavior at boundary inputs.

## Worked examples

- Claim: For any subring `s` of a ring `R`, `VTask.subringCongr (rfl : s = s)` is the identity ring isomorphism on `s`, meaning for any element `x : s` the value of the coercion of the image equals the coercion of `x`.

- Claim: If `h : s = t` is a proof of subring equality, then the symmetry of `VTask.subringCongr h` equals `VTask.subringCongr h.symm`; that is, the inverse isomorphism obtained by flipping `h` coincides with the inverse of the constructed isomorphism.

- Claim: For any `x : ↥s` and proof `h : s = t`, `(VTask.subringCongr h x).val = x.val`; the isomorphism acts as the identity on underlying elements of `R`.

## Boundaries

- The only input to the construction is the equality proof `h : s = t`. When `h` is `rfl` (i.e., `s = t = s`), the result is literally the identity isomorphism on `s`.
- Because the map sends every element to itself (as elements of `R`), composition of `VTask.subringCongr h` with `VTask.subringCongr h.symm` is the identity isomorphism on `s`, and composition in the other order is the identity on `t`.
- The construction does not depend on any properties of `R` beyond it being a `NonAssocRing`; in particular, commutativity and associativity of `R` are not required.

## Not to be confused with

- `RingEquiv.refl s` — the identity ring isomorphism from `s` to itself; `VTask.subringCongr rfl` coincides with it, but `VTask.subringCongr` handles the case where the two subrings are equal but not definitionally the same term.
- Subring inclusion or coercion maps — those map from a subring into a larger ring, whereas `VTask.subringCongr` maps between two subrings at the same level.
- `Equiv.setCongr` — a plain set-level equivalence between equal sets; `VTask.subringCongr` additionally packages ring-homomorphism compatibility (preservation of `+` and `*`), making it a full ring isomorphism.
