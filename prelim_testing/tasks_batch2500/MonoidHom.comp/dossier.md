## Object

`VTask.comp` constructs the composite of two monoid homomorphisms. Given a homomorphism `hmn : M →* N` and a homomorphism `hnp : N →* P`, it produces a new monoid homomorphism `M →* P` whose underlying function sends each element `x : M` to `hnp(hmn(x))`. The composite automatically inherits the homomorphism properties: it preserves the identity element and respects multiplication.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {M : Type u_4} -> {N : Type u_5} -> {P : Type u_6} -> [MulOne M] -> [MulOne N] -> [MulOne P] -> (hnp : N →* P) -> (hmn : M →* N) -> M →* P
<!-- PINNED-SIGNATURE:END -->


`{M : Type u_4} -> {N : Type u_5} -> {P : Type u_6} -> [MulOne M] -> [MulOne N] -> [MulOne P] -> (hnp : N →* P) -> (hmn : M →* N) -> M →* P`

The three implicit type arguments `M`, `N`, and `P` are the source, intermediate, and target types, each equipped with a `MulOne` instance (providing a multiplication and an identity element). The instance arguments `[MulOne M]`, `[MulOne N]`, and `[MulOne P]` supply the monoid structure on each type. The first explicit argument `hnp` is the homomorphism from the intermediate monoid `N` to the target monoid `P`. The second explicit argument `hmn` is the homomorphism from the source monoid `M` to the intermediate monoid `N`. The result is the composite monoid homomorphism from `M` to `P`.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total construction on well-typed inputs and produces a fully valid monoid homomorphism in all cases.

## Worked examples

- Claim: Composing the identity homomorphism on `ℕ` (multiplicative) with itself yields a morphism that maps each element to itself.

- Claim: For the trivial monoid homomorphism sending every element to `1` in `P`, composing it with any `hmn : M →* N` still sends every element to `1`.

- Claim: `VTask.comp hnp hmn` applied to the identity element `1 : M` gives `1 : P`, since both `hmn` and `hnp` preserve the identity.

- Claim: If `f : ℕ →* ℕ` and `g : ℕ →* ℕ` are both the identity homomorphism, then `(VTask.comp f g) 3 = 3`.
  ```lean
  example : (VTask.comp (MonoidHom.id ℕ) (MonoidHom.id ℕ)) 3 = 3 := by decide
  ```

## Boundaries

- The construction is entirely well-defined regardless of the sizes or natures of `M`, `N`, and `P`; there are no exceptional inputs.
- If either `hmn` or `hnp` is the identity homomorphism on its respective type, the composite is (propositionally) equal to the other factor.
- If `hmn` and `hnp` are both the trivial (constant-one) homomorphism, the composite is also the trivial homomorphism.
- Composition is associative: composing three homomorphisms in either association order yields propositionally equal results.

## Not to be confused with

- `MonoidHom.id`: the identity homomorphism on a single monoid, not a composition of two morphisms.
- Function composition (`Function.comp`): composes bare functions without packaging the result as a monoid homomorphism or verifying any algebraic laws.
- `AddMonoidHom.comp`: the additive analogue, composing additive monoid homomorphisms; structurally identical but for additive (rather than multiplicative) monoids.