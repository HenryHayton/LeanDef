## VTask.drop

### Object

`VTask.drop` is a projection function on multi-dimensional array indices. A `HolorIndex ds` is a tuple of non-negative integers, one per dimension, each bounded by the corresponding entry in the dimension list `ds`. Given a compound index that ranges over the concatenated dimension list `ds₁ ++ ds₂`, `VTask.drop` returns the trailing portion of that index — the sub-index that corresponds to the dimensions in `ds₂` alone — by discarding the first `|ds₁|` components.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.drop : {ds₂ ds₁ : List ℕ} -> HolorIndex (ds₁ ++ ds₂) → HolorIndex ds₂
<!-- PINNED-SIGNATURE:END -->


The implicit argument `ds₂` is the list of trailing dimensions whose index is to be extracted. The implicit argument `ds₁` is the list of leading dimensions whose components are dropped. The explicit argument is a `HolorIndex` over the concatenated dimension list `ds₁ ++ ds₂`; its first `|ds₁|` components belong to the leading block and are discarded, and the remaining `|ds₂|` components, which are within bounds for `ds₂`, form the result.

### Conventions

No special junk-value or boundary conventions are declared for this function: it is a total, type-safe projection. Every well-typed input produces a well-typed output, and no out-of-range or default behaviour is needed.

### Worked examples

- Claim: Dropping a prefix of length 0 from a `HolorIndex` over `[] ++ ds₂` returns the index unchanged (as a `HolorIndex ds₂`).

- Claim: For `ds₁ = [3]` and `ds₂ = [4, 2]`, applying `VTask.drop` to the compound index `⟨[1, 2, 0], _⟩ : HolorIndex ([3] ++ [4, 2])` yields the `HolorIndex [4, 2]` whose underlying list is `[2, 0]`.

- Claim: For `ds₁ = [2, 3]` and `ds₂ = [5]`, applying `VTask.drop` to the compound index `⟨[1, 2, 4], _⟩ : HolorIndex ([2, 3] ++ [5])` yields the `HolorIndex [5]` whose underlying list is `[4]`.

- Claim: When `ds₂ = []`, `VTask.drop` always produces the unique `HolorIndex []` (the empty index), regardless of the leading components.

### Boundaries

- When `ds₁ = []`, the concatenation `[] ++ ds₂` is definitionally `ds₂`, and `VTask.drop` acts as the identity: the input index is returned as-is (interpreted as a `HolorIndex ds₂`).
- When `ds₂ = []`, all components are dropped and the result is the unique empty `HolorIndex []`.
- The function is total: every `HolorIndex (ds₁ ++ ds₂)` has exactly `|ds₁| + |ds₂|` components all within their respective bounds, so the dropped tail is always a valid `HolorIndex ds₂`.

### Not to be confused with

- **`HolorIndex.take` (or a hypothetical `VTask.take`)** — the complementary operation that retains the first `|ds₁|` components instead of the last `|ds₂|`.
- **`List.drop`** — the underlying list operation that drops a prefix of any list; `VTask.drop` lifts this to bounded holor indices, preserving the within-bounds invariant.
- **`HolorIndex ds₂` constructed directly** — one might confuse this projection with simply ignoring the type and slicing an underlying list; `VTask.drop` ensures the result carries the correct `ds₂` bounds proof.
