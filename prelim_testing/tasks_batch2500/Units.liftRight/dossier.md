## Object

`VTask.liftRight` constructs a monoid homomorphism `M →* Nˣ` (from a monoid `M` into the units of a monoid `N`) out of two pieces of data: an ordinary monoid homomorphism `f : M →* N` and a function `g : M → Nˣ` that happens to land in the units of `N`, provided one supplies a proof that the coercion of `g(x)` back into `N` agrees with `f(x)` for every `x`. In other words, it promotes a unit-valued function that is "compatible" with a known homomorphism into a genuine homomorphism into the group of units.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.liftRight : {M : Type u} -> {N : Type v} -> [Monoid M] -> [Monoid N] -> (f : M →* N) -> (g : M → Nˣ) -> (h : ∀ (x : M), ↑(g x) = f x) -> M →* Nˣ
<!-- PINNED-SIGNATURE:END -->


`VTask.liftRight : {M : Type u} -> {N : Type v} -> [Monoid M] -> [Monoid N] -> (f : M →* N) -> (g : M → Nˣ) -> (h : ∀ (x : M), ↑(g x) = f x) -> M →* Nˣ`

The implicit type arguments `M` and `N` are the source and target monoids, respectively. The monoid structures on `M` and `N` are supplied as instance arguments. The argument `f` is the reference monoid homomorphism from `M` to `N` that witnesses the multiplicative structure. The argument `g` is a function from `M` into the units `Nˣ` of `N`; it need not a priori be a homomorphism, but its values must be units. The argument `h` is the coherence hypothesis: for every element `x` of `M`, the coercion of the unit `g(x)` to an element of `N` equals `f(x)`.

## Conventions

The underlying function of the resulting homomorphism is exactly `g`; the homomorphism structure (identity and multiplication) is derived entirely from `f` and the coherence hypothesis `h`, not by any independent computation on `g`.

## Worked examples

- Claim: When `f` is the identity homomorphism on `Nˣ` composed with the coercion to `N`, and `g` is the identity on `Nˣ`, the result of `VTask.liftRight` applied to any element `x` is `x` itself.

- Claim: For the trivial monoid `Unit` with `f : Unit →* Nˣ` the constant map to `1` and `g : Unit → Nˣ` also constant at `1` (with coherence `h` trivial), `VTask.liftRight f g h` is the trivial homomorphism sending the unique element to `1 : Nˣ`.

- Claim: For any `f`, `g`, `h`, and any `x : M`, the coercion `↑(VTask.liftRight f g h x)` equals `f x` in `N` (this is the content of `Units.coe_liftRight`).

- Claim: For any `f`, `g`, `h`, and any `x : M`, multiplying `f x` by the coercion of the inverse of `VTask.liftRight f g h x` yields `1` in `N`.

## Boundaries

- The coherence condition `h` is essential: without it the function `g` might not be multiplicative in any compatible sense. The construction would be ill-typed without this proof.
- The resulting homomorphism's underlying function is literally `g`, so evaluating `VTask.liftRight f g h x` yields exactly `g x` as a term of type `Nˣ`.
- The construction is total: it places no restriction on `M`, `N`, `f`, or `g` beyond what the types already enforce (namely that `g` lands in `Nˣ` and that the coherence holds).
- When `N` itself is a group, every element is a unit, so `Nˣ` is isomorphic to `N` and the construction specialises to ordinary lifting of a homomorphism along the units isomorphism.

## Not to be confused with

- `MonoidHom.toHomUnits`: lifts an existing monoid homomorphism `M →* N` to `M →* Nˣ` when every value of `f` is a unit, without requiring a separate function `g`.
- `Units.lift` (if present): a more general construction that may not require the coherence hypothesis.
- `Units.map`: the functorial action that post-composes a homomorphism `M →* N` with the units functor, producing `Mˣ →* Nˣ`, which goes in the opposite direction (source is units, not target).