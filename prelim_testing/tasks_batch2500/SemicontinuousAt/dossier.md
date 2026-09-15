## 1. Object

`VTask.SemicontinuousAt r x` is the proposition that the binary relation `r : α → β → Prop` is *semicontinuous at the point `x : α`*: for every `y : β` such that `r x y` holds, there exists a neighbourhood of `x` throughout which `r x' y` continues to hold. In other words, every "certificate" `y` witnessed at `x` persists under small perturbations of the domain argument. This is a pointwise stability condition on `r` with respect to the topology of `α`.

The notion unifies several classical concepts: when `β` is a linearly ordered type and `r x y` is `f(x) > y` (strict lower bound), the condition recovers *lower semicontinuity* of the function `f` at `x`; when `r x y` is `f(x) < y`, it recovers *upper semicontinuity*. For set-valued maps (where `r x y` means `y ∈ F(x)`), it recovers *lower hemicontinuity* of the correspondence `F` at `x`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SemicontinuousAt : {α : Type u_1} -> {β : Type u_2} -> [TopologicalSpace α] -> (r : α → β → Prop) -> (x : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.SemicontinuousAt : {α : Type u_1} -> {β : Type u_2} -> [TopologicalSpace α] -> (r : α → β → Prop) -> (x : α) -> Prop
```

The implicit type `α` is the domain, which carries the topology used to form neighbourhoods; `β` is the codomain type with no topology assumed. The instance argument is the topological space structure on `α`. The explicit argument `r` is the binary relation whose semicontinuity is being tested. The explicit argument `x` is the specific point of `α` at which semicontinuity is asserted.

## 3. Conventions

No special junk-value or edge conventions are declared for this definition: it is a universally quantified `Prop` over all `y` satisfying `r x y`, so it is vacuously true when `r x` holds for no `y` at all (i.e., when the fibre of `r` at `x` is empty), and it places no restriction on `β` beyond it being a type.

## 4. Worked Examples

- Claim: A constant relation (one that does not depend on the domain point) is always semicontinuous at every point, because `r x' y` reduces to `r y` for all `x'`.

- Claim: If `r : α → β → Prop` is semicontinuous everywhere (i.e., `Semicontinuous r` holds globally), then in particular `VTask.SemicontinuousAt r x` holds for every `x : α`.

- Claim: If `f : α → γ` is continuous at `x` and `γ` is a linear order, then the relation `r a b := b < f a` (which encodes lower semicontinuity) satisfies `VTask.SemicontinuousAt r x`.

- Claim: `VTask.SemicontinuousAt r x` implies `SemicontinuousWithinAt r s x` for every set `s : Set α`, meaning the at-a-point version is stronger than the within-a-set version.

## 5. Boundaries

- **Empty fibre**: If no `y` satisfies `r x y`, the universal quantification is vacuously true and `VTask.SemicontinuousAt r x` holds automatically, regardless of how `r` behaves near `x`.
- **Indiscrete topology**: In an indiscrete topological space on `α`, the only neighbourhood of `x` is all of `α`, so the condition requires `r x' y` for *all* `x' : α` whenever `r x y`. This is a very strong global condition.
- **Discrete topology**: Every singleton `{x}` is open, so every neighbourhood of `x` contains `x` itself, and the filter `𝓝 x` has `{x}` as a member. The condition becomes trivially satisfied since `r x y` already witnesses the required element in every neighbourhood.
- **No topology on `β`**: The condition imposes no requirements on `β` having a topology; only `α` needs one. This is what allows the notion to generalise set-valued maps as well as real-valued functions.

## 6. Not to be confused with

- **`SemicontinuousWithinAt r s x`**: the weaker variant that only requires `r x' y` for points `x'` in a specified subset `s`, restricted to the subspace neighbourhood filter.
- **`Semicontinuous r`**: the *global* version asserting `VTask.SemicontinuousAt r x` for every `x : α`, not just at a single point.
- **`LowerSemicontinuousAt f x`** / **`UpperSemicontinuousAt f x`**: these are the classical order-theoretic specialisations for a real- (or linearly-ordered-) valued function `f`; they are instances of `VTask.SemicontinuousAt` with specific choices of `r`, not a separate generalisation of it.