## Object

`VTask.ringEquivCongr h` is the canonical ring isomorphism `ZMod m ≃+* ZMod n` that witnesses the equality of the two residue-ring types when the moduli `m` and `n` are provably equal natural numbers. Because `ZMod` is defined by cases (it is `ℤ` when the modulus is `0`, and `Fin k` when the modulus is a positive `k`), an equality proof `h : m = n` is not enough on its own to produce a *ring* isomorphism — this construction packages the underlying type equivalence together with the verification that it respects addition and multiplication, yielding a fully bundled `RingEquiv`.

When `h` is `rfl`, the isomorphism is the identity on every element.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ringEquivCongr : {m n : ℕ} -> (h : m = n) -> ZMod m ≃+* ZMod n
<!-- PINNED-SIGNATURE:END -->


`VTask.ringEquivCongr : {m n : ℕ} -> (h : m = n) -> ZMod m ≃+* ZMod n`

The implicit arguments `m` and `n` are the two natural-number moduli; they are inferred from the explicit equality proof. The explicit argument `h` is a proof that `m` equals `n`; it is the sole piece of data driving the construction.

## Conventions

When applied at `h = rfl`, the resulting isomorphism acts as the identity: every element of `ZMod m` is sent to itself. No junk values are introduced because the function is total on all natural numbers including `0`.

## Worked examples

- Claim: Applying `VTask.ringEquivCongr rfl` to any element `x : ZMod 5` returns `x` unchanged.

- Claim: The `ZMod.val` of the image of any element under `VTask.ringEquivCongr h` equals the `ZMod.val` of the original element; concretely, if `h : 4 = 4` and `x : ZMod 4`, then `ZMod.val (VTask.ringEquivCongr rfl x) = ZMod.val x`.

- Claim: For `h : 3 = 3`, the isomorphism `VTask.ringEquivCongr h` composed with its own inverse `(VTask.ringEquivCongr h).symm` equals `VTask.ringEquivCongr h.symm` (symmetry law).

- Claim: For `hab : 6 = 6` and `hbc : 6 = 6`, the composite `(VTask.ringEquivCongr hab).trans (VTask.ringEquivCongr hbc)` equals `VTask.ringEquivCongr (hab.trans hbc)` (transitivity law).

- Claim: For any integer `z : ℤ` and proof `h : m = n`, the image of the integer cast `(z : ZMod m)` under `VTask.ringEquivCongr h` equals the integer cast `(z : ZMod n)`.

## Boundaries

- **Both moduli zero (`m = 0`, `n = 0`):** `ZMod 0` is definitionally `ℤ`, and the isomorphism reduces to the identity ring automorphism of `ℤ`.
- **`h = rfl`:** The isomorphism is literally the identity map; `VTask.ringEquivCongr rfl x = x` for every element.
- **Positive equal moduli (`m = n = k > 0`):** `ZMod k` is `Fin k`, and the isomorphism is the `Fin`-level equivalence induced by the equality, augmented with ring-operation compatibility.
- **Impossible cases (`m = 0, n ≠ 0` or vice versa):** These are excluded by the type system — no proof `h : m = n` can exist when `m` and `n` are concretely different natural numbers, so the impossible branches are never reached.

## Not to be confused with

- `ZMod.chineseRemainder`: a ring isomorphism `ZMod (m * n) ≃+* ZMod m × ZMod n` for coprime moduli — a substantive structural decomposition, not a mere renaming.
- `Equiv.cast` / `Eq.mpr`-style coercions: these reindex the underlying *type* along an equality but do not carry the ring-isomorphism structure that `VTask.ringEquivCongr` provides.
- `RingEquiv.refl`: the identity automorphism of a single ring `R ≃+* R`; `VTask.ringEquivCongr` generalises this to two *a priori* distinct (but provably equal) types.