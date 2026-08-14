## Object

`VTask.pi` constructs, from a family of ring homomorphisms each going from a common source ring `γ` into the `i`-th member `f i` of a family of rings indexed by `I`, a single ring homomorphism from `γ` into the product ring `Π i, f i`. The resulting homomorphism sends each element `x : γ` to the tuple whose `i`-th component is the image of `x` under the `i`-th homomorphism in the family.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {I : Type u} -> {f : I → Type u_1} -> {γ : Type u_2} -> [(i : I) → NonAssocSemiring (f i)] -> [NonAssocSemiring γ] -> (g : (i : I) → γ →+* f i) -> γ →+* (i : I) → f i
<!-- PINNED-SIGNATURE:END -->


`VTask.pi : {I : Type u} -> {f : I → Type u_1} -> {γ : Type u_2} -> [(i : I) → NonAssocSemiring (f i)] -> [NonAssocSemiring γ] -> (g : (i : I) → γ →+* f i) -> γ →+* (i : I) → f i`

The implicit type `I` is the index type parameterising the family. The implicit `f` is the family of types, each equipped with a `NonAssocSemiring` structure via the instance argument `[∀ i, NonAssocSemiring (f i)]`. The implicit `γ` is the common source ring, likewise equipped with `NonAssocSemiring` structure via `[NonAssocSemiring γ]`. The explicit argument `g` is the family of ring homomorphisms: for each index `i : I`, `g i` is a ring homomorphism from `γ` to `f i`.

## Conventions

There are no declared junk-value or edge conventions for this definition: it is a total construction that is well-defined for any family of ring homomorphisms, including the empty family (when `I` is uninhabited), in which case the resulting ring homomorphism targets the trivial product type `Π i : Empty, f i`.

## Worked examples

- Claim: Applying `VTask.pi` to the family consisting of the identity ring homomorphism on `ℤ` and the identity ring homomorphism on `ℤ` yields a homomorphism `ℤ →+* (Bool → ℤ)` whose value at `3` is the constant tuple `(fun _ => 3)`.

- Claim: If `g : ∀ i : Fin 2, ℤ →+* ℤ` is defined by `g 0 = RingHom.id ℤ` and `g 1 = RingHom.id ℤ`, then `VTask.pi g` applied to `x : ℤ` gives the element of `Fin 2 → ℤ` whose `0`-th and `1`-st entries are both `x`.

- Claim: For a family `g : ∀ i : I, γ →+* f i`, the composite of `VTask.pi g` with the `j`-th projection `Pi.evalRingHom f j` equals `g j`.

- Claim: When all component homomorphisms `g i` are injective and `I` is nonempty, `VTask.pi g` is injective.

## Boundaries

- When the index type `I` is empty (uninhabited), the product type `Π i, f i` has a unique element (the empty tuple), so `VTask.pi g` is the unique ring homomorphism into a one-element semiring, regardless of the family `g` (which is also vacuous).
- When `I` has exactly one element, `VTask.pi g` is essentially equivalent to `g` at that single index, up to the canonical isomorphism between a one-fold product and the factor itself.
- Injectivity of `VTask.pi g` requires `I` to be nonempty: with an empty index type, the codomain is trivial and injectivity fails unless `γ` is also trivial.
- The kernel of `VTask.pi g` equals the infimum (intersection) of the kernels of the individual homomorphisms `g i`.

## Not to be confused with

- `Pi.evalRingHom`: the projection ring homomorphism `(Π i, f i) →+* f j` going in the opposite direction — it evaluates at a fixed index, rather than assembling a family into a product map.
- `RingHom.prod`: the binary analogue that pairs two ring homomorphisms into a product of exactly two rings; `VTask.pi` generalises this to an arbitrary index type.
- `NonUnitalRingHom.pi`: the analogous construction for non-unital ring homomorphisms, which does not require the unit-preservation axiom.