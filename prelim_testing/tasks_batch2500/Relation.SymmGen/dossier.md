## VTask.SymmGen

### Object

Given a binary relation `r` on a type `α`, the **symmetric closure** of `r` is the smallest symmetric relation containing `r`. Concretely, `VTask.SymmGen r a b` holds if and only if `a` and `b` are *comparable* under `r`: either `r a b` or `r b a` (or both). This is sometimes called the *comparability relation* induced by `r`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SymmGen : {α : Type u_1} -> (r : α → α → Prop) -> (a b : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the carrier type on which the relation lives. The explicit argument `r` is the base binary relation whose symmetric closure is being formed. The arguments `a` and `b` are the two elements of `α` being tested for comparability.

### Conventions

No special junk-value or edge-case conventions are declared: the relation is total over all inputs — every pair `(a, b)` of elements of `α` is a valid query, and the proposition is simply `r a b ∨ r b a`.

### Worked examples

- Claim: `VTask.SymmGen (· < ·) (1 : ℕ) 2` holds because `1 < 2`.

- Claim: `VTask.SymmGen (· < ·) (2 : ℕ) 1` holds because `1 < 2`, i.e., the reversed direction `r b a` is satisfied.

- Claim: `VTask.SymmGen (· ≤ ·) a b` holds whenever `a` and `b` are comparable in a linear order, since either `a ≤ b` or `b ≤ a`.

- Claim: `VTask.SymmGen r a b ↔ VTask.SymmGen r b a` — the symmetric closure is itself symmetric, so the order of arguments does not matter.

### Boundaries

- When `r` is already symmetric (e.g., equality), `VTask.SymmGen r` coincides with `r` itself.
- When `r` is a total relation (every pair is related in at least one direction), `VTask.SymmGen r a b` holds for every `a` and `b`.
- When neither `r a b` nor `r b a` holds — i.e., `a` and `b` are incomparable under `r` — `VTask.SymmGen r a b` is false. The negation `¬ VTask.SymmGen r a b` is exactly the incomparability relation `IncompRel r a b`.
- Swapping the base relation does not change the symmetric closure: `VTask.SymmGen (swap r) = VTask.SymmGen r`.

### Not to be confused with

- `Relation.ReflTransGen r`: the reflexive-transitive closure of `r`, which is a much coarser operation and is not symmetric in general.
- `IncompRel r`: the *incomparability* relation, which is the *complement* of `VTask.SymmGen r` — `IncompRel r a b` holds precisely when `VTask.SymmGen r a b` is false.
- `AntisymmRel r`: the antisymmetry relation `r a b ∧ r b a`, which requires *both* directions rather than *at least one*.