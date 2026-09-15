## VTask.HasMap

### Object

Let `P` be a standard étale pair over a commutative ring `R`, consisting of two polynomials `P.f` and `P.g` in `R[X]`. Given an `R`-algebra `S` and an element `x : S`, `VTask.HasMap P x` is the proposition asserting that there exists a well-defined `R`-algebra homomorphism from the standard étale `R`-algebra `R[X][Y]/⟨P.f, Y·P.g − 1⟩` to `S` sending the image of `X` to `x`. Concretely, this happens exactly when `x` is a root of `P.f` (evaluated in `S`) and the value `P.g(x)` is a unit in `S`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.HasMap : {R : Type u_1} -> {S : Type u_2} -> [CommRing R] -> [CommRing S] -> [Algebra R S] -> (P : StandardEtalePair R) -> (x : S) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{R : Type u_1} -> {S : Type u_2} -> [CommRing R] -> [CommRing S] -> [Algebra R S] -> (P : StandardEtalePair R) -> (x : S) -> Prop`

The implicit type argument `R` is the base commutative ring. The implicit type argument `S` is the target commutative ring. The instance arguments equip both `R` and `S` with commutative ring structures and `S` with an `R`-algebra structure. The explicit argument `P` is the standard étale pair, which packages two polynomials `P.f` and `P.g` over `R`. The explicit argument `x` is the element of `S` that is the proposed image of the generator `X`.

### Conventions

No special junk-value or boundary conventions are declared for this definition: it is a straightforward conjunction of two conditions (`aeval x P.f = 0` and `IsUnit (aeval x P.g)`) with no degenerate inputs requiring special treatment.

### Worked examples

- Claim: For the standard étale pair over `ℤ` given by `P.f = X - 1` and `P.g = 1`, the element `1 : ℤ` satisfies `VTask.HasMap P 1`, since `1 - 1 = 0` and `1(1) = 1` is a unit.

- Claim: For a standard étale pair over `ℤ` with `P.f = X^2 + 1` and `P.g = 1`, the element `2 : ℤ` does NOT satisfy `VTask.HasMap P 2`, because `2^2 + 1 = 5 ≠ 0` in `ℤ`.

- Claim: For a standard étale pair over `ℤ` with `P.f = X` and `P.g = X - 2`, the element `2 : ℚ` does NOT satisfy `VTask.HasMap P 2`, because although `P.f(2) = 2 ≠ 0`, and even if `P.f(0) = 0`, we need `P.g(0) = 0 - 2 = -2` which is a unit in `ℚ`, illustrating how the two conditions interact.

- Claim: If `VTask.HasMap P x` holds for `x : S`, then `aeval x P.f = 0` and `IsUnit (aeval x P.g)` both hold simultaneously.

### Boundaries

- When `P.g` is a nonzero constant polynomial, `aeval x P.g` is that same constant in `S`, so `IsUnit (aeval x P.g)` depends entirely on whether that constant is a unit in `S`, independently of `x`.
- When `P.f` is the zero polynomial, `aeval x P.f = 0` holds for every `x`, so `VTask.HasMap P x` reduces to `IsUnit (aeval x P.g)` alone.
- When `S = R` (i.e., the algebra is the identity), `VTask.HasMap P x` asks whether `x` is a root of `P.f` in `R` and whether `P.g(x)` is invertible in `R`.
- If `P.g` is the zero polynomial, then `aeval x P.g = 0` for all `x`, and `IsUnit 0` is false (in a nontrivial ring), so `VTask.HasMap P x` is vacuously false for all `x` in any nontrivial `S`.

### Not to be confused with

- `StandardEtalePair.homEquiv`: this is the equivalence that makes precise the bijection between elements satisfying `VTask.HasMap P x` and actual `R`-algebra homomorphisms from the standard étale algebra to `S`; `VTask.HasMap` is just the membership predicate on the underlying element `x`.
- Étaleness of a ring map or formally étale morphisms in general: `VTask.HasMap P x` is a purely algebraic condition on a specific element `x`, not a property of a ring homomorphism or a module-theoretic lifting condition.
- `aeval x P.f = 0` alone (the condition of being a root of `P.f`): `VTask.HasMap` additionally requires invertibility of `P.g(x)`, which is the condition ensuring the localization-type component of the standard étale algebra is realized.