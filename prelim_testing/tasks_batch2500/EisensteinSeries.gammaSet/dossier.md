## Object

`VTask.gammaSet N r a` is the set of all pairs of integers `v = (v₀, v₁)` satisfying two simultaneous conditions:
1. **Congruence condition**: each entry `vᵢ` is congruent to `aᵢ` modulo `N` (i.e., the pair reduces to `a` when viewed mod `N`).
2. **GCD condition**: the greatest common divisor of `v₀` and `v₁` equals `r`.

It arises naturally in the theory of Eisenstein series as the index set over which the classical Eisenstein summands are summed, parametrised by a level `N`, a GCD value `r`, and a residue class `a` mod `N`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.gammaSet : (N r : ℕ) -> (a : Fin 2 → ZMod N) -> Set (Fin 2 → ℤ)
<!-- PINNED-SIGNATURE:END -->


`VTask.gammaSet : (N r : ℕ) -> (a : Fin 2 → ZMod N) -> Set (Fin 2 → ℤ)`

The first argument `N` is the modulus; it determines the ring `ZMod N` in which congruences are checked. The second argument `r` is the required value of the GCD of the two integer entries. The third argument `a` is a pair of residues in `ZMod N`, specifying the congruence class that every member of the set must reduce to mod `N`.

## Conventions

When `N = 1` the congruence condition is vacuous (every integer is congruent to `0` mod `1` and there is only one element of `ZMod 1`), so `VTask.gammaSet 1 r a` depends only on `r` and equals the set of integer pairs whose GCD is exactly `r`, regardless of the choice of `a`. When `r = 0` the GCD condition forces both entries to be zero (since `gcd 0 0 = 0`), so the set is either `{(0, 0)}` (if `a` is the zero residue class) or empty. There is no junk-value convention for out-of-range inputs because all natural number inputs are valid.

## Worked examples

- Claim: The pair `(2, 4)` belongs to `VTask.gammaSet 1 2 0` because both entries are integers with `gcd(2, 4) = 2` and `N = 1` makes the congruence condition automatic.

- Claim: The pair `(3, 5)` belongs to `VTask.gammaSet 1 1 0` because `gcd(3, 5) = 1`, and for `N = 1` the congruence condition is vacuous; in particular, membership is equivalent to `IsCoprime (v 0) (v 1)` in this case.

- Claim: The pair `(2, 3)` does **not** belong to `VTask.gammaSet 5 1 0` because, even though `gcd(2, 3) = 1`, the first entry `2` is not congruent to `0` mod `5`.

- Claim: The pair `(5, 10)` belongs to `VTask.gammaSet 5 5 0` because `5 ≡ 0 (mod 5)`, `10 ≡ 0 (mod 5)`, and `gcd(5, 10) = 5`.

- Claim: For any two choices `a a' : Fin 2 → ZMod 1`, `VTask.gammaSet 1 r a = VTask.gammaSet 1 r a'` (the set is independent of the residue class when `N = 1`).

## Boundaries

- **`r = 0`**: The GCD of two integers is `0` if and only if both integers are `0`. Thus `VTask.gammaSet N 0 a` is `{(0, 0)}` when `a` is the zero class mod `N`, and empty otherwise.
- **`N = 0`**: `ZMod 0 = ℤ`, so the congruence condition reads that the integer pair cast into `ℤ` equals `a` exactly. Combined with the GCD condition, this is a very restrictive (possibly empty or singleton) set.
- **`N = 1`**: The congruence condition is trivially satisfied, leaving only the GCD constraint. All choices of `a : Fin 2 → ZMod 1` give the same set.
- **Disjointness**: For fixed `N` and `a`, the sets `VTask.gammaSet N r a` for different values of `r` are pairwise disjoint, since the GCD of a pair is unique.
- **`SL(2, ℤ)` equivariance**: Right-multiplying a member `v` of `VTask.gammaSet N r a` by a matrix `γ ∈ SL(2, ℤ)` (as a row-vector action) yields a member of `VTask.gammaSet N r (a ᵥ* γ)`. The GCD is preserved because `γ` has determinant `±1`.

## Not to be confused with

- **`gammaSet N 1 0`** (the special case `r = 1`, `a = 0`): this is the set of coprime integer pairs congruent to `(0, 0)` mod `N`, which serves as the standard index set for level-`N` Eisenstein series; it is a special case, not the general definition.
- **The congruence subgroup `Γ(N) ⊆ SL(2, ℤ)`**: also called a "gamma set" informally, but it is a group of matrices, not a set of integer pairs.
- **`Finset (gammaSet N 1 a)`**: finite subsets of the gamma set used as partial sums in the Eisenstein series; these are `Finset`s (finite collections), not the underlying `Set`.
