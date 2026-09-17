## 1. Object

`VTask.cast` produces a type equivalence (`≃`) between two types that are known to be propositionally equal. Given a proof that `α = β`, it packages the canonical coercion between `α` and `β` (and its inverse, coercion along the reversed equality) into a fully-verified `Equiv` structure, showing that coercing back and forth in either direction is the identity.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cast : {α β : Sort u_1} -> (h : α = β) -> α ≃ β
<!-- PINNED-SIGNATURE:END -->


```
VTask.cast : {α β : Sort u_1} -> (h : α = β) -> α ≃ β
```

The implicit arguments `α` and `β` are the two types (or sorts) being related; they are inferred from context. The explicit argument `h` is a proof that `α` and `β` are propositionally equal — it witnesses why the coercion is valid. The result is an equivalence whose forward function coerces from `α` to `β` and whose inverse coerces back from `β` to `α`.

## 3. Conventions

There are no junk-value conventions to declare: the definition is total, and every proof of `α = β` (including `rfl` when `α` and `β` are definitionally the same type) yields a well-formed equivalence. The symmetry of the equivalence corresponds exactly to the symmetry of the equality proof, and composition of two such equivalences corresponds to transitivity of the equality proofs.

## 4. Worked examples

- Claim: `VTask.cast rfl` applied to a value `x : Nat` gives back `x` (the forward function of the equivalence built from `rfl : Nat = Nat` is the identity on `Nat`).

- Claim: The symmetry of `VTask.cast h` equals `VTask.cast h.symm`; that is, `(VTask.cast h).symm = VTask.cast h.symm` for any `h : α = β`.

- Claim: Composing `VTask.cast h` with `VTask.cast h2` (where `h : α = β` and `h2 : β = γ`) yields the same equivalence as `VTask.cast (h.trans h2)`; that is, `VTask.cast (h.trans h2) = (VTask.cast h).trans (VTask.cast h2)`.

- Claim: For `h : α = β`, applying the forward direction of `VTask.cast h` to an element `a : α` yields a value in `β` that is heterogeneously equal to `a`.

## 5. Boundaries

- When `h` is `rfl` (i.e., `α = α`), the resulting equivalence is the identity equivalence: both directions simply return their argument unchanged.
- The definition is total: it is valid for any universe level and for any sort (not just `Type`), so it applies to propositions (`Prop`) as well as types.
- The equivalence respects the group-like structure of equality: symmetry of the equivalence matches symmetry of the equality proof, and transitivity of equivalences matches transitivity of equality proofs.
- When `α` and `β` coincide definitionally (not just propositionally), the coercion in each direction is still well-typed and behaves as the identity.

## 6. Not to be confused with

- `Equiv.refl α` — the identity equivalence on a single type; `VTask.cast rfl` is equal to `Equiv.refl α`, but `Equiv.refl` does not take an equality proof as input.
- `cast h x` (the bare term-level cast) — this applies the coercion to a single element, producing a value but not an `Equiv` structure with an inverse and proofs.
- `Equiv.ofEq` — another name used in some contexts for essentially the same construction; users should check which name is in scope in their Mathlib version.