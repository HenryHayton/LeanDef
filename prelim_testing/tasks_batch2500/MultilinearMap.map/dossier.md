## VTask.map

### Object

Given a multilinear map `f : M₁ → M₂` (indexed by `ι`) and a family of submodules `p i ⊆ M₁ i`, `VTask.map f p` is the **pushforward** of the family `(p i)` through `f`. Its underlying set is the image of `f` restricted to those tuples `v` with `v i ∈ p i` for every index `i`. The result carries the structure of a `SubMulAction`: it is closed under scalar multiplication by `R`, but it is **not** a submodule because it is not necessarily closed under addition.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {R : Type uR} -> {ι : Type uι} -> {M₁ : ι → Type v₁} -> {M₂ : Type v₂} -> [Ring R] -> [(i : ι) → AddCommMonoid (M₁ i)] -> [AddCommMonoid M₂] -> [(i : ι) → Module R (M₁ i)] -> [Module R M₂] -> [Nonempty ι] -> (f : MultilinearMap R M₁ M₂) -> (p : (i : ι) → Submodule R (M₁ i)) -> SubMulAction R M₂
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {R : Type uR} -> {ι : Type uι} -> {M₁ : ι → Type v₁} -> {M₂ : Type v₂} -> [Ring R] -> [(i : ι) → AddCommMonoid (M₁ i)] -> [AddCommMonoid M₂] -> [(i : ι) → Module R (M₁ i)] -> [Module R M₂] -> [Nonempty ι] -> (f : MultilinearMap R M₁ M₂) -> (p : (i : ι) → Submodule R (M₁ i)) -> SubMulAction R M₂`

The implicit arguments `R`, `ι`, `M₁`, `M₂` are, respectively, the coefficient ring, the indexing type, the family of domain modules, and the codomain module. The typeclass instances supply the ring/module structure on all relevant types. The `Nonempty ι` instance ensures the index set is non-empty (required for the scalar-closure argument). The explicit argument `f` is the multilinear map whose values form the underlying set, and `p` is the family of submodules — one submodule of each `M₁ i` — through which `f` is restricted.

### Conventions

The `Nonempty ι` hypothesis is required; the construction does not make sense (and scalar-closure cannot be proved in general) for an empty index type, so there is no junk-value behavior to declare for that parameter. No other special edge-case conventions are declared for this definition.

### Worked examples

- Claim: If every submodule `p i` is the zero submodule of `M₁ i`, then `VTask.map f p` contains exactly the single element `0 ∈ M₂` (since the only tuple with all entries in `⊥` is the zero tuple, and multilinear maps send it to `0`).

- Claim: If every `p i` equals the whole module `M₁ i`, then the carrier of `VTask.map f p` equals the image of `f` over all of `∏ i, M₁ i`, i.e., the full range of `f`.

- Claim: For any `f` and `p`, the set underlying `VTask.map f p` is non-empty (it always contains at least `f 0 = 0`, since zero belongs to every submodule).

- Claim: If `y` belongs to `VTask.map f p` and `c : R`, then `c • y` also belongs to `VTask.map f p` (scalar-closure, the defining property of `SubMulAction`).

### Boundaries

- **Nonemptiness of carrier**: The carrier is always non-empty when `ι` is non-empty; the zero vector lies in every submodule, so `f 0` (which equals `0`) is always a member.
- **Not closed under addition**: The pushforward is explicitly noted not to be a submodule. Two elements of the carrier may sum to something outside it, so no additive closure is guaranteed.
- **`Nonempty ι` is required**: The scalar-closure proof picks an index from `ι`; without `Nonempty ι` the construction would be ill-defined.
- **Smallest and largest cases**: When all `p i = ⊥` the carrier is `{0}`; when all `p i = ⊤` the carrier is the full image (range) of `f`.
- **Scalar multiple witness**: Scalar closure is established by updating a single coordinate of the preimage tuple by the scalar, exploiting multilinearity in that coordinate.

### Not to be confused with

- `MultilinearMap.range` — the image of the entire multilinear map (no submodule restriction), which is the special case where all `p i = ⊤`.
- `Submodule.map` for linear maps — the analogous pushforward for a *linear* (single-argument) map, which *does* produce a `Submodule` (closed under both addition and scalar multiplication).
- `MultilinearMap.domRestrict` — restricts the *domain* of a multilinear map to a family of submodules, yielding a new multilinear map rather than a sub-object of the codomain.
