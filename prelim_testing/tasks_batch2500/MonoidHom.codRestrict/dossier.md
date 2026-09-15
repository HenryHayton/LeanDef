## Object

`VTask.codRestrict` produces a monoid homomorphism from a monoid `M` into a submonoid `s` of a monoid `N`, given a monoid homomorphism `f : M →* N` whose image is entirely contained in `s`. In other words, it "narrows" the codomain of `f` from all of `N` down to the submonoid `s`, yielding a new homomorphism whose values are, by construction, elements of `s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.codRestrict : {M : Type u_1} -> {N : Type u_2} -> [MulOneClass M] -> [MulOneClass N] -> {S : Type u_5} -> [SetLike S N] -> [SubmonoidClass S N] -> (f : M →* N) -> (s : S) -> (h : ∀ (x : M), f x ∈ s) -> M →* ↥s
<!-- PINNED-SIGNATURE:END -->


VTask.codRestrict : {M : Type u_1} -> {N : Type u_2} -> [MulOneClass M] -> [MulOneClass N] -> {S : Type u_5} -> [SetLike S N] -> [SubmonoidClass S N] -> (f : M →* N) -> (s : S) -> (h : ∀ (x : M), f x ∈ s) -> M →* ↥s

The type `M` is the domain monoid; `N` is the ambient codomain monoid; `S` is the type of submonoid-like objects of `N` (the "container" type for submonoids, e.g., `Submonoid N`). The argument `f` is the monoid homomorphism being restricted; `s` is the specific submonoid (of type `S`) to which the codomain is being restricted; and `h` is the proof obligation confirming that every element in the image of `f` belongs to `s`.

## Conventions

The resulting homomorphism's underlying function sends each `x : M` to the element `f x` packaged together with the membership proof `h x`, so the "value" as an element of `N` is exactly `f x`. There are no special junk-value conventions declared for this definition.

## Worked examples

- Claim: For the monoid homomorphism `f : ℕ →* ℕ` defined by `f n = n`, restricting to the submonoid `⊤` (all of `ℕ`) gives a map whose underlying `N`-value at any `n` equals `n`.

- Claim: If `f : M →* N` is a monoid homomorphism whose range lies in a submonoid `s`, then `VTask.codRestrict f s h` composed with the inclusion `s ↪ N` equals `f` as functions `M → N`.

- Claim: The kernel of `VTask.codRestrict f s h` (as a subgroup, when the setting allows) equals the kernel of the original homomorphism `f`.

- Claim: `VTask.codRestrict f s h` is injective if and only if `f` itself is injective.

## Boundaries

- If `s = ⊤` (the top submonoid, i.e., all of `N`), the construction is well-typed and produces a homomorphism into `↥⊤ ≅ N`; the proof `h` is trivially satisfied.
- If `f` is the trivial (constant-one) homomorphism, then `h` reduces to showing that `1 ∈ s`, which holds for any submonoid.
- The proof `h` is not computationally significant — it only affects type membership; the underlying values of the resulting map are exactly those of `f`.
- The definition is total: there is no restriction on `M`, `N`, `f`, or `s` beyond the typeclass assumptions already stated.

## Not to be confused with

- `MonoidHom.restrict` (domain restriction): restricts the *domain* of a monoid homomorphism to a submonoid of `M`, rather than the codomain.
- `MonoidHom.rangeRestrict`: a special case that restricts the codomain specifically to the *range* (image) of `f` inside `N`, without requiring an external membership proof.
- `Submonoid.inclusion`: a canonical monoid homomorphism between two submonoids arising from one being contained in the other, rather than restricting an arbitrary homomorphism.