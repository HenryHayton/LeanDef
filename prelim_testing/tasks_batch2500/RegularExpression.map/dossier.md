## Object

`VTask.map` applies a function on alphabet symbols throughout a regular expression, producing a new regular expression over a (possibly different) alphabet. Every constructor of the regular expression is visited recursively, and each atomic symbol `a` appearing in a `char` node is replaced by `f a`. The structural shape of the expression — choices, concatenations, stars, empty/unit constants — is left entirely unchanged.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> RegularExpression α → RegularExpression β
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> RegularExpression α → RegularExpression β`

The implicit type arguments `α` and `β` are the source and target alphabets. The explicit argument `f` is the function to apply to each symbol in the expression. The final argument is the regular expression over `α` to be transformed.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total structural recursion over all six constructors of `RegularExpression`, and every case is handled in a natural and lossless way.

## Worked examples

- Claim: Mapping any function over the zero (empty language) expression returns zero.
  ```lean
  example (f : Nat → Nat) : (VTask.map f 0) = 0 := by rfl
  ```

- Claim: Mapping any function over the one (empty-word) expression returns one.
  ```lean
  example (f : Nat → Nat) : (VTask.map f 1) = 1 := by rfl
  ```

- Claim: Mapping `f` over `char a` gives `char (f a)`.
  ```lean
  example (f : Nat → Nat) (a : Nat) : VTask.map f (RegularExpression.char a) = RegularExpression.char (f a) := by rfl
  ```

- Claim: Composing two maps equals mapping the composed function — i.e., `(P.map f).map g = P.map (g ∘ f)` for all `P`.

- Claim: Mapping `id` over any regular expression is the identity — i.e., `P.map id = P` for all `P`.

- Claim: The language matched by `P.map f` equals the image of the language matched by `P` under the induced word-level map of `f`.

## Boundaries

- The zero constructor (`0`, representing the empty language) is a fixed point: `map f 0 = 0`.
- The one constructor (`1`, representing the singleton language `{ε}`) is a fixed point: `map f 1 = 1`.
- When `f = id`, the map is the identity on all regular expressions.
- When `f` is not injective, distinct symbols in the source expression may collapse to the same symbol in the result, potentially enlarging the matched language.
- When `f` is not surjective, the image expression only uses symbols in the image of `f`.
- The star, union, and concatenation constructors distribute through the map structurally, preserving nesting depth and shape.

## Not to be confused with

- `RegularExpression.matches'`: the function that computes the *language* (set of words) accepted by a regular expression — a semantic notion, whereas `VTask.map` is a purely syntactic transformation.
- `Language.map`: the map operation on languages (sets of words) induced by a symbol function — `VTask.map` lifts this to regular expressions, and `matches'_map` asserts they commute.
- `RegularExpression.star`: the Kleene-star constructor — easily confused because `map f (star R) = star (map f R)`, but `star` alone does not apply any alphabet function.