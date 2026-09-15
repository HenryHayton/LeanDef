## Object

The **sequential closure** of a set `s` in a topological space `X` is the collection of all points `a ∈ X` that can be reached as limits of sequences whose terms all lie in `s`. Concretely, a point `a` belongs to the sequential closure of `s` if and only if there exists a sequence `x : ℕ → X` with every term in `s` and with `x n` converging (in the topology of `X`) to `a` as `n → ∞`.

The sequential closure is always at least as large as `s` itself, and is always contained in the topological closure of `s`. However, unlike the topological closure, it need not be sequentially closed: a second pass of the sequential-closure operator may yield additional points.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.seqClosure : {X : Type u_1} -> [TopologicalSpace X] -> (s : Set X) -> Set X
<!-- PINNED-SIGNATURE:END -->


`VTask.seqClosure : {X : Type u_1} -> [TopologicalSpace X] -> (s : Set X) -> Set X`

The implicit type argument `X` is the ambient topological space. The instance argument supplies the topology on `X`. The explicit argument `s` is the set whose sequential closure is being formed.

## Conventions

There are no junk-value or degenerate-input conventions specific to this definition that require declaration: the operator is well-defined and meaningful for every set `s` in every topological space, including the empty set and the whole space.

## Worked examples

- Claim: Every point of `s` already belongs to `VTask.seqClosure s` (i.e., `s ⊆ VTask.seqClosure s`), since the constant sequence at any `a ∈ s` is a sequence in `s` converging to `a`.

- Claim: For a set `s` in a Fréchet–Urysohn space, `VTask.seqClosure s` equals the full topological closure of `s`. In particular, in `ℝ` (which is Fréchet–Urysohn), the sequential closure of the open interval `(0, 1)` is the closed interval `[0, 1]`.

- Claim: `VTask.seqClosure s ⊆ closure s` for any set `s` in any topological space, since every limit of a sequence in `s` is also a limit point in the topological sense.

- Claim: If `s` is sequentially closed (i.e., `IsSeqClosed s`), then `VTask.seqClosure s = s`; conversely, `VTask.seqClosure s = s` implies `IsSeqClosed s`.

## Boundaries

- **Empty set**: `VTask.seqClosure ∅ = ∅`, because any sequence in the empty set is vacuously impossible (there are no terms to pick), so no point can arise as a limit of such a sequence.
- **Whole space**: `VTask.seqClosure univ = univ`, since for any point `a` the constant sequence at `a` is a sequence in `univ` converging to `a`.
- **Idempotence fails in general**: Unlike topological closure, applying `VTask.seqClosure` twice is not guaranteed to equal a single application; there exist topological spaces and sets where `VTask.seqClosure (VTask.seqClosure s) ⊋ VTask.seqClosure s`.
- **Fréchet–Urysohn spaces**: In these spaces, sequential closure coincides with topological closure and is therefore idempotent.

## Not to be confused with

- `closure s`: The topological closure of `s`, defined via the neighborhood filter; always contains `VTask.seqClosure s` but may be strictly larger in non-Fréchet–Urysohn spaces.
- `IsSeqClosed s`: A predicate asserting that `s` is sequentially closed, i.e., that `VTask.seqClosure s = s`; this is a property of `s`, not a set derived from `s`.
- `SeqClosure` (iterated or transfinite sequential closure): A construction that applies the sequential-closure operator transfinitely until stabilization; distinct from the single-step `VTask.seqClosure`.