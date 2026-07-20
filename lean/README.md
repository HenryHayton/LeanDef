# lean/definition_verifier

Lean 4 subproject: pinned toolchain, Mathlib dependency, and (later) hand-built tasks.

- `lean-toolchain` pins the exact Lean version.
- `lakefile.toml` pins Mathlib to an exact release tag (see repo-root README "Pinned versions").
- `DefinitionVerifier/` is the library source.

Build with:

```sh
lake exe cache get   # fetch prebuilt Mathlib .olean cache (do this before lake build)
lake build
```
