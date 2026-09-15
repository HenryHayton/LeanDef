## VTask.ofStarAlgHom

### Object

This constructor produces a star algebra equivalence (a bijective, star-preserving, `R`-algebra isomorphism) `A ≃⋆ₐ[R] B` from the data of two star algebra homomorphisms that are mutually inverse. Given `f : A →⋆ₐ[R] B` and `g : B →⋆ₐ[R] A` satisfying `g ∘ f = id` and `f ∘ g = id`, it packages them into a single invertible star algebra map.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofStarAlgHom : {R : Type u_8} -> {A : Type u_9} -> {B : Type u_10} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Star A] -> [Semiring B] -> [Algebra R B] -> [Star B] -> (f : A →⋆ₐ[R] B) -> (g : B →⋆ₐ[R] A) -> (h₁ : g.comp f = StarAlgHom.id R A) -> (h₂ : f.comp g = StarAlgHom.id R B) -> A ≃⋆ₐ[R] B
<!-- PINNED-SIGNATURE:END -->


VTask.ofStarAlgHom : {R : Type u_8} -> {A : Type u_9} -> {B : Type u_10} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Star A] -> [Semiring B] -> [Algebra R B] -> [Star B] -> (f : A →⋆ₐ[R] B) -> (g : B →⋆ₐ[R] A) -> (h₁ : g.comp f = StarAlgHom.id R A) -> (h₂ : f.comp g = StarAlgHom.id R B) -> A ≃⋆ₐ[R] B

`R` is the commutative semiring of scalars over which both algebras are defined. `A` and `B` are the source and target semirings, each carrying an `R`-algebra structure and a star operation. The argument `f` is the forward star algebra homomorphism from `A` to `B`. The argument `g` is the reverse star algebra homomorphism from `B` to `A`, intended to serve as the inverse of `f`. The proof `h₁` witnesses that `g` composed with `f` is the identity on `A`, i.e., `g` is a left inverse of `f`. The proof `h₂` witnesses that `f` composed with `g` is the identity on `B`, i.e., `g` is a right inverse of `f`.

### Conventions

There are no junk-value or edge-case conventions for this constructor: it is a total function whose inputs are required to satisfy the mutual-inverse conditions as explicit proof arguments, so no degenerate output arises.

### Worked examples

- Claim: For the identity star algebra homomorphism `f = g = StarAlgHom.id R A`, `VTask.ofStarAlgHom f g h₁ h₂` is a valid star algebra equivalence, and its underlying forward homomorphism equals `f`.

- Claim: The underlying forward star algebra homomorphism of `VTask.ofStarAlgHom f g h₁ h₂` is `f`, i.e., `(VTask.ofStarAlgHom f g h₁ h₂).toStarAlgHom = f`.

- Claim: The inverse (symmetry) of `VTask.ofStarAlgHom f g h₁ h₂` equals `VTask.ofStarAlgHom g f h₂ h₁`, meaning the roles of `f` and `g` are swapped and the two inverse conditions are exchanged.

- Claim: The underlying star algebra homomorphism of the symmetric equivalence satisfies `(VTask.ofStarAlgHom f g h₁ h₂).symm.toStarAlgHom = g`.

### Boundaries

- The constructor is only available when both `h₁ : g.comp f = StarAlgHom.id R A` and `h₂ : f.comp g = StarAlgHom.id R B` are supplied; these are mandatory proof arguments, not side conditions that could be vacuously satisfied.
- When `A = B` and `f = g = StarAlgHom.id R A`, the two conditions hold trivially and the resulting equivalence is the identity star algebra equivalence.
- There is no requirement that `A` and `B` be unital beyond being semirings; the algebra structure is assumed via the `Algebra R A` and `Algebra R B` typeclasses.
- The star operations on `A` and `B` are required by the `Star A` and `Star B` typeclasses; compatibility of `f` and `g` with the star is guaranteed by their types as star algebra homomorphisms.

### Not to be confused with

- `StarAlgEquiv.mk`: A lower-level constructor that directly provides all fields of a star algebra equivalence without requiring the bundled-homomorphism presentation.
- `AlgEquiv.ofAlgHom`: The analogous constructor for plain algebra equivalences without the star structure; it does not track or require star-compatibility.
- `StarAlgHom.comp`: The composition of two star algebra homomorphisms, which appears in the hypotheses `h₁` and `h₂` but does not itself produce an equivalence.
