## Object

A product `l` (a finite list of elements of an index type, viewed as a monomial in the basis construction for locally constant functions) is called **good** (with respect to a profinite set `C`) if its evaluation as a locally constant function on `C` (with values in `ℤ`) is **not** a `ℤ`-linear combination of evaluations of products that are strictly smaller than `l` in the product order. In other words, `l` is good if and only if it cannot be expressed in terms of "earlier" basis candidates, making it an independent contributor to the module `LocallyConstant C ℤ`.

The collection of all good products is the one proved to index a `ℤ`-basis of `LocallyConstant C ℤ`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.isGood : {I : Type u} -> (C : Set (I → Bool)) -> [LinearOrder I] -> (l : Profinite.NobelingProof.Products I) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.isGood : {I : Type u} -> (C : Set (I → Bool)) -> [LinearOrder I] -> (l : Profinite.NobelingProof.Products I) -> Prop`

- `I` is the index type over which the boolean-valued functions are defined; it is implicit and inferred from context.
- `C` is the underlying profinite set, given as a subset of all `I`-indexed Boolean sequences.
- The `LinearOrder I` instance provides the linear ordering on `I` that is used to define the strict order on products (and hence to compare products as "smaller" or "larger").
- `l` is the product (a formal finite list/monomial indexed by elements of `I`) whose goodness is being tested.

## Conventions

There are no special junk-value or boundary conventions declared for this predicate: it is a straightforwardly meaningful `Prop` for every valid combination of inputs, with no edge case where a degenerate or default value is assigned.

## Worked examples

- Claim: The empty product (the unit element, corresponding to the constant function `1`) is good with respect to any non-empty `C`, because no product is strictly smaller than the empty product, so the span of evaluations of strictly smaller products is `{0}`, and the constant function `1` is nonzero on a non-empty space.

- Claim: If `l` is a product whose evaluation in `LocallyConstant C ℤ` lies in the `ℤ`-span of evaluations of all products strictly less than `l`, then `VTask.isGood C l` is false (i.e., `l` is not good).

- Claim: Among products of the same length, whether a product is good depends on the specific element of `C` and the ordering on `I`; two products at the same level need not have the same goodness status.

## Boundaries

- **Empty product**: The empty product (if `Products I` contains it) is good whenever its evaluation is nonzero in `LocallyConstant C ℤ` (equivalently, whenever `C` is non-empty), since there are no products strictly below it and the span of an empty set is `{0}`.
- **Maximal products**: A product `l` that is maximal in the order will be good if and only if its evaluation is not already in the span of all strictly smaller products' evaluations — this is the generic case and no special shortcut applies.
- **Empty `C`**: If `C` is empty, then all evaluations of products are the zero function; in that case no product is good, since the zero element always belongs to any submodule span (including the trivial span `{0}`).
- **Duplicate products**: The definition treats `l` as a specific element of `Products I`; the order on products comes from the induced ordering on `I`-indexed lists, and the strict inequality `m < l` governs which evaluations enter the span.

## Not to be confused with

- **`Products.eval C l`**: This is the evaluation map sending a product `l` to its corresponding locally constant function on `C`; `VTask.isGood` is a predicate *about* such evaluations, not the evaluation itself.
- **Linear independence of a set of products**: Goodness is a *relative* notion (independence from the span of strictly smaller products), not absolute linear independence of a collection.
- **Membership in a basis**: While good products are proved to form a basis, `VTask.isGood C l` is the local condition on a single product, not a statement that a set is a basis.