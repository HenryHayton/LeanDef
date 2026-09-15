## Object

`VTask.inverse` constructs a non-unital algebra homomorphism in the reverse direction from a bijective non-unital algebra homomorphism. Given a morphism `f : A →ₙₐ[R] B₁` together with a set-theoretic function `g : B₁ → A` that witnesses `f` is both left- and right-invertible, it packages `g` into a genuine non-unital algebra homomorphism `B₁ →ₙₐ[R] A`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inverse : {R : Type u} -> [Monoid R] -> {A : Type v} -> [NonUnitalNonAssocSemiring A] -> [DistribMulAction R A] -> {B₁ : Type u_2} -> [NonUnitalNonAssocSemiring B₁] -> [DistribMulAction R B₁] -> (f : A →ₙₐ[R] B₁) -> (g : B₁ → A) -> (h₁ : Function.LeftInverse g ⇑f) -> (h₂ : Function.RightInverse g ⇑f) -> B₁ →ₙₐ[R] A
<!-- PINNED-SIGNATURE:END -->


VTask.inverse : {R : Type u} -> [Monoid R] -> {A : Type v} -> [NonUnitalNonAssocSemiring A] -> [DistribMulAction R A] -> {B₁ : Type u_2} -> [NonUnitalNonAssocSemiring B₁] -> [DistribMulAction R B₁] -> (f : A →ₙₐ[R] B₁) -> (g : B₁ → A) -> (h₁ : Function.LeftInverse g ⇑f) -> (h₂ : Function.RightInverse g ⇑f) -> B₁ →ₙₐ[R] A

`R` is the scalar monoid, with `A` and `B₁` being non-unital non-associative semirings carrying a compatible distributive `R`-action. The argument `f` is the forward non-unital algebra homomorphism whose bijectivity is being inverted. The argument `g` is the bare set-theoretic inverse function. The proof `h₁` asserts that `g` is a left inverse of `f` (i.e., `g(f(a)) = a` for all `a`), and `h₂` asserts that `g` is a right inverse of `f` (i.e., `f(g(b)) = b` for all `b`). Together `h₁` and `h₂` establish that `f` is bijective and that `g` is its two-sided inverse. The result is the non-unital algebra homomorphism whose underlying map is `g`.

## Conventions

There are no junk-value or out-of-domain conventions for this construction: whenever the inputs are well-typed and the proofs `h₁`, `h₂` are supplied, the result is always a fully valid non-unital algebra homomorphism. No sentinel or degenerate fallback behaviour is involved.

## Worked examples

- Claim: For the identity morphism `f = NonUnitalAlgHom.id R A` with `g = id`, `VTask.inverse f id (fun a => rfl) (fun b => rfl)` is a non-unital algebra homomorphism from `A` to `A` whose underlying function is the identity.

- Claim: If `f : A →ₙₐ[R] B₁` is bijective with inverse function `g`, then composing the underlying function of `VTask.inverse f g h₁ h₂` with `⇑f` yields the identity on `B₁`; concretely, for any `b : B₁`, `(VTask.inverse f g h₁ h₂) (f a) = a` follows from `h₁`.

- Claim: `VTask.inverse f g h₁ h₂` preserves addition: for any `b₁ b₂ : B₁`, `VTask.inverse f g h₁ h₂ (b₁ + b₂) = VTask.inverse f g h₁ h₂ b₁ + VTask.inverse f g h₁ h₂ b₂`, since `g` inherits all homomorphism properties from `f` via the invertibility proofs.

- Claim: `VTask.inverse f g h₁ h₂` preserves scalar multiplication: for any `r : R` and `b : B₁`, `VTask.inverse f g h₁ h₂ (r • b) = r • VTask.inverse f g h₁ h₂ b`.

## Boundaries

- The function `g` itself need only be given as a bare map `B₁ → A`; the algebraic structure (preservation of addition, multiplication, and scalar action) is derived automatically from the proofs `h₁` and `h₂` together with the homomorphism properties of `f`.
- If `g` is truly a two-sided inverse of `f` but the proofs provided are for a *different* function, the result is still type-correct Lean but will not have the expected computational behaviour; the definition is not guarded against this logical misuse.
- The construction does not require `f` to be unital or associative; it works in the fully non-unital non-associative setting.
- If only a one-sided inverse were available (say only `h₁` but not `h₂`), the definition cannot be invoked, since both proofs are mandatory arguments.

## Not to be confused with

- `NonUnitalAlgHom.id`: the identity non-unital algebra homomorphism on a single type, not derived from a bijection.
- `NonUnitalAlgEquiv`: a bundled algebraic equivalence that packages both directions and the inverse proofs together as a single structure, rather than constructing only the inverse morphism from separately supplied data.
- `Function.Involutive`: a self-inverse function property, unrelated to constructing a morphism structure on an inverse.