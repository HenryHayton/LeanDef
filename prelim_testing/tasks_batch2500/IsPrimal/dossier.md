## Object

An element `a` of a semigroup is **primal** if, whenever `a` divides a product `b * c`, one can split `a` itself as a product `a₁ * a₂` where `a₁` divides `b` and `a₂` divides `c`. In other words, every divisibility relation `a ∣ b * c` can be "witnessed" by a factorisation of `a` that tracks the two factors of the product.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsPrimal : {α : Type u_1} -> [Semigroup α] -> (a : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsPrimal : {α : Type u_1} -> [Semigroup α] -> (a : α) -> Prop`

The implicit type argument `α` is the carrier type of the algebraic structure. The instance argument supplies the semigroup (multiplication) structure on `α`. The explicit argument `a` is the element of `α` whose primality is being asserted.

## Conventions

There are no junk-value conventions for this predicate: the definition is a universally quantified statement over all possible products `b * c` divisible by `a`, and it is well-formed for every element of every semigroup without any special-case patching.

## Worked examples

- Claim: Every prime element (in the sense of `Prime`) of a commutative monoid with zero satisfies `VTask.IsPrimal`.

- Claim: Every unit `u` (invertible element) of a semigroup with divisibility satisfies `VTask.IsPrimal u`.

- Claim: The element `0` in a commutative monoid with zero satisfies `VTask.IsPrimal 0`, because if `0 ∣ b * c` then `b * c = 0`, and one can take `a₁ = 0`, `a₂ = 1` (or `a₁ = b`, `a₂ = c` in a suitable zero-product setting) to witness the factorisation.

- Claim: If `m` and `n` are both primal elements in a cancellative commutative monoid with zero, then `m * n` is also primal.

## Boundaries

- The predicate makes sense in any semigroup; no commutativity, cancellation, or zero element is needed for the definition itself, though many useful theorems about it require stronger hypotheses.
- An element can be irreducible without being primal (in a non-UFD), but an irreducible primal element is automatically prime.
- In a UFD every irreducible (hence every prime) is primal, but primality is strictly weaker than primeness in general: units are always primal yet need not be prime.
- The definition is vacuously satisfied when `a` does not divide any product `b * c` in the ambient semigroup, though in practice every element divides at least `a * 1`.

## Not to be confused with

- `Prime`: a prime element satisfies `a ∣ b * c → a ∣ b ∨ a ∣ c`; primality asks for a *factorisation of `a`* tracking both factors, which is a different (and in general incomparable) condition.
- `Irreducible`: irreducibility says `a` cannot be written as a product of two non-units, with no direct reference to divisibility of products.
- `UniqueFactorizationMonoid` / UFD: a global property of the whole monoid, not a property of a single element.