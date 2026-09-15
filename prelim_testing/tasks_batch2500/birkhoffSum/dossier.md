## Object

Given a dynamical system on a type α — a self-map `f : α → α` — and an observable `g : α → M` taking values in an additive commutative monoid, the **Birkhoff sum** (also called an ergodic sum or orbit sum) accumulates the values of `g` along the first `n` steps of the forward orbit of a point `x`. Concretely, it is the finite sum `g(x) + g(f x) + g(f²x) + ⋯ + g(f^{n-1}x)` (with the convention that the empty sum for `n = 0` is zero). This is the central object in ergodic theory, where time averages are formed by dividing such sums by `n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.birkhoffSum : {α : Type u_1} -> {M : Type u_2} -> [AddCommMonoid M] -> (f : α → α) -> (g : α → M) -> (n : ℕ) -> (x : α) -> M
<!-- PINNED-SIGNATURE:END -->


`VTask.birkhoffSum : {α : Type u_1} -> {M : Type u_2} -> [AddCommMonoid M] -> (f : α → α) -> (g : α → M) -> (n : ℕ) -> (x : α) -> M`

The type `α` is the phase space; `M` is the value space, required to carry the structure of an additive commutative monoid so that finite sums make sense. The argument `f` is the dynamical map (iterated to generate the orbit). The argument `g` is the observable whose values are accumulated. The argument `n` is the number of orbit points to include (equivalently, the number of iterates starting from the 0-th). The argument `x` is the initial point of the orbit.

## Conventions

When `n = 0` the sum is empty and the result is the zero element of `M`; no special case needs to be declared because this follows from the empty-sum convention of `AddCommMonoid`.

## Worked examples

- Claim: `VTask.birkhoffSum id (fun n => n) 0 (7 : ℕ) = 0` (zero steps, empty sum)
  ```lean
  example : VTask.birkhoffSum id (fun n => n) 0 (7 : ℕ) = 0 := by decide
  ```

- Claim: `VTask.birkhoffSum id (fun n => n) 1 (42 : ℕ) = 42` (one step, just the initial value)
  ```lean
  example : VTask.birkhoffSum id (fun n => n) 1 (42 : ℕ) = 42 := by decide
  ```

- Claim: `VTask.birkhoffSum id (fun n => n) 4 (0 : ℕ) = 6` (four steps of the identity on ℕ starting at 0: 0+0+0+0 = 0... wait, identity fixes every point, so g(f^k 0) = k-th iterate of id at 0 = 0 for all k; this sums to 0). Actually let us use a non-identity map. Using `Nat.succ` as `f` and `id` as `g`, the orbit of 2 for 3 steps visits 2, 3, 4, summing to 9.
  ```lean
  example : VTask.birkhoffSum Nat.succ id 3 2 = 9 := by decide
  ```

- Claim: For a fixed point `x` of `f`, `VTask.birkhoffSum f g n x = n • g x` (the sum reduces to scalar multiplication).

- Claim: `VTask.birkhoffSum f g (m + n) x = VTask.birkhoffSum f g m x + VTask.birkhoffSum f g n (f^[m] x)` (the sum over `m + n` steps splits into the sum over the first `m` steps plus the sum over the next `n` steps starting from the `m`-th iterate).

## Boundaries

- At `n = 0`: the result is the zero element of `M`, regardless of `f`, `g`, and `x`.
- At `n = 1`: the result equals `g x`, the single evaluation at the starting point.
- When `f` is the identity map, every orbit is constant at `x`, so the result is `n • g x`.
- When `g` is the constant zero function, the result is `0` for all `n` and `x`.
- The function is defined for all natural numbers `n`; there is no upper bound or domain restriction.

## Not to be confused with

- **Birkhoff average**: the Birkhoff sum divided by `n`; this is the time average, not the accumulated sum itself.
- **`∑ k in Finset.range n, g k`**: a plain finite sum over the natural numbers 0 through n-1, with no dynamical iteration involved; `VTask.birkhoffSum` inserts the iterated map `f^[k]` before applying `g`.
- **`VTask.birkhoffSum f g n (f x)`**: the Birkhoff sum started one step later; it differs from `VTask.birkhoffSum f g n x` by replacing `g x` with `g (f^[n] x)` (as captured by the theorem about the difference of consecutive starts).