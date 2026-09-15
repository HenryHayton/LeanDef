## VTask.range_toPermHom'

### Object

For a permutation `g` of a finite type `α`, this is a subgroup of the group of permutations of `g`'s cycle factors: specifically, the subgroup consisting of those permutations `τ` of the set of cycle factors that **preserve cycle length**, i.e., every cycle factor `c` in `g.cycleFactorsFinset` satisfies `|support(τ(c))| = |support(c)|`. In other words, `τ` is allowed to permute the cycles of `g` freely, but only among cycles of the same size.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.range_toPermHom' : {α : Type u_1} -> [DecidableEq α] -> [Fintype α] -> (g : Equiv.Perm α) -> Subgroup (Equiv.Perm ↥g.cycleFactorsFinset)
<!-- PINNED-SIGNATURE:END -->


`VTask.range_toPermHom' : {α : Type u_1} -> [DecidableEq α] -> [Fintype α] -> (g : Equiv.Perm α) -> Subgroup (Equiv.Perm ↥g.cycleFactorsFinset)`

- The implicit type `α` is the finite type on which the base permutation lives.
- The `DecidableEq α` and `Fintype α` instances provide the decidable equality and finiteness needed to work with cycle factors.
- `g` is the permutation of `α` whose cycle-factor structure is used; its cycle factors form the finite set `g.cycleFactorsFinset`, and the subgroup lives in the group of permutations of that set.

### Conventions

There are no special junk-value or boundary conventions declared for this definition: it is a total, well-typed construction on any permutation `g` of any `DecidableEq` `Fintype`, and every case is handled without sentinel values.

### Worked Examples

- Claim: The identity permutation on `g.cycleFactorsFinset` belongs to `VTask.range_toPermHom' g` for any `g`, since `|support(id(c))| = |support(c)|` trivially.

- Claim: For a permutation `g : Equiv.Perm (Fin 4)` that is a single 4-cycle, `g.cycleFactorsFinset` has exactly one element, so the only permutation of cycle factors is the identity, and `VTask.range_toPermHom' g` is the trivial subgroup.

- Claim: For a permutation `g` that decomposes into two cycles of equal length, the permutation of cycle factors that swaps those two cycles belongs to `VTask.range_toPermHom' g`, because swapping two cycles of the same size preserves cycle support cardinality.

- Claim: For a permutation `g` that decomposes into two cycles of **different** lengths, the permutation of cycle factors that swaps those two cycles does **not** belong to `VTask.range_toPermHom' g`, because it would map a cycle of one size to a slot requiring the other size.

### Boundaries

- When `g` is the identity permutation, `g.cycleFactorsFinset` is empty, so the only permutation of cycle factors is the identity, and `VTask.range_toPermHom' g` is the trivial subgroup of the trivial group.
- When `g` is a single cycle (of any length), `g.cycleFactorsFinset` is a singleton, the group of permutations of cycle factors is trivial, and `VTask.range_toPermHom' g` is again the trivial subgroup.
- When all cycles of `g` have distinct lengths, only the identity permutation preserves all cycle-support sizes, so the subgroup is trivial.
- When all cycles of `g` have the same length `k`, any permutation of the cycle factors preserves cycle-support size, so `VTask.range_toPermHom' g` is the full symmetric group on `g.cycleFactorsFinset`.

### Not to be confused with

- `Equiv.Perm.OnCycleFactors.toPermHom`: This is the group homomorphism whose *range* equals `VTask.range_toPermHom'`; the present object is that range as a subgroup, not the homomorphism itself.
- The full symmetric group `⊤ : Subgroup (Equiv.Perm ↥g.cycleFactorsFinset)`: This contains all permutations of cycle factors regardless of cycle length, whereas `VTask.range_toPermHom'` imposes the support-size-preservation constraint.
- `g.cycleFactorsFinset` itself: This is the underlying finite set of cycles, not a subgroup; `VTask.range_toPermHom'` is a subgroup of permutations *of* that set.