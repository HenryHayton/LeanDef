## VTask.IsReflection

### Object

Given a Coxeter system `cs` presenting a group `W` via a Coxeter matrix `M` over an index type `B`, an element `t` of `W` is called a **reflection** of that Coxeter system if `t` is conjugate (within `W`) to some simple reflection. Concretely, `t` is a reflection when there exist a group element `w ∈ W` and an index `i ∈ B` such that `t = w · sᵢ · w⁻¹`, where `sᵢ` denotes the simple reflection corresponding to the generator indexed by `i`. This is the standard notion of a reflection in the theory of Coxeter groups: the reflections form the analogue of all hyperplane reflections in a real reflection group, generalising the simple reflections (which are the generators themselves).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsReflection : {B : Type u_1} -> {W : Type u_2} -> [Group W] -> {M : CoxeterMatrix B} -> (cs : CoxeterSystem M W) -> (t : W) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit argument `B` is the index type parametrising the generators (nodes of the Coxeter diagram). The implicit argument `W` is the underlying group, which must carry a `Group` instance. The implicit argument `M` is the Coxeter matrix encoding the orders of products of pairs of generators. The explicit argument `cs` is the Coxeter system, which packages together `M`, `W`, and the data making `W` a realisation of the Coxeter group presented by `M`. The explicit argument `t` is the element of `W` whose status as a reflection is being tested.

### Conventions

The simple reflections themselves are reflections: taking `w = 1` (the identity) witnesses that every generator `sᵢ` satisfies `sᵢ = 1 · sᵢ · 1⁻¹`. No special junk values are declared, since the definition is a universally meaningful existential statement on a group.

### Worked examples

- Claim: Every simple reflection `s i` satisfies `VTask.IsReflection cs (cs.simple i)` — witnessed by taking `w = 1` and the given index `i`, since `1 · sᵢ · 1⁻¹ = sᵢ`.

- Claim: If `t` satisfies `VTask.IsReflection cs t` and `u ∈ W`, then `u * t * u⁻¹` also satisfies `VTask.IsReflection cs (u * t * u⁻¹)` — the set of reflections is closed under conjugation by arbitrary group elements, because if `t = w · sᵢ · w⁻¹` then `u · t · u⁻¹ = (u · w) · sᵢ · (u · w)⁻¹`.

- Claim: Every reflection `t` satisfying `VTask.IsReflection cs t` is an involution, i.e., `t * t = 1`, since each simple reflection `sᵢ` is an involution and involutions are preserved under conjugation.

### Boundaries

- If the index type `B` is empty (no generators), then there are no simple reflections and hence no reflections at all; `VTask.IsReflection cs t` is `False` for every `t`.
- The identity element `1 ∈ W` is **not** a reflection (except in the trivial Coxeter system where a generator has order 1, which is excluded by standard Coxeter matrix conventions requiring off-diagonal entries ≥ 2 and diagonal entries = 1), since simple reflections have order 2 and conjugation preserves order.
- Reflections are always their own inverses (`t⁻¹ = t`), but the converse fails: not every involution in `W` need be a reflection.

### Not to be confused with

- **Simple reflection** (`cs.simple i`): a simple reflection is a special case of a reflection (with conjugating element `w = 1`); not every reflection is simple.
- **`IsReflection` for a generic group action on a vector space**: in the linear-algebraic setting, a reflection is defined by its eigenvalue structure; the Coxeter-system notion here is purely group-theoretic and makes no reference to any vector space or eigenvalues.
- **`CoxeterSystem.IsSimpleReflection`** (if it exists): would single out only the generators `sᵢ` themselves, a strictly smaller class than all reflections.