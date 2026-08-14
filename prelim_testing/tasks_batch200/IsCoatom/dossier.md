## VTask.IsCoatom

### Object

A **coatom** of a partially ordered set with a greatest element ⊤ is an element that sits immediately below ⊤: it is strictly less than ⊤, and there is no element strictly between it and ⊤. Equivalently, it is an element that is not ⊤ itself and is maximal among elements that are not ⊤. In lattice-theoretic language, a coatom is an element covered by ⊤.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsCoatom : {α : Type u_2} -> [Preorder α] -> [OrderTop α] -> (a : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the carrier type of the ordered structure. The implicit `Preorder α` instance supplies the partial order on `α`, and the implicit `OrderTop α` instance supplies the greatest element ⊤. The explicit argument `a : α` is the element being tested for the coatom property.

### Conventions

No special junk-value or out-of-domain conventions are declared for this predicate; it is a straightforward proposition about an element of any `OrderTop`, and its two conditions (being distinct from ⊤, and having no element strictly between it and ⊤) are well-defined for every element of every such structure.

### Worked examples

- Claim: In a two-element Boolean lattice (e.g., `Bool` ordered by `false < true`), `false` is a coatom, because `false ≠ true` and the only element strictly greater than `false` is `true = ⊤`.

- Claim: In the subgroup lattice of a group `G`, a subgroup `H` is a coatom if and only if `H` is a maximal proper subgroup of `G` — it is not the whole group, and no proper subgroup strictly contains it except `G` itself.

- Claim: For the natural numbers ordered by divisibility with a top element adjoined, a coatom would be an element immediately below that top, with nothing properly between it and the top.

- Claim: `VTask.IsCoatom a` implies `a < ⊤`, i.e., every coatom is strictly below the top element.

- Claim: `VTask.IsCoatom a` implies that for any `b`, `a < b` forces `b = ⊤`.

### Boundaries

- The top element ⊤ itself is **never** a coatom, by the first conjunct `a ≠ ⊤`.
- If the order has no element strictly below ⊤ (e.g., a one-element order where ⊤ is the only element), then no coatom exists.
- If two distinct elements are both strictly below ⊤ and one is strictly between the other and ⊤, neither of them qualifies as a coatom (the lower one has something strictly between it and ⊤, violating the second conjunct).
- In a two-element order `{⊥, ⊤}`, the bottom element ⊥ is a coatom because the only element strictly above ⊥ is ⊤.

### Not to be confused with

- **IsAtom**: the dual notion — an element just above ⊥ rather than just below ⊤.
- **IsMax**: asserts that `a` has no strictly greater element at all, which would force `a = ⊤` in an `OrderTop`; a coatom is strictly less than ⊤, so it is not a maximal element.
- **Covby (a ⋖ b)**: the general covering relation; `VTask.IsCoatom a` is precisely the statement `a ⋖ ⊤`, but the covering relation is stated for arbitrary pairs, not just pairs involving ⊤.