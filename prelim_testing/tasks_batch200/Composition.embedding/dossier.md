## Object

Given a composition `c` of a natural number `n` — that is, an ordered list of positive integers that sum to `n` — and an index `i` pointing to one of its blocks, `VTask.embedding c i` is the order-preserving injection that identifies the `i`-th block (whose size is `c.blocksFun i`) with the corresponding contiguous sub-interval of `{0, 1, …, n-1}`. Concretely, the element at position `j` inside the block is sent to the global position `c.sizeUpTo i + j`, where `c.sizeUpTo i` is the sum of all block sizes strictly before block `i`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.embedding : {n : ℕ} -> (c : Composition n) -> (i : Fin c.length) -> Fin (c.blocksFun i) ↪o Fin n
<!-- PINNED-SIGNATURE:END -->


`VTask.embedding : {n : ℕ} -> (c : Composition n) -> (i : Fin c.length) -> Fin (c.blocksFun i) ↪o Fin n`

The implicit argument `n` is the total being composed. The argument `c` is the composition of `n`, encoding the ordered list of block sizes. The argument `i` is a valid index into the list of blocks (a finite natural number bounded by the number of blocks `c.length`). The result is an order-embedding from the finite set of size equal to the `i`-th block's length into the finite set `Fin n`.

## Conventions

There are no junk-value conventions to declare: every argument is intrinsically bounded by its type (`i` must be a valid block index, `j` must lie within the block), so the function is always well-typed and total within those constraints.

## Worked examples

- Claim: For the single-block composition of `n` (which has exactly one block of size `n`), the unique embedding (at block index `0`) sends every `i : Fin n` to itself.

- Claim: The coercion to `ℕ` of `VTask.embedding c i j` equals `c.sizeUpTo i + j` for any composition `c`, block index `i`, and position `j` within that block.

- Claim: The ranges of `VTask.embedding c i₁` and `VTask.embedding c i₂` are disjoint whenever `i₁ ≠ i₂`.

- Claim: Every element `j : Fin n` belongs to the range of `VTask.embedding c (c.index j)`, meaning the embeddings together cover all of `Fin n`.

- Claim: For the `ones n` composition (each block has size 1), the embedding at block `i` sends the unique element `⟨0, _⟩` to `⟨i, _⟩`.

## Boundaries

- When `n = 0`, the only composition is the empty composition with no blocks, so `c.length = 0` and `i : Fin 0` is vacuous; the embedding is never actually instantiated.
- When a block has size 1 (as in the `ones` composition), the embedding's domain is `Fin 1`, and the single element maps to the starting offset of that block.
- When the composition has exactly one block (the `single` composition), the single embedding is essentially the identity on `Fin n`.
- The offset `c.sizeUpTo i` ensures blocks are placed back-to-back with no gaps and no overlaps; disjointness of ranges is a theorem, not an accident.

## Not to be confused with

- `Composition.invEmbedding`: goes in the opposite direction — given a global index `j : Fin n`, it returns the local position within the block that contains `j`.
- `Composition.index`: also associated to a global index `j`, this gives the block number that contains `j`, not an embedding of the block into `Fin n`.
- `Fin.natAddOrderEmb`: a general order-embedding on finite sets defined by adding a fixed offset, which is a component used internally but is not block-aware.
