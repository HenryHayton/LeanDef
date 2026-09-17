## VTask.emptyOn

### Object

`VTask.emptyOn α` is the unique matroid on the type `α` whose ground set is the empty set. Because the ground set is empty, the only independent set and the only base is the empty set itself. Its rank is zero, and it contains no elements whatsoever. Every matroid on a type `α` is either equal to `VTask.emptyOn α` or has a nonempty ground set.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.emptyOn : (α : Type u_2) -> Matroid α
<!-- PINNED-SIGNATURE:END -->


The single argument `α` is the ambient type over which the matroid is defined. It specifies the universe of potential elements, even though none of them belong to the ground set of this particular matroid.

### Conventions

There are no junk-value or boundary conventions to declare: `VTask.emptyOn` is a total function defined for every type `α`, and its behaviour is entirely uniform — the ground set is always empty, the rank is always zero, and the only base and the only independent set is the empty set.

### Worked examples

- Claim: The ground set of `VTask.emptyOn α` is the empty set for any type `α`.

- Claim: The extended rank of `VTask.emptyOn α` equals `0`.

- Claim: For any type `α`, every matroid on `α` is either equal to `VTask.emptyOn α` or has a nonempty ground set.

- Claim: A matroid `M : Matroid α` satisfies `M.E = ∅` if and only if `M = VTask.emptyOn α`.

- Claim: If `α` is an empty type, then every matroid on `α` equals `VTask.emptyOn α`.

### Boundaries

- When `α` itself is the empty type (`IsEmpty α`), then `VTask.emptyOn α` is the only matroid on `α`, and any matroid on `α` is definitionally equal to it.
- When `α` is nonempty, `VTask.emptyOn α` is still well-defined; the ground set is empty even though the type has elements. Those elements simply do not belong to the matroid.
- The empty set is simultaneously the unique base and the unique independent set of `VTask.emptyOn α`.
- The rank (and extended rank) of `VTask.emptyOn α` is `0`, since the largest independent set has cardinality zero.

### Not to be confused with

- `Matroid.freeOn`: The matroid on a given set where every subset of the ground set is independent (the "free" matroid), which has a nonempty ground set whenever the set is nonempty.
- `Matroid.loopyOn`: The matroid where every element is a loop (the only independent set is still the empty set, but the ground set may be nonempty).
- `Matroid.Nonempty`: A predicate asserting that a matroid has a nonempty ground set, which is precisely the negation of being equal to `VTask.emptyOn`.