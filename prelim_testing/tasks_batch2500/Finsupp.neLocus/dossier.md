## VTask.neLocus

### Object

Given two finitely supported functions `f` and `g` from a type `α` to a type `N` (with zero), `VTask.neLocus f g` is the finite set of elements `x : α` at which `f` and `g` take different values. It is the **disagreement locus** of the two functions: a `Finset α` collecting exactly the points where the two functions differ. Because both `f` and `g` are finitely supported, their disagreement set is automatically finite.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.neLocus : {α : Type u_1} -> {N : Type u_3} -> [DecidableEq α] -> [DecidableEq N] -> [Zero N] -> (f g : α →₀ N) -> Finset α
<!-- PINNED-SIGNATURE:END -->


VTask.neLocus : {α : Type u_1} -> {N : Type u_3} -> [DecidableEq α] -> [DecidableEq N] -> [Zero N] -> (f g : α →₀ N) -> Finset α

- `α` is the index type on which the finitely supported functions are defined.
- `N` is the value type, which must carry a distinguished zero element.
- The `DecidableEq α` instance is needed to form and manipulate the `Finset α` result.
- The `DecidableEq N` instance allows checking whether `f x = g x` at each point.
- The `Zero N` instance specifies what value counts as "not supported" (the default outside finite support).
- `f` and `g` are the two finitely supported functions whose disagreement locus is computed.

### Conventions

There are no junk-value conventions to declare: the definition is total and well-defined for all valid inputs without any edge-case junk assignments.

### Worked examples

- Claim: If `f = g` (the zero finsupp equals the zero finsupp), then `VTask.neLocus f g = ∅`.

- Claim: For `f : Fin 3 →₀ ℕ` that is 1 at position 0 and 0 elsewhere, and `g` the zero function, `VTask.neLocus f g = {0}` — the single point where they differ.

- Claim: `VTask.neLocus f g = VTask.neLocus g f` for all finitely supported `f g`; that is, the locus is symmetric in its two arguments.

- Claim: An element `x : α` belongs to `VTask.neLocus f g` if and only if `f x ≠ g x`.

- Claim: If `f` and `g` agree everywhere (i.e., `f = g`), then `VTask.neLocus f g` is the empty `Finset`.

### Boundaries

- **Both functions are zero**: `VTask.neLocus 0 0 = ∅`, since the two identical zero functions agree everywhere.
- **One function is zero**: `VTask.neLocus f 0` equals the support of `f`, since `f x ≠ 0` exactly on the support of `f`.
- **Disjoint supports**: If `f` and `g` have disjoint supports, then `VTask.neLocus f g = f.support ∪ g.support`, because at every point in either support the two functions disagree (one is nonzero, the other is zero).
- **Identical functions**: For any `f`, `VTask.neLocus f f = ∅` since `f x = f x` everywhere.
- The result is always a subset of `f.support ∪ g.support`; in particular it is always finite.

### Not to be confused with

- `Finsupp.support f`: The support of a single function `f`, recording where `f` is nonzero; `VTask.neLocus f g` generalizes this by comparing two functions rather than one function against zero.
- `(f - g).support`: The support of the pointwise difference, which agrees with `VTask.neLocus f g` when subtraction is available and cancellative, but `VTask.neLocus` is defined even in types without subtraction.
- `Finsupp.eqLocus f g` (if it existed): The complementary set of points where `f` and `g` agree; `VTask.neLocus` records disagreement, not agreement.
