## Object

`VTask.stabilizerEquiv_invFun` takes a family of permutations — one permutation of each fiber of a function `f : α → ι` — and an element `a : α`, and returns the element of `α` obtained by applying the fiber-permutation at `f a` to `a` (viewed as a point of the fiber over `f a`). Concretely, if `g i` permutes all elements of `α` that map to `i` under `f`, then `stabilizerEquiv_invFun g a` is the element of the fiber `f⁻¹(f a)` that `g (f a)` sends `a` to, coerced back to `α`. It serves as the inverse-function component of a `MulEquiv` between the stabilizer of `f` in `Perm α` (permutations of `α` that fix every value of `f`) and the direct product `∏ i, Perm {a // f a = i}`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.stabilizerEquiv_invFun : {α : Type u_1} -> {ι : Type u_2} -> {f : α → ι} -> (g : (i : ι) → Equiv.Perm { a // f a = i }) -> (a : α) -> α
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {ι : Type u_2} -> {f : α → ι} -> (g : (i : ι) → Equiv.Perm { a // f a = i }) -> (a : α) -> α`

The implicit type `α` is the domain being permuted. The implicit type `ι` is the index type (the codomain of `f`). The implicit function `f : α → ι` is the map whose fibers are being permuted; it classifies elements of `α` by their "fiber index". The explicit argument `g` is a family of permutations: for each index `i : ι`, `g i` is a permutation of the subtype `{a : α // f a = i}`, i.e., the fiber of `f` over `i`. The explicit argument `a : α` is the point at which the function is evaluated; it determines which fiber permutation is applied.

## Conventions

There are no junk-value or boundary conventions to declare: the function is total and well-defined for all valid inputs without any special-case overrides.

## Worked examples

- Claim: For the identity family of permutations (each `g i = Equiv.refl _`), `stabilizerEquiv_invFun g a = a` for any `a`.

- Claim: If `f : Fin 4 → Fin 2` is defined by `f i = i % 2` and `g` swaps the two even-indexed elements `⟨0, rfl⟩` and `⟨2, rfl⟩` in the fiber over `0` while acting as the identity on the fiber over `1`, then `stabilizerEquiv_invFun g 0 = 2`.

- Claim: The output of `VTask.stabilizerEquiv_invFun g a` always lies in the same fiber as `a`, i.e., `f (VTask.stabilizerEquiv_invFun g a) = f a` for all `g` and `a` (this is exactly `comp_stabilizerEquiv_invFun`).

- Claim: If `f a = i` then `VTask.stabilizerEquiv_invFun g a = g i ⟨a, h⟩` where `h : f a = i` (this is exactly `stabilizerEquiv_invFun_eq`).

## Boundaries

- The function is total: it is defined for every `g`, `a`, and implicit `f`. There are no restrictions on `α`, `ι`, or `f`.
- When `g i = Equiv.refl _` for all `i` (the identity family), the function returns `a` unchanged.
- When `α` or `ι` is an empty type, the function vacuously applies (there are no elements `a : α` to evaluate at).
- The output always belongs to the same fiber as the input: `f (stabilizerEquiv_invFun g a) = f a`. In other words, `stabilizerEquiv_invFun g` maps each fiber of `f` to itself.

## Not to be confused with

- `Equiv.Perm.ofSubtype`: lifts a permutation of a subtype to a permutation of the whole type by acting as the identity outside the subtype — different construction and different purpose.
- The `toFun` (forward) direction of the stabilizer `MulEquiv`: that map sends a permutation `σ` in the stabilizer to the family of its restrictions to each fiber, which is the inverse of what `stabilizerEquiv_invFun` computes.
- `MulAction.stabilizer`: the stabilizer subgroup itself (a subgroup of `Perm α`), not the function reconstructing a permutation from fiber data.