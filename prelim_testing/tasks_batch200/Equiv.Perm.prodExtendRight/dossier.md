## Object

`VTask.prodExtendRight a e` is a permutation of the product type `α₁ × β₁` constructed from a permutation `e` of `β₁` and a distinguished element `a : α₁`. It acts as `e` on the fiber over `a` — mapping `(a, b)` to `(a, e b)` — while fixing every pair `(a', b)` whose first component `a'` is different from `a`. In other words, it "extends" a permutation of one fiber to a permutation of the whole product by leaving all other fibers untouched.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prodExtendRight : {α₁ : Type u_9} -> {β₁ : Type u_10} -> [DecidableEq α₁] -> (a : α₁) -> (e : Equiv.Perm β₁) -> Equiv.Perm (α₁ × β₁)
<!-- PINNED-SIGNATURE:END -->


VTask.prodExtendRight : {α₁ : Type u_9} -> {β₁ : Type u_10} -> [DecidableEq α₁] -> (a : α₁) -> (e : Equiv.Perm β₁) -> Equiv.Perm (α₁ × β₁)

The implicit type arguments `α₁` and `β₁` are the index type and the fiber type of the product, respectively. The `DecidableEq α₁` instance is needed to decide whether the first component of a pair equals the distinguished element. The explicit argument `a` is the distinguished element of `α₁` that selects which fiber is permuted. The argument `e` is the permutation of `β₁` that is applied on that fiber.

## Conventions

No special junk-value or out-of-domain conventions are declared: the definition is total and its behavior is fully determined for every element of `α₁ × β₁`.

## Worked examples

- Claim: Applying `VTask.prodExtendRight a e` to `(a, b)` acts as `e` on the second component, giving `(a, e b)`.

- Claim: Applying `VTask.prodExtendRight a e` to `(a', b)` where `a' ≠ a` returns `(a', b)` unchanged.

- Claim: The first component is always preserved: `(VTask.prodExtendRight a e (a', b)).fst = a'` for any `a' : α₁` and `b : β₁`.

- Claim: The sign of `VTask.prodExtendRight a σ` equals the sign of `σ`; extending to a larger product does not change parity.

## Boundaries

- When `e` is the identity permutation, `VTask.prodExtendRight a e` is itself the identity on all of `α₁ × β₁`, since the fiber over `a` is fixed pointwise and all other fibers are already fixed.
- When `α₁` is a singleton type there is only one possible value of `a`, so `VTask.prodExtendRight a e` acts as `e` on every element of the product (the "other fibers" case never applies).
- The permutation never changes the first component of any pair: `(VTask.prodExtendRight a e ab).fst = ab.fst` holds universally.
- If a pair `(a', b)` is moved by `VTask.prodExtendRight a e`, then necessarily `a' = a`; movement implies membership in the selected fiber.

## Not to be confused with

- `Equiv.Perm.prodCongrRight`: applies a *family* of permutations `σ : α → Perm β`, one per fiber, rather than a single permutation on a single selected fiber; `VTask.prodExtendRight a e` is a single-fiber special case that, when assembled over all fibers via a list product, recovers `prodCongrRight`.
- `Equiv.Perm.prodCongr`: simultaneously permutes both components of a product using two independent permutations, one on each factor; `VTask.prodExtendRight` instead fixes the first component entirely.
- `Equiv.Perm.extendDomain`: lifts a permutation along an embedding into a larger type by fixing elements outside the image; structurally similar in spirit but operates on an arbitrary embedding rather than a product-fiber inclusion.