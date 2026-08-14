## VTask.Periodic

### Object

`VTask.Periodic f c` is the proposition that the function `f : α → β` is periodic with period `c : α`. Concretely, it asserts that shifting the argument of `f` by `c` (via the addition on `α`) leaves the value of `f` unchanged: for every element `x` of `α`, `f(x + c) = f(x)`. This is the standard mathematical notion of periodicity for functions between types equipped with an addition.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Periodic : {α : Type u_1} -> {β : Type u_2} -> [Add α] -> (f : α → β) -> (c : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Periodic : {α : Type u_1} -> {β : Type u_2} -> [Add α] -> (f : α → β) -> (c : α) -> Prop`

The type `α` is the domain of the function and must carry an addition operation; `β` is the codomain (no algebraic structure required). The instance `[Add α]` supplies the addition used to shift arguments. The argument `f` is the function whose periodicity is being asserted. The argument `c` is the proposed period — the element of `α` by which arguments are shifted.

### Conventions

There are no junk-value conventions to declare: `VTask.Periodic` is a universally quantified proposition, total on all inputs, and every choice of `f` and `c` yields a well-formed (though possibly false) proposition.

### Worked examples

- Claim: The real sine function satisfies `VTask.Periodic Real.sin (2 * Real.pi)`, because `sin(x + 2π) = sin x` for all real `x`.

- Claim: The real tangent function satisfies `VTask.Periodic Real.tan Real.pi`, because `tan(x + π) = tan x` for all real `x`.

- Claim: The constant function `fun (x : ℤ) => (0 : ℤ)` satisfies `VTask.Periodic (fun _ => 0) c` for every `c : ℤ`, since `0 = 0` trivially.

- Claim: The identity function `id : ℤ → ℤ` satisfies `VTask.Periodic id c` if and only if `c = 0`, since `x + c = x` for all `x` forces `c = 0` in `ℤ`.

### Boundaries

- **Period zero**: `VTask.Periodic f 0` is not automatically true; it requires `f (x + 0) = f x` for all `x`. On types where `x + 0 = x` holds (i.e., where `0` is a right identity), every function is periodic with period `0`. On a bare `Add` without such a law, this need not hold.
- **Non-numerical domains**: The definition applies to any type with `Add`, including free monoids, groups, modules, or custom algebraic structures. Periodicity is purely combinatorial: no notion of size or ordering of `c` is required.
- **Non-injective periods**: A function can have multiple periods simultaneously; if `f` is periodic with period `c`, it may also be periodic with period `2c`, `3c`, etc., provided the relevant additive structure supports it.
- **Negative periods**: If `α` is a group, periodicity with `c` and with `-c` are equivalent, but the definition as stated only asserts the forward shift by `c`; closure under negation must be derived separately.

### Not to be confused with

- **`VTask.Antiperiodic f c`**: The proposition `f (x + c) = -f x` for all `x`; antiperiodicity with `c` implies periodicity with `2c` but is strictly stronger.
- **`VTask.Periodic.lift`**: The induced map on the quotient group `α ⧸ ⟨c⟩`; this is a consequence of periodicity, not the periodicity predicate itself.
- **Pointwise periodicity at a single `x`**: `VTask.Periodic f c` is a *universal* statement over all `x`; it must not be confused with the pointwise equation `f (x + c) = f x` holding only at one particular `x`.