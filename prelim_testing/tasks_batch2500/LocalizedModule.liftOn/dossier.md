## Object

`VTask.liftOn` takes a well-defined function on pairs `(module element, submonoid element)` and descends it to the localized module, which is a quotient of the set of such pairs by an equivalence relation capturing the notion that two fractions `m/s` and `m'/s'` represent the same element. The result is a value of any target type `α`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.liftOn : {R : Type u} -> [CommSemiring R] -> {S : Submonoid R} -> {M : Type v} -> [AddCommMonoid M] -> [Module R M] -> {α : Type u_3} -> (x : LocalizedModule S M) -> (f : M × ↥S → α) -> (wd : ∀ (p p' : M × ↥S), p ≈ p' → f p = f p') -> α
<!-- PINNED-SIGNATURE:END -->


`VTask.liftOn : {R : Type u} -> [CommSemiring R] -> {S : Submonoid R} -> {M : Type v} -> [AddCommMonoid M] -> [Module R M] -> {α : Type u_3} -> (x : LocalizedModule S M) -> (f : M × ↥S → α) -> (wd : ∀ (p p' : M × ↥S), p ≈ p' → f p = f p') -> α`

- `R` is the base commutative semiring.
- `S` is a submonoid of `R`, used as the set of denominators in the localization.
- `M` is the `R`-module being localized.
- `α` is the target type of the function being descended.
- `x` is the element of the localized module at which the descended function is evaluated.
- `f` is a function on pairs `(m, s)` with `m : M` and `s : S` that one wishes to push down to the quotient.
- `wd` is the well-definedness proof: `f` must send equivalent pairs to equal values, where equivalence is the relation `≈` on `M × S` defining the localized module.

## Conventions

The defining computational rule is that when `x` is the equivalence class `mk m s` of a pair `(m, s)`, the result of `VTask.liftOn x f wd` equals `f ⟨m, s⟩`.

## Worked examples

- Claim: For any `m : M` and `s : S`, evaluating `VTask.liftOn (mk m s) f wd` on the canonical representative returns `f ⟨m, s⟩` (i.e., `liftOn_mk` holds).

- Claim: If `f : M × S → ℕ` is the constant function `fun _ => 42` (which is trivially well-defined), then `VTask.liftOn x f wd = 42` for every `x` in the localized module.

- Claim: The function sending `mk m s` to the first component `m` can be descended if the chosen representative is made canonical; the `wd` hypothesis is the price ensuring consistency across all representatives of the same element.

## Boundaries

- The only requirement is that `f` is well-defined with respect to the equivalence relation on `M × S`; there is no algebraic compatibility (like linearity) required of `f` itself for `VTask.liftOn` to make sense.
- The target type `α` is completely arbitrary; it need not carry any algebraic structure.
- If two pairs `(m, s)` and `(m', s')` are equivalent (i.e., there exists a `u : S` with `u • s' • m = u • s • m'`), then `f ⟨m, s⟩ = f ⟨m', s'⟩` must hold; this is precisely what `wd` asserts.
- The function is total: every element of the localized module has a well-defined image.

## Not to be confused with

- `VTask.liftOn₂`: the two-argument variant, which lifts a function of two localized module elements simultaneously.
- The localized module's `mk` constructor: `mk m s` builds an element of the localized module, whereas `VTask.liftOn` consumes one.
- Quotient.lift (the general Lean quotient lift): `VTask.liftOn` is a specialization of this to the particular equivalence relation defining the localized module.