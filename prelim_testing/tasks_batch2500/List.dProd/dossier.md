## VTask.dProd

### Object

Given a graded monoid — a family of types `A i` indexed by an additive monoid `ι`, equipped with a unit in `A 0` and a multiplication `A i × A j → A (i + j)` — `VTask.dProd` computes the **dependent product** of a list of elements drawn from that family. Concretely, for each element `a` in the list `l : List α`, one supplies a grade `fι a : ι` and an element `fA a : A (fι a)`; the result is their product in the graded sense, an element of `A (l.dProdIndex fι)`, where `l.dProdIndex fι` is the sum of all grades `fι a` over `a ∈ l`. This is the dependently-typed generalisation of `(l.map fA).prod` for an ordinary (non-graded) monoid.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dProd : {ι : Type u_1} -> {α : Type u_2} -> {A : ι → Type u_3} -> [AddMonoid ι] -> [GradedMonoid.GMonoid A] -> (l : List α) -> (fι : α → ι) -> (fA : (a : α) → A (fι a)) -> A (l.dProdIndex fι)
<!-- PINNED-SIGNATURE:END -->


VTask.dProd : {ι : Type u_1} -> {α : Type u_2} -> {A : ι → Type u_3} -> [AddMonoid ι] -> [GradedMonoid.GMonoid A] -> (l : List α) -> (fι : α → ι) -> (fA : (a : α) → A (fι a)) -> A (l.dProdIndex fι)

- `ι` is the grading index type, which must carry an `AddMonoid` structure so that grades can be summed.
- `α` is the element type of the list being iterated over.
- `A` is the graded family of types, indexed by `ι`.
- The `AddMonoid ι` instance supplies the additive structure used to accumulate grades.
- The `GradedMonoid.GMonoid A` instance supplies the graded unit and multiplication across components.
- `l` is the list of items whose graded components are to be multiplied.
- `fι` assigns a grade in `ι` to each element of `α`.
- `fA` assigns, to each `a : α`, an element of `A (fι a)` — the actual graded factor contributed by `a`.

### Conventions

No junk-value or edge conventions beyond standard algebraic identities are declared for this definition: it is a total function and its behaviour at boundaries (empty list, singleton, etc.) is fully determined by the graded monoid laws (`GOne.one` for the empty product and `GMul.mul` for the cons step).

### Worked examples

- Claim: For the empty list, `VTask.dProd [] fι fA = GradedMonoid.GOne.one` (the graded unit in `A 0`).

- Claim: For a cons list `(a :: l)`, `VTask.dProd (a :: l) fι fA = GradedMonoid.GMul.mul (fA a) (VTask.dProd l fι fA)`, i.e., the product prepends `fA a` to the accumulated product of the tail.

- Claim: When `A` is the constant family `fun _ : ι => R` for an ordinary monoid `R`, `VTask.dProd l fι fA` coincides with `(l.map fA).prod` in `R`, recovering the non-dependent list product.

- Claim: For a two-element list `[a₁, a₂]`, the result lives in `A (fι a₁ + fι a₂)` and equals `GMul.mul (fA a₁) (GMul.mul (fA a₂) GOne.one)`.

### Boundaries

- **Empty list**: `VTask.dProd [] fι fA` is the graded unit `GradedMonoid.GOne.one : A 0`, and the index `[].dProdIndex fι` is `0` (the additive identity of `ι`).
- **Singleton list**: `VTask.dProd [a] fι fA` equals `GMul.mul (fA a) GOne.one` living in `A (fι a + 0)`, which by the monoid law is isomorphic to `A (fι a)`.
- **Non-graded specialisation**: When the grading is trivial (all components are the same type with ordinary monoid structure), the result is provably equal to `(l.map fA).prod`.
- The function is defined for every list length and every choice of `fι` and `fA`; there are no undefined or partial cases.

### Not to be confused with

- `List.prod` — the ordinary (non-dependent) product of a list in a monoid; `VTask.dProd` generalises this to the graded setting where the type of the result depends on the grades of the factors.
- `List.dProdIndex` — this computes only the *grade* (index) of the result, i.e., the sum of grades `fι a`; `VTask.dProd` computes the actual *element* living at that grade.
- `GradedMonoid.mk` / `GradedMonoid.GMul.mul` — these operate on a single graded multiplication step; `VTask.dProd` iterates this over an entire list.