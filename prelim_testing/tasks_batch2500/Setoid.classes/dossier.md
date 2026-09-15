## VTask.classes

### Object

Given a setoid (a type equipped with an equivalence relation), `VTask.classes r` is the **set of all equivalence classes** of the relation `r`. Concretely, it is the collection of all subsets of `α` of the form `{ x | x ~ y }` for some element `y : α` — that is, every set consisting of all elements equivalent to some fixed representative. Together these sets form the **quotient partition** of `α` induced by `r`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.classes : {α : Type u_1} -> (r : Setoid α) -> Set (Set α)
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> (r : Setoid α) -> Set (Set α)`

The implicit type argument `α` is the carrier type whose elements are being partitioned. The explicit argument `r` is the setoid structure on `α`, which packages both the binary equivalence relation and its proof of reflexivity, symmetry, and transitivity. The output is a set whose elements are subsets of `α`, namely all the equivalence classes.

### Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total function defined uniformly for every setoid on every type, and every output is a mathematically meaningful set of equivalence classes.

### Worked examples

- Claim: For the trivial setoid on a two-element type where everything is equivalent, `VTask.classes` yields a singleton collection containing the whole type.

- Claim: For the discrete setoid on a type `α` (where `x ~ y` iff `x = y`), every singleton `{a}` belongs to `VTask.classes`, and those are the only members.

- Claim: A set `s` belongs to `VTask.classes r` if and only if there exists some `y : α` such that `s = { x | r x y }`.

- Claim: The union of all members of `VTask.classes r` equals the universal set `Set.univ` (every element of `α` belongs to its own equivalence class).

### Boundaries

- **Empty type**: When `α` is empty (`α = PEmpty` or similar), there are no elements and hence no equivalence classes; `VTask.classes r` is the empty collection `∅ : Set (Set α)`.
- **Single-element type**: When `α` has exactly one element, there is exactly one equivalence class (the whole type), so `VTask.classes r` is a singleton.
- **Discrete setoid**: When two elements are equivalent only to themselves, `VTask.classes r` consists precisely of all singletons `{a}` for `a : α`.
- **Indiscrete (trivial) setoid**: When all elements are equivalent, `VTask.classes r` is the singleton collection `{Set.univ}`.
- The same equivalence class can be "witnessed" by any of its members as representative, but `VTask.classes r` contains each class only once as a set (set-extensionality ensures no duplicates in the output).

### Not to be confused with

- **`Quotient α r`** — the quotient *type* formed by collapsing equivalence classes to points, not the set-theoretic collection of classes themselves.
- **`Setoid.ker f`** — the setoid whose classes are the fibers of a function `f`, which is a *construction of a setoid* rather than the extraction of its classes.
- **`Set.range`** applied to the quotient map — produces the image of the canonical projection, which relates to but is not the same object as the set of equivalence classes.