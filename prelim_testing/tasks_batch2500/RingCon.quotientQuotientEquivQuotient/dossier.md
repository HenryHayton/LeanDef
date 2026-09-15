## Object

This is the **third isomorphism theorem for semirings (and rings)**. Given two ring congruences `c` and `d` on a semiring `M` with `c ≤ d` (every pair related by `c` is also related by `d`), there is a natural surjective ring homomorphism from the `c`-quotient `M/c` to the `d`-quotient `M/d`. The kernel of this map is itself a ring congruence on `M/c`. The third isomorphism theorem asserts that the quotient of `M/c` by this kernel is canonically ring-isomorphic to `M/d`. This definition packages that canonical isomorphism as a bundled ring equivalence (`≃+*`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.quotientQuotientEquivQuotient : {M : Type u_1} -> [NonAssocSemiring M] -> (c d : RingCon M) -> (h : c ≤ d) -> (RingCon.ker (c.map d h)).Quotient ≃+* d.Quotient
<!-- PINNED-SIGNATURE:END -->


`VTask.quotientQuotientEquivQuotient : {M : Type u_1} -> [NonAssocSemiring M] -> (c d : RingCon M) -> (h : c ≤ d) -> (RingCon.ker (c.map d h)).Quotient ≃+* d.Quotient`

The implicit type `M` is the underlying semiring. The instance `[NonAssocSemiring M]` supplies the ring structure on `M`. The argument `c` is the finer (smaller) ring congruence, and `d` is the coarser (larger) ring congruence. The proof `h : c ≤ d` witnesses that `c` is finer than `d`, which is the hypothesis needed to induce the natural projection from `M/c` to `M/d`. The result is a ring isomorphism from the quotient of `M/c` by the kernel of that projection to `M/d`.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a mathematically meaningful isomorphism whenever the inputs satisfy `c ≤ d`, and the domain imposes no additional restrictions beyond the type class.

## Worked examples

- Claim: For any semiring `M` and congruences `c ≤ d`, the isomorphism `VTask.quotientQuotientEquivQuotient c d h` sends the double-coset `⟦⟦x⟧⟧` (an element of `(M/c) / ker`) to the coset `⟦x⟧` in `M/d`.

- Claim: The inverse of `VTask.quotientQuotientEquivQuotient c d h` sends a coset `⟦x⟧` in `M/d` back to the double-coset `⟦⟦x⟧⟧` in `(M/c) / ker`.

- Claim: `VTask.quotientQuotientEquivQuotient c d h` is compatible with ring addition: for elements `a b : M`, the image of the double-coset of `a + b` equals the sum of the images of the double-cosets of `a` and `b`.

- Claim: `VTask.quotientQuotientEquivQuotient c d h` is compatible with ring multiplication: for elements `a b : M`, the image of the double-coset of `a * b` equals the product of the images of the double-cosets of `a` and `b`.

## Boundaries

- When `c = d` (the two congruences coincide), the kernel of the induced map `M/c → M/d` is trivial (the equality congruence), so the domain of the isomorphism is canonically isomorphic to `M/c` itself, and the isomorphism reduces to the natural identification `M/c ≃+* M/d`.
- When `c` is the trivial congruence (only relates each element to itself) and `d` is arbitrary, the map `M/c ≅ M → M/d` is the standard quotient map, and the theorem recovers the first isomorphism theorem in disguise.
- The definition requires only `NonAssocSemiring` structure on `M`; it applies to semirings without requiring commutativity or the existence of multiplicative inverses.

## Not to be confused with

- The **first isomorphism theorem** for rings (`RingCon.quotientKerEquivOfSurjective`), which gives `M / ker(f) ≃+* im(f)` for a surjective ring homomorphism, rather than a quotient-of-a-quotient.
- The **algebra version** `quotientQuotientEquivQuotientₐ`, which is the analogous statement for `R`-algebras and carries an additional scalar action that is absent here.
- The underlying **setoid-level equivalence** `Setoid.quotientQuotientEquivQuotient`, which is the same bijection at the level of types/setoids but does not carry or verify the ring homomorphism structure.