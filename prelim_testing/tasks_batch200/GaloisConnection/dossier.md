## VTask.GaloisConnection

### Object

A Galois connection between two preordered sets is a pair of order-preserving maps, a "lower adjoint" `l : α → β` and an "upper adjoint" `u : β → α`, satisfying the adjointness condition: for every `a : α` and `b : β`, the inequality `l a ≤ b` holds in `β` if and only if the inequality `a ≤ u b` holds in `α`. Equivalently, `l` is left adjoint to `u` in the sense of order theory. Such pairs arise throughout mathematics whenever one has a "best approximation" in each direction between two ordered structures — for instance, the floor and ceiling functions on real numbers viewed as maps between the integers and reals, or pushforward and pullback of ideals along a ring map.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.GaloisConnection : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (l : α → β) -> (u : β → α) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.GaloisConnection : {α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (l : α → β) -> (u : β → α) -> Prop
```

The implicit type arguments `α` and `β` are the carrier types of the two preordered sets. The instance arguments supply the preorder structure on each carrier. The explicit argument `l` is the **left adjoint** ("lower adjoint"), a function from `α` to `β`; it is the map that moves "upward" in the adjunction. The explicit argument `u` is the **right adjoint** ("upper adjoint"), a function from `β` back to `α`; it is the map that moves "downward" in the adjunction. The proposition asserted is that `l` and `u` form a Galois connection, i.e., that `l a ≤ b ↔ a ≤ u b` for all elements `a` and `b`.

### Conventions

No junk-value or out-of-domain conventions are declared for this definition: it is a universally quantified Prop over all elements of both preordered types, and the predicate is total — every pair of functions `(l, u)` either satisfies it or does not.

### Worked examples

- Claim: The pair `(id, id)` forms a Galois connection on any preorder, since `id a ≤ b ↔ a ≤ id b` is trivially true.

- Claim: For the natural-number division Galois connection, `l n = n * k` (multiplication by a fixed `k > 0`) and `u m = m / k` (floor division) form a Galois connection on `ℕ` with the usual order, because `n * k ≤ m ↔ n ≤ m / k`.

- Claim: The pair `(Ideal.map f, Ideal.comap f)` for a ring homomorphism `f` is a Galois connection between the ideal lattices of the source and target rings (with ideals ordered by inclusion).

- Claim: For the set-relation image/core pair, `(R.image, R.core)` is a Galois connection for any relation `R`, reflecting the adjointness of direct and inverse image.

### Boundaries

- Both `α` and `β` need only be preordered sets (reflexive and transitive order); antisymmetry is not required. In particular, Galois connections make sense on preorders that are not partial orders.
- The condition is symmetric in that swapping `l` and `u` and reversing both orders (passing to the dual preorders) yields another Galois connection, by the `VTask.GaloisConnection.dual` theorem.
- When `α = β` and `l = u = id`, the Galois connection condition reduces to `a ≤ b ↔ a ≤ b`, which is trivially satisfied.
- If the preorder on `α` or `β` is discrete (equality only), the Galois connection condition imposes strong constraints: `l a = b ↔ a = u b`, forcing `l` and `u` to be mutual inverses on their respective images.
- The definition does **not** require `l` or `u` to be monotone; however, monotonicity of both follows as a consequence of the Galois connection condition.

### Not to be confused with

- **Galois insertion**: a Galois connection with the additional property that `l ∘ u = id` (the right adjoint is a section of the left adjoint), giving a stronger "retraction" relationship.
- **Adjoint functors in category theory**: the categorical generalisation; every adjunction between preorder categories (viewed as thin categories) is a Galois connection, but the categorical notion requires functoriality and natural transformations beyond mere order.
- **`GaloisCoinsertion`**: the dual notion to Galois insertion, where instead `u ∘ l = id`, i.e., the left adjoint is a section of the right adjoint.