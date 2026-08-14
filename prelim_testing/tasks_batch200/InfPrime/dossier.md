## VTask.InfPrime

### Object

An element `a` of a semilattice with meets (infima) is called **inf-prime** if it satisfies two conditions simultaneously: first, `a` is not a maximal element of the order (equivalently, it is not ⊤ when a top element exists); and second, whenever the meet (infimum) of two elements `b` and `c` lies below `a`, at least one of `b` or `c` already lies below `a`. This is the order-theoretic analogue of a prime element in a ring or lattice: meets "factor through" inf-prime elements.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.InfPrime : {α : Type u_2} -> [SemilatticeInf α] -> (a : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.InfPrime : {α : Type u_2} -> [SemilatticeInf α] -> (a : α) -> Prop
```

The implicit type argument `α` is the carrier type of the ordered structure. The instance argument equips `α` with binary meet (infimum) operations, making it a semilattice under `⊓`. The explicit argument `a` is the element of `α` being tested for the inf-prime property.

### Conventions

There are no declared junk-value or out-of-domain conventions for this definition: `VTask.InfPrime` is a predicate that is either true or false for every element of every semilattice, with no inputs outside its natural domain.

### Worked examples

- Claim: In the lattice of natural numbers ordered by divisibility, the element 2 is inf-prime because 2 is not maximal and whenever `lcm b c` divides into 2 (i.e., `b ⊓ c ≤ 2`), then `b ≤ 2` or `c ≤ 2`.

- Claim: The top element ⊤ of any semilattice with a top is never inf-prime, since it is a maximal element; formally, `¬ VTask.InfPrime (⊤ : α)` holds in any such structure.

- Claim: In a linear order (total order), every non-maximal element is inf-prime, because in a total order `b ⊓ c` equals the smaller of `b` and `c`, so if `b ⊓ c ≤ a` then at least one of `b`, `c` equals that minimum and is hence `≤ a`.

- Claim: In the two-element Boolean lattice `{⊥, ⊤}`, the bottom element `⊥` is inf-prime if and only if `⊥ ≠ ⊤` (i.e., the lattice is nontrivial), because `⊥` is the unique non-top element and any meet `b ⊓ c ≤ ⊥` forces both `b = ⊥` and `c = ⊥`, so certainly one of them is `≤ ⊥`.

### Boundaries

- **Top element**: If `α` has a top element `⊤`, then `VTask.InfPrime ⊤` is always false, because `⊤` is maximal. The first condition of the conjunction immediately fails.
- **Maximal elements**: Any maximal element fails to be inf-prime, regardless of how meets behave. The condition `¬IsMax a` is necessary.
- **Trivial one-element semilattice**: In a one-element type, the unique element is both ⊤ and maximal, so `VTask.InfPrime` holds of no element.
- **Linear orders**: In a linear (total) order, `VTask.InfPrime a` holds if and only if `a` is not maximal, since the meet condition is automatically satisfied by totality.
- **Equivalence with inf-irreducibility**: In the context of a semilattice, `VTask.InfPrime a` is equivalent to `InfIrred a` (inf-irreducible). This equivalence may fail in more general settings where the two notions diverge.
- **Dual relationship**: `VTask.InfPrime a` in `α` corresponds exactly to `SupPrime (toDual a)` in the dual order `αᵒᵈ`.

### Not to be confused with

- **`InfIrred`** (inf-irreducible): An element that cannot be written as a meet of two strictly larger elements. In a semilattice, this coincides with `VTask.InfPrime`, but the two notions are conceptually distinct and may differ in other structures.
- **`SupPrime`** (sup-prime): The order-dual notion, concerning joins instead of meets; `VTask.InfPrime a` in `α` is equivalent to `SupPrime (toDual a)` in the opposite order.
- **`IsMax`** (maximal element): A maximal element is explicitly excluded from being inf-prime; do not confuse the negativity condition `¬IsMax a` with the positive inf-prime property itself.
