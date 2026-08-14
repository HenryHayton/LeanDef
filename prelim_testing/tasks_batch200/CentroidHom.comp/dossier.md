## VTask.comp

### Object

The composition of two centroid homomorphisms of a non-unital, non-associative semiring. A *centroid homomorphism* on a type `α` is an additive group endomorphism that commutes with left and right multiplication by any fixed element of `α`. Given two such maps `f` and `g`, their composition `VTask.comp g f` is the centroid homomorphism whose underlying function sends every element `a` to `g(f(a))`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_5} -> [NonUnitalNonAssocSemiring α] -> (g f : CentroidHom α) -> CentroidHom α
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_5} -> [NonUnitalNonAssocSemiring α] -> (g f : CentroidHom α) -> CentroidHom α`

The implicit type argument `α` is the carrier type; the instance argument supplies the non-unital, non-associative semiring structure on `α`. The first explicit argument `g` is the outer (post-applied) centroid homomorphism, and `f` is the inner (pre-applied) centroid homomorphism. The result is the centroid homomorphism obtained by first applying `f`, then `g`.

### Conventions

Composition is written in the standard mathematical (right-to-left) order: `VTask.comp g f` applies `f` first and then `g`, matching the convention `(VTask.comp g f) a = g (f a)`. No special junk-value conventions are needed; the operation is total on all `CentroidHom α`.

### Worked examples

- Claim: For any centroid homomorphisms `g`, `f`, and element `a`, `(VTask.comp g f) a = g (f a)` (pointwise evaluation).

- Claim: Composing any centroid homomorphism `f` with the identity centroid homomorphism on the left gives back `f`; that is, `VTask.comp (CentroidHom.id α) f = f`.

- Claim: Composition is associative: for centroid homomorphisms `h`, `g`, `f`, `VTask.comp (VTask.comp h g) f = VTask.comp h (VTask.comp g f)`.

- Claim: Composing `f` with the identity centroid homomorphism on the right gives back `f`; that is, `VTask.comp f (CentroidHom.id α) = f`.

### Boundaries

- The operation is defined for all pairs of centroid homomorphisms on any type bearing a `NonUnitalNonAssocSemiring` instance; there are no inputs for which it is undefined or degenerate.
- When `f` or `g` happens to be the identity centroid homomorphism, composition returns the other map unchanged (identity laws hold on both sides).
- If `g` is injective, then `VTask.comp g f₁ = VTask.comp g f₂` implies `f₁ = f₂` (left cancellation).
- If `f` is surjective, then `VTask.comp g₁ f = VTask.comp g₂ f` implies `g₁ = g₂` (right cancellation).
- For any `T`, `S : CentroidHom α` and `a b : α`, the composed functions satisfy `(T ∘ S)(a * b) = (S ∘ T)(a * b)`, reflecting the commuting nature of centroid homomorphisms on products.

### Not to be confused with

- `AddMonoidHom.comp`: composition of plain additive monoid homomorphisms; `VTask.comp` additionally preserves the centroid homomorphism conditions (left/right multiplication compatibility).
- `CentroidHom.id`: the identity centroid homomorphism, which is the unit for `VTask.comp` on both sides, not the composition operation itself.
- Function composition `(g ∘ f)` on the underlying functions: while `⇑(VTask.comp g f) = g ∘ f` as functions, `VTask.comp g f` packages this into a full `CentroidHom` structure with the required algebraic laws.
