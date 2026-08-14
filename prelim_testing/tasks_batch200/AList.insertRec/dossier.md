## VTask.insertRec

### Object

A recursion principle (and induction scheme) for association lists (`AList β`), which decomposes any such list into a sequence of `insert` steps from the empty list. It allows one to define a function — or prove a property — on every `AList` by specifying what to do on the empty list and how a single `insert` step transforms the result, subject to the guarantee that the newly inserted key is not already present in the rest of the list.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.insertRec : {α : Type u} -> {β : α → Type v} -> [DecidableEq α] -> {C : AList β → Sort u_1} -> (H0 : C ∅) -> (IH : (a : α) → (b : β a) → (l : AList β) → a ∉ l → C l → C (AList.insert a b l)) -> (l : AList β) -> C l
<!-- PINNED-SIGNATURE:END -->


`{α : Type u} -> {β : α → Type v} -> [DecidableEq α] -> {C : AList β → Sort u_1} -> (H0 : C ∅) -> (IH : (a : α) → (b : β a) → (l : AList β) → a ∉ l → C l → C (AList.insert a b l)) -> (l : AList β) -> C l`

- `α` is the type of keys; `β` is the type family of values indexed by keys.
- The `DecidableEq α` instance is required because `AList.insert` must decide key equality when deduplicating entries.
- `C` is the motive: a type (or sort) assigned to each association list, whose inhabitants are to be constructed.
- `H0` is the base case: a term of type `C ∅`, providing the result for the empty association list.
- `IH` is the inductive step: given a key `a`, a value `b` for that key, a sub-list `l` in which `a` does not appear, and the already-computed result for `l`, it produces a result for `l` extended by inserting `(a, b)`.
- `l` is the association list on which the recursion is performed.

### Conventions

The decomposition of `l` into `insert` steps is determined by the internal (key-deduplicated) list representation; the order of steps corresponds to the order in which entries appear in the underlying list. There are no junk-value conventions because the function is total over all `AList β`.

### Worked examples

- Claim: `VTask.insertRec H0 IH ∅ = H0` (the recursor applied to the empty list returns the base case).

- Claim: For any `l : AList β` and key `a` with `h : a ∉ l`, the recursor applied to `AList.insert a b l` equals `IH a b l h (VTask.insertRec H0 IH l)` (the recursor unfolds one insert step, consuming the inductive hypothesis).

- Claim: The recursor can be used to count the number of entries in an `AList`: instantiate `C` as the constant `ℕ`, `H0 := 0`, and `IH a b l _ n := n + 1`; the result equals `l.length`.

### Boundaries

- On the empty list `∅`, the recursor immediately returns `H0` without invoking `IH` at all.
- Each invocation of `IH` in the recursion receives a proof that the key being inserted is **not** already in the remainder, reflecting the no-duplicate-keys invariant of `AList`; this proof is internally derived and passed along automatically.
- Because `AList` enforces unique keys, the decomposition into insert steps is well-defined even though an association list could in principle be constructed from the same key-value pairs in different orders.
- The sort `u_1` in the motive `C` is unrestricted (it can be `Prop`, `Type`, `Sort`, etc.), so `insertRec` serves both as a recursion principle for defining functions and as an induction principle for proofs.

### Not to be confused with

- `AList.keys` / `AList.toList`: these destructure an `AList` into its underlying data without providing a recursion principle.
- `List.rec` or `List.recOn`: these are recursion principles for plain `List`, which do not carry the no-duplicate-key invariant and do not align with `AList.insert`.
- `Finset.induction`: a similar insert-based induction principle, but for finite sets (`Finset`) rather than typed key-value association lists.