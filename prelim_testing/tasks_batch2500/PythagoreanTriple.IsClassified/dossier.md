## VTask.IsClassified

### Object

A predicate on a Pythagorean triple $(x, y, z)$ — that is, a triple of integers satisfying $x^2 + y^2 = z^2$ — asserting that the triple admits the classical parametric description. Specifically, the triple is *classified* if there exist integers $k$, $m$, $n$ with $\gcd(m, n) = 1$ such that, in some order, one of $x, y$ equals $k(m^2 - n^2)$ and the other equals $k(2mn)$. This captures the standard number-theoretic characterisation of all integer Pythagorean triples.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsClassified : {x y z : ℤ} -> PythagoreanTriple x y z → Prop
<!-- PINNED-SIGNATURE:END -->


The implicit arguments $x$, $y$, $z$ are the three integers constituting the Pythagorean triple, fixed by the explicit argument. The explicit argument is a proof that $x$, $y$, $z$ actually form a Pythagorean triple (i.e., a term of type `PythagoreanTriple x y z`); `VTask.IsClassified` is stated as a predicate on that proof object, though its content depends only on the values $x$ and $y$.

### Conventions

The coprimality condition $\gcd(m, n) = 1$ is part of the definition: the witnessing integers $m$ and $n$ must be coprime. The scalar $k$ is allowed to be any integer, including zero or negative. The two legs $x$ and $y$ may be assigned to either of the two parametric forms $k(m^2 - n^2)$ and $k(2mn)$ in either order, so the predicate is symmetric in $x$ and $y$.

### Worked examples

- Claim: Every Pythagorean triple is classified — for any `h : PythagoreanTriple x y z`, `h.IsClassified` holds. This is the content of the global classification theorem `PythagoreanTriple.classified`.

- Claim: The standard triple $(3, 4, 5)$ is classified: take $k = 1$, $m = 2$, $n = 1$, giving $k(m^2 - n^2) = 3$ and $k(2mn) = 4$, with $\gcd(2,1) = 1$.

- Claim: The triple $(5, 12, 13)$ is classified: take $k = 1$, $m = 3$, $n = 2$, giving $k(m^2 - n^2) = 5$ and $k(2mn) = 12$, with $\gcd(3,2) = 1$.

- Claim: If `h : PythagoreanTriple x y z` is classified and $k$ is any integer, then `(h.mul k).IsClassified` holds, by `PythagoreanTriple.mul_isClassified`.

### Boundaries

- When $k = 0$, the witnesses give $x = 0$ and $y = 0$ (and hence $z = 0$), so the zero triple $(0, 0, 0)$ is trivially classified.
- The coprimality requirement $\gcd(m, n) = 1$ is on the *witnesses* only; it does not restrict which triples can be classified — every Pythagorean triple is classified regardless.
- Negative values of $k$, $m$, or $n$ are all permitted; in particular, $m^2 - n^2$ can be negative.
- The roles of $x$ and $y$ are interchangeable by design: both orderings $(x = k(m^2-n^2), y = k(2mn))$ and $(x = k(2mn), y = k(m^2-n^2))$ are accepted, but $z$ does not appear in the parametric equations.

### Not to be confused with

- `PythagoreanTriple.IsPrimitiveClassified`: a strictly stronger predicate requiring additionally that $\gcd(x, y, z) = 1$ (the triple itself is primitive), with its own witness conditions; every primitive classified triple is classified, but not conversely.
- `PythagoreanTriple`: the underlying type asserting merely $x^2 + y^2 = z^2$, with no parametric structure.
- The parametric family without the coprimality constraint on $m, n$: dropping $\gcd(m,n)=1$ would give a weaker (and different) predicate that every triple satisfies for trivial reasons.