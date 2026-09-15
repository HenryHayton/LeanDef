## VTask.sheafify

### Object

Given a prelocal predicate `P` on a type-valued sheaf over a topological space `X`, `VTask.sheafify P` produces the *sheafification* of `P`: the smallest local predicate that is implied by `P` locally. Concretely, `VTask.sheafify P` declares that a section `f` over an open set `U` satisfies the predicate if and only if every point of `U` has some open neighbourhood (contained in `U`) on which the restriction of `f` satisfies the original predicate `P`. This is the standard procedure for turning a prelocal condition into a genuinely local one, analogous to sheafifying a presheaf.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sheafify : {X : TopCat} -> {T : ↑X → Type u_2} -> (P : TopCat.PrelocalPredicate T) -> TopCat.LocalPredicate T
<!-- PINNED-SIGNATURE:END -->


The implicit argument `X` is the topological space over which everything lives. The implicit argument `T` is the type-valued function that assigns a stalk type to each point of `X`. The explicit argument `P` is the prelocal predicate to be sheafified: it specifies a condition on sections that is already stable under restriction but need not satisfy the locality (gluing) axiom.

### Conventions

There are no junk-value or edge-case conventions declared for this definition: it is a total construction that is well-defined for every prelocal predicate on every topological space, and no special output value is assigned at any boundary.

### Worked examples

- Claim: For any prelocal predicate `P` on `T` over `X`, the result `VTask.sheafify P` is a `LocalPredicate T`, meaning it satisfies both the restriction axiom and the locality (gluing) axiom.

- Claim: If `P` is already a local predicate (viewed as a prelocal predicate by forgetting the locality axiom), then `VTask.sheafify P` accepts exactly the same sections as `P` itself — that is, sheafifying an already-local predicate does not change it.

- Claim: For any section `f` over `U` and any open cover of `U` by opens on each of which the restriction of `f` satisfies `P`, the section `f` satisfies `VTask.sheafify P` over `U`.

- Claim: If `P.pred f` holds for a section `f` over `U` (i.e., `f` already satisfies the prelocal predicate on all of `U`), then `(VTask.sheafify P).pred f` also holds, since one may take the whole of `U` as the neighbourhood for each point.

### Boundaries

- When `U` is the empty open set, the universal quantifier `∀ x : U, …` is vacuously true, so every section over the empty set satisfies `VTask.sheafify P`.
- If `P.pred` accepts all sections (the trivially true prelocal predicate), then `VTask.sheafify P` also accepts all sections.
- If `P.pred` rejects all sections, `VTask.sheafify P` likewise rejects all sections, since no neighbourhood can witness the condition.
- The construction is monotone in `P`: if one prelocal predicate implies another pointwise, the same implication holds after sheafification.

### Not to be confused with

- `TopCat.PrelocalPredicate` — the input type; a prelocal predicate satisfies restriction but not necessarily locality, whereas `VTask.sheafify` outputs a full local predicate.
- `TopCat.LocalPredicate` — the output type; one should not confuse the *type* of local predicates with the *operation* of sheafifying a prelocal predicate into one.
- Sheafification of a presheaf of sets/types — that process produces a new sheaf of sections, whereas `VTask.sheafify` operates on predicates (sub-presheaves) and produces a predicate, not a new type-valued sheaf.
