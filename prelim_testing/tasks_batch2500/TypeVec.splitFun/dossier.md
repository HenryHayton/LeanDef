## VTask.splitFun

### Object

`VTask.splitFun` constructs an arrow (a family of functions indexed by a type-vector's positions) between two type-vectors of length `n + 1` by combining two separate pieces of data: a vector-arrow acting on the first `n` components (the "drop" portion) and an ordinary function acting on the final component (the "last" position). It is the canonical way to assemble an arrow between length-`(n+1)` type-vectors out of separately specified behavior on the tail and the head.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.splitFun : {n : ℕ} -> {α : TypeVec.{u_1} (n + 1)} -> {α' : TypeVec.{u_2} (n + 1)} -> (f : α.drop.Arrow α'.drop) -> (g : α.last → α'.last) -> α.Arrow α'
<!-- PINNED-SIGNATURE:END -->


```
VTask.splitFun : {n : ℕ} -> {α : TypeVec.{u_1} (n + 1)} -> {α' : TypeVec.{u_2} (n + 1)} -> (f : α.drop.Arrow α'.drop) -> (g : α.last → α'.last) -> α.Arrow α'
```

The implicit argument `n` is the length of the "drop" portion of the type-vectors. The implicit arguments `α` and `α'` are the source and target type-vectors, each of length `n + 1`. The explicit argument `f` is an arrow between the drop (first-`n`-component) portions of `α` and `α'`; it specifies what happens at every position except the last. The explicit argument `g` is an ordinary function from the last type of `α` to the last type of `α'`; it specifies what happens at the final position.

### Conventions

There are no declared junk-value or boundary conventions for this definition: it is a total function on well-typed inputs with no distinguished degenerate cases.

### Worked examples

- Claim: For any drop-arrow `f` and last-function `g`, applying `VTask.splitFun f g` and then extracting the drop component via `dropFun` recovers `f` exactly.

- Claim: For any drop-arrow `f` and last-function `g`, applying `VTask.splitFun f g` and then extracting the last component via `lastFun` recovers `g` exactly.

- Claim: Every arrow `h : α ⟹ α'` between length-`(n+1)` type-vectors satisfies `VTask.splitFun (dropFun h) (lastFun h) = h`; i.e., `splitFun` together with `dropFun`/`lastFun` provides a perfect splitting.

- Claim: `VTask.splitFun` is injective in both arguments simultaneously: if `VTask.splitFun f g = VTask.splitFun f' g'` then `f = f'` and `g = g'`.

### Boundaries

- When `n = 0`, the "drop" portion is a type-vector of length 0, so `f` is an arrow between empty type-vectors (trivially determined). The entire content of the assembled arrow comes from `g`.
- The construction is well-defined for any universe levels `u_1` and `u_2`; source and target type-vectors may live in different universes.
- When `f` and `g` are both identity-like (identity arrow and identity function), `VTask.splitFun f g` is the identity arrow on `α`.

### Not to be confused with

- `TypeVec.appendFun` (`α ⊗ β`-style): assembles an arrow for append-style type-vectors where the source and target last types may vary independently, whereas `VTask.splitFun` works for arbitrary source/target type-vectors without requiring them to be presented as appends.
- `TypeVec.dropFun`: the projection that *extracts* the drop component from an existing arrow — the inverse direction of what `VTask.splitFun` does for the drop part.
- `TypeVec.lastFun`: the projection that *extracts* the last-component function from an existing arrow — the inverse direction of what `VTask.splitFun` does for the last part.
