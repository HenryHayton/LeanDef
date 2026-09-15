## Object

`VTask.of` is the canonical non-unital `R`-algebra homomorphism that embeds a single component `G i` into the direct limit of the directed system `(G, f)`. Concretely, an element `x : G i` is sent to the equivalence class of the pair `(i, x)` in the direct limit, which is the standard construction that identifies elements from different components whenever they eventually agree under the transition maps.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.of : {R : Type u_1} -> {ι : Type u_2} -> [Preorder ι] -> (G : ι → Type u_3) -> {T : ⦃i j : ι⦄ → i ≤ j → Type u_6} -> (f : (x x_1 : ι) → (h : x ≤ x_1) → T h) -> [(i j : ι) → (h : i ≤ j) → FunLike (T h) (G i) (G j)] -> [DirectedSystem G fun x1 x2 x3 => ⇑(f x1 x2 x3)] -> [IsDirectedOrder ι] -> [CommSemiring R] -> [(i : ι) → NonUnitalNonAssocSemiring (G i)] -> [(i : ι) → DistribMulAction R (G i)] -> [∀ (i j : ι) (h : i ≤ j), NonUnitalAlgHomClass (T h) R (G i) (G j)] -> [Nonempty ι] -> (i : ι) -> G i →ₙₐ[R] DirectLimit G f
<!-- PINNED-SIGNATURE:END -->


The first implicit argument `R` is the commutative semiring of scalars. The implicit argument `ι` is the index type, equipped with a preorder. The argument `G` is the directed system of non-unital semirings indexed by `ι`; each `G i` is the component at index `i`. The argument `T` captures the type family of transition morphisms between components (parameterised by the inequality proof `i ≤ j`). The argument `f` assigns to each pair of indices `x ≤ x₁` a morphism of type `T h`; these are the transition maps that must be compatible with the directed system structure. The remaining implicit/instance arguments assert that the `T h` values are `FunLike`-morphisms from `G i` to `G j`, that the system is a `DirectedSystem`, that `ι` is a directed order, that each `G i` carries the required semiring and scalar-action structures, that each transition map is a non-unital algebra homomorphism class, and that `ι` is non-empty. The explicit argument `i : ι` is the index of the component being embedded. The map returns a non-unital `R`-algebra homomorphism `G i →ₙₐ[R] DirectLimit G f`.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total construction producing a morphism, and its behaviour is uniform across all valid inputs with no degenerate output regime.

## Worked examples

- Claim: For any element `x : G i`, `VTask.of G f i x` equals the equivalence class of the pair `(i, x)` in `DirectLimit G f`.

- Claim: `VTask.of G f i` is a non-unital `R`-algebra homomorphism, so it respects addition: for any `x y : G i`, `VTask.of G f i (x + y) = VTask.of G f i x + VTask.of G f i y`.

- Claim: The embedding is compatible with scalar multiplication: for any `r : R` and `x : G i`, `VTask.of G f i (r • x) = r • VTask.of G f i x`.

- Claim: The canonical maps are compatible with the transition maps: for `i ≤ j` and `x : G i`, `VTask.of G f j (f i j h x) = VTask.of G f i x` in `DirectLimit G f`.

## Boundaries

- The definition is valid for any index `i` in `ι`, including minimal elements; there is no special behaviour at extremal indices.
- When `ι` has a single element (say `i₀`), `VTask.of G f i₀` still provides a well-formed non-unital algebra homomorphism into the direct limit, which in that degenerate case is isomorphic to `G i₀` itself.
- The map is in general not injective unless the directed system's transition maps are injective (i.e., unless the directed system is injective in the appropriate sense).
- Even when `i` is not comparable with some other index `j`, the element `VTask.of G f i x` still lives in the colimit and can be compared with elements from `G j` there, because the directedness of `ι` guarantees a common upper bound.

## Not to be confused with

- `DirectLimit.of` for unital algebra homomorphisms or ring homomorphisms: the present `VTask.of` targets `NonUnitalAlgHom` (`→ₙₐ[R]`), not the unital variant `→ₐ[R]`.
- The transition map `f i j h : T h` itself: `VTask.of G f i` maps `G i` into the colimit, whereas `f i j h` maps `G i` into another component `G j`.
- A section or splitting of the quotient map: `VTask.of G f i` is not a right inverse to any projection out of the direct limit; it is an injection into the colimit (modulo the equivalence relation).