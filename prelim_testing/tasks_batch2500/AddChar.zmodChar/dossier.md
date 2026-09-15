## VTask.zmodChar

### Object

Given a commutative monoid `C`, a positive natural number `n`, and an element `ζ` of `C` satisfying `ζ^n = 1` (an `n`th root of unity), `VTask.zmodChar n hζ` is the additive character from `ZMod n` to `C` that sends each residue class `a` to `ζ^a`, where `a` is lifted to its canonical representative in `{0, 1, …, n−1}`. Concretely, it is the group homomorphism `(ZMod n, +) → (C, ×)` defined by `a ↦ ζ^(a.val)`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.zmodChar : {C : Type v} -> [CommMonoid C] -> (n : ℕ) -> [NeZero n] -> {ζ : C} -> (hζ : ζ ^ n = 1) -> AddChar (ZMod n) C
<!-- PINNED-SIGNATURE:END -->


The type variable `C` is the target commutative monoid. The instance `[CommMonoid C]` supplies the multiplicative structure of `C`. The argument `n : ℕ` is the modulus, i.e., the order of the cyclic group `ZMod n` serving as the domain; the instance `[NeZero n]` ensures `n` is positive so that `ZMod n` is a nontrivial cyclic group. The implicit argument `ζ : C` is the chosen `n`th root of unity in `C`. The explicit argument `hζ : ζ ^ n = 1` is the proof that `ζ` is indeed an `n`th root of unity, which is necessary to ensure the character is well-defined modulo `n`.

### Conventions

No junk-value or boundary conventions are declared: the definition is total and well-typed whenever the typeclass assumptions `[CommMonoid C]` and `[NeZero n]` are satisfied and `hζ` is supplied.

### Worked examples

- Claim: `VTask.zmodChar 4 (show (Complex.exp (2 * Real.pi * Complex.I / 4)) ^ 4 = 1 from ...)` evaluated at `0 : ZMod 4` equals `1`. The character always maps `0` to `1` because `ζ^0 = 1` in any monoid.

- Claim: For `n = 3` and `ζ = 1 : ℤˣ` (which satisfies `1^3 = 1`), `VTask.zmodChar 3 (show (1 : ℤˣ) ^ 3 = 1 from by norm_num)` maps every element of `ZMod 3` to `1`, giving the trivial character.

- Claim: For `n = 2` and `ζ = -1 : ℤ` (satisfying `(-1)^2 = 1`), the character `VTask.zmodChar 2 (show (-1 : ℤ) ^ 2 = 1 from by norm_num)` maps `(0 : ZMod 2)` to `1` and `(1 : ZMod 2)` to `-1`.

- Claim: `VTask.zmodChar n hζ` is a homomorphism of additive characters in the sense that evaluating it at `x + y` equals the product of its values at `x` and at `y`, for all `x y : ZMod n`.

### Boundaries

- At `a = 0 : ZMod n`, the character evaluates to `ζ^0 = 1`, so it always maps the additive identity to the multiplicative identity, as required of a monoid homomorphism.
- When `ζ = 1`, the resulting character is identically `1` on all of `ZMod n` (the trivial character).
- The constraint `[NeZero n]` is essential: for `n = 0`, `ZMod 0` is the integers and the construction does not apply in this form.
- The value of the character at `a` depends only on `a.val mod n`, consistent with the well-definedness guaranteed by `hζ`.
- Different choices of `n`th root `ζ` (e.g., primitive vs. non-primitive) yield different characters, though all are valid additive characters.

### Not to be confused with

- `AddChar.primitive`: a predicate asserting that a given additive character is primitive (not induced from a character of a smaller quotient); `VTask.zmodChar` constructs a character but does not assert primitivity.
- `ZMod.unitOfCoprime` or characters defined via Dirichlet characters: those target `ℂˣ` and involve multiplicative structure of `ZMod n`, whereas `VTask.zmodChar` uses only the additive group structure of `ZMod n`.
- `MulChar` on `ZMod n`: a multiplicative character `(ZMod n)× → C` mapping the multiplicative group, as opposed to `VTask.zmodChar` which is an additive character on the additive group `ZMod n`.