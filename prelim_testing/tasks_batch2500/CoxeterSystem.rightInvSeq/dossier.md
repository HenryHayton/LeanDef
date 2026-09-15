## Object

The **right inversion sequence** of a word $\omega = [i_1, i_2, \ldots, i_\ell]$ in a Coxeter system $(W, S)$ is the finite list of group elements
$$
  s_{i_\ell}\cdots s_{i_2} s_{i_1} s_{i_2}\cdots s_{i_\ell},\quad
  \ldots,\quad
  s_{i_\ell} s_{i_{\ell-1}} s_{i_\ell},\quad
  s_{i_\ell}
$$
obtained by reading the word from left to right and, for each prefix $[i_1, \ldots, i_k]$, conjugating the generator $s_{i_k}$ by the product of all later generators $s_{i_{k+1}}\cdots s_{i_\ell}$.  More precisely, the $k$-th entry (0-indexed from the front) is $(\pi[i_{k+1},\ldots,i_\ell])^{-1}\cdot s_{i_k}\cdot \pi[i_{k+1},\ldots,i_\ell]$, where $\pi$ denotes the product map sending a list of indices to the corresponding product in $W$.  The sequence has the same length as $\omega$.

The right inversion sequence encodes the set of inversions of the group element represented by $\omega$ relative to right multiplication; when $\omega$ is a reduced word, its entries are exactly the right inversions (reflections) of the corresponding element of $W$, listed in a canonical order.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.rightInvSeq : {B : Type u_1} -> {W : Type u_2} -> [Group W] -> {M : CoxeterMatrix B} -> (cs : CoxeterSystem M W) -> (ω : List B) -> List W
<!-- PINNED-SIGNATURE:END -->


VTask.rightInvSeq : {B : Type u_1} -> {W : Type u_2} -> [Group W] -> {M : CoxeterMatrix B} -> (cs : CoxeterSystem M W) -> (ω : List B) -> List W

`B` is the type of generator labels (the index set of the Coxeter matrix). `W` is the Coxeter group, which carries a `Group` instance. `M` is the Coxeter matrix specifying the relations among generators. `cs` is the Coxeter system structure that ties `M` to `W` and provides the generators $s_i$ and the word-product map $\pi$. `ω` is the word over the index set `B` whose right inversion sequence is being computed; it is a list of generator labels.

## Conventions

The right inversion sequence of the empty word is the empty list; no junk value is needed there. The sequence is ordered so that the entry corresponding to the **first** generator of $\omega$ (i.e. $i_1$) appears **first** in the output list, conjugated by all remaining generators $s_{i_2}\cdots s_{i_\ell}$, and the entry for the **last** generator $i_\ell$ is $s_{i_\ell}$ itself, placed **last**.

## Worked examples

- Claim: For the empty word `[]`, `VTask.rightInvSeq cs [] = []` for any Coxeter system `cs`.

- Claim: For a single-letter word `[i]`, `VTask.rightInvSeq cs [i] = [cs.simple i]`. The tail is empty, so the product $\pi[\,]$ is the identity, and the sole entry is $1^{-1}\cdot s_i\cdot 1 = s_i$.

- Claim: For a two-letter word `[i, j]`, `VTask.rightInvSeq cs [i, j] = [cs.simple j * cs.simple i * cs.simple j, cs.simple j]`. The first entry conjugates $s_i$ by $\pi[j] = s_j$, giving $s_j^{-1} s_i s_j = s_j s_i s_j$ (since $s_j$ is an involution); the second entry is $s_j$ itself.

- Claim: The length of `VTask.rightInvSeq cs ω` equals the length of `ω` for any word `ω`.

## Boundaries

- **Empty word**: `VTask.rightInvSeq cs [] = []`. The sequence is empty, consistent with the recursive definition's base case.
- **Length preservation**: The output list always has exactly the same number of elements as the input list `ω`, since each recursive step prepends exactly one element.
- **Single generator**: For `ω = [i]`, the sole entry is `cs.simple i` (conjugation by the identity).
- **Involution entries**: Each entry in the right inversion sequence is a reflection in $W$ (a conjugate of a generator). If $\omega$ is a reduced word these are pairwise distinct; for non-reduced words repetitions may occur.
- **Non-reduced words**: The definition is valid for arbitrary words, not only reduced ones; the algebraic formula applies uniformly.

## Not to be confused with

- **`CoxeterSystem.leftInvSeq`**: The analogous sequence conjugating generators by prefixes rather than suffixes, yielding a list ordered in the opposite direction.
- **`CoxeterSystem.wordProd` (`π`)**: The single group element obtained by multiplying all generators in the word; the right inversion sequence is a *list* of elements, not a single product.
- **The inversion set of a group element**: A set (not a list, and independent of the choice of word); the right inversion sequence of a reduced word *enumerates* this set but as an ordered list depending on the word.