## Object

`VTask.permsOfFinset s` is the finite set of all permutations of the type `α` whose support is contained in (equivalently, that permute only elements of) the finite set `s`. More precisely, it is the `Finset (Equiv.Perm α)` whose members are exactly the bijections `α → α` that can be described as a rearrangement of the elements of `s` (fixing everything outside `s` pointwise). For a set of size `n`, this finset has cardinality `n!`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.permsOfFinset : {α : Type u_1} -> [DecidableEq α] -> (s : Finset α) -> Finset (Equiv.Perm α)
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the ambient type whose elements are being permuted; it must admit decidable equality so that finset membership can be computed. The instance `[DecidableEq α]` is supplied automatically. The explicit argument `s` is the finite set of elements whose permutations are to be enumerated.

## Conventions

There are no junk-value conventions to declare: the function is total and well-defined for every `Finset α`, including the empty finset.

## Worked examples

- Claim: `VTask.permsOfFinset (∅ : Finset ℕ)` has cardinality 1 (the unique permutation of zero elements is the identity).

- Claim: `VTask.permsOfFinset ({0, 1} : Finset ℕ)` has cardinality 2 (the two permutations are the identity and the transposition swapping 0 and 1).

- Claim: `VTask.permsOfFinset ({0, 1, 2} : Finset ℕ)` has cardinality 6, matching `3! = 6`.

- Claim: The identity permutation `Equiv.refl ℕ` belongs to `VTask.permsOfFinset s` for every `Finset ℕ` `s`.

## Boundaries

- **Empty finset**: `VTask.permsOfFinset ∅` is the singleton containing only the identity permutation (the unique permutation of the empty set). Its cardinality is `0! = 1`.
- **Singleton finset**: `VTask.permsOfFinset {a}` is also a singleton, since the only permutation of a one-element set is the identity. Its cardinality is `1! = 1`.
- **General size-n finset**: The result always has exactly `n!` elements, where `n = s.card`.
- **Membership criterion**: A permutation `σ` belongs to `VTask.permsOfFinset s` if and only if `σ` maps `s` to itself (i.e., `s` is invariant under `σ`), or equivalently, `σ` fixes every element not in `s` — matching exactly the permutations that arise as rearrangements of the elements listed in `s`.

## Not to be confused with

- `Finset.perm` (or similar): a relation saying two finsets are permutations of each other, which is about list-like equality of multisets, not about group elements.
- `Equiv.Perm.sumCongrHom` or subgroup constructions: these build the *group* of permutations of `s` as a subgroup, rather than an enumerated `Finset`.
- `List.permutations`: produces a `List` of all list-permutations of a given list, not a `Finset` of group-theoretic `Equiv.Perm` elements.