## VTask.presheafToTypes

### Object

Given a topological space `X` and a type family `T` assigning to each point `x : X` a type `T x`, this is the presheaf of *all* dependent functions over open sets of `X`. Concretely, for every open set `U ⊆ X`, the sections of this presheaf over `U` are all functions that assign to each point `x ∈ U` an element of the fibre `T x`. Restriction maps send a section over a larger open set to its pointwise restriction to a smaller one. No continuity or any other regularity condition is imposed on the sections — they are purely set-theoretic dependent functions.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.presheafToTypes : (X : TopCat) -> (T : ↑X → Type u_1) -> TopCat.Presheaf (Type (max u_1 u_2)) X
<!-- PINNED-SIGNATURE:END -->


`(X : TopCat) -> (T : ↑X → Type u_1) -> TopCat.Presheaf (Type (max u_1 u_2)) X`

The first argument `X` is the ambient topological space over which the presheaf lives. The second argument `T` is a type family, assigning to each point `x` of the underlying set of `X` a type `T x`, which serves as the fibre above that point.

### Conventions

There are no junk-value or boundary conventions for this definition: it is defined for every topological space `X` and every type family `T` without restriction, and every open set (including the empty set) is handled uniformly by the dependent-function construction.

### Worked examples

- Claim: For the trivial one-point space and constant fibre `ℤ`, the sections over the whole space form a type equivalent to `ℤ`.

- Claim: The restriction map of `VTask.presheafToTypes X T` along an inclusion `V ⊆ U` sends a section `f : ∀ x : U, T x` to the section `fun x : V => f (inclusion x)`, i.e., it restricts the domain pointwise.

- Claim: For any open set `U` and the constant family `T = fun _ => α`, the sections `(VTask.presheafToTypes X (fun _ => α)).obj (op U)` are in bijection with all functions from the underlying type of `U` to `α`.

### Boundaries

- **Empty open set**: Sections over the empty open set form the type of functions out of the empty type, which is a contractible singleton (the unique function from `∅`). This is consistent with the general sheaf/presheaf convention.
- **Whole space**: Sections over `X` itself are all functions `∀ x : X, T x` with no restriction whatsoever.
- **Universe levels**: The section type lives in `Type (max u_1 u_2)` to accommodate both the universe of `T` and that of the index; this is a universe bookkeeping detail with no mathematical content.
- **No continuity**: Unlike sheaves of continuous functions, there is no requirement that sections respect the topology. Every set-theoretic dependent function is a valid section.

### Not to be confused with

- **Sheaf of continuous functions / `TopCat.Presheaf` of continuous sections**: That construction requires sections to be continuous maps, whereas `VTask.presheafToTypes` imposes no continuity at all.
- **`TopCat.Presheaf (Type _) X` as an arbitrary presheaf**: The present object is a *specific* presheaf canonically built from a type family `T`; an arbitrary presheaf of types need not arise this way.
- **Constant presheaf**: The constant presheaf assigns the same fixed type to every open set; `VTask.presheafToTypes` allows the fibre to vary pointwise with `T`, so sections are genuinely dependent.