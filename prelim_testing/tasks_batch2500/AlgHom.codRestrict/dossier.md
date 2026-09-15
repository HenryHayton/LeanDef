## VTask.codRestrict

### Object

Given an algebra homomorphism `f : A →ₐ[R] B` whose image is entirely contained in a subalgebra `S` of `B`, `VTask.codRestrict f S hf` is the algebra homomorphism `A →ₐ[R] S` obtained by restricting the codomain of `f` to `S`. The underlying map is the same as `f`, but the target type is narrowed from all of `B` to the subtype `↥S`. The result is an `R`-algebra homomorphism in the full sense: it preserves addition, multiplication, scalar action by `R`, and the algebra map from `R`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.codRestrict : {R : Type u} -> {A : Type v} -> {B : Type w} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Semiring B] -> [Algebra R B] -> (f : A →ₐ[R] B) -> (S : Subalgebra R B) -> (hf : ∀ (x : A), f x ∈ S) -> A →ₐ[R] ↥S
<!-- PINNED-SIGNATURE:END -->


The implicit arguments `R`, `A`, `B` are the commutative semiring of scalars, the source algebra, and the target algebra, respectively, each carrying the appropriate `CommSemiring`/`Semiring`/`Algebra` instances. The argument `f` is the `R`-algebra homomorphism to be restricted. The argument `S` is the subalgebra of `B` that will serve as the new codomain. The argument `hf` is a proof that every element in the image of `f` belongs to `S`, i.e., `f x ∈ S` for all `x : A`.

### Conventions

There are no special junk-value or edge-case conventions for this construction: it is well-defined and total on all inputs satisfying the stated hypotheses, and the only precondition is the membership proof `hf` supplied explicitly by the caller.

### Worked examples

- Claim: For any `f : A →ₐ[R] B`, subalgebra `S`, and proof `hf`, the coercion of `VTask.codRestrict f S hf x` back to `B` equals `f x` for every `x : A`.

- Claim: The inclusion of `S` into `B` (the canonical subalgebra map `S.val`) composed with `VTask.codRestrict f S hf` equals `f` as algebra homomorphisms `A →ₐ[R] B`.

- Claim: `VTask.codRestrict f S hf` is injective if and only if `f` itself is injective.

### Boundaries

- If `S` is all of `B` (i.e., `S = ⊤`), the construction still produces a well-typed homomorphism `A →ₐ[R] ↥⊤`; it is isomorphic to `f` but targets the subtype, not `B` itself.
- If `f` is the zero map (when the algebra is the zero ring), every value lands in `S` trivially; `hf` is still required as an explicit argument.
- The construction does not require `f` to be surjective onto `S`; `S` may be strictly larger than the image of `f`.
- Injectivity is preserved and reflected: the codomain restriction is injective precisely when the original map is injective, since the underlying set-map is unchanged.

### Not to be confused with

- `AlgHom.range`: produces the image subalgebra of `f` inside `B`, rather than restricting to a pre-specified subalgebra.
- `AlgHom.domRestrict` (or restricting to a subalgebra on the source side): narrows the *domain* to a subalgebra of `A`, not the codomain.
- `RingHom.codRestrict`: the analogous construction for ring homomorphisms, without the algebra/scalar-action structure; `VTask.codRestrict` lifts this to the algebra setting.