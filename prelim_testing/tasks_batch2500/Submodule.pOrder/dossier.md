## Object

`VTask.pOrder` is the **p-order** of an element in a `p^∞`-torsion module: given a module `M` all of whose elements are annihilated by some power of a fixed scalar `p`, and given an element `x ∈ M`, it returns the smallest natural number `n` such that `p^n • x = 0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pOrder : {R : Type u_1} -> {M : Type u_2} -> [Monoid R] -> [AddCommMonoid M] -> [DistribMulAction R M] -> {p : R} -> (hM : Module.IsTorsion' M ↥(Submonoid.powers p)) -> (x : M) -> [(n : ℕ) → Decidable (p ^ n • x = 0)] -> ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.pOrder : {R : Type u_1} -> {M : Type u_2} -> [Monoid R] -> [AddCommMonoid M] -> [DistribMulAction R M] -> {p : R} -> (hM : Module.IsTorsion' M ↥(Submonoid.powers p)) -> (x : M) -> [(n : ℕ) → Decidable (p ^ n • x = 0)] -> ℕ`

- `R` is the ring (or monoid) of scalars; it carries a `Monoid` instance.
- `M` is the module (abelian group under addition); it carries an `AddCommMonoid` and a `DistribMulAction R M` instance.
- `p` is the distinguished scalar element of `R` whose powers are the potential annihilators.
- `hM` is the proof that `M` is a `p^∞`-torsion module, i.e., every element of `M` is annihilated by some power of `p`.
- `x` is the particular element of `M` whose p-order is being computed.
- The final instance argument supplies a decision procedure for each `n : ℕ`, determining whether `p^n • x = 0`; this is needed to run the minimization.

## Conventions

When `x = 0`, then `p^0 • 0 = 0` holds trivially, so `VTask.pOrder hM 0 = 0`. More generally, if `p^0 • x = x = 0` then the p-order is `0`.

## Worked examples

- Claim: For the zero element `x = 0` in any `p^∞`-torsion module, `VTask.pOrder hM 0 = 0`, since `p^0 • 0 = 1 • 0 = 0`.

- Claim: If `p • x ≠ 0` but `p^2 • x = 0`, then `VTask.pOrder hM x = 2`, since `n = 2` is the smallest natural number annihilating `x` by powers of `p`.

- Claim: The result always satisfies `p ^ (VTask.pOrder hM x) • x = 0` (this is the content of `pow_pOrder_smul`).

- Claim: For any `n < VTask.pOrder hM x`, we have `p^n • x ≠ 0`, by minimality of the p-order.

## Boundaries

- **Zero element**: The p-order of `0` is `0` because `p^0 • 0 = 0` holds immediately (no power of `p` is needed beyond the zeroth).
- **Minimality**: The value is precisely the *smallest* such `n`; no smaller natural number witnesses annihilation.
- **Decidability requirement**: The function requires a `Decidable` instance for `p^n • x = 0` for each `n`; without it, the computation cannot proceed. This is a typeclass argument, not a mathematical restriction.
- **Torsion hypothesis**: The torsion hypothesis `hM` guarantees existence of *some* `n` with `p^n • x = 0`, so `Nat.find` is well-defined and the function is total under that hypothesis.

## Not to be confused with

- **`multiplicity p n` (or `p`-adic valuation)**: That counts the exact power of `p` dividing an integer `n`; `VTask.pOrder` instead measures the smallest power of a scalar annihilating a module element.
- **`orderOf x` (order of an element in a group)**: That is the smallest positive `n` with `x^n = 1` (multiplicative), whereas `VTask.pOrder` is additive (scalar multiplication) and works in a module, not a group.
- **`Module.IsTorsionBy R M a` (torsion by a fixed element)**: That asserts every element is annihilated by a *single fixed* scalar `a`; `VTask.pOrder` records the minimal power of `p` needed for a *specific* element.