"""Load and pick random captions from a text file."""

from __future__ import annotations

import random
from pathlib import Path


def load_captions(path: str | Path) -> list[str]:
    """Read non-empty lines from the captions file."""
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Captions file not found: {file_path}")

    lines = [
        line.strip()
        for line in file_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not lines:
        raise ValueError(f"Captions file is empty: {file_path}")
    return lines


def pick_random_caption(captions: list[str], rng: random.Random | None = None) -> str:
    """Return a random caption from the list."""
    if not captions:
        raise ValueError("Captions list is empty")
    chooser = rng if rng is not None else random
    return chooser.choice(captions)
