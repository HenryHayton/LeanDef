## Object

`VTask.noncommCoprod f g comm` is the canonical monoid homomorphism from the direct product `M × N` to a monoid `P`, obtained by multiplying the images of the two components: given a pair `(m, n)`, it returns `f(m) · g(n)`. The construction works even when `P` is non-commutative, provided one supplies a proof that every element in the image of `f` commutes with every element in the image of `g`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.noncommCoprod : {M : Type u_1} -> {N : Type u_2} -> {P : Type u_3} -> [MulOneClass M] -> [MulOneClass N] -> [Monoid P] -> (f : M →* P) -> (g : N →* P) -> (comm : ∀ (m : M) (n : N), Commute (f m) (g n)) -> M × N →* P
<!-- PINNED-SIGNATURE:END -->


`VTask.noncommCoprod : {M : Type u_1} -> {N : Type u_2} -> {P : Type u_3} -> [MulOneClass M] -> [MulOneClass N] -> [Monoid P] -> (f : M →* P) -> (g : N →* P) -> (comm : ∀ (m : M) (n : N), Commute (f m) (g n)) -> M × N →* P`

- `M`, `N`, and `P` are the types of the source components and the common codomain, carrying their respective monoid structures via the instance arguments.
- `f` is the monoid homomorphism applied to the first component.
- `g` is the monoid homomorphism applied to the second component.
- `comm` is a proof that for every `m : M` and `n : N`, the elements `f m` and `g n` commute in `P` (i.e., `f(m) · g(n) = g(n) · f(m)`); this is the condition that makes the construction well-behaved without assuming `P` is commutative.

The result is a monoid homomorphism `M × N →* P`.

## Conventions

No junk-value or edge conventions are declared: the definition is total for any `f`, `g`, and `comm` satisfying the type constraints, and there are no degenerate input regimes requiring special treatment.

## Worked examples

- Claim: Composing `VTask.noncommCoprod f g comm` with the left inclusion `inl : M →* M × N` recovers `f`.

- Claim: Composing `VTask.noncommCoprod f g comm` with the right inclusion `inr : N →* M × N` recovers `g`.

- Claim: `VTask.noncommCoprod (inl M N) (inr M N) commute_inl_inr` equals the identity on `M × N`; in other words, the two canonical inclusions into the product together generate the identity via `noncommCoprod`.

- Claim: For any monoid homomorphism `h : M × N →* P`, the morphism `VTask.noncommCoprod (h.comp (inl M N)) (h.comp (inr M N)) _` equals `h` (universal property / uniqueness).

- Claim: For the trivial case where `M = N = P = Unit`, `VTask.noncommCoprod` sends every pair to the unique element `()` of `Unit`.

## Boundaries

- When `f` or `g` is the trivial (constant-one) homomorphism, `VTask.noncommCoprod f g comm` reduces to the other factor: e.g., if `f` is trivial, the result maps `(m, n)` to `g(n)` (since `f(m) = 1` and `1 · g(n) = g(n)`).
- The commutativity hypothesis `comm` is essential for the map to be a homomorphism in general; if `P` is commutative, the condition is automatically satisfied for any `f` and `g`.
- The result is injective if and only if both `f` and `g` are injective and the ranges of `f` and `g` are disjoint as subgroups (in the group case).
- The range of `VTask.noncommCoprod f g comm` (in the group case) equals the join `f.range ⊔ g.range` in the subgroup lattice of `P`.

## Not to be confused with

- `MonoidHom.coprod`: the analogous coproduct for **commutative** monoids, which does not require a commutativity proof and is defined in a commutative setting.
- `MulEquiv.prodCongr` / `MonoidHom.prod`: constructs a homomorphism `M × N →* P × Q` component-wise, rather than multiplying both components into a single target.
- `FreeProduct.lift`: the coproduct in the category of monoids or groups without any commutativity assumption, whose domain is the free product rather than the direct product.