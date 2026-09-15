## Object

The *lower central series* of a subgroup `S` of a group `G`, computed inside the ambient group `G`. It is the sequence of subgroups `S = S_0 ⊇ S_1 ⊇ S_2 ⊇ ⋯` defined by starting at `S` and repeatedly taking the commutator subgroup of the current term with `S`. Concretely, `S_n` consists of all products of (nested) commutators of the form `⁅⁅⋯⁅s₁, s₂⁆, s₃⁆⋯, sₙ₊₁⁆` with each `sᵢ ∈ S`. The series measures how far `S` is from being abelian: it terminates at the trivial subgroup precisely when `S` is nilpotent.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lowerCentralSeries : {G : Type u_1} -> [Group G] -> (S : Subgroup G) -> ℕ → Subgroup G
<!-- PINNED-SIGNATURE:END -->


`VTask.lowerCentralSeries : {G : Type u_1} -> [Group G] -> (S : Subgroup G) -> ℕ → Subgroup G`

The implicit type argument `G` is the ambient group. The instance argument supplies the group structure on `G`. The explicit argument `S` is the subgroup whose lower central series is being computed (taking `S = ⊤` recovers the classical lower central series of `G` itself). The final `ℕ` argument is the index `n`, selecting the `n`-th term of the series.

## Conventions

At index `0` the series returns `S` itself, not the trivial subgroup. Every subsequent term is the mutual commutator subgroup of the previous term with `S`, so the series is anchored at `S` rather than at `G`.

## Worked examples

- Claim: `VTask.lowerCentralSeries S 0 = S` for any subgroup `S` — the zeroth term of the lower central series is `S` itself.

- Claim: `VTask.lowerCentralSeries S 1 = ⁅S, S⁆` — the first term is the commutator subgroup of `S` with itself, i.e. the derived subgroup of `S` computed inside `G`.

- Claim: If `G` is abelian then `VTask.lowerCentralSeries ⊤ 1 = ⊥` — in an abelian group every commutator is trivial, so the first derived term of the whole group is the trivial subgroup.

- Claim: For the trivial subgroup `⊥` of any group, `VTask.lowerCentralSeries ⊥ n = ⊥` for all `n` — since every commutator involving only the identity is again the identity, the series stabilises immediately at the trivial subgroup.

## Boundaries

- At `n = 0`: the series returns exactly `S`, regardless of the structure of `G` or `S`. There is no "pre-initial" term; the series genuinely starts at `S`.
- For the trivial subgroup `⊥`: every term is `⊥`.
- For the whole group `⊤`: the series coincides with the classical lower central series `G = γ₁G ⊇ γ₂G ⊇ ⋯`.
- The series is non-increasing: each term is a subgroup of the preceding one (`S_{n+1} ≤ S_n`).
- If the series reaches `⊥` at some finite stage, `S` is nilpotent; the least such `n` is the nilpotency class of `S`.

## Not to be confused with

- **Upper central series**: a different series ascending from the centre, used also to characterise nilpotency but built dually by taking successive centres rather than successive commutators.
- **Derived series (lower derived series)**: the iterated *derived subgroup* `S ⊇ [S,S] ⊇ [[S,S],[S,S]] ⊇ ⋯` where each step commutes the current term with *itself*, not with the fixed subgroup `S`; this measures solvability rather than nilpotency.
- **`Subgroup.commutator S S`** (a single application): this gives only the first non-trivial term `S_1 = ⁅S, S⁆` of the series, not the full indexed family.