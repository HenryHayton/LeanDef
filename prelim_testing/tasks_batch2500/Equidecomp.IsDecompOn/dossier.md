## VTask.IsDecompOn

### Object

`VTask.IsDecompOn f A S` is a predicate asserting that the function `f : X → X` is a *decomposition on* the set `A`, witnessed by the finite set `S` of group elements. Concretely, this means that for every point `a` in `A`, the value `f(a)` is obtained by acting on `a` with some element of `S`. Informally, one can partition `A` into finitely many pieces — one piece per group element in `S` — and on each piece, `f` acts exactly as that group element. This is the notion of a "decomposition" underlying the Banach–Tarski style equidecomposition theory: a bijection from one set to another that is piecewise given by group elements.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsDecompOn : {X : Type u_1} -> {G : Type u_2} -> [SMul G X] -> (f : X → X) -> (A : Set X) -> (S : Finset G) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsDecompOn : {X : Type u_1} -> {G : Type u_2} -> [SMul G X] -> (f : X → X) -> (A : Set X) -> (S : Finset G) -> Prop
```

The ambient type `X` is the space on which everything lives. The type `G` is the group (or monoid) whose elements act on `X`, with the scalar multiplication `SMul G X` providing the action. The argument `f` is the function whose behavior on `A` we are examining. The argument `A` is the subset of `X` on which the decomposition is required to hold. The argument `S` is the finite *witness set* of group elements: every value `f(a)` for `a ∈ A` must be of the form `g • a` for some `g ∈ S`.

### Conventions

There are no special junk-value or boundary conventions declared for this definition. Outside of `A`, the behavior of `f` is entirely unconstrained by the predicate; the condition is purely local to the set `A`.

### Worked examples

- Claim: If `G = ℤ` acts on `X = ℤ` by addition and `f = id`, then `VTask.IsDecompOn f Set.univ {0}` holds, because `id a = 0 + a` for all `a`.

- Claim: If `S` contains every group element used by `f` on `A`, then `VTask.IsDecompOn f A S` holds. In particular, a function whose restriction to `A` equals the action of a single element `g` satisfies `VTask.IsDecompOn f A {g}`.

- Claim: `VTask.IsDecompOn f A S` implies `VTask.IsDecompOn f A' S` whenever `A' ⊆ A` and `f` agrees with `f` on `A'` (monotonicity in the domain set). Formally, this is the content of `IsDecompOn.mono`.

- Claim: If `VTask.IsDecompOn f A S` and `VTask.IsDecompOn g B T` and `f` maps `A` into `B`, then `VTask.IsDecompOn (g ∘ f) A (T * S)` holds; the composed function is witnessed by the product of the two finite witness sets.

### Boundaries

- When `A` is the empty set, `VTask.IsDecompOn f ∅ S` holds vacuously for any `f` and any `S`, including the empty finset, because there are no elements to check.
- When `S` is the empty finset, `VTask.IsDecompOn f A ∅` holds if and only if `A` is empty, since no witness can be found for any point.
- The predicate places no constraint on `f` outside `A`; two functions that agree on `A` are interchangeable as far as `VTask.IsDecompOn` is concerned.
- The predicate does not require `f` to be injective, surjective, or even measurable; it is a purely pointwise-existential condition.
- Enlarging `S` (passing to a superset) preserves the predicate: if `VTask.IsDecompOn f A S` and `S ⊆ S'`, then `VTask.IsDecompOn f A S'`.

### Not to be confused with

- **`Equidecomp`** (equidecomposability of two sets): this is the symmetric relation asserting that two sets are related by a piecewise-group-element bijection; `VTask.IsDecompOn` is the one-sided, one-function ingredient used to build that relation.
- **`MapsTo f A B`**: asserts that `f` sends `A` into `B`, with no reference to a group action or a finite witness set.
- **`EqOn f g A`**: asserts that two functions agree on `A`, which is a condition between two functions rather than a condition relating a function to a group action.
