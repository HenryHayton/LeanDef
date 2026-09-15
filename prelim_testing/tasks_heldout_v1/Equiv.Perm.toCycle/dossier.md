## VTask.toCycle

### Object

Given a permutation `f` of a finite type `α` that is a cycle (i.e., there exists some element whose entire orbit under repeated application of `f` covers all non-fixed points, and that orbit is finite and non-trivial), `VTask.toCycle f hf` produces the corresponding `Cycle α` — an equivalence class of lists up to rotation — whose elements are exactly the non-fixed points of `f`, listed in the order they are visited by successive applications of `f`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toCycle : {α : Type u_1} -> [Fintype α] -> [DecidableEq α] -> (f : Equiv.Perm α) -> (hf : f.IsCycle) -> Cycle α
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> [Fintype α] -> [DecidableEq α] -> (f : Equiv.Perm α) -> (hf : f.IsCycle) -> Cycle α`

The type `α` is the finite type being permuted; the `Fintype` and `DecidableEq` instances supply finiteness and decidable equality for `α`, which are needed to search through the universe for a non-fixed point and to iterate the permutation. The argument `f` is the cyclic permutation whose orbit structure is to be recorded, and `hf` is the proof that `f` is indeed a cycle (i.e., it has exactly one orbit of size ≥ 2 and fixes everything else).

### Conventions

The resulting `Cycle α` is independent of which non-fixed point of `f` is chosen as the starting element: any two such starting points yield rotations of one another, and `Cycle α` identifies rotations. Thus the output is well-defined and canonical as a cycle value.

### Worked examples

- Claim: For a 3-cycle `f = (0 1 2)` on `Fin 3`, every non-fixed element belongs to `VTask.toCycle f hf`.

- Claim: The cycle produced by `VTask.toCycle f hf` is nodup (no element appears twice), since distinct iterates of a cycle on a finite type are distinct until the orbit closes.

- Claim: The cycle produced by `VTask.toCycle f hf` is nontrivial (has at least two elements), since any cycle permutation moves at least two points.

- Claim: For any cyclic permutation `f` and any non-fixed point `x` (i.e., `f x ≠ x`), `VTask.toCycle f hf` equals `Equiv.Perm.toList f x` as cycles, meaning the output agrees with the list obtained by starting at `x` and iterating `f`.

- Claim: The `next` element of `x` in `VTask.toCycle f hf` (with respect to the cycle's order) is `f x`, so the cycle faithfully encodes the application order of `f`.

### Boundaries

- The function requires a proof `hf : f.IsCycle`; it is not defined for arbitrary permutations. A permutation that is the identity or a product of two or more disjoint cycles does not satisfy `IsCycle` and so cannot be passed.
- An element `x : α` belongs to `VTask.toCycle f hf` if and only if `f x ≠ x`, i.e., `x` is in the support of `f`. Fixed points are absent from the output cycle.
- Since `Cycle α` quotients out by rotation, the specific list representative stored internally may differ between runs or implementations, but the cycle value (the equivalence class) is uniquely determined by `f`.
- The output cycle is always nodup and always nontrivial (length ≥ 2), consistent with the cycle condition requiring at least two non-fixed points.

### Not to be confused with

- `Equiv.Perm.toList f x`: a concrete `List α` starting at a chosen basepoint `x`; `VTask.toCycle` is the canonical rotation-invariant cycle obtained from any such list.
- `Cycle.toPerm`: the inverse direction, turning a `Cycle α` back into a permutation; `VTask.toCycle` goes the other way.
- `Equiv.Perm.cycleOf f x`: the permutation whose single non-trivial orbit is the orbit of `x` under `f`; this is a `Perm α`, not a `Cycle α`.
