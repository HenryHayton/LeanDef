## VTask.Antiperiodic

### Object

A function `f : α → β` is **antiperiodic with antiperiod `c`** if translating the input by `c` negates the output: for every element `x` of the domain, `f(x + c) = −f(x)`. In other words, adding `c` to the argument flips the sign of the value. Classic examples are the real sine and cosine functions, which are antiperiodic with antiperiod `π` (since `sin(x + π) = −sin(x)` for all real `x`).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Antiperiodic : {α : Type u_1} -> {β : Type u_2} -> [Add α] -> [Neg β] -> (f : α → β) -> (c : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Antiperiodic : {α : Type u_1} -> {β : Type u_2} -> [Add α] -> [Neg β] -> (f : α → β) -> (c : α) -> Prop`

The implicit type parameters `α` and `β` are the domain and codomain types, respectively. The instance `[Add α]` supplies addition on the domain (needed to form `x + c`), and `[Neg β]` supplies negation on the codomain (needed to form `−f x`). The explicit argument `f` is the function being tested for antiperiodicity. The explicit argument `c` is the proposed antiperiod — the shift amount in the domain.

### Conventions

There are no special junk-value or edge-case conventions declared: the predicate is a universally quantified `Prop` that is simply `False` whenever the antiperiodic condition fails to hold, and no particular value is assigned in degenerate cases.

### Worked examples

- Claim: `VTask.Antiperiodic Real.sin π` holds, i.e., `sin(x + π) = −sin(x)` for all real `x`.

- Claim: `VTask.Antiperiodic Real.cos π` holds, i.e., `cos(x + π) = −cos(x)` for all real `x`.

- Claim: If `f` is antiperiodic with antiperiod `c`, then `f` is periodic with period `2c`, because applying the antiperiodic shift twice gives `f(x + 2c) = −f(x + c) = −(−f(x)) = f(x)`.

- Claim: For an antiperiodic function `f` with antiperiod `c` satisfying `f 0 = 0`, we have `f(n · c) = 0` for every natural number `n`.

### Boundaries

- When `c = 0`: the condition reduces to `f x = −f x` for all `x`, which (in a type where negation is involutive and the only self-negative element is zero) forces `f` to be identically zero. This is not excluded; the predicate is simply very restrictive.
- When `β` has trivial negation (e.g., negation is the identity): antiperiodicity coincides with ordinary periodicity.
- The predicate makes sense for any types carrying `Add` on the domain and `Neg` on the codomain; it does not require a group structure, so cancellation laws need not hold.
- Applying the antiperiod shift twice yields a periodic function: `f(x + 2c) = f(x)` whenever `Neg` is involutive (e.g., in a group).

### Not to be confused with

- **`Function.Periodic`**: periodicity requires `f(x + c) = f(x)`, not `f(x + c) = −f(x)`; antiperiodic functions with involutive negation are periodic with period `2c`, but not generally with period `c`.
- **`Function.Semiconj`** or **`Function.Commute`**: entirely different notions relating two functions via conjugation or commutation, not the sign-flip translation identity.
- **odd functions** (`f(−x) = −f(x)`): these satisfy a reflection symmetry about zero, whereas antiperiodicity is a translation symmetry combined with negation.