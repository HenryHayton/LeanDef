## 1. Object

A function `f : α → β` (where both types carry a negation operation) is called **odd** if negating the input always negates the output: `f(-x) = -f(x)` for every element `x` of the domain. This is the functional analogue of an odd function in classical real analysis (e.g., `sin`, `x ↦ x³`).

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Odd : {α : Type u_1} -> {β : Type u_2} -> [Neg α] -> [Neg β] -> (f : α → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Odd : {α : Type u_1} -> {β : Type u_2} -> [Neg α] -> [Neg β] -> (f : α → β) -> Prop`

The two universe-polymorphic type arguments `α` and `β` are the domain and codomain of the function; they are inferred implicitly. The two instance arguments supply negation operations on `α` and `β` respectively — negation on the domain is needed to form `-x`, and negation on the codomain is needed to form `-f(x)`. The explicit argument `f` is the function whose oddness is being asserted.

## 3. Conventions

The property is a universally quantified proposition with no junk values or out-of-domain inputs; it is total and well-formed for any choice of `α`, `β`, and `f`.

## 4. Worked examples

- Claim: The constant zero function `fun (_ : ℤ) ↦ (0 : ℤ)` satisfies `VTask.Odd`.

- Claim: The identity function `fun (x : ℤ) ↦ x` satisfies `VTask.Odd`, since `-(−x) = x = −(−x)` ... wait, the identity gives `f(-x) = -x` and `-f(x) = -x`, so indeed `f(-x) = -f(x)` for all `x`.

- Claim: The function `fun (x : ℤ) ↦ 2 * x` satisfies `VTask.Odd`, because `2 * (-x) = -(2 * x)` for all integers `x`.

- Claim: The product of two odd functions (when the codomain has a compatible negation and multiplication) is even, not odd; concretely, if `f` and `g` are both `VTask.Odd`, then `f * g` satisfies `VTask.Even`.

- Claim: If `f : α → β` and `g : β → γ` are both odd (with appropriate negation instances), then `g ∘ f` is also odd.

## 5. Boundaries

- **Zero function**: When the codomain is a `NegZeroClass`, the constant zero function is odd, since `0 = -0`.
- **Map at zero**: If the domain has a `NegZeroClass` structure (so `-0 = 0`), any odd function must satisfy `f(0) = 0`, because `f(0) = f(-0) = -f(0)` forces `f(0) = 0` in an additive group.
- **Finite symmetric domains**: On a `Fintype` with an involutive negation, an odd function sums to zero over the entire type.
- **Composition**: Odd ∘ Odd = Odd; Even ∘ Odd = Even.
- **Products**: Odd × Odd = Even (pointwise product); Even × Odd = Odd.

## 6. Not to be confused with

- **`Odd : ℕ → Prop` (the number-theoretic predicate)**: asserts that a natural number is not divisible by 2; entirely unrelated to this functional notion.
- **`VTask.Even` (even functions)**: the companion property `f(-x) = f(x)`; differs by the sign on the right-hand side.
- **`Function.Injective` / `Function.Surjective`**: structural properties of functions that say nothing about interaction with negation.