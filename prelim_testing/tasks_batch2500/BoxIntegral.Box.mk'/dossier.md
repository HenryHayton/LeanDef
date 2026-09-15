## VTask.mk'

### Object
A constructor that builds a box (or signals failure) from two corner functions. Given lower-bound function `l` and upper-bound function `u` on an index type `ι`, it returns the axis-aligned half-open box `{x | ∀ i, l i < x i ≤ u i}` as an element of `WithBot (BoxIntegral.Box ι)`. If every coordinate satisfies `l i < u i` the result is the actual box `⟨l, u, _⟩` lifted into `WithBot`; otherwise (at least one coordinate has `u i ≤ l i`) the result is `⊥`, representing the empty or degenerate case. In either case, the value interpreted as a subset of `ι → ℝ` equals `∏ i, Ioc (l i) (u i)` (the Cartesian product of half-open intervals).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk' : {ι : Type u_1} -> (l u : ι → ℝ) -> WithBot (BoxIntegral.Box ι)
<!-- PINNED-SIGNATURE:END -->


The index type `ι` is implicit and classifies the coordinates of the box. The argument `l : ι → ℝ` supplies the lower bound at each coordinate; the argument `u : ι → ℝ` supplies the upper bound at each coordinate.

### Conventions

When at least one coordinate has `u i ≤ l i` (the box is empty or degenerate), the function returns `⊥` rather than an ill-formed box; there is no partial function or error — `⊥` is the canonical junk value for this situation inside `WithBot (BoxIntegral.Box ι)`.

### Worked examples

- Claim: For `l = fun _ : Fin 2 => (0 : ℝ)` and `u = fun _ : Fin 2 => 1`, `VTask.mk' l u` equals the box with lower corner `l` and upper corner `u`.

- Claim: If `u i ≤ l i` for some `i`, then `VTask.mk' l u = ⊥`. For example, with a single index `Fin 1`, setting `l _ = 1` and `u _ = 0` gives `⊥` because `u 0 = 0 ≤ 1 = l 0`.

- Claim: The set interpretation `(VTask.mk' l u : Set (Fin 1 → ℝ))` equals `Set.pi Set.univ (fun i => Set.Ioc (l i) (u i))` for any `l u : Fin 1 → ℝ`, regardless of whether the box is empty or not.

- Claim: `VTask.mk' l u = ⊥ ↔ ∃ i, u i ≤ l i`.

### Boundaries

- If `l i = u i` for some (or all) `i`, the interval `Ioc (l i) (u i)` is empty, so the function returns `⊥` (not a zero-volume box).
- If every coordinate strictly satisfies `l i < u i`, the result is the coercion of the genuine `Box ι` value, never `⊥`.
- The index type `ι` may be empty; in that case the condition `∀ i, l i < u i` is vacuously true and the result is the (unique, universe-spanning) box over the empty index type, coerced into `WithBot`.
- The set interpretation `∏ i, Ioc (l i) (u i)` holds uniformly: when the result is `⊥` this product is empty (because at least one `Ioc (l i) (u i)` is empty), matching the convention that `⊥` represents the empty box.

### Not to be confused with

- `BoxIntegral.Box.mk` (the raw structure constructor): requires a proof that `∀ i, l i < u i` as an explicit argument and always produces a `Box ι`, not a `WithBot (Box ι)`.
- `WithBot.some` / coercion `↑b`: lifts an already-constructed `Box ι` into `WithBot (Box ι)` without performing any validity check on corners.
- `Set.pi univ (fun i => Set.Ioc (l i) (u i))`: the purely set-theoretic Cartesian product, which is always defined as a set and carries no box structure.