## Object

`VTask.pi s L` is the **product sublattice** of the full dependent-function lattice `(i : κ) → π i`. Concretely, it is the sublattice whose elements are exactly those dependent functions `f` such that, for every index `i` belonging to the index set `s`, the value `f i` lies in the sublattice `L i`. For indices `i` outside `s`, no constraint is imposed on `f i`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {κ : Type u_5} -> {π : κ → Type u_6} -> [(i : κ) → Lattice (π i)] -> (s : Set κ) -> (L : (i : κ) → Sublattice (π i)) -> Sublattice ((i : κ) → π i)
<!-- PINNED-SIGNATURE:END -->


```
VTask.pi : {κ : Type u_5} -> {π : κ → Type u_6} -> [(i : κ) → Lattice (π i)] -> (s : Set κ) -> (L : (i : κ) → Sublattice (π i)) -> Sublattice ((i : κ) → π i)
```

- `κ` is the implicit index type whose elements label the coordinate directions.
- `π` is the implicit family of types, one per index, each equipped with a lattice structure via the instance argument `[(i : κ) → Lattice (π i)]`.
- `s` is the **controlling index set**: membership in the product sublattice is enforced only at indices belonging to `s`.
- `L` is the **family of sublattices**: for each index `i`, `L i` is a sublattice of `π i` specifying which values are permitted at coordinate `i` (when `i ∈ s`).

## Conventions

When `s = Set.univ`, every coordinate is constrained, and `VTask.pi Set.univ L` is the "full" product of the sublattices `L i`. When `s = ∅`, no coordinate is constrained, and `VTask.pi ∅ L` is the top sublattice of `(i : κ) → π i` (every dependent function qualifies). These two extreme choices of `s` are the canonical boundary conventions; there are no junk-value conventions for out-of-domain inputs because the definition is total.

## Worked examples

- Claim: A dependent function `f : (i : Fin 2) → Bool` belongs to `VTask.pi Set.univ L` if and only if `f i ∈ L i` for every `i`.

- Claim: For any family `L` and any dependent function `f`, `f ∈ VTask.pi ∅ L` holds unconditionally (because no index lies in the empty set, so no constraint is imposed).

- Claim: If `L i = ⊥` for some `i`, then `VTask.pi Set.univ L = ⊥` (the whole product sublattice collapses to bottom, since the only member would need to have `f i` in the bottom sublattice for every coordinate).

- Claim: `VTask.pi s L ≤ VTask.pi s L'` whenever `L i ≤ L' i` for all `i ∈ s` (monotonicity in the fiber sublattices).

## Boundaries

- **Empty index set (`s = ∅`):** No index is controlled, so every dependent function belongs to `VTask.pi ∅ L`. This equals the top sublattice `⊤`.
- **Full index set (`s = Set.univ`):** Every coordinate is constrained. The resulting sublattice is the standard cartesian product of all `L i`.
- **Bottom fiber (`L i = ⊥` for some `i ∈ s`):** The product sublattice over `Set.univ` collapses to `⊥` (as guaranteed by `pi_univ_eq_bot`).
- **Bottom all fibers with nonempty index type:** `VTask.pi Set.univ (fun _ ↦ ⊥) = ⊥` (as guaranteed by `pi_univ_bot`).
- **The definition is total:** it accepts any `s : Set κ` and any family `L`, with no domain restriction.

## Not to be confused with

- `Sublattice.comap`: pulls back a single sublattice along a lattice homomorphism; `VTask.pi` simultaneously controls all coordinates over a set of indices.
- `Set.pi`: the analogous construction for plain sets (not sublattices); `VTask.pi` additionally closes under finite meets and joins in each fiber.
- `Sublattice.iInf` / meet of sublattices: takes the intersection of sublattices of the *same* lattice, whereas `VTask.pi` builds a sublattice of the *product* lattice from sublattices of each factor.
