## Object

`VTask.noncommCoprod f g comm` is the **non-commutative coproduct** of two multiplicative homomorphisms `f : M →ₙ* P` and `g : N →ₙ* P` into a common semigroup codomain `P`. It is the unique `MulHom` from the direct product `M × N` to `P` that acts on a pair `(m, n)` by `f m * g n` (left factor first, then right factor), where the commutativity hypothesis `comm` ensures that this formula is itself multiplicative. In the commutative setting one would use the ordinary coproduct; here the explicit `Commute` assumption replaces the requirement that `P` be commutative.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.noncommCoprod : {M : Type u_1} -> {N : Type u_2} -> {P : Type u_3} -> [Mul M] -> [Mul N] -> [Semigroup P] -> (f : M →ₙ* P) -> (g : N →ₙ* P) -> (comm : ∀ (m : M) (n : N), Commute (f m) (g n)) -> M × N →ₙ* P
<!-- PINNED-SIGNATURE:END -->


`{M : Type u_1} -> {N : Type u_2} -> {P : Type u_3} -> [Mul M] -> [Mul N] -> [Semigroup P] -> (f : M →ₙ* P) -> (g : N →ₙ* P) -> (comm : ∀ (m : M) (n : N), Commute (f m) (g n)) -> M × N →ₙ* P`

The first three implicit type arguments are the types of the two source monoids/semigroups and the common target semigroup. The next three implicit arguments supply the necessary `Mul` instances on the sources and the `Semigroup` structure on the target. `f` is the multiplicative homomorphism from the left factor `M` to `P`. `g` is the multiplicative homomorphism from the right factor `N` to `P`. `comm` is the family of proofs asserting that, for every `m : M` and `n : N`, the elements `f m` and `g n` commute in `P` (i.e., `f m * g n = g n * f m`); this is the key hypothesis that makes the product formula multiplicative without requiring `P` to be commutative.

## Conventions

The canonical evaluation formula is `(VTask.noncommCoprod f g comm) (m, n) = f m * g n`; the left factor is applied first and the right factor second. There is an alternative evaluation identity `(VTask.noncommCoprod f g comm) (m, n) = g n * f m`, which holds because `comm m n` says exactly that these two orderings agree.

## Worked examples

- Claim: For `f = MulHom.id ℕ` (viewed additively as multiplication-by-1) and `g = MulHom.id ℕ` mapping into the commutative semigroup `(ℕ, *)`, `(VTask.noncommCoprod f g comm) (3, 4) = f 3 * g 4 = 3 * 4 = 12`.

- Claim: Composing `VTask.noncommCoprod f g comm` with a further `MulHom` `h : P →ₙ* Q` yields `VTask.noncommCoprod (h.comp f) (h.comp g) _`, i.e., `h` distributes over the non-commutative coproduct construction.

- Claim: When `P` is a commutative semigroup, the condition `comm m n` is always satisfied, so `VTask.noncommCoprod f g comm` coincides with the ordinary coproduct; in particular its value on `(m, n)` equals both `f m * g n` and `g n * f m`.

## Boundaries

- The type `P` is only required to be a `Semigroup` (not a monoid or group), so there is no identity element or inverses assumed in the codomain.
- The types `M` and `N` only need `Mul` (not even associativity), since their role is solely as domains of the input homomorphisms.
- If `comm` is not actually a proof of commutativity (e.g., wrong values supplied), the resulting map is still well-typed but may not satisfy the multiplicativity axiom in practice — the correctness of `comm` is trusted by the construction.
- There are no junk-value or partial-function considerations: the definition is total on all pairs `(m, n) : M × N`.

## Not to be confused with

- `MulHom.coprod`: the ordinary coproduct for a commutative (or at least a fully commutative) codomain, which does not require an explicit commutativity hypothesis.
- `FreeProduct.lift` / coproduct in the category of groups: the non-commutative coproduct in the categorical sense (the free product), which is a very different construction involving words.
- `MulHom.prod`: pairs a morphism `M →ₙ* P` with `M →ₙ* Q` into `M →ₙ* P × Q`, mapping a single source into a product codomain rather than a product source into a single codomain.