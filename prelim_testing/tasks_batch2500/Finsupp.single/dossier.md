## Object

`VTask.single a b` is the finitely supported function from `α` to `M` (a type equipped with a zero) that equals `b` at the single point `a` and is `0` everywhere else. Its support — the finite set of points where it is nonzero — is `{a}` when `b ≠ 0`, and empty when `b = 0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.single : {α : Type u_1} -> {M : Type u_5} -> [Zero M] -> (a : α) -> (b : M) -> α →₀ M
<!-- PINNED-SIGNATURE:END -->


`VTask.single : {α : Type u_1} -> {M : Type u_5} -> [Zero M] -> (a : α) -> (b : M) -> α →₀ M`

The type `α` is the domain of the finitely supported function; it is inferred implicitly. The type `M` is the codomain, which must carry a zero element (supplied via the `[Zero M]` instance). The explicit argument `a : α` is the distinguished point at which the function takes a potentially nonzero value. The explicit argument `b : M` is the value assigned at `a`.

## Conventions

When `b = 0`, the support is empty and the function is the zero finitely supported function, even though `a` is still supplied as an argument; the element `a` is silently dropped from the support in this degenerate case.

## Worked examples

- Claim: For `a : Fin 3` equal to `1` and `b : ℕ` equal to `5`, evaluating `VTask.single a b` at `a` returns `5`.

- Claim: For any `α` and any `a : α`, `VTask.single a (0 : ℕ)` has empty support.

- Claim: For `a b : Fin 5` with `a ≠ b`, evaluating `VTask.single a (3 : ℕ)` at `b` returns `0`.

- Claim: The support of `VTask.single (a : ℕ) (7 : ℕ)` equals `{a}`.

## Boundaries

- **`b = 0`:** The support becomes `∅` regardless of `a`. The resulting finitely supported function is identically zero; `a` plays no role in the output.
- **`b ≠ 0`:** The support is exactly `{a}`, a singleton, and the function equals `b` at `a` and `0` at every other point.
- **Evaluation at `a` when `b = 0`:** Returns `0`, consistently with the support being empty.
- **`α` a singleton type:** `VTask.single a b` is still well-formed; the only point is `a` itself, so the function is everywhere `b` (or everywhere `0` if `b = 0`).

## Not to be confused with

- **The indicator function / characteristic function:** Those are `{0,1}`-valued; `VTask.single` takes an arbitrary value `b : M` at `a`.
- **`Finsupp.update f a b`:** That modifies an existing finitely supported function `f` at `a`; `VTask.single` always starts from the zero function.
- **`Pi.single a b`:** That is a plain function `α → M` (no finiteness condition on the support), whereas `VTask.single a b` packages the support and the function together into an `α →₀ M`.