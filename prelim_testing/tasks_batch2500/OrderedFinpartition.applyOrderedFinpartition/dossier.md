## VTask.applyOrderedFinpartition

### Object

Given an ordered finite partition `c` of the integer `n` into consecutive blocks, and a family `p` of continuous multilinear maps (one for each block, taking as many inputs as that block's size), `VTask.applyOrderedFinpartition c p` produces a function that:
1. Accepts a vector `v : Fin n → E` of `n` inputs from a normed space `E`.
2. Returns, for each block index `i : Fin c.length`, the value obtained by (a) selecting the coordinates of `v` that belong to the `i`-th block via the block's canonical embedding `c.emb i`, and (b) applying the continuous multilinear map `p i` to those selected coordinates.

In short, it "evaluates each block's multilinear map on the corresponding slice of the input vector," producing one output in `F` per block of the partition.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.applyOrderedFinpartition : {𝕜 : Type u_1} -> [NontriviallyNormedField 𝕜] -> {E : Type u_2} -> [NormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> {F : Type u_3} -> [NormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> {n : ℕ} -> (c : OrderedFinpartition n) -> (p : (i : Fin c.length) → E [×c.partSize i]→L[𝕜] F) -> (Fin n → E) → Fin c.length → F
<!-- PINNED-SIGNATURE:END -->


The type string is inserted automatically above. The arguments are:
- `𝕜`: the scalar field, required to be a nontrivially normed field.
- `E`: the input normed space over `𝕜`.
- `F`: the output normed space over `𝕜`.
- `n`: the total number of input variables being partitioned.
- `c : OrderedFinpartition n`: an ordered partition of `{0, …, n-1}` into `c.length` consecutive blocks, each of size `c.partSize i`.
- `p`: a dependent family of continuous multilinear maps — for each block index `i : Fin c.length`, the map `p i` takes `c.partSize i` inputs from `E` and produces an output in `F`.
- The remaining two arguments (not bound in the definition's name but present in the return type) are: a vector `v : Fin n → E` providing all `n` inputs, and a block index `m : Fin c.length` selecting which block's output to compute.

### Conventions

No special junk-value or boundary conventions are declared: the definition is total and well-typed for every valid combination of inputs without any special out-of-range sentinels.

### Worked examples

- Claim: For the trivial ordered partition of `n = 1` into a single block of size 1, `VTask.applyOrderedFinpartition c p v ⟨0, by omega⟩` equals `p ⟨0, by omega⟩ (v ∘ c.emb ⟨0, by omega⟩)` — i.e., the unique multilinear map is applied to the single-element slice of `v`.

- Claim: For a partition of `n = 3` into two blocks of sizes 2 and 1 (so `c.length = 2`), evaluating at block index `⟨0, _⟩` returns `p ⟨0, _⟩` applied to the first two components of `v`, while evaluating at block index `⟨1, _⟩` returns `p ⟨1, _⟩` applied to the third component of `v`; the two outputs are independent of each other.

- Claim: If all maps `p i` are the zero multilinear map, then `VTask.applyOrderedFinpartition c p v m = 0` for every `v` and every `m`.

- Claim: The function `VTask.applyOrderedFinpartition c p v` is determined entirely by the slices `v ∘ c.emb i` for each block `i`; changing coordinates of `v` that lie in block `j` does not affect the output at block `i ≠ j`.

### Boundaries

- When `c.length = 0` (empty partition, `n = 0`), the family `p` is empty, and the output function `Fin 0 → F` is vacuously defined — there are no blocks to evaluate.
- When a block has size `0` (an empty block), the corresponding multilinear map `p i` takes zero arguments; it is evaluated on the empty tuple, returning a fixed element of `F` regardless of `v`.
- The function is not expected to be continuous or multilinear in `v` as a whole; each component output `m ↦ p m (v ∘ c.emb m)` is multilinear only in the coordinates of `v` belonging to block `m`.

### Not to be confused with

- `FormalMultilinearSeries.applyComposition`: applies a composition structure to a formal multilinear series, combining block outputs into a single multilinear evaluation rather than returning a block-indexed family.
- `OrderedFinpartition.emb`: just the embedding of a single block's indices into `Fin n`, without applying any multilinear map.
- `ContinuousMultilinearMap.compContinuousLinearMap`: composes a multilinear map with linear maps on each argument slot, which is a different kind of substitution than selecting a slice of a shared input vector.