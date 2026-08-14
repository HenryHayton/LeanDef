## Object

`VTask.sigma s t` constructs a multiset of dependent pairs `⟨a, b⟩` (elements of the sigma type `(a : α) × σ a`) by ranging `a` over the multiset `s` and, for each such `a`, ranging `b` over the multiset `t a`. It is the dependent-type generalisation of the Cartesian product of two multisets: every pair `⟨a, b⟩` appears in the result with multiplicity equal to the product of the multiplicity of `a` in `s` and the multiplicity of `b` in `t a`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sigma : {α : Type u_1} -> {σ : α → Type u_4} -> (s : Multiset α) -> (t : (a : α) → Multiset (σ a)) -> Multiset ((a : α) × σ a)
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {σ : α → Type u_4} -> (s : Multiset α) -> (t : (a : α) → Multiset (σ a)) -> Multiset ((a : α) × σ a)`

The implicit type `α` is the index type. The implicit `σ` is a type family over `α`, specifying the fibre type at each index. The argument `s` is the multiset of indices being iterated over. The argument `t` is a function assigning, to each index `a : α`, the multiset of fibre values at `a` to be paired with it.

## Conventions

There are no junk-value conventions to declare for this definition: `VTask.sigma` is a total function defined for all multisets `s` and all fibre families `t`, including empty multisets and the zero family, with no special out-of-domain assignments needed.

## Worked examples

- Claim: `VTask.sigma (0 : Multiset ℕ) (fun a => ({a} : Multiset ℕ)) = 0`
  (The sigma of the empty multiset with any family is the empty multiset.)

- Claim: `VTask.sigma ({(0 : ℕ)} : Multiset ℕ) (fun a => (0 : Multiset ℕ)) = 0`
  (If the fibre at every index is empty, the result is the empty multiset regardless of `s`.)

- Claim: For `s = {a}` and `t a = {b}`, `VTask.sigma s t = {⟨a, b⟩}`. That is, the sigma of two singleton multisets is a singleton multiset containing the single dependent pair.

- Claim: `card (VTask.sigma s t) = Multiset.sum (Multiset.map (fun a => Multiset.card (t a)) s)`. The cardinality of the sigma multiset equals the sum over all elements `a` of `s` of the cardinality of `t a` (counting `a` with its multiplicity in `s`).

- Claim: `VTask.sigma (s + t_idx) u = VTask.sigma s u + VTask.sigma t_idx u` for multisets `s`, `t_idx` over `α` and a fibre family `u`. The construction distributes over addition in the first argument.

## Boundaries

- When `s = 0` (the empty multiset), `VTask.sigma s t = 0` for any `t`; there are no indices to iterate over.
- When `t a = 0` for every `a`, `VTask.sigma s t = 0` for any `s`; no pairs can be formed.
- Multiplicity is respected: if `a` appears `k` times in `s` and `b` appears `m` times in `t a`, then `⟨a, b⟩` appears `k * m` times in `VTask.sigma s t`.
- If both `s` and all `t a` are duplicate-free (satisfy `Nodup`), then `VTask.sigma s t` is also duplicate-free.
- The sigma distributes over addition in both arguments: adding two index multisets or two fibre multisets corresponds to union (addition) of the resulting sigma multisets.

## Not to be confused with

- `Multiset.product`: the non-dependent Cartesian product of two multisets, producing pairs in `α × β` rather than dependent pairs in `(a : α) × σ a`.
- `Finset.sigma`: the analogous construction for finite sets (no duplicate tracking) rather than multisets.
- `List.sigma`: the list-level version, which produces an ordered list of dependent pairs and distinguishes positional duplicates.
