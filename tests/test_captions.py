"""Tests for caption loading and selection."""

from __future__ import annotations

import random
from pathlib import Path

import pytest

from bot.captions import load_captions, pick_random_caption


def test_load_captions(tmp_path: Path) -> None:
    captions_file = tmp_path / "captions.txt"
    captions_file.write_text("первая\n\nвторая\n  третья  \n", encoding="utf-8")

    captions = load_captions(captions_file)

    assert captions == ["первая", "вторая", "третья"]


def test_load_captions_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_captions(tmp_path / "missing.txt")


def test_load_captions_empty_file(tmp_path: Path) -> None:
    empty = tmp_path / "empty.txt"
    empty.write_text("\n\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_captions(empty)


def test_pick_random_caption_deterministic() -> None:
    captions = ["a", "b", "c"]
    rng = random.Random(42)

    assert pick_random_caption(captions, rng=rng) == pick_random_caption(
        captions, rng=random.Random(42)
    )


def test_pick_random_caption_empty() -> None:
    with pytest.raises(ValueError):
        pick_random_caption([])
