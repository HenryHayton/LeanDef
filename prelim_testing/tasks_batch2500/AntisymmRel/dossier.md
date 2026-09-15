## Object

`VTask.AntisymmRel r a b` is the proposition that two elements `a` and `b` of a type `α` are related *in both directions* by a binary relation `r`. Concretely, it holds if and only if `r a b` and `r b a` are both true simultaneously. In order-theoretic language, when `r` is a preorder `≤`, this says that `a` and `b` are mutually comparable — each is ≤ the other — which in an antisymmetric order would force `a = b`. More generally it captures the equivalence kernel of a preorder: the "same level" relation.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.AntisymmRel : {α : Type u_1} -> (r : α → α → Prop) -> (a b : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


VTask.AntisymmRel : {α : Type u_1} -> (r : α → α → Prop) -> (a b : α) -> Prop

The implicit type argument `α` is the carrier type whose elements are being related. The explicit argument `r` is the underlying binary relation on `α`. The arguments `a` and `b` are the two elements of `α` whose mutual relatedness under `r` is being asserted.

## Conventions

No special junk-value or out-of-domain conventions are declared: the definition is a total predicate on all binary relations and all pairs of elements; there are no edge cases that receive a conventional default value.

## Worked examples

- Claim: `VTask.AntisymmRel (· ≤ ·) (3 : ℤ) 3` holds, because `3 ≤ 3` and `3 ≤ 3` are both true.

- Claim: `VTask.AntisymmRel (· ≤ ·) (2 : ℤ) 5` does not hold, because `5 ≤ 2` is false.

- Claim: For the relation `r a b := True` on any type, `VTask.AntisymmRel r a b` holds for every pair `a b`, since both `r a b` and `r b a` reduce to `True`.

- Claim: `VTask.AntisymmRel r a b → VTask.AntisymmRel r b a` for any relation `r` and any `a b`; that is, the antisymmetrization relation is itself symmetric.

## Boundaries

- When `r` is reflexive and antisymmetric (e.g. a partial order), `VTask.AntisymmRel r a b` holds if and only if `a = b`. The diagonal is exactly the set where the relation is symmetric.
- When `r` is the trivial relation `fun _ _ => False`, `VTask.AntisymmRel r a b` is always `False`, even for `a = b`.
- When `r` is the total relation `fun _ _ => True`, `VTask.AntisymmRel r a b` is always `True` for every pair.
- Reflexivity of `VTask.AntisymmRel r` on `a` (i.e. `VTask.AntisymmRel r a a`) follows whenever `r` itself is reflexive, since both conjuncts `r a a` coincide.
- `VTask.AntisymmRel r` is always symmetric in `a` and `b` by commutativity of conjunction, regardless of any property of `r`.

## Not to be confused with

- `Antisymm r` (the *property* that `r` is antisymmetric): that asserts `∀ a b, r a b → r b a → a = b`, a global condition on `r`, not a relation on pairs.
- `IncompRel r a b` (the incomparability relation): holds when *neither* `r a b` nor `r b a` holds — the logical complement of `VTask.AntisymmRel r a b` among comparable pairs.
- `SymmGen r a b` (the symmetric closure): holds when `r a b` *or* `r b a`, a strictly weaker condition than requiring both.