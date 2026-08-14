## Object

`VTask.CovBy a b` is the proposition that `b` *covers* `a` in a type equipped with a strict order. This means two things simultaneously: `a` is strictly less than `b`, and there is no element strictly between them — i.e., no `c` with `a < c < b`. The covering relation is the order-theoretic notion of an "immediate successor" without any intervening element, commonly written `a ⋖ b`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.CovBy : {α : Type u_2} -> [LT α] -> (a b : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.CovBy : {α : Type u_2} -> [LT α] -> (a b : α) -> Prop`

The implicit type argument `α` is the carrier type of the ordered structure. The instance argument supplies the strict less-than relation on `α`. The explicit argument `a` is the element being covered (the smaller one), and `b` is the covering element (the larger one). The result is a proposition asserting that `b` immediately covers `a`.

## Conventions

There are no special junk-value or boundary conventions declared for this definition: it is a universally-quantified proposition over any type with a `LT` instance, and it holds or fails on its own logical merits for every pair `(a, b)`.

## Worked examples

- Claim: In the natural numbers, `VTask.CovBy 3 4` holds — 4 immediately covers 3 because there is no natural number strictly between 3 and 4.

- Claim: In the natural numbers, `VTask.CovBy 3 5` does not hold — 5 does not cover 3 because 4 lies strictly between them, violating the gap condition.

- Claim: In the integers ordered by divisibility (if it were a `LT` instance), two elements satisfying the covering relation would have no divisor strictly in between; in the linear integer order, `VTask.CovBy n (n+1)` holds for every integer `n`.

- Claim: `VTask.CovBy a a` is always false for any `a`, since it requires `a < a`, which is impossible in any irreflexive order.

## Boundaries

- The definition requires only a `LT` instance, not a full partial order or linear order; in particular, antisymmetry and transitivity are not assumed.
- If `α` has the discrete order (where `a < b` holds for no pair), then `VTask.CovBy a b` is vacuously false for all `a, b`.
- If `α` has a dense linear order (such as the rationals or reals), then `VTask.CovBy a b` is false for every pair `a, b`, since between any two distinct elements there is always another.
- The proposition is not reflexive: `VTask.CovBy a a` always fails.
- The proposition is not in general transitive: if `b` covers `a` and `c` covers `b`, then `c` does not cover `a` (since `b` lies strictly between them).
- The open interval `Ioo a b` is empty if and only if `VTask.CovBy a b` holds (given `a < b`).

## Not to be confused with

- `WCovBy a b` (weak covering, `a ⩿ b`): allows `a = b`; it is the reflexive closure of the covering relation and holds when either `a = b` or `b` strictly covers `a`.
- `a < b` (strict inequality alone): weaker than covering — it only requires `a` to be less than `b` without the gap condition.
- `a ≤ b` (non-strict inequality): even weaker, allowing equality and intermediate elements.