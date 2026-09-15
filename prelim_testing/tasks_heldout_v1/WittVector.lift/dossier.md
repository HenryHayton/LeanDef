## Object

`VTask.lift` constructs the unique ring homomorphism from a semiring `S` into the *p*-typical Witt vectors `𝕎 R` that is compatible with a given compatible system of ring homomorphisms from `S` into the truncated Witt vectors of all lengths. It realises `𝕎 R` as the inverse limit of the truncated Witt vectors `TruncatedWittVector p k R` in the category of rings: any cone over that inverse system with apex `S` factors uniquely through `𝕎 R` via this homomorphism.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {p : ℕ} -> {R : Type u_1} -> [CommRing R] -> [Fact (Nat.Prime p)] -> {S : Type u_2} -> [Semiring S] -> (f : (k : ℕ) → S →+* TruncatedWittVector p k R) -> (f_compat : ∀ (k₁ k₂ : ℕ) (hk : k₁ ≤ k₂), (TruncatedWittVector.truncate hk).comp (f k₂) = f k₁) -> S →+* WittVector p R
<!-- PINNED-SIGNATURE:END -->


`{p : ℕ}` is the prime characteristic governing the Witt vector construction. `{R : Type u_1}` with `[CommRing R]` is the coefficient ring. `[Fact (Nat.Prime p)]` asserts that `p` is indeed prime. `{S : Type u_2}` with `[Semiring S]` is the source ring whose homomorphisms into the truncated Witt vectors are being lifted. The explicit argument `f` is the family of ring homomorphisms: for each natural number `k`, `f k : S →+* TruncatedWittVector p k R` is the component map at truncation level `k`. The argument `f_compat` is the coherence condition on this family: for any `k₁ ≤ k₂`, the truncation map from level `k₂` down to level `k₁` composed with `f k₂` equals `f k₁`, i.e., the cone condition holds.

## Conventions

The implicit argument `_` standing for `f_compat` is threaded into `lift` so callers need only supply the family `f` explicitly and let Lean elaborate the compatibility proof; in practice the notation `lift _ f_compat` is used in the library.

## Worked examples

- Claim: For any compatible family `f` and any `s : S`, applying the truncation map at level `n` to `VTask.lift f f_compat s` recovers `f n s`.

- Claim: The composite ring hom `(WittVector.truncate n).comp (VTask.lift _ f_compat)` equals `f n` as ring homs `S →+* TruncatedWittVector p n R`.

- Claim: If `g : S →+* 𝕎 R` is any ring hom satisfying `(WittVector.truncate k).comp g = f k` for all `k`, then `g = VTask.lift _ f_compat` (uniqueness of the lift).

## Boundaries

- When `S` is the zero ring, the lift exists trivially and sends everything to zero.
- The construction requires `f_compat` to hold for *all* pairs `k₁ ≤ k₂`; if the compatibility condition fails at even one level, the resulting function would not be a well-defined map into `𝕎 R` (the intersection of kernels would not yield a single consistent element).
- The result is a ring homomorphism (preserving addition, multiplication, 0, and 1), not merely a set map; all ring-homomorphism axioms are guaranteed by the construction.
- The lift is unique among ring homomorphisms compatible with all truncations, as stated by the universal property.

## Not to be confused with

- `WittVector.truncate`: the *projection* ring hom going the other direction, from `𝕎 R` down to `TruncatedWittVector p k R`; `VTask.lift` is its universal section from a cone.
- `TruncatedWittVector.lift` (if it existed): one might confuse this with a lift defined only at a fixed truncation level rather than the full inverse-limit universal property.
- `RingHom.lift` or localization/quotient universal properties: those lift along surjections or inverting elements, whereas `VTask.lift` lifts into an inverse limit along a compatible family of projections.