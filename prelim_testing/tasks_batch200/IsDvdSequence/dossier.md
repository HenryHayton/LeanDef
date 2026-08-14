## VTask.IsDvdSequence

### Object

A function `f : α → β` between two types each equipped with a divisibility relation is called a **divisibility sequence** if it preserves divisibility: whenever `a` divides `b` in `α`, it follows that `f a` divides `f b` in `β`. This is a morphism-like condition that says divisibility is respected by `f` in the forward direction.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsDvdSequence : {α : Type u_1} -> {β : Type u_2} -> [Dvd α] -> [Dvd β] -> (f : α → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first two implicit arguments are the types `α` and `β` of the domain and codomain, respectively. The next two arguments are typeclass witnesses supplying a divisibility relation on `α` and on `β`. The final explicit argument `f` is the function under scrutiny, mapping elements of `α` to elements of `β`.

### Conventions

No special junk-value or boundary conventions are declared for this predicate: it is a universally quantified proposition whose meaning is entirely determined by the divisibility structures on `α` and `β`.

### Worked examples

- Claim: The identity function on any type with a divisibility relation is a divisibility sequence (`VTask.IsDvdSequence (id : ℕ → ℕ)`).

- Claim: The Fibonacci function `Nat.fib : ℕ → ℕ` is a divisibility sequence, meaning that if `m ∣ n` then `Nat.fib m ∣ Nat.fib n`.

- Claim: For any monoid `β`, a constant function `fun _ : α ↦ b` is a divisibility sequence, since `b ∣ b` always holds and the output never changes.

- Claim: If `f : α → β` and `g : α → β` are both divisibility sequences into a commutative monoid, then their pointwise product `f * g` is also a divisibility sequence.

### Boundaries

- The predicate is vacuously satisfied on any type `α` with a divisibility relation that has no divisibility pairs (i.e., the relation is empty), because the universal quantification `∀ a b, a ∣ b → ...` has no applicable instances.
- When `α = β` and the divisibility relations coincide, the identity function always satisfies the predicate.
- Constant functions from any `α` into a monoid satisfy the predicate because a fixed element always divides itself.
- The predicate does not require `f` to be injective, surjective, or a monoid homomorphism — it is solely a one-directional divisibility-preservation condition.

### Not to be confused with

- `VTask.IsStrongDvdSequence`: a strictly stronger condition (defined for `ℕ → ℕ`) requiring that `f a ∣ f b` implies `a ∣ b` as well; every strong divisibility sequence is a divisibility sequence, but not vice versa.
- An order-preserving map: divisibility is a preorder, but `VTask.IsDvdSequence` specifically concerns divisibility, not an arbitrary preorder morphism.
- A ring or monoid homomorphism: such maps preserve divisibility as a consequence of multiplicativity, but `VTask.IsDvdSequence` is weaker and does not require any algebraic structure on `f` beyond the divisibility-preservation property.