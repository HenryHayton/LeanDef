## Object

`VTask.Erased α` is a type that is in bijection with `α` but whose elements are **erased at runtime** — they exist only as ghost data for the purposes of type-checking and proof, and are discarded (treated like a proof or a type) by the virtual machine. It is the computational analogue of "proof-irrelevance" for arbitrary data: you can track the *existence* and *type* of a value without paying any runtime storage cost for it.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Erased : (α : Sort u) -> Sort (max 1 u)
<!-- PINNED-SIGNATURE:END -->


The sole argument `α : Sort u` is the type whose elements are to be ghost-tracked. `u` is the universe level of `α`; the result lives in `Sort (max 1 u)`, ensuring the erased wrapper is always at least in `Prop`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: `VTask.Erased` is a total, universe-polymorphic type constructor with no distinguished edge inputs.

## Worked examples

- Claim: `VTask.Erased Nat` is a type that is nonempty if and only if `Nat` is nonempty.

- Claim: Given any `a : α`, wrapping it with `VTask.Erased.mk a` and then extracting via `.out` recovers `a`; that is, `(VTask.Erased.mk a).out = a`.

- Claim: For `p : Prop`, every element of `VTask.Erased p` is a proof of `p`; in other words `VTask.Erased.out_proof` states that if `a : VTask.Erased p` then `p` holds.

- Claim: `VTask.Erased.mk` followed by `VTask.Erased.out` is the identity: for all `a : VTask.Erased α`, `VTask.Erased.mk a.out = a`.

## Boundaries

- When `α : Prop`, `VTask.Erased α` is itself a `Prop`-like object (it lives in `Sort 1`); extracting `.out` from it yields a proof of `α` via `out_proof`.
- When `α : Type u`, `VTask.Erased α` lives in `Sort (max 1 (u+1))` and behaves like a ghost copy of `α` with no runtime representation.
- `VTask.Erased α` is nonempty if and only if `α` is nonempty (`nonempty_iff`); it does not conjure inhabitants out of thin air.
- The `out` extraction is injective (`out_inj`): two erased values that share the same extracted element are definitionally equal, so the wrapper is truly a bijection with `α`.

## Not to be confused with

- `Squash α` / `Trunc α` — collapses all elements to a single point (proof-irrelevant quotient); `VTask.Erased` retains the ability to distinguish elements via `out`.
- `Thunk α` — defers computation lazily but still stores the value at runtime; `VTask.Erased` stores nothing at runtime.
- `PLift α` / `ULift α` — universe-lifting wrappers that keep full runtime storage and have no erasure semantics.