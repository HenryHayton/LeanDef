## VTask.comp

### Object

`VTask.comp R S` is the **relational composition** of two set-valued relations `R : α → β` and `S : β → γ`. It is the relation on `α × γ` consisting of all pairs `(a, c)` such that there exists some intermediate element `b : β` with `a` related to `b` by `R` and `b` related to `c` by `S`. This is the standard notion of composition of binary relations, analogous to composition of functions but generalised to allow multiple (or zero) witnesses.

Note that the argument order follows the **category-theory convention**: `R` is applied first (left-to-right), so `VTask.comp R S` means "first `R`, then `S`" — the opposite of the usual mathematical function-composition order `S ∘ R`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> (R : SetRel α β) -> (S : SetRel β γ) -> SetRel α γ
<!-- PINNED-SIGNATURE:END -->


{α β γ : Type} are the source, intermediate, and target types, respectively. `R : SetRel α β` is the first relation, going from `α` to `β`. `S : SetRel β γ` is the second relation, going from `β` to `γ`. The result `SetRel α γ` is the composed relation from `α` to `γ`.

### Conventions

There are no declared junk-value or boundary conventions for this definition: `VTask.comp` is a total operation defined for all relations `R` and `S` of matching types, and every pair `(a, c)` either belongs to the composition (if a witness exists) or does not (if none exists). No degenerate input produces an undefined or conventionally-specified output.

### Worked Examples

- Claim: If `R = {(0,1), (0,2)}` and `S = {(1,10), (2,20)}` (as relations on `Fin`-like types), then `(0, 10)` belongs to `VTask.comp R S` (witnessed by the intermediate element `1`).

- Claim: If `R` is the empty relation `∅ : SetRel α β`, then `VTask.comp R S` is also empty for any `S`, since no intermediate witness can exist.

- Claim: For the identity relation `id_rel` on `β` (where every element is related only to itself), `VTask.comp R id_rel = R` for any `R : SetRel α β`.

- Claim: `VTask.comp` is associative: for relations `R : SetRel α β`, `S : SetRel β γ`, `T : SetRel γ δ`, the relation `VTask.comp (VTask.comp R S) T` equals `VTask.comp R (VTask.comp S T)`.

### Boundaries

- **Empty intermediate type**: If `β` is an uninhabited type (i.e., `β = Empty`), then `VTask.comp R S` is the empty relation for any `R` and `S`, because no witness `b : β` can ever be found.
- **Empty relations**: If either `R` or `S` is the empty relation, then `VTask.comp R S` is empty, since the existential witness fails in either factor.
- **Universal relation**: If both `R` and `S` are the total (universal) relation on their respective types, then `VTask.comp R S` is likewise the total relation (every pair `(a, c)` has a witness).
- **Non-unique witnesses**: A pair `(a, c)` belongs to the composition if *at least one* intermediate `b` exists; there may be many such witnesses.

### Not to be confused with

- **Function composition** (`Function.comp`): That composes functions `f : α → β` and `g : β → γ` in the *right-to-left* order `g ∘ f`; `VTask.comp` uses the *left-to-right* (category-theory) order and works with relations rather than functions.
- **`SetRel.trans` or relational transitivity closure**: The transitive closure of a relation repeatedly composes a relation with *itself*; `VTask.comp R S` composes two *distinct* relations exactly once.
- **`Rel.comp` (opposite argument order)**: Some libraries define relational composition with the *opposite* argument order (the mathematical convention `S ∘ R`), so that the second argument is applied first; `VTask.comp` follows the category-theory order where the first argument is applied first.