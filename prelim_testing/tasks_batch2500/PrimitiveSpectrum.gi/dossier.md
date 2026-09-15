## Object

Given a complete lattice `α` and a subset `T` of `α` that *order-generates* `α` (meaning every element of `α` is an infimum of elements drawn from `T`), `VTask.gi` constructs a **Galois insertion** between

- the poset of subsets of `T` (the *primitive spectrum* side), and  
- the opposite order of `α` (written `αᵒᵈ`).

Concretely, the left adjoint sends a subset `S ⊆ T` to the *kernel* of `S` — the infimum in `α` of all elements of `S` — viewed in the opposite order; the right adjoint sends an element `a : α` (presented in the opposite order) to the *hull* of `a` relative to `T` — the set of all members of `T` that are ≥ `a`.

The Galois-insertion structure says that the left adjoint is left-inverse to the right adjoint (i.e. `kernel (hull T a) = a` for all `a`), and that this pair is monotone and satisfies the full adjunction inequality. The key point distinguishing a Galois *insertion* from a mere Galois *connection* is that the unit of the adjunction is an identity: applying hull then kernel recovers the original element exactly, not merely a weaker version of it.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.gi : {α : Type u_1} -> [CompleteLattice α] -> {T : Set α} -> (hG : PrimitiveSpectrum.OrderGenerates T) -> GaloisInsertion (⇑OrderDual.toDual ∘ PrimitiveSpectrum.kernel) (PrimitiveSpectrum.hull T ∘ ⇑OrderDual.ofDual)
<!-- PINNED-SIGNATURE:END -->


The implicit argument `α` is the underlying complete lattice whose elements are being studied. The instance `[CompleteLattice α]` supplies the lattice structure needed to form arbitrary infima. The implicit argument `T` is the distinguished subset of `α` serving as the primitive spectrum — the collection of "prime-like" elements. The explicit argument `hG` is the proof that `T` order-generates `α`, i.e. every element of `α` can be expressed as an infimum of a subset of `T`; this hypothesis is exactly what promotes the Galois connection to a Galois insertion.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a proof-carrying structure (a `GaloisInsertion` term), not a partial function, and is simply not constructed when the hypothesis `hG` does not hold.

## Worked examples

- Claim: For the complete lattice `α = Set X` (for some type `X`) with `T` being all principal filters (which order-generates `Set X`), the Galois insertion produced by `VTask.gi` has the property that the counit is the identity, i.e., `kernel (hull T a) = a` for every `a : Set X`.

- Claim: For `α` a complete Boolean algebra with `T = Set.univ` (which trivially order-generates since every element equals the inf of its singleton), the resulting Galois insertion `VTask.gi hG` satisfies `(VTask.gi hG).le_l_u s` for every subset `s : Set T`, witnessing the hull-kernel roundtrip inequality that is part of the insertion data.

- Claim: When `T` order-generates `α`, the closure operator on subsets of `T` determined by `VTask.gi hG` sends any `S : Set T` to `hull T (kernel S)`, the hull of the kernel of `S`.

## Boundaries

- If `T` did *not* order-generate `α`, one could still form the underlying Galois *connection* (`gc`), but one could not generally promote it to an insertion; the hypothesis `hG` is essential and not removable.
- When `T = ∅`, the kernel of any subset of `T` is the top element `⊤` of `α` (an empty infimum), and the hull of `⊤` is `∅`; the insertion degenerates trivially but is still well-formed given a proof of `hG`.
- When `T` contains every element of `α`, the hull and kernel are essentially inverse operations and the insertion is very tight.
- The construction is purely order-theoretic; no topology on `T` or `α` is assumed. Topological consequences (e.g., that closed sets are exactly hulls) require additional hypotheses and are not part of this definition.

## Not to be confused with

- `PrimitiveSpectrum.gc` — the underlying Galois *connection* between subsets of `T` and `αᵒᵈ`; `VTask.gi` is the strengthening of this to a Galois *insertion*, requiring the extra order-generating hypothesis.
- `PrimitiveSpectrum.hull` — the individual right-adjoint function sending `a : α` to the set `{p ∈ T | a ≤ p}`; `VTask.gi` packages both hull and kernel together as an adjoint pair with proof of the insertion property.
- `GaloisConnection` — a weaker notion than `GaloisInsertion`; a Galois connection only guarantees the adjunction inequalities, whereas a Galois insertion additionally requires that one of the round-trip composites is the identity.
