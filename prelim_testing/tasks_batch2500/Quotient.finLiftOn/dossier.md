## Object

`VTask.finLiftOn` evaluates a function `f` on a finite dependent product of quotient types. Given, for each index `i` in a finite type `ι`, a quotient element `q i ∈ Quotient (S i)`, it produces a value of type `β` by first choosing a canonical section (a representative family `a : ∀ i, α i`) and then applying `f` to it. The result is well-defined because `h` guarantees that `f` is constant on equivalence classes: if two families agree modulo the respective setoid relations, they yield the same value under `f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finLiftOn : {ι : Type u_1} -> [Fintype ι] -> [DecidableEq ι] -> {α : ι → Sort u_2} -> {S : (i : ι) → Setoid (α i)} -> {β : Sort u_3} -> (q : (i : ι) → Quotient (S i)) -> (f : ((i : ι) → α i) → β) -> (h : ∀ (a b : (i : ι) → α i), (∀ (i : ι), a i ≈ b i) → f a = f b) -> β
<!-- PINNED-SIGNATURE:END -->


`VTask.finLiftOn : {ι : Type u_1} -> [Fintype ι] -> [DecidableEq ι] -> {α : ι → Sort u_2} -> {S : (i : ι) → Setoid (α i)} -> {β : Sort u_3} -> (q : (i : ι) → Quotient (S i)) -> (f : ((i : ι) → α i) → β) -> (h : ∀ (a b : (i : ι) → α i), (∀ (i : ι), a i ≈ b i) → f a = f b) -> β`

- `ι` is the finite index type over which the product is taken; it is required to be a `Fintype` (there are only finitely many indices) and have `DecidableEq` (indices can be compared for equality).
- `α` is a family of types, one for each index; the quotient is built over these types.
- `S` assigns a setoid (an equivalence relation) to each fibre `α i`.
- `β` is the target type of the lifted function.
- `q` is the family of quotient elements being evaluated: for each `i`, `q i` is an element of the quotient of `α i` by `S i`.
- `f` is the function to be lifted: it takes a choice of representative for every index and returns a value in `β`.
- `h` is the well-definedness proof: it asserts that if two representative families are pointwise equivalent (each `a i ≈ b i`), then `f` gives the same result on both.

## Conventions

There are no junk-value or out-of-domain conventions because the function is total and every argument is fully constrained by its type: `h` is required as a proof, and the finiteness + decidability hypotheses are type-class arguments that Lean fills automatically.

## Worked examples

- Claim: When every `q i` is the equivalence class of some representative family `a`, `VTask.finLiftOn (⟦a ·⟧) f h` reduces to `f a`.
  This is the content of `Quotient.finLiftOn_mk`: the lifted function evaluated at a family of canonical classes `⟦a i⟧` equals `f a`.

- Claim: When `ι` is empty, `VTask.finLiftOn q f h` equals `f (IsEmpty.elim · )` regardless of what `q` is, because there is only one function out of an empty type.
  This is the content of `Quotient.finLiftOn_empty`: the empty-index case always returns `f` applied to the unique map from the empty type.

- Claim: For `ι = Fin 1`, `S 0 = ⟨(· = ·), …⟩` (the discrete setoid on `ℕ`), `q 0 = ⟦3⟧`, and `f a = a 0 + 1`, evaluating `VTask.finLiftOn q f h` yields `4`.

- Claim: Well-definedness is essential: if `a i ≈ b i` for all `i`, then `VTask.finLiftOn (fun i => ⟦a i⟧) f h = VTask.finLiftOn (fun i => ⟦b i⟧) f h` by applying `h`.

## Boundaries

- **Empty index type**: If `ι` is empty (`IsEmpty ι`), there is exactly one function `ι → _`, so `f` is called on the unique map `IsEmpty.elim`. The quotient family `q` is irrelevant in this case.
- **Singleton index type**: For `ι = Fin 1` (or any one-element type), the construction reduces to a single ordinary quotient lift.
- **Equivalence class representatives**: The output does not depend on which representative is chosen within any equivalence class; `h` ensures all representatives give the same value.
- **Non-propositional β**: The target `β` is a `Sort`, so this works for both data and propositions, not just propositions.

## Not to be confused with

- `Quotient.liftOn` — the single-quotient version; lifts a function on one quotient rather than a finite product of quotients.
- `Quotient.finLift` — a related combinator that takes the representative family as an explicit function argument and produces a function on quotients, rather than evaluating directly.
- `Quotient.choice` / `Quotient.finChoice` — the internal mechanism that selects a canonical representative family; `VTask.finLiftOn` builds on this but hides it behind the well-definedness proof.
