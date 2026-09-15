## Object

`VTask.translate` is the monoid homomorphism that turns a real number, presented as an element of the multiplicative reals, into the rigid translation of the real line by that number, viewed as an invertible degree-1 circle lift. Concretely, to the element corresponding to a real number `x` it associates the map `y ↦ x + y`, packaged as a unit (invertible element) in the monoid of degree-1 circle lifts. Because it is a monoid homomorphism, it converts the multiplicative group structure on `Multiplicative ℝ` (which mirrors addition of reals) into composition of translations.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.translate : Multiplicative ℝ →* CircleDeg1Liftˣ
<!-- PINNED-SIGNATURE:END -->


`VTask.translate : Multiplicative ℝ →* CircleDeg1Liftˣ`

This homomorphism takes no explicit arguments beyond its source-element when applied: the domain is `Multiplicative ℝ`, whose elements are real numbers equipped with a multiplicative notation so that the group operation corresponds to real-number addition. The codomain is `CircleDeg1Liftˣ`, the group of invertible elements of the monoid of degree-1 lifts of circle maps. An element `Multiplicative.ofAdd x` in the domain represents the translation amount `x ∈ ℝ`, and `VTask.translate` sends it to the unit whose underlying function is `y ↦ x + y`.

## Conventions

To access the translation by a concrete real number `x`, one writes `VTask.translate (Multiplicative.ofAdd x)`; the `Multiplicative.ofAdd` coercion is the standard bridge between additive and multiplicative notation for ℝ. The inverse of the translation by `x` is the translation by `−x`, reflecting the group-inverse in `CircleDeg1Liftˣ`. The identity element of `Multiplicative ℝ` (corresponding to `0 : ℝ` under `ofAdd`) maps to the identity unit, i.e., the identity function on ℝ.

## Worked examples

- Claim: Applying `VTask.translate (Multiplicative.ofAdd x)` to a real number `y` yields `x + y`.
  (Formally: `VTask.translate (Multiplicative.ofAdd x) y = x + y` for all `x y : ℝ`.)

- Claim: The translation number of `VTask.translate (Multiplicative.ofAdd x)` equals `x`; that is, the asymptotic average displacement of the translation-by-`x` map is exactly `x`.

- Claim: Iterating `VTask.translate (Multiplicative.ofAdd x)` exactly `n : ℕ` times yields `VTask.translate (Multiplicative.ofAdd (↑n * x))`; translation by `x`, iterated `n` times, is the same as a single translation by `n * x`.

- Claim: The inverse `(VTask.translate (Multiplicative.ofAdd x))⁻¹` applied to `y` gives `−x + y`.

## Boundaries

- The map is defined for every element of `Multiplicative ℝ`, i.e., every real number; there are no domain restrictions.
- At `x = 0` (the multiplicative identity, `Multiplicative.ofAdd 0`), the result is the identity unit of `CircleDeg1Liftˣ`, whose underlying function is `y ↦ y`.
- Negative translations are fully supported; `VTask.translate (Multiplicative.ofAdd (-x))` is the compositional inverse of `VTask.translate (Multiplicative.ofAdd x)` in `CircleDeg1Liftˣ`.
- Because `CircleDeg1Liftˣ` packages both the map and its inverse as part of the unit structure, the invertibility of every translation is automatic.

## Not to be confused with

- `CircleDeg1Lift` (without the `ˣ` superscript): the monoid of all degree-1 circle lifts, which need not be invertible; `VTask.translate` lands in the strictly smaller group of *units*.
- The rotation-number function `τ`: that is a map *from* `CircleDeg1Lift` to `ℝ` measuring asymptotic displacement, not a constructor of translations.
- `Multiplicative.ofAdd` by itself: that is only the type-coercion wrapper converting an additive real into a multiplicative one, with no geometric content; `VTask.translate` is the geometrically meaningful homomorphism built on top of it.