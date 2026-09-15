## Object

`VTask.head'` extracts the **root label** (the element of the pfunctor's shape/type-index set `F.A`) from a non-trivial approximation of the greatest fixed point (cofix) of a polynomial functor. An approximation of depth `n+1` consists of a root label together with children; `VTask.head'` returns just that root label, discarding the children.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.head' : {F : PFunctor.{uA, uB}} -> {n : ℕ} -> PFunctor.Approx.CofixA F n.succ → F.A
<!-- PINNED-SIGNATURE:END -->


`{F : PFunctor.{uA, uB}} -> {n : ℕ} -> PFunctor.Approx.CofixA F n.succ → F.A`

The implicit argument `F` is the polynomial functor whose cofix is being approximated. The implicit natural number `n` is the depth parameter; the approximation has depth `n+1` (it is non-trivial, i.e., at least one level deep). The explicit argument is a depth-`(n+1)` approximation of the cofix of `F`; it must have the successor form so that it contains a root label. The return value is an element of `F.A`, the set of shapes (labels) of the functor.

## Conventions

This function is only defined for approximations of depth `n.succ` (i.e., strictly positive depth). There is no corresponding `head'` for depth-`0` approximations because such approximations carry no data and have no root label.

## Worked examples

- Claim: For any pfunctor `F`, any natural number `n`, and any `CofixA F n.succ` constructed as `CofixA.intro i children`, `VTask.head' (CofixA.intro i children) = i`.

- Claim: If two depth-`(n+1)` approximations `t₁` and `t₂` satisfy `VTask.head' t₁ = VTask.head' t₂`, then their root labels are equal (they agree on `F.A`).

- Claim: For the identity pfunctor (where `F.A` has a single element `*`), `VTask.head'` always returns that unique element regardless of which depth-`(n+1)` approximation is supplied.

## Boundaries

- The function requires the depth to be a successor (`n.succ`), so it is simply not applicable to depth-`0` approximations (`CofixA F 0`). There is no junk value or partiality; the type system enforces that only non-trivial approximations are supplied.
- The children of the root node are completely ignored; only the `F.A`-valued label is returned.
- The function is total and non-recursive on the natural number `n`; it pattern-matches only on the single constructor `CofixA.intro`.

## Not to be confused with

- `PFunctor.M.head` / `head` for the actual cofix (`M F`): that extracts the root label from a genuine infinite tree, not a finite approximation.
- `PFunctor.Approx.CofixA.children` (or an analogous projection): that extracts the child approximations rather than the root label.
- `PFunctor.B` (the branching-type field of a pfunctor): `F.A` is the set of shapes/labels, while `F.B` indexes the children; `VTask.head'` returns an `F.A` value, not an `F.B` value.