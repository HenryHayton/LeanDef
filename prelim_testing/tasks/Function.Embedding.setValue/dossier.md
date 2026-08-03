## 1. Object

Given an injective function (embedding) `f : α ↪ β`, a point `a : α`, and a target value `b : β`, `VTask.setValue f a b` produces a new embedding `α ↪ β` that agrees with `f` everywhere except possibly at `a` (and at most one other point), and whose value at `a` is exactly `b`. The modification is performed in the most conservative way that preserves injectivity: if `b` is already the image of some point `a' ≠ a` under `f`, then `f(a')` and `f(a)` are swapped — `a'` now maps to the old `f(a)`, and `a` maps to `b`; otherwise only the value at `a` is changed.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.setValue : {α : Sort u_1} -> {β : Sort u_2} -> (f : α ↪ β) -> (a : α) -> (b : β) -> [(a' : α) → Decidable (a' = a)] -> [(a' : α) → Decidable (f a' = b)] -> α ↪ β
<!-- PINNED-SIGNATURE:END -->


`VTask.setValue : {α : Sort u_1} -> {β : Sort u_2} -> (f : α ↪ β) -> (a : α) -> (b : β) -> [(a' : α) → Decidable (a' = a)] -> [(a' : α) → Decidable (f a' = b)] -> α ↪ β`

The implicit `α` and `β` are the domain and codomain sorts. `f` is the embedding being modified. `a` is the point at which the value is to be changed. `b` is the new prescribed image of `a`. The first instance argument provides decidable equality for testing whether an arbitrary point `a'` equals `a`. The second instance argument provides decidable equality for testing whether the image `f a'` equals `b`, which is needed to detect collisions.

## 3. Conventions

The new embedding maps `a` to `b` unconditionally. If some other point `a'` already satisfies `f a' = b`, then `a'` is redirected to the old `f a`, effecting a swap; otherwise all other points keep their original images under `f`.

## 4. Worked examples

- Claim: For any embedding `f`, `VTask.setValue f a b` evaluated at `a` equals `b` (the prescribed value is placed at the designated point).

- Claim: If `c ≠ a` and `f c ≠ b`, then `VTask.setValue f a b c = f c` (points that are neither `a` nor a collision point are left unchanged).

- Claim: For `f : Fin 3 ↪ Fin 5` defined by `f i = i` (inclusion), setting the value at `0` to `2` gives `VTask.setValue f 0 2 0 = 2`.

- Claim: Using the same `f`, after setting `0 ↦ 2`, the point `2` (which was mapped to `2` by `f`) is now redirected: `VTask.setValue f 0 2 2 = f 0 = 0`, so the old image of `0` fills the slot vacated by `2`.

## 5. Boundaries

- If `b = f a` (the value is already correct), the embedding is unchanged at `a`, and since no other point is mapped to `b` by `f` except via injectivity, effectively the entire embedding is unchanged.
- If `b` is already the image of exactly one other point `a'` under `f`, the values at `a` and `a'` are swapped; no other points are affected.
- Since `f` is injective, at most one point `a'` can satisfy `f a' = b`, so the swap is always between at most two points.
- The result is always an injection (embedding), regardless of the choice of `b`; the construction guarantees this.
- The instances for decidability are required explicitly; without them the construction cannot check for collisions computationally.

## 6. Not to be confused with

- `Function.Embedding.trans`: composes two embeddings rather than modifying a single value.
- `Function.update` (for plain functions): also modifies a function at one point, but does not preserve injectivity and does not perform any swap to avoid collisions.
- `Equiv.swap`: permutes two values in an equivalence, but operates on bijections between types rather than injections, and swaps two prescribed points rather than resolving a collision automatically.