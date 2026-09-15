## VTask.IncompRel

### Object

The incomparability relation with respect to a binary relation `r` on a type `α`. Two elements `a` and `b` are *incomparable under `r`* when neither `r a b` nor `r b a` holds — that is, the relation `r` places no order between them in either direction. This is the standard notion of incomparability in the theory of partial orders and preorders, but it is defined for any binary relation.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IncompRel : {α : Type u_1} -> (r : α → α → Prop) -> (a b : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IncompRel : {α : Type u_1} -> (r : α → α → Prop) -> (a b : α) -> Prop`

The implicit type argument `α` is the carrier type whose elements are being compared. The argument `r` is the binary relation with respect to which incomparability is measured. The arguments `a` and `b` are the two elements whose comparability under `r` is in question.

### Conventions

No special junk-value or out-of-domain conventions are declared: the relation is defined for every binary relation `r` and every pair of elements, with no restrictions whatsoever.

### Worked examples

- Claim: For the usual `≤` on natural numbers, `VTask.IncompRel (· ≤ ·) 2 3` does **not** hold, because `2 ≤ 3`.

- Claim: For the strict less-than relation `<` on natural numbers, `VTask.IncompRel (· < ·) 3 3` holds, because neither `3 < 3` nor `3 < 3` (i.e., `¬ 3 < 3` and `¬ 3 < 3`).

- Claim: `VTask.IncompRel (· ≤ ·) 2 5` does not hold under `≤` on `ℕ`, since `2 ≤ 5`.

- Claim: If `r` is the empty relation on a type (relating no elements to any), then `VTask.IncompRel r a b` holds for every pair `a b`.

### Boundaries

- When `r` is a total relation (such as `≤` on a linearly ordered type), `VTask.IncompRel r a b` is always false for every `a` and `b`; there are no incomparable pairs.
- When `r` is an irreflexive relation (such as strict `<`), `VTask.IncompRel r a a` holds for every `a`, since `¬ r a a` follows from irreflexivity; incomparability is reflexive in this setting.
- When `r` is reflexive (e.g., `≤`), `VTask.IncompRel r a a` is always false.
- `VTask.IncompRel r` is always a symmetric relation: if `a` and `b` are incomparable, then so are `b` and `a`.
- `VTask.IncompRel r a b` and `AntisymmRel r a b` (which requires both `r a b` and `r b a`) are mutually exclusive.

### Not to be confused with

- `AntisymmRel r a b`: this asserts *both* `r a b` and `r b a`, making `a` and `b` equivalent under `r`; incomparability is the opposite extreme where *neither* direction holds.
- The complement of `r`: `¬ r a b` is a one-directional negation, whereas `VTask.IncompRel r a b` requires the negation in *both* directions simultaneously.
- `Relation.SymmGen r a b`: this asserts that `r a b` or `r b a` holds (i.e., the symmetric closure), which is exactly the *negation* of incomparability.