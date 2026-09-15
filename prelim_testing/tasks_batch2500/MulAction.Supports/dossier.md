## VTask.Supports

### Object

Given a group (or monoid) `G` acting on two types `α` and `β`, a set `s ⊆ α` *supports* an element `b : β` if every group element that fixes every point of `s` also fixes `b`. Intuitively, the "behaviour" of `b` under the action of `G` is entirely determined by what happens on `s`: if you cannot distinguish any element of `s` from itself via a group element `g`, then `g` cannot move `b` either.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Supports : (G : Type u_1) -> {α : Type u_3} -> {β : Type u_4} -> [SMul G α] -> [SMul G β] -> (s : Set α) -> (b : β) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.Supports : (G : Type u_1) -> {α : Type u_3} -> {β : Type u_4} -> [SMul G α] -> [SMul G β] -> (s : Set α) -> (b : β) -> Prop
```

`G` is the group (or any type equipped with a scalar multiplication) whose elements act on both `α` and `β`. The implicit types `α` and `β` are the carrier types being acted upon: `α` is the type containing the supporting set, and `β` is the type containing the element being supported. The instance arguments `[SMul G α]` and `[SMul G β]` supply the two scalar-multiplication structures. The explicit argument `s` is the supporting set — a subset of `α` whose pointwise stabiliser is being considered. The explicit argument `b` is the element of `β` whose stabilisation is being asserted.

### Conventions

There are no declared junk-value or edge-case conventions for this definition: `VTask.Supports` is a universally quantified `Prop` that is well-formed for any set `s` (including the empty set) and any element `b`, so no special sentinel values or out-of-domain conventions arise.

### Worked examples

- Claim: If `a ∈ s`, then `s` supports `a` (under any `G`-action). That is, any element of `s` is supported by `s` itself, because any `g` fixing all of `s` in particular fixes `a`.

- Claim: If `s ⊆ t` and `s` supports `b`, then `t` also supports `b`. Any group element that fixes all of `t` certainly fixes all of `s`, so the hypothesis applies and `g • b = b` follows.

- Claim: The empty set `∅ ⊆ α` supports `b : β` if and only if every `g : G` satisfies `g • b = b` (i.e., `b` lies in the fixed-point set of the entire action). This is because the condition "g fixes every element of ∅" is vacuously true for every `g`.

- Claim: If `s` supports `b` and `g : H` acts on both `α` and `β` (compatibly), then `g • s` supports `g • b`.

### Boundaries

- **Empty supporting set**: `VTask.Supports G ∅ b` holds if and only if every `g : G` fixes `b`, since the premise "g fixes every point of ∅" is vacuously satisfied by every `g`.
- **Full supporting set**: `VTask.Supports G Set.univ b` holds trivially for every `b`, since any `g` that fixes every element of the entire type `α` in particular fixes `b` (the premise is very strong and the conclusion follows from `supports_of_mem` combined with monotonicity, or directly).
- **Monotonicity**: Enlarging the supporting set can only preserve (never destroy) the `Supports` relation — a larger set imposes a stronger premise on `g` and thus makes the universal statement easier to satisfy.
- **Type generality**: The definition requires no group axioms beyond the existence of the `SMul` operation; it applies to arbitrary scalar multiplications, not just group actions.

### Not to be confused with

- **`MulAction.fixedPoints` / `MulAction.stabilizer`**: These record which elements or group elements are globally fixed, rather than asking which sets "control" the orbit of a specific element.
- **`MulAction.support` (of a permutation or function)**: The support of a permutation is the set of points it *moves*, which is conceptually the opposite of a supporting set in the `VTask.Supports` sense.
- **`Function.support`**: The support of a function `f : α → β` (where `β` has a zero) is `{x | f x ≠ 0}`, a completely different notion unrelated to group actions.