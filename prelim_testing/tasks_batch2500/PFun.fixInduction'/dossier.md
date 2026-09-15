## Object

`VTask.fixInduction'` is a structural induction principle (recursion scheme) for the fixed-point membership predicate of a partial function. Given a partial function `f : α →. β ⊕ α` and a proof that some value `b : β` belongs to the fixed point `f.fix a` (i.e., iterating `f` from `a` eventually halts with the left-sum value `b`), it lets you prove that a predicate `C : α → Sort*` holds at the starting point `a`. It does so by case analysis along the iteration chain: either `f` immediately returns `b` at `a` (base case), or `f` steps to some intermediate `α`-value from which `b` is eventually reached (inductive case).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.fixInduction' : {α : Type u_1} -> {β : Type u_2} -> {C : α → Sort u_7} -> {f : α →. β ⊕ α} -> {b : β} -> {a : α} -> (h : b ∈ f.fix a) -> (hbase : (a_final : α) → Sum.inl b ∈ f a_final → C a_final) -> (hind : (a₀ a₁ : α) → b ∈ f.fix a₁ → Sum.inr a₁ ∈ f a₀ → C a₁ → C a₀) -> C a
<!-- PINNED-SIGNATURE:END -->


`VTask.fixInduction' : {α : Type u_1} -> {β : Type u_2} -> {C : α → Sort u_7} -> {f : α →. β ⊕ α} -> {b : β} -> {a : α} -> (h : b ∈ f.fix a) -> (hbase : (a_final : α) → Sum.inl b ∈ f a_final → C a_final) -> (hind : (a₀ a₁ : α) → b ∈ f.fix a₁ → Sum.inr a₁ ∈ f a₀ → C a₁ → C a₀) -> C a`

The type parameters `α` and `β` are the state type and the terminal-value type of the iteration. `C` is the motive predicate over states that one wishes to establish. `f` is the partial function being iterated: at each state it either terminates with a `β`-value (left summand) or steps to a new state (right summand). `b` is the specific terminal value that the iteration reaches, and `a` is the starting state. The argument `h` witnesses that iterating `f` from `a` indeed terminates at `b`. The argument `hbase` is the base case: it supplies a proof of `C a_final` for any state `a_final` at which `f` immediately returns `b`. The argument `hind` is the inductive step: given that `f` steps from `a₀` to `a₁` (via `Sum.inr a₁ ∈ f a₀`) and the iteration from `a₁` reaches `b`, and the inductive hypothesis `C a₁`, it produces `C a₀`.

## Conventions

There are no junk-value conventions for this definition: its inputs are fully constrained by the proof obligations, and the function is only well-typed when all hypotheses are genuinely satisfied. The sort `Sort u_7` subsumes both `Prop` (proofs) and `Type`-valued predicates, so the principle works uniformly for both proof-relevant and proof-irrelevant motives.

## Worked examples

- Claim: When `f a_final` immediately returns `Sum.inl b`, calling `VTask.fixInduction'` with the corresponding membership proof reduces to the base case handler `hbase` applied to `a_final` and the membership evidence. Formally, `VTask.fixInduction' h hbase hind = hbase a_final fa` whenever `fa : Sum.inl b ∈ f a_final` witnesses the immediate return (this is the content of the `fixInduction'_stop` computation rule).

- Claim: When `f a₀` steps to `Sum.inr a₁` (with `fa : Sum.inr a₁ ∈ f a₀`) and `h' : b ∈ f.fix a₁` witnesses that the iteration from `a₁` reaches `b`, calling `VTask.fixInduction'` on the composite proof `h` at `a₀` reduces to `hind a₀ a₁ h' fa (VTask.fixInduction' h' hbase hind)`. That is, the inductive-step handler is applied, and the result of recursing on the sub-problem at `a₁` is passed as the inductive hypothesis.

- Claim: If `b ∈ f.fix a` holds and `C` is the constantly-`True` predicate, then `VTask.fixInduction' h (fun _ _ => trivial) (fun _ _ _ _ ih => ih)` produces a proof of `C a`, illustrating that the trivially-propagating induction always succeeds.

## Boundaries

- The function is only defined (the term is well-typed) when the proof `h : b ∈ f.fix a` exists, which requires that the iteration chain from `a` under `f` is finite and terminates at `b`. If `f.fix a` is empty or contains only values other than `b`, there is no way to supply `h` and the principle does not apply.
- The inductive step `hind` receives *both* the forward membership `Sum.inr a₁ ∈ f a₀` *and* the recursive fixed-point membership `b ∈ f.fix a₁`, giving the user maximal information at each step.
- The principle is stated for any `Sort`, so it covers data-extraction tasks (where `C a` is a `Type`-valued computation) as well as pure proof obligations (where `C a` is a `Prop`).
- There is no explicit bound on the length of the iteration chain; termination is guaranteed by the well-foundedness argument buried in the definition of `PFun.fix`.

## Not to be confused with

- `PFun.fixInduction` (the simpler variant): that version provides a single induction step that exposes the raw `get`-value of `f a'`, without splitting into named base/inductive cases or providing the sub-problem membership `b ∈ f.fix a₁` in the step.
- `PFun.fix`: the actual fixed-point operator for partial functions, which this induction principle reasons *about* but does not itself compute.
- `WellFounded.recursion` / `Nat.rec`: general recursion/induction combinators; `VTask.fixInduction'` is specifically tailored to the iteration structure of `PFun.fix` and carries the domain witness `h` as an explicit argument.