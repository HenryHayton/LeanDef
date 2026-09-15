## VTask.lift

### Object

Given a directed system of commutative `R`-algebras `G i` (indexed by a directed preorder `ι`, with transition maps `f i j hij : G i → G j` for `i ≤ j`), the **direct limit** `DirectLimit G f` is the colimit of this system in the category of `R`-algebras. `VTask.lift` realises the universal property of this colimit: given any `R`-algebra `P` and a compatible family of `R`-algebra homomorphisms `g i : G i →ₐ[R] P` (compatible meaning `g j (f i j hij x) = g i x` for all `i ≤ j` and all `x : G i`), there is a unique `R`-algebra homomorphism `DirectLimit G f →ₐ[R] P` such that composing with each canonical inclusion `of G f i : G i →ₐ[R] DirectLimit G f` recovers `g i`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {R : Type u_1} -> {ι : Type u_2} -> [Preorder ι] -> (G : ι → Type u_3) -> {T : ⦃i j : ι⦄ → i ≤ j → Type u_6} -> (f : (x x_1 : ι) → (h : x ≤ x_1) → T h) -> [(i j : ι) → (h : i ≤ j) → FunLike (T h) (G i) (G j)] -> [DirectedSystem G fun x1 x2 x3 => ⇑(f x1 x2 x3)] -> [IsDirectedOrder ι] -> [CommSemiring R] -> [(i : ι) → Semiring (G i)] -> [(i : ι) → Algebra R (G i)] -> [∀ (i j : ι) (h : i ≤ j), AlgHomClass (T h) R (G i) (G j)] -> [Nonempty ι] -> (P : Type u_7) -> [Semiring P] -> [Algebra R P] -> (g : (i : ι) → G i →ₐ[R] P) -> (Hg : ∀ (i j : ι) (hij : i ≤ j) (x : G i), (g j) ((f i j hij) x) = (g i) x) -> DirectLimit G f →ₐ[R] P
<!-- PINNED-SIGNATURE:END -->


`VTask.lift : {R : Type u_1} -> {ι : Type u_2} -> [Preorder ι] -> (G : ι → Type u_3) -> {T : ⦃i j : ι⦄ → i ≤ j → Type u_6} -> (f : (x x_1 : ι) → (h : x ≤ x_1) → T h) -> [(i j : ι) → (h : i ≤ j) → FunLike (T h) (G i) (G j)] -> [DirectedSystem G fun x1 x2 x3 => ⇑(f x1 x2 x3)] -> [IsDirectedOrder ι] -> [CommSemiring R] -> [(i : ι) → Semiring (G i)] -> [(i : ι) → Algebra R (G i)] -> [∀ (i j : ι) (h : i ≤ j), AlgHomClass (T h) R (G i) (G j)] -> [Nonempty ι] -> (P : Type u_7) -> [Semiring P] -> [Algebra R P] -> (g : (i : ι) → G i →ₐ[R] P) -> (Hg : ∀ (i j : ι) (hij : i ≤ j) (x : G i), (g j) ((f i j hij) x) = (g i) x) -> DirectLimit G f →ₐ[R] P`

- `R` is the base commutative semiring over which all algebras are defined.
- `ι` is the index type, equipped with a directed preorder structure via `[Preorder ι]` and `[IsDirectedOrder ι]`.
- `G` is the functor assigning to each index `i` the `R`-algebra `G i`.
- `T` is the type family for transition morphisms; the transition map from `G i` to `G j` when `i ≤ j` has type `T h`.
- `f` produces the actual transition maps: for each `i ≤ j`, `f i j h : T h` is the `R`-algebra homomorphism `G i → G j`.
- The `FunLike`, `DirectedSystem`, `AlgHomClass`, `Semiring`, and `Algebra` instances assert that the transition maps form a valid directed system of `R`-algebras.
- `[Nonempty ι]` ensures the index category is non-empty, which is required for the direct limit to be well-formed.
- `P` is the target `R`-algebra (a semiring with an `R`-algebra structure).
- `g` is the compatible family: for each `i`, an `R`-algebra homomorphism `G i →ₐ[R] P`.
- `Hg` is the compatibility (commutativity) condition asserting that the maps `g i` intertwine with the transition maps: applying `f i j hij` then `g j` equals applying `g i` directly.

### Conventions

There are no declared junk-value conventions for this definition: the function is only called when all typeclass and data requirements (directed system, algebra structures, compatibility condition) are satisfied, so there are no edge inputs with arbitrary or degenerate output behaviour.

### Worked examples

- Claim: For any compatible family `g` with compatibility `Hg`, composing the lift with the canonical inclusion `of G f i` recovers `g i` — that is, `(VTask.lift G f P g Hg).comp (of G f i) = g i`.

- Claim: For any element `x : G i`, evaluating the lift at the image of `x` under the canonical inclusion gives `g i x` — that is, `VTask.lift G f P g Hg (of G f i x) = g i x`.

- Claim: The result of `VTask.lift G f P g Hg` is an `R`-algebra homomorphism `DirectLimit G f →ₐ[R] P`, and in particular it commutes with the `R`-algebra structure maps (e.g., `algebraMap R (DirectLimit G f)`) on both sides.

### Boundaries

- If `ι` is a singleton (a single-element directed order), the direct limit is isomorphic to the unique `G i`, and `VTask.lift` reduces to `g i` itself.
- The compatibility condition `Hg` is necessary: without it, one cannot define a well-posed map out of the direct limit (which identifies elements related by transition maps). If `Hg` does not hold, the resulting construction would not be well-defined as a function.
- Uniqueness of the lift: by the universal property, any two `R`-algebra homomorphisms `DirectLimit G f →ₐ[R] P` that agree on every `of G f i` must be equal. Thus `VTask.lift` produces the unique such map satisfying the intertwining condition.
- The index type must be `Nonempty`; this is required so that the direct limit itself is non-trivial and has the expected algebraic structure.

### Not to be confused with

- `DirectLimit.lift` for rings (without the algebra structure): that is the ring-theoretic version of the same construction, without tracking the `R`-linear/algebra structure.
- `DirectLimit.of G f i`: the canonical inclusion map `G i →ₐ[R] DirectLimit G f` pointing *into* the direct limit, as opposed to `VTask.lift` which constructs maps *out of* it.
- The direct limit of *modules* (as opposed to algebras): the universal property there applies to `R`-linear maps rather than `R`-algebra homomorphisms.
