## VTask.lfpApprox

### Object

`VTask.lfpApprox f x a` is the `a`-th stage in a transfinite approximation sequence converging to the least fixed point of a monotone map `f` on a complete lattice, starting from an initial value `x`. The sequence is indexed by ordinals and built by iterating `f` transfinitely: at each stage `a`, the approximant is the join (supremum) of all values `f(lfpApprox f x b)` for ordinals `b` strictly less than `a`, taken together with the initial value `x`. In particular, stage `0` simply returns `x` itself, and at each later stage the approximant can only grow. The sequence is non-decreasing in `a` and, for a sufficiently large ordinal, stabilises at the least fixed point of `f` that is greater than or equal to `x`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lfpApprox : {α : Type u} -> [CompleteLattice α] -> (f : α →o α) -> (x : α) -> (a : Ordinal.{u}) -> α
<!-- PINNED-SIGNATURE:END -->


The type parameter `α` is the underlying complete lattice type. The instance argument supplies the complete-lattice structure on `α`. The argument `f` is the monotone self-map of `α` whose least fixed point (above `x`) is being approximated; it is given as an order-homomorphism `α →o α`. The argument `x` is the initial value (lower bound) from which the iteration starts. The argument `a` is the ordinal index selecting which stage of the approximation sequence to evaluate.

### Conventions

At ordinal `0`, the approximant equals the initial value `x` exactly: `VTask.lfpApprox f x 0 = x`. This is a boundary convention arising from the empty supremum being the bottom element of the lattice, joined with `x`. There are no junk-value conventions beyond this canonical base case, since the function is total and well-defined at every ordinal.

### Worked examples

- Claim: For any complete lattice `α`, monotone map `f`, and element `x`, `VTask.lfpApprox f x 0 = x`.

- Claim: For the identity map `id` on a complete lattice and initial value `x`, every stage of the approximation satisfies `VTask.lfpApprox (OrderHom.id) x a = x`, because applying `id` and taking suprema over a chain of constant `x` values still yields `x`.

- Claim: The approximation sequence is monotone in its ordinal argument: if `a ≤ b` then `VTask.lfpApprox f x a ≤ VTask.lfpApprox f x b`.

- Claim: For every ordinal `a`, the initial value is a lower bound: `x ≤ VTask.lfpApprox f x a`.

- Claim: For a successor ordinal `a + 1`, the approximant satisfies `VTask.lfpApprox f x (a + 1) = x ⊔ f (VTask.lfpApprox f x a)`, reflecting one explicit application of `f` beyond stage `a`.

### Boundaries

- At ordinal `0`: the approximant is exactly `x`, since the supremum over the empty set of ordinals below `0` is `⊥`, and `x ⊔ ⊥ = x`.
- At a successor ordinal `a + 1`: the approximant equals `x ⊔ f(VTask.lfpApprox f x a)`, folding in precisely one new application of `f`.
- At a limit ordinal `λ`: the approximant is the supremum `x ⊔ ⨆ {b | b < λ}, f(VTask.lfpApprox f x b)`, capturing the least upper bound of all previous stages' images under `f`.
- The sequence is bounded above by any pre-fixed point of `f` that is ≥ `x`; in particular it is bounded above by the least fixed point of `f` that is ≥ `x`.
- For a sufficiently large ordinal (related to the cardinality of `α`), the sequence stabilises and its value is the least fixed point of `f` above `x`.

### Not to be confused with

- `OrderHom.lfp`: the actual least fixed point of `f` on a complete lattice, which is the eventual limit of the approximation sequence, not an intermediate stage.
- `gfpApprox`: the dual sequence approximating the greatest fixed point from above by a downward iteration.
- The plain iteration `f^[n] x` indexed by natural numbers: `lfpApprox` is indexed by arbitrary ordinals and takes suprema at limit stages, making it strictly more general than simple Nat-indexed iteration.