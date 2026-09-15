## VTask.mixedEmbeddingsOver

### Object

Given a base field `K`, an extension field `L`, and a fixed ring homomorphism `ψ : K →+* ℂ` (a complex embedding of `K`), this is the set of all ring homomorphisms `φ : L →+* ℂ` (complex embeddings of `L`) that simultaneously (1) extend `ψ`, meaning the restriction of `φ` to `K` agrees with `ψ`, and (2) are *mixed* in the sense that `φ` is neither a real embedding nor the conjugate of a real embedding — i.e., `φ` is a non-real complex embedding that is not identified with its own complex conjugate when considered as an embedding of `L` over `K`.

Intuitively, it is the fiber of the mixed (non-real, not self-conjugate) embeddings of `L` into `ℂ` lying above a chosen embedding of the base field.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mixedEmbeddingsOver : {K : Type u_3} -> (L : Type u_4) -> [Field K] -> [Field L] -> (ψ : K →+* ℂ) -> [Algebra K L] -> Set (L →+* ℂ)
<!-- PINNED-SIGNATURE:END -->


`{K : Type u_3} → (L : Type u_4) → [Field K] → [Field L] → (ψ : K →+* ℂ) → [Algebra K L] → Set (L →+* ℂ)`

The implicit type argument `K` is the base field. The explicit argument `L` is the extension field (the field whose embeddings are being classified). The instance argument `[Field K]` equips `K` with its field structure. The instance argument `[Field L]` equips `L` with its field structure. The argument `ψ : K →+* ℂ` is the chosen complex embedding of the base field `K` that the embeddings of `L` must extend. The instance `[Algebra K L]` makes `L` an algebra over `K`, providing the notion of restriction of embeddings from `L` to `K`.

### Conventions

No junk-value conventions are declared for this definition: the definition is total and set-valued; for any valid inputs the result is a well-formed (possibly empty) subset of `L →+* ℂ`.

### Worked examples

- Claim: For `L = ℂ`, `K = ℝ`, and `ψ` the inclusion `ℝ →+* ℂ`, the set `VTask.mixedEmbeddingsOver ℂ ψ` contains the identity embedding `id : ℂ →+* ℂ` if and only if the identity is mixed over `ℝ`.

- Claim: For `K = ℚ`, `L = ℚ`, and `ψ : ℚ →+* ℂ` the unique embedding, the set `VTask.mixedEmbeddingsOver ℚ ψ` is empty, since the unique embedding of `ℚ` into `ℂ` has image in `ℝ` and is therefore real, not mixed.

- Claim: For a totally imaginary quadratic extension `L/K` in which all embeddings are non-real, every embedding of `L` lying over `ψ` belongs to `VTask.mixedEmbeddingsOver L ψ` (the mixed condition is satisfied by all of them).

### Boundaries

- If `L = K` (the trivial extension), then the only embedding lying over `ψ` is `ψ` itself when restricted; if `ψ` happens to be a real embedding (image in `ℝ`), the set is empty.
- If every embedding of `L` over `ψ` is real (e.g. `L/K` is totally real), then `VTask.mixedEmbeddingsOver L ψ` is empty.
- If every embedding of `L` over `ψ` is non-real and mixed (e.g. totally imaginary extensions), then the set equals the full fiber of embeddings over `ψ`.
- The set is always a subset of the full set of embeddings of `L` into `ℂ` lying over `ψ`; the complementary subset consists of the real embeddings over `ψ`.

### Not to be confused with

- The set of *all* complex embeddings of `L` lying over `ψ` (without the mixed condition) — that is a strictly larger set whenever there are real embeddings above `ψ`.
- `ComplexEmbedding.IsMixed K φ` alone — that predicate applies to a single embedding and does not filter by a fixed `ψ`.
- The set of *real* embeddings over `ψ` — those are the complementary embeddings (neither mixed nor otherwise complex) in the fiber over `ψ`.