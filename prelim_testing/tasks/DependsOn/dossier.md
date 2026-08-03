## Object

`VTask.DependsOn f s` is the proposition that the function `f`, which takes a dependent-product (family of values indexed by `ι`) and returns a value in `β`, **depends only on the components indexed by `s`**: whenever two inputs `x` and `y` agree on every index in `s`, their images under `f` are equal.  In other words, `f` cannot "see" the difference between `x` and `y` outside of `s`.

The predicate should be read as "`f` potentially depends only on variables in `s`".  It does **not** assert that `f` actively uses every element of `s`; a constant function satisfies `VTask.DependsOn f ∅` (and hence every superset), and every function satisfies `VTask.DependsOn f univ`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.DependsOn : {ι : Type u_1} -> {α : ι → Type u_2} -> {β : Type u_3} -> (f : ((i : ι) → α i) → β) -> (s : Set ι) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.DependsOn : {ι : Type u_1} -> {α : ι → Type u_2} -> {β : Type u_3} -> (f : ((i : ι) → α i) → β) -> (s : Set ι) -> Prop`

The implicit argument `ι` is the index type parameterising the family.  The implicit argument `α` assigns a type to each index; together `(i : ι) → α i` forms the dependent-product domain of `f`.  The implicit argument `β` is the codomain type.  The explicit argument `f` is the function whose dependence is being described.  The explicit argument `s` is the set of indices on which `f` is claimed to depend (i.e., the set that is sufficient to determine `f`'s output).

## Conventions

There are no junk-value or out-of-domain conventions for this definition: it is a universally-quantified proposition that is well-formed for every function `f` and every set `s`, including the empty set and the universal set.

## Worked examples

- Claim: Every function `f : ((i : ι) → α i) → β` satisfies `VTask.DependsOn f Set.univ`, because any two inputs that agree on all of `univ` are equal everywhere and thus have the same image.

- Claim: A constant function `fun (_ : (i : ι) → α i) => b` satisfies `VTask.DependsOn (fun _ => b) ∅`, because its output is independent of its input entirely, so the vacuous condition (agree on all indices in `∅`) is trivially sufficient.

- Claim: If `VTask.DependsOn f s` holds and `s ⊆ t`, then `VTask.DependsOn f t` holds, since any two inputs that agree on the larger set `t` in particular agree on `s`, and `f` already cannot distinguish inputs that agree on `s`.

- Claim: The restriction function `Set.restrict s (π := α)`, which projects a family to the sub-family indexed by `s`, satisfies `VTask.DependsOn (Set.restrict s) s`.

## Boundaries

- **Empty set:** `VTask.DependsOn f ∅` holds if and only if `f` is constant (since the agreement condition over `∅` is vacuous, it forces `f x = f y` for all `x` and `y`).
- **Universal set:** `VTask.DependsOn f Set.univ` holds for every `f`, because two inputs that agree on every index in `univ` are identical, so `f` trivially maps them to the same value.
- **Monotonicity:** The property is monotone in `s`; if `f` depends only on `s` then it depends on any superset `t ⊇ s`.  (The converse does not hold in general.)
- **Constant functions:** A constant function depends on the empty set, and consequently on every set.
- **The predicate makes no claim about minimality:** `VTask.DependsOn f s` does not mean `s` is the smallest such set; it only asserts that `s` is *sufficient*.

## Not to be confused with

- `Function.FactorsThrough`: a related notion asserting that `f` factors through another function; `VTask.DependsOn f s` is equivalent to `f` factoring through the restriction `Set.restrict s`, but `FactorsThrough` is a more general concept.
- `Set.EqOn`: `Set.EqOn f g s` says two functions `f` and `g` agree pointwise on `s`; this is about equality of two functions on a set, not about a single function's dependence on coordinates.
- `Function.support`: the support of a function identifies where a function is nonzero, which is a different (and generally incomparable) concept to the index-set on which the function's output depends.