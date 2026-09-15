## VTask.subtypeNeLift

### Object

Given an index type `ι`, a type family `M` over `ι`, a distinguished index `i₀`, a map `f` defined on all indices *other than* `i₀`, and a chosen value `x` in the fiber `M i₀`, this construction produces a complete dependent function `(i : ι) → M i` that equals `x` at `i₀` and agrees with `f` everywhere else.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subtypeNeLift : {ι : Type u_1} -> [DecidableEq ι] -> {M : ι → Type u_2} -> (i₀ : ι) -> (f : (j : { i // i ≠ i₀ }) → M ↑j) -> (x : M i₀) -> (i : ι) -> M i
<!-- PINNED-SIGNATURE:END -->


The implicit type `ι` is the index type; `DecidableEq ι` is required to decide equality of indices. The type family `M` assigns a type to each index. The explicit argument `i₀` is the distinguished index where the supplied value `x` is placed. The argument `f` is the pre-existing map defined on the subtype of indices strictly different from `i₀`; its domain is the subtype `{i : ι // i ≠ i₀}`. The argument `x` is the chosen value at `i₀`, living in `M i₀`. The final argument `i` is the index at which the resulting dependent function is being evaluated.

### Conventions

At the distinguished index `i₀` the function always returns `x`, regardless of what `f` might do elsewhere. At any index `i` with `i ≠ i₀` the function returns `f ⟨i, h⟩`, using the proof `h : i ≠ i₀` to form the subtype element.

### Worked examples

- Claim: `VTask.subtypeNeLift i₀ f x i₀ = x` for any choice of `i₀`, `f`, and `x`.
  This is the case where `i = i₀`; the result is exactly the supplied fiber value.

- Claim: For `i ≠ i₀`, `VTask.subtypeNeLift i₀ f x i = f ⟨i, h⟩` where `h : i ≠ i₀`.
  This is the complementary case; the result is whatever `f` prescribed for that index.

- Claim: If `φ : ∀ i, M i` is any total dependent function, then `VTask.subtypeNeLift i₀ (fun i => φ i) (φ i₀) = φ`.
  Restricting `φ` to the complement and supplying `φ i₀` as the fiber value reconstructs `φ` exactly.

### Boundaries

When `ι` has exactly one element and `i₀` is that element, the subtype `{i // i ≠ i₀}` is empty, so `f` is vacuously defined (it is a function from the empty type) and the resulting function is entirely determined by `x`. The construction is well-defined in this degenerate case. There are no undefined or partial cases; the function is total for all index types, all families, and all inputs.

### Not to be confused with

- `Function.update`: updates a single index of an *existing* total function to a new value, rather than assembling a new function from a complement-map and a fiber value.
- `Finset.piecewise` / `Set.piecewise`: glues two total functions together on complementary sets; requires both to already be defined everywhere, not just on the complement of a singleton.
- `Pi.single` (or `Pi.mulSingle`): places a chosen value at one index and a canonical default (zero or one) everywhere else, whereas `VTask.subtypeNeLift` uses an arbitrary supplied map on the complement.