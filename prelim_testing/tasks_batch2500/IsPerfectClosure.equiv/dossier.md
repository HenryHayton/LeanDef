## Object

Given a commutative ring `K` and two perfect closures of `K` — namely `L` (via ring map `i : K →+* L`) and `M` (via ring map `j : K →+* M`) — `VTask.equiv i j p` is the canonical ring isomorphism `L ≃+* M`. It expresses the fact that the perfect closure of a ring is unique up to isomorphism: any two rings that each satisfy the universal property of the perfect closure of `K` (with respect to the same characteristic exponent `p`) are canonically isomorphic as rings over `K`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.equiv : {K : Type u_1} -> {L : Type u_2} -> {M : Type u_3} -> [CommRing K] -> [CommRing L] -> [CommRing M] -> (i : K →+* L) -> (j : K →+* M) -> (p : ℕ) -> [ExpChar M p] -> [ExpChar K p] -> [ExpChar L p] -> [PerfectRing L p] -> [IsPerfectClosure i p] -> [PerfectRing M p] -> [IsPerfectClosure j p] -> L ≃+* M
<!-- PINNED-SIGNATURE:END -->


`VTask.equiv : {K : Type u_1} -> {L : Type u_2} -> {M : Type u_3} -> [CommRing K] -> [CommRing L] -> [CommRing M] -> (i : K →+* L) -> (j : K →+* M) -> (p : ℕ) -> [ExpChar M p] -> [ExpChar K p] -> [ExpChar L p] -> [PerfectRing L p] -> [IsPerfectClosure i p] -> [PerfectRing M p] -> [IsPerfectClosure j p] -> L ≃+* M`

The implicit type arguments `K`, `L`, `M` are the commutative rings in question, with `CommRing` instances supplied automatically. The argument `i` is the ring homomorphism from the base ring `K` into the first candidate perfect closure `L`; it witnesses that `L` is a perfect closure of `K`. The argument `j` is the ring homomorphism from `K` into the second candidate perfect closure `M`; it witnesses that `M` is a perfect closure of `K`. The natural number `p` is the characteristic exponent shared by all three rings (it is `1` in characteristic zero, and the characteristic `p` in characteristic `p > 0`). The typeclass instances `ExpChar` assert that each of `K`, `L`, `M` has characteristic exponent `p`. The instances `PerfectRing L p` and `PerfectRing M p` assert that `L` and `M` are each perfect rings of characteristic exponent `p` (i.e., the Frobenius endomorphism is bijective). The instances `IsPerfectClosure i p` and `IsPerfectClosure j p` assert that `i` and `j` respectively exhibit `L` and `M` as perfect closures of `K` over the prime `p`, meaning they satisfy the appropriate universal property.

## Conventions

There are no junk-value or edge-case output conventions to declare for this construction: the isomorphism is well-defined and canonical whenever all the required hypotheses are satisfied, and the definition is not meaningfully invoked outside that regime.

## Worked examples

- Claim: When `L` and `M` are both perfect closures of `K`, the forward direction of `VTask.equiv i j p` is a ring homomorphism `L →+* M` that is compatible with the structure maps from `K`.

- Claim: When `L` and `M` are both perfect closures of `K`, the composition `(VTask.equiv i j p).symm.trans (VTask.equiv i j p)` is the identity isomorphism on `L`.

- Claim: For any element `x : L`, applying `(VTask.equiv i j p).symm` after `VTask.equiv i j p` returns `x`; that is, the isomorphism is self-inverse in the sense that its forward and backward maps are mutual inverses.

## Boundaries

- When `K`, `L`, and `M` all coincide (e.g., `K` is already perfect and `i = j = id`), `VTask.equiv i j p` reduces to an automorphism of the perfect ring, which must be the identity (by uniqueness of the universal property map).
- The construction is only meaningful when `p` genuinely is the characteristic exponent of `K`, `L`, and `M`; the `ExpChar` instances enforce this automatically and prevent mismatched primes.
- There is no restriction on the specific value of `p` beyond it being a valid characteristic exponent (either `1` or a prime); the isomorphism is produced in both the characteristic-zero case (`p = 1`) and the positive-characteristic case.

## Not to be confused with

- `IsAlgClosure.equiv`: the analogous canonical isomorphism for algebraic closures, not perfect closures.
- `IsSepClosure.equiv`: the analogous canonical isomorphism for separable closures, not perfect closures.
- `PerfectRing.lift`: the underlying ring homomorphism `L →+* M` used to build `VTask.equiv`; it goes only one way and is not the full isomorphism.