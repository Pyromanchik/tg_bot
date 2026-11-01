"""Tests for filename formatting and caption drawing."""

from __future__ import annotations

from datetime import datetime
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PIL import Image

from bot.image_processor import draw_caption, make_image_filename, save_user_image

FONT_PATH = Path(__file__).resolve().parents[1] / "fonts" / "Lobster-Regular.ttf"


def _jpeg_bytes(size: tuple[int, int] = (400, 300), color: str = "skyblue") -> bytes:
    image = Image.new("RGB", size, color=color)
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_make_image_filename() -> None:
    when = datetime(2026, 11, 1, 15, 7)
    assert make_image_filename(42, when=when) == "2026-11-01_15:07_42.jpg"


def test_save_user_image_uses_required_name(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import bot.image_processor as module

    fixed = datetime(2026, 11, 1, 9, 5)

    class FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):  # noqa: ANN001
            return fixed

    monkeypatch.setattr(module, "datetime", FixedDatetime)

    written: dict[str, bytes] = {}

    def fake_write_bytes(self: Path, data: bytes) -> int:  # noqa: ANN001
        written["name"] = self.name
        written["data"] = data
        return len(data)

    monkeypatch.setattr(Path, "write_bytes", fake_write_bytes)
    monkeypatch.setattr(Path, "mkdir", MagicMock())

    path = save_user_image(_jpeg_bytes(), tmp_path, user_id=1001)

    assert path.name == "2026-11-01_09:05_1001.jpg"
    assert written["name"] == "2026-11-01_09:05_1001.jpg"
    assert written["data"]


def test_draw_caption_returns_jpeg() -> None:
    result = draw_caption(_jpeg_bytes(), "Тестовая подпись", FONT_PATH)

    with Image.open(BytesIO(result)) as image:
        assert image.format == "JPEG"
        assert image.size == (400, 300)


def test_font_file_exists() -> None:
    assert FONT_PATH.is_file()
