"""Miner configuration.

`TARGET_MODULES` is the config list of Mathlib corners scanned by this first harvest batch --
easily widened later, not a structural limit of the scanner.
"""

from pathlib import Path

from harness import config as harness_cfg

MATHLIB_ROOT = harness_cfg.LEAN_PROJECT_DIR / ".lake" / "packages" / "mathlib" / "Mathlib"

TARGET_MODULES: list[str] = [
    "Data/Nat",
    "Data/List",
    "Data/Finset",
    "Data/Int",
    "Logic",
]


def target_dirs(mathlib_root: Path | None = None) -> list[Path]:
    mathlib_root = mathlib_root if mathlib_root is not None else MATHLIB_ROOT
    return [mathlib_root / m for m in TARGET_MODULES]
