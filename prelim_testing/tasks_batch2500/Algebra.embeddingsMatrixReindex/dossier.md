## VTask.embeddingsMatrixReindex

### Object

Given a family of elements `b : κ → B` and a bijection `e` from the index type `κ` to the set of all `A`-algebra homomorphisms from `B` to `C`, `embeddingsMatrixReindex A C b e` is the square matrix of size `κ × κ` with entries in `C` whose `(i, j)`-entry is `σⱼ(b(i))`, where `σⱼ` denotes the embedding `e(j) : B →ₐ[A] C`. In other words, row `i` records the images of `b(i)` under every embedding, and column `j` records the values of the embedding `e(j)` applied to each generator `b(i)`. This matrix appears naturally in algebraic number theory when computing discriminants and studying separability of field extensions, and is most useful when `A` and `B` are fields and `C` is algebraically closed.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.embeddingsMatrixReindex : {κ : Type w} -> (A : Type u) -> {B : Type v} -> (C : Type z) -> [CommRing A] -> [CommRing B] -> [Algebra A B] -> [CommRing C] -> [Algebra A C] -> (b : κ → B) -> (e : κ ≃ (B →ₐ[A] C)) -> Matrix κ κ C
<!-- PINNED-SIGNATURE:END -->


The first explicit argument `A` is the base commutative ring (the ground ring of the algebra structure). The second explicit argument `C` is the target commutative ring into which all embeddings land and whose elements populate the matrix entries. The implicit argument `κ` is the index type used both to index the family of generators and to label rows and columns of the resulting matrix. The implicit argument `B` is the intermediate commutative ring (an `A`-algebra from which embeddings depart). The argument `b : κ → B` is a family of elements of `B`, one for each index in `κ`; it provides the generators whose images fill the matrix. The argument `e : κ ≃ (B →ₐ[A] C)` is a bijection between the index type `κ` and the type of all `A`-algebra homomorphisms from `B` to `C`; it is used to identify column indices with embeddings.

### Conventions

The matrix is indexed on both rows and columns by `κ`: rows correspond to the index of the generator family `b`, and columns correspond to the index of the embedding via the equivalence `e`. The column index `j` selects the embedding `e(j)`, not `e.symm(j)`; the bijection `e` is applied forward when choosing which embedding labels column `j`. When `κ` is not a `Fintype`, the matrix still exists as a value of type `Matrix κ κ C` but computations such as determinant require finiteness. There are no junk values: the definition is total and well-defined for any types and instances satisfying the stated type-class assumptions.

### Worked examples

- Claim: For the trivial case where `κ = Unit`, `B = C = A` (the algebra maps are ring identity), and `b` is the constant family sending the unique element to `1 : A`, the single entry of `embeddingsMatrixReindex A A b e` is `1`, because every `A`-algebra map sends `1` to `1`.

- Claim: If `e` is an equivalence sending `j₀ : κ` to the identity embedding `AlgHom.id A B` (cast appropriately so `C = B`), then the `(i, j₀)`-entry of `embeddingsMatrixReindex A B b e` equals `b(i)`, the generator itself, since the identity embedding fixes every element.

- Claim: Changing the bijection `e` to `e'` by composing with a permutation `π : κ ≃ κ` on the right (i.e., `e' = e ∘ π`) permutes the columns of `embeddingsMatrixReindex A C b e` by `π`, leaving the row structure intact.

### Boundaries

When `κ` is empty, the resulting matrix is the unique `0 × 0` matrix over `C`, which is vacuously well-defined. When `b` is the zero map (sending every index to `0 : B`), every entry of the matrix is `0` since every `A`-algebra homomorphism preserves `0`. The equivalence `e` must be a genuine bijection; if `κ` has a different cardinality from the set of `A`-algebra homomorphisms `B →ₐ[A] C`, no such `e` can be constructed, so the definition simply cannot be applied. The type-class assumptions (both rings commutative, both algebra structures present) are required for the embeddings to be `A`-algebra homomorphisms in the first place.

### Not to be confused with

- `embeddingsMatrix A C b`: the version without reindexing, whose columns are indexed directly by the type `B →ₐ[A] C` rather than by `κ` via an equivalence.
- `Matrix.reindex`: the purely combinatorial operation of relabelling rows and columns of a matrix by equivalences, with no algebraic meaning attached to the new indices.
- The Vandermonde matrix: a superficially similar polynomial-evaluation matrix, but constructed from powers of elements rather than algebra-homomorphism images.