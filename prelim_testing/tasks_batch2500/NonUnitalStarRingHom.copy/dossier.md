## Object

`VTask.copy` constructs a non-unital star ring homomorphism from `A` to `B` that is definitionally equal to a given one, but whose underlying function is replaced by a (provably equal) alternative function `f'`. This is a bookkeeping device: the resulting morphism carries all the same algebraic properties as the original, but because its `toFun` field is literally `f'` rather than the coercion of `f`, Lean's definitional equality checker can more easily recognise it in contexts where `f'` appears.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {A : Type u_1} -> {B : Type u_2} -> [NonUnitalNonAssocSemiring A] -> [Star A] -> [NonUnitalNonAssocSemiring B] -> [Star B] -> (f : A →⋆ₙ+* B) -> (f' : A → B) -> (h : f' = ⇑f) -> A →⋆ₙ+* B
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {A : Type u_1} -> {B : Type u_2} -> [NonUnitalNonAssocSemiring A] -> [Star A] -> [NonUnitalNonAssocSemiring B] -> [Star B] -> (f : A →⋆ₙ+* B) -> (f' : A → B) -> (h : f' = ⇑f) -> A →⋆ₙ+* B`

The implicit type arguments `A` and `B` are the source and target types, each carrying their respective semiring and star structures via instance arguments. The argument `f` is the original non-unital star ring homomorphism being copied. The argument `f'` is the new bare function that will serve as the underlying map of the result; it must map from `A` to `B`. The proof `h` witnesses that `f'` is pointwise equal to the coercion of `f` to a plain function, ensuring all algebraic axioms can be transferred.

## Conventions

There are no junk-value or edge-case conventions for this definition: it is a total constructor taking structurally valid inputs, and the proof obligation `h` fully constrains `f'` to agree with `f` everywhere, leaving no room for degenerate or undefined behaviour.

## Worked examples

- Claim: For any non-unital star ring homomorphism `f : A →⋆ₙ+* B`, copying it with its own coercion and the reflexivity proof yields a morphism whose underlying function is the coercion of `f`.

- Claim: The copied morphism `VTask.copy f f' h` is equal (as a non-unital star ring homomorphism) to the original `f`, regardless of the choice of equal representative `f'`. This follows from `coe_copy` and `copy_eq`.

- Claim: The coercion of `VTask.copy f f' h` to a bare function equals `f'` exactly (not merely pointwise, but definitionally), which is the primary reason this constructor is useful for fixing definitional equalities.

- Claim: If `f' = ⇑f`, then for every `a : A`, `(VTask.copy f f' h) a = f' a` holds by definition of the copied morphism.

## Boundaries

- The proof `h` must be an exact equality `f' = ⇑f` (not merely pointwise); the definition requires this as a propositional equality of functions.
- If `f'` is taken to be exactly `⇑f` and `h` is `rfl`, the copy is indistinguishable from `f` in every respect, and `copy_eq` confirms the two are equal as structured morphisms.
- The definition is total: there are no restrictions on `A`, `B`, `f`, or `f'` beyond those expressed in the type signature.
- Preservation of all four homomorphism axioms (zero, addition, multiplication, star) is guaranteed by transporting them along `h`, so the copy is a fully valid non-unital star ring homomorphism.

## Not to be confused with

- `NonUnitalStarRingHom.mk` — the raw constructor for a non-unital star ring homomorphism from scratch, requiring independent proofs of all axioms rather than copying from an existing morphism.
- `StarRingHom.copy` — the analogous copy constructor for *unital* star ring homomorphisms (`A →⋆+* B`), which additionally requires preservation of the multiplicative identity.
- `NonUnitalRingHom.copy` — the copy constructor for non-unital ring homomorphisms without the star structure, lacking the `map_star'` field.
