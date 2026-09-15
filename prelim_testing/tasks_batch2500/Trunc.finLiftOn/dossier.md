## Object

`VTask.finLiftOn` extracts a well-defined value of type `β` from a family of truncated types. Given, for each index `i` in a finite type `ι`, a term `q i : Trunc (α i)` (a non-empty type whose elements are identified), and a function `f` from a concrete section `(∀ i, α i)` to `β` that assigns the same value to every such section, `VTask.finLiftOn` produces the unique element of `β` that `f` would yield on any representative section. In other words, it uses the finiteness of `ι` to simultaneously pick representatives from all the truncated fibres and apply `f`, and the condition `h` guarantees the result is independent of which representatives are chosen.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finLiftOn : {ι : Type u_1} -> [DecidableEq ι] -> [Fintype ι] -> {α : ι → Sort u_2} -> {β : Sort u_3} -> (q : (i : ι) → Trunc (α i)) -> (f : ((i : ι) → α i) → β) -> (h : ∀ (a b : (i : ι) → α i), f a = f b) -> β
<!-- PINNED-SIGNATURE:END -->


VTask.finLiftOn : {ι : Type u_1} -> [DecidableEq ι] -> [Fintype ι] -> {α : ι → Sort u_2} -> {β : Sort u_3} -> (q : (i : ι) → Trunc (α i)) -> (f : ((i : ι) → α i) → β) -> (h : ∀ (a b : (i : ι) → α i), f a = f b) -> β

The implicit type `ι` is the finite index type over which the family is indexed. The `DecidableEq` and `Fintype` instances supply the decidable equality and finiteness structure needed to enumerate all indices. The implicit dependent type `α` assigns a type to each index. The implicit type `β` is the codomain into which the result lands. The argument `q` is the family of truncated values: for each index `i`, `q i` is an element of `Trunc (α i)`, packaging the non-empty type `α i` without exposing a canonical representative. The argument `f` is the function to be lifted: it takes a concrete global section (a choice of one element from each `α i`) and returns a value in `β`. The argument `h` is the proof that `f` is constant on all global sections, i.e., that the output of `f` is independent of which representatives are chosen — this is what makes the lift well-defined.

## Conventions

When `ι` is an empty type (`IsEmpty ι`), there is exactly one section of `α` (the empty section), so the result equals `f` applied to the canonical empty section provided by the `IsEmpty` instance, regardless of what `q` is.

## Worked examples

- Claim: When every `q i` is `Trunc.mk (a i)` for a concrete section `a`, then `VTask.finLiftOn (fun i => Trunc.mk (a i)) f h = f a` (the beta-reduction / `finLiftOn_mk` equation).

- Claim: For `ι = Fin 0` (the empty finite type), `VTask.finLiftOn q f h` equals `f (Fin.elim0)` for any `q`, `f`, and `h`, since there is only one section of any family over the empty type.

- Claim: For `ι = Unit`, `α _ = ℕ`, `q _ = Trunc.mk 3`, and `f s = s ()`, the result is `3`, since the only meaningful representative is `3` and `f` simply evaluates the section at the unique index.

## Boundaries

- When `ι` is empty, the result is fully determined by `f` alone (applied to the empty/absurd section); the argument `q` plays no role.
- The condition `h` is essential: without requiring `f a = f b` for all sections `a` and `b`, the result would depend on the internal (non-canonical) representative hidden inside each `Trunc (α i)`, making the lift ill-defined.
- The function is defined for any `Fintype ι`, including singleton types, two-element types, etc.; each case works by simultaneously choosing representatives across all indices.
- There is no restriction on `β`; it can be any `Sort`, including `Prop`.

## Not to be confused with

- `Trunc.lift` (or `Trunc.liftOn`): lifts a function out of a single `Trunc α`, not a family of truncations indexed by a finite type.
- `Quotient.finLiftOn`: the analogous lifting operation for families of `Quotient` types (setoid quotients) rather than `Trunc` types; `VTask.finLiftOn` is specifically for `Trunc`.
- `Trunc.rec` / `Trunc.recOn`: recursors for a single `Trunc`, which require the target to be a `Prop` or a subsingleton; `VTask.finLiftOn` instead imposes constancy of `f` to handle an arbitrary codomain `β`.