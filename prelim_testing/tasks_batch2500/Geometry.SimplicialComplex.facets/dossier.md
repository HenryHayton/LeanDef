## VTask.facets

### Object

Given a simplicial complex `K`, the **facets** of `K` are those faces of `K` that are *maximal*: a face `s` is a facet if no strictly larger face of `K` contains it. Equivalently, `s` is a facet if and only if `s` belongs to `K` and there is no face `t` of `K` with `s ⊊ t`. The set of facets is a subset of the set of all faces, and every face of `K` is contained in at least one facet (in finite settings, though this is a structural property of simplicial complexes in general).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.facets : {𝕜 : Type u_1} -> {E : Type u_2} -> [Ring 𝕜] -> [PartialOrder 𝕜] -> [AddCommGroup E] -> [Module 𝕜 E] -> (K : Geometry.SimplicialComplex 𝕜 E) -> Set (Finset E)
<!-- PINNED-SIGNATURE:END -->


The implicit arguments `𝕜` and `E` are the coefficient ring (carrying a ring structure and a partial order) and the ambient vector space (carrying an additive commutative group and a module structure over `𝕜`). The explicit argument `K` is the simplicial complex whose set of facets is being extracted.

### Conventions

There are no special junk-value conventions for this definition: it is a well-defined subset of a well-defined set of faces, and every simplicial complex (including the empty one) yields a valid, possibly empty, set of facets.

### Worked examples

- Claim: Every facet of `K` is a face of `K`; that is, `VTask.facets K ⊆ K.faces` for any simplicial complex `K`.

- Claim: If `K` has a single face `{v}` (for some vertex `v`), then `{v}` is a facet of `K`, because there is no strictly larger face to contain it.

- Claim: If `s` and `t` are both facets of `K` and `s ⊆ t`, then `s = t`; distinct facets of the same complex are never comparable by inclusion.

- Claim: The empty simplicial complex (with no faces) has an empty set of facets: `VTask.facets K = ∅` when `K.faces = ∅`.

### Boundaries

- **Empty complex**: If `K.faces` is empty, then `VTask.facets K` is also empty—there are no faces to be maximal.
- **Single face**: If `K` has exactly one face `s`, then `s` is its unique facet.
- **Point complex**: A simplicial complex consisting only of a single vertex `{v}` has `{v}` as its sole facet.
- **Subsumption**: A face `s` that is strictly contained in another face of `K` is *not* a facet, even if `s` has large cardinality.
- **All faces maximal**: In a simplicial complex where no face is a subset of another (an antichain), every face is a facet.

### Not to be confused with

- `K.faces`: The set of *all* faces of the simplicial complex, of which `VTask.facets K` is a (possibly proper) subset.
- The faces of a convex polytope: In polyhedral geometry, "facets" refers specifically to codimension-1 faces; here the term means maximal faces of the simplicial complex, regardless of dimension.
- `Geometry.SimplicialComplex.ofErase` or similar constructors: These build simplicial complexes from facet data, which is conceptually the reverse operation from extracting facets via `VTask.facets`.