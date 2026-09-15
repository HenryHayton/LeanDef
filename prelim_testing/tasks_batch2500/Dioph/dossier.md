## VTask.Dioph

### Object

A set `S` of functions from an index type `α` into the natural numbers — equivalently, a set of "tuples" of natural numbers indexed by `α`, i.e., a subset of `ℕ^α` — is called **Diophantine** if there is a multivariate polynomial `p`, defined over the extended index set `α ⊕ β` for some auxiliary type `β`, such that a tuple `v : α → ℕ` belongs to `S` if and only if the system `p(v, t) = 0` has at least one solution `t : β → ℕ`. In other words, membership in `S` is exactly captured by the solvability of a single polynomial equation over the natural numbers, after existentially quantifying over some extra "hidden" variables.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Dioph : {α : Type u} -> (S : Set (α → ℕ)) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit argument `α` is the index type parameterising the tuples; it specifies in how many (and which) coordinates the set lives. The explicit argument `S` is the set of natural-number-valued functions on `α` whose Diophantine character is being asserted.

### Conventions

There are no special junk-value or out-of-domain conventions for this predicate: it is a universally-quantified existential statement over all possible polynomials and witness types, and it is defined for every set `S` of functions `α → ℕ`.

### Worked examples

- Claim: The set `{v : Fin 2 → ℕ | v 0 = v 1}` is Diophantine, witnessed by the polynomial `p(x, y) = x - y` with no auxiliary variables.

- Claim: The set `{v : Fin 2 → ℕ | v 0 ≤ v 1}` is Diophantine, because `v 0 ≤ v 1` iff there exists a natural number `t` with `v 1 = v 0 + t`, which is a polynomial equation in `v 0`, `v 1`, and `t`.

- Claim: The set `{v : Fin 2 → ℕ | v 0 ∣ v 1}` is Diophantine, because divisibility is equivalent to the existence of a natural-number quotient, expressible as `v 1 = v 0 * t` for some `t`.

- Claim: If `S` and `S'` are both Diophantine subsets of `ℕ^α`, then `S ∪ S'` is also Diophantine. (This follows by multiplying the two defining polynomials: `p · q = 0` iff `p = 0` or `q = 0`.)

- Claim: Every finite intersection of Diophantine sets is Diophantine, since simultaneously requiring several polynomial equations is equivalent to requiring the sum of their squares to vanish.

### Boundaries

- The empty set over any index type is Diophantine (take the polynomial `p = 1`, which has no natural-number root).
- The full set `ℕ^α` is Diophantine (take the polynomial `p = 0`).
- The definition requires the polynomial to be zero at the witness, not merely at the projection; the auxiliary type `β` can be empty (giving no hidden variables) or arbitrarily large.
- The universe level of `β` is required to match that of `α` (both live in `Type u`), which is a technical Lean constraint, not a mathematical one.
- Because the natural numbers are used (not the integers), the subtraction in `ℕ` is truncated, but the polynomial ring `Poly` is constructed to handle this correctly as a ring of polynomials over `ℕ`.

### Not to be confused with

- `VTask.DiophFn`: asserts that a *function* `(α → ℕ) → ℕ` is Diophantine (its graph is a Diophantine set), rather than a set directly.
- `VTask.DiophList.forall`: a statement that a *list* of sets is simultaneously Diophantine, i.e., the conjunction of Diophantine conditions is again Diophantine.
- Classical Diophantine equations over `ℤ`: `VTask.Dioph` works specifically over `ℕ`, so "no solution" and "solution" must be interpreted in the non-negative integers.