## VTask.prevFixed

### 1. Object

Given a monotone self-map `f` on a complete lattice `α` and a point `x` satisfying `f x ≤ x` (i.e., `x` is a post-fixed point of `f`), `VTask.prevFixed f x hx` is the **greatest fixed point of `f` that is less than or equal to `x`**. It is an element of the subtype `Function.fixedPoints f` (i.e., it carries a proof that applying `f` to it returns it unchanged), and it is the largest such fixed point below `x`.

### 2. Signature

```
VTask.prevFixed : {α : Type u} -> [CompleteLattice α] -> (f : α →o α) -> (x : α) -> (hx : f x ≤ x) -> ↑(Function.fixedPoints ⇑f)
```

- `α` — the underlying type, inferred; must carry a `CompleteLattice` instance.
- `[CompleteLattice α]` — the complete lattice structure on `α`, found automatically.
- `f : α →o α` — a monotone self-map (an `OrderHom`).
- `x : α` — a post-fixed point: a point at which `f x ≤ x`.
- `hx : f x ≤ x` — the proof that `x` is a post-fixed point.
- **Returns** an element of `Function.fixedPoints f`, i.e., a pair `⟨p, hp⟩` where `p : α` and `hp : f p = p`, with the property that `p` is the greatest fixed point of `f` satisfying `p ≤ x`.

### 3. Conventions

The function is total: it is defined for every monotone map `f` on a complete lattice and every post-fixed point `x` (i.e., every `x` with `f x ≤ x`). No junk-value conventions are needed because the domain is exactly the triples `(f, x, hx)` for which the result is meaningful. There are no declared edge-case conventions beyond this totality.

### 4. Worked examples

- Claim: For any monotone map `f` on a complete lattice and post-fixed point `x`, the underlying value of `VTask.prevFixed f x hx` is ≤ `x`.
  (This follows from `prevFixed_le`: the coercion of `f.prevFixed x hx` into `α` satisfies `↑(f.prevFixed x hx) ≤ x`.)

- Claim: For any monotone map `f` on a complete lattice, any post-fixed point `x`, and any fixed point `y` of `f` with `↑y ≤ x`, we have `y ≤ f.prevFixed x hx` as fixed points.
  (This is `le_prevFixed`: `VTask.prevFixed f x hx` is the *greatest* fixed point below `x`, so every fixed point below `x` is below it.)

- Claim: The element returned by `VTask.prevFixed f x hx` is itself a fixed point of `f`, i.e., its underlying value `p` satisfies `f p = p`.
  (This is immediate from the return type being `Function.fixedPoints f`.)

### 5. Boundaries

- **When `f = id` (identity map):** Every point is a fixed point, and `x` is itself a post-fixed point (since `id x = x ≤ x`). The result is `x` itself coerced as a fixed point, since `x` is the greatest fixed point ≤ `x`.
- **When `x = ⊥` (bottom element):** The condition `f ⊥ ≤ ⊥` forces `f ⊥ = ⊥`, so `⊥` is itself a fixed point. The result is `⊥` as the (only) fixed point ≤ `⊥`.
- **When `x = ⊤` (top element):** The condition `f ⊤ ≤ ⊤` is always true since `⊤` is the greatest element. The result is the greatest fixed point of `f` overall (i.e., the greatest fixed point in the entire lattice), since there is no upper bound constraint beyond `⊤`.
- **Existence is guaranteed:** By the Knaster–Tarski theorem, monotone maps on complete lattices always have fixed points, and the greatest fixed point below any post-fixed point always exists; thus `VTask.prevFixed` is well-defined in all cases.

### 6. Not to be confused with

- **`OrderHom.gfp` (greatest fixed point):** The overall greatest fixed point of `f` in `α`, with no upper-bound constraint; `VTask.prevFixed` is the greatest fixed point *below a specified post-fixed point `x`*.
- **`OrderHom.nextFixed`:** The dual construction — the *least* fixed point of `f` that is *greater than or equal to* a given pre-fixed point (where `x ≤ f x`); `VTask.prevFixed` goes in the opposite direction.
- **`Function.fixedPoints`:** The *set* of all fixed points of `f`; `VTask.prevFixed` picks out a specific *element* of this set, namely the greatest one below `x`.
