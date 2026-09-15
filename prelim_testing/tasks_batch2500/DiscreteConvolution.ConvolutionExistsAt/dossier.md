## VTask.ConvolutionExistsAt

### Object

`VTask.ConvolutionExistsAt L f g x` is the proposition asserting that the discrete additive convolution of the functions `f` and `g`, bilinearly paired via `L`, is well-defined at the point `x`. Concretely, it says that the collection of values `L(f(a), g(b))` — ranging over all pairs `(a, b)` in the monoid `M` whose product `a * b` equals `x` — forms a summable family in the topological module `F`. When this holds, the convolution sum at `x` converges and can be meaningfully evaluated.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ConvolutionExistsAt : {M : Type u_1} -> {S : Type u_2} -> {E : Type u_3} -> {E' : Type u_4} -> {F : Type u_6} -> [Monoid M] -> [CommSemiring S] -> [AddCommMonoid E] -> [AddCommMonoid E'] -> [AddCommMonoid F] -> [Module S E] -> [Module S E'] -> [Module S F] -> [TopologicalSpace F] -> (L : E →ₗ[S] E' →ₗ[S] F) -> (f : M → E) -> (g : M → E') -> (x : M) -> Prop
<!-- PINNED-SIGNATURE:END -->


`(L : E →ₗ[S] E' →ₗ[S] F)` is the bilinear map (given as a curried `S`-linear map) that pairs values of `f` with values of `g` to produce elements of the output module `F`. `(f : M → E)` is the first function being convolved, taking values in the left module `E`. `(g : M → E')` is the second function being convolved, taking values in the right module `E'`. `(x : M)` is the specific element of the monoid at which convolution existence is being tested: one asks whether the fiber sum over all factorizations of `x` as a product `a * b` is summable.

### Conventions

There are no declared junk-value or edge-case conventions for this definition: it is a `Prop`-valued predicate that is simply `False` (not satisfied) whenever the relevant fiber sum is not summable, and no special behavior is assigned to degenerate or boundary inputs beyond what the general definition of summability provides.

### Worked examples

- Claim: If `f` and `g` are finitely supported functions on a monoid `M` and `L` is any continuous bilinear map, then `VTask.ConvolutionExistsAt L f g x` holds for every `x`, because the fiber over any `x` involves only finitely many nonzero terms and any finite sum is summable.

- Claim: For the monoid `ℕ` under addition and `L` the scalar multiplication `S →ₗ[S] S →ₗ[S] S`, if `f n = (1/2)^n` and `g n = (1/3)^n` (as real-valued sequences), then `VTask.ConvolutionExistsAt L f g x` holds for every `x : ℕ`, since the fiber sum over pairs `(a, b)` with `a + b = x` is finite (exactly `x + 1` terms) and hence summable.

- Claim: `VTask.ConvolutionExistsAt L f g x` is preserved under scalar multiplication of `f`: if `VTask.ConvolutionExistsAt L f g x` holds, then so does `VTask.ConvolutionExistsAt L (c • f) g x` for any scalar `c : S`, because scaling by a constant preserves summability.

- Claim: `VTask.ConvolutionExistsAt L f g x` is additive in `g`: if `VTask.ConvolutionExistsAt L f g x` and `VTask.ConvolutionExistsAt L f g' x` both hold, then so does `VTask.ConvolutionExistsAt L f (g + g') x`.

### Boundaries

- If `x` has an empty fiber (no pairs `(a, b)` with `a * b = x`) — which cannot happen in a monoid since at least the pair is possible, but structurally the empty sum is summable — then `VTask.ConvolutionExistsAt L f g x` holds trivially.
- When `M` is a finite monoid, the fiber over any `x` is finite, so `VTask.ConvolutionExistsAt L f g x` holds for all `f`, `g`, `x`, and `L`.
- The predicate does not require any continuity of `L`; summability of the fiber sum is purely algebraic/topological in `F` and does not depend on properties of `L` beyond its definition.
- The proposition may fail — be `False` — when `f` or `g` decay too slowly, causing the terms `L(f(a), g(b))` to be non-summable over the (potentially infinite) fiber.

### Not to be confused with

- `ConvolutionExists`: the global version asserting that the convolution exists at *every* point `x : M`, not just a single specified point.
- `Summable`: the underlying summability predicate over an arbitrary index type; `VTask.ConvolutionExistsAt` is specifically summability indexed by the multiplicative fiber `{(a, b) : M × M | a * b = x}`.
- The continuous convolution `MeasureTheory.convolution`: an integral-based convolution for functions on locally compact groups, entirely different from this discrete sum-based notion.