## Object

`VTask.leftInv S` is the submonoid of `M` consisting of all elements that are **left inverses** of some element of `S`. Concretely, an element `x : M` belongs to `VTask.leftInv S` if and only if there exists some `y ∈ S` such that `x * y = 1`.

Intuitively, this construction collects all "left-side" inverses of the given submonoid `S` and packages them as a submonoid in their own right.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.leftInv : {M : Type u_1} -> [Monoid M] -> (S : Submonoid M) -> Submonoid M
<!-- PINNED-SIGNATURE:END -->


`VTask.leftInv : {M : Type u_1} -> [Monoid M] -> (S : Submonoid M) -> Submonoid M`

The ambient type `M` is inferred; it must carry a monoid structure, supplied by the instance argument. The explicit argument `S` is the submonoid of `M` whose left inverses are being collected.

## Conventions

There are no special junk-value or boundary conventions to declare for this definition: it is a total construction defined for every submonoid `S` of every monoid `M`, and no degenerate inputs produce undefined or arbitrary output.

## Worked examples

- Claim: In any monoid `M`, the identity element `1` belongs to `VTask.leftInv S` for every submonoid `S`, because `1 * 1 = 1` and `1 ∈ S`.

- Claim: If `x ∈ M` satisfies `x * s = 1` for some `s ∈ S`, then `x ∈ VTask.leftInv S`.

- Claim: If `a, b ∈ VTask.leftInv S` with witnesses `a * s = 1` and `b * t = 1` (where `s, t ∈ S`), then `a * b ∈ VTask.leftInv S`, witnessed by `t * s ∈ S` via `(a * b) * (t * s) = 1`.

- Claim: When `M` is a group and `S = ⊤` (the whole monoid), every element of `M` belongs to `VTask.leftInv S`, since every element has a two-sided inverse.

## Boundaries

- **Trivial submonoid (`S = ⊥`, containing only `1`):** The only witness available is `y = 1`, so `x ∈ VTask.leftInv S` iff `x * 1 = 1`, i.e., `x = 1`. Hence `VTask.leftInv ⊥ = ⊥`.
- **Full submonoid (`S = ⊤`):** Any element that has *any* right inverse in `M` belongs to `VTask.leftInv ⊤`.
- **Non-cancellative monoids:** An element can be a left inverse of multiple distinct elements of `S`; the definition asks only for *existence* of one such witness.
- **The identity `1` always belongs:** `1 * 1 = 1` and `1 ∈ S` (since `S` is a submonoid), so `1 ∈ VTask.leftInv S` unconditionally.
- **Closure under multiplication is built in:** The result is closed under the monoid operation by construction, so it is a genuine submonoid.

## Not to be confused with

- **`Submonoid.map` / `Submonoid.comap`:** These transfer a submonoid along a homomorphism, rather than collecting inverse witnesses.
- **Two-sided inverses / units:** `VTask.leftInv S` tracks *left* inverses only; an element `x` need not satisfy `y * x = 1` for any `y ∈ S`.
- **`Subgroup.leftInv` or additive analogues:** In an additive setting the analogous construction collects left negatives; the docstring mentions `leftNeg`, but the present definition is the multiplicative version for submonoids.
