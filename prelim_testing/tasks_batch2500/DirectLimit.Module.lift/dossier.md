## VTask.lift

### Object

`VTask.lift` constructs the canonical linear map out of the direct limit of a directed system of modules. Given a directed system of `R`-modules `G i` connected by transition maps `f i j hij : G i →ₗ[R] G j`, and a target `R`-module `P` equipped with a compatible family of linear maps `g i : G i →ₗ[R] P` (compatible meaning `g j ∘ f i j hij = g i` for all `i ≤ j`), there exists a unique linear map `DirectLimit G f →ₗ[R] P` making every triangle commute. `VTask.lift` produces this universal map.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : (R : Type u_1) -> (ι : Type u_2) -> [Preorder ι] -> (G : ι → Type u_3) -> {T : ⦃i j : ι⦄ → i ≤ j → Type u_6} -> (f : (x x_1 : ι) → (h : x ≤ x_1) → T h) -> [(i j : ι) → (h : i ≤ j) → FunLike (T h) (G i) (G j)] -> [DirectedSystem G fun x1 x2 x3 => ⇑(f x1 x2 x3)] -> [IsDirectedOrder ι] -> [Semiring R] -> [(i : ι) → AddCommMonoid (G i)] -> [(i : ι) → Module R (G i)] -> [∀ (i j : ι) (h : i ≤ j), LinearMapClass (T h) R (G i) (G j)] -> [Nonempty ι] -> {P : Type u_7} -> [AddCommMonoid P] -> [Module R P] -> (g : (i : ι) → G i →ₗ[R] P) -> (Hg : ∀ (i j : ι) (hij : i ≤ j) (x : G i), (g j) ((f i j hij) x) = (g i) x) -> DirectLimit G f →ₗ[R] P
<!-- PINNED-SIGNATURE:END -->


VTask.lift : (R : Type u_1) -> (ι : Type u_2) -> [Preorder ι] -> (G : ι → Type u_3) -> {T : ⦃i j : ι⦄ → i ≤ j → Type u_6} -> (f : (x x_1 : ι) → (h : x ≤ x_1) → T h) -> [(i j : ι) → (h : i ≤ j) → FunLike (T h) (G i) (G j)] -> [DirectedSystem G fun x1 x2 x3 => ⇑(f x1 x2 x3)] -> [IsDirectedOrder ι] -> [Semiring R] -> [(i : ι) → AddCommMonoid (G i)] -> [(i : ι) → Module R (G i)] -> [∀ (i j : ι) (h : i ≤ j), LinearMapClass (T h) R (G i) (G j)] -> [Nonempty ι] -> {P : Type u_7} -> [AddCommMonoid P] -> [Module R P] -> (g : (i : ι) → G i →ₗ[R] P) -> (Hg : ∀ (i j : ι) (hij : i ≤ j) (x : G i), (g j) ((f i j hij) x) = (g i) x) -> DirectLimit G f →ₗ[R] P

`R` is the commutative semiring of scalars shared by all modules in the system. `ι` is the directed index type ordered by the `Preorder` instance. `G` assigns to each index `i` the component module `G i`. `T` is a family of types for the transition morphisms, and `f` assigns to each pair `i ≤ j` a transition morphism of type `T h` from `G i` to `G j`. The `FunLike`, `DirectedSystem`, and `LinearMapClass` instances assert that these transition morphisms are indeed linear maps forming a directed system. `IsDirectedOrder ι` asserts that the index poset is directed. The `AddCommMonoid` and `Module` instances equip each `G i` with the required algebraic structure. `Nonempty ι` ensures the index set is non-empty. `P` is the target `R`-module. `g` is the compatible family of linear maps, one from each `G i` into `P`. `Hg` is the commutativity condition: for every `i ≤ j` and every element `x : G i`, applying the transition map first and then `g j` yields the same result as applying `g i` directly.

### Conventions

The constructed linear map is the unique linear map out of the direct limit satisfying the universal property triangle; no junk values arise because the compatibility hypothesis `Hg` is required as explicit input and the construction is well-defined on equivalence classes of the direct limit.

### Worked examples

- Claim: For a compatible family `g`, the composition of `VTask.lift R ι G f g Hg` with the canonical inclusion `of R ι G f i` equals `g i` as linear maps (the universal triangle commutes on each component).

- Claim: For a compatible family `g` and an element `x : G i`, evaluating `VTask.lift R ι G f g Hg` on the image of `x` under the canonical inclusion into the direct limit yields `g i x`.

- Claim: If two compatible families `g` and `g'` agree on every canonical inclusion (i.e., `g i = g' i` for all `i`), then the lifted maps `VTask.lift R ι G f g Hg` and `VTask.lift R ι G f g' Hg'` are equal.

### Boundaries

- The index type `ι` must be nonempty; this is enforced by the `Nonempty ι` instance. If the system were empty, there would be no canonical element and the construction would be ill-defined.
- When the directed system is trivially indexed by a single element, `VTask.lift` reduces essentially to `g` itself, since the direct limit over a one-element poset is isomorphic to `G` at that element.
- The compatibility condition `Hg` is an exact equality (not just equality up to some equivalence), so `VTask.lift` is only defined when the family `g` is strictly compatible with all transition maps.
- The map constructed by `VTask.lift` is `R`-linear by construction, preserving both addition and scalar multiplication.

### Not to be confused with

- `DirectLimit.Module.of`: the canonical *inclusion* linear map `G i →ₗ[R] DirectLimit G f` going *into* the direct limit, rather than out of it.
- The direct limit of rings or algebras (also called `DirectLimit`): a similar universal construction but in the category of rings or `R`-algebras, with a different compatibility condition and target.
- The inverse limit (projective limit): the dual construction, where compatible maps come *from* a target into the components rather than from components into a target.