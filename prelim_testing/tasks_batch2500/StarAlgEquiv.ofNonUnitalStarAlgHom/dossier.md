## VTask.ofNonUnitalStarAlgHom

### Object

A constructor that packages a mutually inverse pair of non-unital star algebra homomorphisms into a single star algebra equivalence (an isomorphism that respects the ring structure, the scalar action, and the star involution). Given maps `f : A₁ → A₂` and `g : A₂ → A₁` that are each non-unital star `R`-algebra homomorphisms and that are two-sided inverses of each other (witnessed by explicit proofs), the constructor produces a bundled star algebra isomorphism `A₁ ≃⋆ₐ[R] A₂` whose underlying forward map is `f` and whose underlying inverse map is `g`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofNonUnitalStarAlgHom : {R : Type u_1} -> {A₁ : Type u_2} -> {A₂ : Type u_3} -> [Monoid R] -> [NonUnitalNonAssocSemiring A₁] -> [DistribMulAction R A₁] -> [Star A₁] -> [NonUnitalNonAssocSemiring A₂] -> [DistribMulAction R A₂] -> [Star A₂] -> (f : A₁ →⋆ₙₐ[R] A₂) -> (g : A₂ →⋆ₙₐ[R] A₁) -> (h₁ : g.comp f = NonUnitalStarAlgHom.id R A₁) -> (h₂ : f.comp g = NonUnitalStarAlgHom.id R A₂) -> A₁ ≃⋆ₐ[R] A₂
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `R`, `A₁`, `A₂` are respectively the scalar monoid and the two non-unital non-associative semirings carrying a distributing scalar action and a star involution. The instance arguments supply the algebraic structure on these types. The argument `f` is the forward non-unital star `R`-algebra homomorphism from `A₁` to `A₂`. The argument `g` is the proposed inverse, a non-unital star `R`-algebra homomorphism from `A₂` back to `A₁`. The proof `h₁` asserts that `g` composed with `f` equals the identity on `A₁` (i.e., `f` is a right inverse of `g` from `A₁`'s perspective). The proof `h₂` asserts that `f` composed with `g` equals the identity on `A₂` (i.e., `g` is a right inverse of `f` from `A₂`'s perspective). Together `h₁` and `h₂` certify that `f` and `g` are mutual inverses.

### Conventions

No special junk-value or edge-case conventions are declared for this constructor: it is a total function and every well-typed input satisfying the stated inverse conditions produces a well-defined star algebra equivalence.

### Worked examples

- Claim: For any non-unital star `R`-algebras `A₁` and `A₂`, if `e = VTask.ofNonUnitalStarAlgHom f g h₁ h₂`, then the underlying non-unital star algebra homomorphism of `e` equals `f`.

- Claim: For any non-unital star `R`-algebras `A₁` and `A₂`, if `e = VTask.ofNonUnitalStarAlgHom f g h₁ h₂`, then `e.symm` equals `VTask.ofNonUnitalStarAlgHom g f h₂ h₁` (i.e., swapping `f` and `g` and the two inverse proofs yields the symmetric equivalence).

- Claim: For any non-unital star `R`-algebras `A₁` and `A₂`, if `e = VTask.ofNonUnitalStarAlgHom f g h₁ h₂`, then the underlying non-unital star algebra homomorphism of `e.symm` equals `g`.

### Boundaries

- The constructor requires exactly two proofs of inverse composition; omitting or swapping them (e.g., providing `h₁` in place of `h₂`) would yield a type error, since each proof has a distinct type.
- The resulting equivalence carries the full star algebra structure: it respects addition, scalar multiplication, multiplication, and the star involution, because `f` and `g` are required to be non-unital star algebra homomorphisms.
- No unitality is assumed: the algebras need not be unital, so this is strictly more general than constructors that require unital morphisms.
- The scalar monoid `R` need not be commutative.

### Not to be confused with

- `StarAlgEquiv.ofStarAlgHom` (hypothetical unital variant): a constructor that would require unital star algebra homomorphisms; `VTask.ofNonUnitalStarAlgHom` makes no unitality assumption on `f` or `g`.
- `NonUnitalStarAlgHom.comp`: the operation of composing two non-unital star algebra homomorphisms, which appears in the inverse conditions `h₁` and `h₂` but is not itself a constructor of an equivalence.
- `StarAlgEquiv.symm`: the operation that swaps the forward and backward directions of an *existing* star algebra equivalence, as opposed to `VTask.ofNonUnitalStarAlgHom` which *constructs* a new equivalence from raw morphism data.
