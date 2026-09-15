## Object

The *boundary of the N-cube* is the subset of the unit cube $I^N$ (the set of all functions from a type $N$ to the unit interval $[0,1]$) consisting of those points that are "on the face" of the cube: a point belongs to the boundary if and only if at least one of its coordinate projections attains the extreme value $0$ or $1$.

Intuitively, for a finite $N$ this recovers the usual topological boundary of the hypercube $[0,1]^N$: the union of all codimension-1 faces.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.boundary : (N : Type u_1) -> Set (N → ↑unitInterval)
<!-- PINNED-SIGNATURE:END -->


`VTask.boundary : (N : Type u_1) -> Set (N → ↑unitInterval)`

The single argument `N` is the *index type* whose elements name the coordinate directions of the cube. The output is a subset of the function type $I^N$ (functions from `N` into the unit interval), namely those functions that witness at least one extreme coordinate.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a set-valued definition that is well-behaved at every type `N`, including the empty type, where the boundary is the empty set (no index exists to be extreme).

## Worked examples

- Claim: A constant function sending every index to $0$ belongs to `VTask.boundary N` for any inhabited type `N`.

- Claim: A constant function sending every index to $1$ belongs to `VTask.boundary N` for any inhabited type `N`.

- Claim: For `N = Empty`, the boundary `VTask.boundary Empty` is the empty set, because there is no index `i : Empty` to satisfy the existential condition.

- Claim: A function `y : I^N` belongs to `VTask.boundary (M ⊕ N)` if and only if either its restriction to the `M`-coordinates belongs to `VTask.boundary M` or its restriction to the `N`-coordinates belongs to `VTask.boundary N` (this is the content of `Cube.boundary_sum_iff`).

## Boundaries

- **Empty index type**: When `N = Empty` (or any empty type), there are no coordinates, so no point can satisfy the existential; the boundary is the empty set. The unique element of $I^{\text{Empty}}$ (the empty function) is therefore *not* in the boundary.
- **Singleton index type**: When `N` has exactly one element, the cube is just $I$ itself, and the boundary consists of exactly the two points $\{0, 1\}$.
- **Interior points**: Any function all of whose coordinates lie strictly in $(0,1)$ does *not* belong to the boundary. The complement of the boundary inside the cube is the open interior.
- **Partial extremality suffices**: A point with even one coordinate equal to $0$ or $1$ is in the boundary, regardless of all other coordinates.

## Not to be confused with

- **The topological boundary `frontier`**: The set-theoretic topological frontier (closure minus interior) of the cube in some ambient space. For the cube as a topological space, these notions agree, but `VTask.boundary` is defined combinatorially via coordinate values, not via topological closure/interior operators.
- **`GenLoop` (Ω^N X x)**: The type of maps from the N-cube to a space that are constant on `VTask.boundary N`; this uses the boundary as a *domain restriction*, not as the object itself.
- **`Cube.insertAt`**: An operation that inserts a coordinate value into a point of the (N−1)-cube to produce a point of the N-cube; closely related (its range may land in the boundary) but is not the boundary set itself.