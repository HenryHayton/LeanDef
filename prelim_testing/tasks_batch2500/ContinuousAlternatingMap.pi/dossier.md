## Object

`VTask.pi` constructs a single continuous alternating map into a product (pi) type from a family of continuous alternating maps that share the same domain module. Given maps `f i : M [⋀^ι]→L[R] M' i` for each index `i : ι'`, it produces a continuous alternating map `M [⋀^ι]→L[R] (∀ i, M' i)` whose `j`-th component, when evaluated on a tuple `m : ι → M`, is exactly `f j m`. In other words, it is the canonical "diagonal" or "product" construction familiar from linear algebra: turn a family of maps into a single map targeting the product space.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {R : Type u_1} -> {M : Type u_2} -> {ι : Type u_6} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> [TopologicalSpace M] -> {ι' : Type u_7} -> {M' : ι' → Type u_8} -> [(i : ι') → AddCommMonoid (M' i)] -> [(i : ι') → TopologicalSpace (M' i)] -> [(i : ι') → Module R (M' i)] -> (f : (i : ι') → M [⋀^ι]→L[R] M' i) -> M [⋀^ι]→L[R] ((i : ι') → M' i)
<!-- PINNED-SIGNATURE:END -->


VTask.pi : {R : Type u_1} -> {M : Type u_2} -> {ι : Type u_6} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> [TopologicalSpace M] -> {ι' : Type u_7} -> {M' : ι' → Type u_8} -> [(i : ι') → AddCommMonoid (M' i)] -> [(i : ι') → TopologicalSpace (M' i)] -> [(i : ι') → Module R (M' i)] -> (f : (i : ι') → M [⋀^ι]→L[R] M' i) -> M [⋀^ι]→L[R] ((i : ι') → M' i)

`R` is the scalar semiring shared by all maps. `M` is the common source module, a topological `R`-module whose elements are assembled into tuples of type `ι → M` as inputs. `ι` is the index type for those input tuples (the "arity" index of the alternating map). `ι'` is the index type parametrising the family of target modules. `M' i` is the target module corresponding to index `i : ι'`, each carrying its own additive, scalar, and topological structure (supplied by the three instance families). `f` is the family of continuous alternating maps to be combined: `f i` maps `ι`-tuples from `M` into `M' i`.

## Conventions

There are no special junk-value or boundary conventions declared for this construction: the definition is genuinely total and well-defined for any family `f`, including the empty family (when `ι'` is empty), in which case the result targets the unit/trivial product type.

## Worked examples

- Claim: Evaluating `VTask.pi f` at a tuple `m` and then projecting to index `j` gives `f j m` — formally, `(VTask.pi f) m j = f j m` for all `m` and `j`.

- Claim: When `ι'` has two elements and `f` consists of two continuous alternating maps `g` and `h`, then `VTask.pi (fun i => if i = 0 then g else h)` evaluated at `m` yields the pair `(g m, h m)` in the product.

- Claim: In the normed setting (where `‖·‖` is available on each `M' i` and `ι'` is a `Fintype`), the operator norm satisfies `‖VTask.pi f‖ = ‖f‖`, reflecting that the combined map is no "larger" than the family taken together.

## Boundaries

- **Empty index family (`ι'` empty):** The construction is still valid; the resulting map takes values in the trivially empty product type `∀ i : Empty, M' i`, which is a one-element type. The map sends every input to the unique element.
- **Empty arity (`ι` empty or a singleton):** The alternating condition is vacuous for arities 0 or 1, so `VTask.pi` still produces a valid (trivially alternating) continuous multilinear map; nothing special happens.
- **Single-element `ι'`:** The result is essentially isomorphic to the sole map `f` in the family; the pi construction introduces a trivial product wrapper.

## Not to be confused with

- `ContinuousMultilinearMap.pi`: The analogous construction for continuous multilinear maps that do **not** enforce the alternating (vanishing on repeated inputs) condition.
- `AlternatingMap.pi`: The purely algebraic (non-topological) pi construction for alternating maps, which ignores continuity.
- `ContinuousLinearMap.pi`: The pi construction for **linear** (not multilinear) continuous maps; same component-wise idea but for maps of arity 1.