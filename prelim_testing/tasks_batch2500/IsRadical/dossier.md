## Object

An element `y` of a type `R` (equipped with divisibility and natural-number powers) is called **radical** if it satisfies the following absorption property: whenever `y` divides some power `xⁿ` of an element `x`, then `y` already divides `x` itself. Intuitively, `y` cannot be "created" by repeated multiplication; any prime-like divisibility behaviour is already witnessed at the first level.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsRadical : {R : Type u_1} -> [Dvd R] -> [Pow R ℕ] -> (y : R) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsRadical : {R : Type u_1} -> [Dvd R] -> [Pow R ℕ] -> (y : R) -> Prop`

The implicit type argument `R` is the carrier type on which divisibility and powers are defined. The two instance arguments supply the divisibility relation on `R` and the operation of raising elements of `R` to natural-number exponents. The explicit argument `y` is the element of `R` being tested for the radical property.

## Conventions

The natural number `n` in the universal quantification ranges over all of `ℕ`, including `0`. When `n = 0`, the condition `y ∣ x ^ 0` may be vacuously satisfied or not depending on what `x ^ 0` evaluates to in `R`; the definition makes no special exception for this case.

## Worked examples

- Claim: In ℤ, the element `1` satisfies `VTask.IsRadical 1` because `1` divides every integer, hence in particular divides `x` whenever it divides any power of `x`.

- Claim: In ℤ, a squarefree integer (e.g., `6 = 2 · 3`) satisfies `VTask.IsRadical 6`. If `6 ∣ xⁿ` for some `n ≥ 1`, then both `2` and `3` divide `xⁿ`, and since they are prime they divide `x`, so `6 ∣ x`.

- Claim: In ℤ, the element `4` does **not** satisfy `VTask.IsRadical 4`: taking `x = 2` and `n = 2` gives `4 ∣ 2² = 4`, yet `4 ∤ 2`, so the condition fails.

- Claim: Every prime ideal `I` in a commutative ring satisfies `VTask.IsRadical I` (the ideal-level version of this predicate), which reflects the usual fact that prime ideals are radical.

## Boundaries

- When `n = 0`: the hypothesis `y ∣ x ^ 0` may hold for all `x` (if `x ^ 0` is the multiplicative identity and `y` divides it), potentially placing a non-trivial constraint on `y` regardless of `x`.
- The definition is stated for any type with `Dvd` and `Pow R ℕ`; it does not require `R` to be a ring, a monoid, or even to have a multiplicative identity. In very sparse algebraic structures, some of the expected implications may hold vacuously.
- Squarefree elements are radical (in integral domains or GCD domains), and conversely a nonzero radical element is squarefree in such settings.
- The zero element and the unit element can each be radical or not depending on the ambient structure.

## Not to be confused with

- **`Ideal.radical`**: The *radical of an ideal*, which produces the ideal consisting of all elements some power of which lies in the given ideal; this is a construction, not the predicate tested here.
- **`Squarefree`**: The property that an element has no repeated non-unit factors; closely related (squarefree implies radical, and radical implies squarefree for nonzero elements in suitable domains) but defined differently and applicable in a wider range of contexts under `VTask.IsRadical`.
- **`IsPrime`**: The property that an element is prime (i.e., if it divides a product it divides one of the factors); prime elements are radical, but radical elements need not be prime.
