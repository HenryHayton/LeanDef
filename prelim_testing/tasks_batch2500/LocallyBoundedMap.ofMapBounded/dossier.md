## Object

`VTask.ofMapBounded` constructs a *locally bounded map* — a structure-preserving map between bornological spaces that pulls bounded sets back to bounded sets — from a plain function together with an explicit proof that the function maps bounded sets to bounded sets. It packages the function and the boundedness-preservation evidence into the `LocallyBoundedMap` type, which records both the underlying function and the bornological compatibility condition.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofMapBounded : {α : Type u_2} -> {β : Type u_3} -> [Bornology α] -> [Bornology β] -> (f : α → β) -> (h : ∀ ⦃s : Set α⦄, Bornology.IsBounded s → Bornology.IsBounded (f '' s)) -> LocallyBoundedMap α β
<!-- PINNED-SIGNATURE:END -->


VTask.ofMapBounded : {α : Type u_2} -> {β : Type u_3} -> [Bornology α] -> [Bornology β] -> (f : α → β) -> (h : ∀ ⦃s : Set α⦄, Bornology.IsBounded s → Bornology.IsBounded (f '' s)) -> LocallyBoundedMap α β

The implicit type arguments `α` and `β` are the source and target types, respectively. The two instance arguments supply the bornological structure (the notion of bounded sets) on each type. The argument `f` is the underlying set-theoretic function being promoted to a locally bounded map. The argument `h` is the boundedness-preservation proof: for every bounded subset `s` of `α`, the direct image `f '' s` is bounded in `β`.

## Conventions

There are no junk-value conventions for this definition: it is a total constructor whose two explicit arguments are a function and a proof, and it is always well-defined whenever those arguments are supplied.

## Worked examples

- Claim: The underlying function of `VTask.ofMapBounded f h` is definitionally equal to `f` itself; that is, applying `VTask.ofMapBounded f h` to any element `a` of `α` yields `f a`.

- Claim: The coercion of `VTask.ofMapBounded f h` to a function equals `f`, i.e., `⇑(VTask.ofMapBounded f h) = f`.

- Claim: For the identity function `id : α → α` with a proof that `id` maps bounded sets to bounded sets (which is trivial since `id '' s = s`), `VTask.ofMapBounded id (fun s hs => by simp [hs])` is a valid `LocallyBoundedMap α α`, and applying it to any point `a` returns `a`.

## Boundaries

- The function `f` need not be continuous or linear; only the bounded-image condition is required.
- If `α` carries the discrete bornology (every set bounded) and `β` carries the indiscrete bornology (only the empty set bounded in the empty space, or all sets bounded), the proof obligation `h` may be trivial or vacuous, but `VTask.ofMapBounded` still produces a well-typed result.
- The constructor does not verify or require that `f` is surjective, injective, or continuous.
- On types with trivial bornology (where every set is bounded), the hypothesis `h` is automatically satisfied, and `VTask.ofMapBounded f h` wraps any function at all.

## Not to be confused with

- `LocallyBoundedMap.mk` — the raw structure constructor that takes the underlying function and a filter condition on cobounded sets directly, rather than an image-of-bounded-sets hypothesis.
- Continuous maps constructed via `ContinuousMap.mk` — those encode topological continuity, not bornological boundedness preservation.
- `BoundedContinuousFunction` — maps that are simultaneously continuous and globally bounded in norm, a stronger condition than locally bounded in the bornological sense.