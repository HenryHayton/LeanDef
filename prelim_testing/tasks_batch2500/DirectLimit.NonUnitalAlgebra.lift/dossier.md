## VTask.lift

### Object

Given a directed system of non-unital `R`-algebras `G i` indexed by a directed preorder `ι`, and a compatible family of non-unital `R`-algebra homomorphisms `g i : G i →ₙₐ[R] P` into a target non-unital `R`-algebra `P` (meaning each `g j ∘ f i j = g i`), `VTask.lift` produces the unique non-unital `R`-algebra homomorphism out of the direct limit `DirectLimit G f` into `P` whose restriction to each component `G i` (via the canonical inclusion) equals `g i`. This is precisely the universal property of the colimit (direct limit) in the category of non-unital `R`-algebras.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {R : Type u_1} -> {ι : Type u_2} -> [Preorder ι] -> (G : ι → Type u_3) -> {T : ⦃i j : ι⦄ → i ≤ j → Type u_6} -> (f : (x x_1 : ι) → (h : x ≤ x_1) → T h) -> [(i j : ι) → (h : i ≤ j) → FunLike (T h) (G i) (G j)] -> [DirectedSystem G fun x1 x2 x3 => ⇑(f x1 x2 x3)] -> [IsDirectedOrder ι] -> [CommSemiring R] -> [(i : ι) → NonUnitalNonAssocSemiring (G i)] -> [(i : ι) → DistribMulAction R (G i)] -> [∀ (i j : ι) (h : i ≤ j), NonUnitalAlgHomClass (T h) R (G i) (G j)] -> [Nonempty ι] -> (P : Type u_7) -> [NonUnitalNonAssocSemiring P] -> [DistribMulAction R P] -> (g : (i : ι) → G i →ₙₐ[R] P) -> (Hg : ∀ (i j : ι) (hij : i ≤ j) (x : G i), (g j) ((f i j hij) x) = (g i) x) -> DirectLimit G f →ₙₐ[R] P
<!-- PINNED-SIGNATURE:END -->


`VTask.lift : {R : Type u_1} -> {ι : Type u_2} -> [Preorder ι] -> (G : ι → Type u_3) -> {T : ⦃i j : ι⦄ → i ≤ j → Type u_6} -> (f : (x x_1 : ι) → (h : x ≤ x_1) → T h) -> [(i j : ι) → (h : i ≤ j) → FunLike (T h) (G i) (G j)] -> [DirectedSystem G fun x1 x2 x3 => ⇑(f x1 x2 x3)] -> [IsDirectedOrder ι] -> [CommSemiring R] -> [(i : ι) → NonUnitalNonAssocSemiring (G i)] -> [(i : ι) → DistribMulAction R (G i)] -> [∀ (i j : ι) (h : i ≤ j), NonUnitalAlgHomClass (T h) R (G i) (G j)] -> [Nonempty ι] -> (P : Type u_7) -> [NonUnitalNonAssocSemiring P] -> [DistribMulAction R P] -> (g : (i : ι) → G i →ₙₐ[R] P) -> (Hg : ∀ (i j : ι) (hij : i ≤ j) (x : G i), (g j) ((f i j hij) x) = (g i) x) -> DirectLimit G f →ₙₐ[R] P`

- `R` is the commutative semiring acting as the scalar ring for the algebra structures.
- `ι` is the indexing type, carrying a directed preorder that governs which indices are comparable.
- `G` is the functor assigning to each index `i` the non-unital `R`-algebra at that stage of the system.
- `T` and `f` together encode the transition morphisms: for each pair `i ≤ j`, `f i j h : T h` is the non-unital `R`-algebra homomorphism from `G i` to `G j`, making the system directed.
- `P` is the target non-unital `R`-algebra into which the lifted map will land.
- `g` is the compatible family of non-unital `R`-algebra homomorphisms, one `g i : G i →ₙₐ[R] P` for each index `i`.
- `Hg` is the commutativity (compatibility) condition asserting that the diagrams formed by the `g i` and the transition maps `f i j` commute: applying the transition map then `g j` is the same as applying `g i` directly.

### Conventions

There are no special junk-value or edge-case conventions for this definition: it is a total construction whose output is fully determined by its inputs, and the compatibility hypothesis `Hg` ensures the construction is well-defined on all equivalence classes in the direct limit.

### Worked examples

- Claim: For any compatible family `g` and element `x : G i`, the lifted map composed with the canonical inclusion `of G f i` evaluates to `g i x` — that is, `VTask.lift G f P g Hg (of G f i x) = g i x`.

- Claim: The composite non-unital `R`-algebra homomorphism `(VTask.lift G f P g Hg).comp (of G f i)` equals `g i` as a morphism — i.e., the lifted map restricted to each component recovers the original component map.

- Claim: When `ι` is a single-element directed order and `G` is constant at some algebra `A`, and `g` is the identity map on `A`, then `VTask.lift` produces the canonical isomorphism from the (trivial) direct limit back to `A`.

### Boundaries

- The definition requires the index type `ι` to be nonempty and directed; without these conditions the direct limit itself may be ill-formed or empty.
- Uniqueness: the universal property guarantees that `VTask.lift G f P g Hg` is the *unique* non-unital `R`-algebra homomorphism out of `DirectLimit G f` that restricts to `g i` on each component — any two such maps must agree.
- If `Hg` fails for some triple `i j hij x`, the construction cannot be applied (the type of `Hg` enforces the compatibility requirement at the type level).
- When `ι` has a maximum element `m`, the direct limit is isomorphic to `G m`, and `VTask.lift` simply reproduces `g m` (up to this isomorphism).

### Not to be confused with

- `DirectLimit.lift` (the underlying set-level or ring-level lift): the present definition packages the full non-unital `R`-algebra homomorphism structure, not merely a function or ring map.
- `VTask.of` (the canonical inclusion maps `G i → DirectLimit G f`): these go *into* the direct limit, whereas `VTask.lift` produces a map *out of* it.
- The unital algebra version `DirectLimit.lift` for `AlgHom`: the present definition works for non-unital `R`-algebras and produces a `NonUnitalAlgHom`, not a unital `AlgHom`.