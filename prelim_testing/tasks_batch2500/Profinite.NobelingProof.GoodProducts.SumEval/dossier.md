## VTask.SumEval

### Object

`VTask.SumEval C ho` is a map from the disjoint union (coproduct) of two sets of "good products" into the module of locally constant integer-valued functions on `C`. Concretely, the domain is the disjoint union of:
- the good products of the restricted space `π C (ord I · < o)` (those indexed products of projections that form a linearly independent spanning set for the smaller space), and
- the "max products" of `C` relative to the ordinal `o` (those good products that involve the new, maximal coordinate introduced at stage `o`).

The map sends each element of this coproduct to the locally constant function on `C` obtained by evaluating the underlying product at points of `C`. It is the canonical way to package, into a single map out of the coproduct `ι ⊕ ι'`, both the evaluation of lower-stage good products on `C` and the evaluation of new max products on `C`. It plays the role of `u` in the commutative diagram central to the inductive step of Nöbeling's theorem.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SumEval : {I : Type u} -> (C : Set (I → Bool)) -> [LinearOrder I] -> [WellFoundedLT I] -> {o : Ordinal.{u}} -> (ho : o < Ordinal.type fun x1 x2 => x1 < x2) -> ↑(Profinite.NobelingProof.GoodProducts (Profinite.NobelingProof.π C fun x => Profinite.NobelingProof.ord I x < o)) ⊕
      ↑(Profinite.NobelingProof.GoodProducts.MaxProducts C ho) →
    LocallyConstant ↑C ℤ
<!-- PINNED-SIGNATURE:END -->


`{I : Type u} -> (C : Set (I → Bool)) -> [LinearOrder I] -> [WellFoundedLT I] -> {o : Ordinal.{u}} -> (ho : o < Ordinal.type fun x1 x2 => x1 < x2) -> ↑(Profinite.NobelingProof.GoodProducts (Profinite.NobelingProof.π C fun x => Profinite.NobelingProof.ord I x < o)) ⊕ ↑(Profinite.NobelingProof.GoodProducts.MaxProducts C ho) -> LocallyConstant ↑C ℤ`

- `I` is the index type, which must be equipped with a well-founded linear order (these are instance arguments).
- `C` is the closed subset of `I → Bool` (a profinite space) on which the locally constant functions live.
- `ho` is a proof that the ordinal `o` is strictly less than the order type of `I`, ensuring the stage `o` is a legitimate position in the well-founded ordering on `I` and that the "max products" at `o` are well-defined.
- The final argument is an element of the coproduct: either a good product from the restricted space at levels below `o`, or a max product at level `o`.

### Conventions

There are no declared junk-value or boundary conventions: the function is defined on all elements of a coproduct of subtypes, both summands are handled uniformly by evaluating on `C`, and there is no degenerate input yielding a conventional output.

### Worked examples

- Claim: For any element `l` from the left summand (a good product of `π C (ord I · < o)`), `VTask.SumEval C ho (Sum.inl l)` equals `l.1.eval C`, i.e., the evaluation of the underlying product list directly on `C`.

- Claim: For any element `r` from the right summand (a max product), `VTask.SumEval C ho (Sum.inr r)` also equals `r.1.eval C`, i.e., the evaluation of the underlying product list directly on `C`.

- Claim: The composite `VTask.SumEval C ho ∘ Sum.inl` coincides with the composite of the restriction map `πs C o` and the evaluation map `GoodProducts.eval (π C (ord I · < o))`, as expressed by `GoodProducts.square_commutes`.

- Claim: Linear independence of `GoodProducts.eval C` is equivalent to linear independence of `VTask.SumEval C ho`, as expressed by `GoodProducts.linearIndependent_iff_sum`.

### Boundaries

- When `o = 0`, the set `π C (ord I · < 0)` collapses to the one-point space (all products are trivial), and the good products from the left summand are trivial; the map is still well-defined and sends them to the appropriate constant function on `C`.
- When `C` is empty, all locally constant functions on `C` are trivially equal (there is only one function from the empty set), and `VTask.SumEval C ho` sends everything to this unique element.
- The map is not injective in general; its linear independence as a family (indexed over the coproduct) is exactly the condition studied by `linearIndependent_iff_sum`.
- Both summands are mapped into `LocallyConstant C ℤ` by the same mechanism (eval on `C`), so there is no asymmetry in behaviour between left and right summands beyond the type of the input.

### Not to be confused with

- `GoodProducts.eval C` — the evaluation map from good products of `C` itself (not a coproduct domain) into `LocallyConstant C ℤ`; `VTask.SumEval` packages two evaluation maps into one map out of a coproduct.
- `GoodProducts.eval (π C (ord I · < o))` — the evaluation map for the *restricted* space, landing in `LocallyConstant (π C (ord I · < o)) ℤ`, not in `LocallyConstant C ℤ`.
- `MaxProducts` — the subtype forming the right summand of the domain; `VTask.SumEval` is the map *out of* the coproduct involving max products, not the max products themselves.
