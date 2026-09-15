## VTask.eqLocus

### Object

Given two ring homomorphisms `f` and `g` from a ring `R` to a semiring `S`, the **equalizer locus** (or **equalizer subring**) is the set of all elements `x` in `R` for which `f(x) = g(x)`. This set is closed under the ring operations of `R` and therefore forms a subring of `R`. It is the largest subring of `R` on which `f` and `g` agree.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.eqLocus : {R : Type u} -> [NonAssocRing R] -> {S : Type v} -> [Semiring S] -> (f g : R →+* S) -> Subring R
<!-- PINNED-SIGNATURE:END -->


`{R : Type u} -> [NonAssocRing R] -> {S : Type v} -> [Semiring S] -> (f g : R →+* S) -> Subring R`

The implicit type `R` is the source ring (required to be a non-associative ring), and `S` is the target type (required to be a semiring). The instance arguments supply the ring and semiring structures respectively. The two explicit arguments `f` and `g` are the ring homomorphisms being compared: `f` is the first homomorphism and `g` is the second. The result is a subring of `R`.

### Conventions

No special junk-value or edge-case conventions are declared for this definition: the construction is well-defined for any two ring homomorphisms between the given algebraic structures, and the equalizer is always a valid subring (possibly trivial, possibly all of `R`).

### Worked examples

- Claim: For any ring `R` and any single ring homomorphism `f : R →+* S`, every element of `R` belongs to `VTask.eqLocus f f`, since `f x = f x` trivially.

- Claim: If `f` and `g` are ring homomorphisms from `ℤ` to `ℤ` and `f` is the identity while `g` is the zero map, then `VTask.eqLocus f g` contains exactly `0`, because `f(x) = x` and `g(x) = 0` agree only when `x = 0`.

- Claim: For any two ring homomorphisms `f g : R →+* S`, the element `0 : R` always belongs to `VTask.eqLocus f g`, since both `f` and `g` send `0` to `0` (as ring homomorphisms preserve zero).

- Claim: For any two ring homomorphisms `f g : R →+* S`, the element `1 : R` always belongs to `VTask.eqLocus f g`, since both `f` and `g` send `1` to `1` (as ring homomorphisms preserve one).

### Boundaries

- **When `f = g`**: The equalizer locus is all of `R`, i.e., `VTask.eqLocus f f = ⊤` as a subring.
- **When `f` and `g` differ everywhere except at `0` and `1`**: The equalizer locus is the trivial subring `{0, 1}` (or possibly larger if the ring has characteristic 0 vs. positive characteristic considerations force more coincidences).
- **Zero and one always belong**: Since every ring homomorphism preserves `0` and `1`, both `0` and `1` are always members of the equalizer locus regardless of `f` and `g`.
- **The equalizer locus is a subring, not merely a subset**: It is closed under addition, subtraction (negation), and multiplication, inheriting these from `R`.
- **Monotonicity**: If one pair of homomorphisms agrees on a larger set than another pair, the corresponding equalizer locus is larger as a subring.

### Not to be confused with

- **`RingHom.ker f`**: The kernel is the set `{x | f x = 0}`, a single homomorphism compared to zero, while the equalizer locus compares two homomorphisms to each other.
- **`MonoidHom.eqLocusM`**: The equalizer of two monoid homomorphisms, which yields a submonoid rather than a subring; `VTask.eqLocus` refines this to a full subring structure.
- **`AddMonoidHom.eqLocus`**: The equalizer of two additive monoid homomorphisms, yielding an additive submonoid; again `VTask.eqLocus` combines both the multiplicative and additive equalizer data into a subring.
