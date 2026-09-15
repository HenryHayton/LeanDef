## VTask.codRestrict

### Object

Given a first-order language `L`, two `L`-structures `M` and `N`, a substructure `p` of `N`, and an `L`-embedding `f : M → N` whose image is entirely contained in `p`, `VTask.codRestrict p f h` is the `L`-embedding `M → p` obtained by viewing `f` as mapping into `p` rather than all of `N`. The resulting map sends each element `m : M` to the element `f m` regarded as a member of `p`. It is injective and preserves all function symbols and relation symbols of `L`, just as `f` does.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.codRestrict : {L : FirstOrder.Language} -> {M : Type w} -> {N : Type u_1} -> [L.Structure M] -> [L.Structure N] -> (p : L.Substructure N) -> (f : L.Embedding M N) -> (h : ∀ (c : M), f c ∈ p) -> L.Embedding M ↥p
<!-- PINNED-SIGNATURE:END -->


`VTask.codRestrict : {L : FirstOrder.Language} -> {M : Type w} -> {N : Type u_1} -> [L.Structure M] -> [L.Structure N] -> (p : L.Substructure N) -> (f : L.Embedding M N) -> (h : ∀ (c : M), f c ∈ p) -> L.Embedding M ↥p`

The implicit argument `L` is the first-order language with respect to which all structures and embeddings are defined. The implicit type `M` is the domain structure being embedded. The implicit type `N` is the ambient target structure. The instance arguments equip `M` and `N` with their respective `L`-structure. The explicit argument `p` is the substructure of `N` that serves as the restricted codomain. The argument `f` is the original `L`-embedding from `M` into `N`. The argument `h` is the proof that every element of `M` maps under `f` into `p`, which is the condition that makes the codomain restriction well-defined.

### Conventions

No junk-value conventions are declared for this definition: it is a total construction whose output is uniquely determined once the arguments are supplied, and every input satisfying the stated types and the membership hypothesis `h` yields a valid bundled embedding. There are no out-of-domain inputs to assign sentinel values to.

### Worked examples

- Claim: For the trivial embedding of a structure into itself (the identity), restricting the codomain to the top substructure yields an embedding whose underlying function agrees with the identity on each element.

- Claim: If `f : M → N` is an `L`-embedding and `p` is the image substructure of `f`, then `VTask.codRestrict p f h` is an `L`-embedding `M → p` sending each `m` to the element `⟨f m, _⟩ : p`.

- Claim: The composition of the substructure inclusion `p → N` with `VTask.codRestrict p f h` equals `f` as an embedding `M → N`.

### Boundaries

- If `p` is the top substructure (equal to all of `N`), then `VTask.codRestrict p f h` still produces a well-typed embedding `M → ↥p`, which is canonically isomorphic to `f` itself.
- If `p` is a proper substructure, the restricted embedding has a strictly smaller (or equal) codomain type, even though the underlying function values are identical to those of `f`.
- The hypothesis `h` must cover *every* element of `M`; a partial containment is not sufficient to invoke this construction.
- The injectivity of the resulting embedding is inherited directly from `f`; no additional injectivity hypothesis on `p` is needed.

### Not to be confused with

- `L.Substructure.inclusion`: the canonical embedding of one substructure into a larger one, not a restriction of a given embedding's codomain.
- `L.Embedding.domRestrict` (or analogous): a restriction of the *domain* of an embedding to a substructure, as opposed to restricting the codomain.
- `L.Hom.codRestrict`: the analogous construction for `L`-homomorphisms (which are not required to be injective), of which this is the injective refinement.