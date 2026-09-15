## Object

Given two non-unital ring homomorphisms `f` and `g` from `R` to `S`, `VTask.eqLocus f g` is the **equalizer subring**: the set of all elements `x` of `R` for which `f x = g x`, equipped with the structure of a `NonUnitalSubring` of `R`. Algebraically, it is the largest subring of `R` on which `f` and `g` agree.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.eqLocus : {R : Type u} -> {S : Type v} -> [NonUnitalNonAssocRing R] -> [NonUnitalNonAssocRing S] -> (f g : R →ₙ+* S) -> NonUnitalSubring R
<!-- PINNED-SIGNATURE:END -->


`VTask.eqLocus : {R : Type u} -> {S : Type v} -> [NonUnitalNonAssocRing R] -> [NonUnitalNonAssocRing S] -> (f g : R →ₙ+* S) -> NonUnitalSubring R`

The universe-polymorphic types `R` and `S` are inferred automatically; they carry non-unital non-associative ring structures supplied by the two instance arguments. The first explicit argument `f` is one non-unital ring homomorphism from `R` to `S`; the second explicit argument `g` is another non-unital ring homomorphism from `R` to `S`. The result is the subring of `R` formed by all points where `f` and `g` coincide.

## Conventions

No junk-value or boundary conventions are declared for this definition: it is a total construction whose carrier is a well-defined subset of `R` for every pair of homomorphisms, including the case `f = g` (which yields all of `R`) and the case where the two maps agree nowhere except at `0` (which yields the trivial subring `{0}`).

## Worked examples

- Claim: The zero element `0 : R` always belongs to `VTask.eqLocus f g`, because any non-unital ring homomorphism sends `0` to `0`.

- Claim: If `f = g`, then every element of `R` belongs to `VTask.eqLocus f g`, so the equalizer locus equals the whole ring `R` (as a `NonUnitalSubring`).

- Claim: For the two ring homomorphisms `f, g : ℤ →ₙ+* ℤ` defined by `f = id` and `g = id`, the equalizer locus is all of `ℤ`.

- Claim: If `x` belongs to `VTask.eqLocus f g` and `y` belongs to `VTask.eqLocus f g`, then `x + y` belongs to `VTask.eqLocus f g`, since `f (x + y) = f x + f y = g x + g y = g (x + y)`.

## Boundaries

- When `f` and `g` are identical homomorphisms, the equalizer locus is the entire ring `R`.
- When `f` and `g` agree only at `0`, the equalizer locus is the trivial subring `{0}`.
- Because `R` is only required to be a non-unital non-associative ring, there is no multiplicative identity, and the equalizer locus need not contain a unit element — it is a `NonUnitalSubring`, not a `Subring`.
- The construction is symmetric in a limited sense: in general `VTask.eqLocus f g` and `VTask.eqLocus g f` have the same underlying set (both are `{x | f x = g x}`), but Lean may distinguish the two as terms.

## Not to be confused with

- `NonUnitalRingHom.ker f`: the kernel of a single homomorphism, which is the equalizer of `f` with the zero map — a special case of the equalizer locus.
- `RingHom.eqLocus f g`: the analogous construction for unital ring homomorphisms; it lives in the category of `Subring`s and requires a unital ring structure.
- `NonUnitalSubring.center R`: the center of `R` as a non-unital subring, an entirely different subobject unrelated to a pair of homomorphisms.