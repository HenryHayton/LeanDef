## Object

`VTask.starCenterIsoCentroid` is the canonical star-ring isomorphism between two naturally associated algebraic objects attached to a non-associative semiring `α` equipped with a star: the *star-center* (the center of `α` viewed as a star-subring) and the *centroid* of `α` (the ring of "left-and-right multiplication" operators on `α` that commute with the ring operations). The isomorphism sends a central element `z` to the map `x ↦ z * x` (equivalently `x ↦ x * z`, since `z` is central), and its inverse recovers a central element from a centroid homomorphism `T` by evaluating `T` at `1`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.starCenterIsoCentroid : {α : Type u_1} -> [NonAssocSemiring α] -> [StarRing α] -> ↥(StarSubsemiring.center α) ≃⋆+* CentroidHom α
<!-- PINNED-SIGNATURE:END -->


`VTask.starCenterIsoCentroid : ↥(StarSubsemiring.center α) ≃⋆+* CentroidHom α`

The ambient type `α` is implicit; it is a non-associative semiring carrying a star. No explicit arguments are required: the isomorphism is a single bundled value (a term of type `StarSubsemiring.center α ≃⋆+* CentroidHom α`) that lives in the universe of `α`.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a bundled isomorphism between two algebraic structures and is defined without case analysis on any input.

## Worked examples

- Claim: For any element `z` in the star-center, `VTask.starCenterIsoCentroid z` equals `VTask.starCenterToCentroid z` (i.e., the forward map agrees with the underlying additive-star-ring homomorphism).

- Claim: For any centroid homomorphism `T : CentroidHom α`, the underlying element of `α` recovered by `VTask.starCenterIsoCentroid.symm T` is `T 1` (evaluation at the multiplicative identity).

- Claim: `VTask.starCenterIsoCentroid` is an isomorphism, so composing it with its inverse gives the identity on `StarSubsemiring.center α`.

## Boundaries

- The isomorphism requires `α` to be a *non-associative semiring* with a star; associativity is not assumed. The construction is still well-defined because central elements act as centroid homomorphisms even without associativity.
- The inverse map `T ↦ T 1` is well-defined precisely because `α` has a multiplicative identity `1`; the underlying type is `NonAssocSemiring`, which does include `1`.
- Because the isomorphism is bundled as a `≃⋆+*`, it simultaneously witnesses: (a) a bijection of underlying sets, (b) preservation of the ring operations, and (c) preservation of the star. All three are part of the single object.
- There are no restrictions on the cardinality or commutativity of `α` beyond what `NonAssocSemiring` and `StarRing` demand.

## Not to be confused with

- `VTask.starCenterToCentroid`: the underlying one-directional star-ring homomorphism from the center to the centroid; `VTask.starCenterIsoCentroid` is strictly stronger, carrying the inverse and the proof of bijectivity.
- `CentroidHom α`: the *codomain* ring of centroid endomorphisms; not itself a center or a subring of `α`.
- `StarSubsemiring.center α`: the *domain* star-subring of central elements; `VTask.starCenterIsoCentroid` relates it to the centroid but is not the same object as the center itself.