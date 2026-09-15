## VTask.IsFixedPt

### Object

A point `x` is a **fixed point** of a self-map `f` on a type `α` if applying `f` to `x` returns `x` unchanged, i.e., `f x = x`. This is the standard notion of a fixed point from mathematics: a value that `f` leaves invariant.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsFixedPt : {α : Type u₁} -> (f : α → α) -> (x : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first argument `f` is the self-map (a function from a type to itself) whose fixed points are being studied. The second argument `x` is the candidate point in that type to test for being a fixed point.

### Conventions

There are no junk-value or out-of-domain conventions to declare: `VTask.IsFixedPt` is a fully general proposition defined for every self-map and every point in any type, with no restriction or special boundary behaviour.

### Worked examples

- Claim: Every point is a fixed point of the identity function `id`.

- Claim: The value `3 : ℕ` is a fixed point of the constant function `fun _ => 3`.

- Claim: The value `0 : ℕ` is a fixed point of the function `fun n => n * 0` (since `0 * 0 = 0`).

- Claim: In a subsingleton type (one with at most one element), every function has every point as a fixed point, because all elements are equal.

- Claim: If `f` is injective and `f (f x) = f x`, then `f x = x`; equivalently, `IsFixedPt f (f x)` iff `IsFixedPt f x` for injective `f`.

- Claim: Any fixed point of `f` is also a periodic point of `f` for every period `n : ℕ`.

### Boundaries

- **Identity function**: Every point of every type is a fixed point of `id`. This is a special case available in all generality.
- **Subsingleton types**: When the type has at most one element, every self-map trivially has every point as a fixed point, because all values are propositionally equal.
- **Constant functions**: A constant function `fun _ => c` has exactly `c` as a fixed point (and no other points, unless all points are equal to `c`).
- **Period-1 equivalence**: A point is a fixed point of `f` if and only if its minimal period under `f` is 1 (with the standard convention that the minimal period is 1 precisely for fixed points).
- **Relation to periodic points**: Every fixed point is automatically a periodic point for every natural number period `n`.

### Not to be confused with

- **`Function.fixedPoints f`** (the set/subtype of all fixed points of `f`): that is the *collection* of fixed points, whereas `VTask.IsFixedPt f x` is the *proposition* that a specific `x` is one. Membership in `fixedPoints f` is equivalent to `VTask.IsFixedPt f x`.
- **`Function.IsPeriodicPt f n x`** (periodic point of period `n`): a strictly weaker condition requiring only `f^[n] x = x` for some `n`, not `f x = x` directly. Every fixed point is periodic, but not conversely.
- **`Function.Semiconj`** or **`Function.Commute`**: these describe relationships between two different functions, not the invariance of a point under a single function.