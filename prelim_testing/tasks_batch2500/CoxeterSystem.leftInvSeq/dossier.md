## Object

The **left inversion sequence** of a word $\omega = [i_1, i_2, \ldots, i_\ell]$ (a list of Coxeter generator indices) is the list of group elements
$$s_{i_1},\quad s_{i_1}s_{i_2}s_{i_1},\quad s_{i_1}s_{i_2}s_{i_3}s_{i_2}s_{i_1},\quad \ldots,\quad s_{i_1}\cdots s_{i_\ell}\cdots s_{i_1}.$$
Each entry is obtained by conjugating the $k$-th generator $s_{i_k}$ by the prefix $s_{i_1}\cdots s_{i_{k-1}}$. These elements are reflections in the Coxeter group $W$, and the left inversion sequence encodes the set of left inversions of the group element represented by $\omega$.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.leftInvSeq : {B : Type u_1} -> {W : Type u_2} -> [Group W] -> {M : CoxeterMatrix B} -> (cs : CoxeterSystem M W) -> (ω : List B) -> List W
<!-- PINNED-SIGNATURE:END -->


VTask.leftInvSeq : {B : Type u_1} -> {W : Type u_2} -> [Group W] -> {M : CoxeterMatrix B} -> (cs : CoxeterSystem M W) -> (ω : List B) -> List W

`B` is the type indexing the Coxeter generators (the "alphabet"). `W` is the Coxeter group, which carries a `Group` instance. `M` is the Coxeter matrix specifying the relations among generators. `cs` is the Coxeter system structure, which packages the group $W$ together with its presentation by generators and relations given by `M`. `ω` is the word whose left inversion sequence is to be computed: a list of generator indices from `B`.

## Conventions

The left inversion sequence of the empty word is the empty list. No junk values arise for well-typed inputs because the function is total over all lists `ω : List B`.

## Worked examples

- Claim: For the empty word, `VTask.leftInvSeq cs []` returns `[]` for any Coxeter system `cs`.
  ```lean
  example {B W : Type*} [Group W] {M : CoxeterMatrix B} (cs : CoxeterSystem M W) :
      VTask.leftInvSeq cs [] = [] := rfl
  ```

- Claim: For a single-letter word `[i]`, `VTask.leftInvSeq cs [i]` is the singleton list `[cs.simple i]` (i.e., the generator itself), since conjugating by the empty prefix is the identity.
  ```lean
  example {B W : Type*} [Group W] {M : CoxeterMatrix B} (cs : CoxeterSystem M W) (i : B) :
      VTask.leftInvSeq cs [i] = [cs.simple i] := rfl
  ```

- Claim: The length of `VTask.leftInvSeq cs ω` equals the length of `ω`, for any word `ω`.

- Claim: For a two-letter word `[i, j]`, `VTask.leftInvSeq cs [i, j]` equals `[cs.simple i, cs.simple i * cs.simple j * cs.simple i]`, where the second entry is `s_i` conjugated by $s_i$, followed by $s_j$ conjugated by $s_i$... concretely, `[s i, s i * s j * s i]`.

## Boundaries

- **Empty word**: `VTask.leftInvSeq cs [] = []`. The sequence has no entries.
- **Single letter**: `VTask.leftInvSeq cs [i] = [cs.simple i]`. The unique entry is the generator $s_i$ itself.
- **Reduced words**: For a reduced word $\omega$, the entries of the left inversion sequence are pairwise distinct reflections, and their set equals the left inversion set of the group element $w = s_{i_1}\cdots s_{i_\ell}$.
- **Non-reduced words**: For non-reduced $\omega$, the left inversion sequence may contain repeated elements; in particular, if two consecutive entries coincide, this signals a deletion opportunity.
- **Length**: The output list always has the same length as the input list `ω`.

## Not to be confused with

- **Right inversion sequence**: The analogous sequence using right conjugation/prefixes from the right; the ordering and conjugating elements differ.
- **Inversion set**: The *set* (not sequence) of reflections that are inversions of a group element $w$; the left inversion sequence records these with multiplicity and in order tied to the chosen word.
- **`CoxeterSystem.wordProd`**: The product $s_{i_1}\cdots s_{i_\ell}$ of generators in a word, which collapses the word to a single group element rather than producing a list of conjugated generators.