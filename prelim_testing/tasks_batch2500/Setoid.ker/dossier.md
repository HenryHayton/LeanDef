## Object

`VTask.ker f` is the **kernel** of a function `f : α → β`, packaged as a `Setoid` on `α`. Two elements `a₁, a₂ : α` are related by this setoid if and only if `f a₁ = f a₂`; i.e., they are indistinguishable under `f`. The resulting structure includes both the binary relation and the proof that it is an equivalence relation (reflexivity, symmetry, and transitivity all follow immediately from equality in `β`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ker : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> Setoid α
<!-- PINNED-SIGNATURE:END -->


`VTask.ker : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> Setoid α`

The type parameters `α` and `β` are implicit: `α` is the domain type on which the setoid is constructed, and `β` is the codomain type whose equality structure induces the relation. The explicit argument `f` is the function whose fibres (preimages of single points) define the equivalence classes.

## Conventions

There are no junk-value conventions for this definition: it is a total function defined for every choice of types `α`, `β`, and function `f : α → β`.

## Worked examples

- Claim: For `f : Bool → Bool` equal to `id`, every element is related only to itself under `VTask.ker f`, since `id b₁ = id b₂` iff `b₁ = b₂`.

- Claim: For the constant function `f : Bool → Unit` (sending everything to `()`), all elements of `Bool` are related to each other under `VTask.ker f`, because `f true = f false = ()`.
  ```lean
  example : (VTask.ker (fun _ : Bool => ())).r true false := by
    show (fun _ : Bool => ()) true = (fun _ : Bool => ()) false
    rfl
  ```

- Claim: For `f : Fin 2 → Fin 2` equal to `id`, `VTask.ker f` relates `0` to `0` (reflexivity).
  ```lean
  example : (VTask.ker (id : Fin 2 → Fin 2)).r 0 0 := by
    show id (0 : Fin 2) = id (0 : Fin 2)
    rfl
  ```

- Claim: For `f : Fin 2 → Fin 2` equal to `id`, `VTask.ker f` does **not** relate `0` to `1`.
  ```lean
  example : ¬ (VTask.ker (id : Fin 2 → Fin 2)).r 0 1 := by
    show ¬ id (0 : Fin 2) = id (1 : Fin 2)
    decide
  ```

## Boundaries

- **Empty domain**: When `α` is empty (e.g., `α = Empty`), the setoid is vacuously well-defined; the relation holds for no pair of inputs.
- **Constant function**: When `f` is constant, all elements of `α` are equivalent, yielding the indiscrete (coarsest) setoid on `α`.
- **Identity or injective function**: When `f` is injective, the kernel is the discrete (finest) setoid on `α`, relating each element only to itself.
- **Surjectivity of `f`** has no effect on `VTask.ker f`; only injectivity matters for the coarseness of the resulting setoid.

## Not to be confused with

- **`Setoid.quotient` / quotient type**: The quotient `Quotient (VTask.ker f)` is the set of fibres of `f`, distinct from the setoid itself.
- **The algebraic kernel** (e.g., kernel of a group homomorphism): That is the preimage of the identity element, a subgroup — not an equivalence relation on the domain.
- **`Function.Injective`**: States that the kernel setoid is discrete, but is a proposition, not the setoid structure itself.