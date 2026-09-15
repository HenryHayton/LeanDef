## Object

`VTask.cast` is the canonical "forgetful" map that sends an element of the integers modulo `n` to a corresponding element of any additive group with a unit (i.e., any `AddGroupWithOne`). Concretely, it interprets the residue class as an element of `R` by repeatedly adding the multiplicative identity. When `n = 0`, the ring `ZMod 0` is identified with the integers, and the cast is just the ordinary integer-to-`R` coercion. When `n ≥ 1`, the cast sends a residue class — represented internally by its canonical representative in `{0, 1, …, n−1}` — to the corresponding natural-number multiple of `1` in `R`. The map is a ring homomorphism precisely when the characteristic of `R` divides `n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cast : {R : Type u_1} -> [AddGroupWithOne R] -> {n : ℕ} -> ZMod n → R
<!-- PINNED-SIGNATURE:END -->


`VTask.cast : {R : Type u_1} -> [AddGroupWithOne R] -> {n : ℕ} -> ZMod n → R`

The implicit type argument `R` is the target additive group with one into which we are casting. The instance argument `[AddGroupWithOne R]` supplies the algebraic structure of `R` that makes the cast meaningful (the ability to add and to form integer multiples of `1`). The implicit natural number `n` is the modulus, i.e., we are casting elements of `ZMod n`. The explicit argument is the element of `ZMod n` being cast.

## Conventions

When `n = 0`, the type `ZMod 0` is definitionally equal to `ℤ`, and `VTask.cast` reduces to the ordinary `Int.cast` coercion; in particular no modular reduction occurs. When `n ≥ 1`, every element of `ZMod n` carries an underlying natural-number representative in `{0, 1, …, n−1}`, and `VTask.cast` maps the element to the corresponding natural-number cast into `R` (i.e., the sum of that many copies of `1 : R`).

## Worked examples

- Claim: In `ZMod 0 ≅ ℤ`, casting the integer `5` to `ℤ` gives `5`.

- Claim: In `ZMod 7`, the element `3 : ZMod 7` casts to `3 : ZMod 7` (the identity cast).
  ```lean
  example : (VTask.cast (3 : ZMod 7) : ZMod 7) = 3 := by decide
  ```

- Claim: In `ZMod 5`, the element `0 : ZMod 5` casts to `0` in any `AddGroupWithOne`.
  ```lean
  example : (VTask.cast (0 : ZMod 5) : ZMod 5) = 0 := by decide
  ```

- Claim: Casting the class of `n` (which equals `0`) in `ZMod n` for `n ≥ 1` gives `0` in `ZMod n`.
  ```lean
  example : (VTask.cast (0 : ZMod 6) : ZMod 6) = 0 := by decide
  ```

- Claim: `VTask.cast` is the identity function when `R = ZMod n` (for any `n`).

## Boundaries

- At `n = 0`, the domain is `ZMod 0 ≅ ℤ` and the cast is simply `Int.cast`; no modular arithmetic is involved.
- At `n = 1`, the only element of `ZMod 1` is `0`, and the cast always returns `0 : R` (the unique value a natural-number cast of `0` can take).
- The cast is NOT guaranteed to be a ring homomorphism in general; it is a morphism of additive groups with one only when the characteristic of `R` divides `n`. Callers needing a bundled ring homomorphism should use `ZMod.castHom`.
- The cast maps each residue class to the natural-number multiple of `1` matching its canonical representative; it does not choose a "least absolute value" representative (for that, see `ZMod.valMinAbs`).

## Not to be confused with

- `ZMod.castHom`: the bundled ring homomorphism version, which requires a proof that the characteristic of `R` divides `n` and packages `VTask.cast` as a `RingHom`.
- `Int.cast`: the coercion from `ℤ` to `R`, which coincides with `VTask.cast` only in the `n = 0` case.
- `ZMod.val`: the function extracting the underlying `ℕ` representative of an element of `ZMod n` (for `n ≥ 1`); `VTask.cast` then applies `Nat.cast` to this value, so the two are related but not the same.
