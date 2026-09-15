## Object

`VTask.ofEq` takes an equivariant map `f : X →ₑ[φ] Y` — a map between sets with scalar multiplications that intertwines the scalar actions via the function `φ : M → N` — and reindexes it along a proof that `φ` equals another function `φ' : M → N`, producing an equivariant map `X →ₑ[φ'] Y` with the same underlying set-map. In short, it lets you replace the "scalar-intertwining" function in the type of an equivariant map by any provably equal function.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofEq : {M : Type u_2} -> {N : Type u_3} -> {φ : M → N} -> {X : Type u_5} -> [SMul M X] -> {Y : Type u_6} -> [SMul N Y] -> {φ' : M → N} -> (h : φ = φ') -> (f : X →ₑ[φ] Y) -> X →ₑ[φ'] Y
<!-- PINNED-SIGNATURE:END -->


`VTask.ofEq : {M : Type u_2} -> {N : Type u_3} -> {φ : M → N} -> {X : Type u_5} -> [SMul M X] -> {Y : Type u_6} -> [SMul N Y] -> {φ' : M → N} -> (h : φ = φ') -> (f : X →ₑ[φ] Y) -> X →ₑ[φ'] Y`

The implicit arguments `M` and `N` are the monoids (or types) of scalars acting on the source and target, respectively. `φ` is the original scalar-intertwining function with which `f` is equivariant, and `φ'` is the new scalar-intertwining function that appears in the output type. The `SMul` instances supply the scalar-multiplication structures on `X` and `Y`. The explicit argument `h` is the proof that `φ = φ'`; it is the sole justification for the type-change. The argument `f` is the source equivariant map, typed with `φ`, that is being reindexed.

## Conventions

No junk-value or boundary conventions are declared: the function is defined for all inputs without restriction, and its output is always the unique equivariant map with underlying function equal to that of `f`.

## Worked examples

- Claim: For any equivariant map `f : X →ₑ[φ] Y` and proof `h : φ = φ`, the result `f.ofEq h` applied to any element `a : X` equals `f a`.

- Claim: The underlying function of `VTask.ofEq h f` equals the underlying function of `f`, regardless of which equal scalar map `φ'` is chosen via `h`.

- Claim: When `φ'` is definitionally `φ` and `h` is `rfl`, the map `VTask.ofEq rfl f` behaves identically to `f` on every input.

## Boundaries

- When `h : φ = φ` is `rfl` (reflexivity), the construction is a no-op: the resulting map has exactly the same underlying function and the same equivariance proof as the original. There is no degenerate or undefined case here.
- The construction makes no assumption about `M`, `N`, `X`, or `Y` beyond the existence of scalar multiplications; in particular `M` and `N` need not be groups.
- Since the result's underlying function is always definitionally equal to `f`'s underlying function (as witnessed by `ofEq_apply`), no information about `f` is lost or modified; only the type annotation changes.

## Not to be confused with

- `MulActionHom.comp`: composition of two equivariant maps, which changes the underlying function rather than merely retyping it.
- The identity equivariant map `MulActionHom.id`: it is the map where `X = Y`, `φ = id`, and the function is the identity, whereas `VTask.ofEq` transports any existing map along an equality.
- Coercion / `MulActionHom.toFun`: this extracts the underlying bare function from an equivariant map, while `VTask.ofEq` produces a new equivariant map with the scalar-intertwining function changed in the type.
