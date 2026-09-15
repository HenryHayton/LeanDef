## VTask.codRestrict

### Object

Given a continuous `R`-algebra homomorphism `f : A →A[R] B` whose image is contained in a subalgebra `p` of `B`, `VTask.codRestrict f p h` is the induced continuous `R`-algebra homomorphism from `A` to `p` (the subalgebra viewed as a topological `R`-algebra in its own right). It is the same map as `f`, but with the codomain narrowed from `B` to `p`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.codRestrict : {R : Type u_1} -> [CommSemiring R] -> {A : Type u_2} -> [Semiring A] -> [TopologicalSpace A] -> {B : Type u_3} -> [Semiring B] -> [TopologicalSpace B] -> [Algebra R A] -> [Algebra R B] -> (f : A →A[R] B) -> (p : Subalgebra R B) -> (h : ∀ (x : A), f x ∈ p) -> A →A[R] ↥p
<!-- PINNED-SIGNATURE:END -->


`VTask.codRestrict : {R : Type u_1} -> [CommSemiring R] -> {A : Type u_2} -> [Semiring A] -> [TopologicalSpace A] -> {B : Type u_3} -> [Semiring B] -> [TopologicalSpace B] -> [Algebra R A] -> [Algebra R B] -> (f : A →A[R] B) -> (p : Subalgebra R B) -> (h : ∀ (x : A), f x ∈ p) -> A →A[R] ↥p`

The implicit arguments `R`, `A`, `B` are the coefficient semiring, the source topological `R`-algebra, and the target topological `R`-algebra, respectively; all algebraic and topological structures are supplied by the accompanying type-class instances. The argument `f` is the continuous `R`-algebra homomorphism whose codomain is to be restricted. The argument `p` is the subalgebra of `B` to which the codomain is being restricted. The argument `h` is the proof (a pointwise membership statement) that every element in the image of `f` belongs to `p`.

### Conventions

No special junk-value or out-of-domain conventions are declared for this definition: it is a total construction whenever the three explicit arguments `f`, `p`, and `h` are supplied, and every well-typed call produces a well-defined continuous `R`-algebra homomorphism into `p`.

### Worked Examples

- Claim: For any continuous `R`-algebra morphism `f : A →A[R] B` with image in `p`, the underlying `B`-valued map of `VTask.codRestrict f p h` agrees pointwise with `f`. That is, `↑(VTask.codRestrict f p h x) = f x` for every `x : A`.

- Claim: The underlying (non-continuous) algebra homomorphism of `VTask.codRestrict f p h` (coerced to `A →ₐ[R] p`) equals the codomain restriction of the underlying algebra homomorphism of `f`. That is, `(VTask.codRestrict f p h : A →ₐ[R] p) = (f : A →ₐ[R] B).codRestrict p h`.

### Boundaries

- If `p` is the top subalgebra `⊤` of `B`, then `h` is trivially satisfied by all elements, and the result is essentially the same map as `f` with a nominal change of codomain to `↥⊤ ≅ B`.
- If `p` is the bottom subalgebra (e.g., the image of the scalars), then `h` forces `f` to land in that small subalgebra, severely constraining which `f` can legally appear.
- The continuity of the result is inherited directly from the continuity of `f`; no additional continuity hypotheses on `p` are needed beyond those already present in the ambient topology on `B`.
- The membership proof `h` is a proof-irrelevant witness: two calls differing only in `h` produce definitionally equal results.

### Not to be confused with

- `AlgHom.codRestrict` — the purely algebraic (non-topological) version that restricts the codomain of a plain `R`-algebra homomorphism, without any continuity requirement or guarantee.
- `ContinuousAlgHom.restrict` (domain restriction) — restricts the *domain* of a continuous algebra morphism to a subalgebra of the source, rather than the codomain.
- `ContinuousLinearMap.codRestrict` — the analogous construction for continuous *linear* maps between modules, which does not carry the multiplicative algebra-homomorphism structure.