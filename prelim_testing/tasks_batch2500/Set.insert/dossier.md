## VTask.insert

### Object

Given an element `a` and a set `s`, `VTask.insert a s` is the set obtained by adjoining `a` to `s`. Concretely, an element `b` belongs to this set if and only if `b` equals `a` or `b` already belongs to `s`. In classical set-theoretic notation this is the union `{a} ∪ s`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.insert : {α : Type u} -> (a : α) -> (s : Set α) -> Set α
<!-- PINNED-SIGNATURE:END -->


The first argument `a : α` is the element being inserted into the set. The second argument `s : Set α` is the base set to which `a` is adjoined. Both live over the same ambient type `α`, which is determined by unification.

### Conventions

No special junk-value or edge conventions are declared: the operation is total and well-defined for every element and every set, including the empty set and sets that already contain `a`.

### Worked examples

- Claim: The natural number 3 is a member of `VTask.insert 3 {5, 7}`.
  (By definition, `b ∈ VTask.insert a s ↔ b = a ∨ b ∈ s`, so `3 = 3` makes 3 a member.)

- Claim: The natural number 5 is a member of `VTask.insert 3 {5, 7}`.
  (Here `5 ≠ 3`, but `5 ∈ {5, 7}`, so the right disjunct applies.)

- Claim: Inserting an element that is already present does not change the set: for any `a : α` and `s : Set α` with `a ∈ s`, `VTask.insert a s = s`.

- Claim: Inserting into the empty set yields a singleton: `VTask.insert a ∅ = {a}` for any element `a`.

- Claim: Insertion is commutative up to equality: `VTask.insert a (VTask.insert b s) = VTask.insert b (VTask.insert a s)` for all `a`, `b`, and `s`.

### Boundaries

- **Element already in `s`:** When `a ∈ s`, `VTask.insert a s` equals `s` exactly; no duplicate is introduced, and the cardinality is unchanged.
- **Empty base set:** `VTask.insert a ∅` is the singleton `{a}`, containing exactly one element.
- **Repeated insertion of the same element:** `VTask.insert a (VTask.insert a s) = VTask.insert a s`; idempotence holds.
- **All types:** The definition is polymorphic and places no restriction on `α`; it works for sets of any type.

### Not to be confused with

- **`List.insert`** – inserts an element into a list, a different (ordered, possibly duplicating) data structure, not a set.
- **`Finset.insert`** – the analogous operation on finite sets (`Finset α`), which carries decidable-equality hypotheses and finiteness bookkeeping not present for `Set α`.
- **`Set.union` / `∪`** – unions two sets of equal type; `VTask.insert a s` is the special case where the left operand is the singleton `{a}`, but `∪` expects a full `Set α` on both sides.