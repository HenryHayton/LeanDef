## Object

Given a quotient type `Quotient s₁` (the quotient of a type `α` by a setoid `s₁`), `VTask.hrecOn'` is a *heterogeneous* (dependent) recursion principle. It produces a value of type `φ qa` — where the return sort `φ` may itself depend on the quotient element `qa` — by specifying what value to return on each representative `a : α`, provided that the chosen values are *heterogeneously equal* whenever the representatives are related by the setoid. In short, it eliminates a single quotient element into a dependent sort, checking that the choice of representative does not matter up to heterogeneous equality.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.hrecOn' : {α : Sort u_1} -> {s₁ : Setoid α} -> {φ : Quotient s₁ → Sort u_5} -> (qa : Quotient s₁) -> (f : (a : α) → φ (Quotient.mk'' a)) -> (c : ∀ (a₁ a₂ : α), a₁ ≈ a₂ → f a₁ ≍ f a₂) -> φ qa
<!-- PINNED-SIGNATURE:END -->


`{α : Sort u_1} -> {s₁ : Setoid α} -> {φ : Quotient s₁ → Sort u_5} -> (qa : Quotient s₁) -> (f : (a : α) → φ (Quotient.mk'' a)) -> (c : ∀ (a₁ a₂ : α), a₁ ≈ a₂ → f a₁ ≍ f a₂) -> φ qa`

- `α` is the underlying type being quotiented.
- `s₁` is the setoid on `α` defining the equivalence relation.
- `φ` is the motive — a sort-valued function on the quotient — making this a *dependent* recursion.
- `qa` is the quotient element being eliminated (the "input" being recursed on).
- `f` is the function that assigns a value of type `φ (Quotient.mk'' a)` to each representative `a : α`; this is the "definition by cases on representatives."
- `c` is the coherence condition: for any two equivalent representatives `a₁ ≈ a₂`, the values `f a₁` and `f a₂` must be *heterogeneously equal* (written `≍`, i.e., `HEq`). This ensures the result is well-defined on the quotient.

## Conventions

When `qa` is of the form `Quotient.mk'' x` (i.e., the class of a concrete representative `x`), the result computes to `f x` definitionally. No junk values are declared; the function is total over all quotient elements.

## Worked examples

- Claim: For the trivial setoid on `ℕ` (where nothing is identified), `VTask.hrecOn' (Quotient.mk'' 3) (fun n => n) (fun a₁ a₂ h => by cases h; rfl)` equals `3`.

- Claim: If `φ : Quotient s₁ → Type*` is constant (i.e., `φ _ = T`), then `VTask.hrecOn'` reduces to the ordinary quotient recursor: applying it to `Quotient.mk'' a` with function `f` and coherence `c` gives `f a`.

- Claim: The computation rule `hrecOn'_mk''` states that `(Quotient.mk'' x).hrecOn' f c = f x` for any representative `x`.

## Boundaries

- The coherence condition `c` requires *heterogeneous* equality (`HEq`) of the values `f a₁` and `f a₂` whenever `a₁ ≈ a₂`. This is strictly weaker than definitional equality but stronger than existence of a cast; it is the appropriate notion when the return types `φ (Quotient.mk'' a₁)` and `φ (Quotient.mk'' a₂)` are propositionally but not necessarily definitionally equal.
- The recursion is into `Sort*`, so it can produce values in `Prop`, `Type`, or any universe — making it suitable both for proof-relevant elimination and for data.
- If `φ` does not depend on the quotient element (constant motive), the coherence condition reduces to ordinary equality, and this specialises to the non-dependent `Quotient.liftOn'`.
- The function is total: every `qa : Quotient s₁` is in the domain, since every quotient element has at least one representative.

## Not to be confused with

- `Quotient.liftOn'`: the non-dependent version, where the motive `φ` is constant (return type does not depend on `qa`); no heterogeneous equality is needed there.
- `Quotient.hrecOn₂'`: the two-argument variant, which eliminates over a pair of quotient elements simultaneously with a coherence condition involving both equivalences.
- `Quotient.recOn'` / `Quotient.inductionOn'`: the induction principles into `Prop`, which do not need a coherence condition because proof irrelevance makes it automatic.