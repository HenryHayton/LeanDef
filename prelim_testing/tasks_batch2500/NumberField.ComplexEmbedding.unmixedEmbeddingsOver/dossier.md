## VTask.unmixedEmbeddingsOver

### Object

Given a field extension $K \subseteq L$ and a ring homomorphism $\psi : K \to \mathbb{C}$ (a complex embedding of the base field $K$), this is the set of all ring homomorphisms $\varphi : L \to \mathbb{C}$ (complex embeddings of $L$) that simultaneously (1) extend $\psi$, i.e., $\varphi|_K = \psi$, and (2) are *unmixed* over $K$, meaning that $\varphi$ and its complex conjugate $\bar{\varphi}$ lie in the same Galois orbit over $K$, or equivalently that $\varphi$ does not "mix" real and complex places in a certain precise sense tied to the embedding theory of number fields.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.unmixedEmbeddingsOver : {K : Type u_3} -> (L : Type u_4) -> [Field K] -> [Field L] -> (ψ : K →+* ℂ) -> [Algebra K L] -> Set (L →+* ℂ)
<!-- PINNED-SIGNATURE:END -->


The type parameters `K` and `L` are fields connected by an algebra structure `[Algebra K L]`. The instance `[Field K]` and `[Field L]` equip both with field operations. The explicit argument `L` is the extension field whose embeddings into $\mathbb{C}$ are being classified. The argument `ψ : K →+* ℂ` is the fixed complex embedding of the base field $K$ that candidate embeddings of $L$ must restrict to.

### Conventions

No special junk-value or boundary conventions are declared for this definition: the set is well-formed for any valid inputs, and an embedding that fails either the lying-over condition or the unmixed condition simply does not belong to the set.

### Worked examples

- Claim: Every element $\varphi$ of `VTask.unmixedEmbeddingsOver L ψ` satisfies `ComplexEmbedding.LiesOver φ ψ`.

- Claim: Every element $\varphi$ of `VTask.unmixedEmbeddingsOver L ψ` satisfies `IsUnmixed K φ`.

- Claim: `VTask.unmixedEmbeddingsOver L ψ` is a subset of the set of all complex embeddings of `L` lying over `ψ` (i.e., the unmixed embeddings form a subset of all extensions of `ψ`).

### Boundaries

- If no complex embedding of $L$ lies over $\psi$, the set is empty.
- If every embedding lying over $\psi$ fails the unmixed condition, the set is also empty.
- If every embedding lying over $\psi$ is unmixed (e.g., when $L$ is totally real or $\psi$ itself is a real embedding and the extension is of a particular type), the set coincides with the full set of embeddings over $\psi$.
- The definition makes sense even when $K = L$ and $\psi$ is the unique embedding lying over itself; in that case membership is determined solely by whether $\psi$ is unmixed.

### Not to be confused with

- The set of *all* complex embeddings of $L$ lying over $\psi$ (no unmixed constraint): this is a strictly larger set whenever some extensions of $\psi$ are mixed.
- `IsUnmixed K φ` alone (the predicate on a single embedding): the present object is a *set* collecting all embeddings satisfying both lying-over and unmixed simultaneously.
- The set of all unmixed embeddings of $L$ (without fixing the base embedding $\psi$): that would be the union over all choices of $\psi$ of the present set.