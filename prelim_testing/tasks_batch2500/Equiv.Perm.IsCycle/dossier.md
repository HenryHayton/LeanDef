## Object

`VTask.IsCycle f` is the proposition that the permutation `f` is a *cycle* in the classical sense: `f` is not the identity, and there exists a single non-fixed point `x` such that every other non-fixed point of `f` can be reached from `x` by repeatedly applying `f` (i.e., all non-fixed points lie in the same orbit under `f`). Equivalently, the orbit of any non-fixed point under `f` is exactly the support of `f`, and that support is non-empty.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsCycle : {α : Type u_2} -> (f : Equiv.Perm α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsCycle : {α : Type u_2} -> (f : Equiv.Perm α) -> Prop`

The implicit type argument `α` is the underlying type being permuted. The explicit argument `f` is the permutation under scrutiny — the function (together with its inverse) that we are asking whether it constitutes a cycle.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a `Prop`-valued predicate, so the only relevant question is truth or falsity, and the definition is well-formed for every permutation on every type (including the identity, which is simply declared to be *not* a cycle by the non-fixedness requirement).

## Worked examples

- Claim: The transposition (swap) of two distinct elements of a three-element type is a cycle.

- Claim: The identity permutation on any non-empty type is **not** a cycle, because it has no non-fixed point.

- Claim: The map `n ↦ n + 1` on `ℤ` (i.e., `Equiv.addLeft 1 : Equiv.Perm ℤ`) is a cycle, since every integer is non-fixed and any integer can be reached from any other by repeated addition of 1.

- Claim: A permutation of a finite set whose order equals the cardinality of the set (and that cardinality is prime) must be a cycle.

## Boundaries

- **Identity permutation**: The identity is never a cycle. The definition requires the existence of at least one non-fixed point, which the identity lacks entirely.
- **Single-element type**: Any permutation on a one-element type is the identity, hence not a cycle.
- **Two-element type**: The unique non-identity permutation (the swap of the two elements) is a cycle; it has exactly two non-fixed points and each is reachable from the other by one application.
- **Infinite types**: `IsCycle` is perfectly meaningful for infinite types. For instance, the permutation `n ↦ n + 1` on `ℤ` is a cycle even though the type is infinite.
- **Powers of cycles**: A power `f^k` of a cycle `f` on a finite support of size `n` is itself a cycle if and only if `k` is coprime to `n`; otherwise it splits into multiple cycles and is not a cycle.
- **Non-identity with multiple orbits**: A permutation that moves points but whose non-fixed points fall into more than one orbit is **not** a cycle, even though it is not the identity.

## Not to be confused with

- `Equiv.Perm.IsCycleOn s`: A weaker/relativized notion — `f` acts as a cycle *on the set `s`* (all of `s` is a single orbit under `f`), without requiring that `s` be precisely the support of `f`.
- `Equiv.Perm.IsSwap`: The special case of a cycle of length exactly 2 (a transposition); every swap is a cycle, but not every cycle is a swap.
- `Equiv.Perm.SameCycle f x y`: The binary relation asserting that `x` and `y` lie in the same orbit under `f`; this is a component used *inside* the definition of `IsCycle`, not the cycle predicate itself.