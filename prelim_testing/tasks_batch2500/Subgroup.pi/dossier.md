## Object

`VTask.pi I H` is the **product (pi) subgroup** of the direct product group `∀ i, f i`. Given an index set `I ⊆ η` and a family of subgroups `H i ≤ f i`, it is the subgroup consisting of all dependent functions `x : ∀ i, f i` such that, for every index `i` belonging to `I`, the component `x i` lies in the subgroup `H i`. Indices outside `I` are unconstrained. This is the group-theoretic analogue of the set-theoretic pi construction.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {η : Type u_7} -> {f : η → Type u_8} -> [(i : η) → Group (f i)] -> (I : Set η) -> (H : (i : η) → Subgroup (f i)) -> Subgroup ((i : η) → f i)
<!-- PINNED-SIGNATURE:END -->


VTask.pi : {η : Type u_7} -> {f : η → Type u_8} -> [(i : η) → Group (f i)] -> (I : Set η) -> (H : (i : η) → Subgroup (f i)) -> Subgroup ((i : η) → f i)

The index type `η` is the type of indices. The family `f : η → Type` assigns a group to each index; the instance argument provides the group structure on each `f i`. The set `I : Set η` is the **active index set**: only indices in `I` contribute constraints. The family `H : (i : η) → Subgroup (f i)` assigns to each index `i` a subgroup of the corresponding component group; the resulting pi subgroup constrains the `i`-th component to lie in `H i` precisely when `i ∈ I`.

## Conventions

When `I = Set.univ`, every component is constrained: `x` belongs to `VTask.pi Set.univ H` if and only if `x i ∈ H i` for all `i`. When `I = ∅`, there are no constraints and `VTask.pi ∅ H` equals the full subgroup `⊤`. For indices `i ∉ I`, the value of `H i` is irrelevant to membership.

## Worked examples

- Claim: A function `x` belongs to `VTask.pi I H` if and only if `x i ∈ H i` for every `i ∈ I`.

- Claim: `VTask.pi Set.univ (fun _ => ⊥)` equals the trivial subgroup `⊥` of `∀ i, f i` (by the theorem `pi_bot` analogue).

- Claim: If `H i = ⊤` for all `i`, then `VTask.pi Set.univ H = ⊤`, since every component constraint is trivially satisfied.

- Claim: For a product of two groups `G₁ × G₂` indexed by `Fin 2`, the pi subgroup over `Set.univ` of subgroups `H 0` and `H 1` consists exactly of pairs whose first component lies in `H 0` and whose second lies in `H 1`.

## Boundaries

- **Empty index set**: `VTask.pi ∅ H = ⊤`, the whole product group, because there are no constraints to impose.
- **Full index set**: `VTask.pi Set.univ H` is the direct product of all the subgroups; it is `⊥` if and only if each `H i = ⊥` (componentwise triviality).
- **Single-element index set**: `VTask.pi {i₀} H` constrains only the `i₀`-th component to lie in `H i₀`; all other components are free.
- **Monotonicity in `H`**: If `H i ≤ K i` for all `i ∈ I`, then `VTask.pi I H ≤ VTask.pi I K`.
- **Monotonicity in `I`**: If `I ⊆ J`, then `VTask.pi J H ≤ VTask.pi I H` (a larger active set imposes more constraints).
- The construction is closed under inverses (as well as products and the identity) by construction, making it a genuine subgroup.

## Not to be confused with

- `Submonoid.pi`: The analogous construction for submonoids, which does **not** include the inverse-closure condition; `VTask.pi` extends it with that closure.
- `AddSubgroup.pi`: The additive version of this exact construction, for families of additive groups and additive subgroups.
- `Set.pi`: The set-theoretic pi construction for sets (not groups), from which this borrows its notation and spirit but which carries no algebraic structure.