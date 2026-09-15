## VTask.Supports

### Object

`VTask.Supports M S` is a proposition about a TM2 (two-stack Turing machine) program `M` and a finite set of states `S`. It asserts two things simultaneously: (1) the default/initial state is a member of `S`, and (2) every state `q` that belongs to `S` has its associated instruction `M q` "supported by" `S` — meaning that every control-flow jump reachable within `M q` targets only states that are also in `S`. Informally, `S` is a closed, reachable subset of the machine's state space that includes the starting state.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Supports : {K : Type u_1} -> {Γ : K → Type u_2} -> {Λ : Type u_3} -> {σ : Type u_4} -> [Inhabited Λ] -> (M : Λ → Turing.TM2.Stmt Γ Λ σ) -> (S : Finset Λ) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.Supports : {K : Type u_1} -> {Γ : K → Type u_2} -> {Λ : Type u_3} -> {σ : Type u_4} -> [Inhabited Λ] -> (M : Λ → Turing.TM2.Stmt Γ Λ σ) -> (S : Finset Λ) -> Prop
```

- `K` is the type indexing the stack alphabet family.
- `Γ` assigns a stack alphabet type to each stack index.
- `Λ` is the type of machine states (labels), which must be `Inhabited` so that a canonical default/initial state exists.
- `σ` is the type of the machine's variable or input/output data.
- `M` is the TM2 program, mapping each state label to a machine statement (instruction).
- `S` is the finite set of state labels being claimed to form a closed, supported subset of the state space.

### Conventions

The `Inhabited Λ` instance is used to extract the default state, which must belong to `S`; there is no special junk value for states outside `S` — the predicate simply requires every state in `S` to jump only within `S`, but makes no claim about states outside `S`.

### Worked examples

- Claim: For a machine whose single state is the default state and whose instruction never jumps to any other state, `VTask.Supports M {default}` holds, because the default is in the singleton set and the instruction supports the set.

- Claim: If `VTask.Supports M S` holds and a machine step takes a configuration with its current state label in `S` to a new configuration, then the new configuration's state label also lies in `Finset.insertNone S` (i.e., is either `none`/halted or a state in `S`). This is the content of the step-preservation theorem.

- Claim: If `VTask.Supports M S` holds and `q` appears among the reachable sub-statements enumerated from states in `S`, then `q` itself supports `S` (all jumps within `q` stay in `S`).

### Boundaries

- When `S` is the empty set (`∅`), `VTask.Supports M ∅` is always **false**, because the condition `default ∈ ∅` fails.
- When every state in `Λ` is in `S` (i.e., `S` covers all labels), the second condition is automatically satisfied for any machine `M`, provided the first condition holds — which it does since `default` is in `S`.
- The predicate says nothing about states **outside** `S`; those may jump arbitrarily, and no constraint is imposed on them.
- The `Inhabited` instance is required; without a notion of default state, the first condition (`default ∈ S`) would be ill-formed.

### Not to be confused with

- `Turing.TM2.SupportsStmt S q`: the per-statement version, asserting that a single instruction `q` only jumps within `S`; `VTask.Supports` applies this globally to all states in `S` and also requires `default ∈ S`.
- `Turing.TM1.Supports` or analogous predicates for TM1/TM0 machines: similar concepts but for different Turing machine models in Mathlib, not the two-stack (TM2) variant.
- Reachability of states: `VTask.Supports M S` asserts closure of `S` under the jump relation of `M`, but does **not** assert that all states in `S` are reachable from the initial configuration.