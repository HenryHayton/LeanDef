## VTask.eqLocusM

### Object

Given two monoid homomorphisms `f` and `g` from a monoid `M` to a monoid `N`, `VTask.eqLocusM f g` is the **equalizer submonoid** of `f` and `g`: the set of all elements `x` in `M` at which `f` and `g` agree (i.e., `f x = g x`), equipped with the submonoid structure inherited from `M`. It is a submonoid because the identity element is always in it (since both homomorphisms send `1` to `1`) and the set is closed under multiplication (since both homomorphisms respect multiplication).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.eqLocusM : {M : Type u_1} -> {N : Type u_2} -> [MulOneClass M] -> [MulOneClass N] -> (f g : M →* N) -> Submonoid M
<!-- PINNED-SIGNATURE:END -->


The two implicit type arguments are the domain monoid type `M` and the codomain monoid type `N`, each required to carry a `MulOneClass` instance. The two explicit arguments `f` and `g` are the pair of monoid homomorphisms `M →* N` whose agreement locus is being formed.

### Conventions

No special junk-value or edge-case output conventions are declared: the construction is total and well-defined for any two monoid homomorphisms between any two `MulOneClass` types.

### Worked examples

- Claim: For any monoid homomorphism `f : M →* N`, every element of `M` lies in `VTask.eqLocusM f f`, i.e., `VTask.eqLocusM f f = ⊤`.

- Claim: An element `x : M` belongs to `VTask.eqLocusM f g` if and only if `f x = g x`.

- Claim: For the monoid homomorphisms `f = MonoidHom.id ℕ` and `g = MonoidHom.id ℕ`, the equalizer submonoid `VTask.eqLocusM f g` equals `⊤` (all of `ℕ` under multiplication).

- Claim: If `f : M →* N` and `g : M →* N` disagree on some element `x`, then `x` is not a member of `VTask.eqLocusM f g`.

### Boundaries

- When `f = g` (the same homomorphism is passed twice), the equalizer submonoid is the entire monoid `M` (i.e., equals `⊤`).
- When `f` and `g` disagree on every non-identity element, the equalizer submonoid contains at minimum the identity element `1`, since both homomorphisms must send `1` to `1`.
- The construction is valid for any `MulOneClass`, not just groups or commutative monoids — no additional algebraic structure is required.

### Not to be confused with

- `MonoidHom.eqLocus` (for groups): a similar construction that produces a subgroup rather than a submonoid, applicable when `M` and `N` carry full group structure.
- The kernel of a single homomorphism `f`: the kernel is the preimage of `{1}` under `f` alone, whereas `VTask.eqLocusM f g` compares two homomorphisms pointwise.
- The set-theoretic equalizer `{x | f x = g x}` as a plain set: `VTask.eqLocusM f g` packages this set together with its submonoid structure, making it a term of type `Submonoid M` rather than `Set M`.
