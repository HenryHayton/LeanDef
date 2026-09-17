## Object

Given a partial value `a : Part α` (an element of the "partial type" over `α`, which either contains a definite value or is undefined), `VTask.getOrElse` extracts that value when it exists, and falls back to a caller-supplied default value `d : α` when `a` is undefined. It is the standard "maybe-get-with-default" operation lifted to the `Part` type.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.getOrElse : {α : Type u_1} -> (a : Part α) -> [Decidable a.Dom] -> (d : α) -> α
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> (a : Part α) -> [Decidable a.Dom] -> (d : α) -> α`

The implicit type argument `α` is the carrier type of the partial value. The argument `a` is the partial value being interrogated — it may or may not have a defined underlying element. The instance argument `[Decidable a.Dom]` supplies the computational evidence that membership in `a`'s domain can be decided; without this, the function cannot branch on whether `a` is defined. The argument `d` is the default value returned when `a` is undefined.

## Conventions

When `a` is the everywhere-undefined partial value (`Part.none`), its domain is empty and the result is always `d`. When `a = Part.some v` for some `v : α`, its domain is a singleton (trivially decidable) and the result is `v`, regardless of `d`.

## Worked examples

- Claim: `VTask.getOrElse Part.none 42 = 42`
  ```lean
  example : VTask.getOrElse Part.none 42 = 42 := by decide
  ```

- Claim: `VTask.getOrElse (Part.some 7) 42 = 7`
  ```lean
  example : VTask.getOrElse (Part.some 7) 42 = 7 := by decide
  ```

- Claim: For any `v d : α`, `VTask.getOrElse (Part.some v) d = v` (the default is ignored when the part is defined).

- Claim: For any `d : α`, `VTask.getOrElse Part.none d = d` (the default is returned when the part is undefined).

## Boundaries

- **Defined part**: When `a.Dom` holds (i.e., `a` has a value), the result equals `a.get h` for any proof `h : a.Dom`. The default `d` plays no role and is discarded.
- **Undefined part**: When `a.Dom` is empty (e.g., `Part.none`), the result is exactly `d`.
- **Decidability requirement**: The function is only usable computationally when a `Decidable a.Dom` instance is available. For `Part.none` and `Part.some v` this instance is always synthesised automatically. For more exotic `Part` constructions (defined via existential propositions), one must supply the instance manually.
- **No junk values**: The function is total on all inputs satisfying the instance constraint; it never fails or produces an arbitrary element.

## Not to be confused with

- `Part.get`: Extracts the value from a `Part` but requires the caller to *prove* the domain condition holds; it has no default and does not compile without that proof.
- `Part.elim`: A more general eliminator that maps both the defined and undefined cases to an output type, accepting two continuation arguments rather than a single default value.
- `Option.getD` / `Option.getOrElse`: The analogous operation on `Option α`; `Part` is strictly more general than `Option` because its domain can be an arbitrary proposition rather than just `True`/`False`.