## VTask.update

### Object

Given a dependent function `f : (a : α) → β a`, a distinguished point `a' : α`, and a new value `v : β a'`, `VTask.update f a' v` is the dependent function that agrees with `f` everywhere except possibly at `a'`, where it returns `v` instead. In other words, it is the result of "overwriting" `f` at the single point `a'` with the value `v`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.update : {α : Sort u} -> {β : α → Sort v} -> [DecidableEq α] -> (f : (a : α) → β a) -> (a' : α) -> (v : β a') -> (a : α) -> β a
<!-- PINNED-SIGNATURE:END -->


`{α : Sort u} -> {β : α → Sort v} -> [DecidableEq α] -> (f : (a : α) → β a) -> (a' : α) -> (v : β a') -> (a : α) -> β a`

The universe-polymorphic index type `α` is the domain of the function being updated. The dependent codomain family `β` assigns a type to each index. The `DecidableEq α` instance allows equality comparisons on `α`. The argument `f` is the original dependent function. The argument `a'` is the point at which the value is to be replaced. The argument `v` is the new value to install at `a'`. The final argument `a` is the point at which the resulting function is being evaluated.

### Conventions

When the evaluation point `a` equals the update point `a'`, the result is the new value `v` (transported along the proof of equality so that its type matches `β a`). When `a ≠ a'`, the result is simply `f a`. No junk values arise because the function is total and the two cases are exhaustive.

### Worked examples

- Claim: `VTask.update (fun n : Fin 3 => n.val) ⟨1, by omega⟩ 42 ⟨1, by omega⟩ = 42`

- Claim: `VTask.update (fun n : Fin 3 => n.val) ⟨1, by omega⟩ 42 ⟨0, by omega⟩ = 0`

- Claim: For any function `f : Bool → Nat`, `VTask.update f true 7 false = f false`.

- Claim: For any function `f : Bool → Nat`, `VTask.update f true 7 true = 7`.

### Boundaries

- **Evaluation at the update point**: `VTask.update f a' v a'` always returns `v`, regardless of what `f a'` was. The original value at `a'` is completely discarded.
- **Evaluation away from the update point**: For any `a` with `a ≠ a'`, `VTask.update f a' v a = f a` exactly; the update has no effect elsewhere.
- **Self-update**: If `v = f a'`, then `VTask.update f a' v` is extensionally equal to `f` (updating with the existing value changes nothing).
- **Double update**: Updating at the same point twice, `VTask.update (VTask.update f a' v₁) a' v₂`, yields the same result as a single update `VTask.update f a' v₂`; the inner update is overwritten.
- **Non-dependent case**: When `β` is a constant family (i.e., `β a = γ` for all `a`), the definition specialises to ordinary function update on a non-dependent function.

### Not to be confused with

- `Function.updateFinset`: updates a dependent function on an entire finite set of indices simultaneously, not just a single point.
- `Finsupp.update`: a version of single-point update specialised to finitely-supported functions, carrying additional finiteness bookkeeping.
- Function extension by cases (`dite` / `if-then-else`): a raw conditional expression lacking the named-update structure and the associated lemma library.
