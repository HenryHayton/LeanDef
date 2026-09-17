## Object

`VTask.prodMap f g` is the semigroup homomorphism from the product semigroup `M × N` to the product semigroup `M' × N'` that applies `f` component-wise to the first factor and `g` component-wise to the second factor. In other words, it is the canonical "product of two homomorphisms", sending a pair `(m, n)` to `(f m, g n)`, in the category of semigroups (magmas with associative multiplication).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prodMap : {M : Type u_3} -> {N : Type u_4} -> {M' : Type u_6} -> {N' : Type u_7} -> [Mul M] -> [Mul N] -> [Mul M'] -> [Mul N'] -> (f : M →ₙ* M') -> (g : N →ₙ* N') -> M × N →ₙ* M' × N'
<!-- PINNED-SIGNATURE:END -->


`VTask.prodMap : {M : Type u_3} -> {N : Type u_4} -> {M' : Type u_6} -> {N' : Type u_7} -> [Mul M] -> [Mul N] -> [Mul M'] -> [Mul N'] -> (f : M →ₙ* M') -> (g : N →ₙ* N') -> M × N →ₙ* M' × N'`

The implicit type arguments `M`, `N`, `M'`, `N'` are the four semigroup (mul-magma) types involved. The four typeclass arguments supply the multiplications on each of these types. The explicit argument `f` is a `MulHom` (semigroup homomorphism, denoted `M →ₙ*  M'`) to be applied to the first component, and `g` is a `MulHom` (`N →ₙ* N'`) to be applied to the second component.

## Conventions

There are no junk-value or edge-case conventions declared for this definition: the construction is total for all valid inputs and the behavior on every element is determined by the formula `(m, n) ↦ (f m, g n)`, with no special treatment for identity elements, empty types, or other boundary cases.

## Worked examples

- Claim: For `f : ℕ →ₙ* ℕ` and `g : ℕ →ₙ* ℕ` both being the identity `MulHom`, `VTask.prodMap f g (3, 5) = (3, 5)`.

- Claim: For any `(m, n) : M × N`, the first component of `VTask.prodMap f g (m, n)` equals `f m`, and the second component equals `g n`.

- Claim: `VTask.prodMap f g` is a `MulHom`, meaning it satisfies `VTask.prodMap f g (a * b) = VTask.prodMap f g a * VTask.prodMap f g b` for all `a b : M × N`. This follows from `f` and `g` each being `MulHom`s, so multiplication in the product is respected component-wise.

## Boundaries

- The definition works for any types carrying a `Mul` instance; neither associativity nor a unit are required. Thus it applies to raw magmas, semigroups, and monoids alike.
- When `M = N = M' = N'` and `f = g = id`, `VTask.prodMap f g` is the identity `MulHom` on `M × M`.
- When either `f` or `g` is a constant map (if such a `MulHom` exists for the given types), `VTask.prodMap f g` maps every pair to a pair whose corresponding component is constant.
- The definition does not require the types to be non-empty.

## Not to be confused with

- `MulHom.prod f g`: Given `f : M →ₙ* N` and `g : M →ₙ* P` with the *same* source `M`, this forms a hom into `N × P` by pairing — distinct from `prodMap`, which takes *two* homs with *different* sources.
- `Prod.map f g` (the plain function): The function-level `Prod.map` does not carry or verify the `MulHom` structure; `VTask.prodMap` is its upgrade to the category of mul-magmas.
- `MulHom.fst` / `MulHom.snd`: These are the *projection* `MulHom`s from a product; `VTask.prodMap` goes the opposite direction (into a product).