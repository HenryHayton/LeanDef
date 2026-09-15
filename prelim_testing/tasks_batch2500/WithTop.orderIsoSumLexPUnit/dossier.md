## Object

`VTask.orderIsoSumLexPUnit` is a concrete order isomorphism between `WithTop α` and the lexicographic sum `α ⊕ₗ PUnit`. Concretely, the top element `⊤` of `WithTop α` is sent to the single element of `PUnit` (placed on the right of the sum), while every coerced element `↑a` for `a : α` is sent to `inl a` (placed on the left). The ordering is respected: elements of `α`, viewed as `inl` terms, are all strictly less than the `inr PUnit.unit` term in the lex sum, exactly mirroring the fact that every coerced `a` is below `⊤` in `WithTop α`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.orderIsoSumLexPUnit : {α : Type u_1} -> [LE α] -> WithTop α ≃o α ⊕ₗ PUnit.{u_4 + 1}
<!-- PINNED-SIGNATURE:END -->


`VTask.orderIsoSumLexPUnit : {α : Type u_1} -> [LE α] -> WithTop α ≃o α ⊕ₗ PUnit.{u_4 + 1}`

The implicit type argument `α` is the underlying ordered type. The `LE α` instance supplies the order relation on `α`. The result is a bundled order isomorphism (`≃o`) between `WithTop α` (which freely adjoins a greatest element) and the lexicographic sum `α ⊕ₗ PUnit` (where every left element is below every right element, and `PUnit` contributes exactly one right element).

## Conventions

There are no junk-value conventions for this definition: the isomorphism is a total bijection defined on all of `WithTop α`, and both the forward and inverse maps are well-defined everywhere on their respective domains.

## Worked examples

- Claim: The top element of `WithTop α` maps to `toLex (inr PUnit.unit)` under `VTask.orderIsoSumLexPUnit`.

- Claim: A coerced element `↑a` (for `a : α`) maps to `toLex (inl a)` under `VTask.orderIsoSumLexPUnit`.

- Claim: The inverse of `VTask.orderIsoSumLexPUnit` sends `toLex (inl a)` back to the coercion `↑a` in `WithTop α`.

- Claim: The inverse of `VTask.orderIsoSumLexPUnit` sends `toLex (inr PUnit.unit)` back to `⊤` in `WithTop α`.

## Boundaries

- The type `α` needs only a `LE` instance; no additional structure (transitivity, reflexivity, totality) is required for the isomorphism to be stated, though the isomorphism respects whatever order structure `α` has.
- `PUnit` is the unit type with a single element, so `α ⊕ₗ PUnit` has exactly one more element than `α`, precisely as `WithTop α` does.
- When `α` itself is empty, `WithTop α` is a one-element type (just `⊤`), and `α ⊕ₗ PUnit` is also a one-element type (just `inr PUnit.unit`); the isomorphism still holds.
- The lexicographic order on `α ⊕ₗ PUnit` makes all left (`inl`) elements less than or equal to all right (`inr`) elements, which faithfully captures the fact that every coe'd element of `WithTop α` is ≤ `⊤`.

## Not to be confused with

- `WithBot α ≃o PUnit ⊕ₗ α`: the analogous isomorphism for `WithBot`, where the extra element `⊥` is placed on the *left* of the lex sum.
- `WithTop.orderIsoNat` or similar: other order isomorphisms involving `WithTop` but for specific types rather than a general `α`.
- The underlying `Equiv` (bare bijection) between `WithTop α` and `α ⊕ₗ PUnit`: `VTask.orderIsoSumLexPUnit` is a *bundled order isomorphism* (`≃o`), not just a set-theoretic equivalence; it additionally certifies that the map and its inverse are both order-preserving.