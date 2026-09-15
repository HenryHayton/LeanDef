## VTask.lift

### Object

`VTask.lift` constructs the canonical linear map out of a module direct limit. Given a directed system of modules `G i` indexed by a preordered type `ι`, connected by transition maps `f i j : G i →ₗ[R] G j` for `i ≤ j`, and given a compatible family of linear maps `g i : G i →ₗ[R] P` into a target module `P` (compatible meaning that `g j ∘ f i j = g i` for all `i ≤ j`), `VTask.lift` produces a unique linear map `Module.DirectLimit G f →ₗ[R] P` whose restriction to each component `G i` (via the canonical inclusion) agrees with `g i`. This is the universal property of the colimit in the category of `R`-modules.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : (R : Type u_1) -> [Semiring R] -> (ι : Type u_2) -> [Preorder ι] -> (G : ι → Type u_3) -> [(i : ι) → AddCommMonoid (G i)] -> [(i : ι) → Module R (G i)] -> (f : (i j : ι) → i ≤ j → G i →ₗ[R] G j) -> [DecidableEq ι] -> {P : Type u_4} -> [AddCommMonoid P] -> [Module R P] -> (g : (i : ι) → G i →ₗ[R] P) -> (Hg : ∀ (i j : ι) (hij : i ≤ j) (x : G i), (g j) ((f i j hij) x) = (g i) x) -> Module.DirectLimit G f →ₗ[R] P
<!-- PINNED-SIGNATURE:END -->


`VTask.lift (R : Type u_1) [Semiring R] (ι : Type u_2) [Preorder ι] (G : ι → Type u_3) [(i : ι) → AddCommMonoid (G i)] [(i : ι) → Module R (G i)] (f : (i j : ι) → i ≤ j → G i →ₗ[R] G j) [DecidableEq ι] {P : Type u_4} [AddCommMonoid P] [Module R P] (g : (i : ι) → G i →ₗ[R] P) (Hg : ∀ (i j : ι) (hij : i ≤ j) (x : G i), (g j) ((f i j hij) x) = (g i) x) : Module.DirectLimit G f →ₗ[R] P`

- `R` is the commutative semiring of scalars.
- `ι` is the index type, carrying a preorder that describes the directed system's shape.
- `G` is the family of modules, one for each index `i : ι`.
- `f` is the transition data: for each pair `i ≤ j`, a linear map `G i →ₗ[R] G j`.
- `P` is the target `R`-module into which we map.
- `g` is the compatible family of linear maps from each `G i` into `P`.
- `Hg` is the coherence/commutativity condition asserting that `g j (f i j hij x) = g i x` for all `i ≤ j` and `x : G i`, i.e., the family `g` respects the transition maps.

### Conventions

No junk-value conventions are declared: every input satisfying the stated type constraints yields a well-defined linear map out of the direct limit, and no special fallback value is assigned at any degenerate input.

### Worked examples

- Claim: When all transition maps are zero and `g i = 0` for all `i`, `VTask.lift` produces the zero map from `Module.DirectLimit G f` to `P`.

- Claim: The composite of `VTask.lift R ι G f g Hg` with the canonical inclusion `Module.DirectLimit.of R ι G f i : G i →ₗ[R] Module.DirectLimit G f` equals `g i` for each index `i`. That is, `(VTask.lift R ι G f g Hg).comp (Module.DirectLimit.of R ι G f i) = g i`.

- Claim: When each `g i` is `Module.DirectLimit.of R ι G f i`, and `Hg` is witnessed by the directed system axioms, `VTask.lift` returns the identity on `Module.DirectLimit G f`. Formally, `VTask.lift R ι G f (Module.DirectLimit.of R ι G f) (fun i j hij x => by simp) = LinearMap.id`.

- Claim: `VTask.lift` is surjective onto the class of linear maps out of the direct limit: for any `F : Module.DirectLimit G f →ₗ[R] P`, one has `VTask.lift R ι G f (fun i => F.comp (Module.DirectLimit.of R ι G f i)) (fun i j hij x => by simp) = F`.

### Boundaries

- If `ι` is empty (has no elements), the direct limit is the zero module, and `VTask.lift` necessarily produces the zero map regardless of `g` (which has no components to specify).
- If only a single index `i₀` exists, the direct limit is isomorphic to `G i₀`, and `VTask.lift` is simply `g i₀` (up to that isomorphism).
- The `DecidableEq ι` instance is required for the construction to be computable/definitional; without it the map still exists mathematically but the Lean definition needs it for implementation.
- If `P` is the zero module, then `VTask.lift` always yields the zero map regardless of `g`.
- The map produced is `R`-linear by construction; in particular it respects both addition and scalar multiplication.
- Under a `IsDirectedOrder ι` assumption and when all `g i` are injective, `VTask.lift` is itself injective.

### Not to be confused with

- `Module.DirectLimit.of`: the canonical linear map *into* the direct limit from a single component `G i`, going in the opposite direction from `VTask.lift`.
- `Module.DirectLimit` (the type itself): `VTask.lift` constructs a map *out of* this type, not the type itself.
- `DirectSum.toModule`: the analogous universal map for direct sums (coproducts), which does not impose any compatibility condition between components; `VTask.lift` is the colimit version that does quotient by the transition-map relations.