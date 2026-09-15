## VTask.lift

### Object

Given a commutative ring `R`, a ring `S` presented as the result of adjoining a root of a polynomial `f ∈ R[X]` to `R` (witnessed by `h : IsAdjoinRoot S f`), a ring homomorphism `i : R →+* T`, and an element `x ∈ T` that is a root of `f` under `i` (i.e., `f` evaluated at `x` via `i` equals zero), `VTask.lift` produces the unique ring homomorphism `S →+* T` that extends `i` on the base ring `R` and sends the adjoined root in `S` to `x` in `T`.

This is the universal property of an adjunction: a ring map out of `S` is the same data as a ring map out of `R` together with a compatible root in the target.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {R : Type u} -> {S : Type v} -> [CommRing R] -> [Ring S] -> {f : Polynomial R} -> [Algebra R S] -> (h : IsAdjoinRoot S f) -> {T : Type u_1} -> [CommRing T] -> (i : R →+* T) -> (x : T) -> (hx : Polynomial.eval₂ i x f = 0) -> S →+* T
<!-- PINNED-SIGNATURE:END -->


`{R : Type u} -> {S : Type v} -> [CommRing R] -> [Ring S] -> {f : Polynomial R} -> [Algebra R S] -> (h : IsAdjoinRoot S f) -> {T : Type u_1} -> [CommRing T] -> (i : R →+* T) -> (x : T) -> (hx : Polynomial.eval₂ i x f = 0) -> S →+* T`

- `R` is the base commutative ring from which the polynomial `f` is drawn.
- `S` is the ring obtained by adjoining a root of `f` to `R`; the `Algebra R S` instance encodes that `R` maps into `S`.
- `h` is the witness (an `IsAdjoinRoot` structure) certifying that `S` is indeed the ring obtained by adjoining a root of `f` over `R`.
- `T` is the target commutative ring into which we wish to map.
- `i` is the ring homomorphism from the base ring `R` into `T`.
- `x` is the element of `T` chosen to be the image of the adjoined root.
- `hx` is the proof that `x` is actually a root of `f` in `T`, computed via `i` — that is, `Polynomial.eval₂ i x f = 0`.

The output is a ring homomorphism `S →+* T`.

### Conventions

There are no junk-value or degenerate-input conventions for this construction: every valid input satisfying the stated types and the root condition `hx` yields a well-defined ring homomorphism. The definition is total on its domain.

### Worked examples

- Claim: Evaluating `VTask.lift h i x hx` at the distinguished root `h.root` of `S` returns `x`.
  (This is the theorem `lift_root`: the lift sends the generator to the specified root.)

- Claim: Evaluating `VTask.lift h i x hx` at `algebraMap R S a` (the image of a base-ring element `a`) returns `i a`.
  (This is the theorem `lift_algebraMap`: the lift extends `i` on the base ring.)

- Claim: For any polynomial `z : R[X]`, the lift satisfies `VTask.lift h i x hx (h.map z) = Polynomial.eval₂ i x z`.
  (This is the theorem `lift_map`: the lift is compatible with evaluating polynomials at `x`.)

- Claim: Taking `T = S`, `i = algebraMap R S`, and `x = h.root`, the lift `VTask.lift h (algebraMap R S) h.root h.aeval_root_self` equals the identity ring homomorphism on `S`.
  (This is the theorem `lift_self`.)

### Boundaries

- **When `f = 0`**: Every element of `T` is vacuously a root of the zero polynomial, so `hx` is always satisfiable. The lift still exists and is uniquely determined by where `h.root` maps.
- **When `f` is a nonzero constant**: The condition `eval₂ i x f = 0` forces `i` to map that constant to zero in `T`. If this cannot hold, no valid `hx` exists and the lift is inapplicable, but whenever `hx` is supplied the lift is well-defined.
- **Uniqueness**: The lift is the *unique* ring homomorphism `g : S →+* T` satisfying both `g ∘ algebraMap R S = i` and `g h.root = x`. Any other such homomorphism must equal `VTask.lift h i x hx` pointwise (as stated by `eq_lift`).
- **Self-lift**: Lifting along the structure map back to `S` itself with `h.root` as the target root recovers exactly the identity map on `S`.

### Not to be confused with

- `IsAdjoinRoot.liftHom`: The algebra-homomorphism (`R`-algebra map `S →ₐ[R] T`) variant of the same universal property; it requires `T` to carry an `Algebra R T` instance compatible with `i`.
- `Polynomial.eval₂`: Evaluates a polynomial at a point in a ring via a ring homomorphism; `VTask.lift` uses `eval₂` internally on representatives but produces a map on the quotient ring `S`, not on polynomials.
- `AdjoinRoot.liftHom`: The analogous lift for the *concrete* adjoin-root construction `AdjoinRoot f = R[X] ⧸ (f)`, as opposed to the abstract `IsAdjoinRoot` predicate used here.
