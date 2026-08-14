## VTask.dlookup

### Object

`VTask.dlookup a l` performs a *dependent* key lookup in a list of dependent pairs (sigma types). Given a key `a` of type `α` and a list whose elements are pairs `⟨a', b⟩` where each `b` lives in the fiber `β a'`, it returns the *first* value whose key equals `a`, wrapped in `some`, cast to the correct fiber type `β a`. If no entry with key `a` exists, it returns `none`. The result type `Option (β a)` is itself dependent on the key, which distinguishes this from a plain `lookup` on homogeneous lists.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dlookup : {α : Type u} -> {β : α → Type v} -> [DecidableEq α] -> (a : α) -> List (Sigma β) → Option (β a)
<!-- PINNED-SIGNATURE:END -->


The universe-polymorphic type variables `α` (type `u`) and `β` (a family over `α`, type `v`) are inferred. The `DecidableEq α` instance provides the decidable equality needed to compare keys. The explicit argument `a : α` is the key being searched for. The final argument is the list of sigma-typed pairs to search through.

### Conventions

No special junk-value or edge conventions beyond standard `Option` usage are declared: when the list is empty or contains no matching key, the return value is `none`, which is the natural total-function behaviour and requires no extra convention.

### Worked examples

- Claim: `VTask.dlookup 'b' [⟨'a', 1⟩, ⟨'b', 2⟩, ⟨'b', 3⟩]` evaluates to `some 2` (first match wins).

- Claim: `VTask.dlookup 'z' [⟨'a', 1⟩, ⟨'b', 2⟩]` evaluates to `none` (key absent).

- Claim: For any key `a` and any value `b : β a`, looking up `a` in the singleton list `[⟨a, b⟩]` yields `some b`; this is the content of `dlookup_cons_eq`.

- Claim: Looking up any key in the empty list always yields `none`; this is the content of `dlookup_nil`.

### Boundaries

- **Empty list**: `VTask.dlookup a []` is definitionally `none` for every `a`.
- **First match wins**: When multiple entries share the same key, only the value associated with the *first* such entry is returned; later duplicates are ignored.
- **No-key case**: `VTask.dlookup a l = none` if and only if `a` is not a member of `l.keys`.
- **Presence indicator**: `(VTask.dlookup a l).isSome` holds exactly when `a ∈ l.keys`.
- **Key-erasure interaction**: After erasing all entries for key `a` from a `NodupKeys` list, looking up `a` again yields `none`.
- **Key-insert interaction**: After inserting `⟨a, b⟩` via `kinsert`, looking up `a` yields `some b`.
- **Dedup invariance**: `VTask.dlookup a (dedupKeys l) = VTask.dlookup a l`; deduplication does not change lookup results.

### Not to be confused with

- `List.lookup` — the non-dependent analogue for homogeneous `List (α × β)`, where the value type is a fixed `β` rather than a family `β a`.
- `List.find?` — searches for the first element satisfying a predicate and returns the whole element, not just a projected fiber value.
- `List.kextract` — simultaneously returns both the looked-up value and the list with that key erased, rather than the value alone.
