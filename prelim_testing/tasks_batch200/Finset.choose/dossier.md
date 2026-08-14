## 1. Object

`VTask.choose` extracts the unique element of a finite set satisfying a given predicate. Given a finset `l`, a decidable predicate `p`, and a proof that there is exactly one element of `l` satisfying `p`, it returns that unique element as a value of the ambient type `α`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.choose : {α : Type u_1} -> (p : α → Prop) -> [DecidablePred p] -> (l : Finset α) -> (hp : ∃! a, a ∈ l ∧ p a) -> α
<!-- PINNED-SIGNATURE:END -->


`VTask.choose : {α : Type u_1} -> (p : α → Prop) -> [DecidablePred p] -> (l : Finset α) -> (hp : ∃! a, a ∈ l ∧ p a) -> α`

The type `α` is the ambient type, inferred implicitly. The argument `p` is the predicate that the chosen element must satisfy. The instance `[DecidablePred p]` provides a computational decision procedure for `p`. The argument `l` is the finset from which the unique element is drawn. The argument `hp` is the proof that there exists a unique element of `l` satisfying `p`; it is this proof that licenses the extraction and guarantees the result is well-defined.

## 3. Conventions

The function is only defined when `hp` is actually provided, so there is no junk value or default: the uniqueness proof is part of the function's signature, not a side condition that could fail. No special conventions for degenerate inputs are needed or declared.

## 4. Worked examples

- Claim: For `l = {1, 2, 3} : Finset ℕ` and `p = (· = 2)`, `VTask.choose p l hp` equals `2`, where `hp` witnesses the unique element 2.

- Claim: The result of `VTask.choose p l hp` is always a member of `l`; that is, `VTask.choose p l hp ∈ l` holds for any valid `hp`.

- Claim: The result of `VTask.choose p l hp` always satisfies `p`; that is, `p (VTask.choose p l hp)` holds for any valid `hp`.

- Claim: For `l = {0} : Finset ℕ` and `p = (· = 0)`, `VTask.choose p l hp = 0`.

## 5. Boundaries

- **Uniqueness is required:** The hypothesis `hp` must assert exactly one element satisfies both `· ∈ l` and `p`. If the predicate holds for zero or more than one element of `l`, the required proof cannot be constructed, and the function cannot be called.
- **Membership guaranteed:** The returned element is always a member of `l`, as stated by `choose_mem`.
- **Predicate guaranteed:** The returned element always satisfies `p`, as stated by `choose_property`.
- **Both together:** `choose_spec` packages the membership and predicate satisfaction as a conjunction.
- **Uniqueness pinned:** Because `hp` asserts uniqueness, the returned element is the only element of `l` satisfying `p`; any other element of `l` satisfying `p` would be equal to the returned one.
- **The ambient type matters:** The result lives in `α`, not in `l` or a subtype; membership in `l` is an additional proved property, not baked into the return type.

## 6. Not to be confused with

- **`Classical.choose`**: Extracts a witness from any `∃` proof (not restricted to finsets, and not requiring uniqueness); does not guarantee membership in any set.
- **`Finset.chooseX`**: A closely related internal variant that returns the element together with bundled proof data, rather than the bare element.
- **`Nat.choose`** (binomial coefficient): A completely unrelated function computing the binomial coefficient "n choose k"; shares the name `choose` but operates on natural numbers, not finsets or predicates.