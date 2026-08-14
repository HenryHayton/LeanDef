## VTask.blimsup

### Object

`VTask.blimsup u f p` is the **bounded limit superior** of a function `u : β → α` along a filter `f` on `β`, restricted to those indices where the predicate `p` holds. Concretely, it is the greatest lower bound (infimum) of the set of all values `a` in the lattice `α` such that, eventually along `f`, every `x` satisfying `p x` also satisfies `u x ≤ a`. In other words, it is the smallest asymptotic upper bound on the values `u x` when `p x` is true, as `x` is swept through `f`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.blimsup : {α : Type u_1} -> {β : Type u_2} -> [ConditionallyCompleteLattice α] -> (u : β → α) -> (f : Filter β) -> (p : β → Prop) -> α
<!-- PINNED-SIGNATURE:END -->


The implicit type parameters `α` and `β` are the codomain and domain types, respectively. The instance `[ConditionallyCompleteLattice α]` equips the codomain with enough order structure to form infima. The explicit argument `u` is the function whose asymptotic upper behaviour is being measured. The argument `f` is the filter encoding the notion of "eventually" or "asymptotically" along which the bound is computed. The argument `p` is a predicate on the domain that restricts attention to only those points where `p` is satisfied; values of `u` at points where `p` fails are entirely ignored.

### Conventions

When the predicate `p` is identically `False`, every element of the lattice is vacuously an eventual upper bound (the implication `False → u x ≤ a` always holds), so the infimum of the entire lattice is taken, yielding the bottom element `⊥` of `α`. When the predicate `p` is identically `True`, the bounded limit superior coincides with the ordinary (unbounded) `limsup u f`.

### Worked examples

- Claim: For the identically-False predicate, `VTask.blimsup u f (fun _ => False) = ⊥` for any `u` and `f` (the blimsup over an empty restriction is the bottom of the lattice).

- Claim: For the identically-True predicate, `VTask.blimsup u f (fun _ => True) = Filter.limsup u f` for any `u` and `f` (restricting to everything recovers the ordinary limsup).

- Claim: If `p x → q x` for all `x`, then `VTask.blimsup u f p ≤ VTask.blimsup u f q` (monotonicity in the predicate: a wider predicate can only raise the limsup).

- Claim: For any predicates `p` and `q`, `VTask.blimsup u f p ⊔ VTask.blimsup u f (¬p ·) = Filter.limsup u f` (the two complementary bounded limsups together account for the full limsup).

### Boundaries

- **Vacuous predicate (`p` always False):** The defining set of upper bounds becomes all of `α` (every `a` satisfies the vacuous implication), so the infimum is `⊥`. This is the minimum possible value.
- **Universal predicate (`p` always True):** The restriction disappears and `VTask.blimsup u f (fun _ => True)` equals `Filter.limsup u f`.
- **Finer filter (larger `f` in the order):** A larger filter imposes more eventual constraints, so `VTask.blimsup u f p ≤ VTask.blimsup u g p` whenever `f ≤ g` in the filter order (i.e., `f` is finer); making the filter coarser can only raise or keep the value.
- **Pointwise-smaller function:** If `p x → u x ≤ v x` for all `x`, then `VTask.blimsup u f p ≤ VTask.blimsup v f p`.
- **Predicate conjunction:** Intersecting the predicate (`p x ∧ q x`) gives a value ≤ that of either factor predicate alone.
- **Predicate disjunction:** The join `VTask.blimsup u f p ⊔ VTask.blimsup u f q ≤ VTask.blimsup u f (fun x => p x ∨ q x)`, and the two complementary halves exactly reconstruct `limsup`.

### Not to be confused with

- **`Filter.limsup u f`** — the ordinary (unbounded) limit superior, which is exactly `VTask.blimsup u f (fun _ => True)`; it does not accept a restricting predicate.
- **`Filter.bliminf u f p`** — the dual bounded limit inferior, defined as a supremum of eventual lower bounds restricted by `p`; `bliminf` and `blimsup` are order-duals of each other.
- **`Filter.limsup` applied after filtering** — one might try to pre-filter the domain by `p` and then take limsup, but that is not the same construction; `VTask.blimsup` works directly with implications inside the eventual condition rather than restricting the filter.
