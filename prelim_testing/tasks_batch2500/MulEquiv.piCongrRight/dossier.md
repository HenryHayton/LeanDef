## Object

`VTask.piCongrRight` constructs a multiplicative equivalence (isomorphism of types equipped with a binary multiplication) between two dependent product types, given a pointwise family of multiplicative equivalences. Concretely, if for each index `j` in an index type `η` there is a multiplicative equivalence `Ms j ≃* Ns j`, then the function types `(∀ j, Ms j)` and `(∀ j, Ns j)` are themselves multiplicatively equivalent, where multiplication on each dependent product is defined pointwise.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piCongrRight : {η : Type u_16} -> {Ms : η → Type u_17} -> {Ns : η → Type u_18} -> [(j : η) → Mul (Ms j)] -> [(j : η) → Mul (Ns j)] -> (es : (j : η) → Ms j ≃* Ns j) -> ((j : η) → Ms j) ≃* ((j : η) → Ns j)
<!-- PINNED-SIGNATURE:END -->


`VTask.piCongrRight : {η : Type u_16} -> {Ms : η → Type u_17} -> {Ns : η → Type u_18} -> [(j : η) → Mul (Ms j)] -> [(j : η) → Mul (Ns j)] -> (es : (j : η) → Ms j ≃* Ns j) -> ((j : η) → Ms j) ≃* ((j : η) → Ns j)`

The implicit type `η` is the index type ranging over the family. The implicit dependent functions `Ms` and `Ns` assign a type to each index, with `Ms j` being the domain type at index `j` and `Ns j` being the codomain type at index `j`. The two instance arguments supply the pointwise `Mul` structure on the dependent products `(∀ j, Ms j)` and `(∀ j, Ns j)` respectively. The explicit argument `es` is the family of multiplicative equivalences: for each index `j`, `es j` is a multiplicative equivalence `Ms j ≃* Ns j`.

## Conventions

The forward map of the resulting equivalence acts pointwise: applied to a function `x : ∀ j, Ms j`, it returns the function sending each `j` to `(es j) (x j)`. The inverse map also acts pointwise via the pointwise inverses `(es j).symm`. There are no junk-value conventions to declare for this definition, since it is a total construction on well-typed inputs with no degenerate cases.

## Worked examples

- Claim: For a single-element index type `Unit` and `es : Unit → ℕ ≃* ℕ` consisting of the identity equivalences, `VTask.piCongrRight es` is the identity multiplicative equivalence on `Unit → ℕ`.

- Claim: The symmetry of `VTask.piCongrRight es` equals `VTask.piCongrRight (fun i => (es i).symm)`, meaning inverting the whole equivalence corresponds to inverting each component equivalence pointwise.

- Claim: The composition `(VTask.piCongrRight es).trans (VTask.piCongrRight fs)` equals `VTask.piCongrRight (fun i => (es i).trans (fs i))`, so composing two pointwise-lifted equivalences is the same as lifting the pointwise compositions.

- Claim: If all component equivalences `es j` are the identity `MulEquiv.refl (Ms j)`, then `VTask.piCongrRight (fun j => MulEquiv.refl (Ms j))` equals `MulEquiv.refl (∀ j, Ms j)`.

## Boundaries

- When `η` is empty (`PEmpty` or a type with no inhabitants), the dependent product `∀ j, Ms j` is a one-element type and the resulting equivalence is the unique equivalence between two such trivially equal types; the construction remains valid and trivial.
- When `η` is a `Unit` type, the construction reduces to a single multiplicative equivalence lifted to function types, behaving identically to wrapping a single `MulEquiv`.
- When all `es j` are the identity equivalences `MulEquiv.refl (Ms j)`, the result is the identity multiplicative equivalence on `∀ j, Ms j`.
- The construction is fully coherent with symmetry and transitivity: the symmetry of the lifted equivalence is the lift of the pointwise symmetries, and the transitivity of two lifted equivalences is the lift of the pointwise transitions.

## Not to be confused with

- `Equiv.piCongrRight`: the underlying set-theoretic (non-multiplicative) version that only tracks the bijection, without the `map_mul` property.
- `MulEquiv.arrowCongr`: the non-dependent version for function types `α → β` where the domain is not indexed, i.e., both source and target of the equivalence are non-dependent arrow types.
- `AddEquiv.piCongrRight`: the additive analogue of this construction, where `Mul` is replaced by `Add` and `MulEquiv` by `AddEquiv`; despite the docstring reference, this definition is the *multiplicative* version.