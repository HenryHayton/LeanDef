## Object

`VTask.IsAtom a` holds when `a` is an *atom* of the partially ordered set with a bottom element `⊥`: it is the notion that `a` sits immediately above `⊥` with nothing strictly between them, and that `a` is not itself `⊥`. In lattice theory an atom is a minimal non-bottom element.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsAtom : {α : Type u_2} -> [Preorder α] -> [OrderBot α] -> (a : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsAtom : {α : Type u_2} -> [Preorder α] -> [OrderBot α] -> (a : α) -> Prop
```

The implicit type `α` is the carrier of the ordered set. The `Preorder` instance supplies the strict and non-strict order relations on `α`. The `OrderBot` instance supplies the distinguished bottom element `⊥`. The explicit argument `a` is the element being tested for atomicity.

## Conventions

No junk-value or edge conventions are declared for this predicate; it is a well-defined `Prop` for every element of every `OrderBot` preorder, including `⊥` itself (where it is simply false).

## Worked examples

- Claim: In the natural numbers with bottom `0`, the element `1` satisfies `VTask.IsAtom 1`, because `1 ≠ 0` and the only natural number strictly less than `1` is `0`.

- Claim: In the natural numbers with bottom `0`, the element `2` does not satisfy `VTask.IsAtom 2`, because `1` lies strictly between `0` and `2`, violating the minimality condition.

- Claim: In the Boolean lattice on two elements `{⊥, ⊤}`, the unique non-bottom element `⊤` satisfies `VTask.IsAtom ⊤` precisely when there is no element strictly between `⊥` and `⊤`.

- Claim: For any `OrderBot` `α`, the bottom element `⊥` never satisfies `VTask.IsAtom ⊥`, because the first conjunct `⊥ ≠ ⊥` is false.

## Boundaries

- **Bottom element**: `VTask.IsAtom ⊥` is always false, because the definition requires the element to be distinct from `⊥`.
- **Single-element order**: If `α` has only one element, that element is `⊥`, so no atom exists.
- **Covers**: An element `a` is an atom if and only if `⊥ ⋖ a` (i.e., `⊥` is covered by `a`), provided the order has no element strictly between them. The set of elements `≤ a` is exactly `{⊥, a}` when `a` is an atom.
- **Suborders**: If `a` is an atom in `α` and `a ≤ x`, then the image of `a` in the sub-order `Set.Iic x` is again an atom.

## Not to be confused with

- `VTask.IsCoatom`: the dual notion, an element immediately below the top `⊤` rather than immediately above `⊥`.
- `FirstOrder.Language.BoundedFormula.IsAtomic`: atomicity of *logical formulas* (equality or relation formulas), a completely unrelated syntactic notion.
- Irreducible or prime elements: in a lattice, primes and irreducibles generalise atoms but are strictly weaker conditions in general.