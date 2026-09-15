## 1. Object

This is a canonical isomorphism of R-algebras between two ways to encode the **dual quaternions** over a commutative ring R:

- **Left side:** quaternions whose four coefficients (re, i, j, k) are each a dual number over R — that is, elements of `R[ε]/(ε²)`. In symbols, `ℍ(R[ε])`, a quaternion algebra over the ring of dual numbers.
- **Right side:** a dual number whose two components (the "real part" and the "infinitesimal part") are each a quaternion over R. In symbols, `ℍ(R)[ε]`, a dual-number algebra over the quaternion algebra.

The two representations carry exactly the same eight scalar data — four real parts and four infinitesimal parts of the four quaternion components — just packaged differently. The equivalence transports them by reassembling that data in the opposite order, and it respects the full R-algebra structure (addition, multiplication, and the scalar action of R).

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dualNumberEquiv : {R : Type u_1} -> [CommRing R] -> Quaternion (DualNumber R) ≃ₐ[R] DualNumber (Quaternion R)
<!-- PINNED-SIGNATURE:END -->


`VTask.dualNumberEquiv : {R : Type u_1} -> [CommRing R] -> Quaternion (DualNumber R) ≃ₐ[R] DualNumber (Quaternion R)`

The implicit type parameter `R` is the underlying commutative ring whose elements serve as the scalar coefficients at the bottom of both constructions. The instance `[CommRing R]` supplies the ring structure on R that is needed to form both the quaternion algebra and the dual-number algebra over it. There are no explicit arguments: the equivalence itself is the value — it is a bundled object carrying both directions of the isomorphism and the proofs that they are mutually inverse R-algebra homomorphisms.

## 3. Conventions

No junk-value or default-value conventions are declared for this definition: it is a total, structure-valued term (a bundled algebra equivalence) with no inputs on which an out-of-domain or degenerate case could arise.

## 4. Worked examples

- Claim: For a quaternion `q : Quaternion (DualNumber R)`, the real part of the "real quaternion" component of `VTask.dualNumberEquiv q` equals the real part of the real-part dual number of `q`. That is, `(VTask.dualNumberEquiv q).fst.re = q.re.fst`.

- Claim: For a quaternion `q : Quaternion (DualNumber R)`, the i-component of the "epsilon quaternion" component of `VTask.dualNumberEquiv q` equals the infinitesimal part of the i-component dual number of `q`. That is, `(VTask.dualNumberEquiv q).snd.imI = q.imI.snd`.

- Claim: Applying `VTask.dualNumberEquiv` and then its inverse recovers the original element: for any `q : Quaternion (DualNumber R)`, `VTask.dualNumberEquiv.symm (VTask.dualNumberEquiv q) = q`.

- Claim: `VTask.dualNumberEquiv` is an R-algebra homomorphism, so in particular it maps the sum of two elements to the sum of their images: `VTask.dualNumberEquiv (p + q) = VTask.dualNumberEquiv p + VTask.dualNumberEquiv q`.

## 5. Boundaries

- The definition is valid for any commutative ring R, including degenerate cases such as the zero ring (where `0 = 1`). The isomorphism still holds in those cases, as the algebraic identities are purely formal.
- There is no restriction to fields or to characteristic-zero rings; the equivalence is purely ring-theoretic and requires no invertibility hypotheses.
- The two algebra structures being identified are not isomorphic as *non-associative* algebras in general; the isomorphism is specifically one of *associative* R-algebras, and both sides do carry the same associative multiplication.
- Since this is an equivalence (not merely a homomorphism in one direction), both `VTask.dualNumberEquiv` and `VTask.dualNumberEquiv.symm` are inverse R-algebra isomorphisms.

## 6. Not to be confused with

- **`Matrix.dualNumberEquiv`**: the analogous isomorphism for matrices instead of quaternions — matrices with dual-number entries versus dual numbers with matrix entries; structurally parallel but for a different algebra.
- **`Quaternion.instAlgebraDualNumber`** (the algebra instance alone): the algebra structure on `Quaternion (DualNumber R)` as an R-algebra, without the isomorphism to the other presentation.
- **`TrivSqZeroExt`** (the general dual-number / trivial square-zero extension construction): the general framework of which `DualNumber R` is a special case; `VTask.dualNumberEquiv` is a specific isomorphism between two instances of this construction, not the construction itself.