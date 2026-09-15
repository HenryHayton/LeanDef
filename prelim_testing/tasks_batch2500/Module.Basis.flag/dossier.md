## VTask.flag

### Object

Given a finite basis `b` of a module `M` over a semiring `R`, indexed by `Fin n`, and a cut-point `k` in `Fin (n + 1)`, `VTask.flag b k` is the submodule of `M` spanned by the first `k` basis vectors — that is, those basis vectors `b i` for which the index `i` (viewed in `Fin (n + 1)`) is strictly less than `k`. When `k = 0` this is the zero submodule; when `k = n` (the largest element of `Fin (n + 1)`) this is all of `M`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.flag : {R : Type u_1} -> {M : Type u_2} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> {n : ℕ} -> (b : Module.Basis (Fin n) R M) -> (k : Fin (n + 1)) -> Submodule R M
<!-- PINNED-SIGNATURE:END -->


The first argument `b` is a basis of `M` over `R` indexed by `Fin n`; it supplies both the indexing structure and the distinguished spanning vectors. The second argument `k : Fin (n + 1)` is the cut-point: only those basis vectors whose (coerced) index is strictly less than `k` are included in the span.

### Conventions

When `k = 0` (the smallest element of `Fin (n + 1)`), no basis vectors satisfy the strict-inequality condition, so the image set is empty and `VTask.flag b k` is the zero submodule `⊥`.

### Worked examples

- Claim: For the standard basis of `Fin 3 → ℚ`, `VTask.flag b 0 = ⊥` (the zero submodule), because no basis vectors are included.

- Claim: For the standard basis `b` of `Fin 3 → ℚ` indexed by `Fin 3`, `VTask.flag b 2` is the span of the first two standard basis vectors `e₀` and `e₁`, hence isomorphic to `ℚ²` sitting inside `ℚ³`.

- Claim: `VTask.flag b k ≤ VTask.flag b l` whenever `k ≤ l` as elements of `Fin (n + 1)`, because the set of indices satisfying `i < k` is a subset of those satisfying `i < l`, so the corresponding spans are nested.

- Claim: For the standard basis of `Fin n → ℚ`, `VTask.flag b ⟨n, Nat.lt_succ_self n⟩` equals `⊤` (the whole module), since all `n` basis vectors are included.

### Boundaries

- At `k = 0`: the condition `i.castSucc < 0` is never satisfied in `Fin (n + 1)`, so the span is over the empty set, yielding the zero submodule `⊥`.
- At `k = n` (top of `Fin (n + 1)`): all basis vectors are included, so the span equals the whole module `⊤`.
- The definition is total: it is well-typed for every `k : Fin (n + 1)`, including the extremes.
- When `n = 0`, there is only one value `k = 0` in `Fin 1`, and the submodule is `⊥ = ⊤ = M` (which is the zero module).

### Not to be confused with

- `Module.Basis.span` applied to an arbitrary set of basis indices — `VTask.flag` specifically takes an initial segment `{i | i < k}`, giving a canonical filtration (flag) structure.
- A complete flag variety in algebraic geometry, which parametrises all such nested chains; `VTask.flag b k` is a single member of such a chain, not the chain itself.
- `Submodule.span R (Set.range b)` — that is the span of *all* basis vectors and equals `⊤`; `VTask.flag b k` takes only an initial segment.