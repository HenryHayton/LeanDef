## VTask.mapEquivMonic

### Object

This is an equivalence of sets (in fact a bijection of types) between two objects naturally associated to a commutative-algebra pair `R → S` and a natural number `n`:

- On the left: `R`-algebra homomorphisms from the multivariate polynomial ring `R[X₁, …, Xₙ]` (variables indexed by `Fin n`) into `S`.
- On the right: monic univariate polynomials over `S` of degree exactly `n` (the type `MonicDegreeEq S n`).

Informally, this records the classical fact that specifying an `R`-algebra map out of `R[X₁, …, Xₙ]` is the same as choosing a monic degree-`n` polynomial over `S`: one provides the coefficients (below the leading term) freely, while the leading coefficient is forced to be 1. The universal element on the polynomial-ring side is `freeMonic`, the tautological monic polynomial whose non-leading coefficients are the generators `X₁, …, Xₙ`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapEquivMonic : (R : Type u_1) -> (S : Type u_2) -> [CommRing R] -> [CommRing S] -> [Algebra R S] -> (n : ℕ) -> (MvPolynomial (Fin n) R →ₐ[R] S) ≃ Polynomial.MonicDegreeEq S n
<!-- PINNED-SIGNATURE:END -->


```
VTask.mapEquivMonic : (R : Type u_1) -> (S : Type u_2) -> [CommRing R] -> [CommRing S] -> [Algebra R S] -> (n : ℕ) -> (MvPolynomial (Fin n) R →ₐ[R] S) ≃ Polynomial.MonicDegreeEq S n
```

`R` is the base commutative ring; `S` is the target commutative ring equipped with an `R`-algebra structure via the `Algebra R S` instance. The natural number `n` is the degree of the monic univariate polynomial (equivalently, the number of free variables in the multivariate polynomial ring). Together these data determine both sides of the equivalence.

### Conventions

No edge-case junk-value conventions are declared for this definition: it is a total bijection between well-typed objects for every valid input, including `n = 0` (where the algebra-map side consists of choices of a single unit in `S` — namely `1` — and the polynomial side is the single monic polynomial `1` of degree 0).

### Worked examples

- Claim: Applying `VTask.mapEquivMonic R S n` to the composition `g.comp f` yields the image of `VTask.mapEquivMonic R S n f` under `g`, i.e., the forward direction is natural in `S` in the sense that `mapEquivMonic R T n (g.comp f) = (mapEquivMonic R S n f).map g` for any `g : S →ₐ[R] T`.

- Claim: The inverse direction `(VTask.mapEquivMonic R S n).symm` satisfies: for a monic degree-`n` polynomial `p` over `S` and an `R`-algebra map `g : S →ₐ[R] T`, `(mapEquivMonic R T n).symm (p.map g) = g.comp ((mapEquivMonic R S n).symm p)`. This says that mapping `p` along `g` and then taking the inverse corresponds to post-composing the inverse algebra map with `g`.

- Claim: When `n = 0`, the only monic degree-0 polynomial over `S` is the constant polynomial `1`, and the only `R`-algebra map from `R[]` (the polynomial ring in zero variables, isomorphic to `R`) to `S` is the structure map. The equivalence matches these unique elements.

### Boundaries

- **`n = 0`**: The multivariate polynomial ring `MvPolynomial (Fin 0) R` is isomorphic to `R` itself (no variables), so the only `R`-algebra map to `S` is the structure map `algebraMap R S`. On the other side, `MonicDegreeEq S 0` consists of the single monic polynomial of degree 0 over `S`, which is `1`. The equivalence is well-defined and maps the unique element to the unique element.
- **The leading coefficient**: The equivalence never produces a non-monic polynomial; the `MonicDegreeEq` type enforces that the degree-`n` coefficient is exactly `1` and all higher coefficients vanish. These constraints are verified automatically by the equivalence.
- **Scalar tower compatibility**: When there is a further algebra `T` over `S` (with `S` over `R`), the symm direction interacts with scalar towers via `IsScalarTower`: `(mapEquivMonic R T n).symm (p.map (algebraMap S T)) = (IsScalarTower.toAlgHom R S T).comp ((mapEquivMonic R S n).symm p)`.

### Not to be confused with

- **`MvPolynomial.aeval`**: The raw evaluation map sending a tuple of elements of `S` to an `R`-algebra map; `mapEquivMonic` is a *structured equivalence* packaging these maps bijectively against monic polynomials, not just a single evaluation.
- **`Polynomial.MonicDegreeEq`**: The *type* of monic degree-`n` polynomials over `S`; `mapEquivMonic` is the *equivalence* that identifies this type with algebra maps out of the multivariate polynomial ring.
- **`MvPolynomial.freeMonic`**: The universal (tautological) element on the polynomial side, whose coefficients are the generators; `mapEquivMonic` is the equivalence whose forward map applies any algebra homomorphism to `freeMonic`.