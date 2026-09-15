## Object

`VTask.Contravariant` is a proposition asserting that a given action **reflects** a given relation: whenever acting by some element on the left sends one pair of elements into a related pair, the original pair was already related. In other words, the action is *cancellable* with respect to the relation in the forward-reflecting direction: `μ m n₁ r μ m n₂` implies `n₁ r n₂`, for every acting element `m` and every pair `n₁, n₂`.

Typically one thinks of `μ` as left-multiplication by `m` in some algebraic structure, and `r` as an order relation such as `≤` or `<`, so that `VTask.Contravariant` says the action is *order-reflecting*: if multiplying on the left preserves the order comparison, then the original elements already satisfied it.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Contravariant : (M : Type u_1) -> (N : Type u_2) -> (μ : M → N → N) -> (r : N → N → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Contravariant : (M : Type u_1) -> (N : Type u_2) -> (μ : M → N → N) -> (r : N → N → Prop) -> Prop`

`M` is the type whose elements act on `N`; it is the type of *actors* or *scalars*. `N` is the type being acted upon; the relation `r` lives on `N`. `μ` is the action itself, a function taking an element of `M` and an element of `N` and returning an element of `N` (e.g., left-multiplication). `r` is the binary relation on `N` whose reflection by `μ` the proposition asserts.

## Conventions

No junk-value or default-output conventions are declared for this definition: it is a universally quantified `Prop` with no inputs requiring a fallback value.

## Worked examples

- Claim: `VTask.Contravariant ℤ ℤ (· + ·) (· ≤ ·)` holds, because adding a fixed integer to both sides of `≤` can be cancelled: `m + n₁ ≤ m + n₂ → n₁ ≤ n₂`.

- Claim: `VTask.Contravariant ℕ ℕ (· * ·) (· ≤ ·)` does **not** hold in general (it fails when the acting element is `0`), illustrating that the proposition can be false for specific choices of `μ` and `r`.

- Claim: If `VTask.Contravariant M N μ r` holds, then `VTask.Contravariant M N μ (flip r)` also holds, because reflecting `r` implies reflecting its flip.

- Claim: For a group `N` with multiplication, `VTask.Contravariant N N (· * ·) r` is equivalent to the corresponding covariant statement, reflecting the cancellation properties of groups.

## Boundaries

- When `r` is the trivially-true relation `fun _ _ => True`, `VTask.Contravariant M N μ r` holds vacuously for any `μ`.
- When `r` is the trivially-false relation `fun _ _ => False`, the hypothesis `r (μ m n₁) (μ m n₂)` is never satisfied, so `VTask.Contravariant M N μ r` holds vacuously as well.
- The quantification is over *all* `m : M` simultaneously, so a single counterexample element (like `0` in `ℕ` under multiplication) suffices to falsify the whole proposition.
- In a linear order, `VTask.Contravariant M N μ (· ≤ ·)` implies `VTask.Contravariant M N μ (· < ·)`, and under suitable order assumptions the two are interchangeable with the covariant versions.

## Not to be confused with

- **`VTask.Covariant`** (the companion proposition): asserts that the action *preserves* the relation (`n₁ r n₂ → μ m n₁ r μ m n₂`), the dual direction to reflection.
- **`ContravariantClass`** (the typeclass wrapper): bundles `VTask.Contravariant` as a typeclass instance so it can be inferred automatically by Lean's typeclass system; `VTask.Contravariant` itself is the bare proposition.
- **`MulLECancellable`**: a closely related but element-wise notion asserting cancellability for a *specific* element rather than universally over all of `M`.