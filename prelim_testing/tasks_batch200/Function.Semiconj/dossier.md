## 1. Object

A predicate on three functions that expresses a **semiconjugacy relation**: `VTask.Semiconj f ga gb` holds when the function `f : α → β` intertwines the self-map `ga` on `α` with the self-map `gb` on `β`, in the sense that applying `f` after `ga` always gives the same result as applying `gb` after `f`. Concretely, this means `f ∘ ga = gb ∘ f` as functions, witnessed pointwise by the equation `f (ga x) = gb (f x)` for every `x : α`.

Intuitively, `f` "translates" the dynamics of `ga` into the dynamics of `gb`: wherever `ga` moves a point in `α`, `f` tracks that movement faithfully in `β` via `gb`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Semiconj : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> (ga : α → α) -> (gb : β → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first argument `f` is the **intertwining map** from the source type `α` to the target type `β`; it is the map that conjugates the two self-maps. The second argument `ga` is the **self-map on the source** type `α` being semiconjugated. The third argument `gb` is the **self-map on the target** type `β` to which `ga` is being semiconjugated.

## 3. Conventions

No special junk-value or boundary conventions are declared: the predicate is a universally-quantified equality of terms in `β`, which is always a well-formed `Prop` for any three functions of the correct types, with no edge-case overrides.

## 4. Worked examples

- Claim: `VTask.Semiconj id ga ga` holds for any `ga : α → α` — the identity function always semiconjugates any self-map to itself.

- Claim: `VTask.Semiconj (fun _ : α => b₀) ga (fun _ => b₀)` holds for any constant function whose value `b₀` is a fixed point of `gb` — a constant function semiconjugates any `ga` to a self-map that fixes `b₀`.

- Claim: If `h₁ : VTask.Semiconj f ga gb` and `h₂ : VTask.Semiconj g gb gc`, then `VTask.Semiconj (g ∘ f) ga gc` — semiconjugacies compose: if `f` intertwines `ga` with `gb`, and `g` intertwines `gb` with `gc`, then `g ∘ f` intertwines `ga` with `gc`.

- Claim: `VTask.Semiconj f ga gb` and `VTask.Semiconj f ga' gb'` imply `VTask.Semiconj f (ga ∘ ga') (gb ∘ gb')` — semiconjugacy is preserved under composition of the self-maps on each side.

## 5. Boundaries

- When `α` is empty, the predicate holds vacuously for any three functions, since there are no points `x : α` to check.
- When `f` is a bijection and `VTask.Semiconj f ga gb`, the relation becomes a genuine conjugacy: `gb` is conjugate to `ga` via `f`, and one can recover `ga = f⁻¹ ∘ gb ∘ f`.
- The predicate is **not** symmetric in `ga` and `gb` in general: `VTask.Semiconj f ga gb` does not imply `VTask.Semiconj f gb ga`; injectivity of `f` is needed to reverse the direction.
- When `f = id`, the predicate reduces to `ga = gb` (pointwise), i.e., the two self-maps are identical.

## 6. Not to be confused with

- **`Commute f g`** (or `VTask.Semiconj f g g`): semiconjugacy of `f` to itself via `g` means `f` and `g` commute; commutation is the special case where both self-maps are the same.
- **Conjugacy** (`gb = f ∘ ga ∘ f⁻¹`): full conjugacy is the two-sided version requiring `f` to be invertible; semiconjugacy is the one-sided (and potentially non-invertible) generalization.
- **`SemiconjBy a b c`** in a monoid: the algebraic notion that `a * b = c * a`; this is the pointwise multiplication analogue, not a function-theoretic intertwining.