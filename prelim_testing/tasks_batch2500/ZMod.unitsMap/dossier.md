## VTask.unitsMap

### Object

Given natural numbers `n` and `m` with `n` dividing `m`, `VTask.unitsMap` is the canonical group homomorphism from the group of units of `ZMod m` to the group of units of `ZMod n`. Concretely, it sends an invertible residue class modulo `m` to its reduction modulo `n`, which is guaranteed to remain invertible because `n ∣ m`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.unitsMap : {n m : ℕ} -> (hm : n ∣ m) -> (ZMod m)ˣ →* (ZMod n)ˣ
<!-- PINNED-SIGNATURE:END -->


```
VTask.unitsMap : {n m : ℕ} -> (hm : n ∣ m) -> (ZMod m)ˣ →* (ZMod n)ˣ
```

The implicit argument `n` is the smaller modulus (the target of the reduction). The implicit argument `m` is the larger modulus (the source of the units group). The explicit argument `hm` is the proof that `n` divides `m`, which is required for the reduction to preserve invertibility. The return type is a monoid homomorphism (in fact a group homomorphism) from the units of `ZMod m` to the units of `ZMod n`.

### Conventions

The divisibility condition `n ∣ m` is required as an explicit proof argument; there is no junk value defined for the case when `n` does not divide `m` — the function is simply not applicable in that regime. When `m = 0` and `n = 0`, the single divisibility instance `0 ∣ 0` is valid and the map acts on the units of `ZMod 0`, which are the units of `ℤ`. When `n = 1`, every element of `ZMod 1` is the unique unit, so the homomorphism is the trivial map to the trivial group.

### Worked examples

- Claim: For `n = 2`, `m = 6`, and the divisibility `2 ∣ 6`, the image of any unit of `ZMod 6` under `VTask.unitsMap` lies in `(ZMod 2)ˣ`, which has exactly one element.

- Claim: The map `VTask.unitsMap (show 1 ∣ m from one_dvd m)` is the unique homomorphism from `(ZMod m)ˣ` to the trivial group `(ZMod 1)ˣ`.

- Claim: For `n = m`, the divisibility `n ∣ n` (i.e., `dvd_refl n`) yields a homomorphism `VTask.unitsMap (dvd_refl n) : (ZMod n)ˣ →* (ZMod n)ˣ` which is the identity homomorphism.

- Claim: `VTask.unitsMap` is compatible with transitivity of divisibility: if `a ∣ b` and `b ∣ c`, then composing `VTask.unitsMap (a ∣ b)` after `VTask.unitsMap (b ∣ c)` equals `VTask.unitsMap (a ∣ c)` (as monoid homomorphisms).

### Boundaries

- **`n = 1`**: The target group `(ZMod 1)ˣ` is the trivial group, so `VTask.unitsMap` sends every unit to the unique element regardless of `m`.
- **`n = m`**: The divisibility is `dvd_refl n`, and `VTask.unitsMap` reduces to the identity map on `(ZMod n)ˣ`.
- **`m = 0`**: `ZMod 0` is `ℤ`, and the units are `{1, -1}`. For any `n ∣ 0` (all `n` divide 0), the map sends units of `ℤ` to units of `ZMod n` by reduction.
- **`n = 0`, `m = 0`**: Both rings coincide with `ℤ`; the map is the identity on `ℤˣ`.
- The map is surjective in general for the cases arising from `n ∣ m` when `n` and `m` are coprime components allow it, but surjectivity is not guaranteed for all divisibility pairs.

### Not to be confused with

- `ZMod.castHom`: The underlying ring homomorphism `ZMod m →+* ZMod n` (not restricted to units; `VTask.unitsMap` is its units-level counterpart).
- `Units.map`: The general functor taking any monoid homomorphism to a group homomorphism on units; `VTask.unitsMap` is specifically `Units.map` applied to `castHom`.
- The inclusion `(ZMod n)ˣ →* (ZMod m)ˣ` (going in the opposite direction, lifting units from the smaller to the larger modulus), which does not exist canonically and should not be confused with this reduction map.
