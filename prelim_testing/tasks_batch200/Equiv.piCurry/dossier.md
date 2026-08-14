## Object

`VTask.piCurry` is a canonical equivalence (a bijection with explicit inverse) between two types of dependent functions:

- The **source** type is the type of dependent functions whose domain is a sigma-type `Σ i, β i` (i.e., dependent pairs), mapping each such pair `⟨i, b⟩` to a value in `γ i b`.
- The **target** type is the type of iterated dependent functions: first take an index `a : α`, then a fiber element `b : β a`, and return a value in `γ a b`.

Informally, this is the dependent-type analogue of the classical fact that a function on a product (or here, sigma-type) is the same as a curried function of two arguments. The forward direction is "currying" (splitting a single pair-argument into two separate arguments), and the backward direction is "uncurrying" (combining two separate arguments into one pair).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piCurry : {α : Type u_11} -> {β : α → Type u_9} -> (γ : (a : α) → β a → Type u_10) -> ((x : (i : α) × β i) → γ x.fst x.snd) ≃ ((a : α) → (b : β a) → γ a b)
<!-- PINNED-SIGNATURE:END -->


`VTask.piCurry : {α : Type u_11} -> {β : α → Type u_9} -> (γ : (a : α) → β a → Type u_10) -> ((x : (i : α) × β i) → γ x.fst x.snd) ≃ ((a : α) → (b : β a) → γ a b)`

- `α` is the base type, serving as the index set for the sigma-type and the first argument of the curried functions.
- `β` is a type family over `α`, assigning to each index `a : α` the fiber type `β a`; together with `α` it forms the sigma-type `Σ i, β i`.
- `γ` is the dependent return-type family: for each `a : α` and each `b : β a`, `γ a b` is the type of values to be produced. It determines what both function spaces map into.

The result is a bundled `Equiv` (an explicit, invertible map) between the two dependent function types.

## Conventions

No junk-value or edge-case conventions are declared: `VTask.piCurry` is a total equivalence of types, defined for all choices of `α`, `β`, and `γ`, including when `α` is empty, when any fiber `β a` is empty, or when `γ a b` is a proposition. The bijection is well-defined in all these cases.

## Worked examples

- Claim: For constant families, `VTask.piCurry (fun _ _ => Nat)` is an equivalence between `(Σ i : Bool, Fin 2) → ℕ` and `(a : Bool) → (Fin 2) → ℕ`.

- Claim: The forward direction of `VTask.piCurry (fun (a : Unit) (_ : Unit) => ℕ)` maps the function `fun ⟨(), ()⟩ => 42` to the iterated function `fun () () => 42`.

- Claim: Applying `VTask.piCurry` to a sigma-type with empty base type `α = Empty` yields an equivalence between the two (both singleton, by vacuity) dependent function types.

- Claim: The inverse (`symm`) of `VTask.piCurry γ` applied to a curried function `f` and then re-applied to `VTask.piCurry γ` recovers `f`; that is, `(VTask.piCurry γ).symm` is a left inverse to `(VTask.piCurry γ)`, witnessing the `left_inv` condition.

## Boundaries

- When `α` is the empty type, both function types are singletons (there is exactly one dependent function out of each), and the equivalence maps the unique element on one side to the unique element on the other side.
- When some fiber `β a` is empty, functions in the source type need not return a value for pairs `⟨a, _⟩` (none exist), and correspondingly in the curried form the function `f a` is a function from an empty type, which is vacuously anything. The equivalence remains valid.
- When `γ a b` is a `Prop` for all `a` and `b`, the equivalence specialises to one between two types of proofs/propositions; all the same structural properties hold.
- The equivalence is strict: both the forward and backward maps are definitionally computable, not merely propositionally invertible.

## Not to be confused with

- `Equiv.curry` (non-dependent): the analogous equivalence for ordinary (non-dependent) function types `(α × β → γ) ≃ (α → β → γ)`, which uses a product type in the domain rather than a sigma-type.
- `Sigma.curry` / `Sigma.uncurry`: the raw forward and backward functions underlying `VTask.piCurry`, without the bundled `Equiv` structure (no proof that they are mutually inverse is packaged with them).
- `Equiv.piCongrLeft` / `Equiv.piCongrRight`: related equivalences that rearrange the domain or codomain of a pi-type using a given equivalence of types, rather than currying a sigma-domain.