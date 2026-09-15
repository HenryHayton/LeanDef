## Object

`VTask.zmod n x` is the additive character of `ZMod n` with values in the unit circle `Circle ⊆ ℂ` indexed by the element `x ∈ ZMod n`. Concretely, it is the group homomorphism `ZMod n → Circle` that sends `y` to `e^(2πi·x·y/n)`, i.e., the character whose frequency (or Pontryagin-dual parameter) is `x`. Together these characters exhaust all complex additive characters of `ZMod n`, giving a natural isomorphism between `ZMod n` and its own Pontryagin dual.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.zmod : (n : ℕ) -> [NeZero n] -> (x : ZMod n) -> AddChar (ZMod n) Circle
<!-- PINNED-SIGNATURE:END -->


`VTask.zmod : (n : ℕ) -> [NeZero n] -> (x : ZMod n) -> AddChar (ZMod n) Circle`

The first argument `n` is the modulus, i.e., the order of the cyclic group `ZMod n`; the instance `[NeZero n]` ensures the modulus is nonzero so that `ZMod n` is a well-formed finite cyclic group. The second argument `x` is the index of the character inside the Pontryagin dual: it selects which of the `n` distinct additive characters is returned.

## Conventions

When `x = 0`, the resulting character is the trivial (principal) character sending every `y` to `1 ∈ Circle`, since `e^(2πi·0·y/n) = 1` for all `y`. No other junk-value conventions are declared for this definition; it is well-defined and non-trivial for every nonzero `x`.

## Worked examples

- Claim: `VTask.zmod 4 0` is the trivial additive character of `ZMod 4`, sending every element to `1 ∈ Circle`.

- Claim: `VTask.zmod 4 1` evaluated at `1 : ZMod 4` returns `e^(2πi·1·1/4) = e^(πi/2) = i ∈ Circle`.

- Claim: `VTask.zmod n x` is a group homomorphism, i.e., for all `y z : ZMod n`, `(VTask.zmod n x) (y + z) = (VTask.zmod n x) y * (VTask.zmod n x) z`; this follows from the `AddChar` structure.

- Claim: The map `x ↦ VTask.zmod n x` is injective, so distinct elements of `ZMod n` yield distinct characters; this reflects the non-degeneracy of the pairing `(x, y) ↦ e^(2πi·x·y/n)`.

## Boundaries

- The `NeZero n` hypothesis is required; without it `ZMod 0 = ℤ` and the formula `e^(2πi·x·y/n)` is undefined (division by zero), so this construction is simply not available at `n = 0`.
- At `x = 0 : ZMod n` the character is trivially the constant map to `1`, the identity of `Circle`.
- At `x = n - 1` (the element just below the modulus), the character is the complex conjugate of the character at `x = 1`, since `e^(2πi·(n-1)·y/n) = \overline{e^(2πi·y/n)}`.
- All `n` characters obtained this way are distinct and together they form a complete orthonormal system for `ZMod n`, with the standard discrete Fourier orthogonality relation.

## Not to be confused with

- `AddChar.mulShift` or generic `AddChar` constructors: those build characters for arbitrary additive groups, whereas `VTask.zmod` specifically exploits the ring structure of `ZMod n` to parametrise characters by elements of the same ring.
- `ZMod.toAddCircle`: this is a group homomorphism `ZMod n → AddCircle (1/n)` (or similar), a step in the construction but not itself an element of `AddChar (ZMod n) Circle`.
- The multiplicative characters of `ZMod n` (Dirichlet characters): those are homomorphisms from the multiplicative group `(ZMod n)ˣ` to `Circle`, not additive characters of the additive group.