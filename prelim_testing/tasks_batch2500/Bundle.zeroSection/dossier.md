## VTask.zeroSection

### Object

The zero section of a (vector) bundle is the canonical map that sends each point of the base space to the zero element in the fiber over that point. Concretely, it produces a section of the total space by pairing every base point `b : B` with the distinguished zero element `0 : E b`, yielding an element of the total space `TotalSpace F E`. The image of this map is the "zero section" of the bundle, a copy of the base space sitting inside the total space with each fiber coordinate equal to zero.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.zeroSection : {B : Type u_2} -> (F : Type u_3) -> (E : B → Type u_4) -> [(x : B) → Zero (E x)] -> B → Bundle.TotalSpace F E
<!-- PINNED-SIGNATURE:END -->


`VTask.zeroSection : {B : Type u_2} -> (F : Type u_3) -> (E : B → Type u_4) -> [(x : B) → Zero (E x)] -> B → Bundle.TotalSpace F E`

The implicit argument `B` is the base type (the parameter space). The explicit argument `F` is the fiber type index (a phantom type used to identify which bundle structure is in play; it appears in `TotalSpace` but does not directly determine the fibers). The explicit argument `E` is the family of fiber types, a function assigning to each base point `b : B` a type `E b`. The instance argument `[(x : B) → Zero (E x)]` provides, for every base point, a zero element in the corresponding fiber. The final argument is the base point `b : B` at which the zero section is evaluated.

### Conventions

There are no junk-value or edge-case conventions declared for this definition: the map is total and well-defined for every base point whenever the required `Zero` instances exist, so no special conventions are needed.

### Worked examples

- Claim: Applying `VTask.zeroSection` to the base point `(0 : Fin 3)` in the trivial bundle `Fin 3 → ℝ` (with `F = ℝ`) yields the total-space element `⟨0, 0⟩` (base point 0, fiber value 0).

- Claim: For the product bundle over `Bool` with fibers `ℝ`, the zero section sends `true` to `⟨true, 0⟩` and `false` to `⟨false, 0⟩`.

- Claim: The zero section is injective: if `VTask.zeroSection F E b₁ = VTask.zeroSection F E b₂`, then `b₁ = b₂`, because the base point is stored unmodified in the first component of the total-space pair.

### Boundaries

- When `B` is empty (an uninhabited type), the zero section is vacuously a function on an empty domain and its image is empty; this is consistent and raises no issues.
- When all fibers `E b` are the trivial (unit) type with a trivial `Zero` instance, the zero section still produces well-typed total-space elements; the zero element is just the unique term of that type.
- The phantom type `F` does not affect which fiber element is chosen; it only tags the total space for disambiguation purposes.

### Not to be confused with

- `Bundle.TotalSpace` itself — that is the type of the total space; the zero section is a *map into* it, not the space itself.
- A general section of the bundle — the zero section is the *specific* section that always picks the zero fiber element; a general section may pick any element in each fiber.
- The zero morphism in an abelian-group bundle — while related in spirit, the zero section is a set-theoretic map from the base; continuity or linearity properties require additional structure and are separate lemmas.
