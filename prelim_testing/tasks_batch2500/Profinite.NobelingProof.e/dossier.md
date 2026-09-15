## Object

`VTask.e C i` is the indicator function for the `i`-th coordinate being `true`, viewed as a locally constant map from the subspace `C ⊆ (I → Bool)` (equipped with the subspace topology) to the integers `ℤ`. Concretely, it sends a Boolean-valued function `f : C` to `1` if `f i = true`, and to `0` if `f i = false`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.e : {I : Type u} -> (C : Set (I → Bool)) -> (i : I) -> LocallyConstant ↑C ℤ
<!-- PINNED-SIGNATURE:END -->


`VTask.e : {I : Type u} -> (C : Set (I → Bool)) -> (i : I) -> LocallyConstant ↑C ℤ`

The implicit argument `I` is the index type that parameterises the Boolean-valued functions in the ambient space `I → Bool`. The explicit argument `C` is a subset of `I → Bool` that forms the domain of the locally constant function (given the subspace topology inherited from the product of discrete spaces). The argument `i` is the coordinate index whose value is being tested: `e C i` evaluates the Boolean at position `i` in each element of `C`.

## Conventions

The codomain is `ℤ` (the integers), not `Bool` or `{0,1}`: the indicator takes the integer value `1` for `true` and `0` for `false`. There are no junk-value conventions declared for this definition beyond the universal totality of the `if–then–else` expression.

## Worked examples

- Claim: For the full space `C = Set.univ : Set (Fin 3 → Bool)` and index `i = 0`, the function `VTask.e Set.univ 0` sends any `f` with `f 0 = true` to `1`.

- Claim: For the full space `C = Set.univ : Set (Fin 3 → Bool)` and index `i = 1`, the function `VTask.e Set.univ 1` sends any `f` with `f 1 = false` to `0`.

- Claim: For `C = {f : Fin 1 → Bool | True}` and `i = ⟨0, by omega⟩`, `(VTask.e Set.univ i).toFun ⟨fun _ => true, trivial⟩ = 1` — the function returns `1` for the all-`true` element.

- Claim: `Products.eval C ⟨a :: l, hla⟩ = (VTask.e C a) * Products.eval C ⟨l, _⟩` (the `evalCons` factorisation), expressing that the evaluation of a product indexed by `a :: l` factors as the indicator `e C a` times the evaluation of the shorter product.

## Boundaries

- When `C` is empty (the empty subspace), `VTask.e C i` is a locally constant function on the empty space; it exists and is well-typed, but has no inputs to evaluate on.
- The function is total over all elements of `C` and all indices `i : I`; there is no partial-definition issue because `Bool` has exactly two values and the `if–then–else` covers both.
- When `f i = true`, the output is exactly `1 : ℤ`; when `f i = false`, the output is exactly `0 : ℤ`. There is no third case.
- The local constancy holds because the topology on `I → Bool` is the product of discrete topologies, so evaluation at any coordinate is continuous.

## Not to be confused with

- `Products.eval C l` — the evaluation of an entire *list* of indices (a monomial), which is a product of several `e C i` terms rather than a single indicator.
- The characteristic function of a subset of `C` — `VTask.e C i` is the characteristic function of the *coordinate hyperplane* `{f ∈ C | f i = true}` inside `C`, not the indicator of an arbitrary subset.
- The canonical basis elements of a free module — while `e C i` spans parts of the module `LocallyConstant C ℤ`, it is a function on a topological space, not an abstract basis vector indexed by `I`.
